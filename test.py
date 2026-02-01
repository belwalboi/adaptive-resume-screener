import torch
from ml.inference.resume_screener import ResumeScreeningModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ResumeScreeningModel(
    model_path="ml/models/resume_net.pt",
    input_dim=7,
    device=device
)

sample = [6, 84.7, 1, 7, 234, 158, 0]
print(model.predict(sample))
