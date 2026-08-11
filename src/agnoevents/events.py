import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()


def get_eventbrite_events_calgary() -> dict:
    """
    Fetch events from Eventbrite for a specific place ID.

    Returns:
        dict: A dictionary containing the events data.
    """

    EVENTBRITE_URL = "https://www.eventbrite.com/home/api/search/"

    HEADERS = {
        "Content-Type": "application/json",
    }

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
            "id": event.get("id"),
            "name": event.get("name", {}),
            "venue": event.get("primary_venue", {}).get("name"),
            "address": event.get("primary_venue", {}).get("address", {}).get("localized_address_display"),
            "start_date": event.get("start_date", {}),
            "start_time": event.get("start_time", {}),
            "ticket_availability": event.get("ticket_availability", {}).get("has_available_tickets"),
            "ticket_price": event.get("ticket_availability", {}).get("min_ticket_price", {}).get("display"),
            "url": event.get("url"),
        }
        events.append(event_info)

    return events


def get_ticketmaster_events_calgary() -> dict:

    TICKETMASTER_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

    api_key = os.environ["TICKETMASTER_API_KEY"]

    params = {
        "apikey": api_key,
        "city": "Calgary",
        "countryCode": "CA",
    }

    response = requests.get(TICKETMASTER_URL, params=params, timeout=10)
    if not response.ok:
        raise RuntimeError(
            f"Ticketmaster returned {response.status_code}: {response.text[:1000]}"
        )

    data = response.json().get("_embedded", {}).get("events", [])

    events = []

    for event in data:

        event_info = {
            "id": event.get("id"),
            "name": event.get("name"),
            "url": event.get("url"),
            "date_start": event.get("dates", {}).get("start", {}).get("localDate"),
            "time_start": event.get("dates", {}).get("start", {}).get("localTime"),
            "info": event.get("info"),
            "venue": event.get("_embedded", {}).get("venues", [{}])[0].get("name"),
            "location": event.get("_embedded", {}).get("venues", [{}])[0].get("address", {}).get("line1"),
        }
        events.append(event_info)
    return events

# this does not work because the Ticketmaster API lied to me and does not provide price information in the event details
# but it would work if it did, so I will leave it here for now in case they fix their API in the future
def get_ticketmaster_events_calgary_price(event_id: str) -> dict:
    TICKETMASTER_URL = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json"
    
    api_key = os.environ["TICKETMASTER_API_KEY"]
    
    params = {
        "apikey": api_key,
    }

    response = requests.get(TICKETMASTER_URL, params=params, timeout=10)

    if not response.ok:
        raise RuntimeError(
            f"Ticketmaster returned {response.status_code}: {response.text[:1000]}"
        )

    response = response.json()
    
    event_info = {
        "name": response.get("name"),
        "venue": response.get("_embedded", {}).get("venues", [{}])[0].get("address", {}).get("line1"),
        "price_min": response.get("priceRanges", [{}])[0].get("min"),
        "price_max": response.get("priceRanges", [{}])[0].get("max"),
        }
    return event_info
