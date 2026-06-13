from aiogram.utils.keyboard import InlineKeyboardBuilder


def club_history_menu():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔄 Обновить",
        callback_data="club_history"
    )

    builder.button(
        text="🏠 Главное меню",
        callback_data="back_main"
    )

    builder.adjust(2)

    return builder.as_markup()
