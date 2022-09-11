
from flask_restx import Resource
from flask import request
from functionalities.sports import (get_all_sports, 
                            create_sports_record, 
                            update_sports_record,
                            get_filtered_sport,)


class SportList(Resource):
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
        print("Got Kwargs: %s", kwargs)
        filter_args = request.args
        if len(filter_args):
            all_sports = get_filtered_sport(**filter_args)
        else:        
            all_sports = get_all_sports()
        return all_sports
    

class Sport(Resource):
    """
    - Purpose: To Create Sport Record, Update sport record, and get sport by slug
    """

    def post(self, **kwargs):
        json_data = request.get_json(force=True)
        print("Creating a sport entity")
        name = json_data['name']
        slug = json_data['slug']
        return create_sports_record(name=name, slug=slug)
    

    def patch(self, slug, **kwargs):
        json_data = request.get_json(force=True)
        print("Updating the sports entity")
        name = json_data['name']
        return update_sports_record(slug, name)
    

    def get(self, slug, **kwargs):
        sports_record = get_filtered_sport(slug, **kwargs)
        if sports_record:
            return sports_record[0]
        return {"errMsg": "No Record Found"}, 400
