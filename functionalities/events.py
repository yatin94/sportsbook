from models import Event, Sport
from functionalities.sports import get_sport_id_from_sports_slug
from datetime import datetime


def validate_event_slug(slug):
    """
    - Purpose:
    - Args:
    - Returns:
    """
    event_obj = Event.get_event_by_slug(slug)
    if event_obj:
        raise Exception("Slug already exists")

def validate_schedule_time(schedule_time):
    utc_dt =  datetime.utcfromtimestamp(schedule_time)
    current_utc_dt = datetime.utcnow()
    if current_utc_dt > utc_dt:
        raise Exception("Invalid Schedule Start Time")
    return utc_dt



def create_new_event(name, slug, sport, schedule_start):
    """
    - Purpose: To create a new event
    """
    try:
        validate_event_slug(slug=slug)
        sports_id, sport_active_status = get_sport_id_from_sports_slug(slug=sport)
        schedule_start = validate_schedule_time(schedule_start)
        Event.create_event(name, slug, sports_id, schedule_start, sport_active_status)

        return {"message": "Event Created successfully"}
    except Exception as exec:
        return {"errMsg" : str(exec)}, 400



def update_events_record(slug, events_json):
    """
    - Purpose: To Update the events
    """
    try:

        if events_json.get("sport"):
            events_json["sport"], events_json['sport_status'] = get_sport_id_from_sports_slug(slug=events_json.get("sport"))

        if events_json.get("schedule_start"):
            events_json["schedule_start"] = validate_schedule_time(events_json.get("schedule_start"))

        Event.update_event(events_json, event_slug=slug)
        return {"message": "Event Updated Successfully"}

    except Exception as exec:
        return {"errMsg" : str(exec)}, 400


def get_filtered_event(slug=None, name=None, name_start=None, slug_start=None, type=None, status=None, sport=None, schedule_start_from=None, schedule_start_to=None, selection_threshold=None, **kwargs):
    """
    - Purpose:
    - Args:
    - Returns:
    """
    if schedule_start_to and schedule_start_from:
        schedule_start_from = datetime.utcfromtimestamp(int(schedule_start_from))
        schedule_start_to = datetime.utcfromtimestamp(int(schedule_start_to))
    filtered_events = Event.filtered_event(slug, name, name_start, slug_start, type, status, sport, schedule_start_from, schedule_start_to, selection_threshold)
    filtered_events = [dict(id=i[0], name=i[1], type=i[3], sport=i[4], status=i[5], slug=i[6], schedule_start=str(i[7])) for i in filtered_events]
    return filtered_events



def get_all_events():
    """
    - Purpose:
    - Args:
    - Returns
        - all_sports(list)
    """
    all_events = Event.get_all_events()
    all_event_dict = [dict(id=i[0], name=i[1], type=i[3], sport=i[4], status=i[5], slug=i[6], schedule_start=str(i[7])) for i in all_events]
    return all_event_dict



def get_all_events_of_sport(sport_slug):
    """
    - Purpose: To get all events of a sport slug
    """
    event_records = Event.get_all_events_by_sport(sport_slug)
    all_sports_dict = [dict(id=i[0], name=i[1], type=i[3], sport=i[4], status=i[5], slug=i[6], schedule_start=str(i[7])) for i in event_records]
    return all_sports_dict