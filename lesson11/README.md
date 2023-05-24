## Домашнее задание к уроку 11


### Цель:

* Подготовить среду и развернуть Cassandra кластер для дальнейшего изучения возможностей маштабирования и восстанавления Cassandra кластеров.

### Домашнее задание:
* развернуть docker локально или в облаке
* поднять 3 узловый Cassandra кластер.
* Создать keyspase с 2-мя таблицами. Одна из таблиц должна иметь составной Partition key, как минимум одно поле - clustering key, как минимум одно поле не входящее в primiry key.
* Заполнить данными обе таблицы.
* Выполнить 2-3 варианта запроса использую WHERE
* Создать вторичный индекс на поле, не входящее в primiry key.
* (*) нагрузить кластер при помощи Cassandra Stress Tool (используя "How to use Apache Cassandra Stress Tool.pdf" из материалов).

#

1. Развернут поднято 3 ноды кластера Cassandra в docker-compose

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson11/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson11/screenshots/1.png" alt="" width="500" /></a>
</p>

2. Создан keyspase с 2-мя таблицами
```
CREATE KEYSPACE store WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};
```

* Таблица с составным Partition key, как минимум одно поле - clustering key  

```
CREATE TABLE store.orders (
    city text,
    order_date date,
    order_id UUID,
    product_name text,
    quantity int,
    total_amount decimal,
    PRIMARY KEY ((city, order_date), order_id)
);
```
<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson11/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson11/screenshots/2.png" alt="" width="500" /></a>
</p>

* Вторая таблица с обычным PRIMARY KEY
```
CREATE TABLE store.daily_visitors (
    visit_date date PRIMARY KEY,
    visitor_count int,
    total_sales decimal
);
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson11/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson11/screenshots/3.png" alt="" width="500" /></a>
</p>

