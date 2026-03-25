import sqlite3

from backend.services.prediction_repository import PredictionRepository


def test_save_feedback_persists_label_and_note(tmp_path):
    db_path = tmp_path / "resume_screening.db"
    repository = PredictionRepository(db_path)
    repository.initialize(schema_path="database/schema.sql")

    prediction_id = repository.save_prediction(
        features=[4.0, 82.0, 6.0, 3.0, 450.0, 2.0],
        result={"probability": 0.84, "decision": "shortlist", "threshold": 0.3},
        model_version="resume_net_test",
        source="manual",
        analysis_data={"feature_profile": "test_fixture"},
    )

    saved = repository.save_feedback(
        prediction_id=prediction_id,
        reviewed_label=1,
        feedback_note="Strong fit for the role.",
    )

    assert saved is True

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT reviewed_label, feedback_note, reviewed_at FROM predictions WHERE id = ?",
            (prediction_id,),
        )
        row = cursor.fetchone()

    assert row is not None
    assert row[0] == 1
    assert row[1] == "Strong fit for the role."
    assert row[2] is not None
