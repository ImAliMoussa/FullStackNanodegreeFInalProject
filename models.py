from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
