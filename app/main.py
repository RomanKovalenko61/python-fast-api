import uvicorn
from fastapi import FastAPI

from app.service import routes

app = FastAPI(
    title="Proga API",
    description="API for ....",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "Projects ...",
            "description": "Descrpt ..."
        }
    ]
)
app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
