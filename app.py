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
    get_pc_types,
    get_pc_linking,
    get_adminconsole,
    pc_manage
)

from utils.show_pc_card import show_pc_card

from utils.pc_status import (
    set_status
)

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

@dp.message(Command("checkpc"))
async def checkpc(message: Message):

    from langame_api import get_pc_linking, get_guest_sessions

    pcs = get_pc_linking()
    sessions = get_guest_sessions()

    text = ""

    for pc in pcs["data"]:

        if pc["packets_type_PC"] == 3:

            text += (
                f"ПК-{pc['name']}\n"
                f"{pc['UUID']}\n\n"
            )

    await message.answer(
        text[:4000]
    )

@dp.message(Command("adminconsole"))
async def adminconsole(message: Message):

    data = get_adminconsole()

    import json

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

    with open(
        "pcs.json",
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
        "pcs.json"
    )

    await message.answer_document(
        file,
        caption="Список ПК"
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

    data = get_pc_linking()

    pcs = []

    for pc in data["data"]:

        if (
            pc["packets_type_PC"] == pc_type
            and pc["name"] is not None
        ):

            pcs.append(
                pc
            )

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
        show_pc_card(uuid),
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
async def confirm_action(
    callback: CallbackQuery
):

    data = callback.data.split(
        "_"
    )

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

    response = pc_manage(
        commands[action],
        uuid
    )

    add_history(
        uuid,
        names[action]
    )

    pc_name = "Неизвестно"

    data_pc = get_pc_linking()

    for pc in data_pc["data"]:

        if pc["UUID"] == uuid:

            pc_name = pc["name"]

            break

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
            int(pc_name)
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

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )
