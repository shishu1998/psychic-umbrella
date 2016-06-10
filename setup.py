from pymongo import MongoClient
import database
connection = MongoClient()
connection.drop_database("data3")
database.regPass("worldhistoryrules")
c = connection["data3"]
world = c["World"]