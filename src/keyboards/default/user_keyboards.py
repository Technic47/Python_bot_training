from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

commands_users_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/add_user'),
            KeyboardButton(text='/delete_user'),
            KeyboardButton(text='/del_all_users')
        ],
        [
            KeyboardButton(text='/update_user'),
            KeyboardButton(text='/show_user'),
            KeyboardButton(text='/show_users')
        ],
        [
            KeyboardButton(text='/new_table_users'),
            KeyboardButton(text='/del_tab_users'),
            KeyboardButton(text='Hide')
        ]
    ],
    resize_keyboard=True
)
