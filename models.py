import enum

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Enum

db = SQLAlchemy()


def setup_db(app):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


class GenderEnum(enum.Enum):
    """
    constraint gender to be one of:
        male
        female
    to avoid strings other than in the database
    """
    male = 1
    female = 2


class Actor(db.Model):
    """
    Database model for actor
    """
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(Enum(GenderEnum))
