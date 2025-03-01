from enum import Enum
from functools import wraps

from .session import get_session


class Propagation(Enum):
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


class Transactional:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            session = await get_session()  # Leverage existing session function
            try:
                async with session.start_transaction():
                    result = await function(*args, **kwargs)
                    return result
            except Exception as exception:
                # await session.abort_transaction()
                raise exception

        return decorator