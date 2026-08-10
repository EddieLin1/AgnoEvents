import requests

EVENTBRITE_URL = "https://www.eventbrite.com/home/api/search/"

HEADERS = {
    "Content-Type": "application/json",
}



def get_eventbrite_events() -> dict:
    """
    Fetch events from Eventbrite for a specific place ID.

    Returns:
        dict: A dictionary containing the events data.
    """
    # Calgary place_id, as given
    PLACE_ID = "890458845"

    payload = {
        "placeId": PLACE_ID,
        "tab": "all",
    }

    response = requests.post(
        EVENTBRITE_URL,
        json=payload,
        headers=HEADERS,
        timeout=10,
    )

    if not response.ok:
        raise RuntimeError(
            f"Eventbrite returned {response.status_code}: {response.text[:1000]}"
        )

    data =  response.json()
    events = []
    for event in data.get("events", []):
        event_info = {
            "name": event.get("name", {}),
            "venue": event.get("primary_venue", {}).get("name"),
            "address": event.get("primary_venue", {}).get("address", {}).get("localized_address_display"),
            "start_date": event.get("start_date", {}),
            "start_time": event.get("start_time", {}),
            "ticket_availability": event.get("ticket_availability", {}).get("has_available_tickets"),
            "ticket_price": event.get("ticket_availability", {}).get("min_ticket_price", {}).get("display"),
        }
        events.append(event_info)

    return events

print(get_eventbrite_events())