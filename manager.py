from scrap import scrap
from data import *


# main(got link from id) -> userCreateUpdate() -> data/crt_upd(id, link)
async def userCreateUpdate(tg_id, link):
    await crt_upd(tg_id, link)

# main(today/tomorrow button) -> getNow() -> scrap(data/getLink(id), day)
async def getNow(tg_id, date):
    link = await getLink(tg_id)
    schedule = await scrap(link, date)
    return schedule

async def userGetMailing(id):
    mailing = await getMailingStatus(id)
    return mailing

async def userUpdateMailing(id, mailing):
    return await updateMailingStatus(id, mailing)

async def mailingUsers():
    return await getMailingUsers()