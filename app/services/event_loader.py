"""
Event loader service
Builds astronomy events from NASA APIs when database is empty
"""

from datetime import datetime, timedelta
from app.models import Event
from app.services.nasa import get_neo_feed


MAX_SEEDED_EVENTS = 20


def ensure_events_available():
    """
    Ensures events table has data for users.
    If table is empty, it loads events from NASA NEO feed.
    """

    existing_events = Event.get_upcoming(limit=1)

    if existing_events:
        return

    start_date = datetime.utcnow().date()
    end_date = start_date + timedelta(days=4)

    neo_data = get_neo_feed(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    for neo in neo_data[:MAX_SEEDED_EVENTS]:
        title = f"NEO Close Approach: {neo.get('name', 'Unknown object')}"

        hazard_label = "Potentially hazardous" if neo.get("is_hazardous") else "Not hazardous"

        description = (
            f"Estimated max diameter: {neo.get('diameter_km', 'n/a')} km. "
            f"Relative speed: {neo.get('velocity_kph', 'n/a')} km/h. "
            f"Safety status: {hazard_label}."
        )

        Event.create(
            title=title,
            description=description,
            event_date=neo.get("date"),
            event_type="Near-Earth Object"
        )
