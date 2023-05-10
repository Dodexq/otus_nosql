## Необходимо установить MongoDB заполнить данными, написать несколько запросов на выборку и обновление данных. Создать индексы и сравнить производительность.
#

1. Датасет был успешно залит, посмотрим содержимое документов используя лимит:

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/1.png" alt="" width="500" /></a>
</p>

2. Посмотрим количество вин, определенной крепости:

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/2.png" alt="" width="500" /></a>
</p>

3. Обновим крепость у первого выданного вина с `_id=ObjectId("645b4bdd77b76f5503611c66")`

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/3.png" alt="" width="500" /></a>
</p>

4. Теперь обновим несколько документов. Например, мы хотим обновить quality у всех вин, у которых pH строго меньше 2.9

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/4.png" alt="" width="500" /></a>
</p>

5. Создаем индекс, удаляем изначально "citric acid" <=1, после коллекцию и саму базу

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/5.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/5.png" alt="" width="500" /></a>
</p>

6. Сравнение с индексом и без, на данных побольше

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/6.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/6.png" alt="" width="500" /></a>
</p>

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/7.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson03/screenshots/7.png" alt="" width="500" /></a>
</p>