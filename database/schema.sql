CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    years_experience REAL NOT NULL,
    skills_match_score REAL NOT NULL,
    education_level REAL NOT NULL,
    projects_count REAL NOT NULL,
    github_activity_score REAL NOT NULL,
    certifications_count REAL NOT NULL,
    probability REAL NOT NULL,
    decision TEXT NOT NULL CHECK(decision IN ('shortlist', 'reject')),
    threshold REAL NOT NULL,
    model_version TEXT NOT NULL,
    reviewed_label INTEGER NULL CHECK(reviewed_label IN (0, 1)),
    reviewed_at TEXT NULL,
    source TEXT NOT NULL DEFAULT 'manual',
    resume_filename TEXT NULL,
    job_description TEXT NULL,
    resume_excerpt TEXT NULL,
    ats_score REAL NULL,
    semantic_score REAL NULL,
    final_score REAL NULL,
    matched_keywords_json TEXT NULL,
    missing_keywords_json TEXT NULL,
    explanation TEXT NULL,
    model_features_json TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_predictions_reviewed_label ON predictions(reviewed_label);
