# basic imports
import asyncio
import logging
import sqlite3

# sripts connecting
from data import *
from cfg.secret import *
from message import *
from scrap import *

# aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


# connecting to "bot"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

# connecting to DB
db_path = 'cfg/data.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
sql = [cursor, conn]


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE)

# main handler
@dp.message()
async def handler(message: types.Message):

    # updeate/create link to the user
    if message.text.startswith(SIBSAU_LINK_TEMPLATE):
        await bot.send_message(message.from_user.id, LINK_GET)
        await crt_upd(sql, message.from_user.id, message.text)
    else:
        await bot.send_message(message.from_user.id, LINK_PROBLEM)

    if message.text == "":
        pass


async def mailing():
    pass


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
