
#Imported Stuff for Activating Database
from pymongo import MongoClient
from hashlib import sha512
import json
#Hidden Password
hidden =""
salt =""

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
    c[continent].remove({'empire-name':empireName})

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
    print d
    c[empName].insert(d)
    #print c[empName].find_one('date': date)

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
    if new_date is None:
        c[empireName].update({'date':old_date},{"$set":{'image':new_link}})
    elif new_link is None:
        c[empireName].update({'date':old_date},{"$set":{'date':new_date}})
    elif new_data is None and new_link is None:
        return
    else:
        c[empireName].update({'date':old_date},{"$set":{'date':new_date,'image':new_link}})

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
       # print x
        d[x['date']] = x['image']
        array.append(d)
        d = {}
    #Return the Dictionary
    
    #print array
    return array
"""
addMap("China","2222","http://cdn.playbuzz.com/cdn/b9792862-7151-446f-95bf-56ab4ecc4cd8/dec57bda-3c22-4887-99ac-de17b0539f36.jpg")
addMap("China","1111","http://ohrubbishblog.com/wp-content/uploads/2015/08/Scooby-Doo-6.jpg")
addMap("China","4444","http://vignette1.wikia.nocookie.net/villainstournament/images/9/96/Scooby_Doo.png/revision/latest?cb=20151026140949")
addMap("China","3333","http://vignette3.wikia.nocookie.net/hanna-barbera/images/2/24/Scoobydoo.jpg/revision/latest?cb=20090921172226")
print getMaps("China")
"""
def rmvMap(empire, date):
    connection = MongoClient()
    c = connection['data3']
    c[empire].remove({'date':date})

#For hiding the password
def regPass(password):
    salt = uuid4().hex
    hashvalue = sha512((password + salt)*10000).hexdigest()
    hidden = hashvalue

#Authenticating the password
def authenticate(password):
    if (sha512((password + salt)*10000).hexdigest() == hidden):
        return True
    return False

#addEmpire("NA","United States")
#addEmpire("NA","Canadia")
#addEmpire("NA","Aztecs")
#addEmpire("OC","Australia")
#addEmpire("OC","Aboriginalies")
#addEmpire("EU","Great Britania")
#addEmpire("EU","Francia")
#addEmpire("EU","GERMANIA")
#addEmpire("AF","ZuLu")
#addEmpire("AF","South Africa")
