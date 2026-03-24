from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from ml.models.resume_net import ResumeNet
from ml.preprocessing.preprocess_tabular import preprocess_dataset

PROCESSED_DIR = Path("data/processed")
MODEL_OUTPUT_PATH = Path("ml/models/resume_net.pt")
DEFAULT_THRESHOLD = 0.30


def load_processed_tensors(processed_dir: Path = PROCESSED_DIR) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    required_files = [
        processed_dir / "X_train.pt",
        processed_dir / "X_test.pt",
        processed_dir / "y_train.pt",
        processed_dir / "y_test.pt",
    ]
    if not all(path.exists() for path in required_files):
        preprocess_dataset(output_dir=processed_dir)

    X_train = torch.load(processed_dir / "X_train.pt")
    X_test = torch.load(processed_dir / "X_test.pt")
    y_train = torch.load(processed_dir / "y_train.pt")
    y_test = torch.load(processed_dir / "y_test.pt")
    return X_train, X_test, y_train, y_test


def train_model(epochs: int = 20, learning_rate: float = 1e-3) -> tuple[ResumeNet, float]:
    X_train, _, y_train, _ = load_processed_tensors()

    model = ResumeNet(input_dim=6)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-4)

    model.train()
    final_loss = 0.0
    for _ in range(epochs):
        optimizer.zero_grad()
        logits = model(X_train).squeeze(1)
        loss = criterion(logits, y_train)
        loss.backward()
        optimizer.step()
        final_loss = float(loss.item())

    return model, final_loss


def evaluate_model(model: ResumeNet, threshold: float = DEFAULT_THRESHOLD) -> dict[str, float]:
    _, X_test, _, y_test = load_processed_tensors()

    model.eval()
    with torch.no_grad():
        probabilities = torch.sigmoid(model(X_test).squeeze(1)).cpu().numpy()

    labels = y_test.cpu().numpy().astype(int)
    predictions = (probabilities >= threshold).astype(int)

    return {
        "accuracy": round(float(accuracy_score(labels, predictions)), 4),
        "precision": round(float(precision_score(labels, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(labels, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(labels, predictions, zero_division=0)), 4),
    }


def main() -> None:
    model, final_loss = train_model()
    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), MODEL_OUTPUT_PATH)
    metrics = evaluate_model(model=model)

    print(f"Saved model to {MODEL_OUTPUT_PATH}")
    print(f"Final training loss: {final_loss:.6f}")
    print(f"Evaluation metrics at threshold {DEFAULT_THRESHOLD}: {metrics}")


if __name__ == "__main__":
    main()
