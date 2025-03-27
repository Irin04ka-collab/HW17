from app.dao.models.movies import Movie
from app.dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all_by_filter(self, set_of_query):

        # all_movie = self.dao.get_all()
        query = self.dao.get_all()

        if set_of_query.get('genre_id'):
            query = query.filter(Movie.genre_id == set_of_query['genre_id'])
        if set_of_query.get('year'):
            query = query.filter(Movie.year == set_of_query['year'])
        if set_of_query.get('director_id'):
            query = query.filter(Movie.director_id == set_of_query['director_id'])

        movies = query.all()
        # movies_by_filter = [ ]

        # for movie in all_movie:
        #
        #     if filter.get('genre_id'):
        #         if filter['genre_id'] == movie.genre_id:
        #             movies_by_filter.append(movie)
        #
        #     if filter.get('year'):
        #         if filter['year'] == movie.year:
        #             movies_by_filter.append(movie)
        #
        #     if filter.get('director_id'):
        #         if filter['director_id'] == movie.director_id:
        #             movies_by_filter.append(movie)

        return movies


    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        mid = data.get("id")
        movie = self.get_one(mid)

        for key, value in data.items():
            setattr(movie, key, value)

        return self.dao.update(movie)

    def update_partial(self, data):
        mid = data.get("id")
        movie = self.get_one(mid)

        if "title" in data:
            movie.title = data.get("title")
        if "description" in data:
            movie.description = data.get("description")
        if "trailer" in data:
            movie.trailer = data.get("trailer")
        if "year" in data:
            movie.year = data.get("year")
        if "rating" in data:
            movie.rating = data.get("rating")
        if "genre_id" in data:
            movie.genre_id = data.get("genre_id")
        if "director_id" in data:
            movie.director_id = data.get("director_id")

        return self.dao.update(movie)

    def delete(self, mid):
        self.dao.delete(mid)
