
#Imported Stuff for Activating Database
from pymongo import MongoClient
from hashlib import sha512
#Hidden Password
hidden =""
salt =""

#Add Map
#Takes an EmpireName, A date, and a Link to an image file as parameters
#Stores the date and image link in a table named by the empireName
def addMap(empireName, date, image):
    #Establish Connection
    connection = MongoClient()
    c = connection['data2']
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
    c = connection['data2']
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
    c = connection['data2']
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
    
    print array
    return array
    
#addMap("China","bkad","bdasd")
getMaps("China")
updateMap("China","bkad","zero")
getMaps("China")

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

    
