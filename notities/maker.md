# De Level Maker nieuwstijl

De knop **Maker nieuwstijl** in het startmenu. Een los grid om de ruwe vorm van een level te
schetsen en meteen te spelen. Staat helemaal op zichzelf: het raakt de spel-loop, de levels
(regel 1) niet aan. De sectie in de HTML heet `// ---------- Level Maker ----------`.

## Hoe het in elkaar zit

Alle state zit in één object, `MK`: de maat (`cols`, `rows`), de grondlijn-rij (`ground`), het
`grid` (per cel een id uit `MK_TYPES`, zoals `savanne`, `rots`, `gang`, `ravijn`, `laag`), `start` en
`eind`, de voorwerpen (`objects`: `{c, r, k, note, ...}` met per soort eigen velden), de maskers
(`maskers`), de zwarte cellen (`zwart`), de vrije zwarte vormen (`vormen`), en wat er geselecteerd
is (`sel`, `selMask`, `selVorm`). Eén cel is 175 wereld-px breed (`MK_CEL_PX`) en 150 eenheden
hoog (`MK_CEL_EENH`), ongeveer één sprong.

De palet-categorieën staan in `MK_CATS`, de gereedschappen in `MK_TYPES` (een terreincel heeft
een letter `ch` voor de export, een voorwerp `obj: true`). De vijanden staan in `MK_VIJANDEN`, met
varianten voor de bandiet en de schildbandiet, en de knoppen per vijand in `MK_VIJ_KNOP`.
Een vijand staat op het grid, in het palet (`mkStaal` met een soort) en op de plakstempel als het gekleurde
rondje van zijn soort met een icoon erin (`mkVijIcoon`, met `mkVijBadge` voor het badge rechtsonder): een
tekening in canvas-lijnen op schaal van de cel, dus scherp op elke zoom. De varianten en de knoppen die aanstaan
(`params.n`, `params.over`) zie je aan het badge, de elite aan een gouden ring, de gehurkte bandiet aan een
platgedrukt rondje en de makkelijke schildbandiet aan een schild zonder vulling. De minimap blijft een rood
puntje per vijand.

| wat | functies |
| --- | --- |
| tekenen | `mkTeken` (alles, elke keer opnieuw), `mkCelOp` (welke cel onder de muis) |
| schilderen | `mkKlik` (een klik), `mkVerf` en `mkVerfCel` (een streek, met Bresenham tussen de cellen), `mkRect` (Shift+slepen vult een rechthoek), `mkVul` (Alt+klik, de vulemmer), `mkIsStreek` |
| selecteren | `mkObjOp` (het voorwerp op een cel, ook op de balk van een breed platform, een rijzer of een overhang), `mkNotePaneel` (het paneel rechts), `mkVulVijKnoppen`, `mkVulZegel`, `mkVulRijs`, `mkVulRijsSelect`, `mkVulOver`, `mkVulRichel` |
| een gebied | `MK.gebied` (Shift+slepen in Selecteren), `mkKopieer`, `mkKnip`, `mkGebiedWis`, `mkSpiegel`, `mkPlakStart` en `mkPlakZet` (de stempel `mkPlak` volgt de muis), het klembord `mkKlembord` |
| maat | `mkZetMaat`, `mkRijBoven`, `mkRijOnder` (rijen erbij of eraf; `mkRijRefSchuif` schuift alles mee, ook maskers, zwarte cellen en vormen) |
| opslaan | `mkNaarJSON` en `mkUitJSON` (het grid-formaat, `MK_VERSIE`), `mkBewaar` (wacht 250 ms) en `mkBewaarNu` (de autosave in `localStorage['amir-mk']` plus een stap in de geschiedenis) |
| ongedaan maken | `mkHist`, `mkHistZet`, `mkHistNaar`, `mkOngedaan`, `mkOpnieuw` (`MK_HIST_MAX` stappen, hele grids als tekst) |
| controle | `mkControle` (de meldingen), `mkControleToon` (het paneel), `mkNaarCel` (naar een cel springen, met `mkFlits`) |
| spelen | `mkNaarLevel(opt)` (het grid naar het spelformaat; `opt.vanaf` zet Amir op een andere kolom), `mkTest` en `mkTerug` (die ook de laadpoort sluit), `mkSpelExport` (de Spel-JSON), de knop Test vanaf hier (`#mktestvanaf`, op de linkerbovencel van het gebied) |
| minimap | `mkMiniTeken` (het hele grid klein, linksonder; de cellen in een buffer van een pixel per cel, `mkMiniVuil` na elke wijziging), `mkMiniNaar` (klikken of slepen brengt die plek in beeld), M verbergt hem |
| openen en sluiten | `mkOpen` (met het versieslot op de autosave), `mkDicht` |

