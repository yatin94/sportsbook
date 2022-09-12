
from flask_restx import Resource
from flask import request
from functionalities.events import (create_new_event, 
                                update_events_record, 
                                get_filtered_event,
                                get_all_events, get_all_events_of_sport)


class EventList(Resource):
    """
    - Purpose: To get all events and filtered events  query param
        - query params
            - slug : To Get Record by slug
            - name : To get record by name
            - name_like : To Get record with matching name
            - slug_like : To get Record with matching slug
            - is_active: To get records with specific active status
    """

    def get(self, **kwargs):
        filter_args = request.args
        if len(filter_args):
            all_sports = get_filtered_event(**filter_args)
        else:        
            all_sports = get_all_events()
        return all_sports
    



class Event(Resource):
    """
    - Purpose: To Create Sport Record, Update sport record, and get sport by slug
    """

    def post(self, **kwargs):
        json_data = request.get_json(force=True)
        name = json_data['name']
        slug = json_data['slug']
        sport = json_data['sport']
        schedule_start = json_data['schedule_start']
        return create_new_event(name=name, slug=slug, sport=sport, schedule_start=schedule_start)
    

    def patch(self, slug, **kwargs):
        json_data = request.get_json(force=True)
        return update_events_record(slug, json_data)
    

    def get(self, slug=None, sport_slug=None):
        try:
            if slug:
                sports_record = get_filtered_event(slug)
                if sports_record:
                    sports_record = sports_record[0]
                else:
                    raise Exception("No Record Found")
            if sport_slug:
                sports_record = get_all_events_of_sport(sport_slug)

            return sports_record
        except Exception as exec:
            return {"errMsg":str(exec)}, 400

        