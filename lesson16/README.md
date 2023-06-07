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
