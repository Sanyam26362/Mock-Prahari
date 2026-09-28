from fastapi import APIRouter
from app.loader import load_json, load_keyed_json

router = APIRouter(prefix="/api/event-detail", tags=["Event Detail"])


# Static /events route MUST be registered before dynamic /{eventId}
@router.get("/events")
async def get_event_detail_list():
    return load_json("eventDetail/events.json")


@router.get("/{eventId}")
async def get_selected_event_detail(eventId: str):
    return load_keyed_json("eventDetail/selectedEvent.json", eventId)


@router.get("/{eventId}/overview")
async def get_event_detail_overview(eventId: str):
    return load_keyed_json("eventDetail/overview.json", eventId)


@router.get("/{eventId}/map")
async def get_event_detail_map(eventId: str):
    return load_keyed_json("eventDetail/map.json", eventId)


@router.get("/{eventId}/metrics")
async def get_event_detail_metrics(eventId: str):
    return load_keyed_json("eventDetail/metrics.json", eventId)


@router.get("/{eventId}/hazard")
async def get_event_detail_hazard(eventId: str):
    return load_keyed_json("eventDetail/hazard.json", eventId)


@router.get("/{eventId}/alerts")
async def get_event_detail_alerts(eventId: str):
    return load_keyed_json("eventDetail/alerts.json", eventId)
