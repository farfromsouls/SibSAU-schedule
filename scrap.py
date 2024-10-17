import requests
import re

from message import *
from bs4 import BeautifulSoup
from datetime import datetime


def problemCheck(link):
    # getting text and checking basic errors
    try:
        res = requests.get(SIBSAU_LINK_TEMPLATE + link)
        if res.status_code != 200:
            return "сайт упал"
    except:
        return "сайт упал"

    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("title").text

    # check for link errors
    if title == "Internal Server Error":
        return "нет страницы"
    elif title.startswith("404"):
        return "нет страницы"

    return soup


def week_name():

    today = datetime.today()
    first_september = datetime(today.year, 9, 1)
    days_difference = (today - first_september).days

    # если текущая неделя четная, то 2, иначе 1
    w_num = ((days_difference // 7) + 1) % 2
    if w_num == 0:
        return 2
    return 1


def weekday_name(day):
    # находим нужный день недели
    days = ["Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"]

    # возвращает день недели (сегодня/завтра) на русском
    if day == "today":
        return days[datetime.today().weekday()]
    return days[datetime.today().weekday()+1]


def one_day(text, day):
    week = text.split("Понедельник")[week_name()]
    if week.find(weekday_name(day)) == -1:
        return "Это выходной, дружище :)"
    else:
        




def scrap(link, date):

    soup = problemCheck(link)
    if soup in ["сайт упал", "нет страницы"]:
        return soup

    # if no server/link errors:
    # formating text by words
    text = soup.text.replace('\n', '')
    text = re.sub(r'\s+', ' ', text)

    # calling text-functions for task date
    if date in ["today", "tomorrow"]:
        schedule = one_day(text, date)

    elif date in ["week1", "week2"]:
        schedule = 0

    return schedule


# print(scrap("group/13925", "tomorrow"))
print(scrap("group/13925", "today"))
