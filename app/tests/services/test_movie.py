from unittest.mock import MagicMock

import pytest

from app.dao.models.movies import Movie
from app.service.movies import MovieService
from app.tests.conftest import movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self,movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies)>0

    def test_create(self):
        movie_d = {
            "title":"Django Unchained",
            "description":"description",
            "trailer":"trailer",
            "year":2012,
            "rating":"",
            "genre_id":17,
            "director_id":2
        }
        movie = self.movie_service.create(movie_d)


        assert isinstance(movie, Movie)
        assert movie.id is not None
        assert isinstance(movie.year, int)
        assert isinstance(movie.genre_id, int)
        assert isinstance(movie.director_id, int)
        assert movie.title == movie_d["title"]
        assert movie.description == movie_d["description"]
        assert movie.trailer == movie_d["trailer"]
        assert movie.year == movie_d["year"]
        assert movie.rating == movie_d["rating"]
        assert movie.genre_id == movie_d["genre_id"]
        assert movie.director_id == movie_d["director_id"]

    def test_update(self):
        movie_d = {
            "title": "Django Unchained updated",
            "description": "description updated",
            "trailer": "trailer updated",
            "year": 2013,
            "rating": "updated",
            "genre_id": 4,
            "director_id": 3
        }
        movie = self.movie_service.update(movie_d)

        assert movie is not None
        assert movie.id == 3
        assert movie.title == movie_d["title"]
        assert movie.description == movie_d["description"]
        assert movie.trailer == movie_d["trailer"]
        assert movie.year == movie_d["year"]
        assert movie.rating == movie_d["rating"]
        assert movie.genre_id == movie_d["genre_id"]
        assert movie.director_id == movie_d["director_id"]

    def test_update_partial(self):
        movie_d = {
            "id":3,
            "title": "Django Unchained partial updated",
            "year": 2013
        }
        movie = self.movie_service.update_partial(movie_d)

        assert movie is not None
        assert movie.id == 3
        assert movie.title == "Django Unchained partial updated"
        assert movie.year == 2013
        assert movie.description == "description"   # Не изменилось
        assert movie.director_id == 2               # Не изменилось

    def test_delete(self):
        self.movie_service.delete(1)

        # Проверяем, что delete был вызван с ID = 1
        self.movie_service.dao.delete.assert_called_once_with(1)

        # Теперь настраиваем поведение get_one, чтобы он вернул None (фильм удален)
        self.movie_service.dao.get_one = MagicMock(return_value=None)

        movie = self.movie_service.get_one(1)
        assert movie is None
