from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

#Etusivu: Etusivulta siirrytään sisäänkirjautumiseen tai rekisteröitymiseen.
@app.route("/", methods=["GET", "POST"])
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
	sql = "SELECT pass FROM users WHERE name=:username"
	result = db.session.execute(sql, {"username":username})
	ps = result.fetchone()
	if ps == None:
		#Tunnusta ei ole
		return redirect("/login/bad")
	else:
		hash_value = ps[0]
		if check_password_hash(hash_value, password):
			#Oikea tunnus ja salasana
			session["username"] = username
			return redirect("/lista")
		else:
			#Väärä salasana
			return redirect("/login/bad")

#login/bad: Kirjautuminen epäonnistui
@app.route("/login/bad", methods=["POST", "GET"])
def loginbad():
	return render_template("loginbad.html")

#logout: Toteuttaa uloskirjautumisen
@app.route("/logout", methods=["POST"])
def logout():
	del session["username"]
	return redirect("/")

#Rekisteröityminen: Tällä sivulla käyttäjä syöttää tunnuksen ja salasanan rekisteröitymistä varten
@app.route("/register", methods=["GET", "POST"])
def register():
	return render_template("register.html")

#register/redirect: Toteuttaa rekisteröitymisen
@app.route("/register/redirect", methods=["GET","POST"])
def registerredirect():
	reguser = request.form["reguser"]
	regpass = request.form["regpass"]
	if not reguser or not regpass:
		return redirect("/register/emptyfield")
	sql1 = "SELECT name FROM users WHERE name=:reguser"
	result = db.session.execute(sql1, {"reguser":reguser})
	regu = result.fetchone()
	if regu == None:
		hash_value = generate_password_hash(regpass)
		sql2 = "INSERT INTO users(name,pass,created,status,perms) VALUES(:reguser,:password,LOCALTIMESTAMP,3,'luser')"
		db.session.execute(sql2, {"reguser":reguser,"password":hash_value})
		db.session.commit();
		return redirect("/register/success")
	else:
		return redirect("/register/nametaken")

#register/nametaken: Sivu, jonne käyttäjä ohjautuu yrittäessään rekisteröidä käytössä olevaa käyttäjänimeä
@app.route("/register/nametaken", methods=["GET","POST"])
def nametaken():
	return render_template("nametaken.html")

#register/emptyfield: Sivu, jonne käyttäjä ohjautuu jos käyttäjänimi tai salasana-kenttä on tyhjä
@app.route("/register/emptyfield")
def emptyfield():
	return render_template("emptyfield.html")

#register/success: Ilmoittaa käyttäjälle rekisteröinnin onnistumisesta
@app.route("/register/success", methods=["GET","POST"])
def registersuccess():
	return render_template("registersuccess.html")

#Lista: Sisältää listan pelisaleista, klikkaamalla salia pääsee salin sivulle
#TODO: Kaikki, sivu tällä hetkellä placeholder
@app.route("/lista", methods=["GET","POST"])
def lista():
	saliote = db.session.execute("SELECT name FROM locations")
	salit = saliote.fetchall()
	return render_template("lista.html", salit=salit)

#Salisivu: Näyttää käyttäjälle salissa olevat pöydät, käyttäjä voi tästä liittyä pöydän jonoon
@app.route("/lista/<string:salinnimi>", methods =["GET","POST"])
def salinnimi(salinnimi):
	sql = "SELECT id FROM locations WHERE name=:salinnimi"
	result = db.session.execute(sql, {"salinnimi":salinnimi}).fetchone()
	salid = result[0]
	sql2 = "SELECT * FROM tables WHERE location_id=:salid"
	resu2 = db.session.execute(sql2, {"salid":salid})
	poytalista = resu2.fetchall()
	return render_template("salinnimi.html", salinnimi=salinnimi, poytalista=poytalista)

#lista/table_id: Toteuttaa liittymisen
#TODO Tarkistus, onko käyttäjä jo jonossa ko. pöytään
@app.route("/lista/poyta/<string:tableid>", methods =["GET","POST"])
def tableid(tableid):
	name = session.get("username")
	sql = "SELECT id FROM users WHERE name=:name"
	result = db.session.execute(sql, {"name":name}).fetchone()
	userid = result[0]
	sql2 = "INSERT INTO queue(user_id,table_id,inqueue,arrived) VALUES(:userid,:tableid,TRUE,LOCALTIMESTAMP)"
	db.session.execute(sql2, {"userid":userid,"tableid":tableid})
	db.session.commit();
	sql3 = "SELECT COUNT(*) FROM queue WHERE table_id=:tableid AND inqueue=TRUE"
	result = db.session.execute(sql3, {"tableid":tableid}).fetchone()
	place = result[0]
	sql4 = "SELECT name FROM tables WHERE id=:tableid"
	result = db.session.execute(sql4, {"tableid":tableid}).fetchone()
	tablename = result[0]
	return render_template("tableid.html", name=name, tablename=tablename, place=place)
