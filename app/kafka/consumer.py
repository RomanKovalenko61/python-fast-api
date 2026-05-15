import asyncio
import json
import logging
from typing import Callable, Awaitable, Optional

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app.common.config import get_settings

logger = logging.getLogger(__name__)


class KafkaConsumerClient:
    """
    Kafka Consumer для чтения событий.

    Использование:
        consumer = KafkaConsumerClient('orders', handler_func)
        await consumer.start()
    """

    def __init__(
            self,
            topic: str,
            handler: Callable[[dict], Awaitable[None]],
            group_id: Optional[str] = None,
    ):
        self.topic = topic
        self.handler = handler
        self.group_id = group_id or get_settings().kafka_consumer_group
        self.consumer: Optional[AIOKafkaConsumer] = None
        self._running = False

    async def start(self):
        """Создаёт consumer и начинает обработку"""
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=get_settings().kafka_bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset=get_settings().kafka_auto_offset_reset,
            enable_auto_commit=False,  # Ручной commit для надёжности
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )

        await self.consumer.start()
        logger.info(f"Consumer started for topic: {self.topic}")

        self._running = True
        asyncio.create_task(self._consume_loop())

    async def stop(self):
        """Останавливает consumer"""
        self._running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info(f"Consumer stopped for topic: {self.topic}")

    async def _consume_loop(self):
        """Основной цикл чтения событий"""
        try:
            async for message in self.consumer:
                try:
                    # Обрабатываем событие
                    await self.handler(message.value)

                    # Commit offset после успешной обработки
                    await self.consumer.commit()

                    logger.debug(
                        f"Processed message from {self.topic}: "
                        f"partition={message.partition}, offset={message.offset}"
                    )

                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    # Не делаем commit → сообщение будет перечитано

        except KafkaError as e:
            logger.error(f"Kafka error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)