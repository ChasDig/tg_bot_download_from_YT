# BoundFilter - Base Filter from aiogram:
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


# ----- Filters: Private chat ----- #

class IsPrivate(BoundFilter):
    """Chat privacy check."""
    key = "is_private"  # Checking chat for privacy using a key.

    def __init__(self, is_private=False):
        self.is_private = is_private

    async def check(self, call: types.CallbackQuery):
        """Check on privacy.
        :param call: CallbackQuery.
        :return: True, if chat privacy, or False if not.
        """
        if not self.is_private:
            return False
        else:
            return call.message.chat.type == types.ChatType.PRIVATE  # Checking: if our chat is private - handler using.
