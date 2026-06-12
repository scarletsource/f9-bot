python
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu():

    builder = InlineKeyboardBuilder()

    builder.button(text="👤 Профиль", callback_data="profile")
    builder.button(text="💰 Баланс", callback_data="balance")

    builder.button(text="⭐ Бонусы", callback_data="bonus")
    builder.button(text="🎮 История", callback_data="sessions")

    builder.button(text="🥤 Склад", callback_data="goods")
    builder.button(text="💵 Продажи", callback_data="sales")

    builder.button(text="📊 Статистика", callback_data="stats")
    builder.button(text="🖥 Компьютеры", callback_data="pc")

    builder.button(text="⚙️ Админка", callback_data="admin")

    builder.adjust(2, 2, 2, 2, 1)

    return builder.as_markup()
