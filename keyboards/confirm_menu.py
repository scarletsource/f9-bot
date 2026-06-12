from aiogram.utils.keyboard import InlineKeyboardBuilder


def confirm_menu():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Подтвердить",
        callback_data="confirm_action"
    )

    builder.button(
        text="❌ Отмена",
        callback_data="cancel_action"
    )

    builder.adjust(2)

    return builder.as_markup()
