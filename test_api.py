from api import create_app
import os
import unittest
import json
from auth.auth import AuthError
        
assistant_token = os.environ['ASSISTANT_TOKEN']
director_token = os.environ['DIRECTOR_TOKEN']
producer_token = os.environ['PRODUCER_TOKEN']

class ApiTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = os.environ['DATABASE_TEST_PATH']

        self.app = create_app(self.database_path)
        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def getUserTokenHeaders(self, token=''):
        return { 'authorization': "Bearer " + token}     

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    # POST /actor
    def test_post_actor_unauthorized(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().post("/actor", json={
            "name": "Tom Hanks",
            "age": 67,
            "gender": "male",
        }, headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'unauthorized')
        self.assertFalse(data["success"])
    
    def test_post_actor_unprocessable_entity(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().post("/actor", json={
            "name": "Leonardo DiCaprio",
            "age": 49,
            "gender": "male"
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")
        
    def test_post_actor_success(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().post("/actor", json={
            "name": "Tom Hanks",
            "age": 67,
            "gender": "male",
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    # PATCH /actor
    def test_patch_actor_success(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().patch("/actor", json={
            "id": 1,
            "name": "Leonardo DiCaprio",
            "age": 49,
            "gender": "male",
        }, headers=headers)
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_patch_actor_unprocessable(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().patch("/actor", json={
            "id": 1,
            "name": "Tom Cruise",
            "age": 61,
            "gender": "male",
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    # DELETE /actor/<int:question_id>
    def test_delete_actor_unauthorized(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().delete("/actor/1", headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'unauthorized')
        self.assertFalse(data["success"])

    def test_delete_actor_resource_not_found(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().delete("/actor/100", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actor_success(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().delete("/actor/3", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], 3)

    # GET /actors
    def test_get_actors(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/actors",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
            [{'age': 49, 'gender': 'male', 'id': 1, 'name': 'Leonardo DiCaprio'}, 
             {'age': 61, 'gender': 'male', 'id': 2, 'name': 'Tom Cruise'}])
    
    # GET /actor-detail/:id
    def test_get_actor_detail_success(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/actor-detail/1", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
            {'age': 49, 'gender': 'male', 'id': 1, 'movies': [], 'name': 'Leonardo DiCaprio'})
    
    def test_get_actor_detail_not_found(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/actor-detail/100", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    # GET /movies
    def test_get_movies_success(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/movies",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
            [{'id': 1, 'releaseDate': 'Fri, 19 Dec 1997 00:00:00 GMT', 'title': 'Titanic'},
            {'id': 2, 'releaseDate': 'Wed, 22 May 1996 00:00:00 GMT', 'title': 'Mission: Impossible'}])
    
    # GET /movie-detail/:id
    def test_get_movie_detail_success(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/movie-detail/1", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"],
           {'actors': [], 'id': 1, 'releaseDate': 'Fri, 19 Dec 1997 00:00:00 GMT', 'title': 'Titanic'})
    
    def test_get_movie_detail_fail(self):
        headers = self.getUserTokenHeaders(assistant_token)
        res = self.client().get("/movie-detail/100", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    # POST /movie
    def test_post_movie_unauthorized(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().post("/movie", json={
            "title": "Toy Story",
            "releaseDate": 'Wed, 22 Nov 1995 00:00:00 GMT',
        }, headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'unauthorized')
        self.assertFalse(data["success"])
        
    def test_post_movie_success(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().post("/movie", json={
            "title": "Toy Story",
            "releaseDate": 'Wed, 22 Nov 1995 00:00:00 GMT'
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    # PATCH /movie
    def test_patch_movie_success(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().patch("/movie", json={
            "id": 1,
            "title": "Titanic 1",
            "releaseDate": 'Fri, 19 Dec 1997 00:00:00 GMT'
        }, headers=headers)
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_patch_movie_unprocessable(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().patch("/movie", json={
            "id": 1,
            "releaseDate": "Wed, 22 May 1996 00:00:00 GMT",
            "title": "Mission: Impossible"
        }, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")
    
    
    # DELETE /movie/<int:question_id>
    def test_delete_movie_unauthorized(self):
        headers = self.getUserTokenHeaders(director_token)
        res = self.client().delete("/movie/1", headers=headers)
        data = json.loads(res.data)

        self.assertRaises(AuthError)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], 'unauthorized')
        self.assertFalse(data["success"])

    def test_delete_movie_resource_not_found(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().delete("/movie/100", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie_success(self):
        headers = self.getUserTokenHeaders(producer_token)
        res = self.client().delete("/movie/3", headers=headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], 3)

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()