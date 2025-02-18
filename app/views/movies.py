from flask import request
from flask_restx import Namespace, Resource

from app.container import movie_service
from app.dao.models.movies import MovieSchema

movies_ns = Namespace('/movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = movie_service.get_all()
        filter = {}

        gid = request.args.get('genre_id')
        year = request.args.get('year')
        did = request.args.get('director_id')

        if gid is not None:
            filter['genre_id'] = int(gid)
        if year is not None:
            filter['year'] = int(year)
        if did is not None:
            filter['director_id'] = int(did)

        if not filter:
            return movies_schema.dump(all_movies), 200

        movies_by_filter = movie_service.get_all_by_filter(filter)
        return movies_schema.dump(movies_by_filter), 200


    def post(self):
        req_json = request.json
        movie_service.create(req_json)

        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        movie = movie_service.get_one(mid)

        return movie_schema.dump(movie), 200

    def put(self, mid: int):
        req_json = request.json
        req_json["id"] = mid
        movie_service.update(req_json)

        return "", 204

    def patch(self, mid: int):
        req_json = request.json
        req_json["id"] = mid
        movie_service.update_partial(req_json)

        return "", 204

    def delete(self, mid: int):
        movie_service.delete(mid)

        return "", 204