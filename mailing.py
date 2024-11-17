from data import getAllMailingGroups
from manager import schedule

async def mailingData():

    mailingGroups = set([group[0] for group in await getAllMailingGroups()])
    mailingGroups = list(mailingGroups)
    groupSchedules = {}

    for group in mailingGroups:
        groupSchedules[group] = await schedule(link=group, date="tomorrow", tg_id=None)

    return groupSchedules