from flask import Blueprint, request, make_response

from cache import cache
from database import db
from models.user import User
from repositories import portal_repository, acadonline_repository

from utils.response import success, error, conditional_response

from datetime import datetime

acadonline_blueprint = Blueprint("acadonline", __name__, url_prefix="/acadonline")


@acadonline_blueprint.route("/login", methods=["POST"])
def authenticate():
    login = request.form.get('login')
    password = request.form.get('password')

    token = acadonline_repository.authenticate(login, password)

    perfil = acadonline_repository.get_perfil(token)

    user = User.query.filter_by(academic_register=login).first()

    name = " ".join(
        [
            perfil['complete_name'].split()[0],
            perfil['complete_name'].split()[-1]
        ]
    ) if len(perfil['complete_name'].split()) > 2 else perfil['complete_name']

    if user is None:
        user = User(
            token=token,
            name=name,
            academic_register=perfil['academic_register']
        )

        db.session.add(user)
    else:
        user.token = token

    db.session.commit()

    response = make_response(success(message="Login realizado com sucesso", perfil=perfil, token=token))
    response.headers["x-api-token"] = token

    return conditional_response(perfil, response, error(message="Usuário inválido"))


@acadonline_blueprint.route("/home", methods=["GET"])
@cache.cached(timeout=120, query_string=True)
def home():
    date = request.args.get("date")

    if date is None:
        date = datetime.strptime(datetime.today().strftime('%d/%m/%Y'), '%d/%m/%Y')
    else:
        date = datetime.strptime(date, '%d/%m/%Y')

    _featured = portal_repository.featured()
    _news = portal_repository.news_item(date)

    return success(message="Destaques retornados com sucesso", featured=_featured, daily_news=_news)


@acadonline_blueprint.route("/perfil", methods=["GET"])
def get_perfil():
    token = request.headers.get("x-api-token")

    perfil = acadonline_repository.get_perfil(token)

    return conditional_response(
        perfil,
        success(
            message="Perfil capturado com sucesso!",
            perfil=perfil,
            token=token
        ),
        error(
            message="Perfil inválido"
        )
    )


@acadonline_blueprint.route("/perfil", methods=["POST"])
def set_perfil():
    data = request.get_json()
    token = request.headers.get("x-api-token")

    acadonline_repository.set_perfil(token, data)

    return success(message="Perfil atualizado com sucesso", token=token)


@acadonline_blueprint.route("/password", methods=["POST"])
def set_password():
    data = request.get_json()
    token = request.headers.get("x-api-token")

    acadonline_repository.set_password(token, data)

    return success(message="Perfil atualizado com sucesso", token=token)


@acadonline_blueprint.route("/rememberpassword", methods=["POST"])
def remember_password():
    token = request.headers.get("x-api-token")

    acadonline_repository.remember_password(token)

    return error(message="Serviço ainda não finalizado")


@acadonline_blueprint.route("/documents", methods=["GET"])
def get_documents():
    pass


@acadonline_blueprint.route("/grade", methods=["GET"])
def get_grade():
    token = request.headers.get("x-api-token")
    extra = request.args.get("extra")
    sample = bool(request.args.get("sample"))

    disciplines = acadonline_repository.get_grade_with_info(token) \
        if extra else acadonline_repository.get_grade(token, sample)

    condition = len(disciplines) > 0

    return conditional_response(
        condition,
        success(
            message="Notas capturadas com sucesso!",
            token=token,
            disciplines=disciplines
        ),
        error(
            message="Erro ao capturar notas"
        )
    )


@acadonline_blueprint.route("/disciplines", methods=["GET"])
def get_disciplines():
    token = request.headers.get("x-api-token")

    disciplines = acadonline_repository.get_disciplines(token)

    condition = len(disciplines) > 0

    return conditional_response(
        condition,
        success(
            message="Disciplinas returnadas com sucesso!",
            token=token,
            disciplines=disciplines
        ),
        error(
            message="Erro ao retornar disciplinas"
        )
    )


@acadonline_blueprint.route('/schedule', methods=["GET"])
def get_schedule():
    token = request.headers.get("x-api-token")

    acadonline_repository.get_class_schedule(token)

    return success(
        message="Horário retornado com sucesso!",
        token=token
    )


@acadonline_blueprint.route("/activities", methods=["GET"])
def get_additional_activities():
    token = request.headers.get("x-api-token")

    activities = acadonline_repository.get_additional_activities(token)

    return success(
        message="Atividades capturadas com sucesso!",
        token=token,
        activities=activities,
    )
