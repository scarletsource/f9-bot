from aiogram.utils.keyboard import InlineKeyboardBuilder


def pc_list_menu(pcs):

    builder = InlineKeyboardBuilder()

    for pc in pcs:

        builder.button(
            text=f"🖥 PC-{pc['name']}",
            callback_data=f"pcid_{pc['UUID']}"
        )

    builder.button(
        text="◀️ Назад",
        callback_data="pc"
    )

    builder.adjust(2)

    return builder.as_markup()
