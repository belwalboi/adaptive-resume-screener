import logging
import threading
from pathlib import Path

from ml.inference.resume_screener import ResumeScreeningModel, detect_device

logger = logging.getLogger(__name__)


class ModelService:
    def __init__(self, model_path: str | Path, threshold: float = 0.6, device: str | None = None) -> None:
        self.model_path = Path(model_path)
        self.threshold = threshold
        self.device = detect_device() if device is None else device
        self._model: ResumeScreeningModel | None = None
        self._active_model_path = self.model_path
        self._reload_lock = threading.RLock()

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def active_model_path(self) -> str:
        return str(self._active_model_path)

    @property
    def active_model_version(self) -> str:
        return self._active_model_path.stem

    def load(self, model_path: str | Path | None = None) -> None:
        path = Path(model_path) if model_path is not None else self.model_path
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")

        with self._reload_lock:
            self._model = ResumeScreeningModel(
                model_path=str(path),
                device=self.device,
                threshold=self.threshold,
            )
            self._active_model_path = path
            logger.info("Model loaded successfully from %s on device=%s", path, self.device)

    def reload(self, model_path: str | Path) -> None:
        self.load(model_path=model_path)

    def predict(self, features: list[float]) -> dict:
        with self._reload_lock:
            if self._model is None:
                raise RuntimeError("Model is not loaded")
            return self._model.predict(features)