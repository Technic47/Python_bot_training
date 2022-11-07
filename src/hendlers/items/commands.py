from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ReplyKeyboardRemove, InputFile, InputMediaPhoto
import aiogram.utils.markdown as md
from .state_classes import *
from keyboards import *
from aiogram import types
from loader import dp, db, bot


@dp.message_handler(commands=['start', 'menu'])
async def answer_start(message: types.Message):
    await message.answer(text=f'Hi!\nNice to see you!', reply_markup=basket_keyboard)


@dp.message_handler(commands='items')
async def answer_start(message: types.Message):
    await message.answer(text=f'Lets work with items.', reply_markup=commands_items_keyboard)


@dp.message_handler(commands='users')
async def answer_start(message: types.Message):
    await message.answer(text=f'Lets work with users.', reply_markup=commands_users_keyboard)


@dp.message_handler(text='Hide')
async def answer_hide(message: types.Message):
    await message.answer(text=f'Use /menu pr /start commands to show menu again', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=['all_items', 'All_items'])
@dp.message_handler(text=['all_items', 'All_items'])
async def all_items(message: types.Message):
    first_item_info = db.select_item_info(id=1)
    first_item_info = first_item_info[0]
    _, name, quantity, photo_path = first_item_info
    item_text = f"Item name = {name}" \
                f"\nQuantity = {quantity}"
    photo = InputFile(path_or_bytesio=photo_path)
    await message.answer_photo(photo=photo,
                               caption=item_text,
                               reply_markup=get_item_inline_keyboard())


@dp.callback_query_handler(navigation_data_callback.filter(for_data='items'))
async def see_new_item(call: types.CallbackQuery):
    # print(call)
    # print(call.data)
    current_item_id = int(call.data.split(':')[-1])
    first_item_info = db.select_item_info(id=current_item_id)
    first_item_info = first_item_info[0]
    _, name, quantity, photo_path = first_item_info
    item_text = f"Item name = {name}" \
                f"\nQuantity = {quantity}"
    photo = InputFile(path_or_bytesio=photo_path)
    await bot.edit_message_media(media=InputMediaPhoto(media=photo,
                                                       caption=item_text),
                                 chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 reply_markup=get_item_inline_keyboard(id=current_item_id))


@dp.callback_query_handler(navigation_data_callback.filter(for_data='basket'))
async def add_to_basket(call: types.CallbackQuery):
    print(call.data)
    user_id = call.from_user.id
    item_id = int(call.data.split(':')[-1])
    db.add_to_basket(user_id, item_id)
    await bot.answer_callback_query(callback_query_id=call.id, text="Added to your basket",
                                    show_alert=False)


@dp.message_handler(text=['My_basket', 'my_basket'])
@dp.message_handler(commands=['My_basket', 'my_basket'])
async def show_basket(message: types.Message):
    user_id = message.from_user.id
    basket_items = db.show_basket(user_id)
    for i in basket_items:
        await message.answer(text=f'{i} = {basket_items.get(i)}', reply_markup=basket_keyboard)


@dp.message_handler(text=['Clear_basket', 'clear_basket'])
@dp.message_handler(commands=['Clear_basket', 'clear_basket'])
async def show_basket(message: types.Message):
    user_id = message.from_user.id
    db.clear_basket(user_id)
    await message.answer(text=f'Your basket is cleared!', reply_markup=basket_keyboard)


@dp.message_handler(commands='new_table_items')
async def create_table_items(message: types.Message):
    db.create_table_items()
    await message.answer(text=f'Table "Items" created', reply_markup=commands_items_keyboard)


@dp.message_handler(commands='add_item')
async def add_item(message: types.Message):
    await message.answer(text=f'Assign id:')
    await add.state1.set()


@dp.message_handler(state=add.state1)
async def id_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
    await add.next()
    await message.reply('Enter item name:')
    await add.state2.set()


@dp.message_handler(state=add.state2)
async def item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state2'] = message.text
    await add.next()
    await message.reply('Enter item quantity:')
    await add.state3.set()


@dp.message_handler(state=add.state3)
async def item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state3'] = message.text
        print(data['state3'])
    await add.next()
    await message.reply('Enter photo directory:')
    await add.state4.set()


@dp.message_handler(state=add.state4)
async def item_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state4'] = message.text
        print(data['state4'])
        await bot.send_message(
            message.from_user.id,
            md.text(
                md.text(f'Created'),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN)
        db.add_item(id=int(data['state1']), name=str(data['state2']), quantity=int(data['state3']),
                    photo_path=str(data['state4']))
    await state.finish()


@dp.message_handler(commands='update_item')
async def update_item(message: types.Message):
    await message.answer(text=f'Select item id:')
    await update.state1.set()


@dp.message_handler(state=update.state1)
async def id_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
    await update.next()
    await message.reply('Enter new quantity:')
    await update.state2.set()


@dp.message_handler(state=update.state2)
async def new_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state2'] = message.text
        db.update_item_number(int(data['state1']), str(data['state2']))
        await message.answer(text=f"Item with id {data['state1']} now has new quantity {data['state2']}")
    await state.finish()


@dp.message_handler(commands='show_item')
async def show_item(message: types.Message):
    await message.answer(text=f'Select id:')
    await show.state1.set()


@dp.message_handler(state=show.state1)
async def id_find(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
        await message.answer(text=f"{db.select_item_info(id=int(data['state1']))}")
    await state.finish()


@dp.message_handler(commands='delete_item')
async def delete_item(message: types.Message):
    await message.answer(text=f'Select id:')
    await del_user.state1.set()


@dp.message_handler(state=del_user.state1)
async def id_find_del(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['state1'] = message.text
        db.delete_item(id=int(data['state1']))
        await message.answer(text=f"Item with id {data['state1']} deleted.")
    await state.finish()


@dp.message_handler(commands='show_items')
async def show_items(message: types.Message):
    await message.answer(text='id, name, quantity')
    for item in db.select_all_items():
        await message.answer(text=item)


@dp.message_handler(commands='del_all_items')
async def del_all_items(message: types.Message):
    db.delete_all_items()
    await message.answer(text='All items are deleted')


@dp.message_handler(commands='del_tab_items')
async def del_tab_items(message: types.Message):
    db.drop_all_items()
    await message.answer(text='Table "Items" deleted')
