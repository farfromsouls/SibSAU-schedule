# basic imports
import asyncio
import logging

# sripts connecting
from manager import *
from message import *

# aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types
from cfg.secret import TG_TOKEN

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# keyboard buttons
days_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сегодня", callback_data="today")],
        [KeyboardButton(text="Завтра", callback_data="next")]
    ]
)

# connecting to "bot"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE, reply_markup=days_btn)


# main handler
@dp.message()
async def handler(message: types.Message):

    id = message.from_user.id
    text = message.text

    # updeate/create link to the user
    if text.startswith(SIBSAU_LINK_TEMPLATE):
        try:
            await userCreateUpdate(id, text)
            await bot.send_message(id, LINK_GET)
        except:
            await bot.send_message(id, LINK_PROBLEM)

    # send schedule for today/tomorrow
    elif text in ["Сегодня", "Завтра"]:
        if text == "Сегодня":
            await bot.send_message(id, await getNow(id, "today"))
        if text == "Завтра":
            await bot.send_message(id, await getNow(id, "tomorrow"))

# start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
