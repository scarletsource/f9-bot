from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.pc_status import get_status_icon


def pc_list_menu(pcs):

    builder = InlineKeyboardBuilder()

    for pc in pcs:

        icon = get_status_icon(
            pc["UUID"]
        )

        builder.button(
            text=f"{icon} ПК-{int(pc['name']):02}",
            callback_data=f"pcid_{pc['UUID']}"
        )

    builder.button(
        text="◀ Назад",
        callback_data="pc"
    )

    builder.adjust(2)

    return builder.as_markup()
