from enum import Enum

import uvicorn
from fastapi import FastAPI, Path, Request
from fastapi.params import Query

from app.common.config import Settings

app = FastAPI()
settings = Settings()


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@app.get("/")
def root():
    return {"message": "I'm alive!",
            "service": settings.service_name,
            "database": settings.db.url}


@app.get("/{user_id}")
def user(user_id: int = Path(ge=5)):
    return {"user_id": user_id}


@app.get("/users/")
def get_users(
        limit: int = 10,
        offset: int = Query(0, ge=0),
        tags: list[str] = Query([]),
        order: SortOrder = SortOrder.asc):
    return {"limit": limit, "offset": offset, "tags": tags, "order": order}


# @app.post("/users")
# def create_user(body: dict = Body()):
#     return body

@app.post("/users")
async def create_user(request: Request):
    data = await request.json()
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
