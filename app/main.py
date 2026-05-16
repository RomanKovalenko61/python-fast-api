import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.service import routes
from app.consumers.order_handler import start_order_consumer, stop_order_consumer
from app.kafka.producer import get_kafka_producer, _producer_client
from app.routers import orders
from app.common.config import Settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle: startup and shutdown"""

    # Startup: запускаем Kafka Producer
    await get_kafka_producer()

    # Startup: запускаем Kafka Consumers
    await start_order_consumer()

    yield

    # Shutdown: останавливаем Producer и Consumers
    if _producer_client:
        await _producer_client.stop()

    await stop_order_consumer()

def create_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - [%(levelname)s] %(name)s - %(message)s]"
    )
    settings = Settings()
    new_app = FastAPI(
        lifespan=lifespan,
        title=settings.app.name,
        description="API for ....",
        version="0.0.1",
        openapi_tags=[
            {
                "name": "Projects ...",
                "description": "Descrpt ..."
            }
        ])

    new_app.state.settings = settings
    new_app.include_router(routes.router)
    new_app.include_router(orders.router)
    return new_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
