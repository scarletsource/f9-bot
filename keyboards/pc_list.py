from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.pc_monitor import (
    get_monitor_status
)


def get_status_icon(uuid):

    status = get_monitor_status(
        uuid
    )

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


def pc_list_menu(pcs):

    builder = InlineKeyboardBuilder()

    for pc in pcs:

        try:

            pc_name = f"{int(pc['name']):02}"

        except:

            pc_name = str(
                pc["name"]
            )

        icon = get_status_icon(
            pc["UUID"]
        )

        builder.button(

            text=f"{icon} ПК-{pc_name}",

            callback_data=f"pcid_{pc['UUID']}"

        )

    builder.button(

        text="◀ Назад",

        callback_data="pc"

    )

    builder.adjust(
        2
    )

    return builder.as_markup()
