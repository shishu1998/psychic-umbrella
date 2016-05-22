from flask import Flask, render_template, session, request
from flask import redirect, url_for
from pymongo import MongoClient
import database.py

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return render_template("data.html")

@app.route("/map/<empire>", methods=['GET','POST'])
def map(empire=''):
    conn = MongoClient()
    c = connection['data2']
    str=''
    if not c[empire] is None:
        for link in maps:
            str+= '"<img src="'+ link + '" height="42" width="42" class="map">'
    return render_template("map.html", map=str, empire=empire)

if __name__ == "__main__":
    app.secret_key = "plsfortheloveofgodletthiswork"
    app.debug = True
    app.run('0.0.0.0', port=8000)
