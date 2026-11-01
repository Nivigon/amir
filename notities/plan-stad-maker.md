# Plan: de stad in de Level Maker nieuwstijl

Status: plan, met de keuzes van de opdrachtgever erin. Wordt per stap gebouwd; vink af wat er staat.

## Uitgangspunt

- De stad bestaat al als leveldefinitie (`level.stad`, zie `notities/stad.md`): gevels, galerijen, kramen,
  voetdecor, trappen, paleis en seed. Gevels, kramen en voetdecor staan los op een x; een galerij en een trap
  hangen aan een gevel (zijn index in `gevels`).
- De Maker kent nog niets van de stad, en schrijft geen `stad` en geen `lagen`.
- `MK_CATS` heeft al 6 categorieën (`MK_PALET_MAX`). Er komt dus geen categorie Stad bij, maar een schakelaar.
- De grondafwerking in de Maker is nu voor het hele level: de eerste rots- of sneeuwcel op de grondlijn bepaalt
  de bodem (`afwerking` in `mkNaarLevel`). Het spel tekent op elke plek dezelfde tegel (`bodemPic`).

## De keuzes

| # | vraag | keuze |
| --- | --- | --- |
| 1 | waar mag straat komen | overal: basisgrond, terrassen, zwevers, gangbodem |
| 2 | de naad tussen straat en savanne | zacht: de tegel loopt uit in zand, over een halve cel |
| 3 | stadsstuk op grond die geen straat is | mag, `mkControle` meldt LET OP |
| 4 | het uitzicht | een per level, keuze Uitzicht in de balk, standaard vanzelf |
| 5 | tekenen in het grid | de echte plaatjes, klein en half doorzichtig |
| 6 | een galerij leggen | slepen van gevel naar gevel, daarna extra lengte links en rechts |
| 7 | een trap | klik op de zijkant van een gevel; kant, niveau en balkon in het paneel |
| 8 | een vijand op een dak | vanzelf `dak` als hij op een dak of galerij staat |
| 9 | sneltoets voor de schakelaar | G |
| 10 | de stad in de verte | knop Andere stad (nieuwe seed), het paleis als verschuifbare markering, onder een kopje Stad |
| - | breedte | een gevel schaalt mee met het scherm; de Maker tekent op laptopmaat en de controle waarschuwt bij overlap |
| - | plek van de schakelaar | bovenaan de legenda, boven de categorieknoppen |

## De schakelaar Savanne | Stad

- Bovenaan de linkerkolom, sneltoets G. Hij filtert alleen het palet: wat in het grid staat blijft staan.
- Elk item in `MK_TYPES` krijgt `thema: 'savanne'` of `'stad'`; zonder veld staat het in beide.
  `mkPaletBoom` bouwt de boom uit wat bij de stand past. Per stand onthoudt de Maker het laatste gereedschap.
- Terrein: grond, ravijn, gang en rots in beide; sneeuw alleen bij Savanne; straat en leem alleen bij Stad (groep Stad).
- Decor bij Stad: groep Huizen (gevel, galerij, trap) en groep Straat (kraam riet, kraam doek, voetdecor, paleis).
- Vijanden, Punten, Objecten en Verbergen: in beide gelijk.
- `makertest.js` (controle `maat`) loopt per stand.

## Grondsoort per plek (nieuw in het spel)

- Een nieuw levelveld met stroken grondsoort langs x, bijvoorbeeld `grondSoort: [{van, tot, soort}]`, `soort`
  savanne, rots of straat; de sneeuwlaag erop blijft `sneeuw` (die kent al `van` en `tot`).
- De tekenplekken van `bodemPic` tekenen per strook, met een zachte grens zoals `sneeuwJag`.
- Ook voor de bovenkant van een terras, zwever en gangbodem.
- De Maker schrijft de stroken uit de cellen, in plaats van een `afwerking` voor het hele level. Een opgeslagen
  Maker-level met gemengde cellen ziet er daarna anders uit (zoals je het geschilderd hebt). De echte episodes en
  testlevels hebben het veld niet en blijven gelijk.

## De stukken

| stuk | in het grid | paneel | naar het level |
| --- | --- | --- | --- |
| gevel | ankercel linksonder, zo breed als het huis | hoogte 1 tot 4, spiegelen | `gevels: {x, hoog, f}` |
| kraam | ankercel in het midden | soort, spiegelen | `kramen` |
| voetdecor | een cel | stuk, spiegelen | `voet` |
| paleis | een per level, markering | geen | `paleis: x` |
| galerij | slepen van gevel naar gevel | niveau, extra links en rechts | `galerijen: {van, tot, h, meer}` |
| trap | zijkant van een gevel | kant, niveau, balkon | `trappen` |

- Elke gevel krijgt in de Maker een eigen id; pas `mkNaarLevel` zet dat om naar een index.
- `stadLaad` alleen als de stand Stad aan is of het grid stadsstukken heeft (lui laden).
- Een stadsstuk in het grid geeft `stad` en `lagen: 'stad_dag'` en als standaard de stadmuziek.

## Volgorde

1. [x] Fundament: schakelaar, `thema`, G, Uitzicht in de balk, en de leemmuur (pull request 517) als terreinsoort
   **Muur van leem** in de stand Stad. Het veld `stad` zelf komt mee met de eerste stukken in stap 3.
2. [x] Grondsoort per plek in het spel, met straat als terreincel in de Maker (het veld `grondSoort`,
   zie `notities/grondsoort.md`).
3. [x] Losse stukken: gevel, kraam, voetdecor, paleis (zie "De losse stukken van de stad" in `notities/maker.md`). Met het
   veld `stad` en `lagen: 'stad_dag'`, de stadmuziek als standaard, `stadLaad` lui, en een eigen id per gevel.
4. [x] Gekoppelde stukken: galerij en trap (zie "De gekoppelde stukken: galerij en trap" in `notities/maker.md`). Een
   galerij of trap zonder zijn gevel gaat in de Maker mee weg (`mkStadKoppel`), en `mkNaarLevel` slaat er een over voor de zekerheid.
5. [ ] Afwerking: vijanden op daken, meldingen in `mkControle`, proefgrid in `makertest.js`,
   `notities/maker.md`, `notities/stad.md` en `README.md`.
   Al gedaan (naar voren gehaald in stap 3): de LET OP voor een gevel, kraam of voetdecor op grond die geen straat is,
   en de LET OP voor een straatcel of leemmuur boven de grondlijn zonder straat op de grondlijn eronder. Ook al gedaan:
   een eigen controle `stadsstukken` in `makertest.js` (nog niet in het proefgrid), en de notities en README voor
   stap 3. Ook al gedaan (stap 4): de controle `stadsstukken` kent galerij en trap. Nog te doen: de overige meldingen (overlap van
   gevels op laptopmaat, een galerij hoger dan zijn huizen, een trap zonder vloer aan de voet of de uitgang), de vijanden
   op daken en het proefgrid.

Na elke stap `node tools/makertest.js` en `python3 tools/levelcheck.py`. Geen level van een episode of
bestaand testlevel verandert.
