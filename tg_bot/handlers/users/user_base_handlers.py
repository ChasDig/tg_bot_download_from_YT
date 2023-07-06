import os
from environs import Env
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher
# Import Users Keyboards:
# from tg_bot.keyboards.reply.user import kb_user_menu
from tg_bot.misc import rate_limit
# Import Filters:
from tg_bot.filters import IsPrivate
# IMport State Machine:
from aiogram.dispatcher import FSMContext
from tg_bot.states import UserDownloadVideo
# Import func for download from YT:
from tg_bot.download_from_yt import get_videos_resolution, download_user_file
#
from tg_bot.create_advertising import create_files_for_advertising

env = Env()
env.read_env(path='.env')


# ----- Handlers: Users Start ----- #
@rate_limit(limit=15)
async def user_start_and_menu(message: types.Message):
    """ Send start message to User.
    :param message: message from User.
    :return: None
    """
    text_hello = f"Приветствую тебя, {message.from_user.username} 🫡\n" \
                 f"С помощью этого бота ты сможешь скачивать аудио и видео прямиком с YouTube 😉\n" \
                 f"Для этого, просто отправь боту ссылку и выбери интересующий Тебя формат:\n" \
                 f"- - - - -\n" \
                 f"P.S: На данный момент, бот находится на тестовом сервере. В связи с чем, скорость загрузки " \
                 f"файлов может быть снижена. В скором времени мы переведем его уже на боевое дежурство 🫠"
    await message.answer(
        text=text_hello,
    )
    await UserDownloadVideo.user_download_video_audio_1.set()


@rate_limit(limit=5)
async def send_user_video_quality_options(message: types.Message, state: FSMContext):
    """Get info about video or audio, send info user and save info in state.
    :param message:  message(url) from User.
    :param state: State Machine.
    :return: None.
    """
    videos_url = str(message.text).strip()
    await message.delete()
    try:
        video_info = get_videos_resolution(videos_url)
        text_answer = f"Готово 👌\n" \
                      f"<b>Имя скачиваемого файла:</b> «{str(video_info[0])}»\n" \
                      f"<b>Название канала:</b> {str(video_info[2])}\n" \
                      f"<b>Количество просмотров видео:</b> {str(video_info[3])}\n" \
                      f"<b>Количество лайков:</b> {str(video_info[4])}\n"\
                      f"<b>Ссылка на скачиваемый файл:</b> {videos_url}"
        #  Create Markup with video resolutions:
        markup = types.InlineKeyboardMarkup()
        count_videos_resolutions = len(video_info[1])
        for video_resolve in range(0, count_videos_resolutions - 1, 3):
            buffer_button = (count_videos_resolutions - 1) - video_resolve
            if buffer_button < 2:
                if buffer_button == 1:
                    markup.row(
                        types.InlineKeyboardButton(
                            video_info[1][video_resolve],
                            callback_data=str(video_info[1][video_resolve]),
                        ),
                        types.InlineKeyboardButton(
                            video_info[1][video_resolve + 1],
                            callback_data=str(video_info[1][video_resolve + 1]),
                        ),
                    )
                elif buffer_button == 0:
                    markup.row(
                        types.InlineKeyboardButton(
                            video_info[1][video_resolve],
                            callback_data=str(video_info[1][video_resolve]),
                        ),
                    )
                break
            else:
                markup.row(
                    types.InlineKeyboardButton(
                        video_info[1][video_resolve],
                        callback_data=str(video_info[1][video_resolve]),
                    ),
                    types.InlineKeyboardButton(
                        video_info[1][video_resolve + 1],
                        callback_data=(video_info[1][video_resolve + 1]),
                    ),
                    types.InlineKeyboardButton(
                        video_info[1][video_resolve + 2],
                        callback_data=str(video_info[1][video_resolve + 2]),
                    ),
                )
        markup.row(
            types.InlineKeyboardButton(
                "Audio",
                callback_data="audio",
            ),
        )
        await message.answer(
            text=text_answer,
            reply_markup=markup,
        )
        async with state.proxy() as data:
            data["videos_url"] = videos_url
            data["username"] = message.from_user.username
        await UserDownloadVideo.user_download_video_audio_2.set()
    except Exception as ex:
        print(f"Error: {ex}")
        text_error = f"Ошибка 🫣 при получении информации по ссылке: {videos_url} \n" \
                   f"Прошу проверить правильность введеной ссылки и отправить корректный ее вариант через 5 секунд 🧐"
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=text_error,
        )
        await UserDownloadVideo.user_download_video_audio_1.set()


@rate_limit(limit=5)
async def download_file_user(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data_file_url = data.get("videos_url")
    file_resolution = callback.data
    await callback.message.delete()
    advertising_data = create_files_for_advertising()
    message_button = [
        [
            InlineKeyboardButton("Подробнее", url="https://t.me/freedom_cats")
        ]
    ]
    markup = InlineKeyboardMarkup(message_button)
    async with Client("my_account", env.str("API_ID"), env.str("API_HASH")) as app:
        await app.send_photo(
            str(data.get("username")),
            advertising_data[1],
            caption=advertising_data[0],
            reply_markup=markup,
        )
        file_data = download_user_file(str(data_file_url), file_resolution)
        await app.send_video(
            str(data.get("username")),
            f"{os.getcwd()}/tg_bot/user_files/{file_data[0]}.{file_data[1]}",
        )
        os.remove(f"{os.getcwd()}/tg_bot/user_files/{file_data[0]}.{file_data[1]}")
    await UserDownloadVideo.user_download_video_audio_1.set()


# ----- Handlers: Register User Base (Регестрируем обработчики) ----- #
def register_user_base(dp: Dispatcher):
    """
    Регестрируем handlers от пользователя
    :param dp: Dispatcher
    :return: register user handlers
    """
    # Регестрируем handlers:
    # is_admin - проверка входа администратора: при входе обычного пользователя - False:
    # /start:
    dp.register_message_handler(
        user_start_and_menu,
        IsPrivate,
        commands=["start"],
    )
    #  Отправляем пользователю информацию о видео:
    dp.register_message_handler(
        send_user_video_quality_options,
        IsPrivate,
        state=UserDownloadVideo.user_download_video_audio_1,
    )
    dp.register_callback_query_handler(
        download_file_user,
        lambda callback_query: True,
        state=UserDownloadVideo.user_download_video_audio_2,
    )
