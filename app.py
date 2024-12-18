# app.py

from flask import Flask, request
from flask_restx import Api, Resource


def create_app():
    from namespaces.director_namespace import directors_ns
    from namespaces.movie_namespace import  movies_ns
    from namespaces.genre_namespace import genres_ns
    from model_db import db

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    api = Api(app)

    api.add_namespace(directors_ns, path='/directors')
    api.add_namespace(movies_ns, path='/movies')
    api.add_namespace(genres_ns, path='/genres')

    return app


