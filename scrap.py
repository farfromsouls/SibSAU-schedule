import requests
import re

from message import *
from bs4 import BeautifulSoup

async def scrap(link, day):

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


    # ---------------------------------- #
    #           if no errors:

    # formating text by words (from day=today to the end of 2 weeks)
    text = soup.text.replace('\n', '')
    text = re.sub(r'\s+', ' ', text)
    text = text[text.find("сегодня"):]
    text = re.sub(r"\d\d:\d\d\d\d:\d\d", "", text)

    # list of remaining days
    days = ["Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"]
    days = re.findall("|".join(days), text)

    if day == "today":
        text = text[:text.find(days[0])]
        text = text.replace("сегодняВремяДисциплина ", "")
    elif day == "tomorrow":
        text = text[text.find(days[0]):text.find(days[1])]

    return text


