from fastapi import APIRouter
from app.loader import load_json, load_keyed_json

router = APIRouter(prefix="/api/events", tags=["Event Monitor"])


@router.get("/")
async def get_event_options():
    return load_json("eventMonitor/eventOptions.json")


@router.get("/{eventId}")
async def get_event(eventId: str):
    return load_keyed_json("eventMonitor/event.json", eventId)


@router.get("/{eventId}/trajectory")
async def get_trajectory(eventId: str):
    return load_keyed_json("eventMonitor/trajectory.json", eventId)


@router.get("/{eventId}/timeline")
async def get_timeline(eventId: str):
    return load_keyed_json("eventMonitor/timeline.json", eventId)


@router.get("/{eventId}/telemetry")
async def get_telemetry(eventId: str):
    return load_keyed_json("eventMonitor/telemetry.json", eventId)


@router.get("/{eventId}/diagnostics")
async def get_diagnostics(eventId: str):
    return load_keyed_json("eventMonitor/diagnostics.json", eventId)


@router.get("/{eventId}/intensity-distribution")
async def get_intensity_distribution(eventId: str):
    return load_keyed_json("eventMonitor/intensityDistribution.json", eventId)


@router.get("/{eventId}/risk-alerts")
async def get_risk_alerts(eventId: str):
    return load_keyed_json("eventMonitor/downstreamRiskAlerts.json", eventId)
