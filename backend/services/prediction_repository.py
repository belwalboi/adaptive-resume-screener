import json
import sqlite3
from pathlib import Path


class PredictionRepository:
    EXTRA_COLUMNS = [
        ("source", "TEXT NOT NULL DEFAULT 'manual'"),
        ("resume_filename", "TEXT"),
        ("job_description", "TEXT"),
        ("resume_excerpt", "TEXT"),
        ("ats_score", "REAL"),
        ("semantic_score", "REAL"),
        ("final_score", "REAL"),
        ("matched_keywords_json", "TEXT"),
        ("missing_keywords_json", "TEXT"),
        ("explanation", "TEXT"),
        ("model_features_json", "TEXT"),
        ("project_count", "REAL"),
        ("resume_length", "REAL"),
        ("github_activity", "REAL"),
        ("extracted_features_json", "TEXT"),
        ("feature_order_json", "TEXT"),
        ("feature_profile", "TEXT"),
    ]

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)

    def initialize(self, schema_path: str | Path) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        schema_sql = Path(schema_path).read_text(encoding="utf-8")
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema_sql)
            self._ensure_extra_columns(conn)
            self._ensure_indexes(conn)
            conn.commit()

    def _ensure_extra_columns(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(predictions)")
        existing = {row[1] for row in cursor.fetchall()}

        for column_name, column_type in self.EXTRA_COLUMNS:
            if column_name not in existing:
                cursor.execute(f"ALTER TABLE predictions ADD COLUMN {column_name} {column_type}")

    def _ensure_indexes(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_source ON predictions(source)")

    def save_prediction(
        self,
        features: list[float],
        result: dict,
        model_version: str = "resume_net_v1",
        source: str = "manual",
        analysis_data: dict | None = None,
    ) -> int:
        analysis_data = analysis_data or {}
        extracted_features = analysis_data.get("extracted_features") or {}

        project_count = extracted_features.get("project_count")
        resume_length = extracted_features.get("resume_length")
        github_activity = extracted_features.get("github_activity")
        legacy_projects_count = features[3]
        legacy_github_activity_score = features[4]
        legacy_certifications_count = features[5]

        if source == "manual":
            project_count = features[3]
            github_activity = features[4]
        else:
            legacy_github_activity_score = github_activity
            legacy_certifications_count = 0.0

        query = """
        INSERT INTO predictions (
            years_experience,
            skills_match_score,
            education_level,
            projects_count,
            github_activity_score,
            certifications_count,
            probability,
            decision,
            threshold,
            model_version,
            source,
            resume_filename,
            job_description,
            resume_excerpt,
            ats_score,
            semantic_score,
            final_score,
            matched_keywords_json,
            missing_keywords_json,
            explanation,
            model_features_json,
            project_count,
            resume_length,
            github_activity,
            extracted_features_json,
            feature_order_json,
            feature_profile
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    features[0],
                    features[1],
                    features[2],
                    legacy_projects_count,
                    legacy_github_activity_score,
                    legacy_certifications_count,
                    result["probability"],
                    result["decision"],
                    result["threshold"],
                    model_version,
                    source,
                    analysis_data.get("resume_filename"),
                    analysis_data.get("job_description"),
                    analysis_data.get("resume_excerpt"),
                    analysis_data.get("ats_score"),
                    analysis_data.get("semantic_score"),
                    analysis_data.get("final_score"),
                    json.dumps(analysis_data.get("matched_keywords", [])),
                    json.dumps(analysis_data.get("missing_keywords", [])),
                    analysis_data.get("explanation"),
                    json.dumps(features),
                    project_count,
                    resume_length,
                    github_activity,
                    json.dumps(extracted_features) if extracted_features else None,
                    json.dumps(analysis_data.get("model_feature_order", [])),
                    analysis_data.get("feature_profile"),
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def save_feedback(self, prediction_id: int, reviewed_label: int) -> bool:
        query = """
        UPDATE predictions
        SET reviewed_label = ?, reviewed_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (reviewed_label, prediction_id))
            conn.commit()
            return cursor.rowcount > 0

    def labeled_feedback_count(self) -> int:
        query = "SELECT COUNT(*) FROM predictions WHERE reviewed_label IS NOT NULL"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return int(row[0] if row else 0)

    def fetch_labeled_samples(self) -> list[tuple[list[float], int]]:
        query = """
        SELECT
            years_experience,
            skills_match_score,
            education_level,
            projects_count,
            github_activity_score,
            certifications_count,
            reviewed_label,
            model_features_json
        FROM predictions
        WHERE reviewed_label IS NOT NULL
        """

        samples: list[tuple[list[float], int]] = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            label = int(row[6])
            serialized_features = row[7]
            features: list[float]
            if serialized_features:
                try:
                    decoded = json.loads(serialized_features)
                    if isinstance(decoded, list) and len(decoded) == 6:
                        features = [float(v) for v in decoded]
                    else:
                        raise ValueError("Invalid serialized feature vector")
                except Exception:
                    features = [float(v) for v in row[:6]]
            else:
                features = [float(v) for v in row[:6]]

            samples.append((features, label))

        return samples
