# DZĪVOKĻA ĪRES PIEDĀVĀJUMU MEKLĒŠANAS SISTĒMA RĪGĀ - SS.COM SPECIALIZĒTĀ VERSIJA

## Projekta uzdevums

Šis projekts automatizē dzīvokļa īres piedāvājumu meklēšanu Rīgā, izmantojot web scraping tehnoloģijas un datu struktūras. Tas iegūst jaunākos, aktuālus īres piedāvājumus no SS.com, analizē un strukturē datus, atvieglojot to filtrēšanu un atlasi pēc lietotāja noteiktiem kritērijiem.

## Projekta mērķis

Izstrādāt rīku, kas palīdzētu atrast optimālu īres dzīvokli Rīgā — tādu, kas ir vizuāli pievilcīgs, aprīkots ar pēc iespējas vairāk ērtībām, atrodas tuvu pilsētas centram un ir pieejams par zemāko iespējamo cenu. Šī sistēma kalpo kā praktisks palīgs personīgai vajadzībai — atrast ideālu mājvietu diviem cilvēkiem.

## Funkcionalitāte

* Datu iegūšana no SS.com ar `PropertyScraper`
* Datu attālināta apstrāde un filtrēšana ar `PropertyFilter`
* Lietotāja mijiedarbība ar interaktīvu termināli (`main.py`)
* Attāluma aprēķins līdz Rīgas centram (`utils.py`)
* Unikālo piedāvājumu identificēšana un jaunu sludinājumu noteikšana (pickle)
* Veiktspējas mērīšana (QuickSort, BST, Heap, PriorityQueue)

## Lietotāja iespējas

1. Apskatīt visus īres piedāvājumus (sakārtoti augušā secībā pēc cenas)
2. Filtrēt piedāvājumus pēc cenu diapazona (BST)
3. Filtrēt piedāvājumus ar iekļautām komunālajām izmaksām
4. Filtrēt pēc attāluma no centra
5. Apskatīt algoritmu veiktspējas metriku
6. Pārtraukt programmu

## Galvenās izmantotās komponentes

### Klase: `Property`

Reprezentē vienu sludinājumu ar visiem tā parametriem. Atbalsta salīdzināšanu, izvadu un hash noteikšanu dublikātu apstrādei.

### Datu struktūras

* `BinarySearchTree` (meklēšana un filtrēšana pēc cenas)
* `MinHeap` un `MaxHeap` (lētāko/dārgāko piedāvājumu izgūšanai)
* `PriorityQueue` (pielāgota salīdzināšana, piem. ar/bez komunālajiem maksājumiem)

### Filtrēšanas metodes (`PropertyFilter`):

* Cenu diapazons
* Komunālās izmaksas iekļautas
* Istabu skaits
* Mēbeles
* Attālums no centra
* Dzīvnieku atļaušana
* Autostāvvieta
* Publicēšanas datums
* Rajons

### Ģeogrāfiskais attālums (`utils.py`):

Adrese tiek šifrēta uz koordinātām izmantojot OSM Nominatim API, aprēķināts attālums (Haversine formula) un braukšanas laiks (30 km/h).

### Saglabāšana un dublikātu apstrāde

Dati tiek serializēti ar `pickle`, iepriekšēji rezultāti salīdzināti, lai izceltu jaunus sludinājumus.

## Bibliotēkas

* `requests`, `beautifulsoup4` - web scraping
* `re`, `datetime`, `time`, `random` - datu parsēšana un kontrole
* `math`, `pickle`, `sys`, `os`

## Palaišana

1. Vispirms instalēt terminal sadaļā prasītās bibliotēkas:

```
pip install requests vai pip3 install requests
pip install requests beautifulsoup4
```

2. Lai palaistu programmu no, piemēram, VS code, to var izdarīt, izmantojot command promt. Atrod command prompt datora iestatījumos, atver to, tad ieraksta šo:

```
2.1. cd C:\Users\renar\Downloads\mekletajs

2.2. set PYTHONIOENCODING=utf-8

2.3. python main.py VAI py main.py
```
3. Programma jāpalaiž tikai caur galveno failu (main.py), ja to dara Github.com vietnē.

## Rezultātu attēlojums

Katrs īpašums tiek izvērtēts un izvadīts sekojošā formātā:

* Nosaukums
* Cena (EUR/mēnesī)
* Istabu skaits
* Adrese
* Platība
* Stāvs
* Mēbeles
* Virtuves aprīkojums
* Vannas istaba
* Attālums līdz centram (km, min)
* Autostāvvieta
* Dzīvnieki
* Minimālais īres termiņš
* Publicēšanas datums
* Saite, kur piedāvājums atrodams

## Algoritmu veiktspējas mērījumi

* QuickSort: cenas sakārtošana
* BST: cenu diapazona meklēšana
* MinHeap: lētākie piedāvājumi
* PriorityQueue: kombinēta prioritāšu atlase

Mērītie parametri: laiks, elementu skaits, sarežģītīas analīze (teorija un prakse).

## Piezīmes

* Projekts paredzēts Python 3 vidē.
* Kods ir strukturēts loģiski ar komentāriem un atdalītām funkcionalitātēm.
