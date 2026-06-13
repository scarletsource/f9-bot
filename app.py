import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    ReplyKeyboardRemove
)

from langame_api import (
    get_clubs,
    get_products,
    pc_manage,
    get_adminconsole,
    get_all_operations_log,
    get_guest_logs,
    get_working_shifts
)

from utils.pc_monitor import (
    monitor_pcs,
    get_monitor_pc_name,
    set_power_state,
    set_mode_state,
    set_action_state,
    get_all_pcs
)

from utils.show_pc_card import show_pc_card

from utils.pc_history import (
    add_history
)

from utils.club_history import (
    add_club_history,
    get_club_history
)

from keyboards.menu import main_menu
from keyboards.confirm_menu import confirm_menu
from keyboards.result_menu import result_menu
from keyboards.pc_types import pc_types_menu
from keyboards.pc_list import pc_list_menu
from keyboards.pc_actions import pc_actions_menu
from keyboards.club_history_menu import club_history_menu


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "Обновляю интерфейс...",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "👋 Добро пожаловать в F9 Кибер Арена\n\n"
        "Выберите раздел:",
        reply_markup=main_menu()
    )


@dp.message(Command("operations"))
async def operations(message: Message):

    data = get_all_operations_log()

    await message.answer(
        str(data)[:4000]
    )


@dp.message(Command("shifts"))
async def shifts(message: Message):

    data = get_working_shifts()

    await message.answer(
        str(data)[:4000]
    )


@dp.message(Command("guestlogs"))
async def guestlogs(message: Message):

    import json

    data = get_guest_logs()

    with open(
        "guest_logs.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    file = FSInputFile(
        "guest_logs.json"
    )

    await message.answer_document(
        file
    )


@dp.message(Command("adminconsole"))
async def adminconsole(message: Message):

    import json

    data = get_adminconsole()

    with open(
        "adminconsole.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    file = FSInputFile(
        "adminconsole.json"
    )

    await message.answer_document(
        file
    )


@dp.callback_query(
    lambda c: c.data == "pc"
)
async def open_pc_menu(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "🖥 Выберите зону:",
        reply_markup=pc_types_menu()
    )

    await callback.answer()


@dp.callback_query(
    lambda c: c.data.startswith("type_")
)
async def show_pcs(
    callback: CallbackQuery
):

    pc_type = int(
        callback.data.split("_")[1]
    )

    pcs = []

    all_pcs = get_all_pcs()

    for uuid, pc in all_pcs.items():

        if pc["type_id"] == pc_type:

            if pc["pc_name"] is not None:

                pcs.append({

                    "UUID": uuid,

                    "name": pc["pc_name"]

                })

    pcs = sorted(
        pcs,
        key=lambda x: int(x["name"])
    )

    await callback.message.edit_text(
        "🖥 Выберите компьютер:",
        reply_markup=pc_list_menu(
            pcs
        )
    )

    await callback.answer()

@dp.callback_query(
    lambda c: c.data == "back_main"
)
async def back_main(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "👋 Добро пожаловать в F9 Кибер Арена\n\n"
        "Выберите раздел:",
        reply_markup=main_menu()
    )

    await callback.answer()


@dp.callback_query(
    lambda c: c.data.startswith("pcid_")
)
async def pc_selected(
    callback: CallbackQuery
):

    uuid = callback.data.replace(
        "pcid_",
        ""
    )

    await callback.message.edit_text(
        show_pc_card(
            uuid
        ),
        reply_markup=pc_actions_menu(
            uuid
        ),
        parse_mode="HTML"
    )

    await callback.answer()


@dp.callback_query(
    lambda c: c.data.startswith("action_")
)
async def pc_action(
    callback: CallbackQuery
):

    data = callback.data.split(
        "_"
    )

    action = data[1]

    uuid = "_".join(
        data[2:]
    )

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
        "⚠ Подтвердите действие\n\n"
        f"{names[action]}",
        reply_markup=confirm_menu(
            action,
            uuid
        )
    )

    await callback.answer()

