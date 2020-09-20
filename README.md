# Tietokantasovellus-harjoitustyö

***Lassi Savolainen***

**Pokerijonosovellus**

 - Heroku: pokerijonosovellus.herokuapp.com

*Sovelluksen tarkoitus*

 - Sovelluksella hallinoidaan pokeripöytien, jotka on jaoiteltu toimipisteittäin (kutsutaan pelisaleiksi), pelaajatilannetta, jonotusta ja jonosta pöytään siirtymistä
 - Käyttäjälle sovellus näyttää pöytätilanteet pelisaleittain. Käyttäjä voi sovelluksen kautta liittyä pöytään/jonoon
 - Työntekijä pitää sovelluksen avulla kirjaa pöytätilanteista, siirtää käyttäjiä jonosta pöytään, sekä voi lisätä ja poistaa pöytiä

*Sovelluksen sisältö*

 - Sovellus näyttää käyttäjille pöytien jonotustilanteen, joko vapaiden paikkojen määrän tai jonon pituuden
 - Käyttäjä voi liittyä yhden tai useamman pöydän jonoon
 - Sovelluksessa näkyy jonotustilanne, pöytäpaikan vapautuessa jonon ensimmäinen siiretään saapuviin pelaajiin
 - Työntekijä voi vapauttaa paikan pöydästä, jolloin jonon ensimmäinen siirtyy saapuviin pelaajiin
 - Työntekijä poistaa käyttäjän saapuvista pelaajista
 - Työntekijä voi poistaa käyttäjiä myös itse jonosta
 - Ylläpitäjä ja työntekijä voivat lisätä ja poistaa pöytiä
 - Ylläpitäjä voi poistaa käyttäjiä
 - Ylläpitäjä ja työntekijä voivat luoda työntekijä-tilejä
 - Käyttäjä saa ilmoituksen kun hänet siirretään saapuviin pelaajiin, tai hänet poistetaan jonosta

*Sovellukseen jo toteutetut ominaisuudet*

 - Sovelluksen tietokantarakenne
 - Käyttäjän rekisteröityminen ja kirjautuminen sivulle
 - Listasivulta siirtyminen salikohtaisille sivuille
 - Käyttäjän liittyminen jonoon
 - Oikeuksien tarkistaminen työntekijöiden ja ylläpitäjien sivuilla
 - Pöydässä olevien pelaajien määrän päivittäminen

*Sovellukseen toteutettavat, vielä puuttuvat ominaisuudet*

 - Jonosijan näyttäminen käyttäjälle
 - Liittymään pääsyn näyttäminen käyttäjälle
 - Käyttäjän poistuminen jonoista
 - Jonottajien tietojen näyttäminen työntekijälle kontrollisivulla
 - Työntekijän toiminto siirtää käyttäjiä jonosta valmistautumaan ja valmistautumasta pöytään
 - Työntekijän toiminto poistaa ja muokata pöytiä
 - Ylläpitäjän toiminnot

*Etusivu*

 - Etusivulla käyttäjä voi kirjautua sisään ja rekisteröityä
 - Sisäänkirjautunut käyttäjä ohjataan Listasivulle
 - Sisäänkirjautunut työntekijä ohjataan Kontrollisivulle
 - Sisäänkirjautunut ylläpitäjä ohjataan Ylläpitosivulle

*Listasivu*

 - Listasivulla on lista pelisaleista (Nimi, avoimet pöydät)
 - Käyttäjä pääsee pelisalin nimeä klikkaamalla ko. salin omalle sivulle

*Pelisalin oma sivu*

 - Salin sivulla käyttäjä näkee tarkemmat tiedot kustakin pöydästä (Peli, panostaso, senhetkinen ja maksimipelaajamäärä, jonon pituus)
 - Salin sivulla pöytää klikkaamalla käyttäjä ilmoittautuu jonoon
 - Jonossa olevat käyttäjät näkevät jonotustilanteensa sovelluksen jokaisella sivulla

*Pöytäpaikan vapautuessa*

 - Käyttäjän saadessa paikan pöydästä, tämä ilmoitetaan hänelle jokaisella sovelluksen sivulla
 - Työntekijä vahvistaa käyttäjän saapumisen/saapumatta jättämisen poistamalla tämän vapautuvalta paikalta

*Kontrollisivu*

 - Työntekijä näkee omien saliensa pöytien tilanteet (samat kuin pelisalin omalla sivulla), sekä jonossa olevat käyttäjät
 - Työntekijä voi avata ja sulkea pöytiä
 - Työntekijä voi ilmoittaa järjestelmälle vapautuneesta paikasta, jolloin jonon ensimmäinen käyttäjä siirtyy saapuviin pelaajiin
 - Työntekijä näkee saapuvat pelaajat, sekä ajan jonka he ovat olleet saapumassa
 - Työntekijä poistaa käyttäjän saapuvista pelaajista tietyn ajan jälkeen/heidän liittyessä pöytään

*Ylläpitosivu*

 - Ylläpitäjä voi lisätä ja poistaa käyttäjiä, työntekijöitä ja ylläpitäjiä
 - Ylläpitäjä voi lisätä ja poistaa pelisaleja
 - Ylläpitäjä voi käyttää kaikkien pelisalien kontrollisivuja
