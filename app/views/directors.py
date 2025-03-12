from flask import request
from flask_restx import Namespace, Resource

from app.container import director_service
from app.dao.models.directors import DirectorSchema
from app.utils.auth import auth_required, admin_required

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@directors_ns.route('')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all()
        return directors_schema.dump(all_directors), 200

    @admin_required
    def post(self):
        req_json = request.json
        director_service.create(req_json)

        return "", 201

@directors_ns.route('/<did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did: int):
        director = director_service.get_one(did)
        return director_schema.dump(director), 200

    @admin_required
    def put(self, did:int):
        req_json = request.json
        req_json["id"] = did
        director_service.update(req_json)

        return "", 204

    @admin_required
    def delete(self, did:int):
        director_service.delete(did)

        return "", 204

