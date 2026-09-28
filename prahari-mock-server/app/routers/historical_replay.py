from fastapi import APIRouter
from app.loader import load_json, load_keyed_json

router = APIRouter(prefix="/api/historical-events", tags=["Historical Replay"])


@router.get("/")
async def get_historical_events():
    return load_json("historicalReplay/events.json")


# Comparison modes MUST be registered before /{eventId} to prevent route shadowing
@router.get("/comparison-modes")
async def get_comparison_modes():
    return load_json("historicalReplay/comparisonModes.json")


@router.get("/{eventId}")
async def get_selected_historical_event(eventId: str):
    return load_keyed_json("historicalReplay/selectedEvent.json", eventId)


@router.get("/{eventId}/timeline")
async def get_historical_timeline(eventId: str):
    return load_keyed_json("historicalReplay/timeline.json", eventId)


@router.get("/{eventId}/track")
async def get_historical_track(eventId: str):
    return load_keyed_json("historicalReplay/track.json", eventId)


@router.get("/{eventId}/hazard-envelope")
async def get_historical_hazard_envelope(eventId: str):
    return load_keyed_json("historicalReplay/hazardEnvelope.json", eventId)


@router.get("/{eventId}/map-layers")
async def get_historical_map_layers(eventId: str):
    return load_keyed_json("historicalReplay/mapLayers.json", eventId)


@router.get("/{eventId}/metrics")
async def get_historical_metrics(eventId: str):
    return load_keyed_json("historicalReplay/metrics.json", eventId)
