import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from langame_api import get_clubs, get_routes


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "F9 Club Bot успешно запущен!\n\n"
        "Доступные команды:\n"
        "/clubs - список клубов\n"
        "/routes - доступные методы API"
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
