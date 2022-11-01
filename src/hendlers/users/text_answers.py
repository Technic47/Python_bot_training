from aiogram import types
from loader import dp


@dp.message_handler(text='text')
async def answer_text(message: types.Message):
    await message.answer(text='This is a serious place. No chat allowed!')
