import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from backend.services.model_service import ModelService
from backend.services.prediction_repository import PredictionRepository
from ml.models.resume_net import ResumeNet

logger = logging.getLogger(__name__)


class AdaptiveRetrainer:
    def __init__(
        self,
        registry_path: str | Path,
        models_dir: str | Path,
        retrain_epochs: int = 20,
        min_new_samples: int = 10,
        min_validation_accuracy: float = 0.55,
    ) -> None:
        self.registry_path = Path(registry_path)
        self.models_dir = Path(models_dir)
        self.retrain_epochs = retrain_epochs
        self.min_new_samples = min_new_samples
        self.min_validation_accuracy = min_validation_accuracy
        self._lock = threading.Lock()

    def initialize_registry(self, default_model_path: str) -> str:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        if self.registry_path.exists():
            metadata = self._read_metadata()
            active = str(metadata.get("active_model_path", default_model_path))
            return active

        metadata = {
            "active_model_path": default_model_path,
            "active_model_version": Path(default_model_path).stem,
            "last_trained_feedback_count": 0,
            "last_metrics": {},
            "updated_at": self._now_iso(),
        }
        self._write_metadata(metadata)
        return default_model_path

    def maybe_retrain(
        self,
        repository: PredictionRepository,
        model_service: ModelService,
        minimum_required: int,
    ) -> dict:
        try:
            with self._lock:
                samples = repository.fetch_labeled_samples()
                sample_count = len(samples)

                if sample_count < minimum_required:
                    return {
                        "status": "skipped",
                        "reason": "not_enough_labeled_samples",
                        "sample_count": sample_count,
                    }

                metadata = self._read_metadata()
                last_count = int(metadata.get("last_trained_feedback_count", 0))
                if sample_count - last_count < self.min_new_samples:
                    return {
                        "status": "skipped",
                        "reason": "insufficient_new_samples_since_last_retrain",
                        "sample_count": sample_count,
                        "last_trained_feedback_count": last_count,
                    }

                labels = [label for _, label in samples]
                if len(set(labels)) < 2:
                    return {
                        "status": "skipped",
                        "reason": "requires_both_classes",
                        "sample_count": sample_count,
                    }

                X = torch.tensor([features for features, _ in samples], dtype=torch.float32)
                y = torch.tensor(labels, dtype=torch.float32)

                X_train, X_val, y_train, y_val = self._split_train_validation(X, y)

                trained_model, train_loss = self._train_model(X_train, y_train)
                val_accuracy = self._evaluate_accuracy(trained_model, X_val, y_val)

                if X_val.shape[0] >= 4 and val_accuracy < self.min_validation_accuracy:
                    return {
                        "status": "skipped",
                        "reason": "validation_guardrail_failed",
                        "validation_accuracy": round(val_accuracy, 4),
                        "sample_count": sample_count,
                    }

                version = f"resume_net_feedback_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
                output_path = self.models_dir / f"{version}.pt"
                torch.save(trained_model.state_dict(), output_path)

                model_service.reload(output_path)

                metrics = {
                    "train_loss": round(train_loss, 6),
                    "validation_accuracy": round(val_accuracy, 4),
                    "sample_count": sample_count,
                }
                metadata.update(
                    {
                        "active_model_path": str(output_path),
                        "active_model_version": version,
                        "last_trained_feedback_count": sample_count,
                        "last_metrics": metrics,
                        "updated_at": self._now_iso(),
                    }
                )
                self._write_metadata(metadata)

                logger.info("Adaptive retraining completed: version=%s metrics=%s", version, metrics)
                return {"status": "retrained", "version": version, "metrics": metrics}
        except Exception:
            logger.exception("Adaptive retraining failed")
            return {"status": "failed"}

    def _split_train_validation(self, X: torch.Tensor, y: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        labels = y.int().tolist()
        class0 = labels.count(0)
        class1 = labels.count(1)

        if len(labels) >= 12 and class0 >= 2 and class1 >= 2:
            indices = list(range(len(labels)))
            train_idx, val_idx = train_test_split(
                indices,
                test_size=0.2,
                random_state=42,
                stratify=labels,
            )
            train_idx_tensor = torch.tensor(train_idx, dtype=torch.long)
            val_idx_tensor = torch.tensor(val_idx, dtype=torch.long)
            return X[train_idx_tensor], X[val_idx_tensor], y[train_idx_tensor], y[val_idx_tensor]

        return X, X, y, y

    def _train_model(self, X_train: torch.Tensor, y_train: torch.Tensor) -> tuple[ResumeNet, float]:
        model = ResumeNet(input_dim=6)
        criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

        model.train()
        final_loss = 0.0
        for _ in range(self.retrain_epochs):
            optimizer.zero_grad()
            logits = model(X_train).squeeze(1)
            loss = criterion(logits, y_train)
            loss.backward()
            optimizer.step()
            final_loss = float(loss.item())

        return model, final_loss

    def _evaluate_accuracy(self, model: ResumeNet, X_val: torch.Tensor, y_val: torch.Tensor) -> float:
        model.eval()
        with torch.no_grad():
            probs = torch.sigmoid(model(X_val).squeeze(1))
            preds = (probs >= 0.5).int().cpu().numpy()
            truth = y_val.int().cpu().numpy()
        return float(accuracy_score(truth, preds))

    def _read_metadata(self) -> dict:
        if not self.registry_path.exists():
            return {}
        return json.loads(self.registry_path.read_text(encoding="utf-8"))

    def _write_metadata(self, metadata: dict) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()
