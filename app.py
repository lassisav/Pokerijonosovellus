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


#APUFUNKTIOT:


#onkoAdmin: Funktio jolla tarkistetaan käyttäjän adminstatus
def onkoAdmin():
	name = session.get("username")
	if not name == None:
		sql = "SELECT * FROM users WHERE name=:name AND status=1"
		result = db.session.execute(sql, {"name":name}).fetchone()
		if not result == None:
			return True
	return False

#onkoTyontekija: Funktio, jolla tarkistetaan käyttäjän työntekijästatus
def onkoTyontekija():
	name = session.get("username")
	if not name == None:
		sql = "SELECT * FROM users WHERE name=:name AND status=2"
		result = db.session.execute(sql, {"name":name}).fetchone()
		if not result == None:
			return True
	return False


#SIVUT:


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
			session["message"] = "nothingtoseehere"
			if onkoAdmin():
				return redirect("/admin")
			if onkoTyontekija():
				return redirect("/control")
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
	passcheck = request.form["passcheck"]
	if regpass != passcheck:
		return render_template("register.html", error = "Salasanat eivät täsmää")
	if not reguser or not regpass:
		return render_template("register.html", error = "Syötä nimi ja salasana")
	sql1 = "SELECT name FROM users WHERE name=:reguser"
	result = db.session.execute(sql1, {"reguser":reguser})
	regu = result.fetchone()
	if regu == None:
		hash_value = generate_password_hash(regpass)
		sql2 = "INSERT INTO users(name,pass,created,status,perms) VALUES(:reguser,:password,LOCALTIMESTAMP,3,'luser')"
		db.session.execute(sql2, {"reguser":reguser,"password":hash_value})
		db.session.commit()
		return redirect("/register/success")
	else:
		return redirect("/register/nametaken")

#register/nametaken: Sivu, jonne käyttäjä ohjautuu yrittäessään rekisteröidä käytössä olevaa käyttäjänimeä
@app.route("/register/nametaken", methods=["GET","POST"])
def nametaken():
	return render_template("nametaken.html")

#register/success: Ilmoittaa käyttäjälle rekisteröinnin onnistumisesta
@app.route("/register/success", methods=["GET","POST"])
def registersuccess():
	return render_template("registersuccess.html")

#Lista: Sisältää listan pelisaleista, klikkaamalla salia pääsee salin sivulle
#TODO: Kaikki, sivu tällä hetkellä placeholder
@app.route("/lista", methods=["GET","POST"])
def lista():
	saliote = db.session.execute("SELECT L.name, (SELECT COUNT(*) FROM tables AS T WHERE T.location_id=L.id AND T.open='t') FROM locations AS L")
	salit = saliote.fetchall()
	return render_template("lista.html", salit=salit)

#Salisivu: Näyttää käyttäjälle salissa olevat pöydät, käyttäjä voi tästä liittyä pöydän jonoon
@app.route("/lista/<string:salinnimi>", methods =["GET","POST"])
def salinnimi(salinnimi):
	sql = "SELECT id FROM locations WHERE name=:salinnimi"
	result = db.session.execute(sql, {"salinnimi":salinnimi}).fetchone()
	salid = result[0]
	sql2 = "SELECT T.id,T.name,T.game,T.betsize,T.players,T.seattotal,(SELECT COUNT(Q.id) FROM queue AS Q WHERE Q.table_id=T.id AND Q.inqueue = TRUE) FROM tables AS T WHERE T.location_id=:salid ORDER BY T.id"
	resu2 = db.session.execute(sql2, {"salid":salid})
	poytalista = resu2.fetchall()
	return render_template("salinnimi.html", salinnimi=salinnimi, poytalista=poytalista)

#lista/table_id: Toteuttaa liittymisen
@app.route("/lista/poyta/<string:tableid>", methods =["GET","POST"])
def tableid(tableid):
	name = session.get("username")
	sql = "SELECT id FROM users WHERE name=:name"
	result = db.session.execute(sql, {"name":name}).fetchone()
	userid = result[0]
	sqlx = "SELECT * FROM queue WHERE (user_id=:userid AND table_id=:tableid) AND inqueue='t'"
	result = db.session.execute(sqlx, {"userid":userid,"tableid":tableid}).fetchone()
	if not result == None:
		print(result)
		return redirect("/queuefail")
	sqly = "SELECT * FROM joiners WHERE (user_id=:userid AND table_id=:tableid) AND tojoin='t'"
	result = db.session.execute(sqly, {"userid":userid,"tableid":tableid}).fetchone()
	if not result == None:
		print(result)
		return redirect("/queuefail")
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

