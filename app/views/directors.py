from flask_restx import Namespace, Resource

from app.container import director_service
from app.dao.models.directors import DirectorSchema

directors_ns = Namespace('/directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = director_service.get_all()
        return directors_schema.dump(all_directors), 200

@directors_ns.route('/<did>')
class DirectorView(Resource):
    def get(self, did: int):
        director = director_service.get_one(did)
        return director_schema.dump(director), 200