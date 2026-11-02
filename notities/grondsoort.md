# Grondsoort per plek: stroken straat of rots in de bodem

`GRONDSOORT`, `grondSoort`, `grondStroken`, `grondTegelVan`, `grondTegelRij`, `grondStrokenTeken`, `leesGrondSoort`

Stap 2 van `notities/plan-stad-maker.md`. Een level kan de bodem per strook een andere
soort geven dan de rest:

```
grondSoort: [{van, tot, soort}]      soort 'savanne', 'rots', 'straat' of 'plein'
```

`van` is de startkant (minst negatief), `tot` verderop, zoals bij `sneeuw`; de code
normaliseert zelf, dus omgekeerd mag ook. Geen bestaand level heeft het veld; de Maker
nieuwstijl schrijft het uit de terreincellen op de grondlijn, en in de sandbox staan de
knoppen onder Terrein, **Grondsoort** (Strook straat, Strook rots, Weg, `sbGrondSoort`).

## Hoe het tekent

De basis blijft `bodemPic` (de bodem van het level zelf: savanne, de rotsbodem van het
veld `sneeuw`, de wintergrond of de straat van een level met `stad`). Elke strook wordt
daar met zijn eigen tegel overheen getekend; alle grondtegels hebben de maten en rijen
van `EDGE` (savanne `grondrand.png`, rots `grondrand_rots.png` via `loadSneeuw`, straat
`design/stad/straat.png` en plein `design/stad/plein.png` via `stadLaad`), dus het anker en de schaal zijn gelijk.

De grens loopt grillig (`sneeuwJag`, dezelfde jag als de sneeuwgrens) en de tegel loopt
over ongeveer een halve Maker-cel (`GRONDSOORT.rand`, 88 wereld-px) zacht uit in de grond
ernaast: `grondStrokenTeken` tekent per strook twee lagen, eerst een halfdoorzichtige
(`GRONDSOORT.uitAlpha`) tot de buitenrand (strook plus een halve `rand`), daarbinnen de
volle tegel tot de binnenrand (strook min een halve `rand`). Zo mengt de tegel over een
halve cel met de grond eronder, de keuze "zacht: de tegel loopt uit in zand" uit het plan.

De aanroepen:

- **de basisgrond**: in `sceneGrond`, direct na de tegelrij, binnen dezelfde clip die de
  ravijnen eruit knipt (dus een strook stopt netjes bij een gat).
- **een hogere of zwevende savannelaag**: in `savanneLaag`, na de tegelrij en voor het
  sneeuwdek, binnen het laag-silhouet (`terClipPath`); niet op een zwarte laag.
- **de gangvloer**: in `drawHolte` (de vloer-stap), met de tegel in hetzelfde donker als
  de vloer zelf (`holteVloerTegel`, dezelfde verdonkering als `holteSet.vloer`, die nu in
  `holteVloerLaag` staat), binnen de put-clip, zodat een put er ook uit geknipt blijft.

De sneeuwlaag (het veld `sneeuw`) ligt er gewoon overheen, zoals op de gewone bodem.

## Wat de basis houdt

Een zuil, een rijzer (zijn `look`), het overloopje, de schachtkap en het nep-terrein van
een masker tekenen nog met `bodemPic` alleen: daar doet het veld niets. Met `golf`
(golvende rand) doet het veld op de basisgrond ook niets (de golfrand tekent zijn eigen
kruin); geen level combineert ze. Overlappende stroken zijn niet de bedoeling: ze tekenen
over elkaar heen en de halfdoorzichtige randen stapelen; de Maker schrijft ze nooit
overlappend. De donkere massa onder de tegel blijft overal `bodemDonker` (de kleur van de
basis); je ziet daar alleen iets van wie heel diep in een ravijn kijkt.

## De Maker

De terreincel **Grond: straat** (`straat`, letter `A`, groep `terrein/stad`, stand Stad,
naast de leemmuur). Op de grondlijn wordt hij een strook `soort: 'straat'`; rots- en
sneeuwrots-cellen op de grondlijn worden nu stroken `soort: 'rots'` (per plek, zoals je
het schildert) in plaats van de oude `afwerking` die de hele bodem omzette. Een
sneeuwcel (sneeuw of sneeuw op rots) geeft nog steeds een dichte sneeuwlaag over de hele
bodem, nu altijd als `sneeuw: {soort: 'savanne', dek: 1, vol: true}`: de grijze bodem
komt uit de strook, niet meer uit `sneeuw.soort`. Boven de grondlijn telt een straatcel
als savanne (een terras van grond, een zwever); welke tegel zijn bovenkant krijgt bepaalt
de strook op de grondlijn op die x, dus een straatterras hoort op een straatstrook te
staan; `mkControle` meldt een straatcel of leemmuur boven de grondlijn zonder straat op de
grondlijn eronder (LET OP). Een straatcel zet via `mkHeeftStad` (thema stad) ook vanzelf het uitzicht op de
stad. Staat er een stadsstuk in het grid (stap 3), dan schrijft de Maker het veld `stad`, en daarmee is de basis
de straat (`bodemPic`): dan krijgen savanne- en sneeuwcellen op de grondlijn een strook `soort: 'savanne'`, zodat
de bodem blijft zoals je hem schildert. `tools/makertest.js` kijkt het na (het proefgrid heeft een strook straat, en de
controle `stad` een strook rots en straat); `tools/levelcheck.py` keurt een onbekende
soort af (regel `velden`).

## Meetgeschiedenis

- 2026-10: gebouwd (stap 2 van het plan). Nagekeken met schermafdrukken uit de sandbox:
  de strook straat op de vlakke grond met de zachte rand aan beide kanten, de strook rots
  op de bovenkant van een savannelaag, en de strook straat op een gangvloer (donker, met
  de lichtschacht van de ingang ernaast). De gang-overgang (aarde naar steen,
  `holteOvergang`) valt over de onderkant van de straattegel heen, zodat die in het steen
  van de gang uitloopt.
