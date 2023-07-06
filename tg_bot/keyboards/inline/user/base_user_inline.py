# InlineKeyboardMarkup - inline клавиатура
# InlineKeyboardButton - inline кнопка
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ----- Inline Keyboard User ----- #

# User order:
# Заказы пользователей:

# kb_user_register_order = InlineKeyboardMarkup(
#
#     inline_keyboard=[
#         [
#             # callback_data - callback(ответ/перенаправление) на ответ пользователя:
#             InlineKeyboardButton(text="Заполнить форму", callback_data=fill_form_order),
#             InlineKeyboardButton(text="Связаться с разработчиком", callback_data=""),
#         ],
#         [
#             InlineKeyboardButton(text="Отмена", callback_data="cancel"),
#         ]
#     ]
# )
