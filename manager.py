from scrap import scrap
from data import getLink, crt_upd


# main(got link from id) -> userCreateUpdate() -> data/crt_upd(id, link)
async def userCreateUpdate(tg_id, link):
    await crt_upd(tg_id, link)


# main(today/tomorrow button) -> getNow() -> scrap(data/getLink(id), day)
async def getNow(tg_id, date):
    link = await getLink(tg_id)
    schedule = await scrap(link, date)
    return schedule