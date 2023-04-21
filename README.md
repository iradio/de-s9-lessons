## Redis
``` JSON
{
    "redis":{
        "host": "c-c9qs6ld6nntbvr2u5o6e.rw.mdb.yandexcloud.net",
        "port": 6380,
        "password": "de_password"
    }
}
```

to fill Redis with test object
``` bash
 curl -X POST https://redis-data-service.sprint9.tgcloudenv.ru/test_redis \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "c-c9qs6ld6nntbvr2u5o6e.rw.mdb.yandexcloud.net",
        "port": 6380,
        "password": "de_password"
    }
}
EOF
```

Load users to Redis with "fill Redis service"
``` bash
curl -X POST https://redis-data-service.sprint9.tgcloudenv.ru/load_users \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "c-c9qs6ld6nntbvr2u5o6e.rw.mdb.yandexcloud.net",
        "port": 6380,
        "password": "de_password"
    }
}
EOF 
```
Load restoraunts to Redis with "fill Redis service"
``` bash
curl -X POST https://redis-data-service.sprint9.tgcloudenv.ru/load_restaurants \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "redis":{
        "host": "c-c9qs6ld6nntbvr2u5o6e.rw.mdb.yandexcloud.net",
        "port": 6380,
        "password": "de_password"
    }
}
EOF 
```
## Kafka
``` bash
docker run \
    -it \
    --network=host \
    -v "/home/tim/dev/YndDE/s9-lessons/certs/CA.pem:/data/CA.pem" \
    edenhill/kcat:1.7.1 \
    -b rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net:9091 \
    -X security.protocol=SASL_SSL \
    -X sasl.mechanisms=SCRAM-SHA-512 \
    -X sasl.username=producer_consumer \
    -X sasl.password=de_password \
    -X ssl.ca.location=/data/CA.pem \
    -L 
```

```
kafkacat -C \
        -b rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net:9091 \
        -X security.protocol=SASL_SSL \
        -X sasl.mechanisms=SCRAM-SHA-512 \
        -X sasl.username=producer_consumer \
        -X sasl.password=de_password \
        -X ssl.ca.location=./certs/CA.pem \
        -L
```
Получение сообщений из топика `order-service_orders`
``` bash
docker run \
    -it \
    --name "kcat" \
    --network=host \
    --rm \
    -v "/home/tim/dev/YndDE/s9-lessons/certs/CA.pem:/data/CA.pem" \
    edenhill/kcat:1.7.1 \
    -b rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net:9091 \
    -X security.protocol=SASL_SSL \
    -X sasl.mechanisms=SCRAM-SHA-512 \
    -X sasl.username=producer_consumer \
    -X sasl.password=de_password \
    -X ssl.ca.location=/data/CA.pem \
    -t order-service_orders \
    -C \
    -o beginning
```
Проверьте корректность работы кластера: отправьте параметры подключения к Kafka POST-запросом в наш сервис — https://order-gen-service.sprint9.tgcloudenv.ru/test_kafka. Это можно сделать с помощью утилиты curl:
``` bash
curl -X POST https://order-gen-service.sprint9.tgcloudenv.ru/test_kafka \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "student": "tim.aleinikov",
    "kafka_connect":{
        "host": "rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net",
        "port": 9091,
        "topic": "order-service_orders",
        "producer_name": "producer_consumer",
        "producer_password": "de_password"
    }
}
EOF
```

Вам необходимо передать параметры подключения к вашему Kafka коллегам из команды бэкенда, чтобы те настроили поток сообщений в брокер.
Для этого выполните запрос, подставив параметры подключения к Kafka.
``` BASH
curl -X POST https://order-gen-service.sprint9.tgcloudenv.ru/register_kafka \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
    "student": "tim.aleinikov",
    "kafka_connect":{
        "host": "rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net",
        "port": 9091,
        "topic": "order-service_orders",
        "producer_name": "producer_consumer",
        "producer_password": "de_password",
        "topic": "order-service_orders"
    }
}
EOF
```

Снова переведите kcat в режим консьюмера:
``` bash
docker run \
    -it \
    --name "kcat" \
    --network=host \
    --rm \
    -v "/home/tim/dev/YndDE/s9-lessons/certs/CA.pem:/data/CA.pem" \
    edenhill/kcat:1.7.1 \
    -b rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net:9091 \
    -X security.protocol=SASL_SSL \
    -X sasl.mechanisms=SCRAM-SHA-512 \
    -X sasl.username=producer_consumer \
    -X sasl.password=de_password \
    -X ssl.ca.location=/data/CA.pem \
    -t order-service_orders \
    -C \
    -o beginning
```

Отправьте параметры подключения к PostgreSQL POST-запросом в наш сервис — https://postgres-check-service.sprint9.tgcloudenv.ru/init_schemas. Это можно сделать с помощью утилиты curl:
``` bash
curl -X POST https://postgres-check-service.sprint9.tgcloudenv.ru/init_schemas \
-H 'Content-Type: application/json; charset=utf-8' \
--data-binary @- << EOF
{
  "student": "tim.aleinikov",
  "pg_settings": {
    "host": "rc1b-pkh0xycy94xo8dd1.mdb.yandexcloud.net",
    "port": 6432,
    "dbname": "sprint9dwh",
    "username": "de_user",
    "password": "de_password"
  }
}
EOF
```
Создайте топик в вашей Kafka, назовите его stg-service-orders.
``` bash
kafkacat -P \
        -b rc1b-ritu3rhvp59visbp.mdb.yandexcloud.net:9091 \
        -X security.protocol=SASL_SSL \
        -X sasl.mechanisms=SCRAM-SHA-512 \
        -X sasl.username=producer_consumer \
        -X sasl.password=de_password \
        -X ssl.ca.location=./certs/CA.pem \
        -t stg-service-orders