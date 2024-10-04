def scrap(link):
    from bs4 import BeautifulSoup
    import requests
    import re

    page = requests.get(
        'https://timetable.pallada.sibsau.ru/timetable/group/13925')
    soup = BeautifulSoup(page.text, "html.parser")
    x = soup.findall('div', class_="body")
    print(x)

scrap(1)
