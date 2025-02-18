from flask_restx import Namespace, Resource

from app.container import genre_service
from app.dao.models.genres import GenreSchema

genres_ns = Namespace('/genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = genre_service.get_all()
        return genres_schema.dump(all_genres), 200


@genres_ns.route('/<gid>')
class GenreView(Resource):
    def get(self, gid: int):
        genre = genre_service.get_one(gid)
        return genre_schema.dump(genre), 200