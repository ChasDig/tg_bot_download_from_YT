# StatesGroup - группа состояний
from aiogram.dispatcher.filters.state import State, StatesGroup


# ----- State Machine: Admin send mailing ----- #

class AdminReportStateMachine(StatesGroup):
    """
        Рассылка для зарегестрированных пользователей:
    """
    text_advertising = State()
    photo_advertising = State()
