from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='All_items'),
            KeyboardButton(text='My_basket'),
        ],
    ],
    resize_keyboard=True
)
