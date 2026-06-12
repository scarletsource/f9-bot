from aiogram.utils.keyboard import InlineKeyboardBuilder


def result_menu():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔙 К компьютерам",
        callback_data="pc"
    )

    builder.button(
        text="🏠 Главное меню",
        callback_data="back_main"
    )

    builder.adjust(1)

    return builder.as_markup()
