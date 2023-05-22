## Домашнее задание к уроку 06


### Цели занятия
* описать основы работы с Clickhouse, архитектура и возможности.

### Краткое содержание
* когда Clickhouse полезен, а когда не стоит его использовать;
* основные движки таблиц/БД Clickhouse и их особенности;
* движок MergeTree и его специфика;
* использование совместно с Kafka и PostgreSQL
* протоколы доступа (http, tcp и базовые библиотеки);
* установка и настройка

### Домашнее задание
* развернуть БД;
* выполнить импорт тестовой БД;
* выполнить несколько запросов и оценить скорость выполнения.
* развернуть дополнительно одну из тестовых БД https://clickhouse.com/docs/en/getting-started/example-datasets , протестировать скорость запросов
* развернуть Кликхаус в кластерном исполнении, создать распределенную таблицу, заполнить данными и протестировать скорость по сравнению с 1 инстансом

#

* Данные скачаны и залиты в CH

```
cat n(файла) | clickhouse-client --password=passwd --query 'INSERT INTO taxi.taxi_trips FORMAT CSVWithNames'
```

* Создание таблицы 

```
CREATE TABLE taxi.taxi_trips
(
    `unique_key` String,
    `taxi_id` String,
    `trip_start_timestamp` DateTime,
    `trip_end_timestamp` DateTime,
    `trip_seconds` Int64,
    `trip_miles` Decimal(10, 4),
    `pickup_census_tract` String,
    `dropoff_census_tract` String,
    `pickup_community_area` String,
    `dropoff_community_area` String,
    `fare` Decimal(10, 4),
    `tips` Decimal(10, 4),
    `tolls` Decimal(10, 4),
    `extras` Decimal(10, 4),
    `trip_total` Decimal(10, 4),
    `payment_type` String,
    `company` String,
    `pickup_latitude` Decimal(10, 4),
    `pickup_longitude` Decimal(10, 4),
    `pickup_location` String,
    `dropoff_latitude` Decimal(10, 4),
    `dropoff_longitude` Decimal(10, 4),
    `dropoff_location` String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(trip_start_timestamp)
ORDER BY (payment_type, tips, tolls)
```
ENGINE - движок

PARTITION BY - партиционирование gj

ORDER BY - группировака (индексирование)

* выведен count(*)

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/1.png" alt="" width="500" /></a>
</p>

* Выполним оценку времени выполнения эталонного запроса

```
select payment_type, round(sum(tips)/sum(trip_total)*100, 0) + 0 as tips_percent, count(*) as c from taxi.taxi_trips group by payment_type order by 3
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/2.png" alt="" width="500" /></a>
</p>

* Смотрим парты

```
SELECT
    table,
    partition,
    name,
    rows,
    disk_name
FROM system.parts;
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/3.png" alt="" width="500" /></a>
</p>

* Принудительная оптимизация PARTITION
```
OPTIMIZE TABLE taxi.taxi_trips FINAL
```

* После того, как прошла оптимизация, повторный запрос оценки времени (скорость кратно возрасла)

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/3.png" alt="" width="500" /></a>
</p>

#

### ClickHouse Cluster на VM