**Ongedaan maken** werkt per gebaar: elke keer dat de Maker iets wegschrijft (`mkBewaarNu`) is
een stap, en `mkBewaar` wacht een kwart seconde, zodat een hele streek, een hele sleep of een
schuifje dat je verschuift één stap is. Een nieuwe muisbeweging legt de vorige wijziging eerst
vast. Terug laden gaat met `mkUitJSON`, maar de zoom, het schuiven, het gereedschap en het palet
blijven staan. Tijdens het terugladen staat `mkHistStil` aan, zodat dat zelf geen stap wordt. Staat de
controle open, dan wordt die lijst na ongedaan maken ook ververst.

`mkUitJSON` leest eerst alles (en gooit bij rommel een fout) en overschrijft `MK` pas daarna, zodat een
kapot bestand het grid niet half geladen achterlaat. Wat buiten de maat valt (een voorwerp, een masker-cel,
een zwarte cel, de start) leest hij niet, en een vijand-soort telt alleen als hij echt in `MK_VIJ_INFO` staat
(`hasOwnProperty`, dus geen `constructor`). Sluit je het tabblad binnen die kwart seconde, dan bewaart
`pagehide` de laatste wijziging alsnog. Overal staat `mkBewaar()` vóór `mkTeken()`, want `mkBewaar` zet
`mkMiniVuil`, en anders liep de minimap een tekenbeurt achter.

**Een gebied** is een rechthoek cellen die je met Shift+slepen in Selecteren kiest. Het klembord
is een losse kopie: de cellen, de voorwerpen (met hun plek ten opzichte van de linkerbovenhoek, en
een doelhoogte of wiel-koppeling als die in het gebied valt), de masker-cellen op naam en de
zwarte cellen. Plakken (Ctrl+V of de knop) is een stempel die de muis volgt; een klik zet hem
neer, en het geplakte stuk is daarna het gebied (alleen het deel binnen het grid, `mkGebiedKlem`). Wat
er al op de geplakte cellen stond gaat weg, net als bij Wis, anders stapelden de voorwerpen zich op.
Spiegelen (H) keert het klembord om: een richel wijst de andere kant op (en zijn X-bijstelling keert mee),
de paal van een platform gaat naar de andere kant (rechts is "geen veld", links is `stamZij: -1`, en het
klembord bewaart alleen die vorm, zodat twee keer spiegelen het origineel geeft).

Het gebied schuift mee met een rij erbij of eraf (`mkRijRefSchuif`) en krimpt mee bij verkleinen, plakken
over de rand of Alles wissen (`mkGebiedKlem`, aangeroepen uit `mkZetMaat` en `mkNaMaat`). De rij van de
grondlijn kan niet weg: `mkRijBoven(-1)` weigert bij grondlijn 0 en `mkRijOnder(-1)` bij de grondlijn
onderaan, anders schoof de inhoud een rij ten opzichte van de grondlijn. Een leeg Breed- of Hoog-veld laat
de maat staan.

**De balk** loopt op een smal scherm over twee regels; de legenda, het podium en het paneel
schuiven mee via `--balkh` (een ResizeObserver op `#mkbalk`). Vanaf 1560 px past alles op een
regel, daaronder valt de titel weg.

## Van grid naar level (`mkNaarLevel`)

Altijd WYSIWYG: links in het grid is links in het spel, de wereld-x is `(kolom - startkolom) * 175`.

- Een ravijn-cel op de grondlijn is een gat (`gaps`); elders doet een ravijn-cel niets (de controle
  meldt het).
- Een blok vaste cellen boven de grondlijn is een terras (`terraces`, savanne met `grond: true`,
  rots en muur met `af: true`); een blok met lucht eronder is een zwever (`zwevers`). Een muur die
  op de grondlijn doorloopt gaat precies die ene cel de grond in (`door`).
