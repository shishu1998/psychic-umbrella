
from pymongo import MongoClient

def addMap(empireName, date, image):
    #Establish Connection
    connection = MongoClient()
    c = connection['data']
    empName = empireName
    #Create the new row
    d = {'date':date,
         'image-link':image,
        }
    #Add it to the Empire?
    c[empName].insert(d)

def getMaps(empireName):
    #Establish Connection
    connection = MongoClient()
    c = connection['data']
    empName = empireName
    #Get Everything and put it in a dictionary
    d = {}
    for x in c[empName].find():
        d[x.date] = x.image
    #Return the Dictionary
    return d
    
