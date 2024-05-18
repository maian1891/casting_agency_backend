import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from models import setup_db


class ApiTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_TEST_PATH']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

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
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
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