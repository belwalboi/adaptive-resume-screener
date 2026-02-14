import torch
import torch.nn as nn

from ml.models.resume_net import ResumeNet


def detect_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


class LegacyResumeNet(nn.Module):
    """Compatibility architecture for older saved checkpoints."""

    def __init__(self, input_dim: int = 6) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x):
        return self.net(x)


class ResumeScreeningModel:
    def __init__(self, model_path, device=None, threshold=0.6):
        self.device = detect_device() if device is None else torch.device(device)
        self.threshold = threshold

        state_dict = self._safe_load_state_dict(model_path, self.device)
        self.model = self._build_model_for_checkpoint(state_dict).to(self.device)
        self.model.load_state_dict(state_dict, strict=True)
        self.model.eval()

    @staticmethod
    def _safe_load_state_dict(model_path, map_location):
        try:
            checkpoint = torch.load(model_path, map_location=map_location, weights_only=True)
        except TypeError:
            checkpoint = torch.load(model_path, map_location=map_location)

        if isinstance(checkpoint, dict) and "state_dict" in checkpoint and isinstance(checkpoint["state_dict"], dict):
            return checkpoint["state_dict"]
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint and isinstance(
            checkpoint["model_state_dict"], dict
        ):
            return checkpoint["model_state_dict"]
        if isinstance(checkpoint, dict):
            return checkpoint

        raise ValueError("Unsupported checkpoint format; expected state_dict dictionary")

    @staticmethod
    def _build_model_for_checkpoint(state_dict):
        # Legacy checkpoints contain a deeper classifier ending with net.10.*.
        if "net.10.weight" in state_dict and "net.8.weight" in state_dict:
            return LegacyResumeNet(input_dim=6)
        return ResumeNet(input_dim=6)

    def predict(self, features):
        if len(features) != 6:
            raise ValueError("Exactly 6 input features are required")

        x = torch.tensor([features], dtype=torch.float32).to(self.device)

        with torch.no_grad():
            prob = torch.sigmoid(self.model(x)).item()

        return {
            "probability": round(float(prob), 4),
            "decision": "shortlist" if prob >= self.threshold else "reject",
            "threshold": self.threshold,
        }
