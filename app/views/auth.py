from flask import request
from flask_restx import Namespace, Resource, abort

from app.container import auth_service, user_service
from app.utils.auth import is_valid_email

auth_ns = Namespace('auth')

@auth_ns.route('/register')
class AuthRegView(Resource):
    def post(self):
        data = request.json

        email = data.get("email", None)
        password = data.get("password", None)

        if not is_valid_email(email):
            abort(400, "The email address is not in a valid format")

        # Устанавливаем "user" по умолчанию, если role не передан
        data.setdefault("role", "user")

        if user_service.get_by_username(email):
            abort(409, "User with this email already exists")

        if None in [email, password]:
            abort(400, "Email and password are required")

        user = user_service.create(data)

        return {"message": f"User {user.email} created successfully"}, 201, {"Location": f"{request.base_url}/{user.id}"}

@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        data = request.json

        email = data.get("email", None)
        password = data.get("password", None)

        if None in [email, password]:
            abort(400, "Email and password are required")

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201


    def put(self):
        data = request.json
        token = data.get("refresh_token")

        if not token:
            abort(400, "Refresh token is missing")

        tokens = auth_service.approve_refresh_token(token)
        if not tokens:
            abort(401, "Invalid or expired refresh token")

        return tokens, 200