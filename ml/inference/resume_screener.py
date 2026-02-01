import torch
from ml.models.resume_net import ResumeNet

class ResumeScreeningModel:
    def __init__(self, model_path, device, threshold=0.6):
        self.device = device
        self.threshold = threshold

        self.model = ResumeNet(input_dim=6).to(device)
        self.model.load_state_dict(
            torch.load(model_path, map_location=device)
        )
        self.model.eval()

    def predict(self, features):
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(self.device)

        with torch.no_grad():
            prob = torch.sigmoid(self.model(x)).item()

        return {
            "probability": round(prob, 4),
            "decision": "shortlist" if prob >= self.threshold else "reject",
            "threshold": self.threshold
        }
