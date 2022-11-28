from aiogram import Dispatcher
from .db_mw import GetDBUser


def setup(dp: Dispatcher):
    dp.middleware.setup(GetDBUser())
