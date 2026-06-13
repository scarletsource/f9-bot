from langame_api import get_pc_linking

from utils.pc_status import (
    get_status_icon,
    get_status_name,
    get_pc_user,
    get_pc_play_time
)

from utils.pc_history import get_history


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
        f"{get_status_icon(uuid)} {get_status_name(uuid)}\n\n"

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
