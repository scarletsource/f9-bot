import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from langame_api import (
    get_clubs,
    get_routes,
    get_products,
    get_pc_list,
    pc_manage
)

from keyboards.menu import main_menu
from keyboards.pc_menu import pc_menu, confirm_restart_menu


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


@dp.callback_query(lambda c: c.data == "pc")
async def open_pc_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        "🖥 Управление компьютерами",
        reply_markup=pc_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "back_main")
async def back_main(callback: CallbackQuery):

    await callback.message.edit_text(
        "👋 Добро пожаловать в F9 Кибер Арена\n\n"
        "Выберите раздел:",
        reply_markup=main_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "pc_restart")
async def pc_restart(callback: CallbackQuery):

    await callback.message.edit_text(
        "⚠️ Вы уверены, что хотите перезагрузить все свободные ПК?",
        reply_markup=confirm_restart_menu()
    )

    await callback.answer()
    
@dp.callback_query(lambda c: c.data == "pc_poweron")
async def pc_poweron(callback: CallbackQuery):

    await callback.answer()

    await callback.message.answer(
        "⚡ Функция включения ПК находится в разработке."
    )


@dp.callback_query(lambda c: c.data == "pc_lock")
async def pc_lock(callback: CallbackQuery):

    await callback.answer()

    await callback.message.answer(
        "🔒 Функция блокировки ПК находится в разработке."
    )


@dp.callback_query(lambda c: c.data == "pc_shutdown")
async def pc_shutdown(callback: CallbackQuery):

    await callback.answer()

    await callback.message.answer(
        "⛔ Функция выключения ПК находится в разработке."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
