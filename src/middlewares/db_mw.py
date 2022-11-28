from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import db


class GetDBUser(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        data['get_user_basket'] = db.select_user_basket(user_id=message.from_user.id)
        data['some_data'] = 'INFO'

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        # data['del_user_basket'] = db.clear_basket(user_id=call.from_user.id)
        data['info'] = 'some_info'
