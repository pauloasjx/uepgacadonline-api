import requests

import endpoints
from parsers import acadonline_parser


def authenticate(data):
    user = {
        'j_username': data['login'],
        'j_password': data['password']
    }

    session = requests.Session()
    session.post(
        endpoints.acadonline.auth,
        user,
    )

    token = session.cookies.get_dict()['JSESSIONID']

    return token


def get_perfil(token):
    grade_page = requests.get(
        endpoints.acadonline.grades,
        headers=_get_headers(token)
    )

    perfil_page = requests.get(
        endpoints.acadonline.perfil_get,
        headers=_get_headers(token)
    )

    perfil = acadonline_parser.parse_perfil(perfil_page)

    return perfil


def set_perfil(token, data):
    fields = [
        "bairro",
        "cep",
        "cidade",
        "complemento",
        "ddd",
        "email",
        "id",
        "logradouro",
        "numeroTelefone",
        "numero_residencia",
        "uf",
        "url_lattes",
    ]

    perfil = {field: data[field] for field in fields}
    perfil["id"] = "72403"
    perfil["_action_update"] = "Alterar"

    update_perfil = requests.post(
        endpoints.acadonline.perfil_set,
        perfil,
        headers=_get_headers(token)
    )

    return update_perfil


def set_password(token, data):
    fields = [
        "senha1",
        "senha2"
    ]

    password = {field: data[field] for field in fields}
    password["id"] = "72403"
    password["_action_update"] = "Alterar"
    password["_method"] = "PUT"

    update_password = requests.post(
        endpoints.acadonline.password,
        password,
        headers=_get_headers(token)
    )

    return update_password


def remember_password(token):
    params = {"_action_passo2": "OK", "registroAcademico": "14147326"}

    request_remember_page = requests.post(
        endpoints.acadonline.remember_password,
        params,
        headers=_get_headers(token)
    )

    return request_remember_page


def get_grade(token):
    grade_page = requests.get(
        endpoints.acadonline.grades,
        headers=_get_headers(token)
    )

    grades = acadonline_parser.parse_grade(grade_page)["disciplines"]

    return grades


def get_extract(token):
    extract_file = requests.get(
        endpoints.acadonline.extract,
        headers=_get_headers(token)
    )

    print(extract_file.content)

    return None


def get_disciplines(token):
    disciplines_page = requests.get(
        endpoints.acadonline.grades,
        headers=_get_headers(token)
    )

    disciplines = acadonline_parser.parse_disciplines(disciplines_page)

    return disciplines


def get_additional_activities(token):
    activities_page = requests.get(
        endpoints.acadonline.activities,
        headers=_get_headers(token)
    )

    activities = acadonline_parser.parse_additional_activities(activities_page)

    return activities


def _get_cookies(response):
    headers_raw = dict((key, value) for key, value in response.cookies.items())
    headers = {"cookie": f'JSESSIONID={headers_raw["JSESSIONID"]};'}
    return headers, headers_raw["JSESSIONID"]


def _get_headers(jsession):
    return {"cookie": f"JSESSIONID={jsession};"}
