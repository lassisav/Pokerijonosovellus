*Sisällölliset sivut*

 - Etusivu:					/					Tehty, testattu  
 - Sisäänkirjautuminen:				/login					Tehty, testattu  
 - Kirjautuminen epäonnistui:			/login/bad				Tehty, testattu
 - Rekisteröinti:				/register				Tehty, poislukien salasanan vahvistus -kentän toteutus, testattu  
 - Lista pelisaleista:				/lista					Tehty ja testattu, salikohtainen pöytätilanne puuttuu
 - Pelisalin sivu:				/lista/<salinnimi>			Tehty, testattu
 - Kontrollisivu:				/control				Osittain tehty (toiminnot joihin ei kuulu pöytätietojen muokkaaminen), tehdyt toiminnot testattu 
 - Ylläpitosivu:				/admin					Tehty, testattu
 - Ylläpitäjä, käyttäjän lisäys:		/admin/addUser				Tehty, testattu
 - Ylläpitäjä, käyttäjän poisto:		/admin/removeUser			Tehty, testattu
 - Ylläpitäjä, salin lisäys:			/admin/addLocation			Tehty, testattu
 - Salin poisto:				/admin/removeLocation			Tehty, testattu
 - Käyttäjoikeuksien muokkaaminen		/admin/editUser				Placeholder luotu
 - Tyhjä nimi tai salasana:			/register/emptyfield			Tehty, testattu
 - Käyttäjänimi käytössä:			/register/nametaken			Tehty, testattu  
 - Rekisteröinti onnistui:			/register/success			Tehty, testattu  
 - Kirjautuminen epäonnistui:			/login/bad				Tehty, testattu  
 - Jonoon liittyminen:				/lista/poyta/<tableid>			Tehty, testattu
 - Tyhjä kenttä:				/register/emptyfield			Tehty, testattu
 - Jonossa jo:					/queuefail				Tehty, testattu
 - Saapuvista pöytään:				/control/arrival/<tableid>		Tehty, testattu
 - Ei jonoa siirrettäessä valmistautumaan:	/control/next/fail			Tehty, testattu

*Redirect-sivut*  
  
 - Pöydän avaaminen:				/control/open/tableid			Tehty, testattu
 - Pöydän sulkeminen:				/control/close/tableid			Tehty, testattu  
 - Salista pöytään:				/control/join/tableid			Tehty, testattu
 - Jonosta saapuviin:				/control/next/tableid			Tehty, testattu
 - Jono->saapuminen epäonnistui:		/control/next/fail			Tehty, testattu
 - Pöydästä pois				/control/remove/tableid			Tehty, testattu
 - Sisäänkirjautuminen:				/login/redirect				Tehty, testattu  
 - Uloskirjautuminen:				/logout					Tehty, testattu  
 - Rekisteröityminen:				/register/redirect			Tehty, testattu
 - Saapuvan valinta:				/control/arrival/add/joinid		Tehty, testattu
 - Ylläpitäjä, käyttäjän lisäys:		/admin/addUser/redirect			Tehty, testattu
 - Ylläpitäjä, käyttäjän poisto:		/admin/removeUser/redirect		Tehty, testattu
 - Ylläpitäjä, salin lisäys:			/admin/addLocation/redirect		Tehty, testattu
 - Ylläpitäjä, salin poisto:			/admin/removeLocation/locationid	Tehty, testattu

*.html-pohjat*  
  
 - /						index.html				Tehty, testattu  
 - /register					register.html				Tehty, posilukien salasanan vahvistus -kentän toteutus, testattu  
 - /lista					lista.html				Esiversio tehty ja testattu, joitakin suunniteltuja ominaisuuksia puuttuu  
 - /lista/<salinnimi>				salinnimi.html				Tehty, testattu
 - /control					control.html				Tehty, testattu
 - /control					nopermission.html			Tehty, testattu  
 - /admin					admin.html				Tehty, testattu  
 - /admin/addUser				addUser.html				Tehty, testattu
 - /admin/removeUser				removeUser.html				Tehty, testattu
 - /admin/addLocation				addLocation.html			Tehty, testattu
 - /admin/removeLocation			removeLocation.html			Tehty, testattu
 - /admin/editUser				editUser.html				Placeholder luotu
 - /login					login.html				Tehty, testattu  
 - /register/nametaken				nametaken.html				Tehty, testattu  
 - /register/success				registersuccess.html			Tehty, testattu 
 - /login/bad					loginbad.html				Tehty, testattu  
 - /lista/poyta/<tableid>			tableid.html				Tehty, testattu
 - /register/emptyfield				emptyfield.html				Tehty, testattu
 - /queuefail					queuefail.html				Tehty, testattu
 - /control/arrival/<tableid>			arrival.html				Tehty, testattu
 - Layout-pohja pelaajille			layout.html				Tehty, testattu
 - Layout-pohja työntekijöille			employeelayout.html			Ei tehty
 - Layout-pohja ylläpitäjille			adminlayout.html			Tehty, testattu, poislukien control-sivuston implementaatio
