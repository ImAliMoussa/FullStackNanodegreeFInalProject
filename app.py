import os
from http import HTTPStatus

from flask import Flask, jsonify
from flask_cors import CORS

from models import setup_db


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
    def hello():
        return 'hello world'

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
