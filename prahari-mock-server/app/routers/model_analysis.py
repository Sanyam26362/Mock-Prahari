from fastapi import APIRouter
from app.loader import load_json

router = APIRouter(prefix="/api/model-analysis", tags=["Model Analysis"])


@router.get("/overview")
async def get_overview():
    return load_json("modelAnalysis/overview.json")


@router.get("/models")
async def get_models():
    return load_json("modelAnalysis/models.json")


@router.get("/pipeline")
async def get_pipeline():
    return load_json("modelAnalysis/pipeline.json")


@router.get("/configuration")
async def get_configuration():
    return load_json("modelAnalysis/configuration.json")


@router.get("/metrics")
async def get_metrics():
    return load_json("modelAnalysis/metrics.json")


@router.get("/verification")
async def get_verification():
    return load_json("modelAnalysis/verification.json")


@router.get("/track-error-chart")
async def get_track_error_chart():
    return load_json("modelAnalysis/trackErrorChart.json")


@router.get("/baseline-comparison")
async def get_baseline_comparison():
    return load_json("modelAnalysis/baselineComparison.json")
