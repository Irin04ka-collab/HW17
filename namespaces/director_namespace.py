from flask import jsonify
from flask_restx import Namespace, Resource

from schema import DirectorSchema
from model_db import db, Director

# Создаем Namespace
directors_ns = Namespace('/directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        pass

