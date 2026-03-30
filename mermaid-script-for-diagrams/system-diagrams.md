# System Diagrams

These diagrams are based on the current implementation in:

- `backend/main.py`
- `backend/api/routes.py`
- `backend/services/`
- `feedback_loop/`
- `database/schema.sql`
- `frontend/app.js`

## 1. Use Case Diagram

```mermaid
flowchart LR
    recruiter[Recruiter / Reviewer]
    admin[Admin / Developer]

    subgraph ARS[Adaptive Resume Screener]
        UC1((Upload Resume))
        UC2((Enter Job Description))
        UC3((Analyze Resume))
        UC4((View Scores, Decision, and Explanation))
        UC5((Submit Feedback))
        UC6((Check Retraining Status))
        UC7((Manual Feature Prediction))
        UC8((Check API Health and Model Version))
    end

    recruiter --> UC1
    recruiter --> UC2
    recruiter --> UC3
    recruiter --> UC4
    recruiter --> UC5
    recruiter --> UC6

    UC3 -.->|includes| UC1
    UC3 -.->|includes| UC2
    UC3 --> UC4

    admin --> UC7
    admin --> UC8
    admin --> UC6
```

## 2. Data Flow Diagram Level 0

This Level 0 DFD is treated as a context diagram: the whole application is modeled as one process.

```mermaid
flowchart LR
    recruiter[Recruiter / Reviewer]
    admin[Admin / Developer]
    system((Adaptive Resume Screener System))

    recruiter -->|Resume file, job description| system
    system -->|Screening result, scores, explanation, prediction ID| recruiter

    recruiter -->|Reviewed label, feedback note| system
    system -->|Feedback confirmation, retraining progress| recruiter

    admin -->|Health request, manual feature input, retraining status request| system
    system -->|Model status, model version, manual prediction, retraining status| admin
```

## 3. Data Flow Diagram Level 1

This Level 1 DFD expands the internal runtime flow, including the feedback-driven retraining loop.

```mermaid
flowchart TB
    recruiter[Recruiter / Reviewer]
    admin[Admin / Developer]

    P1((1. Capture Analyze Request))
    P2((2. Parse Resume File))
    P3((3. Analyze Resume and Extract Features))
    P4((4. Score with ML Model))
    P5((5. Build Screening Response))
    P6((6. Store Prediction))
    P7((7. Save Feedback))
    P8((8. Check Retraining Readiness))
    P9((9. Adaptive Retraining))

    D1[(D1: SQLite Predictions DB)]
    D2[(D2: Active Model Checkpoint)]
    D3[(D3: Model Registry Metadata)]

    recruiter -->|Resume file, job description| P1
    P1 -->|File bytes, filename| P2
    P1 -->|Job description text| P3
    P2 -->|Parsed resume text| P3

    P3 -->|ATS score, semantic score, matched/missing keywords, extracted features, 6D model features| P4
    P3 -->|Heuristic analysis outputs| P5
    D2 -->|Loaded PyTorch model| P4
    P4 -->|Probability, threshold, model decision| P5

    P5 -->|Prediction record payload| P6
    P6 -->|Insert prediction row| D1
    P5 -->|Analysis response| recruiter

    recruiter -->|Prediction ID, reviewed label, feedback note| P7
    P7 -->|Update reviewed fields| D1

    D1 -->|Labeled feedback count| P8
    P8 -->|Progress / ready message| recruiter
    admin -->|Retraining status request| P8
    P8 -->|Status response| admin

    admin -->|Manual feature vector| P4
    P4 -->|Manual prediction response| admin

    P8 -->|Ready for retraining| P9
    D1 -->|Labeled feature vectors| P9
    D3 -->|Current active model metadata| P9
    P9 -->|New model checkpoint| D2
    P9 -->|Updated model version and metrics| D3
    D2 -->|Reloaded model for future predictions| P4
```

## 4. Entity-Relationship (ER) Diagram

### 4A. ER Diagram As Implemented

The current relational schema has one core table: `predictions`.
Feedback is stored on the same record rather than in a separate `feedback` table.