- Een terras, mesa of muur op het oppervlak boven een gang staat op de savanne, niet in de gang eronder.
  Voor Amir was dat al zo (`updateJump`); voor een vijand in de gang ook: hij loopt eronderdoor
  (`blocksMonster`, en `vloerBij` tilt hem niet naar de top via `terrainHGang`), hij ziet je erdoorheen
  en de lichtkaart maakt de gang er niet donker (`lkVastPunt`, ook via `terrainHGang`). Eerst was zo'n
  kolom voor hem een muur tot op de gangvloer: de schildman bleef er in zijn wacht staan.
- Gang-cellen onder de grondlijn zijn een holte (`holtes`), minstens 3 cellen diep; de ingang teken
  je zelf als ravijn op de grondlijn. Een vaste cel in de gang is een trede op zijn diepte; de
  gangvloer komt uit de holte (`gangVloer`), niet uit de kolom zelf, zodat een trede op de onderste
  rij ook meetelt. Zwarte tegels onder de grond zijn zwevende zwarte blokken op hun hoogte.
- Een kei-cel (`laag`, letter L) is een kei om op te springen (`rocks`, schaal 1), een schuilplek
  voor slangen en panters (regel 7).
- Voorwerpen: overhang naar een zwever, richel naar `ledges` (met `look` als de kleur niet steen is), kalebas naar `hppotions`, platform
  met doel plus zijn tandwielen naar `takels` (met `stam: true`), zegel en rune met een masker naar
  `zegels`/`runes` plus `acties`, een verborgen zegel ook zonder masker, en een zegel of rune die een
  rijzer stuurt ook (met `rijs`).
- Een **rijzer** (Objecten, "Rijzer (grond die stijgt)") is de rijzende grond uit het spel (zie
  `notities/rijzende-grond.md`): een blok steen dat op een zegel uit een ravijn omhoog komt. Hij werkt als het
  platform: zijn rij is waar hij begint (in rust, diep in het ravijn), **Zet doelhoogte** is tot waar hij komt
  (de grondlijn, of hoger als lift naar een terras), en **Breedte** is zijn breedte in cellen (1 tot 5, hetzelfde
  schuifje als het platform). Klik je met het gereedschap op het ravijn op de grondlijn, dan is die cel zijn doel
  en rust hij `MK_RIJS_DIEP` (3) cellen eronder; klik je in de diepte, dan rust hij daar en komt hij tot de
  grondlijn. Zijn cellen liggen om de ankercel (`mkRijsCellen`, bij een even breedte net links van het midden),
  zodat de randen op celranden vallen en het blok in het spel naadloos tegen de ravijnrand sluit (`rijsTeken`
  tekent de grondrand over de hele breedte, dus elke breedte ziet er goed uit; een smaller blok krijgt donkere
  zijkanten). `mkNaarLevel` maakt er `rijzers` van (`r1`, `r2`, ..., `mkRijsNr`), met `van` en `tot` uit de rij
  en het doel maal 150, een bovenkant van 0 wordt `RIJS.tot` (-1), en de rand wordt op de rand van het
  geexporteerde gat gezet als die een halve pixel verschilt (een gat met een oneven breedte heeft een afgerond
  midden). In het paneel: **Snelheid** (`v`), **Wacht** (`wacht`), **Boven** (`duur`, 0 = hij blijft boven) en
  **Zakt onder je weg** (`zak: true`: dan staat hij op zijn rij en zakt hij naar zijn doel zodra Amir erop staat,
  zonder doel 3 cellen; geen zegel nodig), **Look** (`look`: savanne, rots, sneeuw of zwart, rond; `MK_RIJS_LOOKS`)
  en **Zet kleurhoogte** (`mkKleurMode`, een klik op een rij: `kleur: {r}`, in het spel `kleurVanaf`; daaronder
  blijft het blok zwart, een stippellijn over het blok op de kaart, **Wis kleurhoogte** haalt hem weg). Een zegel of rune krijgt het keuzemenu **Stuurt rijzer**
  (`mkVulRijsSelect`): de koppeling is een verwijzing naar het voorwerp (`rijsObj`, `mkRijsVan`), opgeslagen op
  celpositie (`rijzer: {c, r}`, zoals een wiel zijn platform) en in het klembord als `rijsRel`. Spiegelen schuift
  het anker van een rijzer met een even breedte een cel op, zodat zijn cellen op hun plek blijven, en zet de
  koppeling opnieuw. Op de kaart: het blok met een pijl (omhoog, of omlaag bij een zakker), een vage balk op het
  doel met een stippellijn, en een stippellijn van elk zegel naar zijn rijzer. Een zegel op de grondlijn
  boven een gang krijgt `dak: true` en `readLevel` neemt dat over (eerst viel het daar weg, en lag het
  zegel toch op de gang-bodem).
