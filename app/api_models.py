from flask_restx import fields

user_input_fields = {
    'name': fields.String(description='Имя'),
    'surname': fields.String(description='Фамилия'),
    'favorite_genre': fields.Integer(description='ID любимого жанра'),
}

user_output_fields = {
    "email": fields.String(required=True, example="my_email@gmail.com"),
    'name': fields.String(description='Имя'),
    'surname': fields.String(description='Фамилия'),
    'favorite_genre': fields.Integer(description='ID любимого жанра'),
}

users_fields = {
    "id": fields.Integer(required=True, example=1),
    "email": fields.String(required=True, example="my_email@gmail.com"),
    "password": fields.String(required=True, example="my_secret_password"),
    "role": fields.String(required=True, example="user"),
    "name": fields.String(required=False, example="Alex"),
    "surname": fields.String(required=False, example="my_email@gmail.com"),
    "favorite_genre": fields.Integer(required=False, example=1)
}

change_password_fields = {
    'password': fields.String(required=True, description='Пароль'),
    'confirmed_password': fields.String(required=True, description='Подтвердите пароль'),
}

auth_fields = {
    'email': fields.String(required=True, description='Логин'),
    'password': fields.String(required=True, description='Пароль'),
}

genre_fields = {
    "id": fields.Integer(required=True, example=1),
    "name": fields.String(required=True, example="Комедия"),
}

director_fields = {
    "id": fields.Integer(required=True, example=1),
    "name": fields.String(required=True, example="Квентин Тарантино"),
}

favorite_fields = {
    "user_id": fields.Integer(required=True, description='ID пользователя'),
    "movie_id": fields.Integer(required=True, description='ID фильма'),
}

movie_fields = {
    "id": fields.Integer(required=True, example=1),
    "title": fields.String(required=True, example="Йеллоустоун"),
    "description": fields.String(required=False, example="Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»"),
    "trailer": fields.String(required=False, example=""),
    "year": fields.Integer(required=False, example=2018),
    "rating": fields.Integer(required=False, example=8),
    "genre_id": fields.Integer(required=False, example=17),
    "director_id": fields.Integer(required=False, example=1),
    # "genre": fields.Pluck("GenreSchema", "name"),
    # "director": fields.Pluck("DirectorSchema", "name")
}