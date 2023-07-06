# ------ Middleware: Throttling decorators for middleware ----- #

def rate_limit(limit: int, key=None):

    """
    Decorator for configuring rate limit and key in different functions.
    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        """
         Создаем атрибут throttling_rate_limit к функции func и задает ей лимит (limit).
            При создании ключа (key), создает и его. После чего возвращает декоратор(decorator),
            который будет использоваться в дальнейшем.
        :param func:
        :return:
        """

        setattr(func, 'throttling_rate_limit', limit)

        if key:

            setattr(func, 'throttling_key', key)

        return func

    return decorator
