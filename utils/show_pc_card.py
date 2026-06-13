from langame_api import get_pc_linking

from utils.pc_monitor import (
    get_monitor_status,
    get_monitor_guest,
    get_monitor_play_time
)

from utils.pc_monitor import (
    get_monitor_status
)

from utils.pc_history import get_history

def get_status_icon_live(uuid):

    status = get_monitor_status(uuid)

    icons = {
        "free": "🟢",
        "session": "🔵",
        "tech": "🟡",
        "manual_unlock": "🟣",
        "busy": "🟠",
        "poweroff": "🔴",
        "shutdown": "⚫",
        "error": "🚨"
    }

    return icons.get(status, "⚪")


def get_status_name_live(uuid):

    status = get_monitor_status(uuid)

    names = {
        "free": "Свободен",
        "session": "На сессии",
        "tech": "Техрежим",
        "manual_unlock": "Ручная разблокировка",
        "busy": "Выполняется команда",
        "poweroff": "Выключается",
        "shutdown": "Выключен",
        "error": "Ошибка"
    }

    return names.get(status, "Неизвестно")

def show_pc_card(uuid):

    data = get_pc_linking()

    pc_name = "Неизвестно"
    zone_name = "Неизвестно"

    zones = {
    1: "🟢 STANDART",
    2: "🟣 VIP",
    3: "🔵 COMFORT",
    4: "📺 TV"
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
        f"{get_status_icon_live(uuid)} {get_status_name_live(uuid)}\n\n"

        f"📍 Зона\n"
        f"{zone_name}\n\n"

        f"👤 Пользователь\n"
        f"{get_pc_user(uuid)}\n\n"

        f"⏳ Время игры\n"
        f"{get_pc_play_time(uuid)}\n\n"

        f"📜 История действий\n"
        f"{history_text}\n"

        f"🆔 UUID\n"
        f"<code>{uuid}</code>\n\n"

        "━━━━━━━━━━━━━━"
    )

    return text
