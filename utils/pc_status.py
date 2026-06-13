import json
import os

from langame_api import get_busy_pcs

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

    print("SAVE")
    print(FILE_NAME)
    print(statuses)

from langame_api import get_busy_pcs


def get_status(uuid):

    statuses = load_statuses()

    local_status = statuses.get(uuid)

    if local_status in [
        "tech",
        "manual_unlock",
        "poweroff"
    ]:
        return local_status

    busy_pcs = get_busy_pcs()

    if uuid in busy_pcs:

        return "session"

    return "free"
    
def get_status_icon(uuid):

    status = get_status(uuid)

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

    status = get_status(uuid)

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
