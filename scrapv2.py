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
    days_amount = len(tree.xpath(f'//*[@id="week_{w_num}_tab"]/div'))

    # looking for needed day and saving its xpath (if doesn't exist -> weekend return)
    for i_day in range(days_amount):
        day_xpath = f'//*[@id="week_{w_num}_tab"]/div[{i_day+1}]/div[1]/div[1]/div/text()'
        day = tree.xpath(day_xpath)
        day = day[0].replace(" ", "").replace("\n", "")

        if day == weekday:
            day_xpath = f'//*[@id="week_{w_num}_tab"]/div[{i_day+1}]'
            break
        
        if i_day+1 == days_amount:
            return "Это выходной, дружище :)"
        
    answer = ''
    lessons_xpath = f'{day_xpath}/div[2]/div'
    lessons = tree.xpath(lessons_xpath)
    lessons_amount = len(lessons)

    for i_lesson in range(lessons_amount):
        lesson_xpath = f'{lessons_xpath}[{i_lesson+1}]'

        start_time = f'{lesson_xpath}/div[1]/div[2]/text()[1]'
        end_time = f'{lesson_xpath}/div[1]/div[2]/text()[2]'
        name = f'{lesson_xpath}/div[2]/div/div/ul/li[1]/span/text()'
        teacher = f'{lesson_xpath}/div[2]/div/div/ul/li[2]/a/text()'
        room = f'{lesson_xpath}/div[2]/div/div/ul/li[3]/a/text()'
        type = f'{lesson_xpath}/div[2]/div/div/ul/li[1]/text()'

        start_time_text = tree.xpath(start_time)[0]
        end_time_text = tree.xpath(end_time)[0]
        name_text = tree.xpath(name)[0]
        teacher_text = tree.xpath(teacher)[0]
        room_text = tree.xpath(room)[0]
        type_text = tree.xpath(type)[0]
        answer += f'{start_time_text} - {end_time_text}\n{name_text}\n{teacher_text}\n{room_text}\n{type_text}\n\n'

    return answer

async def get_session(page):
    return "Расписание сессии временно недоступно"

async def get_week(page, week):
    return "Расписание на неделю временно недоступно"
