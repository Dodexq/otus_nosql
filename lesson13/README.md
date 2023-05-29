## Домашнее задание к уроку 13

### Цель:
* В результате выполнения ДЗ вы изучите возможности восстановления Cassandra кластеров

### Домашнее задание:

* Воспользовавшись инструкцией https://cassandra.apache.org/doc/latest/cassandra/operating/backups.html создать бэкап и восстановиться из него.
* воспользоваться сторонними средствами для бэкапа всего кластера, например 3dnap:
https://portworx.com/blog/kubernetes-cassandra-run-ha-cassandra-rancher-kubernetes-engine/

#
### Развернут кластер из 2 нод

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/1.png" alt="" width="500" /></a>
</p>

Существует 2 типа бекапа:

* Snapshots
* Incremental Backups 


1. Создание снапшота, на примере снапшота отдельной таблицы кейспейса
```
CREATE KEYSPACE IF NOT EXISTS otus WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '2' };

CREATE TABLE IF NOT EXISTS otus.shopping_cart2 (
userid text,
item_count int,
date_created date,
last_update_timestamp timestamp,
PRIMARY KEY ((userid, date_created), last_update_timestamp)
);

INSERT INTO otus.shopping_cart2
(userid, item_count, date_created, last_update_timestamp)
VALUES ('9876', 2, '2023-05-03', toTimeStamp(now()));
INSERT INTO otus.shopping_cart2
(userid, item_count, date_created,  last_update_timestamp)
VALUES ('1234', 5, '2023-05-02', toTimeStamp(now()));
INSERT INTO otus.shopping_cart2
(userid, item_count, date_created,  last_update_timestamp)
VALUES ('1234', 5, '2023-05-03', toTimeStamp(now()));
INSERT INTO otus.shopping_cart2
(userid, item_count, date_created,  last_update_timestamp)
VALUES ('1234', 6, '2023-05-03', toTimeStamp(now()));

nodetool snapshot --tag otus-snap --table shopping_cart2 otus
```




1. Конфиг бекапа `cassandra.yaml`
* `snapshot_before_compaction` - параметр конфигурации Cassandra, который позволяет создать snapshot данных перед compaction
* `incremental_backups` -  механизм резервного копирования данных в Cassandra, который позволяет создавать инкрементальные копии измененных данных с момента предыдущего резервного копирования. 
* Создание снапшота `nodetool snapshot --tag catalog-ks catalogkeyspace`

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/1.png" alt="" width="500" /></a>
</p>