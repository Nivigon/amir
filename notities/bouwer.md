# De bouwer

## De bouwer

Level maken in het startmenu. Het is dezelfde wereld als het spel, met drie verschillen: je kijkt
van verder weg (`BUILD_ZOOM`), Amir is een geest, en er ligt een laag bediening overheen.

**De indeling.** Een balk boven (`#bbalk`) met de naam, openen, opslaan, de twee testknoppen en
de levellijn (`tekenLijn`, een canvas: het hele level van opzij). Een rand links (`#brand`) met een
knop per soort, die de lijst ernaast uitklapt (`bouwOpen`). Het venster rechtsonder (`#binfo`) is
voor wat je aanklikt. De instellingenbalk van het spel (`#bar`) staat in de bouwer uit; B haalt hem
terug.

**Amir is een geest.** Het spel tekent hem niet (`globalAlpha` 0 in de bouwer, ook zijn schaduw),
en de camera blijft aan hem hangen. `bouwD` is hoe diep je kijkt, in sprite-eenheden, en
`updateCamera` zet de camera daarop. Omdat de camera in de bouwer ook met de zoom schaalt, klopt
`-camY / scale` daar niet: gebruik `camDiepte(scale)` als iets wil weten hoe diep je kijkt. En
reken een klik met `pointerLift`, die telt `camY` mee.

**Een stuk erbij in de bouwer** is vier dingen:

1. een regel in `GEREEDSCHAP` (id, soort, naam; `sneeuw` voor een winterversie, `kop` voor een
   tussenkopje);
2. een tak in de `pointerdown` van de bouwer, op dat id, met een `placeProblem` ervoor;
3. een tak in `builderHit`, zodat je het kunt aanklikken, en een naam in `bouwNaam`;
4. de velden in `bouwVelden` (getal, vink, keuze of tekst), en wat er verder bij hoort in
   `bouwExtra`: regels die zeggen wat er geldt, en knoppen.

Het wegschrijven hoef je niet bij te werken voor een veld dat de bouwer niet zelf beheert:
`syncLevel` begint bij het level zoals het binnenkwam (`level.bron`) en zet daar alleen overheen wat
de bouwer kent. Beheert de bouwer een veld wel, zet het dan in `syncLevel`, en draai
`tools/bouwertest.js`.

**Gangen** maakt de bouwer goed in plaats van ze achteraf na te kijken. `holteMaak` legt een gang
onder een ravijn, laat hem aan de beginkant `HOLTE_BUUR` doorlopen, houdt hem van de speer aan het
begin weg en voegt hem samen met een gang die hij raakt (`holteVerbind`). `holteTrap` legt de
uitgang aan het linkereind: treden van hoogstens `HOLTE_TREDE.stap`, 200 breed, alles boven -441
onder het gat, en raakt het gat de ingang, dan loopt de gang verder door. Verander je daar iets aan,
draai dan `levelcheck.py` en de speelrobot op een level uit de bouwer.

**Schakelaars** (`bouwSchakelTeken`): elke koppeling een kleur uit `KOPPEL_KLEUR` en een nummer, een
stippelkader waar een ravijn later openscheurt, de stippelcirkel om de schijf van een rune
(`RAVIJN_RUNE.raak`) en de streep onder een zegel (`ZEGEL.op`). Het raakvlak van de rotswand
tekent `muurBoxen`.

## level maken

de bouwer: `GEREEDSCHAP` (wat je neer kunt zetten), `bouwOpen` (de rand en de lijst), `bouwVelden` en `bouwExtra` (het venster), `tekenLijn` (de levellijn), `bouwD` en `bouwGeest` (Amir als geest), `bouwTesten` (testen vanaf hier), `holteMaak` en `holteTrap` (gangen), `bouwSchakelTeken` (koppelingen en raakvlakken); zie "De bouwer" hieronder
