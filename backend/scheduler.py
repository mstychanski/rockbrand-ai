from icalendar import Calendar, Event
from datetime import datetime, timedelta
import uuid
import os

ICS_PATH = "data/events.ics"

def generate_calendar(events: list) -> str:
    cal = Calendar()
    cal.add('prodid', '-//RockBandAI Calendar//mxm.dk//')
    cal.add('version', '2.0')

    for e in events:
        event = Event()
        event.add('summary', e['title'])
        event.add('dtstart', e['date'])
        event.add('dtend', e['date'] + timedelta(hours=2))
        event.add('dtstamp', datetime.now())
        event['uid'] = f"{uuid.uuid4()}@rockbrand.ai"
        cal.add_component(event)

    with open(ICS_PATH, 'wb') as f:
        f.write(cal.to_ical())

    return ICS_PATH

def parse_event_input(raw_events):
    parsed_events = [
        {
            "title": ev["title"],
            "date": datetime.strptime(ev["date"], "%Y-%m-%d")
        } for ev in raw_events
    ]
    return parsed_events

if __name__ == "__main__":
    sample_events = [
        {"title": "Koncert w Krakowie", "date": datetime(2025, 7, 20)},
        {"title": "Premiera nowego singla", "date": datetime(2025, 7, 27)}
    ]
    generate_calendar(sample_events)