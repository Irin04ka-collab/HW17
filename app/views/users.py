from flask import request
from flask_restx import Namespace, Resource, abort

from app.container import user_service
from app.dao.models.users import UserSchema, User
from app.utils.auth import admin_required, get_user_from_token
from app.utils.auth import auth_required

users_ns = Namespace('users')
user_ns = Namespace('user')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_ns.route('')
class UserView(Resource):
    @auth_required
    def get(self):
        user = get_user_from_token()  #получаем данные по пользователю из токена
        if not user:
            abort(404, "User not found")

        return {
            "email":user.email,
            "name":user.name,
            "surname":user.surname,
            "favorite_genre":user.favorite_genre
        }

    def patch(self):
        user = get_user_from_token()  #получаем данные по пользователю из токена
        user_id = user.id

        req_json = request.json

        user_service.update_data_partial(req_json, user_id)

        return {"message": f"User {user.email} updated successfully"}, 200


@user_ns.route('/password')
class UserPasswordView(Resource):
    @auth_required
    def put(self):
        user = get_user_from_token()  # получаем данные по пользователю из токена
        req_json = request.json

        password_1 = req_json.get("password_1")
        password_2 = req_json.get("password_2")

        if not password_1 or not password_2:
            abort(400, "Both password_1 and password_2 are required")

        if password_1 != password_2:
            abort(400, "Passwords do not match")

        if user_service.compare_passwords(user.password,password_1):
            abort(400, "The new password must be different from the old one.")

        user_service.update_password(user.id, password_1)
        return {"message": f"Password updated successfully"}, 200

@users_ns.route('')
class UsersView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()
        users = users_schema.dump(all_users)
        return users, 200

    def post(self):
        req_json = request.json

        user_email = req_json.get("email", None)
        user_password = req_json.get("password", None)

        # Устанавливаем "user" по умолчанию, если role не передан
        req_json.setdefault("role", "user")

        if user_service.get_by_username(user_email):
            abort(409, "User with this email already exists")

        if None in [user_email, user_password]:
            abort (400, "Email and password are required")

        user = user_service.create(req_json)
        return "", 201, {"Location": f"{request.base_url}/{user.id}"}

