from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

#Etusivu: Etusivulta siirrytään sisäänkirjautumiseen tai rekisteröitymiseen.
@app.route("/")
def index():
	return render_template("index.html")

#Sisäänkirjautuminen: Käytetään sisäänkirjautumiseen
@app.route("/login", methods=["GET", "POST"])
def login():
	return render_template("login.html")

#login/redirect: Toteuttaa sisäänkirjautumisen
@app.route("/login/redirect", methods=["POST"])
def loginredirect():
	username = request.form["username"]
	password = request.form["password"]
	# TODO: Tarkista tunnus ja salasana
	session["username"] = username
	return redirect("/lista")

#logout: Toteuttaa uloskirjautumisen
@app.route("/logout", methods=["POST"])
def logout():
	del session["username"]
	return redirect("/")

#Rekisteröityminen: Tällä sivulla käyttäjä syöttää tunnuksen ja salasanan rekisteröitymistä varten
@app.route("/register", methods=["GET", "POST"])
def register():
	return render_template("register.html")

#Lista: Sisältää listan pelisaleista, klikkaamalla salia pääsee salin sivulle
#TODO: Kaikki, sivu tällä hetkellä placeholder
@app.route("/lista", methods=["GET","POST"])
def lista():
	return render_template("lista.html")
