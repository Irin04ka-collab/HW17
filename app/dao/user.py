from app.dao.models.users import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_by_username(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.name = user_d.get("name")
        user.surname = user_d.get("surname")
        user.favorite_genre = user_d.get("favorite_genre")
        user.password = user_d.get("password")

        self.session.add(user)
        self.session.commit()