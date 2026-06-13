from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.pc_monitor import (
    get_pc_by_uuid
)


def get_pc_icon(uuid):

    pc = get_pc_by_uuid(uuid)

    if pc is None:

        return "⚫"

    #
    # Сначала действия
    #

    if pc["action_state"] == "reboot":

        return "🔄"

    if pc["power_state"] == "shutdown":

        return "⚫"

    if pc["mode_state"] == "tech":

        return "🛠"

    if pc["mode_state"] == "manual_unlock":

        return "🔓"

    if pc["session_state"]:

        return "🔵"

    return "🟢"


def pc_list_menu(pcs):

    builder = InlineKeyboardBuilder()

    for pc in pcs:

        icon = get_pc_icon(
            pc["UUID"]
        )

        try:

            pc_name = f"{int(pc['name']):02}"

        except:

            pc_name = str(
                pc["name"]
            )

        builder.button(

            text=f"{icon} ПК-{pc_name}",

            callback_data=f"pcid_{pc['UUID']}"

        )

    builder.button(

        text="◀ Назад",

        callback_data="pc"

    )

    builder.adjust(2)

    return builder.as_markup()
