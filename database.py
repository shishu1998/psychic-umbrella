
#Imported Stuff for Activating Database
from pymongo import MongoClient
from hashlib import sha512
import json
from uuid import uuid4
import os
#Hidden Password
random ="User"

UPLOAD_FOLDER = os.path.dirname(__file__)
#Add Empire
def addEmpire(empireName):
    connection = MongoClient()
    c = connection['data3']
    d = {'empire-name':empireName}
    c['empires'].insert(d)
    
#Get Empires
def getEmpires():
    connection = MongoClient()
    c = connection['data3']
    array =[]
    for x in c.empires.find():
        array.append(str(x['empire-name']))
    return array
#Remove Empire
#Takes two strings, a continent abbreviation and an empire name
#Removes an empire from the continent
def rmvEmpire(empireName):
    connection = MongoClient()
    c = connection['data3']
    for x in c[empireName].find():
        if os.path.isfile(UPLOAD_FOLDER+str(x['image'][1:])):
            os.remove(UPLOAD_FOLDER+str(x['image'][1:]))
    c[empireName].drop()
    c.empires.delete_one({'empire-name':empireName})

#Add Map
#Takes an EmpireName, A date, and a Link to an image file as parameters
#Stores the date and image link in a table named by the empireName
def addMap(empireName, date, image, tag):
    #Establish Connection
    connection = MongoClient()
    c = connection['data3']
    empName = empireName
    #Create the new row

    d = {
         'date':date,
         'image':image,
         'tag':tag
        }
    #Add it to the Empire?
    if empName == "" or date == "" or image == "":
        return
    else:
        c[empName].insert(d)

#UpdateMap
#Takes an EmpireName, an old date, and an updated date/link
#Uses the old date to find the table and update it
#If only changing either date or link but not both, simply give the old date/link depending on what you are updating.
#e.g If only updating the date, put the old link for new_link. And vice versa
def updateMap(empireName,old_date,new_date=None,new_link=None,new_tag=None):
    #Establish Connection
    connection = MongoClient()
    c = connection['data3']

   
    #Update stuff
    if new_date == "":
        new_date = None
    if new_link == "":
        new_link = None
    if new_tag =="":
        new_tag = None
    path = ""
    for x in c[empireName].find({'date':old_date}):
        path = str(x['image'])
        
    if not new_link is None:
        c[empireName].update({'date':str(old_date)},{"$set":{'image':new_link}})
        if c[empireName].find({'image':path}).count() == 0:
            if os.path.isfile(UPLOAD_FOLDER+path[1:]):
                os.remove(UPLOAD_FOLDER+path[1:])
    if not new_tag is None:
        c[empireName].update({'date':str(old_date)},{"$set":{'tag':new_tag}})
    if not new_date is None:
        c[empireName].update({'date':str(old_date)},{"$set":{'date':new_date}})
#Get Maps
#Returns an array of all the maps for an empire
#The array is an array of dictionaries where the dictionary has all the dates as keys and corresponding map links as entries
def getMaps(empireName):
    #Establish Connection
    connection = MongoClient()
    c = connection['data3']
    empName = empireName
    #Get Everything and put it in a dictionary
    array = []
    
    for x in c[empName].find():
        d = {}
        for key in x:
            d[str(key)] = str(x[key])
        array.append(d)
    return array

def rmvMap(empire, date):
    connection = MongoClient()
    c = connection['data3']
    for x in c[empire].find({'date':date}):
        path = str(x['image'])
    c[empire].delete_one({'date':date})
    if c[empire].find({'image':path}).count() == 0:
        if os.path.isfile(UPLOAD_FOLDER+path[1:]):
            os.remove(UPLOAD_FOLDER+path[1:])

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

def update(old,new, new2):
    if not new == new2:
        return False
    if authenticate(old):
        connection = MongoClient()
        c = connection['data3']
        c.authent.delete_one({'uname':random})
        regPass(new)
        return True
    else:
        return False