@dp.callback_query(
    lambda c: c.data.startswith("confirm_")
)
@dp.callback_query(
    lambda c: c.data.startswith("confirm_")
)
async def confirm_action(
    callback: CallbackQuery
):

    data = callback.data.split("_")

    action = data[1]

    uuid = "_".join(
        data[2:]
    )

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

    #
    # Обновляем состояние ПК
    #

    if action == "techstart":

        set_mode_state(
            uuid,
            "tech"
        )

    elif action == "techstop":

        set_mode_state(
            uuid,
            "normal"
        )

    elif action == "unlock":

        set_mode_state(
            uuid,
            "manual_unlock"
        )

    elif action == "lock":

        set_mode_state(
            uuid,
            "normal"
        )

    elif action == "poweroff":

        set_power_state(
            uuid,
            "shutdown"
        )

    elif action == "poweron":

        set_power_state(
            uuid,
            "online"
        )

    elif action == "reboot":

        set_action_state(
            uuid,
            "reboot"
        )

    #
    # Отправляем команду в LANGame
    #

    response = pc_manage(
        commands[action],
        uuid
    )

    #
    # История ПК
    #

    add_history(
        uuid,
        names[action]
    )

    #
    # История клуба
    #

    pc_name = get_monitor_pc_name(
        uuid
    )

    try:

        pc_number = int(
            pc_name
        )

    except:

        pc_number = 0

    club_names = {

        "reboot":
        "🔄 ПК-{:02} перезагружен",

        "poweron":
        "⚡ ПК-{:02} включен",

        "lock":
        "🔒 ПК-{:02} заблокирован",

        "unlock":
        "🔓 ПК-{:02} разблокирован",

        "poweroff":
        "⛔ ПК-{:02} выключен",

        "techstart":
        "🛠 ПК-{:02} переведен в техрежим",

        "techstop":
        "🟢 ПК-{:02} выведен из техрежима"

    }

    add_club_history(

        club_names[action].format(
            pc_number
        )

    )

    await callback.message.edit_text(

        "✅ Команда успешно отправлена\n\n"
        f"Действие:\n{names[action]}",

        reply_markup=result_menu()

    )

    await callback.answer()

    data = callback.data.split("_")

    action = data[1]

    uuid = "_".join(
        data[2:]
    )

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

    # Меняем локальный статус
    if action == "techstart":

        set_monitor_status(
            uuid,
            "tech"
        )

    elif action == "techstop":

        set_monitor_status(
            uuid,
            "free"
        )

    elif action == "unlock":

        set_monitor_status(
            uuid,
            "manual_unlock"
        )

    elif action == "lock":

        set_monitor_status(
            uuid,
            "free"
        )

    elif action == "poweroff":

        set_monitor_status(
            uuid,
            "poweroff"
        )

    elif action == "poweron":

        set_monitor_status(
            uuid,
            "free"
        )

    elif action == "reboot":

        set_monitor_status(
            uuid,
            "busy"
        )

    # Отправляем команду в LANGame
    response = pc_manage(
        commands[action],
        uuid
    )

    # Сохраняем историю ПК
    add_history(
        uuid,
        names[action]
    )

    # Получаем номер ПК из монитора
    pc_name = get_monitor_pc_name(
        uuid
    )

    try:

        pc_number = int(
            pc_name
        )

    except:

        pc_number = 0

    club_names = {
        "reboot": "🔄 ПК-{:02} перезагружен",
        "poweron": "⚡ ПК-{:02} включен",
        "lock": "🔒 ПК-{:02} заблокирован",
        "unlock": "🔓 ПК-{:02} разблокирован",
        "poweroff": "⛔ ПК-{:02} выключен",
        "techstart": "🛠 ПК-{:02} переведен в техрежим",
        "techstop": "🟢 ПК-{:02} выведен из техрежима"
    }

    add_club_history(
        club_names[action].format(
            pc_number
        )
    )

    await callback.message.edit_text(
        "✅ Команда успешно отправлена\n\n"
        f"Действие:\n{names[action]}",
        reply_markup=result_menu()
    )

    await callback.answer()

@dp.callback_query(
    lambda c: c.data == "cancel_action"
)
async def cancel_action(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "❌ Действие отменено",
        reply_markup=result_menu()
    )

    await callback.answer()


@dp.callback_query(
    lambda c: c.data == "club_history"
)
async def club_history(
    callback: CallbackQuery
):

    history = get_club_history()

    text = (
        "📋 <b>Последние действия клуба</b>\n\n"
        "━━━━━━━━━━━━━━\n\n"
    )

    if len(history) == 0:

        text += "Нет данных"

    else:

        for item in history:

            text += f"{item}\n"

    text += (
        "\n━━━━━━━━━━━━━━\n\n"
        f"Всего записей: {len(history)}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=club_history_menu(),
        parse_mode="HTML"
    )

    await callback.answer()


async def main():

    asyncio.create_task(
        monitor_pcs()
    )

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )
