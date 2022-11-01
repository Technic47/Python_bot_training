from aiogram.dispatcher.filters.state import StatesGroup, State


class AddItem(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()


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
