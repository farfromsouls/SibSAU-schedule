import requests
import re

from message import *
from bs4 import BeautifulSoup


async def problemCheck(link):
    # getting text and checking basic errors
    res = requests.get(SIBSAU_LINK_TEMPLATE + link)
    if res.status_code != 200:
        return "сайт упал"

    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("title").text

    # check for link errors
    if title == "Internal Server Error":
        return "нет страницы"
    elif title.startswith("404"):
        return "нет страницы"

    return soup


async def one_day(text, day):
    # unneeded ugly time -> delete it
    text = text[text.find("сегодня"):]
    text = re.sub(r"\d\d:\d\d\d\d:\d\d", "", text)

    # list of remaining days
    days = ["Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"]
    days = re.findall("|".join(days), text)

    # crop from (task day) to (task day+1)
    if day == "today":
        text = text[:text.find(days[0])]
    elif day == "tomorrow":
        text = text[text.find(days[0]):text.find(days[1])]
    text = text[text.find("ВремяДисциплина ")+16:]

    # timing and lessons lists
    time = re.findall(r"\d\d:\d\d-\d\d:\d\d", text)
    lesson = re.split(r"\d\d:\d\d-\d\d:\d\d", text)[1:]
    schedule = ''

    # formatting to "{time}:\n{lesson}\n"
    for i in range(len(time)):
        schedule += f'{time[i]}:\n{lesson[i]}\n\n'

    return schedule


async def week(text, date):
    return '0'


async def scrap(link, date):

    soup = await problemCheck(link)
    if soup in ["сайт упал", "нет страницы"]:
        return soup

    # if no server/link errors:
    # formating text by words
    text = soup.text.replace('\n', '')
    text = re.sub(r'\s+', ' ', text)

    # calling text-functions for task date
    if date in ["today", "tomorrow"]:
        schedule = await one_day(text, date)

    elif date in ["week1", "week2"]:
        schedule = await week(text, date)

    return schedule
