import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.routes import router
from backend.core.logging_config import configure_logging
from backend.services.model_service import ModelService
from backend.services.prediction_repository import PredictionRepository
from backend.services.resume_analysis_service import ResumeAnalysisService
from backend.services.resume_parser_service import ResumeParserService
from feedback_loop.adaptive_retrainer import AdaptiveRetrainer
from feedback_loop.retraining_trigger import RetrainingTriggerService

configure_logging()
logger = logging.getLogger(__name__)

MODEL_PATH = "ml/models/resume_net.pt"
DB_PATH = "database/resume_screening.db"
SCHEMA_PATH = "database/schema.sql"


def _read_positive_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default

    try:
        value = int(raw)
    except ValueError:
        logger.warning("Invalid %s=%r. Falling back to default=%s", name, raw, default)
        return default

    if value <= 0:
        logger.warning("Non-positive %s=%r. Falling back to default=%s", name, raw, default)
        return default

    return value


def _read_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    logger.warning("Invalid %s=%r. Falling back to default=%s", name, raw, default)
    return default


def _read_float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        logger.warning("Invalid %s=%r. Falling back to default=%s", name, raw, default)
        return default


RETRAIN_MIN_FEEDBACK = _read_positive_int_env("RETRAIN_MIN_FEEDBACK", 100)
RETRAIN_AUTO_ENABLED = _read_bool_env("RETRAIN_AUTO_ENABLED", True)
RETRAIN_EPOCHS = _read_positive_int_env("RETRAIN_EPOCHS", 20)
RETRAIN_MIN_NEW_SAMPLES = _read_positive_int_env("RETRAIN_MIN_NEW_SAMPLES", RETRAIN_MIN_FEEDBACK)
RETRAIN_MIN_VAL_ACCURACY = _read_float_env("RETRAIN_MIN_VAL_ACCURACY", 0.55)
DEFAULT_THRESHOLD = _read_float_env("MODEL_THRESHOLD", 0.30)


def create_app(load_model_on_startup: bool = True, initialize_db: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.prediction_repository = PredictionRepository(DB_PATH)
        app.state.retraining_service = RetrainingTriggerService(minimum_required=RETRAIN_MIN_FEEDBACK)
        app.state.resume_parser_service = ResumeParserService()
        app.state.resume_analysis_service = ResumeAnalysisService()
        app.state.auto_retrain_enabled = RETRAIN_AUTO_ENABLED
        app.state.adaptive_retrainer = AdaptiveRetrainer(
            registry_path="ml/models/registry/metadata.json",
            models_dir="ml/models/registry",
            retrain_epochs=RETRAIN_EPOCHS,
            min_new_samples=RETRAIN_MIN_NEW_SAMPLES,
            min_validation_accuracy=RETRAIN_MIN_VAL_ACCURACY,
        )

        active_model_path = app.state.adaptive_retrainer.initialize_registry(default_model_path=MODEL_PATH)
        app.state.model_service = ModelService(
            model_path=active_model_path,
            threshold=DEFAULT_THRESHOLD,
        )

        logger.info("Retraining minimum feedback threshold=%s", RETRAIN_MIN_FEEDBACK)
        logger.info("Model decision threshold=%s", DEFAULT_THRESHOLD)
        logger.info(
            "Adaptive retraining enabled=%s epochs=%s min_new_samples=%s min_val_acc=%s",
            RETRAIN_AUTO_ENABLED,
            RETRAIN_EPOCHS,
            RETRAIN_MIN_NEW_SAMPLES,
            RETRAIN_MIN_VAL_ACCURACY,
        )

        if initialize_db:
            app.state.prediction_repository.initialize(schema_path=SCHEMA_PATH)

        if load_model_on_startup:
            try:
                app.state.model_service.load()
            except Exception:
                logger.exception("Failed to initialize model service")
                raise

        yield

    app = FastAPI(
        title="Adaptive Resume Screener API",
        version="2.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):  # pragma: no cover
        logger.exception("Unhandled server error")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    app.include_router(router)
    return app


app = create_app(load_model_on_startup=True, initialize_db=True)
