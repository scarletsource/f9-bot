import json
import os
from datetime import datetime

from langame_api import (
    get_busy_pcs,
    get_pc_session
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FILE_NAME = os.path.join(
    BASE_DIR,
    "pc_status.json"
)

print("STATUS FILE =", FILE_NAME)


def load_statuses():

    if not os.path.exists(FILE_NAME):

        with open(FILE_NAME, "w", encoding="utf-8") as f:

            json.dump({}, f)

    with open(FILE_NAME, "r", encoding="utf-8") as f:

        return json.load(f)


def save_statuses(statuses):

    with open(FILE_NAME, "w", encoding="utf-8") as f:

        json.dump(
            statuses,
            f,
            ensure_ascii=False,
            indent=4
        )


def set_status(uuid, status):

    statuses = load_statuses()

    statuses[uuid] = status

    save_statuses(statuses)


def get_real_status(uuid):

    statuses = load_statuses()

    local_status = statuses.get(uuid)

    # Приоритет локальных режимов
    if local_status == "poweroff":

        return "poweroff"

    if local_status == "tech":

        return "tech"

    if local_status == "manual_unlock":

        return "manual_unlock"

    # Проверка активной сессии
    busy_pcs = get_busy_pcs()

    if uuid in busy_pcs:

        return "session"

    return "free"


def get_status(uuid):

    return get_real_status(uuid)


def get_status_icon(uuid):

    status = get_real_status(uuid)

    icons = {
        "free": "🟢",
        "session": "🔵",
        "tech": "🟡",
        "manual_unlock": "🟣",
        "poweroff": "🔴",
        "offline": "⚫",
        "busy": "🟠",
        "service": "🟤",
        "error": "🚨"
    }

    return icons.get(
        status,
        "⚪"
    )


def get_status_name(uuid):

    status = get_real_status(uuid)

    names = {
        "free": "Свободен",
        "session": "На сессии",
        "tech": "Техрежим",
        "manual_unlock": "Ручная разблокировка",
        "poweroff": "Выключен",
        "offline": "Недоступен",
        "busy": "Выполняется команда",
        "service": "Обслуживание",
        "error": "Ошибка"
    }

    return names.get(
        status,
        "Неизвестно"
    )


def get_pc_user(uuid):

    session = get_pc_session(uuid)

    if session is None:

        return "Свободен"

    return f"ID {session['guest_id']}"


def get_pc_start_time(uuid):

    session = get_pc_session(uuid)

    if session is None:

        return "-"

    return session["date_start"]


def get_pc_play_time(uuid):

    session = get_pc_session(uuid)

    if session is None:

        return "-"

    start = datetime.strptime(
        session["date_start"],
        "%Y-%m-%d %H:%M:%S"
    )

    delta = datetime.now() - start

    hours = delta.seconds // 3600

    minutes = (delta.seconds % 3600) // 60

    return f"{hours}ч {minutes}м"
