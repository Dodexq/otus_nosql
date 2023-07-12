## Домашнее задание к уроку 21
 
### Краткое содержание
* основные юзкейсы для графовой БД;
* архитектура Neo4J.

### Задание
* Взять 4-5 популярных туроператора.
* Каждый туроператор должен быть представлен в виде ноды neo4j
* Взять 10-15 направлений, в которые данные операторы предосавляют путевки.
* Представить направления в виде связки нод: страна - конкретное место
* Взять ближайшие к туриситческим локацимя города, в которых есть аэропорты или вокзалы и представить их в виде нод
* Представить маршруты между городми в виде связей. Каждый маршрут должен быть охарактеризован видом транспорта, который позволяет переместиться между точками.
* Написать запрос, который бы выводил направление (со всеми промежуточными точками), который можно осуществить только наземным транспортом.
* Составить план запроса для задания "Использование neo4j" (с туропертором)
* Добавить индексы для оптимизации запроса
* Еще раз посмотреть план запроса и убедиться, что индексыпозволили оптимизировать запрос

#

```
docker-compose up
```

#

1. Данные были заполнены средствами написанного скрипта `./qneo4j.py`

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/1.png" alt="" width="500" /></a>
</p>

2. Все возможные поездки поездами между городами, куда нельзя попасть напрямую. Пример запроса: 
```
PROFILE MATCH (a:City)-[b:CONNECT_BY {transport: "Train"}]-(c:City)
RETURN a,b,c
```
Возвращает:
<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/2.png" alt="" width="500" /></a>
</p>

#

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/3.png" alt="" width="500" /></a>
</p>

3. Функция `print_train()` принтует все варианты

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/4.png" alt="" width="500" /></a>
</p>

4. PROFILE запроса без интекса:

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/5.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/5.png" alt="" width="500" /></a>
</p>

5. PROFILE запроса, где создано 2 индекса, что ускоряет поиск.
```
CREATE INDEX index_city FOR (n:City) ON (n.name)

CREATE INDEX rel_range_index_name FOR ()-[r:CONNECT_BY]-() ON (r.transport)
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/6.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson21/screenshots/6.png" alt="" width="500" /></a>
</p>