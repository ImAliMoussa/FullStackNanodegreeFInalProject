import enum
from datetime import date

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Enum, Date

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
    Migrate(app, db)


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

    class Movie(db.Model):
        """
        Database model for a movie
        """
        id = Column(Integer, primary_key=True)
        title = Column(String)
        release_date = Column(Date, default=date.today)

        def insert(self):
            db.session.add(self)
            db.session.commit()

        def update(self):
            db.session.commit()

        def delete(self):
            db.session.delete(self)
            db.session.commit()

        def format(self):
            return f'Actor: \n{vars(self)}'


class Movie(db.Model):
    """
    Database model for a movie
    """
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date, default=date.today)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return f'Movie: \n{vars(self)}'
