import asyncio
import logging
import sqlite3

from data import *
from cfg.secret import *
from message import *

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


# Bot 
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

# DB
db_path = 'cfg/data.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE)


@dp.message()
async def handler(message: types.Message):

    if message.text.startswith(SIBSAU_LINK_TEMPLATE):
        await bot.send_message(message.from_user.id, LINK_GET)
        await create(conn, cursor, message.from_user.id, message.text)
    else:
        await bot.send_message(message.from_user.id, LINK_PROBLEM)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
