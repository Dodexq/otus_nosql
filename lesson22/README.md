## Теоретическое занятие 22

### Цели занятия
* Объяснить архитектуру kafka, плюсы и минусы;
* Сравнить в другими брокерами;
* Познакомиться с Kafka APIs;

### Краткое содержание
* kafka - обзор и архитектура;
* kafka Топики. Партишены и Реплики;
* основные операции на кластере;
* понимание кластерных метрик и того как их интерпретировать;
* понимание Producer API Kafka;
* понимание Consumer API Kafka;
* понимание Streams API Kafka;
* возможность интеграции Kafka с внешними системами данных с использованием Kafka Connect.

#
* Собран `docker-compose.replica.yml`
<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson22/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson22/screenshots/1.png" alt="" width="500" /></a>
</p>

#

Получить список топиков
```shell
docker exec -ti kafka-otuskafka /usr/bin/kafka-topics --list --bootstrap-server localhost:9091
```

Отправить сообщение
```shell
docker exec -ti kafka-otuskafka /usr/bin/kafka-console-producer --topic topic1 --bootstrap-server localhost:9091
```

Получить сообщения
```shell
docker exec -ti kafka-otuskafka /usr/bin/kafka-console-consumer --from-beginning --topic topic1 --bootstrap-server localhost:9091 
```

Получить сообщения как consumer1
```shell
docker exec -ti kafka-otuskafka /usr/bin/kafka-console-consumer --group consumer1 --topic topic1 --bootstrap-server localhost:9091 
```

Отправить сообщение c ключом через двоеточие (key:value)
```shell
docker exec -ti kafka-otuskafka /usr/bin/kafka-console-producer --topic topic1 --property "parse.key=true" --property "key.separator=:" --bootstrap-server localhost:9091
```

Коннектор в стандалон-режиме
```shell
docker exec -ti kafka-otuskafka /usr/bin/connect-standalone /usr/bin/connect/connect-standalone.properties /usr/bin/connect/connect-file-source.properties /usr/bin/connect/connect-file-sink.properties
```
