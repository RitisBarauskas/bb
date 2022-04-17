from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderTrim(StatesGroup):
    """
    Список состояний для записи на стрижку
    """
    waiting_for_master = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_service = State()