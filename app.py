import os
from http import HTTPStatus

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from models import setup_db, Actor, GenderEnum


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # setup using one of the config modules in config.py
    # create a APP_SETTINGS variable in .env file such as
    # APP_SETTINGS=config.DevelopmentConfig

    app.config.from_object(os.environ['APP_SETTINGS'])

    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET,PATCH,POST,DELETE,OPTIONS")
        return response

    @app.route('/')
    def default_route():
        """
        Just to test app is running
        """
        return 'Welcome to Agency'

    # Helper functions

    def serialize_list(model_list: list):
        """
        Each model should have a serialize attribute
        To return the data to the frontend serialized this function should be called
        to serialize a list of models
        """
        return [i.serialize for i in model_list]

    # Actor Routes

    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        actors_serialized = serialize_list(actors)
        return jsonify({"actors": actors_serialized}), HTTPStatus.OK

    @app.route('/actors', methods=['POST'])
    def post_actor():
        json = request.get_json()

        name = json.get("name")
        age = int(json.get("age"))
        gender = json.get("gender")

        # make sure all required data is present, else -> 400 error response
        if name is None or age is None or gender is None:
            abort(HTTPStatus.BAD_REQUEST)

        # create new question and add commit to the db
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify(success=True), HTTPStatus.OK

    @app.route('/actors/<int:key>', methods=['DELETE'])
    def delete_actor(key: int):
        actor = Actor.query.get_or_404(key)
        actor.delete()
        return jsonify(success=True), HTTPStatus.OK

    @app.route('/actors/<int:key>', methods=['PATCH'])
    def patch_actor(key: int):
        json = request.get_json()
        actor = Actor.query.get_or_404(key)

        name = json.get("name")
        if name is not None:
            actor.name = name

        age = json.get("age")
        if age is not None:
            actor.age = age

        gender = json.get("gender")
        if gender is not None:
            actor.gender = GenderEnum.transform(gender)

        actor.update()

        return jsonify(success=True), HTTPStatus.OK

    # Error handlers

    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request_400(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": HTTPStatus.BAD_REQUEST,
                    "message": HTTPStatus.BAD_REQUEST.phrase,
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found_404(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": HTTPStatus.NOT_FOUND,
                    "message": HTTPStatus.NOT_FOUND.phrase,
                }
            ),
            HTTPStatus.NOT_FOUND,
        )

    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    def unprocessable_entity_422(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": HTTPStatus.UNPROCESSABLE_ENTITY,
                    "message": HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                }
            ),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_server_error_500(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message": HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
