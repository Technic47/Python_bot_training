from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

commands_items_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/add_item'),
            KeyboardButton(text='/delete_item'),
            KeyboardButton(text='/del_all_items')
        ],
        [
            KeyboardButton(text='/update_item'),
            KeyboardButton(text='/show_item'),
            KeyboardButton(text='/show_items')
        ],
        [
            KeyboardButton(text='/new_table_items'),
            KeyboardButton(text='/del_tab_items'),
            KeyboardButton(text='Hide')
        ]
    ],
    resize_keyboard=True
)
