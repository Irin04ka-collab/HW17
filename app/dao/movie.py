from app.dao.models.directors import Director
from app.dao.models.genres import Genre
from app.dao.models.movies import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self):
        return self.session.query(Movie)


    def create(self, data):
        genre_id = data.pop('genre_id')
        genre = self.session.query(Genre).get(genre_id)

        director_id = data.pop('director_id')
        director = self.session.query(Director).get(director_id)

        movie = Movie(**data)
        movie.genre = genre
        movie.director = director

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):

        self.session.add(movie)
        self.session.commit()

        return movie


    def delete(self, mid):
        movie = self.get_one(mid)
        self.session.delete(movie)
        self.session.commit()