#queuefail: Käyttäjä päätyy sivulle, jos hän on jo jonossa pöytään, jonka jonoon hän yrittää liittyä
@app.route("/queuefail")
def queuefail():
	return render_template("queuefail.html")

#control: Työntekijän käyttäjäsivu, josta työntekijä voi hallinoida pöytiä ja jonoja
#TODO: Lista työntekijän hallinnassa olevista pöydistä
#TODO: Hallinnointitoiminnot
@app.route("/control", methods=["GET","POST"])
def control():
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	msg = session["message"]
	name = session["username"]
	session["message"] = "nothingtoseehere"
	sql1 = "SELECT perms FROM users WHERE name=:name"
	result = db.session.execute(sql1, {"name":name}).fetchone()
	userperms = result[0]
	if onkoTyontekija():
		sql2 = "SELECT T.id,T.name,T.seattotal,T.players,T.location_id,T.open,T.game,T.betsize,(SELECT COUNT(*) FROM queue AS Q WHERE Q.table_id=T.id AND Q.inqueue='t'),(SELECT COUNT(*) FROM joiners AS J WHERE J.table_id=T.id AND tojoin='t'),L.name FROM tables AS T LEFT OUTER JOIN locations AS L ON (T.location_id = L.id) WHERE :userperms LIKE '%' || L.code || '%' ORDER BY T.id"
		poytalista = db.session.execute(sql2, {"userperms":userperms}).fetchall()
	if onkoAdmin():
		sql2 = "SELECT T.id,T.name,T.seattotal,T.players,T.location_id,T.open,T.game,T.betsize,(SELECT COUNT(*) FROM queue AS Q WHERE Q.table_id=T.id AND Q.inqueue='t'),(SELECT COUNT(*) FROM joiners AS J WHERE J.table_id=T.id AND tojoin='t'),L.name FROM tables AS T LEFT OUTER JOIN locations AS L ON (T.location_id = L.id) ORDER BY L.id, T.id"
		poytalista = db.session.execute(sql2).fetchall()
	sql3 = "SELECT Q.table_id,U.name,Q.arrived FROM queue AS Q LEFT OUTER JOIN users AS U ON (Q.user_id=U.id) WHERE Q.inqueue='t' ORDER BY Q.arrived"
	userlista = db.session.execute(sql3).fetchall()
	sql4 = "SELECT J.table_id,U.name,J.arrived FROM joiners AS J LEFT OUTER JOIN users AS U ON (J.user_id=U.id) WHERE J.tojoin='t' ORDER BY J.arrived"
	valmislista = db.session.execute(sql4).fetchall()
	return render_template("control.html", poytalista=poytalista, msg=msg, userlista=userlista, valmislista=valmislista)

#control/join/tableid: Toteuttaa pelaajan lisäämisen pöytään työntekijän toimesta ilman käyntiä jonossa
@app.route("/control/join/<string:tableid>", methods=["GET","POST"])
def jointable(tableid):
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sqlx = "SELECT players FROM tables WHERE id=:tableid"
	result = db.session.execute(sqlx, {"tableid":tableid}).fetchone()
	luku = result[0]
	sqly = "SELECT seattotal FROM tables WHERE id=:tableid"
	result = db.session.execute(sqly, {"tableid":tableid}).fetchone()
	total = result[0]
	if luku == total:
		session["message"] = "Pöytä täynnä, pelaajaa ei lisätty"
	else:
		sql = "UPDATE tables SET players=players+1 WHERE id=:tableid"
		db.session.execute(sql, {"tableid":tableid})
		db.session.commit()
	return redirect("/control")

#control/remove/tableid: Toteuttaa pelaajan poistamisen pöydästä
@app.route("/control/remove/<string:tableid>", methods=["GET","POST"])
def removefromtable(tableid):
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sqlx = "SELECT players FROM tables WHERE id=:tableid"
	result = db.session.execute(sqlx, {"tableid":tableid}).fetchone()
	luku = result[0]
	if luku == 0:
		session["message"] = "Pöytä tyhjä, pelaajaa ei voitu poistaa"
	else:
		sql = "UPDATE tables SET players=players-1 WHERE id=:tableid"
		db.session.execute(sql, {"tableid":tableid})
		db.session.commit()
	return redirect("/control")

