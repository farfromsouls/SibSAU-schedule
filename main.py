# basic imports
import asyncio
import logging
import re

# sripts connecting
from manager import *
from message import *

# aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from secret import TG_TOKEN

# keyboard buttons #1
today_b = KeyboardButton(text="Сегодня")
tomorrow_b = KeyboardButton(text="Завтра")
week1_b = KeyboardButton(text="1 Неделя")
week2_b = KeyboardButton(text="2 Неделя")
session_b = KeyboardButton(text="Сессия")
mailing_b = KeyboardButton(text="Рассылка")

main_btn = ReplyKeyboardMarkup(keyboard=[
    [today_b, week1_b],
    [tomorrow_b, week2_b],
    [session_b, mailing_b]
])

# keyboard buttons #2
mailing_off = KeyboardButton(text="Отключить")
mailing_on = KeyboardButton(text="Включить")
mailing_cancel = KeyboardButton(text="Отмена")


# connecting to "bot"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE)


# main handler
@dp.message()
async def handler(message: types.Message):

    id = message.from_user.id
    text = message.text

    try:
        is_sibsau_link = text.startswith(SIBSAU_LINK_TEMPLATE)
    except:
        is_sibsau_link = False
        await bot.send_message(id, "Некорректный запрос")

    # today/tomorrow/week1/week2/session tasks
    if text == "Сегодня":
        await bot.send_message(id, await getNow(id, "today"))
    elif text == "Завтра":
        await bot.send_message(id, await getNow(id, "tomorrow"))
    elif text == "1 Неделя":
        await bot.send_message(id, await getNow(id, "week1"))
    elif text == "2 Неделя":
        await bot.send_message(id, await getNow(id, "week2"))
    elif text == "Сессия":
        await bot.send_message(id, await getNow(id, "session"))

    # updeate/create link to the user
    elif is_sibsau_link:
        try:
            await userCreateUpdate(id, text)
            await bot.send_message(id, LINK_GET, reply_markup=main_btn)
        except:
            await bot.send_message(id, LINK_PROBLEM)


    # asking turn off/on mailing
    elif text == "Рассылка":

        mailing = await userGetMailing(id)

        if mailing == 0:
            mailing_btn = ReplyKeyboardMarkup(keyboard=[
                [mailing_cancel, mailing_on]
            ])
            mailing_text = "включить"

        elif mailing == 1:
            mailing_btn = ReplyKeyboardMarkup(keyboard=[
                [mailing_cancel, mailing_off]
            ])
            mailing_text = "отключить"

        await bot.send_message(id, f"Хотите {mailing_text} ежедневную рассылку?", 
                                reply_markup=mailing_btn)
    
    # turn off/on mailing
    elif text in ["Отключить", "Включить", "Отмена"]:

        if text == "Отключить":
            mailing = 0
            ans = await userUpdateMailing(id, mailing)

        elif text == "Включить":
            mailing = 1
            ans = await userUpdateMailing(id, mailing)

        elif text == "Отмена":
            ans = 'Возврат в меню'

        await bot.send_message(id, ans, reply_markup=main_btn)

async def mailing():
    mailing_ids = await mailingUsers()
    for id in mailing_ids:
        await bot.send_message(id[0], await getNow(id[0], "tomorrow"))

# start polling
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(mailing, "cron", hour="21", minute="00")
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())