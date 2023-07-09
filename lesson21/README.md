## Домашнее задание к уроку 21

### 

### Краткое содержание
* основные юзкейсы для графовой БД;
* архитектура Neo4J.

#

```
docker-compose up
```

#

```
CREATE (pegas:TourOperator {name: "Пегас Туристик"}) -[:TO_DESTINATION]-> (abh:Destination {name: "Абхазия"}),
	(abh) -[:BELONGS_TO]-> (gagra:City {name: "Гагра"}),
	(gagra) -[:CONNECTED_BY {transport: "Airplane"}]-> (babush:City {name: "Бабушара"}),
	(gagra) -[:CONNECTED_BY {transport: "Airplane"}]-> (galy:City {name: "Гали"}),
	(gagra) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Бабушара"}),
	(gagra) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Дранда"}),
	(gagra) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Зугдиди"}),
	(abh) -[:BELONGS_TO]-> (gudanuta:City {name: "Гудаута"}),
	(gudanuta) -[:CONNECTED_BY {transport: "Train"}]-> (babush),
	(gudanuta) -[:CONNECTED_BY {transport: "Train"}]-> (galy),
	(gudanuta) -[:CONNECTED_BY {transport: "Airplane"}]-> (:City {name: "Мокви"}),
	(abh) -[:BELONGS_TO]-> (:City {name: "Пицунда"}),
	(abh) -[:BELONGS_TO]-> (cand:City {name: "Цандрипш"}),
	(cand) -[:CONNECTED_BY {transport: "Airplane"}]-> (:City {name: "Лихни"}),
	(cand) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Лихни"}),
	(cand) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Инкити"}),
	(cand) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Пицундра"}),
	(abh) -[:BELONGS_TO]-> (:City {name: "Новый Афон"}),
	(pegas) -[:TO_DESTINATION]-> (egypt:Destination {name: "Египет"}),
	(egypt) -[:BELONGS_TO]-> (dakh:City {name: "Дахаб"}),
	(dakh) -[:CONNECTED_BY {transport: "Train"}]-> (nuvey:City {name: "Нувейба"}),
	(dakh) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Таба"}),
	(dakh) -[:CONNECTED_BY {transport: "Airplane"}]-> (:City {name: "Таба"}),
	(dakh) -[:CONNECTED_BY {transport: "Train"}]-> (:City {name: "Акаба"}),
	(egypt) -[:BELONGS_TO]-> (сairo:City {name: "Каир"}),
	(сairo) -[:CONNECTED_BY {transport: "Airplane"}]-> (:City {name: "Асьют"}),
	(сairo) -[:CONNECTED_BY {transport: "Airplane"}]-> (:City {name: "Фарафра"}),
	(сairo) -[:CONNECTED_BY {transport: "Airplane"}]-> (:City {name: "Гирга"}),
	(сairo) -[:CONNECTED_BY {transport: "Train"}]-> (nuvey),
	(egypt) -[:BELONGS_TO]-> (:City {name: "Марса Алам"}),
	(egypt) -[:BELONGS_TO]-> (:City {name: "Матрух"}),
	(egypt) -[:BELONGS_TO]-> (nuvey),
	(pegas) -[:TO_DESTINATION]-> (thail:Destination {name: "Таиланд"}),
 	(thail) -[:BELONGS_TO]-> (:City {name: "Бангок"}),
 	(thail) -[:BELONGS_TO]-> (:City {name: "Као Лак"}),
 	(thail) -[:BELONGS_TO]-> (:City {name: "Ко Чанг"}),
 	(thail) -[:BELONGS_TO]-> (:City {name: "Краби"}),
 	(thail) -[:BELONGS_TO]-> (:City {name: "Паттайя"})
```