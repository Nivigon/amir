# Water

Een materiaal voor al het water: `WATER` in de kop `// ---- water: één materiaal voor plas, poel, rivier, waterval en bron ----`.
Proefstuk: **Test 67: Water** (geen vijanden, `vredig: true`). De oude poel (`POOL`, het veld `water`, een plaat met het
water erin geschilderd) staat er nog los naast en is nog niet overgezet.

## Het idee

Elke vorm water gebruikt dezelfde lagen, en alleen de vorm en de stroming verschillen. Zo past een nieuwe vorm vanzelf
bij de rest. Er zijn geen plaatjes: alles wordt getekend.

1. **Lijf**: een verloop van de verre kant (de horizonkleur van het uitzicht erin, `WATER.lucht`) naar de diepte vooraan.
2. **Rimpels**: twee naadloze texturen (`waterTextuur`, licht en donker), eenmaal getekend en daarna alleen verschoven, elk
   een andere kant op. Bij stromend water schuiven ze mee met de stroming.
3. **Glinsters**: vaste plekjes die flonkeren (`WATER.glinster`), vooraan iets groter.
4. **Rand**: een natte donkere rand om de oever, een schaduwrand onder de verre oever, en een gebroken schuimlijn.
5. **Regen**: bij `weerNu.regen` komen er ringen op elk water (`waterRingen`).

Het palet komt uit de oude poel (`WATER.palet`): diep, midden, ondiep, glans, schuim en nat zand. 's Nachts en in de
avond kleurt de lichtlaag het water mee, net als de rest van de wereld.

## De vormen (`wateren: [{k, x, w}]`)

| `k` | wat | diepte |
| --- | --- | --- |
| `plas` | een ondiepe platte ovaal | 0,28: je spettert, maar loopt bijna even snel |
| `poel` | een grotere kom | 1: wegzakken, trager, lager springen |
| `rivier` | een band die van achteren naar de camera stroomt en kronkelt (onder een brug recht) en vooraan over de lip van de grond langs de wand naar beneden valt. Standaard rustig: trage rimpels en een trage val (`vRustig`, `valRustig`); met `val: true` stroomt en valt hij snel, zoals in Test 67. Met `voor: true` (proef, nog in geen level) valt hij niet maar loopt hij door naar de camera tot onder uit beeld, zoals het pad van een kruispunt | 0,9 |
| `val` | een waterval van de rechterkant (`r`) van het terras op `x`: een beekje op het bovenvlak (`waterTerrasTeken`), het gordijn voor Amir langs (`waterVoorTeken`) en een kom eronder (`kom` keer `w` breed) met schuim en stuifwater | 0,6 in de kom, ondiep bij de wand zodat je het terras op komt |
| `bron` | een kom met een straal (`hoog` in Amir) en een kroon van druppels | 0,5 |
| `fontein` | decor voor de stad: een geschilderde plaat van leem met het water erin (zie hieronder) | 0 |

## De fontein (`k: 'fontein'`)

`WATER.soort.fontein`, `fonteinLaad`, `waterFonteinTeken`, `waterPlats`, `waterFonteinSlag`, `waterFonteinPlons`, `waterStraal`, `sbfontein`

Een fontein van leem voor het plein: een rond bassin, een zuil en een schaal, als plaat (`design/stad/fontein.png`, uit de
Grok-plaat `design/stad/bron/fontein.webp` met `tools/fontein_knip.py`, met de put als stijlreferentie). Het bouwwerk is
geschilderd en het water komt uit dit materiaal: het oppervlak in de opening van het bassin (de zuil wordt er daarna nog eens
overheen getekend), het water in de schaal, twee slierten die over de schaal in het bassin lopen, de straal (`waterStraal`,
gedeeld met de bron), de druppels en het geruis. Alles achter Amir, na `stadVoorTeken`. De maten staan in px van de plaat
(`binnen`, `bassin`, `zuil`, `schaal`, `over`); `amir` maakt de rand even hoog als die van de put.

- **Decor, geen water om in te lopen** (diep 0, `waterenDiep` slaat hem over): je loopt er voorlangs. De rand is een lage
  trede over de hele breedte (`waterPlats`, in `platsNear`), zoals de put, dus je loopt er ook overheen.
- **Slaan in het water**: een steek of de lage zwaai waarvan de punt bij het water komt (het bassin, of vanaf de rand de
  schaal) geeft een plons: een kroon van water die opspringt (`waterPlonzen`), spetters, twee ringen en het plonsgeluid. Het
  water houdt de speer niet tegen, en per vak komt er hooguit elke `plons` (0,3) seconde een.
