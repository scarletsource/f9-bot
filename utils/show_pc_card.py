from utils.pc_monitor import (
    get_monitor_status,
    get_monitor_guest,
    get_monitor_play_time,
    get_monitor_pc_name,
    get_monitor_zone_name
)

from utils.pc_history import get_history


def get_monitor_user(uuid):

    guest = get_monitor_guest(uuid)

    if guest is None:

        return "Свободен"

    return f"ID {guest}"


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

    return icons.get(
        status,
        "⚪"
    )


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

    return names.get(
        status,
        "Неизвестно"
    )


def show_pc_card(uuid):

    pc_name = get_monitor_pc_name(
        uuid
    )

    zone_name = get_monitor_zone_name(
        uuid
    )

    history = get_history(
        uuid
    )

    if len(history) == 0:

        history_text = "Нет данных"

    else:

        history_text = "\n".join(
            history
        )

    try:

        pc_number = f"{int(pc_name):02}"

    except:

        pc_number = str(pc_name)

    text = (

        f"🖥 <b>ПК-{pc_number}</b>\n\n"

        f"📊 Статус\n"
        f"{get_status_icon_live(uuid)} "
        f"{get_status_name_live(uuid)}\n\n"

        f"📍 Зона\n"
        f"{zone_name}\n\n"

        f"👤 Пользователь\n"
        f"{get_monitor_user(uuid)}\n\n"

        f"⏳ Время игры\n"
        f"{get_monitor_play_time(uuid)}\n\n"

        f"📜 История действий\n"
        f"{history_text}\n\n"

        f"🆔 UUID\n"
        f"<code>{uuid}</code>\n\n"

        "━━━━━━━━━━━━━━"

    )

    return text
