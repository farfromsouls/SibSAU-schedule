from lxml import etree
from datetime import datetime, timedelta

days = ["Понедельник", "Вторник", "Среда",
        "Четверг", "Пятница", "Суббота", "Воскресенье"]

async def weekday_name(date): # for "today" or "tomorrow"
    w_day = datetime.today().weekday()
    if date == "today":
        return days[w_day]
    return days[(w_day+1)%7]

async def week_num(date): # week number from 2 september
    
    if date == "today":
        day = datetime.today()
    elif date == "tomorrow":
        day = datetime.today() + timedelta(days=1)

    first_september = datetime(day.year, 9, 2)
    days_difference = (day - first_september).days
    
    # если нужная неделя четная, то 2, иначе 1
    w_num = ((days_difference // 7) + 1) % 2
    if w_num == 0:
        w_num = 2
    return w_num

async def get_day(page, date):

    weekday = await weekday_name(date)
    w_num = await week_num(date)

    tree = etree.HTML(page)
    days_xpath = etree.XPath(f'//*[@id="week_{w_num}_tab"]/div')
    days_elements = days_xpath(tree)
    day = None

    for day_elem in days_elements:
        day_name = day_elem.xpath('./div[1]/div[1]/div/text()')
        day_name = day_name[0].replace(" ", "").replace("\n", "")

        if day_name == weekday:
            day = day_elem
            break

    if day == None:
        return "Это выходной :)"

    lessons = day.xpath('./div[2]/div')
    answer = ""

    for lesson in lessons:
        start = lesson.xpath('./div[1]/div[2]/text()[1]')[0].replace(" ", "").replace("\n", "")
        end = lesson.xpath('./div[1]/div[2]/text()[2]')[0].replace(" ", "").replace("\n", "")
        name = lesson.xpath('./div[2]/div/div/ul/li[1]/span/text()')[0]
        type = lesson.xpath('./div[2]/div/div/ul/li[1]/text()')[0]
        professor = lesson.xpath('./div[2]/div/div/ul/li[2]/a/text()')[0]
        room = lesson.xpath('./div[2]/div/div/ul/li[3]/a/text()')[0]

        answer += " "*10 + f"{start}-{end}\n{name} {type}\n{professor}\n{room}\n\n"

    return answer

async def get_session(page):
    return "Расписание сессии временно недоступно"

async def get_week(page, week):
    return "Расписание на неделю временно недоступно"
