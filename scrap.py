import requests
import re

from message import *
from bs4 import BeautifulSoup
from datetime import datetime


days = ["Понедельник", "Вторник", "Среда",
    "Четверг", "Пятница", "Суббота", "Воскресенье"]

async def problemCheck(link):
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


async def week_name():

    today = datetime.today()
    first_september = datetime(today.year, 9, 1)
    days_difference = (today - first_september).days

    # если текущая неделя четная, то 2, иначе 1
    w_num = ((days_difference // 7) + 1) % 2
    if w_num == 0:
        return 2
    return 1


async def weekday_name(day):
    w_day_num = datetime.today().weekday()

    # returns needed day and needed day+1 in Russian
    if day == "today":
        return [days[w_day_num], days[w_day_num+1]]
    return [days[w_day_num+1], days[w_day_num+2]]


async def one_day(text, day):

    # get 1 needed week with no losing "Понедельник"
    week = "Понедельник" + text.split("Понедельник")[await week_name()]
    w_day_name = await weekday_name(day)

    # get 1 needed day
    if week.find(w_day_name[0]) == -1:
        return CHILL
    else:
        text = text[text.find(w_day_name[0]):text.find(w_day_name[1])]
        text = text[text.find("ВремяДисциплина ")+16:]

    # timing and lessons lists
    text = re.sub(r" \d\d:\d\d\d\d:\d\d ", "", text)
    time = re.findall(r"\d\d:\d\d-\d\d:\d\d", text)
    lesson = re.split(r"\d\d:\d\d-\d\d:\d\d", text)[1:]
    schedule = ''

    # formatting to "{time}:\n{lesson}\n"
    for i in range(len(time)):
        schedule += f'{time[i]}:\n{lesson[i]}\n\n'

    return schedule


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
        schedule = 0

    return schedule


