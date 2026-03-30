# Ritik Guide

## Your Role
You are the machine learning and feature-engineering speaker. Your job is to make the model logic sound clear, interpretable, and academically honest.

You should speak on:
- Slide 8: Machine Learning Pipeline
- Slide 9: Model Results and Metrics

## Folders and Files To Prepare Deeply
- `backend/services/resume_analysis_service.py`: feature extraction and explainability.
- `backend/services/model_service.py`: backend-to-model connection.
- `ml/models/resume_net.py`: current model architecture.
- `ml/inference/resume_screener.py`: model loading and runtime prediction.
- `ml/training/train_model.py`: training flow.
- `ml/training/evaluate_model.py`: evaluation flow.
- `ml/preprocessing/preprocess_tabular.py`: data preparation.
- `feedback_loop/adaptive_retrainer.py`: feedback-based retraining.
- `feedback_loop/retraining_trigger.py`: retraining readiness.
- `data/`: dataset files.
- `notebooks/`: metric notebooks, confusion matrix, ROC curve.

## Feature Engineering You Must Know
The current pipeline creates six interpretable features:
1. `years_experience`: extracted from phrases like `4 years` or `5 yrs`.
2. `skills_match_score`: percentage of tracked job-description keywords found in the resume.
3. `education_level`: encoded from words like diploma, bachelor, master, or PhD.
4. `project_count`: estimated from explicit project mentions.
5. `resume_length`: character length of the cleaned resume text.
6. `github_activity`: heuristic score from GitHub links and open-source hints.

These are strong academic features because each one is easy to explain.

## ATS and Semantic Scoring You Must Know
`backend/services/resume_analysis_service.py` also computes:
- `ats_score`
- `semantic_score`
- `final_score`

`ats_score` is heuristic and combines keyword coverage with section completeness.

`semantic_score` uses `TfidfVectorizer` and cosine similarity, so the project gets meaning-level similarity without needing a heavy transformer model.

`final_score` is weighted as:
- 55% skills match score
- 30% semantic score
- 15% ATS-style score

Important point:
The final returned probability in `/analyze` is created by blending the ML model probability with the analysis score.

## Model You Must Know
The current `ResumeNet` architecture is:
- input dimension `6`
- `Linear(6, 128)`
- `ReLU`
- `BatchNorm1d(128)`
- `Linear(128, 64)`
- `ReLU`
- `Linear(64, 1)`

During inference in `ml/inference/resume_screener.py`, sigmoid is applied and the decision is:
- `shortlist` if probability >= threshold
- `reject` otherwise

Current threshold: `0.30`

Why threshold is low:
The model is intentionally recall-oriented so that potentially suitable candidates are not missed in first-pass screening.

## Exact Speaking Content
### Slide 8
"The machine learning component uses a lightweight PyTorch feedforward neural network called ResumeNet. Before prediction, the resume analysis service extracts six interpretable numerical features: years of experience, skills match score, education level, project count, resume length, and GitHub activity. These features are used because they are understandable and directly connected to resume-job fit."

### Slide 9
"The current checkpoint gives Accuracy 0.6988, Precision 0.6988, Recall 1.0000, F1 Score 0.8227, and AUC-ROC 0.7982. The most important point is that the threshold is set to 0.30, so the model is tuned to achieve very high recall. This makes it useful for first-pass screening, where missing a potentially good candidate is more costly than reviewing some extra candidates."

## Metrics You Must Interpret Correctly
- `Accuracy 0.6988`: about 70% overall correct predictions.
- `Precision 0.6988`: when the model says shortlist, it is correct about 70% of the time.
- `Recall 1.0000`: it catches all actual shortlisted cases in the test set.
- `F1 0.8227`: strong combined score because recall is very high.
- `AUC-ROC 0.7982`: good separation ability, clearly better than random.

Honest conclusion:
These are good prototype results, but they are not enough to claim production-level hiring quality.

## Retraining You Must Know
`feedback_loop/retraining_trigger.py` checks whether enough labeled feedback has been collected. The default minimum is `100`.

`feedback_loop/adaptive_retrainer.py`:
- fetches labeled samples
- checks if enough new samples exist
- checks if both classes are present
- trains and validates a fresh model
- uses validation accuracy as a guardrail
- saves a new model version if retraining succeeds

## Likely Viva Questions and Answers
### What is semantic similarity here?
Semantic similarity is calculated using TF-IDF vectorization and cosine similarity between the resume text and job description.

### Why is recall 1.0?
Because the threshold is set to `0.30`, the model is intentionally more inclusive and avoids missing strong candidates in first-pass screening.

### Does high recall mean the model is perfect?
No. High recall does not mean high selectivity. Precision is still limited, so the system is best treated as a screening aid.

### Why did you use a feature-based model instead of a transformer?
A lightweight feature-based model is easier to train, easier to explain, computationally cheaper, and better suited to a mini-project focused on transparency and system integration.

## Backup Facts You Should Know
- threshold: `0.30`
- framework: PyTorch
- semantic similarity: TF-IDF + cosine similarity
- retraining needs labeled feedback
- six features must be memorized in order

## Transition Line
That covers the feature engineering and model evaluation part of the system. The remaining point is how this result is stored, improved through feedback, and presented as an honest academic prototype.

## Emergency 20-Second Summary
My part is the ML pipeline. We extract six interpretable features from the resume and job description, run them through a lightweight PyTorch model, evaluate the output using standard metrics, and keep the system recall-oriented for first-pass screening.
