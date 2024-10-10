import requests
import re

from message import *
from bs4 import BeautifulSoup

def scrap(link, task):
    
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
    
    # if no errors:
    # formating text by words (from day=today to the end of the week)
    days = ["Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"]
    text = soup.text.replace('\n', '')
    text = re.sub(r'\s+', ' ', text)
    text = text[text.index("сегодня"):]

    if task == "today":
        for day in days:
            try:
                text = text[:text.index(day)]
            except:
                continue

        return text
    
    if task == "tomorrow":
        for day in days:
            try:
                text = 0
            except:
                continue

        return text





print(scrap('group/13925', 'tomorrow'))
