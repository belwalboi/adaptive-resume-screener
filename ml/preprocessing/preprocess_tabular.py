from pathlib import Path

import pandas as pd
import torch
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = Path("data/raw/ai_resume_screening.csv")
PROCESSED_DIR = Path("data/processed")
FEATURE_COLUMNS = [
    "years_experience",
    "skills_match_score",
    "education_level",
    "project_count",
    "resume_length",
    "github_activity",
]
TARGET_COLUMN = "shortlisted"


def encode_education(value: object) -> float:
    normalized = str(value).strip().lower()

    if any(token in normalized for token in ("phd", "doctorate")):
        return 4.0
    if any(token in normalized for token in ("master", "m.tech", "mba", "ms")):
        return 3.0
    if any(token in normalized for token in ("bachelor", "b.tech", "be", "bs")):
        return 2.0
    if any(token in normalized for token in ("diploma", "associate")):
        return 1.0

    return 0.0


def encode_label(value: object) -> float:
    normalized = str(value).strip().lower()
    return 1.0 if normalized in {"yes", "shortlist", "shortlisted", "1", "true"} else 0.0


def build_feature_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    frame = dataframe.copy()
    frame.columns = [column.strip().lower() for column in frame.columns]

    missing = [column for column in FEATURE_COLUMNS + [TARGET_COLUMN] if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    frame["education_level"] = frame["education_level"].map(encode_education)
    frame[TARGET_COLUMN] = frame[TARGET_COLUMN].map(encode_label)
    return frame


def preprocess_dataset(raw_data_path: Path = RAW_DATA_PATH, output_dir: Path = PROCESSED_DIR) -> dict[str, tuple[int, ...]]:
    frame = pd.read_csv(raw_data_path)
    prepared = build_feature_frame(frame)

    X = prepared[FEATURE_COLUMNS].astype("float32").to_numpy()
    y = prepared[TARGET_COLUMN].astype("float32").to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    torch.save(torch.tensor(X_train, dtype=torch.float32), output_dir / "X_train.pt")
    torch.save(torch.tensor(X_test, dtype=torch.float32), output_dir / "X_test.pt")
    torch.save(torch.tensor(y_train, dtype=torch.float32), output_dir / "y_train.pt")
    torch.save(torch.tensor(y_test, dtype=torch.float32), output_dir / "y_test.pt")

    return {
        "X_train": tuple(X_train.shape),
        "X_test": tuple(X_test.shape),
        "y_train": tuple(y_train.shape),
        "y_test": tuple(y_test.shape),
    }


def main() -> None:
    shapes = preprocess_dataset()
    print("Saved processed tensors to data/processed")
    for name, shape in shapes.items():
        print(f"{name}: {shape}")


if __name__ == "__main__":
    main()
