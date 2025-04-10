import base64
import hashlib
import hmac

from app.constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT
from app.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, email):
        return self.dao.get_by_username(email)

    def create(self, user_d):
        user_d["password"] = self.make_user_password_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update_password(self, user_id, new_password):
        user = self.get_one(user_id)
        user.password = self.make_user_password_hash(new_password)
        self.dao.session.commit()
        return user

    def update_data_partial(self, data, uid):
        user = self.get_one(uid)

        if "name" in data:
            user.name = data.get("name")
        if "surname" in data:
            user.surname = data.get("surname")
        if "favorite_genre" in data:
            user.favorite_genre = data.get("favorite_genre")
        self.dao.session.commit()
        return user

    def delete(self, rid):
        self.dao.delete(rid)

    def make_user_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, password_hash, other_password) -> bool:
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256', other_password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        )
