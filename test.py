import datetime
def one_day(text, day):
    # unneeded ugly time -> delete it
    text = text[text.find("сегодня"):]
    text = re.sub(r"\d\d:\d\d\d\d:\d\d", "", text)

    # list of remaining days
    days = ["Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота"]
    days = re.findall("|".join(days), text)
    print(days)

    # crop from (task day) to (task day+1)
    if day == "today":
        text = text[:text.find(days[0])]
    elif day == "tomorrow":
        text = text[text.find(days[0]):text.find(days[1])]
    text = text[text.find("ВремяДисциплина ")+16:]

    # timing and lessons lists
    time = re.findall(r"\d\d:\d\d-\d\d:\d\d", text)
    lesson = re.split(r"\d\d:\d\d-\d\d:\d\d", text)[1:]
    schedule = ''

    # formatting to "{time}:\n{lesson}\n"
    for i in range(len(time)):
        schedule += f'{time[i]}:\n{lesson[i]}\n\n'

    return schedule



