import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile

from langame_api import (
    get_clubs,
    get_routes,
    get_products,
    get_pc_list,
    pc_manage,
    get_pc_types,
    get_pc_linking
)

from keyboards.menu import main_menu
from keyboards.pc_menu import pc_menu, confirm_restart_menu
from keyboards.pc_types import pc_types_menu
from keyboards.pc_list import pc_list_menu
from keyboards.pc_actions import pc_actions_menu

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

@dp.message(Command("pctypes"))
async def pctypes(message: Message):

    data = get_pc_types()

    await message.answer(
        str(data)[:4000]
    )


@dp.message(Command("pclinking"))
async def pclinking(message: Message):

    data = get_pc_linking()

    import json

    with open("pcs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    file = FSInputFile("pcs.json")

    await message.answer_document(
        file,
        caption="Список ПК"
    )
    
@dp.callback_query(lambda c: c.data == "pc")
async def open_pc_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        "🖥 Выберите зону:",
        reply_markup=pc_types_menu()
    )

    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("type_"))
async def show_pcs(callback: CallbackQuery):

    pc_type = int(callback.data.split("_")[1])

    data = get_pc_linking()

    pcs = []

    for pc in data["data"]:

        if pc["packets_type_PC"] == pc_type:

            if pc["name"] is not None:

                pcs.append(pc)

    pcs = sorted(
        pcs,
        key=lambda x: int(x["name"])
    )

    await callback.message.edit_text(
        "🖥 Выберите компьютер:",
        reply_markup=pc_list_menu(pcs)
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

@dp.callback_query(lambda c: c.data.startswith("pcid_"))
async def pc_selected(callback: CallbackQuery):

    uuid = callback.data.replace("pcid_", "")

    await callback.message.edit_text(
        "🖥 Выберите действие:",
        reply_markup=pc_actions_menu(uuid)
    )

    await callback.answer()


@dp.callback_query(
    lambda c:
    c.data.startswith("reboot_")
    or c.data.startswith("poweron_")
    or c.data.startswith("lock_")
    or c.data.startswith("unlock_")
    or c.data.startswith("poweroff_")
    or c.data.startswith("techstart_")
    or c.data.startswith("techstop_")
)
async def pc_action(callback: CallbackQuery):

    action, uuid = callback.data.split("_", 1)

    commands = {
        "reboot": "reboot",
        "poweron": "power_on",
        "lock": "lock",
        "unlock": "unlock",
        "poweroff": "power_off",
        "techstart": "tech_start",
        "techstop": "tech_stop"
    }

    data = pc_manage(
        commands[action],
        uuid
    )

    await callback.message.edit_text(
        f"✅ Команда отправлена.\n\n{data}"
    )

    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
