from flask import Blueprint, request

from cache import cache
from repositories import ru_repository
from samples import ru_sample

from utils.response import success

ru_blueprint = Blueprint("ru", __name__, url_prefix="/ru")


@ru_blueprint.route("/menu", methods=["GET"])
@cache.cached(timeout=600, query_string=True)
def menu():
    campus = request.args.get("campus")
    shift = request.args.get("shift")
    next = request.args.get("next")
    sample = request.args.get("sample")

    weekly_menu = ru_repository.weekly_menu(campus, shift, next, sample)

    return success(message="Cardápio retornado com sucesso", weekly_menu=weekly_menu)
