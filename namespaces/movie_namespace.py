import json

from flask import jsonify
from flask_restx import Namespace, Resource

from schema import MovieSchema
from model_db import db, Movie

# Создаем Namespace
movies_ns = Namespace('/movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        directors = db.session.query(Movie.title).all()
        directors_list = []
        for director in directors:
            directors_list.append(director[0])
        directors_json = json.dumps(directors_list)
        return directors_list, 200

    def post(self):
        pass

@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid:int):
        movie = Movie.query.get(mid)
        if movie is None:
            return "", 404
        return movie_schema.dump(movie), 200

    def put(self, mid:int):
        pass

    def delete(self, mid:int):
        pass

