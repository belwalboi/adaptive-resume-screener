# Presentation Summary

This outline is designed for a teacher presentation of about 8-10 minutes with 5 team members.
Keep each slide visual and clean: use 3-5 bullets maximum, one clear diagram or screenshot where possible, and large readable text.

## Recommended Slide Flow

| Slide | Title | What to insert | Primary speaker | What this member should speak on |
| --- | --- | --- | --- | --- |
| 1 | Title Slide | Project title, team member names, roll numbers, guide name, department, university logo | Shubh | Introduce the project, team, and one-line summary: "Adaptive Resume Screener is an explainable AI-assisted resume screening prototype." |
| 2 | Problem Statement and Need | 3 short bullets on manual screening problems, 1 short objective statement | Shubh | Explain why resume screening needs automation: time-consuming, inconsistent, poor explainability. End with the project objective. |
| 3 | Project Objectives | 5 concise objectives, one line on heuristic + ML hybrid approach | Aditya | Explain what the system is supposed to do: accept resume + job description, analyze, predict, explain, store, and collect feedback. |
| 4 | High-Level System Architecture | Insert the architecture block diagram from the report, add a simple flow: Frontend -> Backend -> ML -> SQLite | Aditya | Explain how the full system is integrated. This is Aditya's strongest slide because it is the system-integration slide. |
| 5 | User Workflow / Demo Flow | Insert 1 screenshot of input page and 1 screenshot of result page, plus a 4-step flow | Mrinalendu | Explain what the user does: upload resume, paste JD, click analyze, receive result and explanation. |
| 6 | Frontend Design | Show the main UI screenshot, result card screenshot, and feedback form screenshot | Mrinalendu | Explain the frontend role: form handling, result rendering, matched/missing keywords, extracted features, and feedback submission. |
| 7 | Backend and API Flow | Insert API endpoints table and a short request-response flow diagram | Harshit | Explain `/analyze`, `/predict`, `/feedback/{prediction_id}`, `/health`, and `/feedback/retraining-status`. Mention validation, parsing, and JSON response flow. |
| 8 | Machine Learning Pipeline | Insert the six-feature table and a simple ResumeNet architecture sketch | Ritik | Explain the 6 input features, how the model makes a shortlist/reject decision, and why a feature-based model was chosen instead of a transformer. |
| 9 | Model Results and Metrics | Insert metrics table, ROC curve, and confusion matrix | Ritik | Explain Accuracy, Precision, Recall, F1, and AUC-ROC. Clearly say the threshold is recall-oriented and the model is for first-pass screening, not final hiring decisions. |
| 10 | Database, Feedback, and Retraining | Insert ER diagram or schema screenshot, plus feedback loop flow | Harshit | Explain what is stored in SQLite, how feedback is linked to `prediction_id`, and how retraining readiness is tracked. |
| 11 | Testing, Deployment, and Demo Readiness | Insert testing table, Docker command, and maybe `docker compose up --build` or test command | Mrinalendu | Explain that the project is tested, containerized, and easy to run for demo day. Mention backend tests, SQLite persistence, and Docker startup. |
| 12 | Conclusion and Future Scope | 3 bullets for contributions, 3 bullets for limitations/future work, ending "Thank you" | Shubh | Summarize the project contribution, mention limitations honestly, and end confidently. |

## What To Put On Each Slide

- Slide 1: Keep it formal and clean. Do not add too much text.
- Slide 2: Use a problem-to-solution style.
- Slide 3: Keep objectives action-based: upload, analyze, predict, explain, store, improve.
- Slide 4: This should be one of the strongest slides visually. Use the architecture diagram.
- Slide 5: If live demo is risky, make this a screenshot-based backup slide.
- Slide 6: Show the feedback form because teachers usually like the human-in-the-loop idea.
- Slide 7: Keep the API explanation simple. Avoid too many implementation details here.
- Slide 8: Put the six features in a table or small cards. Mention threshold `0.30`.
- Slide 9: Show the actual metric values from the project.
- Slide 10: Emphasize that predictions and feedback are both stored, which makes the system adaptive.
- Slide 11: Mention testing and Docker only briefly. This slide is for trust and readiness.
- Slide 12: End with "This is an academically honest prototype, not a production hiring system."

## Exact Content To Paste In PPT

### Slide 1: Title Slide

**Adaptive Resume Screener**  
AI-Assisted and Explainable Resume Screening Prototype

Team Members:
- Shubh Agnihotri
- Aditya
- Mrinalendu
- Harshit
- Ritik

Guide Name: [Insert Guide Name]  
Department of Computer Science and Engineering  
KIIT University

### Slide 2: Problem Statement and Need

**Problem Statement**
- Manual resume screening is time-consuming and repetitive.
- Shortlisting decisions may become inconsistent when done fully by hand.
- Traditional screening methods often lack transparency and explainability.

**Need for the Project**
- Recruiters need a faster and more structured first-pass screening process.
- The system should support shortlisting decisions with clear feature-based explanations.

### Slide 3: Project Objectives

**Project Objectives**
- To accept a candidate resume and a job description as input.
- To extract useful information from the resume text automatically.
- To compare candidate profile details with job requirements.
- To generate a shortlisting recommendation using heuristic analysis and machine learning.
- To provide explainable output including matched keywords, missing terms, and feature values.
- To store predictions and collect reviewer feedback for future improvement.

