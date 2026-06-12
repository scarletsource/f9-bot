from aiogram.utils.keyboard import InlineKeyboardBuilder


def pc_types_menu():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🎮 Game Арена",
        callback_data="type_1"
    )

    builder.button(
        text="👑 VIP Арена",
        callback_data="type_2"
    )

    builder.button(
        text="💎 Comfort Арена",
        callback_data="type_3"
    )

    builder.button(
        text="📺 TV",
        callback_data="type_4"
    )

    builder.button(
        text="👥 DUO ROOM",
        callback_data="type_5"
    )

    builder.button(
        text="◀️ Назад",
        callback_data="back_main"
    )

    builder.adjust(1)

    return builder.as_markup()
