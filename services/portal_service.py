import requests

import endpoints
from headers import headers

from parsers.portal_parser import parse_news, parse_featured, \
    parse_daily_news_items, parse_weekly_news_items, parse_news_items


def featured():
    featured_page = requests.get(endpoints.portal.featured, headers=headers)
    _featured = parse_featured(featured_page)

    return _featured


def daily_news_item(date):
    params = {"ano": date.year, "mes": date.month}

    news_page = requests.post(endpoints.portal.news_item, params, headers=headers)
    _daily_news_item = parse_daily_news_items(news_page, date)

    return _daily_news_item


def weekly_news_items(date):
    params = {"ano": date.year, "mes": date.month}

    news_weekly_page = requests.post(endpoints.portal.news_item, params, headers=headers)
    _weekly_news_items = parse_weekly_news_items(news_weekly_page, date)

    return _weekly_news_items


def news_items(initial_date, final_date):
    initial_params = {"ano": initial_date.year, "mes": initial_date.month}
    final_params = {"ano": final_date.year, "mes": final_date.month}

    initial_news_items_page = requests.post(endpoints.portal.news_item, initial_params, headers=headers)
    final_news_items_page = requests.post(endpoints.portal.news_item, final_params, headers=headers)

    _news_items = parse_news_items(final_news_items_page, final_date, initial_news_items_page, initial_date)

    return _news_items


def news(cod):
    params = {"id": cod}

    news_page = requests.get(endpoints.portal.news, params, headers=headers)
    news_ = parse_news(news_page)

    return news_
