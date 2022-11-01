from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

commands_root_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/items'),
            KeyboardButton(text='/users'),
        ]
    ],
    resize_keyboard=True
)
