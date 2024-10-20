# basic imports
import asyncio
import logging

# sripts connecting
from manager import *
from message import *

# aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types
from secret import TG_TOKEN

# keyboard buttons
today_b = KeyboardButton(text="Сегодня")
tomorrow_b = KeyboardButton(text="Завтра")
week1_b = KeyboardButton(text="1 Неделя")
week2_b = KeyboardButton(text="2 Неделя")
session_b = KeyboardButton(text="Сессия")

days_btn = ReplyKeyboardMarkup(keyboard=[
    [today_b, week1_b],
    [tomorrow_b, week2_b],
    [session_b]
])


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
    elif text.startswith(SIBSAU_LINK_TEMPLATE):
        try:
            await userCreateUpdate(id, text)
            await bot.send_message(id, LINK_GET, reply_markup=days_btn)
        except:
            await bot.send_message(id, LINK_PROBLEM)


# start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())