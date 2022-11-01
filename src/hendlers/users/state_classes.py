from aiogram.dispatcher.filters.state import StatesGroup, State


class AddUser(StatesGroup):
    state1 = State()
    state2 = State()


add = AddUser()


class UpdateUser(StatesGroup):
    state1 = State()
    state2 = State()


update = UpdateUser()


class ShowUser(StatesGroup):
    state1 = State()


show = ShowUser()


class DelUser(StatesGroup):
    state1 = State()


del_user = DelUser()
