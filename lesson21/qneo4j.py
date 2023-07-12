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


def unique_id(tx, city, air_to, transport):
    cid = tx.run("MATCH (a:City {name: $city}) RETURN a", city=city).value()
    aid = tx.run("MATCH (a:City {name: $air_to}) RETURN a", air_to=air_to).value()
    
    try:
        if cid[0]._properties['name'] == city and aid[0]._properties['name'] == air_to:
            tx.run("MATCH (city:City {name: $city}) WHERE id(city) = $cid "
                "MATCH (air_to:City {name: $air_to}) WHERE id(air_to) = $aid "
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
        tx.run("MERGE (:City {name: $city})-[:CONNECT_BY {transport: $transport}]->(:City {name: $air_to})",
        city=city, air_to=air_to, transport=transport)

def print_tour(tx, name):
    for record in tx.run("MATCH (a:City)"
                         "RETURN a", name=name):
        print(record[0].id)
        print(record[0]._properties['name'])

def pegas():
    
    touroperators = ["Пегас Туристик"]
    pegas_country = ["Абхазия", "Египет"]
    abh_city = ["Гагра", "Гудаута", "Пицунда", "Цандрипш", "Новый Афон"]
    abh_city_air = ["Дранда", "Зугдиди", "Сухуми"]
    abh_city_train = ["Бабушара", "Дранда", "Гали", "Очамчира"]
    egypt_city = ["Дахаб", "Каир", "Марса Алам", "Матрух", "Нувейба"]
    egypt_city_air = ["Порт-Судан", "Асьют", "Сохаг", "Халаиб"]
    egypt_city_train = ["Кена", "Луксор", "Асуан", "Эдфу", "Халаиб", "Порт-Судан"]
    

    with driver.session() as session:
        
        for x in touroperators:
            session.write_transaction(add_touroperators, x)
            for y in pegas_country:
                session.write_transaction(add_rship_tour_to_dest, x, y)
                if y == "Абхазия":
                    for z in abh_city:
                        session.write_transaction(add_rship_dest_to_city, y, z)
                elif y == "Египет":
                    for a in egypt_city:
                        session.write_transaction(add_rship_dest_to_city, y, a)
        
        for a in abh_city:
            if abh_city_air:
                session.write_transaction(unique_id, a, abh_city_air.pop(random.randrange(len(abh_city_air))), "Airplane")
            else: 
                break
        for b in abh_city:
            if abh_city_train:
                session.write_transaction(unique_id, b, abh_city_train.pop(random.randrange(len(abh_city_train))), "Train")
            else: 
                break

        for c in egypt_city:
            if egypt_city_air:
                session.write_transaction(unique_id, c, egypt_city_air.pop(random.randrange(len(egypt_city_air))), "Airplane")
            else: 
                break
        for d in egypt_city:
            if egypt_city_train:
                session.write_transaction(unique_id, d, egypt_city_train.pop(random.randrange(len(egypt_city_train))), "Train")
            else: 
                break

    driver.close()

def biblio():
    
    touroperators = ["Библио Глобус"]
    biblio_globus = ["Турция", "Таиланд"]
    turk_city = ["Алания", "Анталия", "Белек", "Бодрум", "Болу"]
    turk_city_air = ["Газипаша", "Мерси", "Конья", "Анкара", "Махмутлар"]
    turk_city_train = ["Каргыджак", "Музкент", "Махмутлар", "Газипаша", "Ушак"]
    tay_city = ["Бангкок", "Као Лак", "Ко Чанг", "Краби", "Пхукет"]
    tay_city_air = ["Мэхонгсон", "Нан", "Нонтхабури", "Паккрет", "Ройет"]
    tay_city_train = ["Сена", "Хуахин", "Банбынг", "Ройет", "Патонг", "Нан"]
    

    with driver.session() as session:
        
        for x in touroperators:
            session.write_transaction(add_touroperators, x)
            for y in biblio_globus:
                session.write_transaction(add_rship_tour_to_dest, x, y)
                if y == "Турция":
                    for z in turk_city:
                        session.write_transaction(add_rship_dest_to_city, y, z)
                elif y == "Таиланд":
                    for a in tay_city:
                        session.write_transaction(add_rship_dest_to_city, y, a)
        
        for a in turk_city:
            if turk_city_air:
                session.write_transaction(unique_id, a, turk_city_air.pop(random.randrange(len(turk_city_air))), "Airplane")
            else: 
                break
        for b in turk_city:
            if turk_city_train:
                session.write_transaction(unique_id, b, turk_city_train.pop(random.randrange(len(turk_city_train))), "Train")
            else: 
                break

        for c in tay_city:
            if tay_city_air:
                session.write_transaction(unique_id, c, tay_city_air.pop(random.randrange(len(tay_city_air))), "Airplane")
            else: 
                break
        for d in tay_city:
            if tay_city_train:
                session.write_transaction(unique_id, d, tay_city_train.pop(random.randrange(len(tay_city_train))), "Train")
            else: 
                break

    driver.close()

def coral():
    
    touroperators = ["Корал Тревел"]
    coral_trevel = ["Шри-Ланка", "Азербайджан"]
    shr_city = ["Бентота", "Галле", "Калутара", "Канди", "Коггала"]
    shr_city_air = ["Сигирия", "Унаватуна", "Негомбо", "Полоннарува", "Калмунай"]
    shr_city_train = ["Моратува", "Калмунай", "Джафна", "Ратнапура", "Бадулла", "Сигирия"]
    azer_city = ["Баку", "Габала", "Нафталан", "Шахдаг", "Шеки"]
    azer_city_air = ["Бабек", "Ахсу", "Гах", "Зердаб", "Шамкир"]
    azer_city_train = ["Лачын", "Бабек", "Барда", "Шамкир", "Шуша", "Ярдымлы"]
    

    with driver.session() as session:
        
        for x in touroperators:
            session.write_transaction(add_touroperators, x)
            for y in coral_trevel:
                session.write_transaction(add_rship_tour_to_dest, x, y)
                if y == "Шри-Ланка":
                    for z in shr_city:
                        session.write_transaction(add_rship_dest_to_city, y, z)
                elif y == "Азербайджан":
                    for a in azer_city:
                        session.write_transaction(add_rship_dest_to_city, y, a)
        
        for a in shr_city:
            if shr_city_air:
                session.write_transaction(unique_id, a, shr_city_air.pop(random.randrange(len(shr_city_air))), "Airplane")
            else: 
                break
        for b in shr_city:
            if shr_city_train:
                session.write_transaction(unique_id, b, shr_city_train.pop(random.randrange(len(shr_city_train))), "Train")
            else: 
                break

        for c in azer_city:
            if azer_city_air:
                session.write_transaction(unique_id, c, azer_city_air.pop(random.randrange(len(azer_city_air))), "Airplane")
            else: 
                break
        for d in azer_city:
            if azer_city_train:
                session.write_transaction(unique_id, d, azer_city_train.pop(random.randrange(len(azer_city_train))), "Train")
            else: 
                break

    driver.close()

def search_train(tx, transport):
    for transport in tx.run("MATCH (a:City)-[b:CONNECT_BY {transport: $transport}]->(c:City)"
                            "RETURN a,b,c", 
                            transport=transport):
        print("Из", transport.data()['c']['name'], "можно добраться поездом до", transport.data()['a']['name'])

def print_train():
    with driver.session() as session:
        s = session.read_transaction(search_train, "Train")
    driver.close()
    return s
    


def main():
    pegas()
    biblio()
    coral()
    print_train()

main()