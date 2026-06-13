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

from utils.pc_status import (
    set_status,
    get_status,
    get_status_icon,
    get_status_name
)

from utils.pc_history import (
    add_history,
    get_history
)

from keyboards.confirm_menu import confirm_menu
from keyboards.result_menu import result_menu
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

@dp.message(Command("routes"))
async def routes(message: Message):

    data = get_routes()

    await message.answer(
        str(data)[:4000]
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

    uuid = callback.data.replace(
        "pcid_",
        ""
    )

    data = get_pc_linking()

    pc_name = "Неизвестно"
    zone_name = "Неизвестно"

    zones = {
        1: "🟢 Standard",
        2: "🟣 VIP",
        3: "🔵 Bootcamp"
    }

    for pc in data["data"]:

        if pc["UUID"] == uuid:

            pc_name = pc["name"]

            zone_name = zones.get(
                pc["packets_type_PC"],
                "⚪ Неизвестно"
            )

            break
            
            history = get_history(uuid)

history_text = ""

for item in history:

    history_text += f"{item}\n"

if history_text == "":

    history_text = "Нет данных"

    text = (
    f"🖥 <b>ПК-{int(pc_name):02}</b>\n\n"

    f"📊 Статус\n"
    f"{get_status_icon(uuid)} {get_status_name(uuid)}\n\n"

    f"📍 Зона\n"
    f"{zone_name}\n\n"

    f"👤 Пользователь\n"
    f"Свободен\n\n"

    f"📜 История действий\n"
    f"{history_text}\n"

    f"🆔 UUID\n"
    f"<code>{uuid}</code>\n\n"

    "━━━━━━━━━━━━━━"
)

    await callback.message.edit_text(
        text,
        reply_markup=pc_actions_menu(uuid),
        parse_mode="HTML"
    )

    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("action_"))
async def pc_action(callback: CallbackQuery):

    data = callback.data.split("_")

    action = data[1]
    uuid = "_".join(data[2:])

    names = {
        "reboot": "🔄 Перезагрузка",
        "poweron": "⚡ Включение",
        "lock": "🔒 Блокировка",
        "unlock": "🔓 Ручная разблокировка",
        "poweroff": "⛔ Выключение",
        "techstart": "🛠 Тех старт",
        "techstop": "🛠 Тех стоп"
    }

    await callback.message.edit_text(
        f"⚠ Подтвердите действие\n\n"
        f"{names[action]}",
        reply_markup=confirm_menu(
            action,
            uuid
        )
    )

    await callback.answer()
    
@dp.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_action(callback: CallbackQuery):

    data = callback.data.split("_")

    action = data[1]
    uuid = "_".join(data[2:])

    commands = {
        "reboot": "reboot",
        "poweron": "power_on",
        "lock": "lock",
        "unlock": "unlock",
        "poweroff": "power_off",
        "techstart": "tech_start",
        "techstop": "tech_stop"
    }

    names = {
        "reboot": "🔄 Перезагрузка",
        "poweron": "⚡ Включение",
        "lock": "🔒 Блокировка",
        "unlock": "🔓 Ручная разблокировка",
        "poweroff": "⛔ Выключение",
        "techstart": "🛠 Тех старт",
        "techstop": "🛠 Тех стоп"
    }

    # Изменение локального статуса
    if action == "techstart":
        set_status(
            uuid,
            "tech"
        )

    elif action == "techstop":
        set_status(
            uuid,
            "free"
        )

    elif action == "unlock":
        set_status(
            uuid,
            "manual_unlock"
        )

    elif action == "lock":
        set_status(
            uuid,
            "free"
        )

    elif action == "poweroff":
        set_status(
            uuid,
            "poweroff"
        )

    elif action == "poweron":
        set_status(
            uuid,
            "free"
        )

    elif action == "reboot":
        set_status(
            uuid,
            "busy"
        )

    # Отправка команды в LANGame
    response = pc_manage(
        commands[action],
        uuid
    )
    
    add_history(
    uuid,
    names[action]
)
    await callback.message.edit_text(
        f"✅ Команда успешно отправлена\n\n"
        f"Действие:\n{names[action]}",
        reply_markup=result_menu()
    )

    await callback.answer()

@dp.callback_query(lambda c: c.data == "cancel_action")
async def cancel_action(callback: CallbackQuery):

    await callback.message.edit_text(
        "❌ Действие отменено",
        reply_markup=result_menu()
    )

    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
