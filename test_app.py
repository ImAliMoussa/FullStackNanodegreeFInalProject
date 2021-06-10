import os
import unittest
from http import HTTPStatus

from dotenv import load_dotenv

from app import create_app
from config import TestingConfig

load_dotenv()


class Roles:
    casting_assistant = 'casting_assistant'
    casting_director = 'casting_director'
    executive_producer = 'executive_producer'


def create_token_header_dict(token: str):
    ret = {
        'Authorization': f'Bearer {token}'
    }
    return ret


class FlaskTestCase(unittest.TestCase):
    """This class represents the test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client

        # Get JWT tokens saved in .env file
        self.tokens = {
            Roles.casting_assistant: create_token_header_dict(os.environ['CAST_ASSIST_TOKEN']),
            Roles.casting_director: create_token_header_dict(os.environ['CAST_DIR_TOKEN']),
            Roles.executive_producer: create_token_header_dict(os.environ['EXEC_PROD_TOKEN'])
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Helper functions

    def getActors(self):
        # token could be any other token, all roles have get access
        token = self.tokens[Roles.executive_producer]

        res = self.client().get("/actors", headers=token)
        json_data = res.get_json()
        return json_data.get("actors")

    def getMovies(self):
        # token could be any other token, all roles have get access
        token = self.tokens[Roles.executive_producer]

        res = self.client().get("/movies", headers=token)
        json_data = res.get_json()
        return json_data.get("movies")

    def test_authorized_get_actors(self):
        """
        Test tokens of all roles can get actors from db
        """
        for key in self.tokens:
            token = self.tokens[key]
            res = self.client().get("/actors", headers=token)
            json_data = res.get_json()
            self.assertEqual(res.status_code, HTTPStatus.OK)
            self.assertTrue(json_data.get("actors") is not None)

    def test_unauthorized_get_actors(self):
        """
        Test a request with no JWT will not pass
        """
        res = self.client().get("/actors")
        self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED)

    # next 2 requests are similar to the 2 previous requests
    # but for a different route

    def test_authorized_get_movies(self):
        for key in self.tokens:
            token = self.tokens[key]
            res = self.client().get("/movies", headers=token)
            json_data = res.get_json()
            self.assertEqual(res.status_code, HTTPStatus.OK)
            self.assertTrue(json_data.get("movies") is not None)

    def test_unauthorized_get_movies(self):
        res = self.client().get("/movies")
        self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED)

    def test_authorized_post_movies(self):
        """
        Test posting to movies
        Case 1: Roles.casting_director JWT
        Case 2: Roles.executive_producer JWT
        Both should succeed
        """
        for key in [Roles.casting_director, Roles.executive_producer]:
            token = self.tokens[key]
            json_req_body = {
                "title": "Harry Potter"
            }
            res = self.client().post("/movies", headers=token, json=json_req_body)
            self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_unauthorized_post_movies(self):
        """
        Test posting to movies
        Case 1: Role of a casting assistant with JWT added as a bearer token
        Case 2: No bearer token
        Both should fail
        """
        for token in [self.tokens[Roles.casting_assistant], None]:
            json_req_body = {
                "title": "Harry Potter"
            }
            res = self.client().post("/movies", headers=token, json=json_req_body)
            self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED)

    def test_authorized_post_actors(self):
        """
        Test posting to movies
        Case 1: Roles.casting_director JWT
        Case 2: Roles.executive_producer JWT
        Both should succeed
        """
        for key in [Roles.casting_director, Roles.executive_producer]:
            token = self.tokens[key]
            json_req_body = {
                "name": "Ali Moussa",
                "age": 22,
                "gender": "male"
            }
            res = self.client().post("/actors", headers=token, json=json_req_body)
            self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_unauthorized_post_actors(self):
        """
        Test posting to movies
        Case 1: Role of a casting assistant with JWT added as a bearer token
        Case 2: No bearer token
        Both should fail
        """
        for token in [self.tokens[Roles.casting_assistant], None]:
            json_req_body = {
                "name": "Ali Moussa",
                "age": 22,
                "gender": "male"
            }
            res = self.client().post("/actors", headers=token, json=json_req_body)
            self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED)

    def test_authorized_delete_actors(self):
        """
        Only executive producer role is authorized to delete actors
        """
        token = self.tokens[Roles.executive_producer]
        actors = self.getActors()
        actor_to_delete = actors[0].get("id")
        route = f'/actors/{actor_to_delete}'
        res = self.client().delete(route, headers=token)
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_unauthorized_delete_actors(self):
        """
        3 Cases will be unauthorized to make deletes
        Case 1: Casting assistant
        Case 2: Casting director
        Case 3: No jwt
        """
        actors = self.getActors()
        actor_to_delete = actors[0].get("id")
        route = f'/actors/{actor_to_delete}'

        tokens = [
            self.tokens[Roles.casting_assistant],
            self.tokens[Roles.casting_director],
            None
        ]

        for token in tokens:
            res = self.client().delete(route, headers=token)
            self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
