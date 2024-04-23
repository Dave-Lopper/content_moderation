from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.content_moderator import ContentModerator

moderation_router = APIRouter(prefix="/moderation")
Mod = ContentModerator()


class ModerationQuery(BaseModel):
    text: str


@moderation_router.post("")
@moderation_router.post("/")
async def moderation(query: ModerationQuery):
    try:
        return Mod.infer(query.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while running inference: {e}\nPlease contact your system administrator",  # noqa: E501
        )


@moderation_router.get("/labels")
@moderation_router.get("/labels/")
async def labels():
    return ContentModerator.LABELS_ACRONYMS_MAPPING
