"""Admin filter."""
from aiogram.dispatcher.filters import BoundFilter
from tg_bot.config import Config


# ----- Admin Filter: фильтрация для администратора ----- #
class AdminFilter(BoundFilter):
    """Check the user for admin rights."""
    key = "is_admin"    # Create admin key

    def __init__(self, is_admin=None):
        self.is_admin = is_admin

    async def check(self, obj):
        """Checking if a user has administrator rights.
        :param obj: may be messaged or CallBackQuery. Object after processing Update.
        :return: True, if the user is admin, else False.
        """
        # Filtering administrator access to certain actions (commands).
        if self.is_admin is None:
            return True
        if not self.is_admin:
            return False

        config: Config = obj.bot.get('config')  # Get list with administrators id.

        user_id = obj.from_user.id  # Get user id.

        return user_id in config.tg_bot.admin_ids
