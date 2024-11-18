from scrap import *
from data import *
from bs4 import BeautifulSoup
from message import SIBSAU_LINK_TEMPLATE
import requests

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
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find("title").text
    # check for link errors
    if title == "Internal Server Error":
        return problems[1]
    elif title.startswith("404"):
        return problems[1]
    return res.text

# main -> getNow() -> scrap(data/getLink(id), date)
async def schedule(date, tg_id, link=None):

    timer = await getLastTime(tg_id=tg_id, date_time=datetime.datetime.utcnow() 
                                         + timedelta(hours=7))
    if timer == False:
        return "Подождите несколько секунд"

    if tg_id != None:
        link = await getLink(tg_id)

    page = await problemCheck(link)
    if page in problems:
        return page

    # if no server/link errors:
    # calling functions for task date
    if date in ["today", "tomorrow"]:
        schedule = await get_day(page, date)
        return schedule
    elif date in ["week1", "week2"]:
        schedule = await get_week(page, date)
        return schedule
    elif date == "session":
        return "Расписание сессии временно недоступно"

# DB connections 
async def userGetMailing(id):
    mailing = await getMailingStatus(id)
    return mailing

async def userUpdateMailing(id, mailing):
    return await updateMailingStatus(id, mailing)

async def mailingUsers():
    return await getMailingUsers()

# main(got link from id) -> userCreateUpdate() -> data/crt_upd(id, link)
async def userCreateUpdate(tg_id, link):
    await crt_upd(tg_id, link)