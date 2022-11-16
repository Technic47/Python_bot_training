from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import navigation_data_callback, item_count_callback
from loader import db


def get_item_inline_keyboard(id: int = 1, current_count: int = 0) -> InlineKeyboardMarkup:
    item_inline_keyboard = InlineKeyboardMarkup()
    left_id = id - 1
    right_id = id + 1

    if id == 1:
        btn = InlineKeyboardButton(text='>>>',
                                   callback_data=navigation_data_callback.new(for_data='items', id=right_id))
        item_inline_keyboard.add(btn)
    elif id == len(db.select_all('Items')):
        btn = InlineKeyboardButton(text='<<<',
                                   callback_data=navigation_data_callback.new(for_data='items', id=left_id))
        item_inline_keyboard.add(btn)
    else:
        btn_left = InlineKeyboardButton(text='<<<',
                                        callback_data=navigation_data_callback.new(for_data='items', id=left_id))
        btn_right = InlineKeyboardButton(text='>>>',
                                         callback_data=navigation_data_callback.new(for_data='items', id=right_id))
        item_inline_keyboard.row(btn_left, btn_right)
    item_inline_keyboard.row(InlineKeyboardButton(text='-',
                                                  callback_data=item_count_callback.new(
                                                      target='item_minus',
                                                      id=id,
                                                      current_count=f'{current_count}')
                                                  ),
                             InlineKeyboardButton(text=f'{current_count}',
                                                  callback_data=item_count_callback.new(
                                                      target='None',
                                                      id=id,
                                                      current_count=f'{current_count}'
                                                  )),
                             InlineKeyboardButton(text='+',
                                                  callback_data=item_count_callback.new(
                                                      target='item_plus',
                                                      id=id,
                                                      current_count=f'{current_count}')))
    item_inline_keyboard.row(InlineKeyboardButton(text='Add to basket',
                                                  callback_data=item_count_callback.new(
                                                      target='basket',
                                                      id=id,
                                                      current_count=f'{current_count}'
                                                  )))

    return item_inline_keyboard
