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
from .venv.secret import TG_TOKEN

# keyboard buttons
days_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сегодня")],
        [KeyboardButton(text="Завтра")],
        [KeyboardButton(text="1 Неделя (в разработке)")],
        [KeyboardButton(text="2 Неделя (в разработке)")]
    ]
)

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

    # updeate/create link to the user
    if text.startswith(SIBSAU_LINK_TEMPLATE):
        try:
            await userCreateUpdate(id, text)
            await bot.send_message(id, LINK_GET, reply_markup=days_btn)
        except:
            await bot.send_message(id, LINK_PROBLEM)

    # send schedule for today/tomorrow/1week/2week
    elif text in ["Сегодня", "Завтра", "1 Неделя (в разработке)", "2 Неделя (в разработке)"]:
        if text == "Сегодня":
            await bot.send_message(id, await getNow(id, "today"))
        if text == "Завтра":
            await bot.send_message(id, await getNow(id, "tomorrow"))
        if text == "1 Неделя (в разработке)":
            await bot.send_message(id, await getNow(id, "week1"))
        if text == "2 Неделя (в разработке)":
            await bot.send_message(id, await getNow(id, "week2"))

# start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
