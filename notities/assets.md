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

Een plaatje hoort alleen in de kleine set als het op een telefoon nog steeds groter
is dan het stukje scherm waar het terechtkomt. De afweging per familie staat in
`DOELEN` in `tools/gen-klein.py` en in de README.

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
