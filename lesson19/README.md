## Теоретическое занятие 19


### Цели занятия
* Научиться работать с foundation db
* Разобраться с особенностями клиентских библиотек
* Проектировать транзакции с учетом их спецификации
* Развернуть класетр FoundationDB 


### Краткое содержание
* foundation db - обзор и архитектура
* Транзакции
* Масштабируемость и отказоустойчивость
* Ограничения

#

* Доступ к FoundationDB из вне `python3 /usr/lib/foundationdb/make_public.py`
* На всех узлах синхронизируется файл кластера со списком координаторов `/etc/foundationdb/fdb.cluster` (уже написано в vagrant provision)

* Собранный кластер

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson19/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson19/screenshots/1.png" alt="" width="500" /></a>
</p>

* Добавляем список координаторов `fdbcli`
```
coordinators 192.168.0.200:4500 192.168.0.201:4500 192.168.0.202:4500
```
* Двойная избыточность `configure double` (одна нода может упасть)

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson19/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson19/screenshots/2.png" alt="" width="500" /></a>
</p>