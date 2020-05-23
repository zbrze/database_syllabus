from neo4j import GraphDatabase
from random import randint
import csv

# class HelloWorldExample(object):

#     def __init__(self, uri, user, password):
#         self._driver = GraphDatabase.driver(uri, auth=(user, password))

#     def close(self):
#         self._driver.close()

#     def print_greeting(self, message):
#         with self._driver.session() as session:
#             greeting = session.write_transaction(self._create_and_return_greeting, message)
#             print(greeting)

#     @staticmethod
#     def _create_and_return_greeting(tx):
#         result = tx.run("CREATE (a:Greeting) "
#                         "SET a.message = $message "
#                         "RETURN a.message + ', from node ' + id(a)", message=message)
#         return result.single()[0]


driver1 = GraphDatabase.driver("bolt://bazy.flemingo.ovh:7687", auth=("neo4j", "marcjansiwikania"))

def create_subjects(tx, filename, faculty_name):
    infile = open(filename, "r")
    csvimport = csv.reader(infile)
    for row in csvimport:
        print(row[0])
        result = tx.run("MATCH (n:Subject { name : $name }) RETURN n", name=row[0])
        if not result.single():
            tx.run("CREATE (a:Subject) SET a.name = $name", name=row[0])
            tx.run("MATCH (a:Subject { name : $name }),(b:Faculty { name : $faculty }) CREATE (a)-[r:BelongsTo]->(b)", name=row[0], faculty=faculty_name)
        else:
            tx.run("MATCH (a:Subject { name : $name }),(b:Faculty { name : $faculty }) CREATE (a)-[r:BelongsTo]->(b)", name=row[0], faculty=faculty_name)

def create_tutors(tx, faculty_name):
    infile = open("wykladowcy.csv", "r")  
    csvimport = csv.reader(infile)
    for row in csvimport:
        print(row[0])
        tx.run("CREATE (a:Tutor) SET a.firstname = $firstname, a.lastname = $lastname, a.mail = $mail, a.degree = $degree", firstname=row[1], lastname=row[0], mail=row[3], degree=row[2])
        tx.run("MATCH (a:Tutor { firstname: $firstname, lastname: $lastname}), (b:Faculty { name : $faculty }) CREATE (a)-[r:WorksIn]->(b)")
        subjectnum = tx.run("MATCH (a:Faculty { name = $faculty}) WITH count(a) AS value RETURN value", faculty=faculty_name).single()[0]
        
        numberofsubjects = randint(1,4)
        for i in range(numberofsubjects):
            randomnum = randint(0, subjectnum)
            subjects = tx.run("MATCH (a:Subject { faculty : $faculty})", faculty=faculty_name)
            subject = subjects[randomnum]
        

with driver1.session() as session:
    session.write_transaction(create_subjects, "przedmioty.csv", "Informatyki")
    session.write_transaction(create_subjects, "przedmioty2.csv", "Elektroniki")
    session.write_transaction(create_subjects, "przedmioty3.csv", "Fizyki Medycznej")