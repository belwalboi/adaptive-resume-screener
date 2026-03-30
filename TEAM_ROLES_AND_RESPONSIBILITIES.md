# Team Roles and Responsibilities

This document reflects the final 5-member split for the Adaptive Resume Screener mini-project. Each major role area is shared by two members so that the team has both ownership and backup during report writing, presentation, and viva.

## Role-to-Folder Ownership

Use this as the primary split of responsibility.

| Member | Role | Main folders/files to own |
| --- | --- | --- |
| Shubh and Aditya | Project Lead and System Integrator | `README.md`, `docker-compose.yml`, `backend/main.py`, `sample_resume.txt` |
| Mrinalendu and Aditya | Frontend and Demo Flow | `frontend/` |
| Harshit and Ritik | Backend and API | `backend/api/`, `backend/schemas/`, `backend/services/` |
| Shubh and Ritik | ML and Feature Engineering | `ml/`, `feedback_loop/`, `data/`, `notebooks/` |
| Mrinalendu and Harshit | Database, Testing, and Deployment | `database/`, `docker/`, `tests/`, `.env.example`, `requirements.txt` |

This does not mean each member only knows their own folder. For the viva, everyone should still understand the full workflow from upload to feedback storage.

## Member-Wise Combined Responsibility Map

| Member | Shared roles | Main folders/files to prepare deeply | Primary viva ownership |
| --- | --- | --- | --- |
| Shubh | Project Lead and System Integrator; ML and Feature Engineering | `README.md`, `docker-compose.yml`, `backend/main.py`, `ml/`, `feedback_loop/`, `data/`, `notebooks/` | problem statement, architecture, ML logic, retraining, conclusion |
| Aditya | Project Lead and System Integrator; Frontend and Demo Flow | `README.md`, `docker-compose.yml`, `backend/main.py`, `frontend/`, `sample_resume.txt` | integration story, system handoff, demo flow, UI walkthrough |
| Mrinalendu | Frontend and Demo Flow; Database, Testing, and Deployment | `frontend/`, `database/`, `docker/`, `tests/`, `requirements.txt` | UI demo, feedback submission, storage overview, deployment basics |
| Harshit | Backend and API; Database, Testing, and Deployment | `backend/api/`, `backend/schemas/`, `backend/services/`, `database/`, `docker/`, `tests/` | API flow, validation, persistence, schema, test coverage |
| Ritik | Backend and API; ML and Feature Engineering | `backend/services/`, `ml/`, `feedback_loop/`, `data/`, `notebooks/` | feature engineering, model inference, metrics, retraining pipeline |

## Named Role Briefs

### Project Lead and System Integrator (Shubh and Aditya)

Responsible for:

- opening the presentation
- explaining the problem, objective, and motivation
- giving the high-level architecture overview
- connecting the frontend, backend, model, and database into one story
- closing with limitations and future work

Primary folders/files:

- `README.md`
- `docker-compose.yml`
- `backend/main.py`
- `sample_resume.txt`
- `VIVA_QUICK_REFERENCE.md`

Must know well:

- how the complete request flow works from browser to database
- what each main folder does
- why the project uses FastAPI, PyTorch, SQLite, and Docker
- what the current limitations are
- what is actually implemented versus future work

Should be ready to explain:

- why resume screening is a useful automation problem
- why the project combines heuristics and ML instead of using only one approach
- what makes the output explainable
- how the whole system fits together in one pipeline

### Frontend and Demo Flow (Mrinalendu and Aditya)

Responsible for:

- showing the web interface
- uploading a resume
- entering the job description
- demonstrating the analysis results
- demonstrating the feedback form

Primary folders/files:

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

Must know well:

- how the UI is structured
- how form submission works
- how `fetch()` calls the backend
- how the response is rendered on the page
- how the feedback form sends `reviewed_label` and `feedback_note`

Should be ready to explain:

- how the UI sends the resume and job description to the backend
- how the result cards, keywords, and feature list are rendered
- how user feedback is submitted from the website
- what happens on success and on error

Questions this role should handle confidently:

- What does the user see after clicking Analyze?
- How do you show explainability in the UI?
- How does the website know which prediction row to attach feedback to?

### Backend and API (Harshit and Ritik)

Responsible for:

- explaining FastAPI structure
- describing `POST /analyze` and `POST /feedback/{prediction_id}`
- explaining validation, parsing, and database writes
- explaining how the backend returns structured JSON for the frontend

Primary folders/files:

- `backend/main.py`
- `backend/api/routes.py`
- `backend/schemas/prediction.py`
- `backend/services/resume_parser_service.py`
- `backend/services/resume_analysis_service.py`
- `backend/services/model_service.py`
- `backend/services/prediction_repository.py`
- `backend/core/logging_config.py`

Must know well:

- how routes are registered in FastAPI
- how request validation works with Pydantic
- how uploaded files are validated and parsed
- how the backend creates the prediction record
- how feedback is saved back to the same record

Should be ready to explain:

- how files are accepted and validated
- how prediction results are saved in SQLite
- how feedback is linked to a specific prediction row
- what each backend service does

Questions this role should handle confidently:

- Why did you separate routes, schemas, and services?
- What does `/analyze` do internally?
- How do you store `feedback_note` and `reviewed_label`?

### ML and Feature Engineering (Shubh and Ritik)

Responsible for:

- explaining the 6 input features
- describing the `ResumeNet` model
- explaining model evaluation metrics
- explaining retraining readiness and adaptive learning

Primary folders/files:

