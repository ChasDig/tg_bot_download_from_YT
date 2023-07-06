import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tg_bot.config import load_config

from tg_bot.middlewares import ThrottlingMiddleware
from tg_bot.filters import AdminFilter, IsPrivate
from tg_bot.handlers import register_admin_base, register_user_base

dp = None

# ----- Логирование для файла bot.py ----- #
logger = logging.getLogger(__name__)


# ----- Регестрируем Middlewares ----- #
def register_all_middlewares(dp):
    # Регестрируем middlewares:
    # - Throttling:
    dp.middleware.setup(ThrottlingMiddleware())


# ----- Регестрируем Filters ----- #
def register_all_filters(dp):
    # Регестрируем filters admin(забайндить):
    dp.filters_factory.bind(AdminFilter)
    # Регестрируем filters users_private(забайндить):
    dp.filters_factory.bind(IsPrivate)


# ----- Регестрируем Handlers ----- #
def register_all_handlers(dp):
    # Регестрируем handlers (отличается от других):
    # Admin:
    register_admin_base(dp=dp)
    # Users:
    register_user_base(dp=dp)


# ----- Асинхронная функция - запускаем бота (main) -----#
async def main():
    # Прописываем логгирование для функции main (уровень логирования и формат вывода данных):
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    # Загружаем конфиги:
    config = load_config('.env')
    # Создаем экземпляр Бота:
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    # Прописываем машину состояний (Storage):
    ## MemoryStorage - если хотим использовать ОЗУ в качестве памяти:
    ## RedisStorage2 - мини БД:
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    # Создаем экземпляр Диспатчера(Диспетчера):
    global dp
    dp = Dispatcher(bot=bot, storage=storage)
    # Создаем у бота доп. переменную config:
    bot["config"] = config
    # Вызываем middlewares:
    # Передаю dp для регистрации:
    register_all_middlewares(dp=dp)
    # Вызываем filters:
    # Передаю dp для регистрации:
    register_all_filters(dp=dp)
    # Вызываем handlers:
    # Передаю dp для регистрации:
    register_all_handlers(dp=dp)
    # Запуск созданного бота:
    try:
        await dp.start_polling()
    finally:
        # В случаем ошибки (или иного события), закрываем storage(соединение):
        await dp.storage.close()
        # Ожидаем закрытия соединения:
        await dp.storage.wait_closed()
        # Закрываем сессию бота:
        await bot.session.close()


# ----- Запускаем асинхронную функцию main ----- #
if __name__ == '__main__':
    try:
        # Запускаем бота (через main):
        print("Bot launched!")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Прописываем действия, означающие остановку бота:
        logger.error("Bot stopped!")
