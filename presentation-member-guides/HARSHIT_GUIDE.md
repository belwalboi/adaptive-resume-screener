# Harshit Guide

## Your Role
You are the backend and database-flow speaker. Your job is to make the internal logic sound clean, structured, and trustworthy.

You should speak on:
- Slide 7: Backend and API Flow
- Slide 10: Database, Feedback, and Retraining

## Folders and Files To Prepare Deeply
- `backend/main.py`: app startup and service wiring.
- `backend/api/routes.py`: endpoint logic.
- `backend/schemas/prediction.py`: request and response schemas.
- `backend/services/resume_parser_service.py`: TXT, PDF, DOCX parsing.
- `backend/services/resume_analysis_service.py`: feature extraction and explainability signals.
- `backend/services/model_service.py`: model loading and prediction.
- `backend/services/prediction_repository.py`: SQLite insert and update logic.
- `database/schema.sql`: database table structure.
- `tests/test_backend_api.py`: API tests.
- `tests/test_prediction_repository.py`: persistence test.

## API Flow You Must Know
Main endpoints:
- `GET /health`
- `POST /predict`
- `POST /analyze`
- `POST /feedback/{prediction_id}`
- `GET /feedback/retraining-status`

The most important endpoint is `/analyze`. It:
1. checks that the job description is not blank
2. reads the uploaded file bytes
3. checks that the file is not empty
4. checks the file size is below 5 MB
5. parses the resume
6. runs resume analysis
7. runs model prediction
8. blends model probability with analysis score
9. stores the result in SQLite
10. returns structured JSON

## Validation Points You Must Know
`backend/schemas/prediction.py` defines typed payloads.
- `PredictionRequest` enforces valid numeric ranges for manual features.
- `FeedbackRequest` enforces `reviewed_label` must be `0` or `1`.
- `AnalysisResponse` defines the full JSON returned to the frontend.

This is good viva material because it proves the API is structured.

## Resume Parsing Points You Must Know
`backend/services/resume_parser_service.py` supports:
- `.txt`
- `.pdf`
- `.docx`

It uses:
- plain decoding for text files
- `pypdf` for PDF
- `python-docx` for DOCX

Then it cleans the text by removing null bytes and collapsing repeated whitespace.

## Database Points You Must Know
The project uses SQLite and the main table is `predictions`.

The schema stores:
- core feature columns
- probability
- decision
- threshold
- model version
- reviewed label
- reviewed time
- feedback note
- source
- resume filename
- job description
- resume excerpt
- ATS score
- semantic score
- final score
- matched keywords
- missing keywords
- explanation
- model features as JSON
- extracted features as JSON

This shows that the project stores both the decision and the reasoning details.

## Repository Logic You Must Know
`backend/services/prediction_repository.py`:
- initializes the database
- saves prediction results
- updates a prediction with feedback
- counts labeled feedback records

When feedback is submitted, `save_feedback()` updates:
- `reviewed_label`
- `reviewed_at`
- `feedback_note`

for the row identified by `prediction_id`.

Best answer for linking feedback to prediction:
We use `prediction_id` as the link, and the feedback endpoint updates the same SQLite record.

## Exact Speaking Content
### Slide 7
"The backend is implemented using FastAPI and is organized into routes, schemas, and services. The `/analyze` endpoint is the central API flow. It validates the request, parses the uploaded resume, extracts features and matching scores, runs model prediction, stores the result in SQLite, and returns a structured JSON response. This keeps the backend modular and easier to test."

### Slide 10
"The database layer stores each prediction in SQLite together with the decision, scores, features, and explanation fields. After the result is shown, the reviewer can submit feedback using the prediction ID. That feedback is saved back into the same prediction record. The system also counts how many labeled feedback records are available and reports when enough data has been collected for adaptive retraining."

## Likely Viva Questions and Answers
### Why did you separate routes, schemas, and services?
Routes handle HTTP flow, schemas define structured data, and services handle business logic such as parsing, analysis, model calls, and database operations.

### What happens if the job description is blank?
The `/analyze` endpoint checks `job_description.strip()` and returns HTTP `400` if it is empty.

### What happens if the prediction ID does not exist during feedback?
The repository update affects zero rows, so the route returns HTTP `404` saying the prediction record was not found.

### Why did you choose SQLite?
SQLite is lightweight, file-based, easy to integrate, and appropriate for a mini-project prototype.

## Tests You Must Mention
`tests/test_backend_api.py` checks health, predict, analyze, feedback, retraining-status, optional feedback note, and blank job description validation.

`tests/test_prediction_repository.py` verifies feedback label, note, and reviewed timestamp are persisted in SQLite.

## Backup Facts You Should Know
- supported formats: `TXT`, `PDF`, `DOCX`
- `/analyze` uses multipart form input
- `/predict` uses manual feature JSON
- database: SQLite
- `prediction_id` links prediction and feedback

## Transition Line
Now that the backend flow is clear, Ritik will explain the machine learning pipeline, the six input features, and how the model performance was evaluated.

## Emergency 20-Second Summary
My part covers the backend API and database flow. FastAPI validates requests, parses the resume, runs analysis and prediction, stores the result in SQLite, and later updates the same record with reviewer feedback using `prediction_id`.
