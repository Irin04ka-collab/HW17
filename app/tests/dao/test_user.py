import pytest


class TestUserDAO:
    def test_get_one(self, user_dao):
        user = user_dao.get_one(1)

        assert user is not None
        assert user.id == 1

    def test_get_all(self,user_dao):
        users = user_dao.get_all()

        assert len()

