import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import Command
from langame_api import get_clubs

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\n\nF9 Club Bot успешно запущен!"
    )
    
@dp.message(Command("clubs"))
async def clubs(message: Message):

    data = get_clubs()

    await message.answer(
        str(data)
    )
    
@dp.message(Command("routes"))
async def routes(message: Message):

    data = get_routes()

    await message.answer(
        str(data)
    )

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
