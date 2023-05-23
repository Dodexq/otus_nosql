## Домашнее задание к уроку 09


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
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/4.png" alt="" width="500" /></a>
</p>

#

### ClickHouse Cluster на VM

* Архитектура

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/5.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/5.png" alt="" width="500" /></a>
</p>

Машины:

`zookeeper1.dodex.home`

`click1.dodex.home`

`click2.dodex.home`

`click3.dodex.home`
#

### Установка ZooKeeper на `zookeeper1.dodex.home` 

1. `sudo apt-get install zookeeper netcat` 
2. Добавить в `/etc/zookeeper/conf/myid` значение 1
3. В конфиг `/etc/zookeeper/conf/zoo.cfg` добавить:

```
autopurge.purgeInterval=1
autopurge.snapRetainCount=5
```
Раскоментить `server.1=zookeeper1.dodex.home`, указав hostname сервера zookeeper

4. Старт zookeeper `sudo -u zookeeper /usr/share/zookeeper/bin/zkServer.sh start`

5. Установка Altinity репо на click1-click3
```
sudo sh -c 'mkdir -p /usr/share/keyrings && curl -s https://builds.altinity.cloud/apt-repo/pubkey.gpg | gpg --dearmor > /usr/share/keyrings/altinity-dev-archive-keyring.gpg'

sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/altinity-dev-archive-keyring.gpg] https://builds.altinity.cloud/apt-repo stable main" > /etc/apt/sources.list.d/altinity-dev.list'

sudo apt update
```

6. Установка ClickHouse
```
version=21.8.13.1.altinitystable

sudo apt-get install clickhouse-common-static=$version clickhouse-client=$version clickhouse-server=$version
```

7. Для простоты примера, удалим пароль default user с каждой ClickHouse VM и запустим 
```
sudo rm /etc/clickhouse-server/users.d/default-password.xml

sudo systemctl start clickhouse-server
```

8. На каждой из нод создать дирректорию и файл конфигурации `/etc/clickhouse-server/config.d/zookeeper.xml` заполнив:

```
<yandex>
    <zookeeper>
        <node>
            <host>zookeeper1.dodex.home</host>
            <port>2181</port>
        </node>
        <session_timeout_ms>30000</session_timeout_ms>
        <operation_timeout_ms>10000</operation_timeout_ms>
    </zookeeper>

    <distributed_ddl>
        <path>/clickhouse/task_queue/ddl</path>
    </distributed_ddl>
</yandex>
```

9. Так же, для каждой из нод, `/etc/clickhouse-server/config.d/macros.xml` для примера 1 нода:

```
<yandex>
    <macros>
        <cluster>clickcluster</cluster>
        <shard>1</shard>
        <replica>click1.dodex.home</replica>
    </macros>
</yandex>
```

10. Настройка кластера `/etc/clickhouse-server/config.d/clusters.xml`
```
<yandex>
    <remote_servers>
        <clickcluster>
            <shard>
                <replica>
                    <host>click1.dodex.home</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>click2.dodex.home</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>click3.dodex.home</host>
                    <port>9000</port>
                </replica>
            </shard>
        </clickcluster>
    </remote_servers>
</yandex>
```
11. Слушать всех IP `/etc/clickhouse-server/users.d/listen.xml`
```
<yandex>
    <listen_host>::</listen_host>
</yandex>
```

12. Рестарт на 3 нодах `systemctl restart clickhouse-server`

13. Проверяем состояние кластера
```
clickhouse-client -q "SELECT * FROM system.clusters WHERE cluster='altinitydemo' FORMAT Vertical;"
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/6.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/6.png" alt="" width="500" /></a>
</p>

#

14. Создадим тестовую таблицу
```
CREATE TABLE replicatest ON CLUSTER '{cluster}'
(
    timestamp DateTime,
    contractid UInt32,
    userid UInt32
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/default/replicatest', '{replica}')
PARTITION BY toYYYYMM(timestamp)
ORDER BY (contractid, toDate(timestamp), userid)
SAMPLE BY userid;
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/7.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/7.png" alt="" width="500" /></a>
</p>


15. Инсертим данные, проверим, как работает репликация

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/8.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/8.png" alt="" width="500" /></a>
</p>

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/9.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/9.png" alt="" width="500" /></a>
</p>



16. Заливаем в кластер данные cell_tower https://clickhouse.com/docs/en/getting-started/example-datasets/cell-towers

```
CREATE DATABASE otus ON CLUSTER '{cluster}'
CREATE TABLE democell_towers ON CLUSTER '{cluster}'
(
    radio Enum8('' = 0, 'CDMA' = 1, 'GSM' = 2, 'LTE' = 3, 'NR' = 4, 'UMTS' = 5),
    mcc UInt16,
    net UInt16,
    area UInt16,
    cell UInt64,
    unit Int16,
    lon Float64,
    lat Float64,
    range UInt32,
    samples UInt32,
    changeable UInt8,
    created DateTime,
    updated DateTime,
    averageSignal UInt8
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/otus/democell_towers', '{replica}')
ORDER BY (radio, mcc, net, created);
```

17. Вставляем
```
clickhouse-client --query "INSERT INTO otus.democell_towers FORMAT CSVWithNames" < cell_towers.csv
```

18. После заливки на ноду click1, проверяем, появились ли данные на других

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/10.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson09/screenshots/10.png" alt="" width="500" /></a>
</p>

```
CREATE TABLE taxi.taxi_trips ON CLUSTER '{cluster}'
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
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/taxi/taxi_trips', '{replica}')
PARTITION BY toYYYYMM(trip_start_timestamp)
ORDER BY (payment_type, tips, tolls)
```