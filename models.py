from app import db
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA, JSONB, SMALLINT, UUID, VARCHAR
from sqlalchemy import DateTime, Enum, Sequence, text
from datetime import datetime

class Sport(db.Model):
    __tablename__ = "sport"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String, unique=False, nullable=False)
    slug = db.Column("slug", db.String, unique=True, nullable=False)
    is_active = db.Column("is_active",SMALLINT(), default=1, nullable=False)

    @staticmethod
    def get_all_sports():
        query = "select * from sport"
        results = db.session.execute(query).all()
        return results

    @staticmethod
    def get_sports_id_by_slug(slug, is_active=False):
        query = f"select id, is_active from sport where slug = '{slug}'"
        if is_active:
            query = query + " and is_active = 1"
        results = db.session.execute(query).first()
        return results

    @staticmethod
    def filtered_sport(slug=None, name=None, is_active=None, slug_like=None, name_like=None, name_start=None, slug_start=None, event_threshold=None):
        query_filters = []
        query = f"select sport.id, sport.name, sport.slug from sport"
        if slug:
            slug_filter_query = f"slug='{slug}'"
            query_filters.append(slug_filter_query)

        if name:
            name_filter_query = f"sport.name='{name}'"
            query_filters.append(name_filter_query)

        if is_active:
            is_active_filter_query = f"sport.is_active='{is_active}'"
            query_filters.append(is_active_filter_query)
        
        if slug_like:
            slug_like_filter_query = f"sport.slug like '%{slug_like}%'"
            query_filters.append(slug_like_filter_query)
        
        if name_like:
            name_like_filter_query = f"sport.name like '%{name_like}%'"
            query_filters.append(name_like_filter_query)

        if name_start:
            name_start_filter_query = f"sport.name ~ '^{name_start}.*$'"
            query_filters.append(name_start_filter_query)

        if slug_start:
            slug_start_filter_query = f"sport.slug ~ '^{slug_start}.*$'"
            query_filters.append(slug_start_filter_query)
        
        if event_threshold:
            query_filters.append("event.is_active = 1")
            filters_query = " and ".join(query_filters)
            query = query + f" inner join event on sport.id = event.sport where {filters_query} group by sport.id, sport.name, sport.slug having count(event.id) >= {event_threshold}"
        else:
            filters_query = " where " + " and ".join(query_filters)
            query = query + filters_query
        results = db.session.execute(query)
        return results.all()


    @staticmethod
    def update_sports_by_id(sport_id, name=None, is_active=None):
        query_list = list()
        if name:
            name_query = f"name='{name}'"
            query_list.append(name_query)
        if is_active != None:
            active_query = f"is_active={is_active}"
            query_list.append(active_query)

        query = f"update sport set {','.join(query_list)} where id= {sport_id}"
        db.session.execute(query)
        db.session.commit()
    

    @staticmethod
    def create_sport(name, slug):
        query = f"insert into sport (name, slug, is_active) values ('{name}', '{slug}', 0)"
        db.session.execute(query)
        db.session.commit()
    


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String, unique=False, nullable=False)
    is_active = db.Column("is_active", SMALLINT(), default=1, nullable=False)
    type = db.Column("type",
            Enum(
                "preplay",
                "foreplay",
                name="event_type",
                create_type=False,
            ),
            nullable=False,
            server_default=text("'preplay'"),
        )

    sport = db.Column(db.Integer, db.ForeignKey("sport.id"), nullable=False)
    status = db.Column("status",
            Enum(
                "Pending",
                "Started",
                "Ended",
                "Cancelled",
                name="status",
                create_type=False,
            ),
            nullable=False,
            server_default=text("'Pending'"),
        )
    slug = db.Column("slug", db.String, unique=False, nullable=False)
    schedule_start = db.Column("schedule_start", DateTime, nullable=False)
    actual_start = db.Column("actual_start", DateTime, nullable=True)

    @staticmethod
    def get_all_events():
        query = "select * from event"
        results = db.session.execute(query).all()
        return results


    @staticmethod
    def get_event_by_slug(slug):
        query = f"select * from event where slug = '{slug}'"
        result = db.session.execute(query).first()
        return result
    
    @staticmethod
    def get_event_by_id(event_id):
        query = f"select * from event where id = {event_id}"
        result = db.session.execute(query).first()
        return result
    
    @staticmethod
    def create_event(name, slug, sport, schedule_start, sport_active_status):
        query = f"insert into event (name, slug, sport, schedule_start, is_active) values ('{name}', '{slug}', {sport}, '{schedule_start}', 0 )"
        db.session.execute(query)
        db.session.commit()

    
    @staticmethod
    def update_event(event_json, event_slug=None, event_id=None):
        if event_slug:
            event_obj = Event.get_event_by_slug(event_slug)
        elif event_id:
            event_obj = Event.get_event_by_id(event_id)

        if not event_obj:
            raise Exception("Invalid Event Slug")

        event_id = event_obj[0]
            
        query_list = list()

        if event_json.get("status"):
            query_list.append(f"status='{event_json.get('status')}'")
            if event_json.get("status") == "Started":
                current_utc_dt = datetime.utcnow()
                query_list.append(f"actual_start='{current_utc_dt}'")
        
        if event_json.get("is_active", None) != None:
            query_list.append(f"is_active={int(event_json.get('is_active'))}")
            if event_json.get("is_active", None) == 1:
                Sport.update_sports_by_id(event_obj[4], is_active=1)
            else:
                Event.check_all_events_is_active_for_sport(event_obj[4], event_id)

        if event_json.get("type"):
            if event_json.get("type") in ["preplay","foreplay"]:
                query_list.append(f"type='{event_json.get('type')}'")
            else:
                raise Exception("Invalid Event Type")
        
        if event_json.get("sport"):
            if event_json.get("sport") != event_obj[4]:
                Event.check_all_events_is_active_for_sport(event_obj[4])
                query_list.append(f"sport='{event_json.get('sport')}'")
                if not event_json.get("sport_status", None) == False:
                    Sport.update_sports_by_id(event_json.get("sport"), is_active=1)

        query = f"update event set {','.join(query_list)} where id = {event_id}"
        db.session.execute(query)
        db.session.commit()



    @staticmethod
    def check_all_events_is_active_for_sport(sport, event_id):
        query = f"select count(*) from event where is_active = 1 and sport = {sport} and id != {event_id}"
        result = db.session.execute(query).first()
        if result[0] == 0:
            Sport.update_sports_by_id(sport, is_active=0)
        else:
            Sport.update_sports_by_id(sport, is_active=1)


    @staticmethod
    def filtered_event(slug=None, name=None, name_start=None, slug_start=None, type=None, status=None, sport=None, schedule_start_from=None, schedule_start_to=None, selection_threshold=None):
        query_filters = []
        query = f"select event.id, event.name, event.is_active, event.type, event.sport, event.status, event.slug, event.schedule_start, event.actual_start  from event"
        if slug:
            slug_filter_query = f"event.slug='{slug}'"
            query_filters.append(slug_filter_query)
        
        if name:
            name_filter_query = f"event.name='{name}'"
            query_filters.append(name_filter_query)

        if type:
            type_filter_query = f"event.type='{type}'"
            query_filters.append(type_filter_query)
        
        if status:
            status_filter_query = f"event.status='{status}'"
            query_filters.append(status_filter_query)
        
        if sport:
            sport_id = Sport.get_sports_id_by_slug(sport)
            if sport_id:
                sport_filter_query = f"event.sport='{sport_id[0]}'"
                query_filters.append(sport_filter_query)
            else:
                raise Exception("Invalid Sport slug")
        
        if schedule_start_from and schedule_start_to:
            schedule_time_query = f"event.schedule_start BETWEEN '{schedule_start_from}' AND '{schedule_start_to}'"
            query_filters.append(schedule_time_query)

        if name_start:
            name_start_filter_query = f"event.name ~ '^{name_start}.*$'"
            query_filters.append(name_start_filter_query)

        if slug_start:
            slug_start_filter_query = f"event.slug ~ '^{slug_start}.*$'"
            query_filters.append(slug_start_filter_query)
        
        if selection_threshold:
            query_filters.append(f"selection.is_active = 1")
            filters_query = " and ".join(query_filters)
            query = query + f" inner join selection on event.id = selection.event where {filters_query} group by event.id, event.name, event.is_active, event.type, event.sport, event.status, event.slug, event.schedule_start, event.actual_start having count(selection.id) >= {selection_threshold}"
        else:
            filters_query = " where " + " and ".join(query_filters)
            query = query + filters_query

        results = db.session.execute(query)
        return results.all()

    @staticmethod
    def get_all_events_by_sport(sport_slug):
        query = f"select event.* from event join sport on event.sport = sport.id where sport.slug = '{sport_slug}'  and event.is_active = 1"
        result = db.session.execute(query).all()
        return result

