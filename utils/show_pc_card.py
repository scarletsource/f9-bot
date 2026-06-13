from utils.pc_monitor import (
    get_pc_by_uuid,
    get_monitor_play_time
)

from utils.pc_history import get_history


def show_pc_card(uuid):

    pc = get_pc_by_uuid(
        uuid
    )

    if pc is None:

        return (
            "❌ Компьютер не найден"
        )

    pc_name = pc["pc_name"]

    zone_name = pc["zone_name"]

    guest_id = pc["guest_id"]

    session_state = pc["session_state"]

    power_state = pc["power_state"]

    mode_state = pc["mode_state"]

    action_state = pc["action_state"]

    # ===== Игровая сессия =====

    if session_state:

        session_text = (
            f"🎮 Да\n"
            f"👤 ID {guest_id}\n"
            f"⏳ {get_monitor_play_time(uuid)}"
        )

    else:

        session_text = "Нет"

    # ===== Питание =====

    power_names = {

        "online": "🟢 Включен",

        "shutdown": "⚫ Выключен",

        "offline": "🔴 Нет связи"

    }

    power_text = power_names.get(
        power_state,
        "Неизвестно"
    )

    # ===== Режим =====

    mode_names = {

        "normal": "Обычный",

        "tech": "🛠 Техрежим",

        "manual_unlock": "🔓 Ручная разблокировка"

    }

    mode_text = mode_names.get(
        mode_state,
        "Неизвестно"
    )

    # ===== Действие =====

    action_names = {

        "none": "Нет",

        "reboot": "🔄 Перезагрузка",

        "poweroff": "⛔ Выключение",

        "poweron": "⚡ Включение",

        "busy": "🟠 Выполняется команда"

    }

    action_text = action_names.get(
        action_state,
        "Нет"
    )

    # ===== История =====

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

        pc_number = str(
            pc_name
        )

    text = (

        f"🖥 <b>ПК-{pc_number}</b>\n\n"

        f"📍 Зона\n"
        f"{zone_name}\n\n"

        f"🎮 Игровая сессия\n"
        f"{session_text}\n\n"

        f"⚡ Питание\n"
        f"{power_text}\n\n"

        f"🛠 Режим\n"
        f"{mode_text}\n\n"

        f"🔄 Текущее действие\n"
        f"{action_text}\n\n"

        f"📜 История действий\n"
        f"{history_text}\n\n"

        f"🆔 UUID\n"
        f"<code>{uuid}</code>"

    )

    return text
