
#Imported Stuff for Activating Database
from pymongo import MongoClient
from hashlib import sha512
import json
from uuid import uuid4
import os
#Hidden Password
random ="User"


#Add Empire
def addEmpire(empireName):
    connection = MongoClient()
    c = connection['data3']
    d = {'empire-name':empireName}
    c.empires.insert(d)
    
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
        if os.path.isfile(str(x['image'])[1:]):
            os.remove(str(x['image'])[1:])
    c[empireName].drop()
    c.empires.delete_one({'empire-name':empireName})

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
    if empName == "" or date == "" or image == "":
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
    if new_date == "":
        new_date = None
    if new_link == "":
        new_link = None
    for x in c[empireName].find({'date':old_date}):
        path = str(x['image'])
    if new_date is None and new_link is None:
        return       
    elif new_date is None:
        print "here"
        c[empireName].update({'date':str(old_date)},{"$set":{'image':new_link}})
        if c[empireName].find({'image':path}).count() == 0:
            if os.path.isfile(path[1:]):
                os.remove(path[1:])    
    elif new_link is None:
        c[empireName].update({'date':str(old_date)},{"$set":{'date':new_date}})
    else:
        print "here2"
        c[empireName].update({'date':str(old_date)},{"$set":{'date':new_date,'image':new_link}})
        if c[empireName].find({'image':path}).count() == 0:
            if os.path.isfile(path[1:]):
                os.remove(path[1:])   
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
    for x in c[empire].find({'date':date}):
        path = str(x['image'])
    c[empire].delete_one({'date':date})
    print path[1:]
    print c[empire].find({'image':path}).count()
    if c[empire].find({'image':path}).count() == 0:
        print "BOOOO"
        if os.path.isfile(path[1:]):
            print "YAAAY"
            os.remove(path[1:])

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
