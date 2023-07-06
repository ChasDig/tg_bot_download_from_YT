# CallbackData - данные, которые мы получаем от пользователя при использовании inline keyboard
from aiogram.utils.callback_data import CallbackData

# ----- CallBack - User CallBackData ----- #

# CallBack пользователя на использование InlineKeyboard 'Заполнить форму':
# prefix - на какой callback_data дается ответ (тригериться):
# Далее идут переменные, которые мы будем сохранять и передавать (parts):

# fill_form_order = CallbackData(prefix="fill_form_order", "username", )
