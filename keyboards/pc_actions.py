from aiogram.utils.keyboard import InlineKeyboardBuilder


def pc_actions_menu(uuid):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔄 Перезагрузить",
        callback_data=f"reboot_{uuid}"
    )

    builder.button(
        text="⚡ Включить",
        callback_data=f"poweron_{uuid}"
    )

    builder.button(
        text="🔒 Заблокировать",
        callback_data=f"lock_{uuid}"
    )

    builder.button(
        text="🔓 Разблокировать",
        callback_data=f"unlock_{uuid}"
    )

    builder.button(
        text="⛔ Выключить",
        callback_data=f"poweroff_{uuid}"
    )

    builder.button(
        text="🛠 Тех старт",
        callback_data=f"techstart_{uuid}"
    )

    builder.button(
        text="🛠 Тех стоп",
        callback_data=f"techstop_{uuid}"
    )

    builder.button(
        text="◀️ Назад",
        callback_data="pc"
    )

    builder.adjust(2, 2, 2, 1, 1)

    return builder.as_markup()
