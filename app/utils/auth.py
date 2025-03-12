import jwt
import os
from flask import request, abort
from functools import wraps
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def get_user_from_token():
    """Извлекает пользователя из токена"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, "Token is missing or invalid")

    token = auth_header.split("Bearer ")[-1].strip()

    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return user  # Возвращает декодированные данные пользователя
    except jwt.ExpiredSignatureError:
        abort(401, "Token has expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_user_from_token()  # Проверяем токен, но ничего не возвращаем
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_user_from_token()  # Получаем пользователя
        if user.get("role") != "admin":
            abort(403, "Admin role required")
        return func(*args, **kwargs)

    return wrapper