from neomodel import config, StructuredNode, StringProperty, RelationshipTo, RelationshipFrom

# Установка конфигурации подключения к базе данных Neo4j
config.DATABASE_URL = 'bolt://neo4j:neo4jtest@localhost:7687'

# Определение моделей данных
class TourOperator(StructuredNode):
    name = StringProperty()

class Destination(StructuredNode):
    name = StringProperty()

class City(StructuredNode):
    name = StringProperty()
    belongs_to = RelationshipTo("Person", 'BELONGS_TO')

class Dog(StructuredNode):
    name = StringProperty(unique_index=True)
    owner = RelationshipTo('Person', 'owner')

class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    pets = RelationshipFrom('Dog', 'owner')

bob = Person.get_or_create({"name": "Bob"})[0]
bobs_gizmo = Dog.get_or_create({"name": "Gizmo"}, relationship=bob.pets)

tim = Person.get_or_create({"name": "Tim"})[0]
tims_gizmo = Dog.get_or_create({"name": "Gizmo"}, relationship=tim.pets)

assert bobs_gizmo[0] != tims_gizmo[0]