#control/open/tableid: Toteuttaa pöydän avaamisen
@app.route("/control/open/<string:tableid>", methods=["GET","POST"])
def opentable(tableid):
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sql = "UPDATE tables SET open='t' WHERE id=:tableid"
	db.session.execute(sql, {"tableid":tableid})
	db.session.commit()
	return redirect("/control")

#control/close/tableid: Toteuttaa pöydän sulkemisen
@app.route("/control/close/<string:tableid>", methods=["GET","POST"])
def closetable(tableid):
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sql = "UPDATE tables SET open='f' WHERE id=:tableid"
	db.session.execute(sql, {"tableid":tableid})
	db.session.commit()
	return redirect("/control")

#control/next/tableid: Toteuttaa pelaajan siirron jonosta liittymään
@app.route("/control/next/<string:tableid>", methods=["GET","POST"])
def nextfromqueue(tableid):
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sql = "SELECT id FROM queue WHERE table_id=:tableid AND inqueue='t' ORDER BY arrived"
	result = db.session.execute(sql, {"tableid":tableid}).fetchone()
	if not result:
		return redirect("/control/next/fail")
	jonoid = result[0]
	sql1 = "SELECT user_id FROM queue WHERE id=:jonoid"
	result = db.session.execute(sql1, {"jonoid":jonoid}).fetchone()
	uid = result[0]
	sql4 = "SELECT name FROM users WHERE id=:uid"
	result = db.session.execute(sql4, {"uid":uid}).fetchone()
	uname = result[0]
	sql5 = "SELECT name FROM tables WHERE id=:tableid"
	result = db.session.execute(sql5, {"tableid":tableid}).fetchone()
	tname = result[0]
	sql2 = "UPDATE queue SET inqueue='f' WHERE id=:jonoid"
	db.session.execute(sql2, {"jonoid":jonoid})
	sql3 = "INSERT INTO joiners(user_id,table_id,tojoin,arrived) VALUES (:uid,:tableid,TRUE,LOCALTIMESTAMP)"
	db.session.execute(sql3, {"uid":uid,"tableid":tableid})
	db.session.commit()
	session["message"] = uname + " lisätty valmistautumaan pöytään: " + tname
	return redirect("/control")

#control/next/fail: Luo viestin valmistautumaan siirtämisen epäonnistumsesta johtuen siitä, että valittuun pöytään ei ole jonoa(backup, ei pitäisi olla tarpeellinen)
#TODO: kaikki
@app.route("/control/next/fail", methods=["GET","POST"])
def nextfail():
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	session["message"] = "Käyttäjää ei voitu siirtää jonosta valmistautumaan, koska jonossa ei ole yhtään käyttäjää"
	return redirect("/control")

#control/arrival/tableid: Toteuttaa pelaajan siirron valmistautumasta pöytään
@app.route("/control/arrival/<string:tableid>", methods=["GET","POST"])
def arrival(tableid):
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sqly = "SELECT players FROM tables WHERE id=:tableid"
	result = db.session.execute(sqly, {"tableid":tableid}).fetchone()
	luku = result[0]
	sqlz = "SELECT seattotal FROM tables WHERE id=:tableid"
	result = db.session.execute(sqlz, {"tableid":tableid}).fetchone()
	total = result[0]
	if luku == total:
		session["message"] = "Pelaajaa ei voida siirtää pöytään, koska pöytä on täynnä"
		return redirect("/control")
	sqlx = "SELECT COUNT(*) FROM joiners WHERE table_id=:tableid AND tojoin='t'"
	result = db.session.execute(sqlx, {"tableid":tableid}).fetchone()
	if result[0] == 1:
		sql1 = "SELECT U.name FROM joiners AS J LEFT OUTER JOIN users as U ON (J.user_id=U.id) WHERE J.table_id=:tableid AND tojoin='t'"
		result = db.session.execute(sql1, {"tableid":tableid}).fetchone()
		uname = result[0]
		sql2 = "UPDATE joiners SET tojoin='f' WHERE table_id=:tableid"
		db.session.execute(sql2, {"tableid":tableid})
		sql3 = "UPDATE tables SET players=players+1 WHERE id=:tableid"
		db.session.execute(sql3, {"tableid":tableid})
		db.session.commit()
		sql4 = "SELECT name FROM tables WHERE id=:tableid"
		result = db.session.execute(sql4, {"tableid":tableid}).fetchone()
		tname = result[0]
		session["message"] = uname + " siirtyi pöytään " + tname
		return redirect("/control")
	else:
		sql = "SELECT U.name,J.id FROM joiners AS J LEFT OUTER JOIN users AS U ON (J.user_id=U.id) WHERE J.table_id=:tableid AND tojoin='t'"
		nimilista = db.session.execute(sql, {"tableid":tableid}).fetchall()
		return render_template("arrival.html", nimilista=nimilista)

