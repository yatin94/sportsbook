from cgitb import reset
from models import Selection,Event
from datetime import datetime



def create_selections_record(name, event, price):
    """
    - Purpose: To create a new event
    """
    try:
        event_obj = Event.get_event_by_slug(event)
        if not event_obj:
            raise Exception("Invalid event slug")
        event_id = event_obj[0]
        Selection.create_selections(name, event_id, price)
        return {"message": "Selection Created successfully"}
    except Exception as exec:
        return {"errMsg" : str(exec)}, 400



def get_all_selections():
    result = Selection.get_all_selections()
    result_json = [dict(id=i[0], name=i[1], event=i[2], price=str(i[3]), outcome=i[5]) for i in result]
    return result_json




def update_selections_record(id, selection_update_json):
    try:
        Selection.update_selections(id, selection_update_json)
        return {"message": "Selection Updated successfully"}
    except Exception as exec:
        return {"errMsg" : str(exec)}, 400




def get_filtered_selections(name=None, is_active=None, name_start=None, id=None, event = None, price_range_start=None, price_range_end=None, outcome=None, **kwargs):
    try:
        result = Selection.filtered_selection(name,is_active,name_start,id,event,price_range_start,price_range_end,outcome)
        result_json = [dict(id=i[0], name=i[1], event=i[2], price=str(i[3]), outcome=i[5]) for i in result]
        return result_json
    except Exception as exec:
        return {"errMsg" : str(exec)}, 400


def get_selection_from_events(event_slug):
    try:
        result = Selection.get_selections_from_event(event_slug)
        result_json = [dict(id=i[0], name=i[1], event=i[2], price=str(i[3]), outcome=i[5]) for i in result]
        return result_json
    except Exception as exec:
        return {"errMsg" : str(exec)}, 400
