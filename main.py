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


# connecting to "bot"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_MESSAGE, reply_markup="")


# main handler
@dp.message()
async def handler(message: types.Message):

    id = message.from_user.id

    # updeate/create link to the user
    if message.text.startswith(SIBSAU_LINK_TEMPLATE):
        try:
            await userCreateUpdate(id, message.text)
            await bot.send_message(id, LINK_GET)
        except:
            await bot.send_message(id, LINK_PROBLEM)


# start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
