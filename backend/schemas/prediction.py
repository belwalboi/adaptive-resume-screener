from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    years_experience: float = Field(..., ge=0, le=60)
    skills_match_score: float = Field(..., ge=0, le=100)
    education_level: float = Field(..., ge=0, le=10)
    projects_count: float = Field(..., ge=0, le=100)
    github_activity_score: float = Field(..., ge=0, le=10000)
    certifications_count: float = Field(..., ge=0, le=100)

    def to_feature_vector(self) -> list[float]:
        return [
            self.years_experience,
            self.skills_match_score,
            self.education_level,
            self.projects_count,
            self.github_activity_score,
            self.certifications_count,
        ]


class PredictionResponse(BaseModel):
    probability: float = Field(..., ge=0.0, le=1.0)
    decision: str
    threshold: float = Field(..., ge=0.0, le=1.0)


class AnalysisResponse(BaseModel):
    prediction_id: int
    probability: float = Field(..., ge=0.0, le=1.0)
    decision: str
    threshold: float = Field(..., ge=0.0, le=1.0)
    ats_score: float = Field(..., ge=0.0, le=100.0)
    semantic_score: float = Field(..., ge=0.0, le=1.0)
    final_score: float = Field(..., ge=0.0, le=100.0)
    extracted_features: dict
    matched_keywords: list[str]
    missing_keywords: list[str]
    explanation: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str
    threshold: float
    model_version: str | None = None
    auto_retrain_enabled: bool = False


class FeedbackRequest(BaseModel):
    reviewed_label: int = Field(..., ge=0, le=1)


class FeedbackResponse(BaseModel):
    prediction_id: int
    saved: bool


class RetrainingStatusResponse(BaseModel):
    ready: bool
    labeled_feedback_count: int
    minimum_required: int
    message: str
