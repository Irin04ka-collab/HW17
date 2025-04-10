from app.setup_db import db
from marshmallow import Schema, fields


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    movie = db.relationship("Movie")


class FavoriteSchema(Schema):
    user_id = fields.Int()
    movie_id = fields.Int()
