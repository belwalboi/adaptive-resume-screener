# Viva Quick Reference

## 30-Second Introduction

"Adaptive Resume Screener is a full-stack mini-project that evaluates a resume against a job description. It combines explainable text analysis with a PyTorch model, stores predictions in SQLite, and collects website feedback for future adaptive retraining."

## 10-12 Minute Demo Flow

1. Explain the problem: manual screening is slow and inconsistent.
2. Show the architecture: frontend -> FastAPI backend -> ML service -> SQLite.
3. Open the web app.
4. Upload `sample_resume.txt`.
5. Paste a targeted job description.
6. Click `Analyze Resume`.
7. Explain:
   - ATS-style score
   - semantic score
   - final screening score
   - matched and missing keywords
   - extracted features
8. Submit feedback from the website.
9. Explain that the feedback is saved in SQLite and counted for retraining readiness.
10. End with limitations and future work.

## Commands To Keep Ready

### Start backend

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Start full stack with Docker

```powershell
docker compose up --build
```

### Run tests

```powershell
python -m pytest -q
```

### Re-check model metrics

```powershell
python -m ml.training.evaluate_model
```

## What To Say About The Scores

- ATS-style score: heuristic score based on keyword coverage and section completeness
- semantic score: TF-IDF cosine similarity between resume text and job description
- final score: blended score used for a readable screening summary
- model probability: PyTorch output based on 6 engineered features

## 6 Features To Memorize

1. Years of experience
2. Skills match score
3. Education level
4. Project count
5. Resume length
6. GitHub activity

## Short Answers For Questions

### Why FastAPI?

It is simple, fast, and automatically provides interactive API docs.

### Why SQLite?

It is lightweight, file-based, and ideal for a college prototype.

### Why not use only keyword matching?

Keyword matching is useful but limited. The model adds another decision signal based on structured features.

### Why not use only deep learning?

A pure black-box approach would be harder to explain. This project balances interpretability and ML.

### Is the system production-ready?

No. It is a working academic prototype designed to demonstrate the complete pipeline.

## What To Show If Asked About Storage

The `predictions` table stores:

- prediction output
- score details
- explainability data
- review label
- review timestamp
- optional feedback note

## Safe Conclusion Line

"Our main contribution is not just prediction, but an end-to-end explainable screening workflow with persistence, testing, and a feedback loop."
