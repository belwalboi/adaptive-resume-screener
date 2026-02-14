# Adaptive Resume Screener

Industry-oriented full-stack resume screening system with resume upload + job description matching, ATS-style scoring, semantic similarity, model inference, feedback capture, auto-retraining, and Dockerized deployment.

## What This Project Does

- Accepts resume uploads (`.txt`, `.pdf`, `.docx`) and job description text.
- Extracts resume text and computes ATS-oriented signals.
- Computes semantic similarity between resume and job description.
- Derives 6 model features automatically and runs existing trained `ResumeNet`.
- Stores predictions and analysis metadata for feedback-driven adaptive retraining.

## Architecture

- `backend/main.py`: FastAPI app lifecycle and dependency wiring.
- `backend/api/routes.py`: API endpoints (`/health`, `/predict`, `/analyze`, feedback endpoints).
- `backend/services/resume_parser_service.py`: File parsing for TXT/PDF/DOCX.
- `backend/services/resume_analysis_service.py`: ATS scoring, keyword matching, semantic scoring, and feature engineering.
- `ml/inference/resume_screener.py`: Model loading + prediction with checkpoint compatibility.
- `feedback_loop/adaptive_retrainer.py`: Auto-retraining pipeline from labeled feedback with model versioning.
- `database/schema.sql`: SQLite schema for prediction + analysis persistence.
- `frontend/`: Upload-based UI for resume screening workflow.

## API Endpoints

- `GET /health`
- `POST /predict` (legacy/manual features)
- `POST /analyze` (multipart resume upload + job description)
- `POST /feedback/{prediction_id}`
- `GET /feedback/retraining-status`

## Adaptive Retraining

Feedback can trigger retraining automatically in background:

1. Prediction is saved.
2. Reviewer submits label via `/feedback/{prediction_id}`.
3. If threshold and class-balance checks pass, a new model is trained and promoted.
4. New model artifact is saved under `ml/models/registry/`.
5. API hot-reloads the new model without restarting service.

Model registry metadata:
- `ml/models/registry/metadata.json`

## Retraining Threshold Configuration

Retraining behavior is configurable:

- `RETRAIN_MIN_FEEDBACK` (default: `100`)
- `RETRAIN_AUTO_ENABLED` (default: `true`)
- `RETRAIN_EPOCHS` (default: `20`)
- `RETRAIN_MIN_NEW_SAMPLES` (default: `10`)
- `RETRAIN_MIN_VAL_ACCURACY` (default: `0.55`)

Local PowerShell example:

```powershell
$env:RETRAIN_MIN_FEEDBACK = "10"
$env:RETRAIN_AUTO_ENABLED = "true"
$env:RETRAIN_EPOCHS = "10"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Docker example:

```powershell
$env:RETRAIN_MIN_FEEDBACK = "10"
$env:RETRAIN_AUTO_ENABLED = "true"
docker compose up --build
```

## Local Setup (VS Code Terminal)

```powershell
cd D:\Important_Projects\adaptive-resume-screener
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run API Locally

```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs:
- `http://localhost:8000/docs`

## Test API

```powershell
python -m pytest -q
```

## Test `/analyze` Quickly (PowerShell 5.1 Compatible)

```powershell
$response = curl.exe -s -X POST "http://localhost:8000/analyze" `
  -F "resume=@sample_resume.txt;type=text/plain" `
  -F "job_description=Looking for a Python FastAPI engineer with SQL, Docker, and cloud exposure."

$analysis = $response | ConvertFrom-Json
$analysis
```

## Run Full Stack in Docker

```powershell
docker compose up --build
```

Open:
- Backend docs: `http://localhost:8000/docs`
- Frontend app: `http://localhost:3000`

## Optional GPU Runtime

```powershell
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up --build
```

## Model Contract (Preserved)

- Existing model architecture/checkpoint kept as-is.
- Input dimension remains exactly `6`.
- Features are generated internally from resume + JD analysis.

## Known Limitations

- ATS scoring is currently heuristic and should be calibrated with production data.
- Semantic matching currently uses TF-IDF cosine similarity, not transformer embeddings.
- Auto-retraining currently trains only on labeled feedback stored in SQLite; production should add stronger data validation, drift checks, and model approval workflows.
