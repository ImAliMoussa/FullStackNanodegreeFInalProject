import os
import unittest
from http import HTTPStatus

from dotenv import load_dotenv

from app import create_app
from config import TestingConfig


class Roles:
    casting_assistant = 'casting_assistant'
    casting_director = 'casting_director'
    executive_producer = 'executive_producer'


def create_token_header_dict(token: str):
    ret = {
        'Authorization': 'Bearer ' + token
    }
    return ret


class FlaskTestCase(unittest.TestCase):
    """This class represents the test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client

        self.tokens = {
            Roles.casting_assistant: create_token_header_dict(os.environ['CAST_ASSIST_TOKEN']),
            Roles.casting_director: create_token_header_dict(os.environ['CAST_DIR_TOKEN']),
            Roles.executive_producer: create_token_header_dict(os.environ['EXEC_PROD_TOKEN'])
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # tests for /actors
    # no tests where this route should fail
    def test_authorized_get_actors(self):
        for key in self.tokens:
            token = self.tokens[key]
            res = self.client().get("/actors", headers=token)
            json_data = res.get_json()
            self.assertEqual(res.status_code, HTTPStatus.OK)
            self.assertTrue(json_data.get("actors") is not None)

    def test_unauthorized_get_actors(self):
        res = self.client().get("/actors")
        self.assertEqual(res.status_code, HTTPStatus.UNAUTHORIZED)

    # tests for /movies
    # no tests where this route should fail
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

    # # successfully get request
    # def test_working_get_questions_with_page(self):
    #     num_pages = self.getNumberOfQuestionPages()
    #
    #     for page in range(1, num_pages + 1):
    #         res = self.client().get("/questions", query_string={"page": page})
    #         json_data = res.get_json()
    #         self.assertEqual(res.status_code, HTTPStatus.OK)
    #         self.assertGreater(len(json_data.get("questions")), 0)
    #         self.assertGreater(len(json_data.get("categories")), 0)
    #         self.assertGreater(json_data.get("total_questions"), 0)

    # def test_unsuccessful_delete(self):
    #     key_not_in_db = 999999
    #     res = self.client().delete(f"/questions/{key_not_in_db}")
    #     json_data = res.get_json()
    #
    #     self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
    #     self.assertEqual(json_data.get("message"), HTTPStatus.NOT_FOUND.phrase)
    #     self.assertFalse(json_data.get("success"))
    #
    # def test_successful_post_question(self):
    #     # get one of the categories
    #     setup_res = self.client().get("/questions")
    #     json_data = setup_res.get_json()
    #     category = list(json_data.get("categories"))[0]
    #     question = {
    #         "question": "Example question text",
    #         "answer": "YES!",
    #         "difficulty": 1,
    #         "category": category,
    #     }
    #
    #     res = self.client().post("/questions", json=question)
    #     self.assertEqual(res.status_code, HTTPStatus.OK)
    #     self.assertTrue(res.get_json().get("success"))
    #
    # # this request fails due to a missing required field
    # def test_unsuccessful_post_question(self):
    #     # category is a missing field
    #     question = {
    #         "question": "Example question text",
    #         "answer": "YES!",
    #         "difficulty": 1,
    #         # 'category': category
    #     }
    #
    #     res = self.client().post("/questions", json=question)
    #     json = res.get_json()
    #     self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
    #     self.assertEqual(json.get("message"), HTTPStatus.BAD_REQUEST.phrase)
    #     self.assertFalse(json.get("success"))
    #
    # # test search questions functionality
    # def test_search_functionality(self):
    #     body = {"searchTerm": "what"}
    #     res = self.client().post("/questions/search", json=body)
    #     json = res.get_json()
    #     self.assertEqual(res.status_code, HTTPStatus.OK)
    #     self.assertTrue(json.get("questions"))
    #     self.assertTrue(json.get("total_questions"))
    #
    # # test getting questions for a specific category
    # def test_get_category_questions(self):
    #     setup_res = self.client().get("/questions")
    #     json_data = setup_res.get_json()
    #     category = list(json_data.get("categories"))[0]
    #     res = self.client().get(f"categories/{category}/questions")
    #     json = res.get_json()
    #     questions = json.get("questions")
    #     for q in questions:
    #         self.assertEqual(q.get("category"), int(category))
    #     self.assertEqual(res.status_code, HTTPStatus.OK)
    #     self.assertGreater(len(questions), 0)
    #     self.assertGreater(json.get("total_questions"), 0)
    #
    # # test getting questions for unknown category
    # def test_get_unknown_category_questions(self):
    #     category = 9999
    #     res = self.client().get(f"categories/{category}/questions")
    #     json = res.get_json()
    #     self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
    #     self.assertFalse(json.get("success"))
    #     self.assertEqual(json.get("message"), HTTPStatus.NOT_FOUND.phrase)
    #
    #     self.assertFalse(json.get("questions"))
    #     self.assertFalse(json.get("total_questions"))
    #
    # # test quizzes that no question will be repeated
    # def test_quiz_no_category(self):
    #     tmp_res = self.client().get("/questions")
    #     tmp_json = tmp_res.get_json()
    #     # get total number of question -> num_questions
    #     # will make num_questions + 1 requests
    #     # all will produce status code 200
    #     # only the last one will return attribute question as None
    #     # which is not an error but signals the end of the quiz
    #     num_questions = int(tmp_json.get("total_questions"))
    #     previous_questions = []
    #     for i in range(num_questions + 1):
    #         data = {"previous_questions": previous_questions}
    #         res = self.client().post("/quizzes", json=data)
    #         json_res = res.get_json()
    #         question = json_res.get("question")
    #
    #         # always 200 OK status code
    #         self.assertEqual(res.status_code, HTTPStatus.OK)
    #
    #         if i < num_questions:
    #             self.assertTrue(json_res.get("question"))
    #             previous_questions.append(question.get("id"))
    #         else:
    #             self.assertFalse(json_res.get("question"))
    #
    # # same as last test but for a specific category
    # def test_quiz_with_category(self):
    #     setup_res = self.client().get("/questions")
    #     json_data = setup_res.get_json()
    #     category_id = list(json_data.get("categories"))[0]
    #     category = {"id": category_id}
    #     res = self.client().get(f"categories/{category_id}/questions")
    #     json = res.get_json()
    #     num_questions = int(json.get("total_questions"))
    #     previous_questions = []
    #     for i in range(num_questions + 1):
    #         data = {
    #             "previous_questions": previous_questions,
    #             "quiz_category": category
    #         }
    #         res = self.client().post("/quizzes", json=data)
    #         json_res = res.get_json()
    #         question = json_res.get("question")
    #
    #         # always 200 OK status code
    #         self.assertEqual(res.status_code, HTTPStatus.OK)
    #
    #         if i < num_questions:
    #             self.assertTrue(json_res.get("question"))
    #             previous_questions.append(question.get("id"))
    #         else:
    #             self.assertFalse(json_res.get("question"))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
