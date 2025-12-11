**Kirjanvinkkisovellus**

Millainen sovellus on ja miten sitä voi testata

**Sovelluksen toiminnot**

***Käyttäjä:***
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä voi kirjautua sisään ja ulos
- Käyttäjä pystyy lisäämään sovellukseen kirjavinkkejä.
- Käyttäjä muokkaamaan ja poistamaan lisäämiään kirjavinkkejä.
- Kaikki näkevät sovellukseen lisätyt kirjavinkit.
- Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kirjavinkit.
- Käyttäjä näkee omat käyttäjäsivut, josta näkee kuinka monta arvioita hän on tehnyt
- Käyttäjät voivat kommentoida ja arvioida toisen lisättyjä kirjoja
- Kaikki pystyvät etsimään kaikkia kirjavinkkejä hakusanoilla, jotka etsivät kaikista kentistä.

***Kirjavinkit:***
- Kirjan lisääminen, muokkaaminen ja poistaminen
- Kirjan kentät: Kirja, Kirjailija, Luokittelu (Osasto, laji), Kuvaus, Arvosana. luokat ovat tietokannassa.
- Sovelluksessa on pääasiallisen tietokohteen (kirja) lisäksi toissijainen tietokohde (arvostelu), joka täydentää pääasiallista tietokohdetta.


**Miten testata?**
*** Sovelluksen asennus***
- Kloonaa sovellus koneellesi:
    - Avaa terminaali ja kirjoita: git clone https://github.com/Kaikkinimet/Kirjavinkkisovellus.git
    - $ cd Kirjavinkkisovellus

**Luo virtuaaliympäristö ja asenna flask -kirjasto:**
- $ python3 -m venv venv
- $ source venv/bin/activate
- $ pip install flask
- $ pip install werkzeug

**Luo tietokanta**
- $ sqlite3 database.db < schema.sql
- $ sqlite3 database.db < init.sql

**Käynnistä sovellus**
- $ flask run

**Kokeile sovellusta:**
- Luo käyttäjä
- Kirjaudu sisään/ulos
- Lisää kirjavinkkejä
- Muokkaa ja poista kirjavinkkejä
- Tee hakutoimintoja
- Kommentoi ja arvioi toisen käyttäjän tekemiä arvioita
