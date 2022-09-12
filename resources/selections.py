
from flask_restx import Resource
from flask import request
from functionalities.selections import (get_all_selections, 
                            create_selections_record, 
                            update_selections_record,
                            get_filtered_selections,
                            get_selection_from_events)


class SelectionList(Resource):
    """
    - Purpose: To get all sports and filtered sports  query param
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
            all_sports = get_filtered_selections(**filter_args)
        else:        
            all_sports = get_all_selections()
        return all_sports


class Selection(Resource):
    """
    - Purpose: To Create Selection Record, Update selection record
    """

    def post(self, **kwargs):
        json_data = request.get_json(force=True)
        name = json_data['name']
        event = json_data['event']
        price = json_data['price']
        return create_selections_record(name=name, event=event, price=price)
    

    def patch(self, selection_id, **kwargs):
        json_data = request.get_json(force=True)
        return update_selections_record(selection_id, json_data)
    

    def get(self, selection_id= None , event_slug= None, **kwargs):
        try:
            if selection_id:
                selection_record = get_filtered_selections(id=selection_id)
            else:
                selection_record = get_selection_from_events(event_slug)
            if not selection_record:
                raise Exception("No Record Found")
            return selection_record
        except Exception as e:
            return {"errMsg": str(e)}, 400
        