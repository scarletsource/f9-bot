from aiogram.utils.keyboard import InlineKeyboardBuilder


def pc_actions_menu(uuid):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔄 Перезагрузка",
        callback_data=f"action_reboot_{uuid}"
    )

    builder.button(
        text="⚡ Включить",
        callback_data=f"action_poweron_{uuid}"
    )

    builder.button(
        text="⛔ Выключить",
        callback_data=f"action_poweroff_{uuid}"
    )

    builder.button(
        text="🔒 Заблокировать",
        callback_data=f"action_lock_{uuid}"
    )

    builder.button(
        text="🔓 Разблокировать",
        callback_data=f"action_unlock_{uuid}"
    )

    builder.button(
        text="🛠 Тех старт",
        callback_data=f"action_techstart_{uuid}"
    )

    builder.button(
        text="🟢 Тех стоп",
        callback_data=f"action_techstop_{uuid}"
    )

    builder.button(
        text="◀ Назад",
        callback_data="pc"
    )

    builder.adjust(2)

    return builder.as_markup()
