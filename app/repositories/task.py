from app.models import Task
from core.repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Task repository provides all the database operations for the Task model.
    """

    async def get_all_by_author_id(self, author_id: int) -> list[Task]:
        """
        Get all tasks by author id.

        :param author_id: The author id to match.
        :return: A list of tasks.
        """
        return await self.get_by(field="task_author_id", value=author_id, unique=False)