import os
from http import HTTPStatus

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from auth import requires_auth, AuthError
from models import setup_db, Actor, GenderEnum, Movie


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
    @requires_auth(permission='get:actors')
    def get_actors():
        actors = Actor.query.all()
        actors_serialized = serialize_list(actors)
        return jsonify({"actors": actors_serialized}), HTTPStatus.OK

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
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
    @requires_auth(permission='delete:actors')
    def delete_actor(key: int):
        actor = Actor.query.get_or_404(key)
        actor.delete()
        return jsonify(success=True), HTTPStatus.OK

    @app.route('/actors/<int:key>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
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

    # Movie handlers

    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movies():
        movies = Movie.query.all()
        movies_serialized = serialize_list(movies)
        return jsonify({"movies": movies_serialized}), HTTPStatus.OK

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movie():
        json = request.get_json()

        title = json.get("title")

        # make sure all required data is present, else -> 400 error response
        if title is None:
            abort(HTTPStatus.BAD_REQUEST)

        # create new question and add commit to the db
        movie = Movie(title=title)
        movie.insert()

        return jsonify(success=True), HTTPStatus.OK

    @app.route('/movies/<int:key>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_actor(key: int):
        movie = Movie.query.get_or_404(key)
        movie.delete()
        return jsonify(success=True), HTTPStatus.OK

    @app.route('/movies/<int:key>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_actor(key: int):
        json = request.get_json()
        movie = Movie.query.get_or_404(key)

        title = json.get("title")
        if title is not None:
            movie.title = title

        movie.update()

        return jsonify(success=True), HTTPStatus.OK

    # Error handlers

    @app.errorhandler(AuthError)
    def auth_error_handler(e: AuthError):
        return (
            jsonify(
                {
                    "success": False,
                    "error": e.status_code,
                    "message": e.error.get("description"),
                }
            ),
            e.status_code,
        )

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

    @app.errorhandler(HTTPStatus.UNAUTHORIZED)
    def unauthorized_401(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": HTTPStatus.UNAUTHORIZED,
                    "message": HTTPStatus.UNAUTHORIZED.phrase,
                }
            ),
            HTTPStatus.UNAUTHORIZED,
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
