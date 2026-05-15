from typing import Annotated

from fastapi import Depends


def get_project_service():
    return ProjectService()


class ProjectService():
    def get_project(self, project_id: int):
        return project_id


ProjectServiceDeps = Annotated[
    ProjectService,
    Depends(get_project_service),
]
