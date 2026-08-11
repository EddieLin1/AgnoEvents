import requests
import sqlite_utils
import hashlib

DB_PATH = "agnoevents.db"

# generate a unique id for a record based on its content
def generate_unique_id(record: dict) -> str:
    key = f"{record.get('title')}|{record.get('address')}|{record.get('next_date_times')}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]  # return first 16 characters of the hash

# update events
def upsert_events(records: list[dict], db_path: str = DB_PATH, table_name: str = "events") -> None:

    # creates db if does not exist, and creates table if does not exist, and upserts records into table
    db = sqlite_utils.Database(db_path)
    table = db[table_name]

    # if there is no record then it means its new and generate a unique id for it, otherwise use the existing id
    for record in records:
        if "id" not in record:
            record["id"] = generate_unique_id(record)

    table.upsert_all(records, pk="id", alter=True)

# fetch events from Calgary Open Data API returns a list of dict
def get_calgary_events() -> list[dict]:

    CALGARY_EVENTS_API_URL = "https://data.calgary.ca/resource/n625-9k5x.json"

    response = requests.get(CALGARY_EVENTS_API_URL, timeout=10)

    if not response.ok:
        raise RuntimeError(
            f"Calgary API returned {response.status_code}: {response.text[:1000]}"
        )

    data = response.json()

    return data

def update_calgary_events() -> None:
    events = get_calgary_events()
    upsert_events(events)

