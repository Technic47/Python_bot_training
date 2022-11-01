import sqlite3

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config import TOKEN
from db_api import DB

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db_path = r'db_api\DataBase\shop_db.db'
db = DB(path_db=db_path)

try:
    db.create_table_users()
except sqlite3.OperationalError as e:
    print(e)
except Exception as e:
    print(e)

try:
    db.create_table_items()
except sqlite3.OperationalError as e:
    print(e)
except Exception as e:
    print(e)