- Eerst getekend in code (een ring, zuil en schaal van vlakken): dat paste niet bij de geschilderde stad, vandaar de plaat.
- **Sandbox**: onder De stad de knop **Fontein**: het plein met de fontein in het midden. Geen level heeft hem nog.

De diepte telt mee in `waterDepthAt`, dus de spetters, het watergeluid, het wegzakken en de speer die in het water verloren
gaat werken voor elke vorm zoals bij de oude poel.

## De brug (`brug: true` op een rivier)

`BRUG`, `brugTeken`, `brugIn`. Een rivier met `brug: true` krijgt een houten brug op straathoogte: de galerij van de stad
(`galerij.png` via `stadStrook`, links, het midden zo vaak als nodig, rechts) met het midden van de planken op de looplijn
en zonder palen. De zware onderbalk ligt op het water, de rivier stroomt eronder door en valt ervoor over de rand.
De brug ligt aan elke kant `BRUG.oever` (0,3 Amir) op de oever. Onder een brug kronkelt de rivier niet (de bocht stak
anders als een los blauw stuk achter de leuning uit).

De brug is een gewoon onderdeel: een nieuw level (met toestemming, regel 3) mag hem gebruiken.

- **Droog**: `waterenDiep` slaat een rivier met een brug over, dus op de brug zak je niet weg, de speer gaat niet
  verloren en vijanden lopen er gewoon overheen. Het geruis blijft.
- **De stoep**: `stadStoep` slaat elke rivier over (net als een ravijn). Eerst schilderde hij straat over de achterkant
  van het dek, zodat er een laag zand tussen de leuning en de planken lag.
- **Laden**: het plaatje hoort bij de stad; `stadLaadLevel` laadt de stadsplaatjes ook in een level met een brug (`brugIn`).
- **Getekend** na de stoep (`brugTeken` in de tekenlus, achter Amir), dus de leuning staat achteraan en Amir loopt ervoor.
- **Sandbox**: onder De stad de knoppen **Brug** (een straat met een rivier ertussen en de brug erover) en **Brug met
  bandiet** (dezelfde, met een bandiet aan de overkant die over de brug op je af komt). **Weg** haalt de brug mee weg.

In **Test 69: De brug**: een stadsstraat met een rivier met brug (een bandiet erop) en een zonder, om het verschil te voelen. Een rivier op een plek zonder brug blijft gewoon water: de looplijn is een lijn, dus een brug
neemt de plek van het water in en je kunt er niet naast het water in stappen.

## Wat er beweegt

- `waterStap(dt)`: de klok (speltijd, stil in de pauze), de druppels (`waterDruppels`, als streepjes in hun vliegrichting),
  de regenringen, de spetters op Amir onder een val of straal, en het geruis.
- Het geruis (`waterGeluid`): een lus bruine ruis door een laagdoorlaat, harder naarmate je dichter bij een rivier, val of
  bron staat (`WATER.geluid`).

## Volgende stappen

- Het stijlblad vastleggen nu het proefstuk er staat (wat werkt, welke getallen).
- De oude poel overzetten op dit materiaal (daar is een droge kuil voor nodig in plaats van de plaat met water).
- Winter: hetzelfde materiaal als ijs.
- Sandbox-knoppen en de Maker, als het materiaal goed is bevonden.

## De spetters van Amir (`SPETTER`)

Landen in het water en door water lopen gaven vroeger de plaatjes `spetter_01..08` en `rimpel_01..08`. Nu tekent het
spel ze zelf, in de kleuren van `WATER.palet` (`SPETTER`, `splashAt`, `updateSplashes`, `drawSplashes`):

- **plons** (landen, `splashAt`): een doorzichtig zuiltje dat omhoog schiet en terugzakt, een druppel die van de top
  losschiet, twee kringen, schuim en acht druppels die terugvallen met een kringetje.
- **spat** (lopen): lage spatjes achter de voet weg, een kleine kring en wat schuim.
- **kring** (stilstaan): alleen een kring.

`SPETTER.maat` is de grootte (een eenheid is zoveel `CHAR_H`), `SPETTER.nieuw: false` zet de oude plaatjes terug.
In de sandbox, tabblad Terrein, rij **Water**: **Poel** en **Plas** zetten water voor Amir neer, **Spetter nieuw/oud**
wisselt tussen de nieuwe en de oude.