#control/arrival/add/tableid: Toteuttaa listasta valitun pelaajan siirtämisen pöytään
@app.route("/control/arrival/add/<string:joinid>", methods=["GET","POST"])
def arrivaladd(joinid):
	allow = False
	if onkoAdmin():
		allow = True
	elif onkoTyontekija():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sqly = "SELECT U.name FROM joiners AS J LEFT OUTER JOIN users AS U ON (J.user_id=U.id) WHERE J.id=:joinid"
	result = db.session.execute(sqly, {"joinid":joinid}).fetchone()
	uname = result[0]
	sqlx = "SELECT table_id FROM joiners WHERE id=:joinid"
	result = db.session.execute(sqlx, {"joinid":joinid}).fetchone()
	tableid = result[0]
	sql = "UPDATE joiners SET tojoin='f' WHERE id=:joinid"
	db.session.execute(sql, {"joinid":joinid})
	sql1 = "UPDATE tables SET players=players+1 WHERE id=:tableid"
	db.session.execute(sql1, {"tableid":tableid})
	db.session.commit()
	sql2 = "SELECT name FROM tables WHERE id=:tableid"
	result = db.session.execute(sql2, {"tableid":tableid}).fetchone()
	tname = result[0]
	session["message"] = uname + " siirtyi pöytään:  " + tname
	return redirect("/control")

#Ylläpitosivu: Näyttää ylläpitäjäkäyttäjälle ylläpitotoiminnot
@app.route("/admin", methods=["GET","POST"])
def admin():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	msg = session["message"]
	session["message"] = "nothingtoseehere"
	uname = session["username"]
	return render_template("admin.html", uname=uname, msg=msg)

#admin/addUser: Käyttäjän lisääminen ylläpitäjän toimesta
@app.route("/admin/addUser", methods=["POST","GET"])
def adminadduser():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sql = "SELECT code, name FROM locations"
	salilista = db.session.execute(sql).fetchall()
	msg = "nothingtoseehere"
	session["message"] = msg
	return render_template("adminadduser.html", salilista=salilista, msg=msg)

#admin/addUser/redirect: Toteuttaa käyttäjän lisäämisen ylläpitäjän toimesta
@app.route("/admin/addUser/redirect", methods=["POST","GET"])
def adminadduserredirect():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	reguser = request.form["reguser"]
	regpass = request.form["regpass"]
	status = int(request.form["status"])
	print(status)
	permslist = request.form.getlist("perms")
	if not permslist:
		perms = ""
		if status == 2:
			session["message"] = "Määritä työntekijälle annettavat pelisalioikeudet"
			return redirect("/admin")
	else:
		perms = ""
		for i in permslist:
			perms = perms + i
	if not reguser or not regpass:
		session["message"] = "Virheellinen käyttäjänimi tai salasana, käyttäjän luominen epäonnistui"
		return redirect("/admin")
	sql1 = "SELECT name FROM users WHERE name=:reguser"
	result = db.session.execute(sql1, {"reguser":reguser})
	regu = result.fetchone()
	if regu == None:
		hash_value = generate_password_hash(regpass)
		if status == 2:
			sql2 = "INSERT INTO users(name,pass,created,status,perms) VALUES(:reguser,:password,LOCALTIMESTAMP,2,:perms)"
			db.session.execute(sql2, {"reguser":reguser,"password":hash_value,"perms":perms})
			db.session.commit();
		elif status == 1:
			sql3 = "INSERT INTO users(name,pass,created,status,perms) VALUES(:reguser,:password,LOCALTIMESTAMP,1,'admin')"
			db.session.execute(sql3, {"reguser":reguser,"password":hash_value})
			db.session.commit();
		else:
			sql4 = "INSERT INTO users(name,pass,created,status,perms) VALUES(:reguser,:password,LOCALTIMESTAMP,3,'luser')"
			db.session.execute(sql4, {"reguser":reguser,"password":hash_value})
			db.session.commit();
		session["message"] = "Uuden käyttäjän luominen onnistui"
		return redirect("/admin")
	else:
		session["message"] = "Valittu käyttäjänimi on jo käytössä"
		return redirect("/admin")

