from aiogram.utils.keyboard import InlineKeyboardBuilder


def confirm_menu(action, uuid):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Подтвердить",
        callback_data=f"confirm_{action}_{uuid}"
    )

    builder.button(
        text="❌ Отмена",
        callback_data="cancel_action"
    )

    builder.adjust(2)

    return builder.as_markup()