- `ml/models/resume_net.py`
- `ml/inference/resume_screener.py`
- `ml/inference/config.py`
- `ml/training/train_model.py`
- `ml/training/evaluate_model.py`
- `ml/preprocessing/preprocess_tabular.py`
- `ml/data/load_resumes.py`
- `feedback_loop/adaptive_retrainer.py`
- `feedback_loop/retraining_trigger.py`
- `data/raw/`
- `data/processed/`
- `notebooks/`

Must know well:

- what the 6 features mean
- how the model converts features into shortlist or reject
- why the threshold is `0.30`
- what accuracy, precision, recall, and F1 mean in this project
- how feedback could later be used for retraining

Should be ready to explain:

- why the features are interpretable
- why the threshold is set to `0.30`
- why recall is high in the current checkpoint
- how retraining readiness is checked

Questions this role should handle confidently:

- Why did you use a feature-based model instead of a transformer?
- How is semantic similarity calculated?
- What happens when enough labeled feedback is collected?

### Database, Testing, and Deployment (Mrinalendu and Harshit)

Responsible for:

- explaining the SQLite schema
- showing where predictions and feedback are stored
- covering Docker setup and tests
- explaining how to run the full stack for demo day

Primary folders/files:

- `database/schema.sql`
- `database/resume_screening.db`
- `docker/`
- `docker-compose.yml`
- `tests/test_backend_api.py`
- `tests/test_resume_analysis_service.py`
- `tests/test_prediction_repository.py`
- `.env.example`
- `requirements.txt`

Must know well:

- what columns are stored in the `predictions` table
- how the database file is initialized
- how Docker starts the frontend and backend
- what the automated tests cover
- how to troubleshoot common demo issues

Should be ready to explain:

- what data is stored after analysis
- what fields change after feedback submission
- how the app is started locally and with Docker
- how the test suite improves confidence

Questions this role should handle confidently:

- Why did you choose SQLite?
- How do you know feedback is really stored?
- What should you do if the app fails during the demo?

## Suggested Report Writing Split

- Shubh: abstract support, project overview, system architecture, ML overview, limitations, future work
- Aditya: problem statement, objectives, integration workflow, demo narrative, frontend explanation support
- Mrinalendu: frontend design, UI flow, screenshots, feedback workflow, deployment notes
- Harshit: backend design, API endpoints, validation flow, database operations, testing coverage
- Ritik: feature engineering, model workflow, scoring logic, evaluation metrics, retraining pipeline

## Suggested Viva Delivery Order

1. Shubh: problem statement, objective, motivation, and high-level architecture
2. Aditya: end-to-end integration story and transition into the live demo
3. Mrinalendu: frontend workflow, analysis screen, result rendering, and feedback form
4. Harshit: backend API flow, validation, parsing, database writes, and test coverage
5. Ritik: feature engineering, model inference, evaluation metrics, threshold logic, and adaptive retraining
6. Harshit and Mrinalendu: answer follow-up questions on SQLite, Docker, deployment, and troubleshooting
7. Shubh: limitations, future work, and final conclusion

## Shared Knowledge Everyone Should Have

Every team member should know the answer to these basic questions:

- What problem does the project solve?
- What are the 5 main API endpoints?
- What are the 6 model features?
- What does the feedback form do?
- Where is data stored?
- What are the main limitations?

Even if a member is not the folder owner, they should still be able to explain:

- `frontend/` at a high level
- `backend/` at a high level
- `ml/` at a high level
- `database/` at a high level

## Folder Knowledge Depth Guide

Use this to decide how deeply each member should prepare.

| Folder | Owner depth | Team depth |
| --- | --- | --- |
| `frontend/` | High | Medium |
| `backend/api/` | High | Medium |
| `backend/services/` | High | Medium |
| `backend/schemas/` | High | Low to Medium |
| `ml/` | High | Medium |
| `feedback_loop/` | High | Low to Medium |
| `database/` | High | Medium |
| `docker/` | High | Low to Medium |
| `tests/` | High | Low to Medium |
| `data/` | Medium to High | Low |
| `notebooks/` | Medium | Low |

## Demo Checklist

- Backend server starts successfully
- Frontend opens correctly
- `sample_resume.txt` is available
- A job description is prepared in advance
- The team knows which member speaks at each stage
- One person is ready to open the SQLite database if asked
- One person is ready to open the API docs at `/docs`

## Key Talking Points

- The project is not just a classifier; it also gives keyword matches, missing terms, feature values, and score explanations.
- The database stores both predictions and feedback, so the system can improve over time.
- Feedback is now submitted directly from the website and stored in SQLite.
- The retraining pipeline exists, but retraining itself is a controlled later step, not something you need to run live in the viva.

## Honest Academic Positioning

Use this wording if your professor asks about scope:

"This is a functional prototype built to demonstrate a complete ML product workflow: data processing, inference, API design, UI integration, persistence, testing, and a feedback loop. It is not intended to replace human hiring decisions."

## Common Questions the Team Should Practice

### Why did you use only 6 features?

Because they are easy to explain, fast to compute, and suitable for a mini-project where interpretability matters.

### Why not use BERT or transformers?

That would increase complexity, compute cost, and explanation difficulty. For this academic prototype, feature-based modeling was the better fit.

### Why is recall so high?

The threshold is intentionally low at `0.30`, which reduces false negatives and makes the demo less likely to reject potentially suitable candidates too aggressively.

### How is feedback used?

Each prediction row can later be labeled as correct or incorrect. Those labeled samples are counted and can be used by the adaptive retraining pipeline.

### What happens if parsing fails for a PDF?

The backend returns an error, and the parser depends on extractable text quality. This is one of the stated limitations.

## Final Advice

- Keep the demo focused on the working flow.
- Do not oversell the project as production-ready hiring AI.
- Emphasize explainability, integration, and learning value.
- Let each member speak about the part they actually understand best.
