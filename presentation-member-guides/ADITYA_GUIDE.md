# Aditya Guide

## Your Role
You are the system integration speaker. Your job is to explain how all modules connect into one working pipeline.

You should speak on:
- Slide 3: Project Objectives
- Slide 4: High-Level System Architecture

## Folders and Files To Prepare Deeply
- `README.md`: overall project purpose and setup.
- `docker-compose.yml`: frontend-backend integration.
- `backend/main.py`: app initialization and services.
- `frontend/index.html`: what the user sees.
- `frontend/app.js`: form submission, API calls, result rendering.
- `frontend/styles.css`: presentation and readability of UI.
- `sample_resume.txt`: example demo input.

## Integration Story You Must Know
When the user fills the form, the frontend collects the resume file and job description. In `frontend/app.js`, the code creates a `FormData` object and sends it to the backend using `fetch()` on `/analyze`.

On the backend, `backend/main.py` has already initialized:
- parser service
- analysis service
- model service
- prediction repository

The `/analyze` route then validates input, parses the resume, extracts features and scores, runs model prediction, blends the model probability with analysis score, stores the result in SQLite, and returns structured JSON to the frontend.

The frontend then displays:
- prediction ID
- confidence
- threshold
- ATS-style score
- semantic score
- final score
- matched keywords
- missing keywords
- extracted features
- explanation
- feedback form

This is your strongest point: the project is a complete end-to-end system, not disconnected modules.

## Frontend-Backend Handoff You Must Understand
`frontend/app.js` builds `API_BASE_URL` dynamically. On localhost it points to port `8000`, so the frontend can talk to FastAPI.

On form submission the frontend:
- checks a file is uploaded
- checks the job description is not blank
- shows a loading state
- sends the request to `/analyze`
- renders the returned JSON in the browser

## Exact Speaking Content
### Slide 3
"The main objectives of the project are to accept a resume and job description as input, extract useful information from the resume automatically, compare the candidate profile with the job requirements, generate a shortlisting recommendation, explain the result using keywords and feature values, and store predictions with reviewer feedback for future improvement."

### Slide 4
"This slide shows how the full system is integrated. The frontend collects the resume and job description from the user. The FastAPI backend receives the request and coordinates the parser, analysis service, model service, and prediction repository. The analysis and machine learning components generate the recommendation, and SQLite stores the prediction and feedback data. Finally, the result is returned to the frontend and displayed to the user."

## What You Must Know About `backend/main.py`
This file proves integration. In the FastAPI lifespan, the app creates `PredictionRepository`, `ResumeParserService`, `ResumeAnalysisService`, `ModelService`, `RetrainingTriggerService`, and `AdaptiveRetrainer`. That is why the app is modular and easy to explain.

## What You Must Know About Docker
`docker-compose.yml` defines two services:
- `backend` on port `8000`
- `frontend` on port `3000`

Your one-line explanation should be:
Docker Compose helps us run the backend and frontend together in a consistent demo environment.

## Likely Viva Questions and Answers
### How are all modules connected?
The frontend collects input, the backend coordinates parsing and analysis, the model produces a prediction, the repository stores the result, and the frontend displays the returned JSON.

### Why did you use FastAPI?
It is lightweight, fast, and suitable for structured APIs with validation.

### Why did you use Docker?
Docker makes the project easier to run consistently for demo and testing.

### What happens when the user clicks Analyze?
The frontend validates the input, sends the resume and job description to `/analyze`, the backend processes the request, stores the result, and returns the response for display.

## Backup Facts You Should Know
- supported formats: `TXT`, `PDF`, `DOCX`
- database: SQLite
- threshold: `0.30`
- feedback is submitted after prediction

## Transition Line
Now that the system architecture is clear, Mrinalendu will show how this workflow appears on the actual user interface and how the user interacts with the application.

## Emergency 20-Second Summary
My part is the integration story. The frontend sends the resume and job description to the backend, the backend coordinates parsing, analysis, model inference, and storage, and then the frontend displays the result and collects feedback.
