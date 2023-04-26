from datetime import datetime
from logging import Logger

from lib.kafka_connect.kafka_connectors import KafkaConsumer, KafkaProducer
from lib.redis import RedisClient
from stg_loader.repository.stg_repository import StgRepository


class StgMessageProcessor:
    def __init__(self,
                 KafkaConsumer: KafkaConsumer,
                 KafkaProducer: KafkaProducer,
                 RedisClient: RedisClient,
                 StgRepository: StgRepository,
                 logger: Logger,
                 batch_size: int) -> None:
        self._consumer = KafkaConsumer
        self._producer = KafkaProducer
        self._redis = RedisClient
        self._stg_repository = StgRepository
        self._logger = logger
        self._batch_size = batch_size

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self._logger.info(f"{datetime.utcnow()}: START")

        # Имитация работы. Здесь будет реализована обработка сообщений.
        for _ in range(self._batch_size):
            input_msg = self._consumer.consume()
            if input_msg is None:
                break

            if input_msg.get('object_id'):
                self._stg_repository.order_events_insert(
                    input_msg['object_id'],
                    input_msg['object_type'],
                    input_msg['sent_dttm'],
                    input_msg['payload'],
                )

                user_id = input_msg['payload']['user']['id']
                restaurant_id = input_msg['payload']['restaurant']['id']

                user_data = self._redis.get(user_id)
                restaurant_data = self._redis.get(restaurant_id)
                
                exit_msg = dict(
                    object_id=input_msg['object_id'],
                    object_type=input_msg['object_type'],
                    payload={
                        "id": input_msg['object_id'],
                        "date": input_msg['payload']['date'],
                        "cost": input_msg['payload']['cost'],
                        "payment": input_msg['payload']['payment'],
                        "status": input_msg['payload']['final_status'],
                        "restaurant": {
                            "id": restaurant_data['_id'],
                            "name": restaurant_data['name']
                        },
                        "user": {
                            "id": user_data['_id'],
                            "name": user_data['name']
                        },
                        "products": restaurant_data['menu']
                    }
                )

                self._producer.produce(exit_msg)

        # Пишем в лог, что джоб успешно завершен.
        self._logger.info(f"{datetime.utcnow()}: FINISH")