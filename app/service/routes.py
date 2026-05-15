from enum import Enum

from fastapi import Path, Request, APIRouter
from fastapi.params import Query

from app.common.config import Settings

settings = Settings()
router = APIRouter()


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/")
def root():
    return {"message": "I'm alive!",
            "service": settings.service_name,
            "database": settings.db.url}


@router.get("/{user_id}")
def user(user_id: int = Path(ge=5)):
    return {"user_id": user_id}


@router.get("/users/")
def get_users(
        limit: int = 10,
        offset: int = Query(0, ge=0),
        tags: list[str] = Query([]),
        order: SortOrder = SortOrder.asc):
    return {"limit": limit, "offset": offset, "tags": tags, "order": order}


# @app.post("/users")
# def create_user(body: dict = Body()):
#     return body

@router.post("/users")
async def create_user(request: Request):
    data = await request.json()
    return data
