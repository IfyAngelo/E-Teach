from contextvars import ContextVar, Token
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from core.config import config

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


async def get_session():
    """
    Get the database session as an async context manager.

    :return: The database session as an async context manager.
    """
    client: AsyncIOMotorClient = AsyncIOMotorClient(config.MONGO_URI)
    session = await client.start_session()
    return session  # Yield the session within the context