import datetime

from app.config import Config
from run import create_app, configure_app
from app.setup_db import db
from app.dao.models.movies import Movie


app_config = Config()
app = create_app(app_config)
configure_app(app)

with app.app_context():

    movies = db.session.query(Movie).filter(Movie.data_added.is_(None)).all()

    for movie in movies:
        movie.data_added = datetime.date.today()

    db.session.commit()

    print("✅ Database seeded!")

