from aiogram.utils.keyboard import InlineKeyboardBuilder

from langame_api import (
    get_pc_types,
    get_pc_linking
)


def pc_types_menu():

    builder = InlineKeyboardBuilder()

    types_data = get_pc_types()["data"]

    pcs_data = get_pc_linking()["data"]

    # считаем количество ПК каждого типа
    pc_count = {}

    for pc in pcs_data:

        type_id = pc["packets_type_PC"]

        if pc["name"] is None:
            continue

        pc_count[type_id] = pc_count.get(
            type_id,
            0
        ) + 1

    # создаем кнопки только для реально существующих зон
    for pc_type in types_data:

        type_id = pc_type["id"]

        count = pc_count.get(
            type_id,
            0
        )

        # если ПК нет — не показываем зону
        if count == 0:
            continue

        zone_name = pc_type["name"]

        builder.button(
            text=f"{zone_name} ({count})",
            callback_data=f"type_{type_id}"
        )

    builder.button(
        text="🏠 Главное меню",
        callback_data="back_main"
    )

    builder.adjust(1)

    return builder.as_markup()
