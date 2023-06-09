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

### На примере кейспейса и таблицы:

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
```

1. Создание снапшота, на примере снапшота отдельной таблицы кейспейса

```
nodetool snapshot --tag otus-snap --table shopping_cart2 otus
```
Снапшот находим в директории `/var/lib/cassandra/data/otus/shopping_cart2-288dc700fe1211ed9575ede754538f2f/snapshots/otus-snap/`



<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/2.png" alt="" width="500" /></a>
</p>

2. Создание инкрементал бекапа

* В конфиге `cassandra.yaml` устанавливаем значение:

```
incremental_backups: true
```

* После каждого flush таблицы или кейспейса (используется для принудительной записи всех внутренних данных мемтаблиц (memtable) на диск в виде SSTable (Sorted String Table) файлов.) 

```
nodetool flush otus shopping_cart2
```

Бекап находим в директории `/var/lib/cassandra/data/otus/shopping_cart2-288dc700fe1211ed9575ede754538f2f/backups` копируем его.

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/3.png" alt="" width="500" /></a>
</p>

3. Восстановление из Снапшота (после очистки данных с 2 нод)

* Перед восстановлением обязательно создать KEYSPACE и TABLE
* Поместить snapshots в директорию `./data/KEYSPACE/TABLE_UUID/snapshots/SNAPSHOTS_NAME/`
```
nodetool import otus shopping_cart2 /var/lib/cassandra/data/otus/shopping_cart2-288dc700fe1211ed9575ede754538f2f/snapshots/otus-snap/
```
* Далее после восстановления данных или переноса на новый кластер необходимо выполнить nodetool repair:

```
nodetool repair otus
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/4.png" alt="" width="500" /></a>
</p>


### Конфиг бекапа `cassandra.yaml`
* `snapshot_before_compaction` - параметр конфигурации Cassandra, который позволяет создать snapshot данных перед compaction
* `incremental_backups` -  механизм резервного копирования данных в Cassandra, который позволяет создавать инкрементальные копии измененных данных с момента предыдущего резервного копирования. 
* Создание снапшота `nodetool snapshot --tag example-tag catalogkeyspace`

#

### Задание со (*) Установка Cassandra в кластер Kubernetes (Rancher) с бекабированием 3DSnap

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/5.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/5.png" alt="" width="500" /></a>
</p>


1. Добавление /dev/sdb на все ноды под portworx, и развертывание portworx

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/6.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/6.png" alt="" width="500" /></a>
</p>

2. Установка cassandra и проверка кластера

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/7.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/7.png" alt="" width="500" /></a>
</p>

3. Заливка тех же данных, что и в примере выше

4. Проверим, на каких нодах лежат данные `kubectl exec -it cassandra-0 -- nodetool getendpoints otus shopping_cart2 userid` фактор репликации - 2

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/8.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/8.png" alt="" width="500" /></a>
</p>

5. Добавляем групповой снапшот и правило для Cassandra `./3dSnap`, проверяем `kubectl get volumesnapshot.volumesnapshot.external-storage.k8s.io`, из них и будем восстанавливаться

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/9.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/9.png" alt="" width="500" /></a>
</p>

```
cassandra-group-snapshot-cassandra-data-cassandra-0-9e01f2bd-230b-4666-bd49-7e63662138a2
cassandra-group-snapshot-cassandra-data-cassandra-1-9e01f2bd-230b-4666-bd49-7e63662138a2
cassandra-group-snapshot-cassandra-data-cassandra-2-9e01f2bd-230b-4666-bd49-7e63662138a2
```

6. Пример PVC для рестора снапшота
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cassandra-data-cassandra-0
  annotations:
    snapshot.alpha.kubernetes.io/snapshot: "cassandra-group-snapshot-cassandra-data-cassandra-0-9e01f2bd-230b-4666-bd49-7e63662138a2"
spec:
  accessModes:
     - ReadWriteOnce
  storageClassName: stork-snapshot-sc
  resources:
    requests:
      storage: 10Gi
```

7. Снес Cassandra и PVC, восстановил PVC из `./cassandra/px-cassandra-restore-pvc.yaml` данные восстановились.

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/10.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson13/screenshots/10.png" alt="" width="500" /></a>
</p>

