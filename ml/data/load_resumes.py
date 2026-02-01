import subprocess
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

print("📥 Downloading resume dataset from Kaggle...")

subprocess.run(
    [
        "kaggle",
        "datasets",
        "download",
        "-d",
        "gauravduttakiit/resume-dataset",
        "-p",
        str(DATA_DIR),
        "--unzip",
    ],
    check=True,
)

# Kaggle dataset contains Resume.csv
csv_path = DATA_DIR / "Resume.csv"
if not csv_path.exists():
    raise FileNotFoundError("Resume.csv not found after Kaggle download")

df = pd.read_csv(csv_path)
df.columns = [c.strip().lower() for c in df.columns]

out_path = DATA_DIR / "resumes.csv"
df.to_csv(out_path, index=False)

print(f"✅ Saved {len(df)} resumes to {out_path}")
print(df.head())