#admin/removeUser: Käyttäjän poistaminen ylläpitäjän toimesta
@app.route("/admin/removeUser", methods=["POST"])
def adminremoveuser():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	msg = "nothingtoseehere"
	session["message"] = msg
	return render_template("adminremoveuser.html",msg=msg)

#admin/removeUser/redirect: Toteuttaa käyttäjän poistamisen ylläpitäjän toimesta
@app.route("/admin/removeUser/redirect", methods=["POST"])
def adminremoveuserredirect():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	todelname = request.form["todel"]
	sql = "SELECT id FROM users WHERE name=:todelname"
	result = db.session.execute(sql, {"todelname":todelname}).fetchone()
	todelid = result[0]
	sql1 = "SELECT table_id FROM joiners WHERE user_id=:todelid AND tojoin='t'"
	result = db.session.execute(sql1, {"todelid":todelid}).fetchall()
	if result:
		session["message"] = "Käyttäjää ei voitu poistaa, koska käyttäjä on liittymässä pöytään"
		return redirect("/admin")
	sql2 = "SELECT table_id FROM queue WHERE user_id=:todelid AND inqueue='t'"
	result = db.session.execute(sql2, {"todelid":todelid}).fetchall()
	if result:
		session["message"] = "Käyttäjää ei voitu poistaa, koska käyttäjä on jonossa pöytään"
		return redirect("/admin")
	sql3 = "DELETE FROM users WHERE id=:todelid"
	sql4 = "UPDATE users SET id=id-1 WHERE id>:todelid"
	sql5 = "UPDATE queue SET user_id=user_id-1 WHERE user_id>:todelid"
	sql6 = "UPDATE joiners SET user_id=user_id-1 WHERE user_id>:todelid"
	db.session.execute(sql3, {"todelid":todelid})
	db.session.execute(sql4, {"todelid":todelid})
	db.session.execute(sql5, {"todelid":todelid})
	db.session.execute(sql6, {"todelid":todelid})
	db.session.commit()
	session["message"] = "Käyttäjä " + todelname + " poistettiin"
	return redirect("/admin")

#admin/addLocation: Salin lisääminen ylläpitäjän toimesta
@app.route("/admin/addLocation", methods=["POST"])
def adminaddlocation():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	msg = "nothingtoseehere"
	session["message"] = msg
	return render_template("adminaddlocation.html",msg=msg)

#admin/addLocation/redirect: Toteuttaa salin lisäämisen ylläpitäjän toimesta
@app.route("/admin/addLocation/redirect", methods=["POST","GET"])
def adminaddlocationredirect():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	toaddname = request.form["toaddname"]
	toaddcode = request.form["toaddcode"]
	toaddname = toaddname.lower()
	toaddname = toaddname.capitalize()
	toaddcode = toaddcode.lower()
	if not toaddname:
		session["message"] = "Pelisalin lisääminen epäonnistui: Pelisalilla ei ollut nimeä"
		return redirect("/admin")
	if not len(toaddcode) == 4:
		session["message"] = "Pelisalin lisääminen epäonnistui: Pelisalin koodi virheellinen"
		return redirect("/admin")
	sql = "SELECT COUNT(*) FROM locations WHERE LOWER(code)=LOWER(:toaddcode) OR LOWER(name)=LOWER(:toaddname)"
	result = db.session.execute(sql, {"toaddcode":toaddcode, "toaddname":toaddname}).fetchone()
	proofcheck = result[0]
	if not proofcheck == 0:
		session["message"] = "Pelisalin lisääminen epäonnistui: Nimi tai koodi käytössä"
		return redirect("/admin")
	sql1 = "INSERT INTO locations(name,code) VALUES (:toaddname,:toaddcode)"
	db.session.execute(sql1, {"toaddcode":toaddcode, "toaddname":toaddname})
	db.session.commit()
	session["message"] = "Lisättiin sali " + toaddname + " koodilla " + toaddcode
	return redirect("/admin")

