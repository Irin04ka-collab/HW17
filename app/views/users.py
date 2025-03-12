from flask import request
from flask_restx import Namespace, Resource, abort

from app.container import user_service
from app.dao.models.users import UserSchema
from app.utils.auth import admin_required
from app.utils.auth import auth_required

users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_ns.route('')
class UsersView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()
        users = users_schema.dump(all_users)
        return users, 200

    def post(self):
        req_json = request.json
        user_name = req_json.get("username", None)
        user_password = req_json.get("password", None)
        user_role = req_json.get("role", None)

        if user_service.get_by_username(user_name):
            abort(409, "User with this username already exists")

        if None in [user_name, user_password, user_role]:
            abort (400, "Username, role and password can't be null")

        user = user_service.create(req_json)
        return "", 201, {"Location": f"{request.base_url}/{user.id}"}


@users_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid: int):
        user = user_service.get_one(uid)
        if not user:
            abort(404, "User not found")

        return user_schema.dump(user), 200

    @admin_required
    def delete(self, uid: int):
        user = user_service.get_one(uid)
        if not user:
            abort(404, "User not found")

        user_service.delete(uid)
        return "", 204
