## Домашнее задание к уроку 20

### Краткое содержание
* особенности графовых баз данных;
* использование графовых баз данных в продакшене;
* тюнинг графовой БД.

#

```
docker run -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/s3cr3tqwe! neo4j
```

```
docker run --name psql -p 5432:5432 -e POSTGRES_USER=psqluser -e POSTGRES_PASSWORD=psqlpasswd -e POSTGRES_DB=dodexdb -d postgres:13.3
```

#

### Воспользоваться моделью, данными и командами из лекции и реализовать аналог в любой выбранной БД (реляционной или нет - на выбор).

1. Запись в Neo4j:

```
create (:Director {name:'Martin Scorsese'}) -[:CREATED]-> 
(sh:Movie {title: 'Shutter Island'}) <-[:PLAYED_IN]- (:Actor {name: 'Mark Ruffalo'})
create (:Actor {name:'Leonardo DiCaprio'}) -[:PLAYED_IN]-> (sh)
```

* Визуализация записи:

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson20/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson20/screenshots/1.png" alt="" width="500" /></a>
</p>

2. Аналог записи (схемы данных), но уже в psql.

```
CREATE TABLE Director (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE Movie (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    director_id INTEGER NOT NULL REFERENCES Director(id)
);

CREATE TABLE Actor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE MovieActor (
    movie_id INTEGER NOT NULL REFERENCES Movie(id),
    actor_id INTEGER NOT NULL REFERENCES Actor(id),
    PRIMARY KEY (movie_id, actor_id)
);
```

* Инсерт данных

```
INSERT INTO Director (name) VALUES ('Martin Scorsese');

INSERT INTO Movie (title, director_id) VALUES ('Shutter Island', 1);

INSERT INTO Actor (name) VALUES ('Mark Ruffalo'), ('Leonardo DiCaprio');

INSERT INTO MovieActor (movie_id, actor_id) VALUES (1, 1), (1, 2);
```

* Визуализация записи

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson20/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson20/screenshots/2.png" alt="" width="500" /></a>
</p>

#
### Придумать 2-3 варианта, когда применима графовая база данных. 

1. Социальные сети: Графовые базы данных отлично подходят для моделирования социальных связей и взаимодействий между пользователями. Они позволяют хранить информацию о профилях пользователей, их друзьях, подписчиках, группах и взаимодействиях, таких как комментарии, лайки и репосты. Графовая модель облегчает поиск и анализ связей между пользователями, рекомендации друзей или контента на основе общих интересов и установление связей между сообществами.

2. Рекомендательные системы: Графовые базы данных полезны для построения рекомендательных систем, которые основаны на анализе связей между объектами. Например, в электронной коммерции графовая база данных может содержать информацию о продуктах, пользователях, их покупках и предпочтениях. С использованием графовой модели можно строить рекомендации, исходя из схожих интересов или покупок других пользователей, а также анализировать связи между продуктами для предложения связанных товаров.

3. Анализ связей и сетевые графы: Графовые базы данных применяются для анализа связей и построения сетевых графов в различных областях, таких как телекоммуникации, биоинформатика, финансы и т.д. Например, в телекоммуникационной отрасли графовые базы данных могут моделировать сети связи между абонентами и анализировать связи между ними для оптимизации маршрутизации и предоставления персонализированных услуг. В биоинформатике графовые базы данных используются для анализа геномных данных, включая моделирование биологических сетей, взаимодействий между белками и генами, а также поиск генетических взаимосвязей и мутаций.