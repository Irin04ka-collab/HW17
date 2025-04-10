from flask import request
from app.dao.models.movies import movies_schema

def paginate_query(movie_query):

    if not request.args.get("page"):
        return movies_schema.dump(movie_query)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated = movie_query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": paginated.page,
        "items": movies_schema.dump(paginated.items)
    }
