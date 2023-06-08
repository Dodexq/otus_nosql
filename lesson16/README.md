## Домашнее задание к уроку 16

### Цель:
* составить стратегии кеширования RDMBS с использованием Redis;
* применять Redis.

### Краткое содержание:
* кластеризация;
* redis sentinel;
* redis cluster.

### Домашнее задание:

* сохранить большой объем (~20МБ) в виде разных структур - string, hset, zset, list;
* протестировать скорость сохранения и чтения;
* предоставить отчет.

* (*) настроить редис кластер на 3х нодах с отказоусточивостью, затюнить таймоуты

#

### Тестирование скорости записи и чтения данных из БД, отчет:

1. Написан скрипт генерации данных, и передача данных разных типов с тестированием на скорость чтение и запись. `./generator.py`

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/1.png" alt="" width="500" /></a>
</p>

2. Все данные ~ 20 мбайт

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/2.png" alt="" width="500" /></a>
</p>

#

### (*) Сборка Redis Sentinel (Репликация + выбор нового Master)

1. Установлен pass на всех нодах в конфиге для дефолтного юзера `requirepass foobared` Передаем в переменную `export REDISCLI_AUTH=foobared`

2. Добавлен в `/etc/redis/redis.conf` на всех нодах
```
replicaof 192.168.0.210 6379
masterauth foobared
```

3. Проверка, 2 слейва успешно подключены

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/3.png" alt="" width="500" /></a>
</p>

* Архитектура `Redis Sentinel` - это отдельный процесс, работающий на порту 26379

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/4.png" alt="" width="500" /></a>
</p>

4. Конфигурационный файл Sentinel взят с офф сайта, внесены правки:
```
daemonize yes
logfile "/var/log/redis/sentinet.log"
sentinel monitor mymaster 192.168.0.210 6379 2
sentinel auth-pass mymaster foobared
sentinel down-after-milliseconds mymaster 30000
```

5. Установка необходимых прав:
```
chown redis:redis /etc/redis/sentinel.conf
touch /var/log/redis/sentinel.log
chown redis:redis /var/log/redis/sentinel.log
chmod 640 /etc/redis/sentinel.conf
chmod 660 /var/log/redis/sentinel.log
```

6. Смотрим логи, что sentinel подключился:

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/5.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/5.png" alt="" width="500" /></a>
</p>

7. Роняем мастер, видим, что мастер переключился:

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/6.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/6.png" alt="" width="500" /></a>
</p>

* другой сервер стал мастером

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/7.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson16/screenshots/7.png" alt="" width="500" /></a>
</p>

* docker-compose кластера `./docker/docker-compose.yaml`