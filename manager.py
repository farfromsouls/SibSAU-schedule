from scrap import *
from data import *


# main(got link from id) -> userCreateUpdate() -> data/crt_upd(id, link)
async def userCreateUpdate(tg_id, link):
    await crt_upd(tg_id, link)


# main(today/tomorrow button) -> getNow() -> scrap(data/getLink(id), day)
async def getNow(tg_id, day):
    link = await getLink(tg_id)
    schedule = await scrap(link, day)
    return schedule