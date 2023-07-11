import random
from neo4j import GraphDatabase

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

def test(tx, city, air_to, transport):
    cid = tx.run("MATCH (a:City {name: $city}) RETURN a", city=city).value()
    aid = tx.run("MATCH (a:City {name: $air_to}) RETURN a", air_to=air_to).value()
    
    try:
        if cid[0]._properties['name'] == city and aid[0]._properties['name'] == air_to:
            tx.run("MATCH (city:City {name: $city}) WHERE id(city) = $cid "
                "MATCH (air_to:City {name: $air_to} WHERE id(air_to) = $aid)"
                "MERGE (city)-[:CONNECT_BY {transport: $transport}]->(air_to)",
                 city=city, cid=cid[0].id, air_to=air_to, aid=aid[0].id, transport=transport)
    except IndexError:
        pass

    try:
        if cid[0]._properties['name'] == city:
            tx.run("MATCH (city:City {name: $city}) WHERE id(city) = $cid "
                "MERGE (city)-[:CONNECT_BY {transport: $transport}]->(air_to:City {name: $air_to})",
                 city=city, cid=cid[0].id, air_to=air_to, transport=transport)
            return
    except IndexError:
        pass        
    
    try:
        if aid[0]._properties['name'] == air_to:
            tx.run("MATCH (air_to:City {name: $air_to}) WHERE id(air_to) = $aid "
                "MERGE (:City {name: $city})-[:CONNECT_BY {transport: $transport}]->(air_to)",
                 city=city, aid=aid[0].id, air_to=air_to, transport=transport)
    except IndexError:
        print("ТУТ")
        tx.run("MERGE (:City {name: $city})-[:CONNECT_BY {transport: $transport}]->(:City {name: $air_to})",
        city=city, air_to=air_to, transport=transport)



def pegas():
    
    touroperators = ["Пегас Туристик"]
    pegas_country = ["Абхазия"]
    abh_city = ["Гагра", "Гудаута", "Пицунда", "Цандрипш", "Новый Афон"]
    ga_city_air = ["Бабушара", "Дранда", "Зугдиди"]
    ga_city_train = ["Бабушара", "Дранда", "Гали"]

    with driver.session() as session:
        
        for x in touroperators:
            session.write_transaction(add_touroperators, x)
            for y in pegas_country:
                session.write_transaction(add_rship_tour_to_dest, x, y)
                for z in abh_city:
                    session.write_transaction(add_rship_dest_to_city, y, z)
        
        for a in abh_city:
            if ga_city_air:
                session.write_transaction(test, a, ga_city_air.pop(random.randrange(len(ga_city_air))), "Airplane")
            else: 
                break
        for b in abh_city:
            if ga_city_train:
                session.write_transaction(test, b, ga_city_train.pop(random.randrange(len(ga_city_train))), "Train")
            else: 
                break

    driver.close()