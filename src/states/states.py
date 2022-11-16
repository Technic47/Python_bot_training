from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyerState(StatesGroup):
    wait_date = State()
    wait_time = State()
    wait_name = State()


class AddItem(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()


add = AddItem()


class UpdateItem(StatesGroup):
    state1 = State()
    state2 = State()


update = UpdateItem()


class ShowItem(StatesGroup):
    state1 = State()


show = ShowItem()


class DelItem(StatesGroup):
    state1 = State()


del_user = DelItem()
