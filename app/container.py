from app.dao.director import DirectorDAO
from app.dao.favorite import FavoriteDAO
from app.dao.genre import GenreDAO
from app.dao.movie import MovieDAO
from app.dao.user import UserDAO
from app.service.auth import AuthService
from app.service.directors import DirectorService
from app.service.favorites import FavoriteService
from app.service.genres import GenreService
from app.service.movies import MovieService
from app.service.users import UserService
from app.setup_db import db


genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)

movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)

user_dao = UserDAO(db.session)
user_service = UserService(user_dao)

auth_service = AuthService(user_service)

favorite_dao = FavoriteDAO(db.session)
favorite_service = FavoriteService(favorite_dao)
