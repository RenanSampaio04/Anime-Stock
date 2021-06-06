from flask import Blueprint, request
from app.models.animes_model import AnimesTable
from psycopg2 import errors
from http import HTTPStatus


bp = Blueprint("bp_animes", __name__)

@bp.route("/animes", methods=["POST", "GET"])
def get_create():
    animes = AnimesTable()
    if request.method == "POST":  
        data = request.get_json()
        try:
            return animes.create_anime(data), 201

        except errors.UniqueViolation as _:
            return {"error": f'Anime \'{data["anime"]}\' already exists'}, 422

        except KeyError as e:
            return e.args[0], 422
    else: 
        return animes.list_anime()

@bp.route("/animes/<int:anime_id>")
def filter(anime_id: int):
    animes = AnimesTable()
    try:
        return animes.filter_anime(anime_id)

    except TypeError as _:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND

        
@bp.route("/animes/<int:anime_id>", methods=["PATCH"])
def update(anime_id: int):
    animes = AnimesTable()
    data = request.get_json()
    try:
        return animes.update_anime(data, anime_id)

    except errors.UniqueViolation as _:
            return {"error": f'Anime \'{data["anime"]}\' already exists'}, 422
    
    except KeyError as e:
            return e.args[0], 422

    except TypeError as _:
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND


@bp.route("/animes/<int:anime_id>", methods=["DELETE"])
def delete(anime_id: int):
    animes = AnimesTable()

    return animes.delete_anime(anime_id)
