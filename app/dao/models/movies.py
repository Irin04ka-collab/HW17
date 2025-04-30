from datetime import date

from app.setup_db import db
from marshmallow import Schema, fields, types, ValidationError


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")
    data_added = db.Column(db.Date, nullable=False, default=date.today, onupdate=None)


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    director_id = fields.Int()
    genre = fields.Pluck("GenreSchema", "name")
    director = fields.Pluck("DirectorSchema", "name")
    # data_added = fields.Date()

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

