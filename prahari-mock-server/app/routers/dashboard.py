from fastapi import APIRouter
from app.loader import load_json

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/overview")
async def get_overview():
    return load_json("dashboard/overview.json")


@router.get("/kpis")
async def get_kpis():
    return load_json("dashboard/kpis.json")


@router.get("/anomaly-overview")
async def get_anomaly_overview():
    return load_json("dashboard/anomalyOverview.json")


@router.get("/active-anomalies")
async def get_active_anomalies():
    return load_json("dashboard/activeAnomalies.json")


@router.get("/forecast-timeline")
async def get_forecast_timeline():
    return load_json("dashboard/forecastTimeline.json")


@router.get("/processing-pipeline")
async def get_processing_pipeline():
    return load_json("dashboard/processingPipeline.json")