- Vijanden via `mkSpawn`: de soort-tekst (`bandiet:dolk`, `kooiman:vogel`, `schildman:makkelijk`)
  wordt de spawn met zijn vlaggen; een vijand op een laag krijgt `boven: true`, in een gang `y`. Ook op het
  dak van een gang (op of boven de grondlijn, met een holte eronder) krijgt hij `boven: true`: `bovenVloer`
  klemt daar op 0, terwijl `terrainH` de gang-bodem gaf. Een kalebas op dat dak krijgt om dezelfde reden
  `y: 0`. Een kei op het dak van een gang zakt nog wel naar de gang-bodem (`rocks` kent geen hoogte).
- Een panter rechts van de start komt niet meteen: de spawner wil eerst dat Amir aan zijn rechterkant is
  geweest (`sp.armed`), en pas als hij zijn plek naar links voorbijgaat verschijnt hij. De echte levels
  merken daar niets van, want daar staat elke panter links van de start.
- De Test zet Amir bovenop een mesa als de start daarop staat (`restart` neemt bij `mkTestActief` altijd
  `terrainH`). Een start onder of op een zwever niet: daar begint hij op de grond eronder.
- Het dakgat voor een lift komt alleen voor een platform dat in de gang staat of erheen reist (zijn rij of
  zijn doel onder de grondlijn), en niet waar je zelf al een ravijn tekende.
  De knoppen uit `MK_VIJ_KNOP` gaan alleen mee als ze van de standaard afwijken; een vinkje als
  `true` of `false` (readLevel kijkt op `=== false`, dus 0 zou daar misgaan).
- De basisvelden: `view: 0.8`, `zicht: true`, `hpBalk: true`, `speerInHand: true`, `rugMax: 1`,
  `valDood: 600` (vier cellen), `kaleKlif`, `voorgrond: false`, `overloop: true`.

## De knoppen per vijand (`MK_VIJ_KNOP`)

Alleen velden die het spel echt leest:

| vijand | knop | op de spawn |
| --- | --- | --- |
| zandslang, zwarte slang, knockslang | Snelheid (0,4 tot 2) | `speed` |
| hyena | Aantal (1 of 2) | `n` |
| bandiet (alle varianten) | Vault over een kei naar je toe (standaard aan) | `vault: false` als uit |
| panter | Komt over keien en ravijnen (standaard uit) | `over: true` als aan |
| elke vijand | Ziet je alleen met vrij zicht (standaard aan) | `zicht: false` als uit |

Het vinkje voor de panter en het uitzetten van de vault zijn de uitzondering op regel 7, als
bewuste keuze van wie het level maakt. Een knop erbij is een regel in `MK_VIJ_KNOP` (schuifje:
`min`, `max`, `step`; vinkje: `vink: true`) plus het veld in `readLevel`.

## De controle (`mkControle`)

De knop **Controle** in de balk. Een lijst meldingen rechtsonder op de kaart, klikbaar (springt
naar de cel), die bijblijft zolang hij open staat. Drie soorten:

- **FOUT**: geen start of eind, een start of eind boven een ravijn zonder bodem of in een vaste
  cel, een vijand in een vaste cel of onder de grond zonder gang, een platform zonder doelhoogte,
  een tandwiel zonder platform, een rijzer die niet helemaal in een ravijn op de grondlijn staat, buiten het
  grid steekt of geen zegel of rune heeft die hem stuurt (een zakker mag overal en heeft er geen nodig).
- **LET OP**: een start of eind die hoog boven zijn vloer hangt, een vijand die zweeft of op de
  start staat, een ravijn of gang op de verkeerde rij, een gang zonder ingang, een platform zonder
  tandwiel of met zijn doel op dezelfde hoogte, een zegel dat naar een weg masker wijst, een val
  van meer dan vier cellen naast een rand (dodelijk in de Test), een rijzer met zijn doel op zijn eigen rij, die
  op of boven de grondlijn rust, of die drie of meer cellen ravijn naast zich open laat, en een zegel dat een
  zakker stuurt.
