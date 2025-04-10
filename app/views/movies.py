from flask import request, jsonify
from flask_restx import Namespace, Resource

from app.container import movie_service
from app.dao.models.movies import movie_schema
from app.dao.models.movies import movies_schema
from app.utils.auth import auth_required, admin_required
from app.utils.movies import paginate_query

movies_ns = Namespace('movies')


@movies_ns.route('')
class MoviesView(Resource):
    @auth_required
    def get(self):

        filters = {
            "genre_id": request.args.get("genre_id"),
            "year": request.args.get("year"),
            "director_id": request.args.get("director_id"),
            "status": request.args.get("status")
        }

        # Filter out empty values from the dictionary and convert them to integers
        # This ensures that only valid filters will be passed to the database query
        filters = {k: v for k, v in filters.items() if v is not None}

        # If no filters were provided, return all movies
        if not filters:
            all_movies = movie_service.get_all()
            response = paginate_query(all_movies)
            return response, 200


        # Otherwise, apply filters to the query
        movies_by_filter = movie_service.get_query_by_filter(filters)
        response = paginate_query(movies_by_filter)
        return response, 200

    @admin_required
    def post(self):
        req_json = request.json

        # Create a new movie in the database
        # The data is taken from the request body (JSON)
        movie = movie_service.create(req_json)

        return "", 201, {"Location": f"/movies/{movie.id}"}


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid: int):
        # Retrieve a single movie from the database by its ID
        movie = movie_service.get_one(mid)

        # Serialize the movie object to JSON format and return it
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid: int):
        req_json = request.json
        req_json["id"] = mid

        # Fully update the movie with the provided data
        # This method requires all fields to be present in the request
        movie_service.update(req_json)

        # Return HTTP 204 No Content status
        return "", 204



    def patch(self, mid: int):
        req_json = request.json
        req_json["id"] = mid

        # Partially update the movie with the provided data
        # This method allows updating only specific fields
        movie_service.update_data_partial(req_json)

        # Return HTTP 204 No Content status
        return "", 204

    @admin_required
    def delete(self, mid: int):
        # Permanently delete the movie from the database
        movie_service.delete(mid)

        # Return HTTP 204 No Content status
        return "", 204