import calendar
import datetime
import os
import jwt

from flask_restx import abort

from app.service.users import UserService

secret = os.getenv("SECRET_KEY")
algo = os.getenv("JWT_ALGORITHM")

class AuthService:
    def __init__(self, user_service:UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.check_user(username, password, is_refresh)

        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def check_user(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)
        if user is None:
            abort(401, "Invalid username or password")

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(401, "Invalid username or password")

        return user

    def generate_access_token(self, user):

        min30 = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)

        data ={
            "username":user.username,
            "role":user.role,
            "exp": calendar.timegm(min30.timetuple())
        }
        access_token = jwt.encode(data, secret, algorithm=algo)

        return  access_token

    def generate_refresh_token(self, user):
        days130 = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=130)

        data = {
            "username":user.username,
            "role":user.role,
            "exp": calendar.timegm(days130.timetuple())
        }
        refresh_token = jwt.encode(data, secret, algorithm=algo)

        return refresh_token

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        username = data.get("username")

        tokens = self.generate_tokens(username, password=None, is_refresh=True)

        return tokens
