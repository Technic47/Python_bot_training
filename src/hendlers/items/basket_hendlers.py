from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards import *
from loader import dp, db, bot
from states import BuyerState


@dp.message_handler(text='My_basket')
@dp.message_handler(commands='My_basket')
async def show_basket(message: Message, get_user_basket):
    user_basket = get_user_basket[1]
    if user_basket != '':
        user_basket = [item_data.split(':') for item_data in user_basket.split()]
        text = 'Basket: '
        for item_id, item_count in user_basket:
            _, name, _, _ = db.select_info('Items', id=item_id)[0]
            text += f'\n{name}: {item_count}'
        await message.answer(text=text,
                             reply_markup=basket_keyboard)
    else:
        text = 'Your basket is EMPTY.'
        await message.answer(text=text)


@dp.callback_query_handler(item_count_callback.filter(target='to_basket'))
async def add_item_basket(call: CallbackQuery):
    current_count = int(call.data.split(':')[-1])
    current_item_id = call.data.split(':')[-2]
    user_id, user_basket = db.select_user_basket(user_id=call.from_user.id)
    user_basket = [item_data.split(':') for item_data in user_basket.split()]
    for i in range(len(user_basket)):
        item_id, item_count = user_basket[i]
        if current_item_id == item_id:
            user_basket[i][1] = str(int(item_count) + current_count)
            break
    else:
        user_basket += [[current_item_id, str(current_count)]]
    user_basket = ' '.join([':'.join(dbl) for dbl in user_basket])
    db.update_user_basket(user_id=user_id, basket=user_basket)
    await bot.answer_callback_query(callback_query_id=call.id,
                                    text="Item added.",
                                    show_alert=False)


@dp.callback_query_handler(basket_callback.filter(action='del_basket'))
async def del_basket(call: CallbackQuery):
    db.clear_basket(user_id=call.from_user.id)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.answer_callback_query(callback_query_id=call.id,
                                    text='Basket cleared!',
                                    show_alert=True)


@dp.callback_query_handler(basket_callback.filter(action='buy'))
async def start_buy(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(text='Write delivery date.')
    await BuyerState.wait_date.set()


@dp.message_handler(state=BuyerState.wait_date)
async def get_date(message: Message, state: FSMContext):
    await state.update_data({'date': message.text})
    await message.answer(text='Write delivery time.')
    await BuyerState.wait_time.set()


@dp.message_handler(state=BuyerState.wait_time)
async def get_time(message: Message, state: FSMContext):
    await state.update_data({'time': message.text})
    await message.answer(text='Write your full name.')
    await BuyerState.wait_name.set()


@dp.message_handler(state=BuyerState.wait_name)
async def get_name(message: Message, state: FSMContext, get_user_basket):
    raw_data = get_user_basket
    user_basket = raw_data[1]
    user_basket = [item_data.split(':') for item_data in user_basket.split()]
    data = await state.get_data()
    text = f'Order\n' \
           f'Your name: {message.text}\n' \
           f'Date: {data["date"]}\n' \
           f'Time: {data["time"]}\n' \
           f'\nItems:'
    for item_id, item_count in user_basket:
        _, name, _, _ = db.select_info('Items', id=item_id)[0]
        text += f'\n{name}: {item_count}'

    for item_id in user_basket:
        current_count = db.select_info('Items', id=item_id[0])[0][2]
        new_count = current_count - int(item_id[1])
        db.update_item_number(id=item_id[0], quantity=new_count)

    db.update_user_basket(user_id=message.from_user.id, basket='')
    await message.answer(text=text)
    await state.reset_state()
