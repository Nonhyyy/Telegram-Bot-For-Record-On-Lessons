from aiogram.fsm.state import StatesGroup, State


class AddLesson(StatesGroup):
    waiting_for_name = State()