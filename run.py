from app.config import Config
from model_db import db
from namespaces.director_namespace import directors_ns
from namespaces.movie_namespace import movies_ns
from namespaces.genre_namespace import genres_ns
from flask import Flask
from flask_restx import Api


def create_app(config: Config) -> Flask:

    application = Flask(__name__)
    application.config.from_object(config)
    return application

def configure_app(application: Flask):
    db.init_app(application)
    api = Api(application)

    api.add_namespace(directors_ns, path='/directors')
    api.add_namespace(movies_ns, path='/movies')
    api.add_namespace(genres_ns, path='/genres')


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)