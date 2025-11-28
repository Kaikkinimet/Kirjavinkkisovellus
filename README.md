Kirjanvinkkisovellus: kuvaus, millainen sovellus on ja miten sitä voi testata.

Sovellus sisältää: Käyttäjä:

Käyttäjä voi luoda tunnuksen
Käyttäjä voi kirjautua sisään ja ulos
Jokainen käyttäjä näkee kaikki sovellukseen lisätyt kirjat
Kirjavinkit:

Kirjan lisääminen
Omat kirjat voi muokata ja poistaa
Kirjan kentät: Otsikko, Kirjailija, Kuvaus
Haku:

Käyttäjä voi etsiä kirjoja hakusanalla
Haku etsii kirjan otsikosta, kirjailijasta ja kuvauksesta
Miten testata?

Avaa terminaali ja kirjoita:
git clone https://github.com/Kaikkinimet/Kirjavinkkisovellus.git
cd Kirjavinkkisovellus
Luo virtuaaliympäristö ja asenna:
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install werkzeug
Luo tietokanta
sqlite3 database.db < schema.sql
Käynnistä sovellus flask --app app. run

Me osoitteeseen http://127.0.0.1:5000 ja kokeile sovellusta:

Luo käyttäjä
Kirjaudu sisään
Lisää kirjavinkkejä
Muokkaa ja poista kirjavinkkejä
Tee hakutoimintoja
To be conntinued...

Kirjavinkkisovellus tulee sisältämään:

Käyttäjät voivat lisätä kirjavinkkejä ja arvioida muiden vinkkejä:

Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
Käyttäjä pystyy lisäämään sovellukseen kirjavinkkejä. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kirjavinkkejä.
Käyttäjä näkee sovellukseen lisätyt kirjavinkit. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kirjavinkit.
Käyttäjä pystyy etsimään kirjavinkkejä hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä kirjavinkkejä.
Sovelluksessa on pääasiallisen tietokohteen (kirja) lisäksi toissijainen tietokohde (arvostelu), joka täydentää pääasiallista tietokohdetta.
Käyttäjä pystyy lisäämään arvosteluita (toissijaisia tietokohteita) omiin ja muiden käyttäjien kirjoihin (tietokohteisiin) liittyen.
Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät kirjavinkit.
Käyttäjä pystyy valitsemaan kirjalle yhden tai useamman luokittelun (esim. osasto, genre, kirjalija, kieli). Mahdolliset luokat ovat tietokannassa.

