# Decor: schilden en speertekens

## speerteken: een speer in de grond met een zwart doek en schedels

`TEKEN`, `tekenUpdate`, `tekenTeken`: decor in vijf varianten (`teken`, `gebroken`, `gekruist`, `jagers`, en `kalebas`: een kalebas aan een koordje die je met het mes lossnijdt, `tkKalebas`, `tekenSnij`); het doek wappert op `windAt` zoals het gras. Maten in Amir

## schilden in de wind

`SCHILD`, `schildStofUpdate`, `schildTil`, `drawSchildStof`: een schild (`schild: true` in `PROPS`) is een windscherm; bij een vlaag stuwt er stof tegen de windkant op, dat eroverheen waait. De plaatjes in `design/schilden/` zijn zelf de bron (het donkere motief van het klauwenschild is er met de hand in teruggezet)

## rotsdecor: losse rotsstukken in de stijl van de klif

`ROTS_FAM`, `rotsSoorten`, `rotsSoort`, `propLaad`, `propLaadLevel`: 24 props uit `design/rotsdecor/` (zuil, plaat, laag,
brok en kei; `rots` in `PROPS` is de familie). Ze zijn `placeOnly` en `lui`: ze laden niet bij het opstarten maar pas als
een level ze neerzet (`propLaadLevel` in `laadLevel`), of in de sandbox (`startSandbox`). `r` is de verhouding breedte op
hoogte, zodat `propHalfW` (de ravijncontrole) al klopt voor het plaatje binnen is. Keien en brokken vallen in een ravijn
dat openscheurt (`RAVIJN_DECOR.valt`); zuilen, platen en lage brokken schuiven of vervagen, zoals ander decor. Het idee:
veel van deze stukken tegen de wanden, zodat een plaat die een doorgang afdekt niet opvalt.

In de Maker: Decor, Stenen en sporen, **Rotsdecor** (zie `notities/maker.md`). In de sandbox: Decor, rij **Rotsdecor**,
een knop per familie die bij elke klik het volgende stuk neerzet (`sbRots`).

Er zijn drie families bij gekomen:

- **Grotkei** (`grotkei_01..07`) en **Ronde kei** (`rondkei_01..08`): de keien uit `design/grot/` die de golvende rand
  vanzelf strooit (`GROT_DEEL`), nu ook los te zetten. Ze hebben de maat van de grot, 850 bronpixels per Amir
  (`grotDecorS`): steentjes en keitjes. Ze vallen in een ravijn dat openscheurt.
- **Hangrots** (`hangrots_01..03`, `hang: true`): hangt met zijn bovenkant aan een plafond. Een prop draagt daarvoor `y`,
  de hoogte van die bovenkant in sprite-eenheden boven de grondlijn; zonder `y` (de sandbox) hangt hij net boven Amir.
  Een hangrots schuift niet weg voor een ravijn (`schoonLevel`, `ravijnDecor`, en in `levelcheck.py` de ravijn- en de
  gangdak-controle): hij hangt aan de rots erboven. De hangblokken in `design/grot/` zijn dezelfde plaatjes.

## kapotte vloer: barsten en puin

De barsten (`barst_1..4`) zijn de platen waarmee Nyundo het plein openslaat (`BRU_SCHADE.platen`,
`design/stad/plein_schade_*.png`), nu als vast decor. Ze hebben `plat: true`: ze liggen op de looplijn zelf, zonder de
stap terug die ander decor krijgt (`PROP_ACHTER`). Hun `h` en `sink` zijn zo gekozen dat ze op Formaat 25 even groot zijn
als op het plein en dat rij `EDGE.walk - BRU_SCHADE.top` van de plaat op de looplijn valt. Ze hebben de kleur van de straat
en het plein, dus ze passen het best in de stad. Het puin (`puin_01..14`) zijn de brokken uit `plein_brokken.png`, los
geknipt door `tools/puin_knip.py` naar `design/stad/puin/`; dat valt in een ravijn dat openscheurt. Beide hebben `vloer`
in `PROPS` als familie (`barst`, `puin`). In de Maker: Decor, Stenen en sporen, **Kapotte vloer**; in de sandbox de rij
**Kapotte vloer**.

De botten in `PROPS` hebben er `bot` (`bot` of `schedel`) en `naam` bij, voor de keuzelijst van **Botten** in de Maker.
## rotsen als decor: een runerots zonder rune

`rotsen`, `rotsenTeken`, `rotsenLaadLevel`: het levelveld `rotsen: [{x, soort, groot, y}]`. Dezelfde platen als onder een
rune (`RUNE_ROTSEN`: `spits`, `pieken`, `zuilen`, `boog`, via `runeBeeld` met het wit eruit) en hetzelfde licht
(`runeLichtMaak`, `runeGrondSchaduw`), maar zonder schijf en zonder ravijn: `x` is de linkervoet van de plaat, `groot` de
hoogte in Amir (0,5 tot 8, standaard `RAVIJN_ROTS.hoog`), `y` een vaste vloer (een plateau) en zonder `y` de grond op het
midden van de plaat. Getekend voor `drawClimb`, dus achter de terrassen en de zwevers: een plateau kan in de rots snijden
alsof de rots hem draagt. De rune-rots zelf wordt na de poorten getekend en tilt zichzelf op een zwever; dit niet. In de
arena gates (`sbGatesVeld`) staan er twee: de pieken links onder het plateau en de spits rechts achter de lage poort.
Nog in geen level en nog niet in de Maker.
