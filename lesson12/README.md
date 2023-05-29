## Домашнее задание к уроку 12

### Цель:
* Научитесь разворачивать ES и использовать полнотекстовый нечеткий поиск

### Домашнее задание:


* Развернуть Instance ES
* Создать в ES индекс, в нём должно быть обязательное поле text типа string
* Создать для индекса pattern
* Добавить в индекс как минимум 3 документа желательно со следующим содержанием:
    - «моя мама мыла посуду а кот жевал сосиски»
    - «рама была отмыта и вылизана котом»
    - «мама мыла раму»
* Написать запрос нечеткого поиска к этой коллекции документов ко ключу     
    - «мама ела сосиски»
* Расшарить коллекцию postman (желательно сдавать в таком формате)

#

1. Создание индекса с маппингом поля text
```
PUT /otus-homework
{
    "settings": {
        "analysis": {
            "filter": {
                "ru_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "ru_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "my_russian": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "ru_stop",
                        "ru_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "text": {
                "type": "text"
            }
        }
    }
}
```

2. Создание шаблона индекса
```
PUT /_index_template/otus-template
{
    "index_patterns": ["otus-*"],
    "template": {
        "settings": {
            "analysis": {
                "filter": {
                    "ru_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "ru_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "my_russian": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "ru_stop",
                            "ru_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "text": {
                    "type": "text"
                }
            }
        }
    }
}
```

* После создания нового индекса `otus-test-index` наследование шаблона

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson12/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson12/screenshots/1.png" alt="" width="500" /></a>
</p>

3. Добавление данных в индекс

```
POST /otus-homework/_doc/
{
  "text": "моя мама мыла посуду а кот жевал сосиски"
}

POST /otus-homework/_doc/
{
  "text": "рама была отмыта и вылизана котом"
}

POST /otus-homework/_doc/
{
  "text": "мама мыла раму"
}
```

4. Запрос нечеткого поиска к этой коллекции документов 

```
{
    "query": {
        "match": {
            "text": "мама ела сосиски"
        }
    }
}
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson12/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson12/screenshots/2.png" alt="" width="500" /></a>
</p>