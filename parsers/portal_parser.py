from bs4 import BeautifulSoup

from models.featured import Featured
from models.group_news import GroupNews
from models.item_news import ItemNews
from models.news import News


def parse_featured(featured_page):
    image_prefix = "https://portal.uepg.br/"

    try:
        featured = [
            Featured(
                image_prefix + value.find("a").find("img")['src'],
                value.find("a")['href']
            ).__dict__
            for value in
            BeautifulSoup(featured_page.content, features="lxml").find("ul", {"id": "slider"}).find_all("li")
        ]
    except:
        featured = None

    return featured


def parse_daily_news_items(news_page, date):
    try:
        news = search_news(news_page)
        news = [new for new in news["news"] if new["date"] == date][0]
    except:
        news = None

    return news


def parse_weekly_news_items(news_items_weekly_page, date):
    try:
        news = search_news(news_items_weekly_page)
        news = [new for new in news["news"]]
    except:
        news = None

    return news


def parse_news_items(final_page, final_date, initial_page=None, initial_date=None):
    try:
        final_news = search_news(final_page)
        news = [new for new in final_news["news"] if final_date >= new["date"] > initial_date]

        if initial_page is not None and initial_date is not None:
            initial_news = search_news(initial_page)

            initial_news = [new for new in initial_news["news"] if final_date >= new["date"] > initial_date]

            news = news + initial_news
    except:
        news = []

    return news

def search_news(news_page):
    return GroupNews([
        [
            value.find("div", "data").text,
            [
                ItemNews(
                    p.find("a")['href'],
                    p.find("span", "hora").text,
                    p.find("a").text
                ).__dict__ for p in value.find_all("p")
            ]
        ]
        for value in
        BeautifulSoup(news_page.content, features="lxml").find_all("div", {"class": "chamada"})[1:]
    ]).__dict__


def search_content(s):
    begin = s.find('<p align="justify"></p>')
    end = s.find('\n</div\r\n<p>&nbsp;</p>')

    return s[begin:end - 6]


def parse_news(news_page):
    # try:
    news_raw = BeautifulSoup(news_page.content, features="lxml").find("div", "noticia")

    print(news_raw.find_all("em"))

    state = len(news_raw.find_all("em"))

    if state == 1:
        news = News(
            news_raw.find("h1", "noticia").text,
            news_raw.find("h2").text if news_raw.find("h2") else "",
            news_raw.find("em").text[4:],
            search_content(str(news_raw)),
            news_raw.find("strong").text,
        ).__dict__
    else:
        news = News(
            news_raw.find("h1", "noticia").text,
            news_raw.find("h2").text if news_raw.find("h2") else "",
            news_raw.find_all("em")[1].text[4:],
            search_content(str(news_raw)),
            news_raw.find("strong").text,
            news_raw.find("em").text[14:]
        ).__dict__
    # except:
    #     news = None

    return news
