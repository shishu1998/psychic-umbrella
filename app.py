from flask import Flask, render_template, session, request
from flask import redirect, url_for
from pymongo import MongoClient
import database

app = Flask(__name__)

#Home Page
#Gets Empires from MongoDB Database and sets Conts variable in index.html to
#a dictionary in the format {<Continent>:<Empire>}
#Renders index.html
@app.route("/", methods = ['GET','POST'])
@app.route("/index", methods = ['GET', 'POST'])
def index():
    Conts = {}
    Conts["AF"] = database.getEmpires("AF")
    Conts["AS"] = database.getEmpires("AS")
    Conts["EU"] = database.getEmpires("EU")
    Conts["NA"] = database.getEmpires("NA")
    Conts["OC"] = database.getEmpires("OC")
    Conts["SA"] = database.getEmpires("SA")
    print Conts
    return render_template("index.html", Conts=Conts )

#Archive Page
#Gets All Empires from MongoDB Database and sets Emps variable in archive.html
#to an array of empire names (Strings)
#Renders archive.html
@app.route("/archive", methods = ['GET','POST'])
def archive():
    Emps = {}
    Emps["AF"] = database.getEmpires("AF")
    Emps["AS"] = database.getEmpires("AS")
    Emps["EU"] = database.getEmpires("EU")
    Emps["NA"] = database.getEmpires("NA")
    Emps["OC"] = database.getEmpires("OC")
    Emps["SA"] = database.getEmpires("SA")
    return render_template("archive.html", Emps = Emps, data = "empires")

@app.route("/<empire>/archive")
def archive2(empire=''):
    Maps = database.getMaps(empire)
    return render_template("archive.html", Emp = empire, Maps = Maps, data = "maps")

#Adding a map to an empire
@app.route("/addMap/<empire>", methods =['GET','POST'])
def edit(empire=''):
    if request.method =="POST":
        form = request.form
        if (form['start'] == form['end']):
            database.addMap(empire,form['start'],form['link'])
        else:
            database.addMap(empire,form['start'],form['link'])
            database.addMap(empire,form['end'],form['link'])
        return redirect(url_for("index"))
    else:
        return render_template("data.html", data = "maps")

#Adding an empire
@app.route("/addEmpire", methods =['GET','POST'])
def add():
    if request.method == "POST":
        form = request.form
        print form
        empire = form['empire']
        cont = form['continents']
        database.addEmpire(cont,empire)
        if (form['start'] == form['end']):
            database.addMap(empire,form['start'],form['link'])
        else:
            database.addMap(empire,form['start'],form['link'])
            database.addMap(empire,form['end'],form['link'])
        if (form['start2'] == form['end2']):
            database.addMap(empire,form['start2'],form['link2'])
        else:
            database.addMap(empire,form['start2'],form['link2'])
            database.addMap(empire,form['end2'],form['link2'])
        return redirect(url_for("index"))
    else:
        return render_template("data.html", data = "empires")

#Removing an empire
@app.route("/removeEmpire/<cont>/<emp>")
def removeEmpire(cont='',emp=''):
    database.rmvEmpire(cont,emp)
    return redirect(url_for("archive"))

@app.route("/map/<empire>", methods=['GET','POST'])
def map(empire=''):
    maps = database.getMaps(empire)
    print maps
    if not maps is None:
        links = ''
        dates = ''
        for ind in range(0,len(maps)):
            links += maps[ind].values()[0] + ' '
            dates += maps[ind].keys()[0] + ' '
    print links
    print dates
    return render_template("map.html", link=links, date=dates, empire=empire)

if __name__ == "__main__":
    app.secret_key = "plsfortheloveofgodletthiswork"
    app.debug = True
    app.run('0.0.0.0', port=8000)
