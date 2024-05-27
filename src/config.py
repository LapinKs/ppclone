from neo4j import GraphDatabase

URI = "bolt://localhost:7999"
USERNAME = "neo4j"
PASSWORD = "password"
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