- **info**: een prop (de Test tekent hem niet), een zegel of rune zonder masker of rijzer (alleen een
  aantekening), een rijzer zonder duur die het hele ravijn vult (het ravijn is daarna voorgoed dicht, dus geen
  schuilplek meer, regel 7).

De vloer onder een cel (`vloerOnder`): boven de grondlijn val je door lucht; een ravijn op de grondlijn is
de ingang van een gang eronder en anders bodemloos (FOUT); een gang is open tot zijn vloer, de eerste
cel die geen gang is; een gang tot de onderrand heeft zijn holte-vloer eronder (rij `R`). Al het andere
op of onder de grondlijn is grond. "Onder de grond zonder gang" kijkt naar de eigen cel van de vijand.

Het is alleen wat uit het grid zelf af te lezen is. Sprongen, bereik en de speer kijkt
`tools/levelcheck.py` na: druk op **Spel-JSON** en geef die tekst als bestand aan levelcheck of de
speelrobot. Levelcheck kent een lift uit de Maker (een platform in het gat boven een gang dat van
de bodem tot de grondlijn reist, `takels`) als weg omhoog uit die gang (`liften_in`).

## Sneltoetsen

Escape (selecteren, deselecteren), spatie (schuiven), Delete (voorwerp of vorm weg), Ctrl+Z en
Ctrl+Y (ongedaan en opnieuw), Ctrl+S (exporteren), F (passend), T (testen), + en - (zoomen),
pijltjes (schuiven, met Shift sneller), M (de minimap), Shift+slepen (rechthoek; in Selecteren een gebied),
Alt+klik (een aaneengesloten vlak vullen), Ctrl+C,
Ctrl+X en Ctrl+V (kopiëren, knippen, plakken), H (het klembord spiegelen), Delete (het gebied
leegmaken). Op een keuzelijst, knop of tekstvak blijven de toetsen van dat veld.

## De makertest: `tools/makertest.js`

Laadt de Maker in Chromium met een proefgrid waar alles op staat (gat, gang met treden, mesa,
zwever, muur door de grond, sneeuw, alle voorwerpen, een tweede ravijn met een rijzer van 2 breed die het zegel
stuurt, een masker, een zwarte cel, een vorm) en
kijkt na: de round-trip van export en import, de vertaling naar een spel-level, rijen invoegen en
weer weghalen, verkleinen, snel schilderen, de rechthoek, het aanklikken van brede voorwerpen,
ongedaan maken, een gebied kopiëren, spiegelen, plakken en knippen, een rijzer van even breedte spiegelen met
zijn zegel eraan, de minimap en Test vanaf hier, de vijand-knoppen, de controle, de Test starten en teruggaan,
de autosave, en of
het proefgrid als spel-level door `levelcheck.py` komt. Draai hem na elke wijziging aan de Maker.

```
node tools/makertest.js                alle controles
node tools/makertest.js --alleen rij   alleen de controles waarvan de naam dit bevat
node tools/makertest.js --shots map    daarna een schermafdruk van de Maker en van de Test
```

Het proefgrid staat in het script (`proefGrid`). Een nieuwe mechaniek in de Maker krijgt er een
regel bij, en een controle in de lijst `check(...)`.

## Wat er nog niet is

Geen aanraking (pannen en zoomen kan
alleen met muis en toetsen), geen prop-keuze (een prop is een aantekening), en een zegel kent
alleen een masker, Verborgen en een rijzer, niet de andere zegel-velden (`speerval`, `plafond`). Een rijzer
staat alleen in een ravijn op de grondlijn: een rijzer in een put onder de grond of een lift die vanaf de
gangvloer door de ingang omhoog komt is in het spel niet beproefd, en de Maker meldt zo'n plek als FOUT.

Bekende randen, nog niet opgelost: alleen de tegel Zwevende laag (F) en Zwart plafond zweven, een blok rots
of savanne met lucht eronder wordt een pilaar tot de grond; de holte is aan de startkant een cel breder dan
getekend (`gangRx + MK_CEL_PX`); `boven` leest het spel niet voor kooiman, meelman, fosfor, hyena en
panter, en `y` niet voor scorp, bandiet en schildman; de knop Zicht doet niets voor panter, kooiman (duel)
en `bandiet:hurk`; één rotscel op de grondlijn maakt de hele bodem kale rots.
