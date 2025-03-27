from unittest.mock import MagicMock

import pytest

from app.service.directors import DirectorService
from app.tests.conftest import director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self,director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors)>0

    def test_create(self):
        director_d = {
            "name":"Christopher Nolan"
        }
        director = self.director_service.create(director_d)

        assert director.id is not None

    def test_update(self):
        director_d = {
            "id":3,
            "name": "Christopher Nolan"
        }
        director = self.director_service.update(director_d)

        assert director is not None
        assert director.id == 3
        assert director.name == "Christopher Nolan"

    def test_update_partial(self):
        director_d = {
            "name": "Christopher Nolan"
        }
        director = self.director_service.update_partial(director_d)

        assert director is not None
        assert director.name == "Christopher Nolan"

    def test_delete(self):
        self.director_service.delete(1)

        # Проверяем, что delete был вызван с ID = 1
        self.director_service.dao.delete.assert_called_once_with(1)

        # Теперь настраиваем поведение get_one, чтобы он вернул None (режиссер удален)
        self.director_service.dao.get_one = MagicMock(return_value=None)

        director = self.director_service.get_one(1)
        assert director is None
