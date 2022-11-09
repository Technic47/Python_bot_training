from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

basket_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='All_items'),
            KeyboardButton(text='My_basket'),
        ],
        [
            KeyboardButton(text='Buy')
        ],
        [
            KeyboardButton(text='Clear_basket')
        ]
    ],
    resize_keyboard=True
)