import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from ml.inference.resume_screener import ResumeScreeningModel
from ml.training.train_model import DEFAULT_THRESHOLD, load_processed_tensors


def main() -> None:
    _, X_test, _, y_test = load_processed_tensors()
    model = ResumeScreeningModel("ml/models/resume_net.pt", device="cpu", threshold=DEFAULT_THRESHOLD)

    with torch.no_grad():
        probabilities = torch.sigmoid(model.model(X_test)).cpu().numpy().reshape(-1)

    labels = y_test.cpu().numpy().reshape(-1).astype(int)
    predictions = (probabilities >= DEFAULT_THRESHOLD).astype(int)

    metrics = {
        "threshold": DEFAULT_THRESHOLD,
        "accuracy": round(float(accuracy_score(labels, predictions)), 4),
        "precision": round(float(precision_score(labels, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(labels, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(labels, predictions, zero_division=0)), 4),
        "test_size": int(labels.shape[0]),
    }
    print(metrics)


if __name__ == "__main__":
    main()
