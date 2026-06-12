import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from langame_api import get_clubs, get_routes, get_products
from keyboards.menu import main_menu
from keyboards.pc_menu import pc_menu
from aiogram.types import CallbackQuery

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "👋 Добро пожаловать в F9 Кибер Арена\n\n"
        "Выберите раздел:",
        reply_markup=main_menu()
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


@dp.message(Command("products"))
async def products(message: Message):

    data = get_products()

    await message.answer(
        str(data)[:4000]
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

@dp.callback_query(lambda c: c.data == "pc")
async def open_pc_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        "🖥 Управление компьютерами",
        reply_markup=pc_menu()
    )
