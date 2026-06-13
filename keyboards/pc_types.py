from aiogram.utils.keyboard import InlineKeyboardBuilder

from langame_api import (
    get_pc_types,
    get_pc_linking
)

from utils.pc_monitor import (
    PC_MONITOR
)


def pc_types_menu():

    builder = InlineKeyboardBuilder()

    types_data = get_pc_types()["data"]

    pcs_data = get_pc_linking()["data"]

    total_count = {}
    busy_count = {}

    for pc in pcs_data:

        if pc["name"] is None:
            continue

        type_id = pc["packets_type_PC"]

        total_count[type_id] = total_count.get(
            type_id,
            0
        ) + 1

        uuid = pc["UUID"]

        if uuid in PC_MONITOR:

            status = PC_MONITOR[uuid]["status"]

            if status == "session":

                busy_count[type_id] = busy_count.get(
                    type_id,
                    0
                ) + 1

    for pc_type in types_data:

        type_id = pc_type["id"]

        total = total_count.get(
            type_id,
            0
        )

        if total == 0:
            continue

        busy = busy_count.get(
            type_id,
            0
        )

        free = total - busy

        zone_name = pc_type["name"]

        icon = "🖥"

        if "VIP" in zone_name.upper():
            icon = "👑"

        elif "COMFORT" in zone_name.upper():
            icon = "💎"

        elif "TV" in zone_name.upper():
            icon = "📺"

        elif "STANDART" in zone_name.upper():
            icon = "🎮"

        builder.button(
            text=f"{icon} {zone_name} ({free}/{total})",
            callback_data=f"type_{type_id}"
        )

    builder.button(
        text="🏠 Главное меню",
        callback_data="back_main"
    )

    builder.adjust(1)

    return builder.as_markup()