### Slide 4: High-Level System Architecture

**System Architecture**
- Frontend collects the resume file and job description from the user.
- Backend API processes the request and coordinates all services.
- Resume analysis generates explainable features and matching signals.
- ResumeNet ML model predicts shortlist suitability.
- SQLite stores predictions, feedback, and retraining readiness data.

**Flow**
Frontend -> FastAPI Backend -> Resume Analysis + ML Model -> SQLite Database -> Result to User

### Slide 5: User Workflow / Demo Flow

**User Workflow**
1. Recruiter uploads a resume in TXT, PDF, or DOCX format.
2. Recruiter enters the target job description.
3. System analyzes the resume and generates scores and prediction.
4. System displays decision, explanation, keywords, and extracted features.
5. Recruiter can submit feedback on whether the decision was correct.

### Slide 6: Frontend Design

**Frontend Features**
- Simple and clean user interface for resume upload and job description input.
- Displays ATS-style score, decision, probability, and explanation.
- Shows matched keywords and missing keywords for transparency.
- Displays extracted feature values used by the backend pipeline.
- Allows the reviewer to submit feedback after viewing the result.

### Slide 7: Backend and API Flow

**Main API Endpoints**
- `GET /health` checks backend and model status.
- `POST /predict` performs direct model prediction using feature inputs.
- `POST /analyze` performs full resume analysis and shortlisting.
- `POST /feedback/{prediction_id}` stores reviewer feedback.
- `GET /feedback/retraining-status` checks whether enough feedback is available for retraining.

**Backend Responsibilities**
- Request validation
- Resume parsing
- Feature extraction
- Model inference
- Database storage
- JSON response generation

### Slide 8: Machine Learning Pipeline

**Machine Learning Pipeline**
- The system uses a lightweight PyTorch feedforward neural network called ResumeNet.
- The model takes 6 numerical features as input.

**Six Input Features**
1. Years of Experience
2. Skills Match Score
3. Education Level
4. Project Count
5. Resume Length
6. GitHub Activity

**Model Note**
- Operational threshold used in the project: `0.30`

### Slide 9: Model Results and Metrics

**Model Performance**
- Accuracy: `0.6988`
- Precision: `0.6988`
- Recall: `1.0000`
- F1 Score: `0.8227`
- AUC-ROC: `0.7982`

**Interpretation**
- The model is tuned to achieve high recall so that strong candidates are not missed in first-pass screening.
- This makes the system useful as an assistive prototype, not a final hiring decision maker.

### Slide 10: Database, Feedback, and Retraining

**Database and Feedback Flow**
- Prediction results are stored in SQLite.
- Each stored prediction receives a unique `prediction_id`.
- Reviewer feedback is linked to the corresponding prediction record.
- Labeled feedback helps monitor when the system is ready for retraining.
- This makes the project adaptive over time.

### Slide 11: Testing, Deployment, and Demo Readiness

**Testing and Deployment**
- Backend API endpoints were tested using automated test cases.
- Resume analysis service logic was validated through focused service-level tests.
- SQLite was used for lightweight local persistence.
- Docker and Docker Compose were used to simplify deployment and demo setup.
- The project can be run in a reproducible way for presentation and evaluation.

**Run Command**
- `docker compose up --build`

### Slide 12: Conclusion and Future Scope

**Conclusion**
- Adaptive Resume Screener is an end-to-end AI-assisted resume screening prototype.
- It combines heuristic analysis, machine learning, explainability, feedback collection, and persistence.
- The system improves transparency and consistency in initial shortlisting.

**Future Scope**
- Improve dataset quality and model selectivity.
- Add stronger document parsing and richer skill extraction.
- Extend the retraining pipeline and support production-grade deployment.

**Closing Line**
- This is an academically honest prototype, not a production hiring system.

## Recommended Member Speaking Order

1. Shubh: Slides 1-2
2. Aditya: Slides 3-4
3. Mrinalendu: Slides 5-6
4. Harshit: Slides 7 and 10
5. Ritik: Slides 8-9
6. Mrinalendu: Slide 11
7. Shubh: Slide 12

## Backup Slides

Keep these after the main deck in case the teacher asks questions:

- Use Case Diagram
- DFD Level 0
- DFD Level 1
- ER Diagram
- Confusion Matrix
- ROC Curve
- Individual Contribution Summary
- Commands slide: `uvicorn backend.main:app --reload`, `docker compose up --build`, `python -m pytest -q`

## What Everyone Must Memorize

- Problem solved by the project
- 5 main API endpoints
- 6 model features
- Threshold = `0.30`
- Metrics: Accuracy `0.6988`, Precision `0.6988`, Recall `1.0000`, F1 `0.8227`, AUC-ROC `0.7982`
- Why the project is explainable
- Why it is a prototype and not a production hiring system

## Final Presentation Tips

- Do not read from the slides.
- Use the diagrams and screenshots as anchors.
- Keep transitions smooth: each member should end by handing over to the next topic.
- If the live demo fails, switch immediately to screenshots and continue confidently.
- Keep the final answer to teacher questions honest and simple.
