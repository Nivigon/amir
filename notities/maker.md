# De Level Maker nieuwstijl

De knop **Maker nieuwstijl** in het startmenu. Een los grid om de ruwe vorm van een level te
schetsen en meteen te spelen. Staat helemaal op zichzelf: het raakt de spel-loop, de levels
(regel 1) en de oude bouwer niet aan. De sectie in de HTML heet `// ---------- Level Maker ----------`.

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
| selecteren | `mkObjOp` (het voorwerp op een cel, ook op de balk van een breed platform of een overhang), `mkNotePaneel` (het paneel rechts), `mkVulVijKnoppen`, `mkVulZegel`, `mkVulOver`, `mkVulRichel` |
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
blijven staan. Tijdens het terugladen staat `mkHistStil` aan, zodat dat zelf geen stap wordt.

**Een gebied** is een rechthoek cellen die je met Shift+slepen in Selecteren kiest. Het klembord
is een losse kopie: de cellen, de voorwerpen (met hun plek ten opzichte van de linkerbovenhoek, en
een doelhoogte of wiel-koppeling als die in het gebied valt), de masker-cellen op naam en de
zwarte cellen. Plakken (Ctrl+V of de knop) is een stempel die de muis volgt; een klik zet hem
neer, en het geplakte stuk is daarna het gebied. Spiegelen (H) keert het klembord om: een richel
wijst de andere kant op, de paal van een platform gaat naar de andere kant.

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
- Gang-cellen onder de grondlijn zijn een holte (`holtes`), minstens 3 cellen diep; de ingang teken
  je zelf als ravijn op de grondlijn. Een vaste cel in de gang is een trede op zijn diepte; de
  gangvloer komt uit de holte (`gangVloer`), niet uit de kolom zelf, zodat een trede op de onderste
  rij ook meetelt. Zwarte tegels onder de grond zijn zwevende zwarte blokken op hun hoogte.
- Een kei-cel (`laag`, letter L) is een kei om op te springen (`rocks`, schaal 1), een schuilplek
  voor slangen en panters (regel 7).
- Voorwerpen: overhang naar een zwever, richel naar `ledges`, kalebas naar `hppotions`, platform
  met doel plus zijn tandwielen naar `takels` (met `stam: true`), zegel en rune met een masker naar
  `zegels`/`runes` plus `acties`, een verborgen zegel ook zonder masker.
- Vijanden via `mkSpawn`: de soort-tekst (`bandiet:dolk`, `kooiman:vogel`, `schildman:makkelijk`)
  wordt de spawn met zijn vlaggen; een vijand op een laag krijgt `boven: true`, in een gang `y`.
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
  een tandwiel zonder platform.
- **LET OP**: een start of eind die hoog boven zijn vloer hangt, een vijand die zweeft of op de
  start staat, een ravijn of gang op de verkeerde rij, een gang zonder ingang, een platform zonder
  tandwiel of met zijn doel op dezelfde hoogte, een zegel dat naar een weg masker wijst, een val
  van meer dan vier cellen naast een rand (dodelijk in de Test).
- **info**: een prop (de Test tekent hem niet), een zegel of rune zonder masker (alleen een
  aantekening).

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
zwever, muur door de grond, sneeuw, alle voorwerpen, een masker, een zwarte cel, een vorm) en
kijkt na: de round-trip van export en import, de vertaling naar een spel-level, rijen invoegen en
weer weghalen, verkleinen, snel schilderen, de rechthoek, het aanklikken van brede voorwerpen,
ongedaan maken, een gebied kopiëren, spiegelen, plakken en knippen, de minimap en Test vanaf
hier, de vijand-knoppen, de controle, de Test starten en teruggaan, de autosave, en of
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
alleen een masker en Verborgen, niet de andere zegel-velden (`speerval`, `rijs`, `plafond`).
