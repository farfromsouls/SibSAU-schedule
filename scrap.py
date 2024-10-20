import requests
import re

from message import *
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


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


async def session(text):

    text = text[text.find("Расписание сессии временно"):]
    text = text[:text.find("Сведения об образовательной организации")]
    return text


async def week_text(text, date = None):
    # if week button
    if date in ["week1", "week2"]:
        week = "Понедельник" + text.split("Понедельник")[int(date[-1])]
        week = week[:week.find("Расписание сессии временно отсутствует")]
        week = re.sub(r" \d\d:\d\d\d\d:\d\d ", "", week)
        time = re.findall(r"\d\d:\d\d-\d\d:\d\d", week)
        lesson = re.split(r"\d\d:\d\d-\d\d:\d\d", week)[1:]
        schedule = ''

        # formatting to "{time}:\n{lesson}\n"
        for i in range(len(time)):
            schedule += f'{time[i]}:\n{lesson[i]}\n\n'

        return f'\n{schedule}'

    # for "one_day" func if not week button
    if date == "today":
        day = datetime.today()
    else:
        day = datetime.today() + timedelta(days=1)

    first_september = datetime(day.year, 9, 2)
    days_difference = (day - first_september).days
    
    # если текущая неделя четная, то 2, иначе 1
    w_num = ((days_difference // 7)+1) % 2

    if w_num == 0:
        w_num = 2

    print(w_num)

    return ("Понедельник" + text.split("Понедельник")[w_num])


async def weekday_name(day):
    w_day_num = datetime.today().weekday()

    # returns needed day and needed day+1 in Russian
    if day == "today":
        return [days[w_day_num], days[(w_day_num+1)%7]]
    return [days[(w_day_num+1)%7], days[(w_day_num+2)%7]]


async def one_day(text, day):
    # get 1 needed week with no losing "Понедельник"
    week = await week_text(text, day)
    w_day_name = await weekday_name(day)

    # if chill:
    if week.find(w_day_name[0]) == -1:
        return f"{w_day_name[0]}:\n\n"+CHILL
    
    # if not chill
    day_t = week[week.find(w_day_name[0]):]
    day_t = day_t[day_t.find("ВремяДисциплина ")+16:]

    if day_t.find(w_day_name[1]) == -1:
        day_t = day_t[:day_t.find("Понедельник")]
    else:
        day_t = day_t[:day_t.find(w_day_name[1])]

    # timing and lessons lists
    day_t = re.sub(r" \d\d:\d\d\d\d:\d\d ", "", day_t)
    time = re.findall(r"\d\d:\d\d-\d\d:\d\d", day_t)
    lesson = re.split(r"\d\d:\d\d-\d\d:\d\d", day_t)[1:]
    schedule = ''

    # formatting to "{time}:\n{lesson}\n"
    for i in range(len(time)):
        schedule += f'{time[i]}:\n{lesson[i]}\n\n'

    return f'{w_day_name[0]}:\n\n{schedule}'


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
        schedule = await week_text(text, date)

    elif date == "session":
        schedule = await session(text)

    return schedule