from unittest.mock import MagicMock

import pytest

from app.dao.director import DirectorDAO
from app.dao.genre import GenreDAO
from app.dao.models.directors import Director
from app.dao.models.genres import Genre
from app.dao.models.movies import Movie
from app.dao.movie import MovieDAO


@pytest.fixture()
def director_dao():
    director_dao = MagicMock(spec_set=DirectorDAO)
    #spec_set=DirectorDAO предотвратит вызов реального __init__ у DirectorDAO и Pytest сразу выдаст ошибку, если метод отсутствует в реальном DirectorDAO.

    tarantino = Director(id=1, name="Quentin Tarantino")
    kubrick = Director(id=2, name="Stanley Kubrick")
    nolan = Director(id=3, name="Christopher Nolan")

    director_dao.get_one = MagicMock(return_value=tarantino)
    director_dao.get_all = MagicMock(return_value=[tarantino, kubrick])
    director_dao.create = MagicMock(return_value=tarantino)
    director_dao.update = MagicMock(return_value=nolan)
                           # (return_value=Director(id=3, name="Christopher Nolan")))
    director_dao.delete = MagicMock()

    return director_dao


@pytest.fixture()
def genre_dao():
    genre_dao = MagicMock(spec_set=GenreDAO)
    #spec_set=GenreDAO предотвратит вызов реального __init__ у DirectorDAO и Pytest сразу выдаст ошибку, если метод отсутствует в реальном DirectorDAO.

    comedy = Genre(id=1, name="comedy")
    thriller = Genre(id=2, name="thriller")
    horror = Director(id=3, name="horror")

    genre_dao.get_one = MagicMock(return_value=comedy)
    genre_dao.get_all = MagicMock(return_value=[comedy, thriller])
    genre_dao.create = MagicMock(return_value=comedy)
    genre_dao.update = MagicMock(return_value=horror)
                           # (return_value=Director(id=3, name="Christopher Nolan")))
    genre_dao.delete = MagicMock()

    return genre_dao


@pytest.fixture()
def movie_dao():
    movie_dao = MagicMock(spec_set=MovieDAO)
    #spec_set=MovieDAO предотвратит вызов реального __init__ у DirectorDAO и Pytest сразу выдаст ошибку, если метод отсутствует в реальном MovieDAO.

    eight = Movie(id=1, title="The Hateful Eight", description="description", trailer="trailer", year=2018, rating="", genre_id=4, director_id=2)
    guys = Movie(id=2, title="The Other Guys", description="description", trailer="trailer", year=1978, rating="", genre_id=17, director_id=3)
    django = Movie(id=3, title="Django Unchained", description="description", trailer="trailer", year=2012, rating="", genre_id=17, director_id=2)
    django_upd = Movie(id=3, title="Django Unchained updated", description="description updated", trailer="trailer updated", year=2013, rating="updated",
                   genre_id=4, director_id=3)
    django_part = Movie(id=3, title="Django Unchained", description="description", trailer="trailer", year=2012, rating="", genre_id=17, director_id=2)

    def update_side_effect(movie):
        """Обновляет данные в объекте movie."""
        django.title = movie.title
        django.description = movie.description
        django.trailer = movie.trailer
        django.year = movie.year
        django.rating = movie.rating
        django.genre_id = movie.genre_id
        django.director_id = movie.director_id
        return django  # Симуляция обновления

    movie_dao.get_one = MagicMock(return_value=eight)
    movie_dao.get_all = MagicMock(return_value=[eight, guys])
    movie_dao.create = MagicMock(return_value=django)
    movie_dao.update = MagicMock(side_effect=update_side_effect)
    movie_dao.delete = MagicMock()

    return movie_dao







