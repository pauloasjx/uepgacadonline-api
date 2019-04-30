from bs4 import BeautifulSoup

from app.models.activity import Activity
from app.models.grade import Grade
from app.models.perfil import Perfil

from collections import ChainMap


def parse_additional_activities(activities_page):
    try:
        activities_raw = [
            [cell.text for cell in row("td")]
            for row in BeautifulSoup(activities_page.content, features="lxml")("tr", "even")
        ]
        activities = [
            Activity(*[field for field in activity_raw]).__dict__
            for activity_raw in activities_raw
        ]
    except:
        activities = None

    return activities


def parse_grade(grades_page):
    try:
        disciplines_raw = [
                              [cell.text for cell in row("td")]
                              for row in BeautifulSoup(grades_page.content, features="lxml")("tr")
                          ][1:]
        disciplines = Grade(disciplines_raw).__dict__
    except:
        disciplines = None

    return disciplines


def parse_disciplines(disciplines_page):
    try:
        disciplines_raw = [
                              [cell.text for cell in row("td")]
                              for row in BeautifulSoup(disciplines_page.content, features="lxml")("tr")
                          ][1:]

        disciplines = [
            {"{cod}-{year}".format(cod=row[0], year=row[3]): row[1]}
            for row in disciplines_raw
        ]

        #disciplines = dict(ChainMap(*disciplines))

    except:
        disciplines = None

    return disciplines


def parse_perfil(perfil_page):
    try:
        perfil_raw = [
            value.find("td", "value")
                .text.replace("\r", "")
                .replace("\n", "")
                .replace("\t", "")
                .replace("/\s\s+/", "")
                .strip()
            for value in BeautifulSoup(perfil_page.content, features="lxml")("tr", "prop")
        ]

        perfil = Perfil(*[field for field in perfil_raw]).__dict__
    except:
        perfil = None

    return perfil
