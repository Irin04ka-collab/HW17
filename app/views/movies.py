from flask import request
from flask_restx import Namespace, Resource

from app.container import movie_service
from app.dao.models.movies import MovieSchema
from app.utils.auth import auth_required, admin_required

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movies_ns.route('')
class MoviesView(Resource):
    @auth_required
    def get(self):

        filters = {
            "genre_id": request.args.get("genre_id"),
            "year": request.args.get("year"),
            "director_id": request.args.get("director_id")
        }

        # Filter out empty values from the dictionary and convert them to integers
        # This ensures that only valid filters will be passed to the database query
        filters = {k: int(v) for k, v in filters.items() if v is not None}

        # If no filters were provided, return all movies
        if not filter:
            all_movies = movie_service.get_all()
            return movies_schema.dump(all_movies), 200

        # Otherwise, apply filters to the query
        movies_by_filter = movie_service.get_all_by_filter(filters)
        return movies_schema.dump(movies_by_filter), 200

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
        movie_service.update_partial(req_json)

        # Return HTTP 204 No Content status
        return "", 204

    @admin_required
    def delete(self, mid: int):
        # Permanently delete the movie from the database
        movie_service.delete(mid)

        # Return HTTP 204 No Content status
        return "", 204