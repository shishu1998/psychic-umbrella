import os
from flask import Flask, render_template, session, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask import send_from_directory
import database

UPLOAD_FOLDER = os.path.dirname(__file__) + '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#max size of 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(24)
#Home Page
#Gets Empires from MongoDB Database and sets Conts variable in index.html to
#a dictionary in the format {<Continent>:<Empire>}
#Renders index.html

def verify():
    if 'log' in session:
        return session['log'] == 'verified'
    else:
        session['log'] = 'unverified'
        return False
    
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
    return render_template("index.html", Conts=Conts, logged = verify())

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', logged = False)
    if request.method == 'POST':
        form = request.form
        pword = form['password']
        if database.authenticate(pword):
            session['log'] = 'verified'
            return redirect(url_for('index'))
        else:
            return render_template('login.html',logged = False, err="Incorrect Password")
@app.route('/change', methods = ['GET', 'POST'])
def change():
    if verify():
        if request.method == 'POST':
            form = request.form
            if database.update(form['old'],form['new']):
                return redirect(url_for('index'))
            else:
                return render_template('change.html', logged = verify(), wrong = "yes", err = "Incorrect Password")
        else:
            return render_template('change.html', logged = verify())
    else:
        return render_template('change.html',logged=verify())
@app.route('/logout')
def logout():
    if verify():
        session['log'] = "unverified"
    session['action'] = "Logged Out"
    return redirect(url_for('index'))
        
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
    return render_template("archive.html", Emps = Emps, data = "empires", logged = verify())

@app.route("/<empire>/archive")
def archive2(empire=''):
    Maps = database.getMaps(empire)
    return render_template("archive.html", emp = empire, Maps = Maps, data = "maps", logged = verify())

#Adding an empire
@app.route("/addEmpire", methods =['GET','POST'])
def add():
    if request.method == "POST":
        form = request.form
        empire = form['empire']
        cont = form['continents']
        database.addEmpire(cont,empire)
        if (RepresentsInt(form['start']) and RepresentsInt(form['end'])):
            if (form['start'] == form['end']):
                database.addMap(empire,form['start'],form['link'])
            else:
                database.addMap(empire,form['start'],form['link'])
                database.addMap(empire,form['end'],form['link'])
        elif (RepresentsInt(form['start'])):
            database.addMap(empire,form['start'],form['link'])
        elif (RepresentsInt(form['end'])):
            database.addMap(empire,form['end'],form['link'])

        return redirect(url_for("index"))
    else:
         return render_template("data.html", data = "empires", logged = verify())

#Removing an empire
@app.route("/removeEmpire/<cont>/<emp>")
def removeEmpire(cont='',emp=''):
    database.rmvEmpire(cont,emp)
    return redirect(url_for("archive"))

@app.route("/map/<empire>", methods=['GET','POST'])
def map(empire=''):
    maps = database.getMaps(empire)
    if not maps is None:
        links = ''
        dates = ''
        for ind in range(0,len(maps)):
            links += maps[ind].values()[0] + ' '
            dates += maps[ind].keys()[0] + ' '
    return render_template("map.html", link=links, date=dates, empire=empire, logged = verify())

#Adding a map to an empire
@app.route("/addMap/<empire>", methods =['GET','POST'])
def addMap(empire=''):
    if request.method =="POST":
        form = request.form
        if (form['start'] == form['end']):
            database.addMap(empire,form['start'],form['link'])
        else:
            database.addMap(empire,form['start'],form['link'])
            database.addMap(empire,form['end'],form['link'])
        return redirect(url_for("archive2", empire=empire))
    else:
        return render_template("data.html", data = "maps", logged = verify())

#Removing a map from an empire
@app.route("/removeMap/<empire>/<date>", methods=['GET','POST'])
def removeMap(empire = '', date= ''):
    database.rmvMap(empire,date)
    return redirect(url_for("archive2", empire=empire))

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#Updating a map
@app.route("/editMap/<empire>/<date>/", methods=['GET','POST'])
def editMap(empire = '', date = ''):
    if request.method == "POST":
	   form = request.form
	   database.updateMap(empire,date,form['newDate'],form['newLink'])
	   return redirect(url_for("map", empire=empire))
    else:
	   return render_template("data.html", data = "date", logged=verify())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file(empire = ''):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filepath = os.path.dirname(__file__) + "/upload/" + file.filename
        if file and allowed_file(file.filename) and not os.path.isfile(filepath):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
        return redirect(url_for("archive2", empire = empire))
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return os.path.dirname(__file__) + send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
       
if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', port=8000)
