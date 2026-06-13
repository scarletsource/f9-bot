from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.pc_monitor import get_all_zones


def pc_types_menu():

    builder = InlineKeyboardBuilder()

    zones = get_all_zones()

    for type_id, zone_name in zones.items():

        builder.button(

            text=zone_name,

            callback_data=f"type_{type_id}"

        )

    builder.button(

        text="🏠 Главное меню",

        callback_data="back_main"

    )

    builder.adjust(1)

    return builder.as_markup()
