import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from models.models import setup_db


class ApiTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = os.environ['DATABASE_TEST_PATH']
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    testingUsers = {
        'testingUser2@funnymail.com': 'BuQ3tUS3 :jbFAL',
        'testingUser3w@funnymail.com': 'y(1726854(b(-KY'
        }
    
    # def getUserToken(user_name):
    # # client id and secret come from LogIn (Test Client)! which has password enabled under "Client > Advanced > Grant Types > Tick Password"
    #     url = 'https://YOUR_AUTH0_DOMAIN/oauth/token' 
    #     headers = {'content-type': 'application/json'}
    #     password = testingUsers[user_name]
    #     parameter = { "client_id":"Jfjrl12w55uqcJswWmMhSm5IG2Qov8w2e", 
    #                 "client_secret": "3E5ZnqLFbPUppBLQiGDjB0H2GtXaLyaD26sdk2HmHrBXQaDYE453UCUoUHmt5nWWh",
    #                 "audience": 'AUTH0_AUDIENCE',
    #                 "grant_type": "password",
    #                 "username": userName,
    #                 "password": password, "scope": "openid" } 
    #     # do the equivalent of a CURL request from https://auth0.com/docs/quickstart/backend/python/02-using#obtaining-an-access-token-for-testing
    #     responseDICT = json.loads(requests.post(url, json=parameter, headers=headers).text)
    #     return responseDICT['access_token']

    # @memoize # memoize code from: https://stackoverflow.com/a/815160
    # def getUserTokenHeaders(userName='testingUser2@funnymail.com'):
    #     return { 'authorization': "Bearer " + getUserToken(userName)}     

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET /actors
    def test_get_actors(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actors"], {
            "1": "Science",
            "2": "Art",
        })

    def test_get_actors_fail(self):
        res = self.client().get("/actor-detail/100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")

    # GET /actors
    def test_get_actors(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actors"],
            [])
        self.assertEqual(len(data["actors"]), 10)
        self.assertEqual(data["movies"], {
            '1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'
        })

    def test_get_actors_by_page(self):
        res = self.client().get("/actors?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actors"], {
            '1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'
        })

    def test_get_actors_fail(self):
        res = self.client().get("/actors?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")

    # DELETE /actor/<int:question_id>
    def test_delete_actor(self):
        res = self.client().delete("/actor/10")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_delete_actor_fail(self):
        res = self.client().delete("/actor/100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable entity")


    # POST /actor
    def test_post_actor(self):
        res = self.client().post("/actor", json={
            "name": "Leonardo DiCaprio",
            "age": 49,
            "gender": "male",
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["message"], "Actor successfully created")
        self.assertTrue(data["success"])
    
    def test_post_actor_fail(self):
        res = self.client().post("/actor", json={
            "name": "Leonardo DiCaprio",
            "age": 49,
            "gender": "male"
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable entity")

    # PATCH /actor
    def test_patch_actor(self):
        res = self.client().patch("/actor", json={
            "id": 2,
            "name": "Angelina Jolie",
            "age": 48,
            "gender": "female",
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_patch_actor_fail(self):
        res = self.client().patch("/actor", json={
            "id": 200,
            "name": "Angelina Jolie",
            "age": 48,
            "gender": "female",
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()