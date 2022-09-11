from calendar import c
from urllib import request


try:
    from config import app
    import unittest
    import json
    import psycopg2
    import datetime
except Exception as exec:
    print(f"Module missing {exec}")


global global_cleanup
global_cleanup = list()

# Unit Tests for Sports 

class SportTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.global_cleanup = list()

    @classmethod
    def tearDownClass(clas) -> None:
        print("Cleaning up")
        connection = psycopg2.connect(user="yatin",
                                  password="yatin",
                                  host="db",
                                  port="5432",
                                  database="sportsbook")

        cursor = connection.cursor()

        for query in clas.global_cleanup:
            cursor.execute(query)
            connection.commit()
        print("Cleanup successful")
    

    def test_create_sport(self):
        sport_data = {
                "name" : "Cricket",
                "slug": "cricket"
            }
        tester = app.test_client(self)
        response = tester.post("/sports", data=json.dumps(sport_data))
        statuscode = response.status_code
        self.global_cleanup.append("delete from sport where slug = 'cricket'")
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.json, {"message":"Sports Successfull Inserted"})
    
    def test_create_sport_same_slug_error(self):
        sport_data = {
                "name" : "Cricket",
                "slug": "cricket"
            }
        tester = app.test_client(self)
        response = tester.post("/sports", data=json.dumps(sport_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.json, {"errMessage":"Slug already exists"})

    def test_update_sport(self):
        sport_data = {
                "name" : "Cricket1",
            }
        tester = app.test_client(self)
        response = tester.patch("/sports/cricket", data=json.dumps(sport_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.json, {"message":"Sports Successfull Updated"})
    

    def test_update_sport_incorrect_slug(self):
        sport_data = {
                "name" : "Cricket1",
            }
        tester = app.test_client(self)
        response = tester.patch("/sports/cricket12", data=json.dumps(sport_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.json, {"errMessage":"Not a valid slug"})
    


    def test_get_sport_using_slug(self):
        tester = app.test_client(self)
        response = tester.get("/sports/cricket")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, dict)


    def test_get_sport_using_incorrect_slug(self):
        tester = app.test_client(self)
        response = tester.get("/sports/cricket12")
        statuscode = response.status_code
        self.assertEqual(response.json, {"errMsg":"No Record Found"})
        self.assertEqual(statuscode, 400)
        self.assertIsInstance(response.json, dict)


    def test_get_all_sports(self):
        tester = app.test_client(self)
        response = tester.get("/sports")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
    
    def test_get_all_sports_with_filter(self):
        tester = app.test_client(self)
        response = tester.get("/sports?name_start=Cr&slug_start=cr")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)




class EventTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.global_cleanup = list()
        sport_data = {
                "name" : "Cricket",
                "slug": "cricket"
            }
        tester = app.test_client(cls)
        response = tester.post("/sports", data=json.dumps(sport_data))
        cls.global_cleanup.append("delete from sport where slug = 'cricket'")
        cls.connection = psycopg2.connect(user="yatin",
                                password="yatin",
                                host="db",
                                port="5432",
                                database="sportsbook")

        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(clas) -> None:
        print("Cleaning up")
        clas.global_cleanup.reverse()

        for query in clas.global_cleanup:
            clas.cursor.execute(query)
            clas.connection.commit()

        print("Cleanup successful")


    def test_create_event(self):
        schedule_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        event_data = {
                "name" : "test Event",
                "sport" : "cricket",
                "slug" : "testEvent",
                "schedule_start": int(schedule_start.timestamp())
            }
        tester = app.test_client(self)
        response = tester.post("/events", data=json.dumps(event_data))
        statuscode = response.status_code
        self.global_cleanup.append("delete from event where slug = 'testEvent'")
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.json, {"message":"Event Created successfully"})
    
    def test_create_event_same_slug_error(self):
        schedule_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        event_data = {
                "name" : "test Event",
                "sport" : "cricket",
                "slug" : "testEvent",
                "schedule_start": int(schedule_start.timestamp())
            }
        tester = app.test_client(self)
        response = tester.post("/events", data=json.dumps(event_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.json, {"errMsg":"Slug already exists"})
    
    def test_update_event(self):
        event_data = {
                "name" : "test Event1",
                "status": "Started",
                "type": "foreplay"
            }
        tester = app.test_client(self)
        response = tester.patch("/events/testEvent", data=json.dumps(event_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.json, {"message":"Event Updated Successfully"})
        query = "select actual_start from event where slug = 'testEvent'"
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        self.assertNotEqual(record[0], None)

    def test_update_event_incorrect_slug(self):
        event_data = {
                "name" : "test Event1",
                "status": "Started",
                "type": "foreplay"
            }
        tester = app.test_client(self)
        response = tester.patch("/events/testEvent123", data=json.dumps(event_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.json, {"errMsg":"Invalid Event Slug"})
    


    def test_get_event_using_slug(self):
        tester = app.test_client(self)
        response = tester.get("/events/testEvent")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, dict)


    def test_get_event_using_incorrect_slug(self):
        tester = app.test_client(self)
        response = tester.get("/events/testEvent12")
        statuscode = response.status_code
        self.assertEqual(response.json, {"errMsg":"No Record Found"})
        self.assertEqual(statuscode, 400)
        self.assertIsInstance(response.json, dict)


    def test_get_event_by_sport(self):
        tester = app.test_client(self)
        response = tester.get("/events/get-by-sport/cricket")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)

    def test_get_all_events(self):
        tester = app.test_client(self)
        response = tester.get("/events")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
    
    def test_get_all_sports_with_filter(self):
        tester = app.test_client(self)
        response = tester.get("/events?status=Started&type=foreplay")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
    





class SelectionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.selection_id = 0
        cls.global_cleanup = list()
        sport_data = {
                "name" : "Cricket",
                "slug": "cricket"
            }
        tester = app.test_client(cls)
        response = tester.post("/sports", data=json.dumps(sport_data))
        cls.global_cleanup.append("delete from sport where slug = 'cricket'")

        schedule_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        event_data = {
                "name" : "test Event",
                "sport" : "cricket",
                "slug" : "testEvent",
                "schedule_start": int(schedule_start.timestamp())
            }
        tester = app.test_client(cls)
        response = tester.post("/events", data=json.dumps(event_data))
        cls.global_cleanup.append("delete from event where slug = 'testEvent'")

        cls.connection = psycopg2.connect(user="yatin",
                                password="yatin",
                                host="db",
                                port="5432",
                                database="sportsbook")

        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(clas) -> None:
        print("Cleaning up")
        clas.global_cleanup.reverse()

        for query in clas.global_cleanup:
            clas.cursor.execute(query)
            clas.connection.commit()

        print("Cleanup successful")


    def test_create_selection(self):
        event_data = {
                "name" : "Test Selection",
                "event" : "testEvent",
                "price" : 12.367
            }
        tester = app.test_client(self)
        response = tester.post("/selections", data=json.dumps(event_data))
        statuscode = response.status_code
        self.global_cleanup.append("delete from selection where name = 'test_selection'")
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.json, {"message":"Selection Created successfully"})
        query = "select event.is_active, sport.is_active from event join sport on event.sport = sport.id where event.slug = 'testEvent';"
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        self.global_cleanup.append(f"delete from selection where name =  'Test Selection'")
        self.assertEqual(record[0], 1)
        self.assertEqual(record[1], 1)
    


    def test_create_selection_invalid_event_slug(self):
        event_data = {
                "name" : "Test Selection",
                "event" : "asdasd123",
                "price" : 12.367
            }
        tester = app.test_client(self)
        response = tester.post("/selections", data=json.dumps(event_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.json, {"errMsg":"Invalid event slug"})


    def test_update_selection(self):
        event_data = {
                "name" : "Test Selection New",
                "price" : 12.452,
                "outcome" : "Win"
            }
        query = "select id from selection where name = 'Test Selection';"
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        tester = app.test_client(self)
        response = tester.patch(f"/selections/{record[0]}", data=json.dumps(event_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.json, {"message":"Selection Updated successfully"})
        query = "select event.is_active, sport.is_active from event join sport on event.sport = sport.id where event.slug = 'testEvent';"
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        self.assertEqual(record[0], 0)
        self.assertEqual(record[1], 0)
        self.global_cleanup.append(f"delete from selection where name =  'Test Selection New'")



    def test_update_event_incorrect_id(self):
        event_data = {
                "name" : "Test Selection New",
                "price" : 12.452,
                "outcome" : "Win"
            }
        tester = app.test_client(self)
        response = tester.patch(f"/selections/12345", data=json.dumps(event_data))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.json, {"errMsg":"Invalid Selection Id"})


    def test_get_event_using_id(self):
        query = "select id from selection where name = 'Test Selection';"
        self.cursor.execute(query)
        record = self.cursor.fetchone()

        tester = app.test_client(self)
        response = tester.get(f"/selections/{record[0]}")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)


    def test_get_selection_using_incorrect_id(self):
        tester = app.test_client(self)
        response = tester.get(f"/selections/123456")
        statuscode = response.status_code
        self.assertEqual(response.json, {"errMsg":"No Record Found"})
        self.assertEqual(statuscode, 400)
        self.assertIsInstance(response.json, dict)


    def test_get_selection_by_event(self):
        tester = app.test_client(self)
        response = tester.get("/selections/get-by-event/testEvent")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)

    def test_get_all_selections(self):
        tester = app.test_client(self)
        response = tester.get("/selections")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
    
    def test_get_all_sports_with_filter(self):
        tester = app.test_client(self)
        response = tester.get("/selections?outcome=Win&price_range_start=12&price_range_end=13")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    def test_get_all_events_greater_than_selection_threshold(self):
        tester = app.test_client(self)
        response = tester.get("/events?selection_threshold=1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
    
    def test_get_all_sports_greater_than_events_threshold(self):
        tester = app.test_client(self)
        response = tester.get("/sports?event_threshold=1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
    



if __name__ == "__main__":
    unittest.main()