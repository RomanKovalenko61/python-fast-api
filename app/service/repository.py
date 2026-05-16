import logging
from typing import Annotated

from fastapi import Depends


from app.model import Project
from app.common.db import DBSessionDebs

logger = logging.getLogger(__name__)


class ProjectRepository():
    def __init__(self, session: DBSessionDebs):
        self.session = session

    def get_by_id(self, project_id: int):
        return project_id

    async def create(self):
        project = Project(
            key="ps",
            name="PurpleSchool",
            description="Обучающая платформа"
        )
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        logger.info(project)


def get_project_repository(session: DBSessionDebs):
    return ProjectRepository(session)


ProjectRepositoryDeps = Annotated[
    ProjectRepository,
    Depends(get_project_repository)
]