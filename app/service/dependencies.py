from typing import Annotated

from fastapi import Depends

from app.service.db import DbSessionDeps


def get_project_repository(db: DbSessionDeps):
    print("get_project_repository")
    return ProjectRepository()


class ProjectRepository():
    def get_by_id(self, project_id: int):
        return project_id


ProjectRepositoryDeps = Annotated[
    ProjectRepository,
    Depends(get_project_repository),
]


def get_project_service(repo: ProjectRepositoryDeps):
    print("get_project_service")
    return ProjectService(repo)


class ProjectService():
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def get_project(self, project_id: int):
        return self.repo.get_by_id(project_id)


ProjectServiceDeps = Annotated[
    ProjectService,
    Depends(get_project_service),
]

# route
# -> service
#   -> repository
