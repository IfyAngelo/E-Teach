from fastapi import APIRouter, Depends

from core.fastapi.dependencies.authentication import AdminRequired

from .knowledge import et_knowledge
from .lesson_note import et_lesson_note
from .lesson_plan import et_lesson_plan

et_router = APIRouter()

et_router.include_router(
    et_knowledge, tags=["ETKRouter"], dependencies=[Depends(AdminRequired)], prefix="/knowledge"
)
et_router.include_router(
    et_lesson_note, tags=["ETLNRouter"], dependencies=[Depends(AdminRequired)], prefix="/lesso-note"
)
et_router.include_router(
    et_lesson_plan, tags=["ETLPRouter"], dependencies=[Depends(AdminRequired)], prefix="/lesson-plan"
)
__all__ = ["et_router"]
