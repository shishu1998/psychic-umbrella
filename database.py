
#Imported Stuff for Activating Database
from pymongo import MongoClient
from hashlib import sha512
import json
from uuid import uuid4
#Hidden Password
random ="User"


#Add Empire
#Takes two strings, a continent abbreviation and an empire name
#Adds an empire to a continent collection with the key 'empire-name'
def addEmpire(continent,empireName):
    connection = MongoClient()
    c = connection['data3']
    d = {'empire-name':empireName}
    c[continent].insert(d)
    
#Get Empires
#Takes one string, the continent abbreviation
#Get the empire names of a continent in the form of a list of strings
#Returns the list of strings
def getEmpires(continent):
    connection = MongoClient()
    c = connection['data3']
    array =[]
    for x in c[continent].find():
        array.append(str(x['empire-name']))
    return array

#Remove Empire
#Takes two strings, a continent abbreviation and an empire name
#Removes an empire from the continent
def rmvEmpire(continent, empireName):
    connection = MongoClient()
    c = connection['data3']
    c[empireName].drop()
    c[continent].delete_one({'empire-name':empireName})

#Add Map
#Takes an EmpireName, A date, and a Link to an image file as parameters
#Stores the date and image link in a table named by the empireName
def addMap(empireName, date, image):
    #Establish Connection
    connection = MongoClient()
    c = connection['data3']
    empName = empireName
    #Create the new row
    d = {'date':date,
         'image':image,
        }
    #Add it to the Empire?
    if empName is None or date is None or image is None:
        return
    else:
        c[empName].insert(d)

#UpdateMap
#Takes an EmpireName, an old date, and an updated date/link
#Uses the old date to find the table and update it
#If only changing either date or link but not both, simply give the old date/link depending on what you are updating.
#e.g If only updating the date, put the old link for new_link. And vice versa
def updateMap(empireName,old_date,new_date=None,new_link=None):
    #Establish Connection
    connection = MongoClient()
    c = connection['data3']
    #Update stuff
    if new_date is None and new_link is None:
        return
    elif new_date is None:
        c[empireName].update({'date':str(old_date)},{"$set":{'image':new_link}})
    elif new_link is None:
        c[empireName].update({'date':str(old_date)},{"$set":{'date':new_date}})
    else:
        c[empireName].update({'date':str(old_date)},{"$set":{'date':new_date,'image':new_link}})

#Get Maps
#Returns an array of all the maps for an empire
#The array is an array of dictionaries where the dictionary has all the dates as keys and corresponding map links as entries
def getMaps(empireName):
    #Establish Connection
    connection = MongoClient()
    c = connection['data3']
    empName = empireName
    #Get Everything and put it in a dictionary
    d = {}
    array = []
    for x in c[empName].find():
        d[str(x['date'])] = str(x['image'])
        array.append(d)
        d = {}
    return array

def rmvMap(empire, date):
    connection = MongoClient()
    c = connection['data3']
    c[empire].delete_one({'date':date})

#For hiding the password
def regPass(password):
    connection = MongoClient()
    c = connection['data3']
    salt = uuid4().hex
    hashvalue = sha512((password + salt)*10000).hexdigest()
    d = {
        'uname':random,
        'pw':hashvalue,
        'salt':salt,}
    c.authent.insert(d)

#Authenticating the password
def authenticate(password):
    connection = MongoClient()
    c = connection['data3']
    salt = c.authent.find_one({'uname':random})['salt']
    encrypted = sha512((password + salt)*10000).hexdigest()
    if (c.authent.find_one({'uname':random})['pw'] == encrypted):
        return True
    return False

def update(old,new):
    if authenticate(old):
        connection = MongoClient()
        c = connection['data3']
        c.authent.delete_one({'uname':random})
        regPass(new)
        return True
    else:
        return False
