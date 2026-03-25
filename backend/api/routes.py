import logging

from fastapi import APIRouter, BackgroundTasks, Body, File, Form, HTTPException, Request, UploadFile

from backend.schemas.prediction import (
    AnalysisResponse,
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
    RetrainingStatusResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    model_service = getattr(request.app.state, "model_service", None)
    if model_service is None:
        return HealthResponse(
            status="degraded",
            model_loaded=False,
            device="unknown",
            threshold=0.0,
            model_version=None,
            auto_retrain_enabled=False,
        )

    return HealthResponse(
        status="ok" if model_service.is_loaded else "degraded",
        model_loaded=model_service.is_loaded,
        device=str(model_service.device),
        threshold=float(model_service.threshold),
        model_version=model_service.active_model_version,
        auto_retrain_enabled=bool(getattr(request.app.state, "auto_retrain_enabled", False)),
    )


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest, request: Request) -> PredictionResponse:
    model_service = getattr(request.app.state, "model_service", None)
    if model_service is None or not model_service.is_loaded:
        raise HTTPException(status_code=503, detail="Model service unavailable")

    features = payload.to_feature_vector()

    try:
        result = model_service.predict(features)
    except ValueError as exc:
        logger.warning("Invalid prediction payload: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed") from exc

    repository = getattr(request.app.state, "prediction_repository", None)
    if repository is not None:
        try:
            repository.save_prediction(
                features=features,
                result=result,
                model_version=model_service.active_model_version,
                source="manual",
                analysis_data={
                    "feature_profile": "legacy_manual_input",
                    "model_feature_order": [
                        "years_experience",
                        "skills_match_score",
                        "education_level",
                        "projects_count",
                        "github_activity_score",
                        "certifications_count",
                    ],
                },
            )
        except Exception:
            logger.exception("Prediction generated but failed to persist")

    return PredictionResponse(**result)


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    request: Request,
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResponse:
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="job_description cannot be empty")

    file_bytes = await resume.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded resume is empty")

    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Resume file too large. Max size is 5MB")

    parser_service = getattr(request.app.state, "resume_parser_service", None)
    analysis_service = getattr(request.app.state, "resume_analysis_service", None)
    model_service = getattr(request.app.state, "model_service", None)
    repository = getattr(request.app.state, "prediction_repository", None)

    if not parser_service or not analysis_service or not model_service or not repository:
        raise HTTPException(status_code=503, detail="Analysis services unavailable")

    try:
        parsed = parser_service.parse(file_bytes=file_bytes, filename=resume.filename or "")
        analysis = analysis_service.analyze(parsed.text, job_description)
        model_result = model_service.predict(analysis.model_features)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.exception("Resume parsing dependency error")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        logger.exception("Analyze flow failed")
        raise HTTPException(status_code=500, detail="Analyze flow failed") from exc

    blended_probability = round(
        (float(model_result["probability"]) + (float(analysis.final_score) / 100.0)) / 2.0,
        4,
    )
    screening_result = {
        "probability": blended_probability,
        "decision": "shortlist" if blended_probability >= float(model_result["threshold"]) else "reject",
        "threshold": float(model_result["threshold"]),
    }

    prediction_id = repository.save_prediction(
        features=analysis.model_features,
        result=screening_result,
        model_version=model_service.active_model_version,
        source="analyze",
        analysis_data={
            "resume_filename": resume.filename,
            "job_description": job_description,
            "resume_excerpt": parsed.text[:1200],
            "ats_score": analysis.ats_score,
            "semantic_score": analysis.semantic_score,
            "final_score": analysis.final_score,
            "matched_keywords": analysis.matched_keywords,
            "missing_keywords": analysis.missing_keywords,
            "explanation": analysis.explanation,
            "extracted_features": analysis.extracted_features,
            "feature_profile": "derived_resume_analysis",
            "model_probability": model_result["probability"],
            "model_decision": model_result["decision"],
            "model_feature_order": [
                "years_experience",
                "skills_match_score",
                "education_level",
                "project_count",
                "resume_length",
                "github_activity",
            ],
        },
    )

    return AnalysisResponse(
        prediction_id=prediction_id,
        probability=screening_result["probability"],
        decision=screening_result["decision"],
        threshold=screening_result["threshold"],
        ats_score=analysis.ats_score,
        semantic_score=analysis.semantic_score,
        final_score=analysis.final_score,
        extracted_features=analysis.extracted_features,
        matched_keywords=analysis.matched_keywords,
        missing_keywords=analysis.missing_keywords,
        explanation=analysis.explanation,
    )


@router.post("/feedback/{prediction_id}", response_model=FeedbackResponse)
def submit_feedback(
    prediction_id: int,
    request: Request,
    background_tasks: BackgroundTasks,
    payload: FeedbackRequest = Body(...),
) -> FeedbackResponse:
    repository = getattr(request.app.state, "prediction_repository", None)
    if repository is None:
        raise HTTPException(status_code=503, detail="Prediction repository unavailable")

    saved = repository.save_feedback(
        prediction_id=prediction_id,
        reviewed_label=payload.reviewed_label,
        feedback_note=payload.feedback_note,
    )
    if not saved:
        raise HTTPException(status_code=404, detail="Prediction record not found")

    auto_retrain_enabled = bool(getattr(request.app.state, "auto_retrain_enabled", False))
    adaptive_retrainer = getattr(request.app.state, "adaptive_retrainer", None)
    model_service = getattr(request.app.state, "model_service", None)
    retraining_service = getattr(request.app.state, "retraining_service", None)
    labeled_feedback_count = repository.labeled_feedback_count()
    retrain_available = False
    minimum_required = None
    message = "Feedback saved successfully."

    if retraining_service is not None:
        status = retraining_service.evaluate(labeled_feedback_count=labeled_feedback_count)
        retrain_available = status.ready
        minimum_required = status.minimum_required
        message = status.message

    logger.info(
        "Saved feedback for prediction_id=%s reviewed_label=%s retrain_available=%s labeled_feedback_count=%s",
        prediction_id,
        payload.reviewed_label,
        retrain_available,
        labeled_feedback_count,
    )

    if auto_retrain_enabled and adaptive_retrainer and model_service and retraining_service:
        background_tasks.add_task(
            adaptive_retrainer.maybe_retrain,
            repository,
            model_service,
            int(retraining_service.minimum_required),
        )

    return FeedbackResponse(
        prediction_id=prediction_id,
        saved=True,
        retrain_available=retrain_available,
        labeled_feedback_count=labeled_feedback_count,
        minimum_required=minimum_required,
        message=message,
    )


@router.get("/feedback/retraining-status", response_model=RetrainingStatusResponse)
def retraining_status(request: Request) -> RetrainingStatusResponse:
    repository = getattr(request.app.state, "prediction_repository", None)
    retraining_service = getattr(request.app.state, "retraining_service", None)

    if repository is None or retraining_service is None:
        raise HTTPException(status_code=503, detail="Feedback services unavailable")

    labeled_count = repository.labeled_feedback_count()
    status = retraining_service.evaluate(labeled_feedback_count=labeled_count)

    return RetrainingStatusResponse(
        ready=status.ready,
        labeled_feedback_count=status.labeled_feedback_count,
        minimum_required=status.minimum_required,
        message=status.message,
    )
