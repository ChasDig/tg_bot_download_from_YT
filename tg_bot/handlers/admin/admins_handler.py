"""
        Admin handler
"""
from asyncio import sleep
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
# Import Filters:
from tg_bot.filters import IsPrivate
# Import Machine State:
from tg_bot.states import AdminReportStateMachine

from tg_bot.create_advertising import AD_TEXT_PATH, PICTURE_PATH


# ----- Handler: Admin ----- #
async def admin_start(message: types.Message):
    """
    Обработчик: обрабатывает ввод пользователем команды start и 'проверяет его на админство'
    :param message: user message 'start'
    :return: reply text message to admin
    """
    await message.reply(
        text='Привет, admin!\n'
             'Для начала работы введи нужную команду:'
    )


async def start_create_new_advertising(message: types.Message):
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text=f"Отправь рекламный текст:"
    )
    await AdminReportStateMachine.text_advertising.set()


async def send_advertising_text(message: types.Message):
    text_advertising = message.text
    text_advertising += f"\n- - - - - - - - - -\n" \
                        f"Тут 👆 может быть и твоя реклама 👉 @freedom_cats"
    with open(AD_TEXT_PATH, "w") as file:
        file.write(text_advertising)
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text="Текст успешно сохранен.\n"
             "Отправь изображение для рекламы:",
    )
    await AdminReportStateMachine.photo_advertising.set()


async def send_advertising_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file=PICTURE_PATH)
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text="Картинка успешно сохранена.",
    )
    await state.reset_state(with_data=False)


# ----- Hendlers: Register Admin (Регестрируем обработчики) ----- #
def register_admin_base(dp: Dispatcher):
    """
    Регестрируем handlers для администратора
    :param dp: Dispatcher
    :return: register admin handlers
    """

    # Регестрируем handlers:

    # is_admin - проверка входа администратора: при входе администраторов - True:
    # /start:
    dp.register_message_handler(
        admin_start,
        IsPrivate,
        commands=['start'],
        is_admin=True
    )
    #  /new_ad:
    dp.register_message_handler(
        start_create_new_advertising,
        IsPrivate,
        commands=['new_ad'],
        is_admin=True
    )
    dp.register_message_handler(
        send_advertising_text,
        IsPrivate,
        state=AdminReportStateMachine.text_advertising,
        is_admin=True
    )
    dp.register_message_handler(
        send_advertising_photo,
        IsPrivate,
        content_types=["photo"],
        state=AdminReportStateMachine.photo_advertising,
        is_admin=True
    )
