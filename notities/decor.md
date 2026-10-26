# Decor: schilden en speertekens

## speerteken: een speer in de grond met een zwart doek en schedels

`TEKEN`, `tekenUpdate`, `tekenTeken`: decor in vijf varianten (`teken`, `gebroken`, `gekruist`, `jagers`, en `kalebas`: een kalebas aan een koordje die je met het mes lossnijdt, `tkKalebas`, `tekenSnij`); het doek wappert op `windAt` zoals het gras. Maten in Amir

## schilden in de wind

`SCHILD`, `schildStofUpdate`, `schildTil`, `drawSchildStof`: een schild (`schild: true` in `PROPS`) is een windscherm; bij een vlaag stuwt er stof tegen de windkant op, dat eroverheen waait. De plaatjes in `design/schilden/` zijn zelf de bron (het donkere motief van het klauwenschild is er met de hand in teruggezet)

## rotsen als decor: een runerots zonder rune

`rotsen`, `rotsenTeken`, `rotsenLaadLevel`: het levelveld `rotsen: [{x, soort, groot, y}]`. Dezelfde platen als onder een
rune (`RUNE_ROTSEN`: `spits`, `pieken`, `zuilen`, `boog`, via `runeBeeld` met het wit eruit) en hetzelfde licht
(`runeLichtMaak`, `runeGrondSchaduw`), maar zonder schijf en zonder ravijn: `x` is de linkervoet van de plaat, `groot` de
hoogte in Amir (0,5 tot 8, standaard `RAVIJN_ROTS.hoog`), `y` een vaste vloer (een plateau) en zonder `y` de grond op het
midden van de plaat. Getekend voor `drawClimb`, dus achter de terrassen en de zwevers: een plateau kan in de rots snijden
alsof de rots hem draagt. De rune-rots zelf wordt na de poorten getekend en tilt zichzelf op een zwever; dit niet. In de
arena gates (`sbGatesVeld`) staan er twee: de pieken links onder het plateau en de spits rechts achter de lage poort.
Nog in geen level en nog niet in de Maker.
