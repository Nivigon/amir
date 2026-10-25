# Assets

## Assets

Sprites toegevoegd, vervangen of weggehaald? Draai daarna, in deze volgorde:

```
python3 tools/gen-klein.py
python3 tools/gen-offline-manifest.py
```

Het eerste script print de lijst die in `KLEIN_FAM` hoort te staan. Loopt die niet
gelijk, dan laadt een telefoon stilletjes de grote versie. Het tweede werkt de lijst
bij die de downloadknop afwerkt; sla je dat over, dan mist de offline-download
bestanden.

## De arena-set van de offline-download

`offline-assets.json` heeft naast de hele lijst (`assets`) een deel `delen.arena` en een lijst
`soorten`: de basis van de Arena modus van de sandbox en per soort uit `SB_ARENA_SOORTEN` zijn
frames, voor de knop **Alleen de Arena modus** onder Instellingen (`#offarena`). Het spel leest
uit `localStorage` (`amir.arenaCfg`) welke soorten in de arena aan staan (`arenaSoorten`) en geeft
de service worker `deel: 'arena'` plus die `soorten` mee; die telt en downloadt dan de basis plus
die soorten (`voorDeel` in `sw.js`), en rekent de bytes uit met `groottes` (de grootte per bestand,
in de volgorde van `assets`). Staat er nog niets aan, dan alle soorten. De basis staat in
`ARENA_MAPPEN` in `tools/gen-offline-manifest.py` (en wat er binnen die mappen toch niet meegaat
in `ARENA_NIET`): Amir, het decor van de arena van de koning, wat de knoppen in de wizard kunnen
oproepen (bloed, doornbos, water, kalebassen, de abilities), wat het spel bij het opstarten altijd
laadt (het gif van de slangen, de dolk, de json en de mp3 van de vijanden), alle geluiden en alle
muziek; de soorten in `ARENA_SOORTEN` (de bandiet met elite en Duinwacht, de kooiman met zijn
vogel, de fosfor met de frames van de zandslang). De kleine set volgt vanzelf (zelfde regel als
`voorSet`). Daarvoor laadt de arena-modus zijn soorten pas bij Start en bij een spawn
(`sbArenaLaad`, `SB_ARENA_LAAD`), niet meer allemaal bij het openen van de sandbox zoals de vrije
sandbox dat doet. Wat het menu voor het gekozen levelkaartje alvast laadt (`laadLevel` in
`setLevel`, bij het opstarten de nieuwste test) hoort niet bij de basis: offline ontbreekt dat
zonder gevolgen, het level wordt niet gespeeld.

Na een wijziging aan die lijst, aan de arena of aan wat de sandbox laadt: `node tools/arena-assets.js`
(zie `notities/tools.md`). Die speelt de arena in Chromium met alle soorten aan en meldt FOUT op elk
bestand dat het spel opvraagt en niet in de set staat, voor de grote en de kleine spriteset apart.

Twee dingen die daarbij aan het licht kwamen: `items/` (de drinkkalebas, de meelzakken) en
`ravijn/assets/` zaten helemaal niet in de lijst, en de json van de schildbandiet (`lagen.json`,
`executie.json`) ging in `sw.js` als "het spel zelf" naar de shellcache terwijl de downloadknop hem
in de assetcache zette, zodat de schildman offline niet laadde. Json onder de assetmappen is nu een
asset (`isAsset`), met een terugval op de andere caches voor wie hem nog in de shellcache heeft.

Een plaatje hoort alleen in de kleine set als het op een telefoon nog steeds groter
is dan het stukje scherm waar het terechtkomt. De afweging per familie staat in
`DOELEN` in `tools/gen-klein.py` en in de README. Een doel dat ook op de helft nog
ruim te groot is krijgt daar een eigen factor (het goudaapje: 0,25, een kwart); zo'n
familie hoort dan ook in `KLEIN_BRON` in de HTML, zodat `bronW` en `bronH` met de
juiste factor terugrekenen (het script print die lijst ook).

De bodem en het dek van het veld `sneeuw` komen uit `tools/sneeuwdek.py`
(`grondrand_rots.png` en `sneeuwlaag_25..100.png`). Die staan met opzet niet in de kleine
set: `grondrand.png` staat daar ook niet in, en een dek dat anders geschaald wordt dan de
bodem eronder gaat schuiven.

De run van de baviaan komt uit `tools/baviaan_run_fix.py`: de aangeleverde frames staan ongewijzigd in
`enemies/baviaan/bron/run/`, het script plakt de kapotte handen en voeten dicht met stukken uit andere
frames en schrijft de speelversie naar `enemies/baviaan/run/`. Een map `bron/` gaat niet mee in de
offline-download, want het spel laadt hem nooit.

