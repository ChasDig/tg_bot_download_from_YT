"""
    Передача переменных окружений и настроек для бота.
"""
from dataclasses import dataclass
from typing import List
from environs import Env
from pathlib import Path

# Base_Dir:
BASE_DIR = Path(__file__).resolve().parent.parent


# ----- Класс бля Бота ----- #A
@dataclass
class TgBot:
    # Токен:
    token: str
    # Id-админов
    admin_ids: List[int]
    # Используем или нет use_redis (по умолчанию-False):
    use_redis: bool


# ----- Класс для 'всего остального' ----- #
@dataclass
class Miscellaneous:
    # Параметры, которые могут нам пригодиться:
    other_params: str = None


# ----- Общий (главный) класс для cinfig: ----- #
@dataclass
class Config:
    # Информация о нашем боте:
    tg_bot: TgBot
    # Прочее:
    misc: Miscellaneous


# ----- Функция: выгружает config ----- #
def load_config(path: str = None):

    # Подгружаем переменное окружение:
    env = Env()
    env.read_env(path=path)

    # Возвращаем конфиги:
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ID_ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        misc=Miscellaneous(),
    )
