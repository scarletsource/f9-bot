from aiogram.utils.keyboard import InlineKeyboardBuilder


def pc_actions_menu():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔄 Перезагрузить",
        callback_data="reboot"
    )

    builder.button(
        text="⚡ Включить",
        callback_data="poweron"
    )

    builder.button(
        text="🔒 Заблокировать",
        callback_data="lock"
    )

    builder.button(
        text="🔓 Разблокировать",
        callback_data="unlock"
    )

    builder.button(
        text="⛔ Выключить",
        callback_data="poweroff"
    )

    builder.button(
        text="🛠 Тех старт",
        callback_data="techstart"
    )

    builder.button(
        text="🛠 Тех стоп",
        callback_data="techstop"
    )

    builder.button(
        text="◀️ Назад",
        callback_data="pc"
    )

    builder.adjust(2, 2, 2, 1, 1)

    return builder.as_markup()