#admin/removeLocation: Salin poistaminen ylläpitäjän toimesta
@app.route("/admin/removeLocation", methods=["POST"])
def adminremovelocation():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	sql = "SELECT id,name FROM locations"
	salilista = db.session.execute(sql).fetchall()
	msg = "nothingtoseehere"
	session["message"] = msg
	return render_template("adminremovelocation.html", salilista=salilista,msg=msg)

#admin/removeLocation/locationid
@app.route("/admin/removeLocation/<string:locationid>", methods=["POST"])
def adminremovelocationredirect(locationid):
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	locationid = int(locationid)
	sql = "SELECT COUNT(*) FROM tables WHERE location_id=:locationid AND open='t'"
	result = db.session.execute(sql, {"locationid":locationid}).fetchone()
	if not result[0] == 0:
		session["message"] = "Salia ei voitu poistaa, koska salissa on auki olevia pöytiä."
		return redirect("/admin")
	sql1 = "SELECT COUNT(*) FROM joiners AS J LEFT OUTER JOIN tables AS T ON J.table_id=T.id WHERE T.location_id=:locationid AND J.tojoin='t'"
	result = db.session.execute(sql1, {"locationid":locationid}).fetchone()
	if not result[0] == 0:
		session["message"] = "Salia ei voitu poistaa, koska salissa olevaan pöytään on liittymässä pelaaja."
		return redirect("/admin")
	sql2 = "SELECT COUNT(*) FROM queue AS Q LEFT OUTER JOIN tables AS T ON Q.table_id=T.id WHERE T.location_id=:locationid AND Q.inqueue='t'"
	result = db.session.execute(sql2, {"locationid":locationid}).fetchone()
	if not result[0] == 0:
		session["message"] = "Salia ei voitu poistaa, koska salissa olevaan pöytään on jonoa."
		return redirect("/admin")
	sqlx = "SELECT name FROM locations WHERE id=:locationid"
	snimi = db.session.execute(sqlx, {"locationid":locationid}).fetchone()
	sql3 = "DELETE FROM locations WHERE id=:locationid"
	sql4 = "DELETE FROM tables WHERE location_id=:locationid"
	sql5 = "UPDATE locations SET id=id-1 WHERE id>:locationid"
	sql6 = "UPDATE tables SET location_id=location_id-1 WHERE id>:locationid"
	db.session.execute(sql3, {"locationid":locationid})
	db.session.execute(sql4, {"locationid":locationid})
	db.session.execute(sql5, {"locationid":locationid})
	db.session.execute(sql6, {"locationid":locationid})
	db.session.commit()
	session["message"] = "Poistettiin sali " + snimi[0]
	return redirect("/admin")

#admin/editUser: Työntekijän oikeuksien muokkaaminen ylläpitäjän toimesta
@app.route("/admin/editUser", methods=["POST"])
def adminedituser():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	msg = "nothingtoseehere"
	session["message"] = msg
	sql = "SELECT id,name FROM users WHERE status=2"
	nimilista = db.session.execute(sql).fetchall()
	sql1 = "SELECT code,name FROM locations"
	salilista = db.session.execute(sql1).fetchall()
	return render_template("adminedituser.html",msg=msg,nimilista=nimilista,salilista=salilista)

#admin/editUser: Toteuttaa työntekijän oikeuksien muokkaamisen
@app.route("/admin/editUser/redirect", methods=["POST"])
def adminedituserredirect():
	allow = False
	if onkoAdmin():
		allow = True
	if not allow:
		return render_template("nopermission.html")
	uid = int(request.form["tochange"])
	permslist = request.form.getlist("perms")
	perms = ""
	if not permslist:
		session["message"] = "Käyttäjäoikeuksien muokkaaminen epäonnistui: käyttäjälle ei valittu yhtään pelisalia"
		return redirect("/admin")
	for i in permslist:
		perms = perms + i
	sql = "UPDATE users SET perms=:perms WHERE id =:uid"
	db.session.execute(sql, {"perms":perms,"uid":uid})
	db.session.commit()
	sql1 = "SELECT name FROM users WHERE id=:uid"
	result = db.session.execute(sql1, {"uid":uid}).fetchone()
	session["message"] = "Muokattiin käyttäjän " + result[0] + " oikeuksia"
	return redirect("/admin")
