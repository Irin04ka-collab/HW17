from flask import request
from flask_restx import Namespace, Resource

from app.container import genre_service
from app.dao.models.genres import GenreSchema
from app.utils.auth import auth_required, admin_required

genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('')
class GenresView(Resource):
    @auth_required
    def get(self):
        all_genres = genre_service.get_all()
        return genres_schema.dump(all_genres), 200

    @admin_required
    def post(self):
        req_json = request.json
        genre_service.create(req_json)

        return "", 201


@genres_ns.route('/<gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid: int):
        genre = genre_service.get_one(gid)
        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, gid: int):
        req_json = request.json
        req_json["id"] = gid
        genre_service.update_data_partial(req_json)

        return "", 204

    @admin_required
    def delete(self, gid: int):
        genre_service.delete(gid)

        return "", 204