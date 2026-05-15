from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.kafka.producer import KafkaProducerClient, get_kafka_producer
from app.common.config import get_settings

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderCreate(BaseModel):
    """Схема создания заказа"""
    user_id: int
    items: list[str] = Field(..., min_items=1)
    total_amount: float = Field(..., gt=0)


class OrderResponse(BaseModel):
    """Ответ API"""
    order_id: int
    status: str = "pending"
    message: str = "Order is being processed"


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_order(
        order: OrderCreate,
        producer: KafkaProducerClient = Depends(get_kafka_producer),
):
    """
    Создаёт заказ и отправляет событие в Kafka.

    Возвращает 202 Accepted — обработка асинхронная.
    """

    # Генерируем ID (в реальности — из БД)
    order_id = 12345  # Заглушка

    # Отправляем событие в Kafka
    await producer.send(
        topic=get_settings().orders_topic,
        value={
            "event_type": "order.created",
            "order_id": order_id,
            "user_id": order.user_id,
            "items": order.items,
            "total_amount": order.total_amount,
        },
        key=str(order.user_id),  # Партиция по user_id
    )

    return OrderResponse(order_id=order_id)