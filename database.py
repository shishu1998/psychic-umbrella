from pymongo import MongoClient
from hashlib import sha512
hidden =""
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

def regPass(password):
    salt = uuid4().hex
    hashvalue = sha512((password + salt)*10000).hexdigest()
    hidden = hashvalue

    
