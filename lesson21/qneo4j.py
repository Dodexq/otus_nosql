from neo4j import GraphDatabase

touroperators = ["Пегас Туристик"]
pegas_country = ["Абхазия"]
abh_city = ["Гагра", "Гудаута", "Пицунда", "Цандрипш", "Новый Афон"]
ga_city_air = ["Бабушара", "Гали", "Бабушара", "Дранда", "Зугдиди"]
ga_city_train = ["Бабушара", "Дранда", "Зугдиди"]

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "neo4jtest"))

def add_touroperators(tx, toperator):
    tx.run("MERGE (operator:TourOperator {name: $toperator})",
           toperator=toperator)
    
def add_rship_tour_to_dest(tx, toperator, country):
    tx.run("MATCH (operator:TourOperator {name: $toperator})"
           "MERGE (operator)-[:TO_DESTINATION]->(:Destination {name: $country})", 
           toperator=toperator, country=country)

def add_rship_dest_to_city(tx, country, city):
    tx.run("MATCH (dest:Destination {name: $country})"
           "MERGE (dest)-[:BELONGS_TO]->(:City {name: $city})",
            country=country, city=city)
    
def add_connect_city_air(tx, city, air_to):
    tx.run("MATCH (city:City {name: $city})"
           "MERGE (city)-[:CONNECT_BY {transport: 'Airplane'}]->(:City {name: $air_to})",
           city=city, air_to=air_to)


def print_tour(tx, name):
    for record in tx.run("MATCH (a:City)"
                         "RETURN a", name=name):
        print(record[0].id)
        print(record[0]._properties['name'])

def test(tx, city, air_to):
    cid = tx.run("MATCH (a:City {name: $city}) RETURN a", city=city).value()
    aid = tx.run("MATCH (a:City {name: $air_to}) RETURN a", air_to=air_to).value()
    try:
        if cid[0]._properties['name'] == city:
            tx.run("MATCH (city:City {name: $city}) WHERE id(city) = $cid "
                "MERGE (:City {name: $city})-[:CONNECT_BY {transport: 'Airplane'}]->(at)",
                 city=city, cid=cid[0].id, air_to=air_to)
            
    except IndexError:
        print("Нет такого элемента", air_to)


def test2(tx, city, air_to):
    tx.run("CREATE (at:City {name: $city}) -[:CONNECT_BY]-> (:City {id: 1, name: $air_to})",
           city=city, air_to=air_to)
    
    
    # try:
    #     if rid[0]._properties['name'] in air_to:
    #         tx.run("MATCH (at:City {name: $air_to}) WHERE id(at) = $rid "
    #                "MERGE (:City {name: $city})-[:CONNECT_BY {transport: 'Airplane'}]->(at)",
    #                 city=city, rid=rid[0].id, air_to=air_to)
    #     print("Просто коннект")
    # except IndexError:
    #         tx.run("MERGE (:City {name: $city})-[:CONNECT_BY {transport: 'Airplane'}]->(:City {name: $air_to})",
    #         city=city, air_to=air_to)
    #         print("ЕХЕПТ")


    #     print(rid)
    #     print(rid[0].id, "YO")
    #     tx.run("MATCH (at:City {name: $air_to}) WHERE id(at) = $rid "
    #     "MERGE (:City {name: $city})-[:CONNECT_BY {transport: 'Airplane'}]->(at)",
    #     city=city, rid=rid[0].id, air_to=air_to)
    # else:
    #     print(rid, "NOYO")
    #     tx.run("MERGE (:City {name: $city})-[:CONNECT_BY {transport: 'Airplane'}]->(:City {name: $air_to})",
    #     city=city, air_to=air_to)

with driver.session() as session:
    session.write_transaction(test2, "Гагра", "Веталь")


    # for x in touroperators:
    #     session.write_transaction(add_touroperators, x)
    #     for y in pegas_country:
    #         session.write_transaction(add_rship_tour_to_dest, x, y)
    #         for z in abh_city:
    #             session.write_transaction(add_rship_dest_to_city, y, z)
    #             for a in ga_city_air:
    #                 session.write_transaction(test, z, a)

driver.close()