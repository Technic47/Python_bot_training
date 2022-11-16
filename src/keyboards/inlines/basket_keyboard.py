from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import basket_callback

basket_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Clear',
                                 callback_data=basket_callback.new(
                                     action='del_basket'
                                 ))
        ],
        [
            InlineKeyboardButton(text='Place an order',
                                 callback_data=basket_callback.new(
                                     action='buy'
                                 ))
        ]
    ])
