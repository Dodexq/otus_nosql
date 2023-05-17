## Домашнее задание к уроку 06

Темы урока:
* виды индексов в mongodb;
* профилирование;
* дисковые движки;
* GridFS;
* производительность кластеров.

Домашнее задание:
* построить шардированный кластер из 3 кластерных нод( по 3 инстанса с репликацией) и с кластером конфига(3 инстанса);
* добавить балансировку, нагрузить данными, выбрать хороший ключ шардирования, посмотреть как данные перебалансируются между шардами;
* поронять разные инстансы, посмотреть, что будет происходить, поднять обратно. Описать что произошло.
* настроить аутентификацию и многоролевой доступ;

#
ShardA:

mongodb-a1.dodex.home:27017

mongodb-a2.dodex.home:27017

mongodb-aa.dodex.home:27017

ShardB:

mongodb-b1.dodex.home:27017

mongodb-b2.dodex.home:27017

mongodb-ba.dodex.home:27017

RScfg:

mongodb-c1.dodex.home:27017

mongodb-c2.dodex.home:27017

mongodb-c3.dodex.home:27017

mongos:

mongodb-c1.dodex.home:27000

mongodb-c2.dodex.home:27000

mongodb-c3.dodex.home:27000

# 

### 1. Создано 9 виртуальных машин `./Vagrantfile`, объедененных в replica set, настроено шардирование.

Provision для всех VW: `./provision`

Конфиги mongodb `./etc`

keyfile `./mongodb-keyfile` 

На всех VM включен `net.bind_ip_all: true`, `replication.replSetName: Shard(*)`, `sharding.clusterRole: shardsvr` (configsvr на RScfg)


Создание пользователя и ролей

```
use admin
db.createUser(
    {
      user: "dodex",
      pwd: "passwd",
      roles: [ "userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase" ]
    }
)
```

Создание роли

```
db.createRole(
    {      
     role: "superRoot",      
     privileges:[
        { resource: {anyResource:true}, actions: ["anyAction"]}
     ],      
     roles:[] 
    }
)
```

Создание superuser

```
db.createUser({      
     user: "root",      
     pwd: "passwd",      
     roles: ["superRoot"] 
})
```


#

```
rs.initiate({"_id" : "ShardA", members : [{"_id" : 0, priority : 3, host : "mongodb-a1.dodex.home:27017"},
{"_id" : 1, host : "mongodb-a2.dodex.home:27017"},
{"_id" : 2, host : "mongodb-aa.dodex.home:27017"}]});
```
<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/1.png" alt="" width="500" /></a>
</p>

```
rs.initiate({"_id" : "ShardB", members : [{"_id" : 0, priority : 3, host : "mongodb-b1.dodex.home:27017"},
{"_id" : 1, host : "mongodb-b2.dodex.home:27017"},
{"_id" : 2, host : "mongodb-ba.dodex.home:27017"}]});
```
<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/2.png" alt="" width="500" /></a>
</p>

```
rs.initiate({"_id" : "RScfg", configsvr: true, members : [{"_id" : 0, priority : 3, host : "mongodb-c1.dodex.home:27017"},
{"_id" : 1, host : "mongodb-c2.dodex.home:27017"},
{"_id" : 2, host : "mongodb-c3.dodex.home:27017"}]});
```

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/3.png" alt="" width="500" /></a>
</p>

#
`sudo mkdir /home/vagrant/dbs && sudo chmod 777 /home/vagrant/dbs`

Запускаем mongos на mongodb-c1(c2,c3)
```
sudo mongos --configdb RScfg/mongodb-c1.dodex.home:27017,mongodb-c2.dodex.home:27017,mongodb-c3.dodex.home:27017 --port 27000 --fork --logpath /home/vagrant/dbs/dbs.log --pidfilepath /home/vagrant/dbsdbs.pid --keyFile /home/vagrant/mongodb-keyfile --bind_ip_all
```

Логинимся `mongosh --port 27017 -u "dodex" -p "passwd" --authenticationDatabase "admin"`, убеждаемся, что шардирование настроено


<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/4.png" alt="" width="500" /></a>
</p>

#

2. Вливаем данные `./dataset.csv`

Меняем chunksize
```
use config
db.settings.updateOne(
   { _id: "chunksize" },
   { $set: { _id: "chunksize", value: 5 } },
   { upsert: true }
)
```

Создаем БД otus и включаем шардинг для всей БД `sh.enableSharding("otus")`
Вливаем данные `mongoimport --type csv -d otus -c users_dataset --headerline /vagrant/dataset.csv -u root --authenticationDatabase "admin" --port 27000`

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/5.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson06/screenshots/5.png" alt="" width="500" /></a>
</p>

Выбираем наиболее уникальный индекс `email`, создаем и указываем как ключ шардирования `db.users_dataset.createIndex({email: 1})`

db.runCommand({shardCollection: "otus.users_dataset", key: {email: 1}})
sh.balancerCollectionStatus("otus.users_dataset")


db.users_dataset.aggregate([ { $match: { state: "TX", gender: "Female", age: { $gt: 25 } } }, { $group: { _id: 0, avgDollar: { $avg: "$dollar" } } }])