# Adaptive Resume Screener

Adaptive Resume Screener is a college mini-project that evaluates a resume against a job description and returns an explainable shortlist recommendation. The project combines resume parsing, ATS-style heuristic checks, TF-IDF semantic similarity, a PyTorch classification model, SQLite persistence, and a feedback-driven retraining loop.

## Professor-Facing Summary

- **Problem:** Resume screening is time-consuming and often inconsistent when done manually.
- **Goal:** Build a prototype that can compare a resume with a target job description and generate an explainable recommendation.
- **Input:** Resume file (`.txt`, `.pdf`, `.docx`) and job description text.
- **Output:** ATS score, semantic score, extracted features, matched and missing keywords, model probability, and final decision.
- **Core learning areas:** FastAPI, frontend integration, file parsing, feature engineering, PyTorch inference, SQLite persistence, and adaptive ML workflows.

## What The System Does

1. Accepts a resume upload and job description.
2. Extracts readable text from TXT, PDF, or DOCX files.
3. Measures keyword coverage and section completeness for ATS-style scoring.
4. Computes semantic similarity using TF-IDF cosine similarity.
5. Builds 6 structured features for the trained `ResumeNet` model.
6. Blends the model output with the explainable final score for the upload-based screening decision.
7. Accepts reviewed feedback and can trigger adaptive retraining when enough labeled samples are available.

## End-To-End Architecture

```text
Frontend (HTML/CSS/JS)
        |
        v
FastAPI API (`/analyze`, `/feedback`, `/health`)
        |
        +--> ResumeParserService
        |      - TXT / PDF / DOCX text extraction
        |
        +--> ResumeAnalysisService
        |      - keyword coverage
        |      - ATS-style section scoring
        |      - semantic similarity
        |      - 6-feature generation
        |
        +--> ModelService
        |      - loads PyTorch ResumeNet checkpoint
        |      - returns shortlist / reject prediction
        |
        +--> PredictionRepository (SQLite)
               - stores predictions
               - stores explainability metadata
               - stores reviewed labels
               - supports adaptive retraining
```

## Model Features Used By ResumeNet

The neural model uses exactly 6 numeric features:

| Feature | Meaning |
| --- | --- |
| `years_experience` | Maximum detected years of experience |
| `skills_match_score` | Percentage of tracked job keywords found in the resume |
| `education_level` | Encoded education level from diploma to PhD |
| `project_count` | Estimated number of projects mentioned |
| `resume_length` | Length of extracted resume text |
| `github_activity` | Heuristic score based on GitHub and open-source references |

## Current Model Snapshot

- Active default decision threshold: `0.30`
- Threshold is configurable via `MODEL_THRESHOLD`
- Reproducible evaluation command:

```powershell
python -m ml.training.evaluate_model
```

Current saved checkpoint evaluation on the processed holdout set:

| Metric | Value |
| --- | --- |
| Accuracy | `0.6988` |
| Precision | `0.6988` |
| Recall | `1.0000` |
| F1 Score | `0.8227` |
| Test size | `6000` |

This project is a prototype, so these metrics should be treated as a baseline rather than a production-grade benchmark. The threshold is intentionally calibrated for higher recall during demos so suitable resumes are less likely to be rejected too aggressively.

## How To Explain This Project In A Viva

Use this short structure during your demo:

1. **Problem statement:** recruiters need faster and more consistent resume screening.
2. **Approach:** combine interpretable text analysis with a trained ML model.
3. **Pipeline:** upload resume -> parse text -> compute ATS and semantic signals -> create 6 features -> run model -> save result.
4. **Decision logic:** the final upload-based recommendation blends model confidence with the explainable fit score to reduce harsh false rejections.
5. **Adaptive part:** reviewed predictions are stored and can later retrain the model automatically.
6. **Limitation:** this is a prototype and still relies on heuristic text analysis rather than large production datasets or transformer embeddings.

## Demo Flow For The Professor

1. Start the API or Docker stack.
2. Open the frontend in the browser.
3. Upload [`sample_resume.txt`](sample_resume.txt).
4. Paste a job description such as:

```text
Looking for a Python FastAPI engineer with SQL, Docker, GitHub, and cloud exposure.
```

5. Show the professor:
   - the matched and missing keywords
   - the ATS, semantic, and final scores
   - the extracted features used by the model
   - the final shortlist or reject recommendation
6. Mention that predictions are stored and can later be reviewed for feedback-based retraining.

## Important Folders

- `backend/`: FastAPI app, routes, schemas, and service layer
- `frontend/`: Static presentation UI for upload and result visualization
- `ml/models/`: `ResumeNet` architecture and trained checkpoint
- `ml/preprocessing/`: dataset preprocessing script for the 6-feature pipeline
- `ml/training/`: model training and evaluation scripts
- `feedback_loop/`: retraining trigger and adaptive retraining logic
- `database/`: SQLite schema and local database storage
- `notebooks/`: exploratory, training, and evaluation notebooks
- `tests/`: API tests

## Local Setup

```powershell
cd D:\Important_Projects\adaptive-resume-screener
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run The Backend Locally

```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- Swagger docs: `http://localhost:8000/docs`

## Run The Full Stack With Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open:

- Frontend app: `http://localhost:3000`
- Backend docs: `http://localhost:8000/docs`

## Reproduce The ML Pipeline

Prepare tensors from the raw dataset:

```powershell
python -m ml.preprocessing.preprocess_tabular
```

Train and save a new model checkpoint:

```powershell
python -m ml.training.train_model
```

Evaluate the current saved checkpoint:

```powershell
python -m ml.training.evaluate_model
```

## API Endpoints

- `GET /health`: checks model readiness and active threshold
- `POST /predict`: legacy manual feature endpoint
- `POST /analyze`: main upload + job description endpoint
- `POST /feedback/{prediction_id}`: stores reviewed labels
- `GET /feedback/retraining-status`: reports whether enough reviewed data exists for retraining

## Adaptive Retraining Logic

When reviewed feedback is submitted:

1. The reviewed label is saved in SQLite.
2. The system checks whether enough new labeled samples exist.
3. If class-balance and validation checks pass, a new model is trained.
4. The new checkpoint is stored in `ml/models/registry/`.
5. The API hot-reloads the promoted model without a manual restart.

Registry metadata is stored in:

- `ml/models/registry/metadata.json`

## Environment Variables

- `MODEL_THRESHOLD` default `0.30`
- `RETRAIN_MIN_FEEDBACK` default `100`
- `RETRAIN_AUTO_ENABLED` default `true`
- `RETRAIN_EPOCHS` default `20`
- `RETRAIN_MIN_NEW_SAMPLES` default `10`
- `RETRAIN_MIN_VAL_ACCURACY` default `0.55`

Demo-friendly values are included in [`.env.example`](.env.example).

## Test The Project

```powershell
python -m pytest -q
```

## Known Limitations

- ATS scoring is heuristic and not calibrated using real recruiter feedback.
- Semantic matching uses TF-IDF, not transformer embeddings.
- Resume parsing quality depends on the extractable text quality inside PDF and DOCX files.
- The current project is designed as a prototype demo, not a production hiring system.

## Possible Future Improvements

- Replace TF-IDF similarity with sentence-transformer embeddings
- Add recruiter login, candidate dashboard, and feedback history UI
- Support batch resume uploads and ranking
- Add better explainability charts and confusion matrix visuals to the frontend
- Introduce approval workflows before promoting retrained models