class Selection(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String, unique=False, nullable=False)
    event = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    price = db.Column("price", db.Numeric(precision=10, scale=2), nullable=False)
    is_active = db.Column("is_active", SMALLINT(), default=1, nullable=False)
    outcome = db.Column("outcome", 
            Enum(
                "Unsettled",
                "Void",
                "Lose",
                "Win",
                name="outcome",
                create_type=False,
            ),
            nullable=False,
            server_default=text("'Unsettled'"),
        )

    @staticmethod
    def create_selections(name, event, price):
        query = f"insert into selection (name, event, price, is_active) values ('{name}', '{event}', '{price}', 1)"
        db.session.execute(query)
        db.session.commit()

        event_active_status = {"is_active":1}
        Event.update_event(event_active_status, event_id=event )
    
    @staticmethod
    def update_selections(id, update_selection_json):
        result = Selection.get_selection_by_id(id)
        if not result:
            raise Exception("Invalid Selection Id")

        query_list = list()

        if update_selection_json.get("name"):
            query_list.append(f"name='{update_selection_json.get('name')}'")

        if update_selection_json.get("event"):
            event_obj = Event.get_event_by_slug(update_selection_json.get("event"))
            if not event_obj:
                raise Exception("Invalid event slug")
            query_list.append(f"event='{event_obj[0]}'")
        
        if update_selection_json.get("price"):
            query_list.append(f"price={update_selection_json.get('price')}")
        
        if update_selection_json.get("outcome"):
            if update_selection_json.get("outcome") in ["Void", "Win", "Loose"]:
                query_list.append(f"is_active=0")
                Selection.check_for_active_selections_of_event(result[2], result[0])
            query_list.append(f"outcome='{update_selection_json.get('outcome')}'")


        query = f"update selection set {','.join(query_list)} where id = {id}"
        db.session.execute(query)
        db.session.commit()

        
    @staticmethod
    def check_for_active_selections_of_event(event_id, selection_id):
        query = f"select count(id) from selection where event = {event_id} and is_active=1 and id != {selection_id}"
        result = db.session.execute(query).first()
        if result[0] == 0:
            event_json = {"is_active":0}
            Event.update_event(event_id=event_id, event_json=event_json)

    @staticmethod
    def get_selection_by_id(selection_id):
        query = f"select * from selection where id = {selection_id}"
        result = db.session.execute(query).first()
        return result


    @staticmethod
    def get_all_selections():
        query = "select * from selection"
        result = db.session.execute(query).all()
        return result


    @staticmethod
    def filtered_selection(name=None, is_active=None, name_start=None, id=None, event = None, price_range_start=None, price_range_end=None, outcome=None):
        query_filters = []
        query = f"select * from selection where "

        if name:
            name_filter_query = f"name='{name}'"
            query_filters.append(name_filter_query)

        if is_active != None:
            is_active_filter_query = f"is_active='{is_active}'"
            query_filters.append(is_active_filter_query)
        
        if id:
            id_filter_query = f"id='{id}'"
            query_filters.append(id_filter_query)

        
        if outcome:
            outcome_filter_query = f"outcome='{outcome}'"
            query_filters.append(outcome_filter_query)
        
        if event:
            event_obj = Event.get_event_by_slug(event)
            if event_obj:
                sport_filter_query = f"event='{event_obj[0]}'"
                query_filters.append(sport_filter_query)
            else:
                raise Exception("Invalid Event slug")
        
        if price_range_start and price_range_end:
            price_query = f"price BETWEEN {price_range_start} AND {price_range_end}"
            query_filters.append(price_query)

        if name_start:
            name_start_filter_query = f"name ~ '^[{name_start}].*$'"
            query_filters.append(name_start_filter_query)


        filters_query = " and ".join(query_filters)
        query = query + filters_query
        results = db.session.execute(query)
        return results.all()
    
    @staticmethod
    def get_selections_from_event(event_slug):
        query = f"select selection.* from selection join event on selection.event = event.id where event.slug = '{event_slug}' and selection.is_active = 1"
        results = db.session.execute(query).all()
        return results

