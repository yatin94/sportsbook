
from flask_restx import Api, Namespace
from resources.sports import SportList, Sport
from resources.events import Event, EventList
from resources.selections import Selection, SelectionList

def create_restful_api(app):

    api = Api(app, catch_all_404s=True)
    sports_ns = Namespace("Sports", description="CRUD APIs for Sports APIs")
    events_ns = Namespace("Events", description="CRUD APIs for Events APIs")
    selections_ns = Namespace("Selections", description="CRUD APIs for Selections APIs")




    api.add_namespace(sports_ns, path="/sports")
    api.add_namespace(events_ns, path="/events")
    api.add_namespace(selections_ns, path="/selections")




    sports_ns.add_resource(SportList, "")
    sports_ns.add_resource(Sport, "", "/<slug>" )


    events_ns.add_resource(EventList, "")
    events_ns.add_resource(Event, "", "/<slug>", "/get-by-sport/<sport_slug>")


    selections_ns.add_resource(SelectionList, "")
    selections_ns.add_resource(Selection, "", "/<selection_id>", "/get-by-event/<event_slug>")
