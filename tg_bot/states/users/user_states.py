# StatesGroup - группа состояний
from aiogram.dispatcher.filters.state import State, StatesGroup


# ----- State Machine: User State ----- #

class UserDownloadVideo(StatesGroup):
    """Send video or audio."""
    user_download_video_audio_1 = State()
    user_download_video_audio_2 = State()

