from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Профиль"),
            KeyboardButton(text="💰 Баланс")
        ],
        [
            KeyboardButton(text="⭐ Бонусы"),
            KeyboardButton(text="🎮 История")
        ],
        [
            KeyboardButton(text="🥤 Склад"),
            KeyboardButton(text="💵 Продажи")
        ],
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="🖥 Компьютеры")
        ],
        [
            KeyboardButton(text="⚙️ Админка")
        ]
    ],
    resize_keyboard=True
)
