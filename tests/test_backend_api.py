from fastapi.testclient import TestClient

from backend.main import create_app


class DummyModelService:
    def __init__(self):
        self.is_loaded = True
        self.device = "cpu"
        self.threshold = 0.6
        self.active_model_version = "resume_net_dummy"

    def predict(self, features):
        assert len(features) == 6
        return {
            "probability": 0.8123,
            "decision": "shortlist",
            "threshold": 0.6,
        }


class DummyRepository:
    def __init__(self):
        self.feedback_count = 0

    def save_prediction(self, features, result, model_version="resume_net_v1", source="manual", analysis_data=None):
        return 1

    def save_feedback(self, prediction_id, reviewed_label):
        if prediction_id != 1:
            return False
        self.feedback_count += 1
        return True

    def labeled_feedback_count(self):
        return self.feedback_count


class DummyRetrainingService:
    minimum_required = 100

    def evaluate(self, labeled_feedback_count):
        class Status:
            def __init__(self, count):
                self.ready = count >= 100
                self.labeled_feedback_count = count
                self.minimum_required = 100
                self.message = "ok"

        return Status(labeled_feedback_count)


class DummyParserService:
    class Parsed:
        text = "python developer with 4 years experience and github.com/test/repo"

    def parse(self, file_bytes, filename):
        return self.Parsed()


class DummyAnalysisService:
    class Result:
        def __init__(self):
            self.model_features = [4.0, 80.0, 2.0, 4.0, 480.0, 500.0]
            self.extracted_features = {
                "years_experience": 4.0,
                "skills_match_score": 80.0,
                "education_level": 2.0,
                "project_count": 4.0,
                "resume_length": 480.0,
                "github_activity": 500.0,
            }
            self.ats_score = 78.2
            self.semantic_score = 0.71
            self.final_score = 76.4
            self.matched_keywords = ["python", "fastapi"]
            self.missing_keywords = ["aws"]
            self.explanation = "test explanation"

    def analyze(self, resume_text, job_description):
        return self.Result()


def _build_test_client() -> TestClient:
    app = create_app(load_model_on_startup=False, initialize_db=False)
    app.state.model_service = DummyModelService()
    app.state.prediction_repository = DummyRepository()
    app.state.retraining_service = DummyRetrainingService()
    app.state.resume_parser_service = DummyParserService()
    app.state.resume_analysis_service = DummyAnalysisService()
    app.state.auto_retrain_enabled = False
    return TestClient(app)


def test_health_endpoint():
    client = _build_test_client()
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True
    assert body["model_version"] == "resume_net_dummy"


def test_predict_endpoint_success():
    client = _build_test_client()

    payload = {
        "years_experience": 6,
        "skills_match_score": 78,
        "education_level": 2,
        "projects_count": 8,
        "github_activity_score": 500,
        "certifications_count": 3,
    }
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["probability"] == 0.8123


def test_analyze_endpoint_success():
    client = _build_test_client()

    files = {
        "resume": ("resume.txt", b"Python FastAPI developer with projects and certifications.", "text/plain")
    }
    data = {"job_description": "Looking for Python FastAPI engineer with AWS experience."}

    response = client.post("/analyze", files=files, data=data)

    assert response.status_code == 200
    body = response.json()
    assert body["prediction_id"] == 1
    assert body["decision"] == "shortlist"
    assert body["ats_score"] == 78.2
    assert body["extracted_features"]["resume_length"] == 480.0


def test_feedback_and_retraining_status():
    client = _build_test_client()

    feedback_response = client.post("/feedback/1", json={"reviewed_label": 1})
    assert feedback_response.status_code == 200

    retraining_response = client.get("/feedback/retraining-status")
    assert retraining_response.status_code == 200
    body = retraining_response.json()
    assert body["labeled_feedback_count"] == 1


def test_analyze_validation_error_for_missing_job_description():
    client = _build_test_client()

    files = {"resume": ("resume.txt", b"resume", "text/plain")}
    response = client.post("/analyze", files=files, data={"job_description": "   "})
    assert response.status_code == 400
