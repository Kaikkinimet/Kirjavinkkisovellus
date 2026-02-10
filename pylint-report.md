
# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:62:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:147:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:167:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:186:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:197:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:215:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:225:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:236:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:261:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:277:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:290:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:312:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:317:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:336:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:357:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:365:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module items
items.py:1:0: C0114: Missing module docstring (missing-module-docstring)
items.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:14:0: R0913: Too many arguments (6/5) (too-many-arguments)
items.py:14:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
items.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:62:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:79:0: R0913: Too many arguments (6/5) (too-many-arguments)
items.py:79:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
items.py:94:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:98:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:113:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:121:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:130:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:146:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:150:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:154:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:158:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.68/10 (previous run: 8.67/10, +0.00)
```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

## **Docstring-ilmoitukset**

Suurin osa raportoin ilmoituksista on seuraavan tyyppisiä ilmoituksia:
```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
```
Nämä ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole docstring-kommentteja. Sovelluksen kehityksessä on tehty tietoisesti päätös kurssimateriaaliin perustuen, ettei docstring-kommentteja käytetä järjestelmällisesti.


## **Too many arguments -ilmoitukset**
```
items.py:14:0: R0913: Too many arguments (6/5) (too-many-arguments)
```
Nämä ilmoitukset tarkoittavat, että funktiolla on enemmän argumentteja kuin pylintin suositeltu enimmäismäärä. Sovelluksen kehityksessä on tehty tietoisesti päätös, että nämä ylitykset on hyväksytty ratkaisu.
