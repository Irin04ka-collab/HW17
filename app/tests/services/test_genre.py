from unittest.mock import MagicMock

import pytest

from app.service.genres import GenreService
from app.tests.conftest import genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self,genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres)>0

    def test_create(self):
        genre_d = {
            "name":"horror"
        }
        genre = self.genre_service.create(genre_d)

        assert genre.id is not None

    def test_update(self):
        genre_d = {
            "id":3,
            "name": "horror"
        }
        genre = self.genre_service.update(genre_d)

        assert genre is not None
        assert genre.id == 3
        assert genre.name == "horror"

    def test_update_partial(self):
        genre_d = {
            "name": "horror"
        }
        genre = self.genre_service.update_partial(genre_d)

        assert genre is not None
        assert genre.name == "horror"

    def test_delete(self):
        self.genre_service.delete(1)

        # Проверяем, что delete был вызван с ID = 1
        self.genre_service.dao.delete.assert_called_once_with(1)

        # Теперь настраиваем поведение get_one, чтобы он вернул None (жанр удален)
        self.genre_service.dao.get_one = MagicMock(return_value=None)

        genre = self.genre_service.get_one(1)
        assert genre is None
