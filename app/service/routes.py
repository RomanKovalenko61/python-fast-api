import logging
import random
from enum import Enum
from venv import logger

from fastapi import APIRouter, Depends
from fastapi.params import Query

from app.common.config import Settings
from app.common.db import check_db, DBSessionDebs
from app.service.dependencies import ProjectServiceDeps
from app.service.schema import RandQuery, UserCreateRequest, UserCreateResponse, ProjectPath

settings = Settings()
router = APIRouter()

logger = logging.getLogger(__name__)


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/")
async def root(session: DBSessionDebs):
    data = await check_db(session)
    logger.info("DB check: %s", data)
    return {"message": "I'm alive!",
            "service": settings.service_name,
            "database": settings.db.url}


# @router.get("/{user_id}")
# def user(user_id: int = Path(ge=5)):
#     return {"user_id": user_id}


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

# @router.post("/users")
# async def create_user(request: Request):
#     data = await request.json()
#     return data

@router.post("/users", response_model=UserCreateResponse)
async def create_user(data: UserCreateRequest):
    # do smth
    # return {**data.model_dump(), "id": 1}
    return UserCreateResponse(
        id=1,
        name=data.name,
    )


@router.get("/random")
def get_random(query: RandQuery = Depends()):
    return {
        "value": random.randint(query.rnd_from, query.rnd_to)
    }


@router.get("/projects/{project_id}", description="""
    Получает проект по его id, если проекта нет возвращает ошибку
            """)
def get_project(service: ProjectServiceDeps, path: ProjectPath = Depends()):
    res = service.get_project(path.project_id)
    return {"id": res}
