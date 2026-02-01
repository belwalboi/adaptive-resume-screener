import torch
import torch.nn as nn

class ResumeNet(nn.Module):
    def __init__(self, input_dim=6):
        super().__init__()

        self.register_buffer("mean", torch.tensor(
            [5.0, 60.0, 1.0, 4.0, 400.0, 200.0]
        ))
        self.register_buffer("std", torch.tensor(
            [4.0, 20.0, 0.8, 3.0, 200.0, 150.0]
        ))

        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        x = (x - self.mean) / self.std   # 🔑 normalization INSIDE model
        return self.net(x)
