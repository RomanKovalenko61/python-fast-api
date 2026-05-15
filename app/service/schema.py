from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator, field_validator


class RandQuery(BaseModel):
    rnd_from: int = Field(0, ge=0, le=100)
    rnd_to: int = Field(100, ge=0, le=100)

    @model_validator(mode="after")
    def check_from_to(self):
        if self.rnd_from > self.rnd_to:
            raise HTTPException(400, "rnd_from > rnd_to")
        return self

    # @model_validator(mode="before")
    # def check_from_to2(cls, data):
    #     ...
    #
    # @model_validator(mode="wrap")
    # def check_from_to3(cls, data, handler):
    #     ...


class UserCreateRequest(BaseModel):
    name: str
    age: int
    description: str | None = None

    # by_default "extra": "ignore"
    # "extra": "forbid"
    # "extra": "allow"
    model_config = {
        "extra": "ignore"
    }

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value):
        if not value.strip():
            raise HTTPException(400, "name must be non-empty string")
        return value


class UserCreateResponse(BaseModel):
    id: int
    name: str


class ProjectPath(BaseModel):
    project_id: int = Field(gt=0)
