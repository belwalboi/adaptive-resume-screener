# Team Roles and Responsibilities

This document is written for a 5-student mini-project team. Replace the placeholder names with your real names before presenting.

## Suggested Team Split

### Member 1: Project Lead and Problem Statement

Responsible for:

- opening the presentation
- explaining the problem, objective, and motivation
- giving the high-level architecture overview
- closing with limitations and future work

Should be ready to explain:

- why resume screening is a useful automation problem
- why the project combines heuristics and ML instead of using only one approach
- what makes the output explainable

### Member 2: Frontend and User Flow

Responsible for:

- showing the web interface
- uploading a resume
- entering the job description
- demonstrating the feedback form

Should be ready to explain:

- how the UI sends the resume and job description to the backend
- how the result cards, keywords, and feature list are rendered
- how user feedback is submitted from the website

### Member 3: Backend and API

Responsible for:

- explaining FastAPI structure
- describing `POST /analyze` and `POST /feedback/{prediction_id}`
- explaining validation, parsing, and database writes

Should be ready to explain:

- how files are accepted and validated
- how prediction results are saved in SQLite
- how feedback is linked to a specific prediction row

### Member 4: Machine Learning and Feature Engineering

Responsible for:

- explaining the 6 input features
- describing the `ResumeNet` model
- explaining the threshold and reported metrics

Should be ready to explain:

- why the features are interpretable
- why the threshold is set to `0.30`
- why recall is high in the current checkpoint

### Member 5: Database, Docker, Testing, and Deployment

Responsible for:

- explaining the SQLite schema
- showing where predictions and feedback are stored
- covering Docker setup and tests
- describing the adaptive retraining pipeline

Should be ready to explain:

- what data is stored after analysis
- what fields change after feedback submission
- how retraining readiness is checked

## Suggested Presentation Order

1. Member 1: Problem and architecture
2. Member 2: Frontend demo
3. Member 3: Backend flow
4. Member 4: ML logic and metrics
5. Member 5: Database, testing, deployment, and retraining
6. Member 1: Limitations and conclusion

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
