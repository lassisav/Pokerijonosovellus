from flask import Flask
from flask import render_template
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#Etusivu: Etusivulta siirrytään sisäänkirjautumiseen tai rekisteröitymiseen.
@app.route("/")
def index():
	return render_template("index.html")

#Sisäänkirjautuminen: Käytetään sisäänkirjautumiseen
@app.route("/login", methods=["GET", "POST"])
def login():
	return render_template("login.html")

#Rekisteröityminen: Tällä sivulla käyttäjä syöttää tunnuksen ja salasanan rekisteröitymistä varten
@app.route("/register", methods=["GET", "POST"])
def register():
	return render_template("register.html")
