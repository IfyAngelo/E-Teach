from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    title: str = Field(..., description="Task name", example="Task 1")
    description: str = Field(
        ..., description="Task description", example="Task 1 description"
    )
    completed: bool = Field(alias="is_completed", description="Task completed status")

    class Config:
        orm_mode = True