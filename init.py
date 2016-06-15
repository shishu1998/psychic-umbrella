import os
from flask import Flask, render_template, session, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask import send_from_directory
import database

UPLOAD_FOLDER = os.path.dirname(__file__) + '/static/images/'
ALLOWED_EXTENSIONS = set(['PNG', 'png', 'jpg', 'jpeg', 'gif'])
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
    return 'log' in session
    
@app.route("/", methods = ['GET','POST'])
@app.route("/index", methods = ['GET', 'POST'])
def index():
    return redirect(url_for("map",empire="World"))

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
            if database.update(form['old'],form['new'], form['new2']):
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
        session.clear()
    return redirect(url_for('index'))
        
#Archive Page
#Gets All Empires from MongoDB Database and sets Emps variable in archive.html
#to an array of empire names (Strings)
#Renders archive.html
@app.route("/archive", methods = ['GET','POST'])
def archive():
    Emps = database.getEmpires()
    return render_template("archive.html", Emps = Emps, data = "empires", logged = verify())

@app.route("/<empire>/archive")
def archive2(empire=''):
    Maps = database.getMaps(empire)
    return render_template("archive.html", emp = empire, Emps = database.getEmpires(), Maps = Maps, data = "maps", logged = verify())

#Adding an empire
@app.route("/addEmpire", methods =['GET','POST'])
def add():
    if request.method == "POST":
        form = request.form
        empire = form['empire']
        database.addEmpire(empire)
        path = upload_file()
        if(path == "/" or path is None):
            path = form['link']
        if(path is None):
            return redirect(url_for("add"))
        if (RepresentsInt(form['start']) and RepresentsInt(form['end'])):
            if (form['start'] == form['end']):
                database.addMap(empire,form['start'],path,form['tag'])
            else:
                database.addMap(empire,form['start'],path,form['tag'])
                database.addMap(empire,form['end'],path,form['tag'])
        elif (RepresentsInt(form['start'])):
            database.addMap(empire,form['start'],path,form['tag'])
        elif (RepresentsInt(form['end'])):
            database.addMap(empire,form['end'],path,form['tag'])

        return redirect(url_for("index"))
    else:
         return render_template("data.html", data = "empires", Emps = database.getEmpires(),logged = verify())

#Removing an empire
@app.route("/removeEmpire/<emp>")
def removeEmpire(emp=''):
    database.rmvEmpire(emp)
    return redirect(url_for("archive"))

@app.route("/map/<empire>", methods=['GET','POST'])
def map(empire=''):
    maps = database.getMaps(empire)
    if not maps is None:
        links = []
        dates = []
        tags = []
        for x in maps:
            dates.append(x['date'])
            links.append(x['image'])
            tags.append(x['tag'])
    return render_template("map.html", link=links, date=dates,Emps=database.getEmpires(), tag=tags,empire=empire, logged = verify())

#Adding a map to an empire
@app.route("/addMap/<empire>", methods =['GET','POST'])
def addMap(empire=''):
    if request.method =="POST":
        form = request.form
        path = upload_file()
        if(path == "/" or path is None):
            path = form['link']
        if(path is None):
            return redirect(url_for("addMap", empire=empire))
        if (form['start'] == form['end']):
            database.addMap(empire,form['start'],path,form['tag'])
        else:
            database.addMap(empire,form['start'],path,form['tag'])
            database.addMap(empire,form['end'],path,form['tag'])
        return redirect(url_for("archive2", empire=empire))
    else:
        return render_template("data.html", data = "maps",Emps=database.getEmpires(), logged = verify())

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
        path = upload_file()
        database.updateMap(empire,date,form['newDate'],path,form['newTag'])
        return redirect(url_for("map", empire=empire))
    else:
        return render_template("data.html", data = "date", Emps = database.getEmpires(),logged=verify())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return None
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return None
    filepath = os.path.dirname(__file__) + "static/images/" + file.filename
    if os.path.isfile(filepath):
        return url_for("static",filename= "images/"+file.filename)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return url_for("static",filename="images/"+filename)
    return None
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return os.path.dirname(__file__) + send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
       
if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', port=8000)
