from flask import request
from flask_restx import Namespace, Resource, abort

from app.container import auth_service, user_service

auth_ns = Namespace('auth')

@auth_ns.route('')
class AuthView(Resource):
    def post(self):
        data = request.json

        username = data.get("username", None)
        password = data.get("password", None)

        if None in [username, password]:
            abort(400, "Username or password is None")

        tokens = auth_service.generate_tokens(username, password)

        return tokens, 201


    def put(self):
        data = request.json
        token = data.get("refresh_token")

        if not token:
            abort(400, "Refresh token is required")

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201