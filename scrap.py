import requests
import lxml
import re
from message import *


from bs4 import BeautifulSoup

def scrap(link):
    res = requests.get(SIBSAU_LINK_TEMPLATE + link)
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.find("title").text

    if title == "Internal Server Error":
        pass
    elif title.startswith("404"):
        pass
    else:
        days = ["Понедельник", "Вторник", "Среда",
                "Четверг", "Пятница", "Суббота"]

        text = soup.text.replace('\n', '')
        text = re.sub(r'\s+', ' ', text)
        text = text[text.index("сегодня"):]

        for i in days:
            try:
                text = text[:text.index(i)]
            except:
                continue

        return text
