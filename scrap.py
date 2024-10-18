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


async def week_text(text, date = None):

    if date == "week1":
        return "Понедельник" + text.split("Понедельник")[1]
    elif date == "week2":
        x = "Понедельник" + text.split("Понедельник")[2]
        x = x[:x.find("Расписание сессии временно отсутствует")]
        return x

    today = datetime.today()
    first_september = datetime(today.year, 9, 1)
    days_difference = (today - first_september).days
    
    # если текущая неделя четная, то 2, иначе 1
    w_num = ((days_difference // 7) + 1) % 2
    if w_num == 0:
        w_num = 2
    w_num = 1

    return "Понедельник" + text.split("Понедельник")[w_num]



async def weekday_name(day):
    w_day_num = datetime.today().weekday()

    # returns needed day and needed day+1 in Russian
    if day == "today":
        return [days[w_day_num], days[w_day_num+1]]
    return [days[w_day_num+1], days[w_day_num+2]]


async def one_day(text, day):

    # get 1 needed week with no losing "Понедельник"
    week = await week_text(text)
    w_day_name = await weekday_name(day)

    # get 1 needed day
    if week.find(w_day_name[0]) == -1:
        return CHILL
    else:
        text = text[text.find(w_day_name[0]):]
        text = text[text.find("ВремяДисциплина ")+16:]

        if text.find(w_day_name[1]) == -1:
            text = text[:text.find("Понедельник")]
        else:
            text = text[:text.find(w_day_name[1])]


    # timing and lessons lists
    text = re.sub(r" \d\d:\d\d\d\d:\d\d ", "", text)
    time = re.findall(r"\d\d:\d\d-\d\d:\d\d", text)
    lesson = re.split(r"\d\d:\d\d-\d\d:\d\d", text)[1:]
    schedule = ''

    # formatting to "{time}:\n{lesson}\n"
    for i in range(len(time)):
        schedule += f'{time[i]}:\n{lesson[i]}\n\n'

    return schedule


async def week(text, date):
    return await week_text(text, date)


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