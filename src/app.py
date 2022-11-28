from aiogram import executor
from hendlers import dp
import middlewares

if __name__ == '__main__':
    middlewares.setup(dp)
    executor.start_polling(dispatcher=dp)
