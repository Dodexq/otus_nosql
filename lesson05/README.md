## Практика к уроку 05

* концепция map-reduce;
* Зачем нужен map-reduce в mondodb;
* концепция pipeline;
* структура и синтаксис агрегации;
* $match;
* стадия $group;
* стадия $lookup;
* работа с геоданными.

#

Датасет `./user_data.csv` (https://www.convertcsv.com/generate-test-data.htm)

1. Агрегация данных (pipeline) по полю state: "NY", где считаем среднее значение dollar 

```
db.data.aggregate([
   { $match: { state: "NY" } },
   { $group: { _id: "$state", total: { $avg: "$dollar" } } },
   { $addFields: { totalRounded: { $round: ["$total"] } } },
   { $project: { total: 0 } }
])
```

2. $lookup = left join 

```
db.orders.insert([
   { "_id" : 1, "item" : "almonds", "price" : 12, "quantity" : 2 },
   { "_id" : 2, "item" : "pecans", "price" : 20, "quantity" : 1 },
   { "_id" : 3  }
])

db.inventory.insertMany([
   { "_id" : 1, "sku" : "almonds", description: "product 1", "instock" : 120 },
   { "_id" : 2, "sku" : "bread", description: "product 2", "instock" : 80 },
   { "_id" : 3, "sku" : "cashews", description: "product 3", "instock" : 60 },
   { "_id" : 4, "sku" : "pecans", description: "product 4", "instock" : 70 },
   { "_id" : 5, "sku": null, description: "Incomplete" },
   { "_id" : 6 }
])
```
Джойним и сохраняем в другую коллекцию
```
db.orders.aggregate([
   {
     $lookup:
       {
         from: "inventory",
         localField: "item",
         foreignField: "sku",
         as: "inventory_docs"
       }
  },
    { $out : "results" }
])
```
3. Map reduce - хотим узнать кол-во людей по штатам
```
function map(){
    emit(this.state, 1);
}

function reduce(key, values) {
    var sum = 0;
    for(var i in values) {
        sum += values[i];
    }
    return sum;
}

db.data.mapReduce(map, reduce,{out:"state"})
```


