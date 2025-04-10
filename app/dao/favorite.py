from app.dao.models.favorites import Favorite


class FavoriteDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, fid):
        return self.session.query(Favorite).get(fid)

    def get_by_user_id(self, uid):
        return self.session.query(Favorite).filter(Favorite.user_id == uid)

    def get_by_user_and_movie(self, uid, mid):
        return self.session.query(Favorite).filter(Favorite.user_id == uid, Favorite.movie_id == mid)

    def create(self, data):
        favorite = Favorite(**data)

        self.session.add(favorite)
        self.session.commit()

        return favorite

    def update(self, favorite):

        self.session.add(favorite)
        self.session.commit()

        return favorite


    def delete(self, fid):
        favorite = self.get_one(fid)
        self.session.delete(favorite)
        self.session.commit()