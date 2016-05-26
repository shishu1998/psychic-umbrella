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
def index():
    Conts = {}
    Conts["AF"] = database.getEmpires("AF")
    Conts["AS"] = database.getEmpires("AS")
    Conts["EU"] = database.getEmpires("EU")
    Conts["NA"] = database.getEmpires("NA")
    Conts["OC"] = database.getEmpires("OC")
    Conts["SA"] = database.getEmpires("SA")
    return render_template("index.html", Conts=Conts )

#Editing Page
#Work in Progress
@app.route("/edit", methods =['GET','POST'])
def edit():
    if request.method == "POST":
        form = request.form
        button = form['button']
        if button == "Add":
            database.addMap(form['empireName'],form['date'],form['link'])
            return redirect(url_for("index"))
    return render_template("data.html")

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

#Renders the page for an empire depending on the empire name
@app.route("/<empire>", methods=['GET'])
def empire(empire=""):
    return render_template("empire.html", empire=empire);

if __name__ == "__main__":
    app.secret_key = "plsfortheloveofgodletthiswork"
    app.debug = True
    app.run('0.0.0.0', port=8000)
