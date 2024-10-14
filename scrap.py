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
    text = soup.text.replace('\n', '')
    text = re.sub(r'\s+', ' ', text)
    text = text[text.index("сегодня"):]

    # list of remaining days
    days = ["Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"]
    days = re.findall("|".join(days), text)
    
    if task == "today":
        text = text[:text.index(days[0])]    
    elif task == "tomorrow":
        text = text[text.index(days[0]):text.index(days[1])]

    return text


print(scrap('group/13925', 'tomorrow'))
