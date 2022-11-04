from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback_data import navigation_data_callback
from src.loader import db


def get_item_inline_keyboard(id: int = 1) -> InlineKeyboardMarkup:
    item_inline_keyboard = InlineKeyboardMarkup()
    left_id = id - 1
    right_id = id + 1
    if id == 1:
        btn = InlineKeyboardButton(text='>>>',
                                   callback_data=navigation_data_callback.new(for_data='items', id=right_id))
        item_inline_keyboard.add(btn)
    elif id == db.get_item_count():
        btn = InlineKeyboardButton(text='<<<',
                                   callback_data=navigation_data_callback.new(for_data='items', id=left_id))
        item_inline_keyboard.add(btn)
    else:
        btn_left = InlineKeyboardButton(text='<<<',
                                        callback_data=navigation_data_callback.new(for_data='items', id=right_id))
        btn_right = InlineKeyboardButton(text='>>>',
                                         callback_data=navigation_data_callback.new(for_data='items', id=left_id))
        item_inline_keyboard.row(btn_left, btn_right)

    return item_inline_keyboard