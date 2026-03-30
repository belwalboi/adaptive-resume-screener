# Mrinalendu Guide

## Your Role
You are the UI, demo-flow, and deployment-readiness speaker. Your job is to make the project feel real and usable.

You should speak on:
- Slide 5: User Workflow / Demo Flow
- Slide 6: Frontend Design
- Slide 11: Testing, Deployment, and Demo Readiness

## Folders and Files To Prepare Deeply
- `frontend/index.html`: page structure.
- `frontend/app.js`: form submission, API calls, result rendering, feedback submission.
- `frontend/styles.css`: UI presentation.
- `database/schema.sql`: what gets stored after analysis and feedback.
- `docker/`: Dockerfiles.
- `docker-compose.yml`: how the project is started.
- `tests/test_backend_api.py`: endpoint testing.
- `tests/test_resume_analysis_service.py`: analysis logic testing.
- `tests/test_prediction_repository.py`: feedback persistence testing.
- `requirements.txt`: major dependencies.

## User Workflow You Must Explain
The user workflow is simple:
1. Upload a resume file.
2. Paste a job description.
3. Click `Analyze Resume`.
4. View the result and explanation.
5. Submit feedback.

This is important because the teacher should immediately understand that the project is practical and easy to use.

## What You Must Know About `frontend/app.js`
This file controls the main UI behavior. It:
- builds the API base URL
- validates the input
- creates `FormData`
- sends a `POST` request to `/analyze`
- shows a loading state
- renders result cards
- shows keyword tags and extracted features
- creates and submits the feedback form

After analysis, the page shows:
- decision banner
- prediction ID
- confidence
- threshold
- ATS-style score
- semantic score
- final score
- matched strengths
- missing requirements
- extracted features
- explanation panel
- feedback form

The feedback form lets the reviewer choose `Correct` or `Incorrect`, add an optional note, and submit `reviewed_label` and `feedback_note` to `/feedback/{prediction_id}`.

## Exact Speaking Content
### Slide 5
"From the user perspective, the workflow is very simple. The recruiter uploads a resume in TXT, PDF, or DOCX format, pastes the job description, and clicks Analyze Resume. The system then processes the input and shows the recommendation along with keyword matches, extracted features, and explanation. After reviewing the result, the recruiter can also submit feedback."

### Slide 6
"The frontend is designed to make the output readable and explainable. Instead of only showing shortlist or reject, the interface shows ATS-style score, semantic score, final score, matched keywords, missing keywords, extracted features, and a feedback form. This makes the system easier to understand and more useful during demonstration."

### Slide 11
"To improve demo readiness and reliability, the project includes automated tests for backend API behavior, resume analysis logic, and feedback persistence. The system is also containerized using Docker and Docker Compose, which makes it easier to run the frontend and backend together in a consistent environment."

## What You Must Know About Deployment
Main command:
`docker compose up --build`

This starts:
- frontend on port `3000`
- backend on port `8000`

Simple explanation:
Docker helps us run the project with less setup trouble and makes the demo more repeatable.

## What You Must Know About Testing
`tests/test_backend_api.py` checks health, predict, analyze, feedback, retraining-status, optional feedback note, and blank job description validation.

`tests/test_resume_analysis_service.py` checks missing keyword detection and prevents false perfect ATS matches.

`tests/test_prediction_repository.py` checks that feedback label, note, and reviewed timestamp are really stored in SQLite.

## Likely Viva Questions and Answers
### What does the user see after clicking Analyze?
The user sees the decision, confidence, threshold, ATS-style score, semantic score, final score, matched keywords, missing keywords, extracted features, explanation text, and then a feedback form.

### How do you show explainability in the UI?
We show matched keywords, missing keywords, feature values, and multiple scores instead of only a final label.

### How is feedback submitted from the UI?
The user selects whether the recommendation was correct or incorrect, can write an optional note, and the frontend sends `reviewed_label` and `feedback_note` to `/feedback/{prediction_id}`.

### What if the live demo fails?
We keep screenshot-based backup slides showing the input page, result screen, and feedback workflow.

## Backup Facts You Should Know
- supported formats: `TXT`, `PDF`, `DOCX`
- main UI endpoint: `/analyze`
- feedback endpoint: `/feedback/{prediction_id}`
- database: SQLite
- startup command: `docker compose up --build`

## Transition Line
Now that the UI and user workflow are clear, Harshit will explain the backend API flow and how the system processes and stores this data internally.

## Emergency 20-Second Summary
My part covers the user workflow, frontend behavior, and demo readiness. The interface collects the inputs, displays detailed results and explainability, accepts reviewer feedback, and the whole project can be started reliably using Docker.
