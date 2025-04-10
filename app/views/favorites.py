from flask import request
from flask_restx import Namespace, Resource, abort

from app.container import favorite_service, movie_service
from app.dao.models.favorites import Favorite, FavoriteSchema
from app.utils.auth import auth_required, get_user_from_token

favorites_ns = Namespace('favorites')
favorite_ns = Namespace('favorite')

favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)

@favorites_ns.route('')
class FavoritesView(Resource):
    @auth_required
    def get(self):
        user = get_user_from_token()  #получаем данные по пользователю из токена
        if not user:
            abort(404, "User not found")

        movies_by_user = favorite_service.get_by_user_id(user.id)

        return favorites_schema.dump(movies_by_user), 200

@favorites_ns.route('movies/<int:mid>')
class FavoritesMovieView(Resource):
    @auth_required
    def post(self, mid: int):
        movie = movie_service.get_one(mid)
        user = get_user_from_token()  # получаем данные по пользователю из токена
        if not user:
            abort(404, "User not found")

        if favorite_service.get_by_user_and_movie(user.id, mid):
            return {"message": f"Movie {movie.title} already marked as favorite movie for {user.name}"}, 200

        favorite_movie = favorite_service.create({
            "user_id": user.id,
            "movie_id": mid
        })

        return {"message": f"Movie {movie.title} added to favorite movies for {user.name}"}, 201

    def delete(self, mid: int):
        user = get_user_from_token()  # получаем данные по пользователю из токена
        if not user:
            abort(404, "User not found")

        favorite = favorite_service.get_by_user_and_movie(user.id, mid)
        favorite_service.delete(favorite.id)
        return "", 204