```mermaid
erDiagram
    PREDICTIONS {
        INTEGER id PK
        TEXT created_at
        REAL years_experience
        REAL skills_match_score
        REAL education_level
        REAL projects_count
        REAL github_activity_score
        REAL certifications_count
        REAL probability
        TEXT decision
        REAL threshold
        TEXT model_version
        INTEGER reviewed_label
        TEXT reviewed_at
        TEXT feedback_note
        TEXT source
        TEXT resume_filename
        TEXT job_description
        TEXT resume_excerpt
        REAL ats_score
        REAL semantic_score
        REAL final_score
        TEXT matched_keywords_json
        TEXT missing_keywords_json
        TEXT explanation
        TEXT model_features_json
        REAL project_count
        REAL resume_length
        REAL github_activity
        TEXT extracted_features_json
        TEXT feature_order_json
        TEXT feature_profile
    }
```

### 4B. Normalized Conceptual ER Diagram

Use this version if you need a more textbook database design for a report, viva, or documentation artifact.
This is a conceptual redesign of the domain model, not the current SQLite implementation.

```mermaid
erDiagram
    CANDIDATE ||--o{ RESUME : owns
    RESUME ||--o{ PREDICTION : evaluated_for
    JOB_DESCRIPTION ||--o{ PREDICTION : compared_against
    MODEL_VERSION ||--o{ PREDICTION : generates
    PREDICTION ||--o| FEEDBACK : receives

    CANDIDATE {
        INT candidate_id PK
        STRING full_name
        STRING email
        STRING phone
        DATETIME created_at
    }

    RESUME {
        INT resume_id PK
        INT candidate_id FK
        STRING file_name
        STRING file_type
        TEXT resume_text
        DATETIME uploaded_at
    }

    JOB_DESCRIPTION {
        INT job_description_id PK
        STRING job_title
        TEXT description_text
        DATETIME created_at
    }

    MODEL_VERSION {
        INT model_version_id PK
        STRING version_name
        STRING model_path
        FLOAT threshold
        DATETIME activated_at
    }

    PREDICTION {
        INT prediction_id PK
        INT resume_id FK
        INT job_description_id FK
        INT model_version_id FK
        FLOAT years_experience
        FLOAT skills_match_score
        FLOAT education_level
        FLOAT project_count
        FLOAT resume_length
        FLOAT github_activity
        FLOAT ats_score
        FLOAT semantic_score
        FLOAT final_score
        FLOAT probability
        STRING decision
        DATETIME created_at
    }

    FEEDBACK {
        INT feedback_id PK
        INT prediction_id FK
        INT reviewed_label
        TEXT feedback_note
        DATETIME reviewed_at
    }
```

## 5. High-Level System Architecture Block Diagram

```mermaid
flowchart LR
    user[Recruiter / Reviewer]
    browser[Web Frontend<br/>frontend/index.html + app.js<br/>or public/ assets]
    api[FastAPI Application<br/>backend/main.py]

    user --> browser
    browser -->|POST /analyze, POST /feedback, GET /health| api
    api -->|JSON responses| browser

    subgraph Backend[Backend Services]
        routes[API Routes]
        parser[ResumeParserService]
        analysis[ResumeAnalysisService]
        modelsvc[ModelService]
        repo[PredictionRepository]
        trigger[RetrainingTriggerService]
        retrainer[AdaptiveRetrainer]
    end

    api --> routes
    routes --> parser
    routes --> analysis
    routes --> modelsvc
    routes --> repo
    routes --> trigger
    routes --> retrainer

    parser -->|Resume text| analysis
    analysis -->|6 derived features + heuristic scores| modelsvc

    subgraph Storage[Storage and Model Assets]
        db[(SQLite DB<br/>database/resume_screening.db)]
        model[(PyTorch model files<br/>ml/models/*.pt)]
        registry[(Model registry<br/>ml/models/registry/metadata.json)]
    end

    repo <--> db
    modelsvc <--> model
    db -->|Reviewed samples| retrainer
    trigger -->|Minimum feedback threshold| retrainer
    retrainer <--> registry
    retrainer -->|Reload active model| modelsvc

    subgraph Offline[Offline Training Pipeline]
        raw[(Raw dataset<br/>data/raw/ai_resume_screening.csv)]
        prep[Preprocessing<br/>ml/preprocessing/preprocess_tabular.py]
        train[Training and evaluation<br/>ml/training/*.py]
    end

    raw --> prep --> train --> model
```

## Notes and Assumptions

- The most important runtime flow is `POST /analyze`, because that is what the frontend uses.
- `POST /predict` is included as an admin/developer style manual prediction use case because it accepts direct feature vectors.
- Section 4A is intentionally "as implemented", while Section 4B is a normalized conceptual redesign for academic presentation.
- Adaptive retraining is background-driven after feedback submission when the labeled-feedback threshold is met.
