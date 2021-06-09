import enum
from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    String,
    Integer,
    Enum,
    DateTime,
    ForeignKey
)

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

    @staticmethod
    def transform(gender: str):
        gender = gender.lower()
        if gender == 'male':
            return GenderEnum.male
        elif gender == 'female':
            return GenderEnum.female
        raise Exception('Gender should be "male" or "female"')

    @staticmethod
    def reverse_transform(gender):
        if gender == GenderEnum.male:
            return 'male'
        return 'female'


class Actor(db.Model):
    """
    Database model for an actor
    """
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(Enum(GenderEnum))
    movies = db.relationship('Job', backref='movie', lazy=True)

    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = GenderEnum.transform(gender)

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

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': GenderEnum.reverse_transform(self.gender)
        }


class Movie(db.Model):
    """
    Database model for a movie
    """
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime, default=datetime.utcnow)
    actors = db.relationship('Job', backref='actor', lazy=True)

    def __init__(self, title: str, release_date: datetime):
        self.title = title
        self.release_date = release_date

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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


class Job(db.Model):
    """
    Many-to-many relationship between actors and movies
    """
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    actor_id = Column(Integer, ForeignKey('actor.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, movie_id: int, actor_id: int):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return f'ActingJob: \n{vars(self)}'
