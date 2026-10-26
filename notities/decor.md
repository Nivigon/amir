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

In de Maker: Decor, **Rotsdecor** (zie `notities/maker.md`). In de sandbox: Decor, rij **Rotsdecor**, een knop per
familie die bij elke klik het volgende stuk neerzet (`sbRots`). De drie hangrotsen (`hangrots_01..03`) staan wel in
`design/rotsdecor/`, maar nog niet in `PROPS`: het spel kan een prop nog niet aan een plafond hangen.
