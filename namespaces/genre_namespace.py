import json

from flask import jsonify
from flask_restx import Namespace, Resource

from schema import GenreSchema
from model_db import db, Genre

# Создаем Namespace
genres_ns = Namespace('/genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        pass