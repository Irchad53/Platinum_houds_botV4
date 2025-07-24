import requests
from datetime import datetime, timedelta

def get_upcoming_races():
    url = "https://games.jikasports.com/Home/GetEventsByType"
    payload = {
        "bettingLayoutEnumValue": "1",
        "feedId": "4",
        "languageCode": "en",
        "name": "PlatinumHounds",
        "nextEventCount": "",
        "offset": 7200,
        "operatorGuid": "514e3877-45b4-4098-81b0-5cd15140197f",
        "primaryMarketClassIds": ["134", "135"],
        "sessionGuid": "f1e2d2c7-96ec-4f20-aeb1-fc30bb102669",
        "userInitiated": True
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    try:
        data = response.json()
    except Exception:
        print("Erreur parsing JSON.")
        return []

    upcoming = []
    for event in data.get("result", []):
        try:
            start_time = datetime.strptime(event["startTime"], "%Y-%m-%dT%H:%M:%SZ")
            dogs = [{"dog_name": comp["name"], "odds": comp["decimalOdds"]} for comp in event["competitors"]]
            upcoming.append({
                "race_id": event["eventId"],
                "start_time": start_time + timedelta(hours=2),  # UTC+2
                "dogs": dogs
            })
        except Exception as e:
            continue

    return upcoming
