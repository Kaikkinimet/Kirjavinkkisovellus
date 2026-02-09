# Kirjanvinkkisovellus

Seuraavassa kerrotaan millainen sovellus on ja miten sitä voi testata.

## **Sovelluksen toiminnot**

***Käyttäjä:***
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä voi kirjautua sisään ja ulos
- Käyttäjä pystyy lisäämään sovellukseen kirjavinkkejä.
- Käyttäjä muokkaamaan ja poistamaan lisäämiään kirjavinkkejä.
- Käyttäjä voi llisätä kirjan kuvan
- Kaikki näkevät sovellukseen lisätyt kirjavinkit.
- Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kirjavinkit.
- Käyttäjä näkee omat käyttäjäsivut, josta näkee kuinka monta arvioita hän on tehnyt
- Käyttäjät voivat kommentoida ja arvioida toisen lisättyjä kirjoja. Käyttäjä voi muokata omaa komenttia tai poistaa sen
- Arvion lisääjä voi poistaa toisten tekemän kommentin
- Kaikki pystyvät etsimään kaikkia kirjavinkkejä hakusanoilla, jotka etsivät kaikista kentistä.

***Kirjavinkit:***
- Kirjan lisääminen, muokkaaminen ja poistaminen
- Kirjan kentät: Kirja, Kirjailija, Luokittelu (Osasto, laji), Kuvaus, Arvosana. luokat ovat tietokannassa.
- Kirjaan voi lisätä kuvan tai poistaa sen.
- Sovelluksessa on pääasiallisen tietokohteen (kirja) lisäksi toissijainen tietokohde (kommentoint), joka täydentää pääasiallista tietokohdetta.


## **Miten testata?**
***Sovelluksen asennus***
- Kloonaa sovellus koneellesi avaamalla terminaali ja kirjoita:
```
  git clone https://github.com/Kaikkinimet/Kirjavinkkisovellus.git
```
- Avaa sovellus
```
  $ cd Kirjavinkkisovellus
```
***Luo virtuaaliympäristö ja asenna flask -kirjasto:***
```
 $ python3 -m venv venv
 $ source venv/bin/activate
 $ pip install flask
```
***Luo tietokanta***
```
 $ sqlite3 database.db < schema.sql
 $ sqlite3 database.db < init.sql
```
***Käynnistä sovellus***
```
 $ flask run
```
***Kokeile sovellusta:***
- Luo käyttäjä
- Kirjaudu sisään/ulos
- Lisää kirjavinkkejä
- Muokkaa ja poista kirjavinkkejä
- Tee hakutoimintoja
- Kommentoi ja arvioi toisen käyttäjän tekemiä arvioita

-------------------
***Suuren tietomäärän käsittely:***
- Sovellusta testattiin suurella tietomäärällä seed.py -skriptin avulla. Tietokantaan generoitiin 1000 käyttäjää, 100 000 kirja-arviota ja 1 000 000 kommenttia, ja jokaiselle arviolle lisättiin luokittelut. Tällä datalla sovellus toimii edelleen oikein, mutta hakujen ja etusivun listauksen vasteaika kasvoi. Sovellukseen otettiin käyttöön tietokohteiden sivutus ja tietokantaan lisättiin indeksit, jotka nopeuttavat suuren tietomäärän käsittelylä.
- Ajanmittaus etusivun kyselyssä: ilman indeksejä ja sivutusta 1,0076 s. Sivutuksen ja indeksoinnin jälkeen 0,8998 s.