`design/grot/rots_vulling.png` (het steen boven een plafondlijn) komt uit `tools/rots_vulling.py`:
dat knipt het massieve deel uit `plafond_strook.png`, haalt het licht-donkerverloop eruit en
maakt de boven- en onderrand op elkaar aansluitend. Verandert de strook, draai het dan opnieuw.

De grotset in `design/grot/` hoort wel in de kleine set: die stukken zijn de grootste
bronnen van het spel en worden tot een tiende getekend. Dat mag hier omdat de tekencode
met de maten uit `grot.json` rekent en elk stuk naar die maat rekt; de ankerpunten
schuiven dus niet mee met de bronmaat. `grot.json` zelf blijft buiten de kleine set,
want `gen-klein.py` pakt alleen png's.

Geluid staat in `music/` en `sounds/`. De achtergrondnummers staan in `music/` en worden
aangemeld in `MUZIEK`; korte geluiden van personages en dieren horen in `sounds/`. Zo staan
`ahhit.mp3` en `stopit.mp3`, de twee kreten van Amir, bij de hyenageluiden en niet bij de
muziek. Beide mappen zitten in de offline-download, dus draai na een nieuw bestand
`tools/gen-offline-manifest.py` opnieuw.

Het speerteken heeft maar twee soorten eigen plaatjes, en die komen uit `tools/speerteken.py`:
het doek in drie kleuren (`design/botten/speerteken/doek_zwart`, `doek_vaal`, `doek_rood`), omgekleurd
op helderheid uit het blauwe doek van het skelet, en `riem.png`, de rode omwikkeling onder Amir zijn
speerpunt in `amirspear.png`, bruin gemaakt. Zo blijft het in de stijl van de rest. Teken er niets met
de hand bij; zoek een stuk uit een bestaande sprite en kleur dat om.

De slangen komen uit `tools/slang_kleur.py`: dat kleurt `enemies/slang1/` om naar de
zandslang in `enemies/slang1_zand/`, `enemies/slang2/` naar de zwarte in `enemies/slang2_roet/`,
en `enemies/slang1/` ook naar de knockslang in `enemies/slang1_knock/` (jade lijf, violette zadels).
Die laatste set krijgt er een eigen `venom.png` bij: de zwarte druppel van `slang2/` omgekleurd naar
jade met een violette kern, zodat de knockslang jade/violet spuugt. Het spel tekent alleen die
omgekleurde mappen (`SNAKE_DIRS`); de originelen blijven staan als bron, en de `venom.png` van de
zwarte komt nog steeds uit `slang2/`. Verandert er een frame, draai het script dan opnieuw. Ze staan
niet in de kleine set.

De elite-garde komt uit `tools/bandiet_elite_kleur.js`: dat kleurt alle reeksen van
`enemies/bandiet/` om naar `enemies/bandiet_elite/`, zwart met een goud accent (een
gradient-map legt de lichte, weinig verzadigde glans van het staal en de gespen op een
goudladder en al het andere op houtskool; de donkere contour blijft zwart). Het spel
tekent die map op de elite-vlag (zie "de bandiet"). Verandert een bronframe, draai het
script dan opnieuw, en daarna `gen-klein.py` en `gen-offline-manifest.py`. De elite-set
staat wel in de kleine set (zoals de gewone bandiet).

De losse kooi-plaat van de kooiman (de duw-lus) komt uit `tools/kooi_kleur.py`: de aangeleverde
bron `enemies/kooiman/bron/kooi/kooi.png` heeft grijze spaken maar een massief gele vulling; het
script haalt het geel eruit en maakt er het interieur uit `sprites.json` van (`cage_interior`, dark
32,32,38 op ~50% alpha), zodat de kooi grijs is met wat doorzichtigheid tussen de spaken, net als de
ingebakken kooien van de man. Het schrijft `enemies/kooiman/kooi/kooi.png`. Verandert de bron, draai
het opnieuw, en daarna `gen-klein.py` en `gen-offline-manifest.py`. De plaat staat wel in de kleine
set; de bron in `bron/` niet.

Winterversies komen uit `tools/sneeuw.py` (rotsen en klimstukken), `sneeuw_bg.py`
(achtergrondpanelen), `sneeuw_dorp.py` (hutten, boom, struik) en `winter_art.py`
(dieren, grond, gras). Verandert een origineel, draai het bijbehorende script dan
opnieuw.
