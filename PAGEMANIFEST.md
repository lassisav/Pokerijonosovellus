*Sisällölliset sivut*

 - Etusivu:					/					Tehty, testattu  
 - Sisäänkirjautuminen:				/login					Tehty, testattu  
 - Rekisteröinti:				/register				Tehty, testattu  
 - Lista pelisaleista:				/lista					Tehty ja testattu, salikohtainen pöytätilanne puuttuu
 - Pelisalin sivu:				/lista/<salinnimi>			Tehty, testattu
 - Kontrollisivu:				/control				Osittain tehty (toiminnot joihin ei kuulu pöytätietojen muokkaaminen), tehdyt toiminnot testattu 
 - Ylläpitosivu:				/admin					Tehty, testattu
 - Ylläpitäjä, käyttäjän lisäys:		/admin/addUser				Tehty, testattu
 - Ylläpitäjä, käyttäjän poisto:		/admin/removeUser			Tehty, testattu
 - Ylläpitäjä, salin lisäys:			/admin/addLocation			Tehty, testattu
 - Ylläpitäjä, salin poisto:			/admin/removeLocation			Tehty, testattu
 - Ylläpitjä, käyttäjoikeuksien muokkaaminen	/admin/editUser				Tehty, testattu  
 - Rekisteröinti onnistui:			/register/success			Tehty, testattu  
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
 - Ylläpitäjä, käyttäjäoikeuksien muokkaaminen:	/admin/editUser/redirect		Tehty, testattu
 - Jonoon liittyminen:				/lista/poyta/<tableid>			Tehty, testattu

*.html-pohjat*  
  
 - /						index.html				Tehty, testattu  
 - /register					register.html				Tehty, testattu  
 - /lista					lista.html				Esiversio tehty ja testattu, joitakin suunniteltuja ominaisuuksia puuttuu  
 - /lista/<salinnimi>				salinnimi.html				Tehty, testattu
 - /control					control.html				Tehty, testattu
 - /control					nopermission.html			Tehty, testattu  
 - /admin					admin.html				Tehty, testattu  
 - /admin/addUser				addUser.html				Tehty, testattu
 - /admin/removeUser				removeUser.html				Tehty, testattu
 - /admin/addLocation				addLocation.html			Tehty, testattu
 - /admin/removeLocation			removeLocation.html			Tehty, testattu
 - /admin/editUser				editUser.html				Tehty, testattu
 - /login					login.html				Tehty, testattu    
 - /register/success				registersuccess.html			Tehty, testattu 
 - /control/arrival/<tableid>			arrival.html				Tehty, testattu
 - Layout-pohja pelaajille			layout.html				Tehty, testattu
 - Layout-pohja työntekijöille			employeelayout.html			Ei tehty
 - Layout-pohja ylläpitäjille			adminlayout.html			Tehty, testattu, poislukien control-sivuston implementaatio
