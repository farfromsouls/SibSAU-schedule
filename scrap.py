import requests
import re

from message import *
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


days = ["Понедельник", "Вторник", "Среда",
        "Четверг", "Пятница", "Суббота", "Воскресенье"]
problems = ["Сайт упал, либо отсутствует нужная страница",
            "Страницы не существует"]

async def problemCheck(link):
    # getting text and checking basic errors
    try:
        res = requests.get(SIBSAU_LINK_TEMPLATE + link)
        if res.status_code != 200:
            return problems[0]
    except:
        return problems[0]

    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("title").text

    # check for link errors
    if title == "Internal Server Error":
        return problems[1]
    elif title.startswith("404"):
        return problems[1]

    return soup


async def session(text):

    text = text[text.find("Расписание сессии временно"):]
    text = text[:text.find("Сведения об образовательной организации")]
    return text


# for week button
async def week_text_WB(text, date):

    week = "Понедельник" + text.split("Понедельник")[int(date[-1])]
    week = week[:week.find("Расписание сессии временно")]
    week = re.sub(r" \d\d:\d\d\d\d:\d\d ", "", week)

    w_days = re.findall(r'|'.join(days), week)
    w_days_content = re.split(r'|'.join(days), week)[1:]

    schedule = ''

    for w_day in range(len(w_days)):
        time = re.findall(r"\d\d:\d\d-\d\d:\d\d", w_days_content[w_day])
        lesson = re.split(r"\d\d:\d\d-\d\d:\d\d", w_days_content[w_day])[1:]
        schedule += " "*15 + f"{w_days[w_day]}:\n\n"
        
        # formatting to "{time}:\n{lesson}\n"
        for i in range(len(time)):
            schedule += f'{time[i]}:\n{lesson[i]}\n\n'

    return f'\n{schedule}'

# for one day
async def week_text_OD(text, date = None):

    if date == "today":
        day = datetime.today()
    else:
        day = datetime.today() + timedelta(days=1)

    first_september = datetime(day.year, 9, 2)
    days_difference = (day - first_september).days
    
    # если нужная неделя четная, то 2, иначе 1
    w_num = ((days_difference // 7)+1) % 2

    if w_num == 0:
        w_num = 2

    return ("Понедельник" + text.split("Понедельник")[w_num])


async def weekday_name(day):

    w_day_num = datetime.today().weekday()

    # returns needed day and needed day+1 in Russian
    if day == "today":
        return [days[w_day_num], days[(w_day_num+1)%7]]
    return [days[(w_day_num+1)%7], days[(w_day_num+2)%7]]


async def one_day(text, day):
    # get 1 needed week with no losing "Понедельник"
    week = await week_text_OD(text, day)
    w_day_name = await weekday_name(day)

    # if chill:
    if week.find(w_day_name[0]) == -1:
        return f"{w_day_name[0]}:\n\n"+CHILL
    
    # if not chill
    day_t = week[week.find(w_day_name[0]):]
    day_t = day_t[day_t.find("ВремяДисциплина ")+16:]

    if day_t.find(w_day_name[1]) == -1:
        day_t = day_t[:day_t.find("Понедельник")]
        day_t = day_t[:day_t.find("Расписание сессии временно отсутствует")]
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
    if soup in problems:
        return soup

    # if no server/link errors:
    # formating text by words
    text = soup.text.replace('\n', '')
    text = re.sub(r'\s+', ' ', text)

    # calling text-functions for task date
    if date in ["today", "tomorrow"]:
        schedule = await one_day(text, date)

    elif date in ["week1", "week2"]:
        schedule = await week_text_WB(text, date)

    elif date == "session":
        schedule = await session(text)

    return schedule
