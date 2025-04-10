from marshmallow import Schema, fields

from app.dao.models.genres import GenreSchema
from app.setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    password = fields.Str()
    role = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Pluck("GenreSchema", "name")
