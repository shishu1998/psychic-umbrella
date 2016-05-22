from flask import Flask, render_template, session, request
from flask import redirect, url_for
from pymongo import MongoClient
import database

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return render_template("data.html")

@app.route("/map/<empire>", methods=['GET','POST'])
def map(empire=''):
    str=''
    maps = database.getMaps(empire)
    if not maps is None:
        print maps
        links = ''
        dates = ''
        for ind in range(0,len(maps)):
            links += '"<img src="'+ maps[ind].keys()[0] + '" height="42" width="42" class="map"> '
            dates += maps[ind].values()[0] + ' '
        links += "/"    
        return render_template("map.html", map=str, date=dates, empire=empire)

if __name__ == "__main__":
    app.secret_key = "plsfortheloveofgodletthiswork"
    app.debug = True
    app.run('0.0.0.0', port=8000)
