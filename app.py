from flask import Flask, render_template, session, request
from flask import redirect, url_for

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key = "plsfortheloveofgodletthiswork"
    app.debug = True
    app.run('0.0.0.0', port=8000)
