PC_STATUS = {}


def set_status(uuid, status):

    PC_STATUS[uuid] = status


def get_status(uuid):

    return PC_STATUS.get(uuid, "free")


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

    return icons.get(status, "⚪")


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

    return names.get(status, "Неизвестно")
