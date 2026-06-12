from aiogram.utils.keyboard import InlineKeyboardBuilder


def pc_menu():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔄 Перезагрузка ПК",
        callback_data="pc_restart"
    )

    builder.button(
        text="⚡ Включить ПК",
        callback_data="pc_poweron"
    )

    builder.button(
        text="🔒 Заблокировать ПК",
        callback_data="pc_lock"
    )

    builder.button(
        text="⛔ Выключить ПК",
        callback_data="pc_shutdown"
    )

    builder.button(
        text="◀️ Назад",
        callback_data="back_main"
    )

    builder.adjust(2, 2, 1)

    return builder.as_markup()
