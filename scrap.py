from lxml import etree
from datetime import datetime, timedelta

days = ["Понедельник", "Вторник", "Среда",
        "Четверг", "Пятница", "Суббота", "Воскресенье"]

async def weekday_name(date): # for "today" or "tomorrow"
    utc_now = datetime.utcnow() + timedelta(hours=7)
    w_day = utc_now.weekday()
    if date == "today":
        return days[w_day]
    return days[(w_day+1)%7]

async def week_num(date): # week number from 2 september
    
    if date == "today":
        day = datetime.utcnow() + timedelta(hours=7)
    elif date == "tomorrow":
        day = datetime.utcnow() + timedelta(days=1, hours=7)

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

    return await parse(day, weekday)

async def get_week(page, week):
    w_num = week[-1]
    
    tree = etree.HTML(page)
    days_xpath = etree.XPath(f'//*[@id="week_{w_num}_tab"]/div')
    days_elements = days_xpath(tree)
    answer = ""

    for day_elem in days_elements:

        day_name = day_elem.xpath('./div[1]/div[1]/div/text()')
        day_name = day_name[0].replace(" ", "").replace("\n", "")

        answer += await parse(day_elem, day_name)
                
    return answer

async def get_session():
    return "Расписание сессии временно недоступно"

async def parse(day, day_name):

    lessons = day.xpath('./div[2]/div')
    answer = f"——————— {day_name} ———————\n\n"
    
    for lesson in lessons:
        start = lesson.xpath('./div[1]/div[2]/text()[1]')[0].replace(" ", "").replace("\n", "")
        end = lesson.xpath('./div[1]/div[2]/text()[2]')[0].replace(" ", "").replace("\n", "")

        if len(lesson.xpath('./div[2]/div/div')) == 1:  # if 1 group
            name = lesson.xpath('./div[2]/div/div/ul/li[1]/span/text()')[0]
            type = lesson.xpath('./div[2]/div/div/ul/li[1]/text()')[0]
            professor = lesson.xpath('./div[2]/div/div/ul/li[2]/a/text()')[0]
            room = lesson.xpath('./div[2]/div/div/ul/li[3]/a/text()')[0]
            group = ""

            # if lesson only for 1 subgroup
            if len(lesson.xpath('./div[2]/div/div/ul/li')) == 4:
                group = f"{lesson.xpath('./div[2]/div/div/ul/li[4]/text()')[0]}\n"
            answer += " "*10 + f"{start}-{end}\n{name}{type}\n{professor}\n{room}\n{group}\n"

        else:  # if 2 subgroups in 1 lesson

            answer += " "*10 + f"{start}-{end}\n"

            for i in [1, 2]:
                name = lesson.xpath(f'./div[2]/div/div[{i}]/ul/li[2]/span/text()')[0]
                type = lesson.xpath(f'./div[2]/div/div[{i}]/ul/li[2]/text()')[0]
                professor = lesson.xpath(f'./div[2]/div/div[{i}]/ul/li[3]/a/text()')[0]
                room = lesson.xpath(f'./div[2]/div/div[{i}]/ul/li[4]/a/text()')[0]
                group = lesson.xpath(f'./div[2]/div/div[{i}]/ul/li[1]/text()')[0]

                answer += f"{name}{type}\n{professor}\n{room}\n{group}\n\n"
    
    return answer