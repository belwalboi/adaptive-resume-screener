# Shubh Guide

## Your Role
You are the main opener and closer of the presentation. You should sound like the person who understands the whole project end to end.

You should speak on:
- Slide 1: Title Slide
- Slide 2: Problem Statement and Need
- Slide 12: Conclusion and Future Scope

## Folders and Files To Prepare Deeply
- `README.md`: project purpose, setup, and overall flow.
- `docker-compose.yml`: how frontend and backend run together.
- `backend/main.py`: app startup, service wiring, environment settings.
- `ml/models/`: model definition.
- `ml/inference/`: how prediction is made at runtime.
- `ml/training/`: training and evaluation flow.
- `feedback_loop/`: retraining readiness and adaptive retraining.
- `data/`: raw and processed data.
- `notebooks/`: metrics and plots used in presentation.

## Full Project Flow You Must Know
The project is an AI-assisted resume screening prototype. A recruiter uploads a resume and provides a job description. The backend parses the resume text, extracts interpretable features, computes ATS-style and semantic matching signals, and runs a PyTorch model to generate a shortlisting recommendation. The result is stored in SQLite along with matched keywords, missing keywords, extracted features, and explanation text. After seeing the result, the reviewer can submit feedback, and that feedback can later be used for retraining.

## Architecture Points You Must Explain Well
The architecture has four main layers:
- `frontend/`: takes input and shows results.
- `backend/`: validates requests and coordinates services.
- `ml/`: contains model and inference logic.
- `database/`: stores predictions and feedback.

In `backend/main.py`, the app creates these services in `app.state`:
- `PredictionRepository`
- `ResumeParserService`
- `ResumeAnalysisService`
- `ModelService`
- `RetrainingTriggerService`
- `AdaptiveRetrainer`

This is your strongest architecture point: the backend is modular and each service has one responsibility.

## Model and Metrics You Must Know
The current `ResumeNet` model in `ml/models/resume_net.py` is a feedforward neural network with:
- 6 input features
- hidden layers of 128 and 64
- ReLU activations
- BatchNorm after the first hidden layer
- 1 output neuron

The six current features are:
1. `years_experience`
2. `skills_match_score`
3. `education_level`
4. `project_count`
5. `resume_length`
6. `github_activity`

Current metrics:
- Accuracy: `0.6988`
- Precision: `0.6988`
- Recall: `1.0000`
- F1 Score: `0.8227`
- AUC-ROC: `0.7982`
- Threshold: `0.30`

Interpretation you should give:
The model is good for an academic prototype and is intentionally recall-oriented so that potentially suitable candidates are not missed in first-pass screening.

## Retraining You Must Understand
`feedback_loop/retraining_trigger.py` checks whether enough feedback-labeled samples exist. The default minimum is `100`.

`feedback_loop/adaptive_retrainer.py` can:
- fetch labeled samples
- check if enough new samples exist
- ensure both classes are present
- retrain a fresh model
- apply validation guardrails
- save a new model version

This is why the project is called adaptive.

## Exact Speaking Content
### Slide 1
"Good morning. Our project is Adaptive Resume Screener, an AI-assisted and explainable resume screening prototype. The system supports the initial shortlisting process by combining heuristic analysis, a lightweight machine learning model, and a feedback-driven improvement loop."

### Slide 2
"Manual resume screening is time-consuming, repetitive, and often inconsistent when many applications must be reviewed quickly. At the same time, fully automated systems are often hard to explain. Our project addresses this by creating a transparent first-pass screening system that compares a resume with a job description, generates a recommendation, and also explains why that recommendation was produced."

### Slide 12
"To conclude, Adaptive Resume Screener is an end-to-end prototype integrating frontend interaction, backend APIs, machine learning, explainability, database storage, and feedback collection. It improves transparency and consistency in initial shortlisting. As future scope, we can improve the dataset, expand feature engineering, strengthen document parsing, and make retraining more mature. This is an academically honest prototype, not a production hiring system."

## Likely Viva Questions and Answers
### Why did you choose this project?
Resume screening is a practical problem because recruiters often receive many applications and need a faster first-pass screening method.

### Why is the system explainable?
Because it shows matched keywords, missing keywords, extracted feature values, ATS-style score, semantic score, and explanation text instead of only a final label.

### Is it production-ready?
No. It is a strong academic prototype, but real hiring systems need larger validated datasets, fairness analysis, and more robust parsing.

### What makes it adaptive?
Feedback is saved after prediction, and the retraining pipeline checks when enough labeled samples are available for another training cycle.

## Facts You Must Memorize
- supported formats: `TXT`, `PDF`, `DOCX`
- endpoints: `/health`, `/predict`, `/analyze`, `/feedback/{prediction_id}`, `/feedback/retraining-status`
- backend: FastAPI
- model: PyTorch
- database: SQLite
- deployment command: `docker compose up --build`

## Emergency 20-Second Summary
Adaptive Resume Screener is an explainable AI-assisted prototype for initial resume shortlisting. It takes a resume and job description, extracts interpretable features, predicts shortlist suitability, stores the result in SQLite, and collects feedback for future retraining.
