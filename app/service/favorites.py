from app.dao.favorite import FavoriteDAO


class FavoriteService:
    def __init__(self, dao: FavoriteDAO):
        self.dao = dao

    def get_by_user_id(self, uid):
        return self.dao.get_by_user_id(uid).all()

    def get_by_user_and_movie(self, uid, mid):
        return self.dao.get_by_user_and_movie(uid, mid).first()

    def create(self, data):
        return self.dao.create(data)

    def delete(self, gid):
        self.dao.delete(gid)
