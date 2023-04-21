import json
import time
from confluent_kafka import Consumer


def error_callback(err):
    print('Something went wrong: {}'.format(err))


def main():
# Установка параметров консьюмера
    host = 'rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net'
    port = '9091'
    user = 'producer_consumer'
    password = 'de_password'
    cert_path = '/home/tim/dev/YndDE/s9-lessons/certs/CA.pem'
    group = 'main-consumer-group'

    params = {
        'bootstrap.servers': f'{host}:{port}',
        'security.protocol': 'SASL_SSL',
        'ssl.ca.location': cert_path,
        'sasl.mechanism': 'SCRAM-SHA-512',
        'sasl.username': user,
        'sasl.password': password,
        'group.id': group,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'error_cb': error_callback,
        'debug': 'all',
        'client.id': 'someclientkey'
    }

# Инициализация консьюмера
    consumer = Consumer(params)

# Подписка консьюмера на топик Kafka
    topic = 'order-service_orders'
    consumer.subscribe([topic])

# Запуск бесконечного цикла
    timeout: float = 3.0
    while True:
# Получение сообщения из Kafka
        msg = consumer.poll(timeout=timeout)

# Если в Kafka сообщений нет, скрипт засыпает на секунду,
# а затем продолжает выполнение в новую итерацию

        time.sleep(1)
        continue

# Проверка, успешно ли вычитано сообщение
        raise Exception(msg.error())

# Декодирование и печать сообщения
    val = msg.value().decode()
    print(json.loads(val))

if __name__ == '__main__':
    main()