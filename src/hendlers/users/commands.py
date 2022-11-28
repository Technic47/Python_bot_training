from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ReplyKeyboardRemove
import aiogram.utils.markdown as md
from .state_classes import *
from keyboards import *
from aiogram import types
from loader import dp, db, bot


@dp.message_handler(commands=['start', 'menu'])
async def answer_start(message: types.Message):
    await message.answer(text=f'Hi!\nNice to see you!', reply_markup=start_keyboard)


@dp.message_handler(commands=['test'])
async def answer_menu_command(message: types.Message, user_basket: tuple[int | str]):
    await message.answer(text='middleware test'
                              f'\n That`s what it gives us: {user_basket}')


@dp.message_handler(text=['admin', 'Admin'])
@dp.message_handler(commands=['admin', 'Admin'])
async def answer_admin(message: types.Message):
    await message.answer(text=f'Lets work with items.', reply_markup=commands_root_keyboard)


@dp.message_handler(commands='users')
async def answer_start(message: types.Message):
    await message.answer(text=f'Lets work with users.', reply_markup=commands_users_keyboard)


@dp.message_handler(text='Hide')
async def answer_hide(message: types.Message):
    await message.answer(text=f'Use /menu pr /start commands to show menu again', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands='new_table_users')
async def create_table(message: types.Message):
    db.create_table_users()
    await message.answer(text=f'Table "Users" created', reply_markup=commands_users_keyboard)


@dp.message_handler(content_types=['contact'])
async def share_contact(message: types.Message):
    if message.contact.user_id == message.from_user.id:
        db.add_user(int(message.from_user.id), str(message.contact.phone_number))
        await message.answer(text=f'Your contact added', reply_markup=commands_users_keyboard)
    else:
        await message.answer(text="Sorry, failed(")


@dp.message_handler(commands='add_user')
async def add_user(message: types.Message):
    await message.answer(text=f'Assign id.')
    await add.state1.set()


@dp.message_handler(state=add.state1)
async def id_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
    await add.next()
    await message.reply('Enter phone number:')
    await add.state2.set()


@dp.message_handler(state=add.state2)
async def phone_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state2'] = message.text
        await bot.send_message(
            message.from_user.id,
            md.text(
                md.text(f'id:', data['state1']),
                md.text(f'phone:', data['state2']),
                md.text(f'Created'),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN)
        db.add_user(int(data['state1']), str(data['state2']))
    await state.finish()


@dp.message_handler(commands='update_user')
async def add_user(message: types.Message):
    await message.answer(text=f'Select user id:')
    await update.state1.set()


@dp.message_handler(state=update.state1)
async def id_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
    await update.next()
    await message.reply('Enter new phone number:')
    await update.state2.set()


@dp.message_handler(state=update.state2)
async def phone_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state2'] = message.text
        db.update_user_phone(int(data['state1']), str(data['state2']))
        await message.answer(text=f"User with id {data['state1']} now has new number {data['state2']}")
    await state.finish()


@dp.message_handler(commands='show_user')
async def show_info(message: types.Message):
    await message.answer(text=f'Select id:')
    await show.state1.set()


@dp.message_handler(state=show.state1)
async def id_find(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
        await message.answer(text=f"{db.select_info('Users', id=int(data['state1']))}")
    await state.finish()


@dp.message_handler(commands='delete_user')
async def delete_user(message: types.Message):
    await message.answer(text=f'Select id:')
    await del_user.state1.set()


@dp.message_handler(state=del_user.state1)
async def id_find_del(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
        db.delete('Users', id=int(data['state1']))
        await message.answer(text=f"User with id {data['state1']} deleted.")
    await state.finish()


@dp.message_handler(commands='show_users')
async def show_users(message: types.Message):
    await message.answer(text='id, phone')
    for item in db.select_all('Users'):
        await message.answer(text=item)


@dp.message_handler(commands='del_all_users')
async def delete_all(message: types.Message):
    db.delete_all('Users')
    await message.answer(text='All users are deleted')


@dp.message_handler(commands='del_tab_users')
async def drop_all(message: types.Message):
    db.drop_all('Users')
    await message.answer(text='Table "Users" deleted')
