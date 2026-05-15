from pydantic import BaseModel, Field


class RandQuery(BaseModel):
    rnd_from: int = Field(0, ge=0, le=100)
    rnd_to: int = Field(0, ge=0, le=100)
