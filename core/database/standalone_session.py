from uuid import uuid4

from .session import reset_session_context, get_session, set_session_context


async def standalone_session(func):
    async def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            async with await get_session() as session:  # Use session from get_session
                await func(*args, **kwargs)
        except Exception as exception:
            await session.abort_transaction()  # Assuming get_session manages transactions
            raise exception
        finally:
            reset_session_context(context=context)

    return _standalone_session
