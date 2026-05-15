import logging
from typing import Optional

from app.common.config import get_settings
from app.kafka.consumer import KafkaConsumerClient

logger = logging.getLogger(__name__)

# Глобальная переменная для consumer
_order_consumer: Optional[KafkaConsumerClient] = None


async def handle_order_created(event: dict):
    """
    Обработчик события order.created.

    Здесь выполняются все side-effects:
    - Отправка email
    - Обновление склада
    - Начисление бонусов
    """
    order_id = event["order_id"]
    user_id = event["user_id"]

    logger.info(f"Processing order {order_id} for user {user_id}")

    try:
        # Эмуляция работы
        await send_order_email(user_id, order_id)
        await update_inventory(event["items"])
        await calculate_bonuses(user_id, event["total_amount"])

        logger.info(f"Order {order_id} processed successfully")

    except Exception as e:
        logger.error(f"Failed to process order {order_id}: {e}")
        raise  # Retry через Kafka


async def send_order_email(user_id: int, order_id: int):
    """Заглушка отправки email"""
    logger.info(f"Email sent to user {user_id} for order {order_id}")


async def update_inventory(items: list[str]):
    """Заглушка обновления склада"""
    logger.info(f"Inventory updated for items: {items}")


async def calculate_bonuses(user_id: int, amount: float):
    """Заглушка начисления бонусов"""
    bonuses = amount * 0.05
    logger.info(f"Bonuses {bonuses} calculated for user {user_id}")


async def start_order_consumer():
    """Запускает consumer для обработки заказов"""
    global _order_consumer

    _order_consumer = KafkaConsumerClient(
        topic=get_settings().orders_topic,
        handler=handle_order_created,
    )

    await _order_consumer.start()


async def stop_order_consumer():
    """Останавливает consumer"""
    if _order_consumer:
        await _order_consumer.stop()
