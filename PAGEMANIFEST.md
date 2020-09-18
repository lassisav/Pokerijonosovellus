*Sisällölliset sivut*

 - Etusivu:		/				Tehty, testattu  
 - Sisäänkirjautuminen:	/login				Tehty, testattu  
 - Rekisteröinti:	/register			Tehty, poislukien salasanan vahvistus -kentän toteutus, testattu  
 - Lista pelisaleista:	/lista				Esiversio tehty ja testattu, joitakin suuniteltuja ominaisuuksia puuttuu
 - Pelisalin sivu:	/lista/<salinnimi>		Tehty, testattu
 - Kontrollisivu:	/control			Osittain tehty (toiminnot joihin ei kuulu jonotus tai pöytätietojen muokkaaminen), tehdyt toiminnot testattu 
 - Ylläpitosivu:	/admin				Ei aloitettu  
 - Käyttäjän lisäys:	/admin/addUser			Ei aloitettu  
 - Käyttäjän poisto:	/admin/removeUser		Ei aloitettu  
 - Salin lisäys/poisto:	/admin/saliPoistaLisaa		Ei aloitettu  
 - Käyttäjänimi käytössä:	/register/nametaken	Tehty, testattu  
 - Rekisteröinti onnistui:	/register/success	Tehty, testattu  
 - Kirjautuminen epäonnistui:	/login/bad		Tehty, testattu  
 - Jonoon liittyminen:	/lista/poyta/<tableid>		Tehty, testattu
 - Tyhjä kenttä:	/register/emptyfield		Tehty, testattu
 - Jonossa jo:		/queuefail			Tehty, testattu

*Redirect-sivut*  
  
 - Pöydän avaaminen:	/control/open/tableid		Tehty, testattu
 - Pöydän sulkeminen:	/control/close/tableid		Tehty, testattu  
 - Salista pöytään:	/control/join/tableid		Tehty, testattu
 - Jonosta saapuviin:	/next				Ei aloitettu  
 - Saapuvista pöytään:	/arrival			Ei aloitettu 
 - Pöydästä pois	/control/remove/tableid		Tehty, testattu
 - Sisäänkirjautuminen:	/login/redirect			Tehty, testattu  
 - Uloskirjautuminen :  /logout				Tehty, testattu  
 - Rekisteröityminen:	/register/redirect		Tehty, testattu
    
*.html-pohjat*  
  
 - /			index.html                      Tehty, testattu  
 - /register		register.html                   Tehty, posilukien salasanan vahvistus -kentän toteutus, testattu  
 - /lista		lista.html                      Esiversio tehty ja testattu, joitakin suunniteltuja ominaisuuksia puuttuu  
 - /lista/<salinnimi>	salinnimi.html                  Tehty, testattu
 - /control		control.html                    Osittain tehty, tehdyt toiminnot testattu
 - /control		nopermission.html		Tehty, testattu  
 - /admin		admin.html                      Ei aloitettu  
 - /admin/addUser	addUser.html                    Ei aloitettu  
 - /admin/removeUser	removeUser.html			Ei aloitettu  
 - /admin/saliPoistaLisaa	saliPoistaLisaa.html	Ei aloitettu  
 - /login			login.html		Tehty, testattu  
 - /register/nametaken	nametaken.html			Tehty, testattu  
 - /register/success	registersuccess.html		Tehty, testattu 
 - /login/bad		loginbad.html			Tehty, testattu  
 - /lista/poyta/<tableid>	tableid.html		Tehty, testattu
 - /register/emptyfield	emptyfield.html			Tehty, testattu
 - /queuefail		queuefail.html			Tehty, testattu
