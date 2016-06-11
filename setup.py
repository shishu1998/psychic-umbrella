from pymongo import MongoClient
import database
import os
names = os.listdir("static/images/")
for x in names:
	os.remove("static/images/"+x)
connection = MongoClient()
connection.drop_database("data3")
database.regPass("worldhistoryrules")
c = connection["data3"]
world = c["World"]