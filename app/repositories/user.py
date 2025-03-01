from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_username(self, username: str) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :return: User or None.
        """
        return await self.get_by(field="username", value=username, unique=True)

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :return: User or None.
        """
        return await self.get_by(field="email", value=email, unique=True)