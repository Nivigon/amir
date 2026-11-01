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

Het palet is een boom die zichzelf bouwt (`mkPaletBoom` naar `MK_PALETTEN`, een boom per stand, zie "Savanne en Stad"): zes categorieën (`MK_CATS`: Terrein,
Start/eind, Vijanden, Objecten, Decor, Verbergen) met daarin groepen (`MK_GROEPEN`, elke groep op een pad zoals
`objecten/takel` met zijn naam), en in een groep de gereedschappen of weer groepen, zo diep als nodig (Vijanden,
Bandieten, Bandiet, zijn varianten). Een gereedschap in `MK_TYPES` zegt met `groep` waar het staat (een pad; alleen een
categorie-id betekent los in die categorie, zoals de kalebas onder Objecten); een vijand in `MK_VIJANDEN` met `groep` in
welke groep uit `MK_VIJ_GROEPEN`, en een vijand met varianten (bandiet, schildbandiet, kooiman) is daarbinnen een groep.
Een gereedschap zonder `groep` landt in Overig van zijn categorie (uit zijn soort, `mkPaletCatVan`), een onbekend pad maakt
een groep zonder naam; `mkPaletKlachten` meldt dat, net als een knoop met meer dan `MK_PALET_MAX` (6) items, en
`mkPaneelKlachten` telt hetzelfde voor het paneel rechts (de zichtbare rijen buiten en binnen elk inklapbaar kopje). De
makertest (controle `maat`) geeft FOUT op elke klacht, en kijkt ook of de klachten echt komen. Elke knoop kent zijn `pad`;
`mkPaletKnoopOp(pad)` en `mkPaletZoek(tool, soort)` zoeken erin. De linkerkolom (`mkLegenda`, `mkLegRijen`) toont de
groepen van de gekozen categorie dichtgeklapt met één keten open (`MK.sub`, de groep-ids onder `MK.cat`; `null` betekent:
de groep van het gereedschap dat aanstaat, anders de eerste); een klik op een groep klapt hem open of dicht (`mkKies`), een
gereedschap kiezen zet zijn groep open. Het zwevende menu onder een categorieknop (`mkMenuToon`, `mkMenuVul`) klapt per
groep opzij uit in een laag dieper (`mkFlyToon`, de lagen in `mkMenuLagen`, zo veel als de boom diep is; een laag die
rechts of onder uit het venster steekt schuift terug). De knoppen per vijand staan in `MK_VIJ_KNOP`. De keuzelijsten Soort
(bij een vijand) en Vijand eruit (bij een poort) volgen dezelfde groepen (`mkVijOpties`, een `optgroup` per groep).

Het paneel rechts van een poort is in drie inklapbare kopjes verdeeld (`details.mkklap`: Uiterlijk, Vijand en hek,
Rotswand), dat van een rijzer in twee (Tempo, Kleur). De eerste keer staat open wat in gebruik is, daarna onthoudt
`mkKlapStaat` wat je zelf open- of dichtklapte (`mkKlapZet`, aangeroepen uit `mkVulPoort` en `mkVulRijs`).
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
- Rotsdecor (`rotsdecor`, onder Decor) wordt een prop `{x, k, s, f}` op het midden van zijn kolom, `k` een
  rotsstuk uit `PROPS` (de soorten met `rots`). Het spel zet hem zelf op de vloer onder die kolom (`terrainH`),
  dus de rij doet er alleen toe voor de controle. Het paneel heeft Soort (per familie: zuil, plaat, laag, brok,
  kei), Gespiegeld en Schaal (`MK_ROTS_S`); de laatst gekozen soort onthoudt hij (`MK.rotsSoort`).
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
  `zegels`/`runes` plus `acties`, een verborgen of onzichtbaar zegel ook zonder masker (Te zien), en een zegel of rune die een
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
- Een **poort** (Objecten, "Poort (stenen boog)") wordt een `poorten`-entry (`b1`, `b2`, ...) met de onderkant
  van de opening op de onderkant van zijn cel; op een laag of op het dak van een gang met `y`. Het hek, de schaal, de
  regie (met `bij` als regiepunt) en de rotswand (`wand`, `wandF`, `wandH`, `wandX`) gaan mee. Met een vijand erin
  komt die als spawn met `poort` mee (via `mkSpawn` op de cel van de poort, zo vaak als **Aantal**), en een zegel of
  rune met **Opent poort** krijgt `poort`. Zie `notities/poort.md`.
- De **stadsstukken** (gevel, kraam, voetdecor, paleis, galerij, trap; zie "De losse stukken van de stad" en "De
  gekoppelde stukken: galerij en trap" hieronder) worden het veld `stad` (`{seed, gevels, kramen, voet, paleis, galerijen,
  trappen}`), alleen als er minstens een in het grid staat. Met dat veld is de basis
  van de bodem de straat (`bodemPic`), dus dan krijgen savanne- en sneeuwcellen op de grondlijn ook een eigen strook
  `grondSoort` met soort `savanne`, en ligt de straat alleen waar je straat schilderde.
- Vijanden via `mkSpawn`: de soort-tekst (`bandiet:dolk`, `kooiman:vogel`, `schildman:makkelijk`)
  wordt de spawn met zijn vlaggen; een vijand op een laag krijgt `boven: true`, in een gang `y`, en op een dak, galerij of
  balkon van de stad `dak` (zie "Vijanden op daken en de meldingen van de stad"). Ook op het
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
- Zonder een enkele spawn (ook niet in een poort) komt er een zandslang ver achter het eind bij, anders stuurde het
  spel vrije slangen; een level met alleen poortvijanden krijgt die niet.
- De basisvelden: `view: 0.8`, `zicht: true`, `hpBalk` (de lijst `MK_HP_SOORTEN`), `speerInHand: true`, `rugMax: 1`,
  `valDood: 600` (vier cellen), `kaleKlif`, `voorgrond: false`, `overloop: true`.
- `hpBalk` is in de Maker een lijst, geen `true`: Amir en de andere vijanden krijgen 3 levens met een balk, maar de
  slangen (zand, zwart, knock en fosfor) staan er niet in en zijn in een klap dood.

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
  een tandwiel zonder platform, een poort in een vaste cel of boven een ravijn zonder bodem, een rijzer die niet helemaal in een ravijn op de grondlijn staat, buiten het
  grid steekt of geen zegel of rune heeft die hem stuurt (een zakker mag overal en heeft er geen nodig).
- **LET OP**: een start of eind die hoog boven zijn vloer hangt, een vijand die zweeft of op de
  start staat, een poort met een vijand maar zonder zegel, rune of regie die hem opent, een regiepunt meer dan
  `MK_POORT_BIJ_VER` cellen van zijn poort (Amir staat stil terwijl de poort buiten beeld opengaat), een ravijn of gang op de verkeerde rij, een gang zonder ingang, een platform zonder
  tandwiel of met zijn doel op dezelfde hoogte, een zegel dat naar een weg masker wijst, een voorwerp dat half in een masker steekt maar zelf te zien blijft (zie Verborgen door masker in `notities/masker.md`), een val
  van meer dan vier cellen naast een rand (dodelijk in de Test), een rijzer met zijn doel op zijn eigen rij, die
  op of boven de grondlijn rust, of die drie of meer cellen ravijn naast zich open laat, en een zegel dat een
  zakker stuurt, een gevel, kraam of voetdecor op grond die geen straat is (de grondlijn-cel op zijn kolom), en een
  straatcel of leemmuur boven de grondlijn zonder straat op de grondlijn eronder (per reeks kolommen een melding; een
  straatterras haalt zijn tegel uit de strook op de grondlijn). Voor de huizen, galerijen, trappen en vijanden op daken
  zie "Vijanden op daken en de meldingen van de stad" (daar staat ook de enige FOUT van de stad: een trap zonder vloer bij
  de uitgang).
- **info**: een prop (de Test tekent hem niet), rotsdecor dat boven zijn vloer hangt (het spel zet hem op de vloer), een poort met regie zonder vijand, een hek dat niets opent, een zegel of rune zonder masker of rijzer (alleen een
  aantekening), een rijzer zonder duur die het hele ravijn vult (het ravijn is daarna voorgoed dicht, dus geen
  schuilplek meer, regel 7).

De vloer onder een cel (`vloerOnder`): boven de grondlijn val je door lucht; een ravijn op de grondlijn is
de ingang van een gang eronder en anders bodemloos (FOUT); een gang is open tot zijn vloer, de eerste
cel die geen gang is; een gang tot de onderrand heeft zijn holte-vloer eronder (rij `R`). Al het andere
op of onder de grondlijn is grond. "Onder de grond zonder gang" kijkt naar de eigen cel van de vijand. Een straatcel is
vast, net als savanne (dat stond er in stap 2 nog niet in, en dan zweefde een vijand op een straatterras in de controle).

Het is alleen wat uit het grid zelf af te lezen is. Sprongen, bereik en de speer kijkt
`tools/levelcheck.py` na: druk op **Spel-JSON** en geef die tekst als bestand aan levelcheck of de
speelrobot. Levelcheck kent een lift uit de Maker (een platform in het gat boven een gang dat van
de bodem tot de grondlijn reist, `takels`) als weg omhoog uit die gang (`liften_in`).

## Savanne en Stad

Bovenaan de legenda staat de schakelaar **Savanne | Stad** (`#mkthema`, `MK_THEMAS`, `mkThemaZet`, `mkThemaToon`;
sneltoets G). Er zijn al zes categorieën (`MK_PALET_MAX`), dus de stad is geen zevende categorie maar een tweede stand
van dezelfde zes. Een gereedschap in `MK_TYPES` met `thema: 'savanne'` of `thema: 'stad'` staat alleen in die stand,
zonder `thema` in allebei. `mkPaletBoom(thema)` bouwt per stand een boom in `MK_PALETTEN`, `mkPalet()` geeft die van
`MK.thema`. Sneeuw staat alleen bij Savanne; de groep `terrein/stad` (nu **Muur van leem**) alleen bij Stad.

De stand filtert alleen het palet: wat al in het grid staat blijft staan en werkt gewoon, ook gemengd. Per stand
onthoudt de Maker je gereedschap (`MK.themaGeheugen`); bestaat dat in de andere stand niet, dan valt hij terug op
de savannegrond. De stand zelf staat los van het grid in `localStorage['amir-mk-thema']`, zodat ongedaan maken hem niet
omzet. `mkPaletKlachten()` en de controle `maat` kijken beide standen na; `mkPaletZoek(tool)` zonder knoop zoekt eerst in
de stand die aan staat en dan in de andere.

**Muur van leem** (`leem`, letter `E`): een blok leemcellen boven de grondlijn wordt een terras met `look: 'leem'`, de
lemen stadsmuur uit `notities/stad.md` ("De leemmuur"). Het botst en draagt als elk terras.

**Grond: straat** (`straat`, letter `A`, groep `terrein/stad`): op de grondlijn een strook `grondSoort` met soort
`straat` (zie `notities/grondsoort.md`); boven de grondlijn telt hij als savanne (een terras van grond, een zwever).
Rots- en sneeuwrots-cellen op de grondlijn worden nu ook zulke stroken (soort `rots`), per plek in plaats van de
oude `afwerking` die de hele bodem omzette; een sneeuwcel geeft nog steeds een dichte sneeuwlaag over de hele
bodem (`sneeuw: {soort: 'savanne', dek: 1, vol: true}`).

### De losse stukken van de stad

`MK_STAD_K`, `mkStadVak`, `mkStadTeken`, `mkVulStad`, `mkStadHeel`, `mkGevelNieuwId`, `mkStadLaad`, `MK_STAD_SCHAAL`

Stap 3 van `notities/plan-stad-maker.md`. Onder Decor in de stand Stad: groep **Huizen** (`decor/huizen`: Gevel) en groep
**Straat** (`decor/straat`: Kraam met rieten dak, Kraam met doek, Voetdecor, Paleis). Het zijn voorwerpen in `MK.objects`:

| stuk | voorwerp | ankercel | paneel (kopje) | naar `stad` |
| --- | --- | --- | --- | --- |
| gevel | `{k: 'gevel', id, hoog, f}` | linksonder | Gevel g1: Hoogte 1 tot 4, Gespiegeld | `gevels: {x, hoog, f}`, x de linkerkant van zijn ankercel |
| kraam | `{k: 'kraam', soort, f}` | midden | Kraam: Soort (riet, doek), Gespiegeld | `kramen: {x, soort, f}` |
| voetdecor | `{k: 'voet', stuk, f}` | midden | Voetdecor: Stuk, Gespiegeld | `voet: {x, stuk, f}` |
| paleis | `{k: 'paleis'}`, een per level | midden | Stad: Andere stad | `paleis: x` |

- **Tekenen** (`mkStadTeken`, voor de andere voorwerpen, van ver naar dichtbij): de echte plaatjes uit `design/stad/`, half
  doorzichtig (`MK_STAD_ALFA`); een gevel gestapeld uit dak, verdiepingen en begane grond zoals `stadTeken`. In het spel
  schaalt een breedte mee met het scherm; de Maker tekent op laptopmaat (`MK_STAD_SCHAAL`, 1280 bij 720 op Formaat 25, de
  maat van levelcheck), zodat een gevel ongeveer 3,1 cellen breed is. Hoogtes liggen vast. De ankercel heeft een dun
  kadertje, een gevel zijn id linksboven, het paleis een stippellijn over het hele grid op zijn kolom.
- **Aanklikken en slepen**: `mkObjOp` vindt een stadsstuk ook op zijn plaatje (voetdecor en kramen voor gevels), en
  slepen houdt vast waar je het pakte (`mkDragOff`), zodat een huis niet naar de muis verspringt.
- **Een eigen id per gevel** (`g1`, `g2`, ...; `mkGevelNieuwId`): het gaat mee in de JSON, en `mkStadHeel` (na laden en
  plakken) geeft een dubbel of leeg id een nieuwe. `mkNaarLevel` zet de gevels van de start af in `stad.gevels` en houdt
  `gevelIdx` (id naar index) bij, voor de galerijen en trappen van stap 4.
- **Het paleis**: een klik met het gereedschap verschuift het bestaande, en `mkStadHeel` laat er na plakken een (het
  laatste). **Andere stad** zet `MK.stadSeed` (in de JSON `stadSeed`, in het level `stad.seed`, standaard 1).
- **Spiegelen** van het klembord keert elk stuk om; een gevel schuift met zijn anker zo ver op dat het huis op dezelfde
  plek blijft (twee keer spiegelen geeft het origineel).
- **Lui laden**: `mkStadLaad` roept `stadLaad` alleen aan in de stand Stad of als het grid stadsstukken of stadcellen heeft
  (`mkOpen`, `mkThemaZet`, `mkStadTeken`, `mkVulStad`).
- Een stadsstuk telt voor `mkHeeftStad`, dus het uitzicht wordt vanzelf `stad_dag`. Muziek: zonder eigen keuze komt er
  geen `muziek` in het level en kiest het spel de stadmuziek (`MUZIEK_STAD`). Daardoor geeft Dark Africa in de balk in
  een stadlevel ook de stadmuziek: Dark Africa is de standaard van de keuzelijst, dus de Maker ziet het verschil niet.

**Uitzicht** in de balk (`#mkuitzicht`, `MK_UITZICHT`, `MK.uitzicht`, `mkUitzichtVan`): de achtergrond van het level,
naar `lvl.lagen`. Vanzelf (`''`) is de stad (`stad_dag`) als er een stadsstuk in het grid staat (`mkHeeftStad`: een cel
met `thema: 'stad'`), anders de gewone savanne in de avond. `basis` is die savanne-avond ook bij stadsstukken. Het gaat
mee in de JSON (`uitzicht`, alleen als het gekozen is).

### De gekoppelde stukken: galerij en trap

`MK_STAD_KOPPEL`, `mkGalerijMaat`, `mkTrapMaat`, `mkKoppelVakken`, `mkStadKoppel`, `mkKoppelKlik`, `mkGalSleep`,
`mkKoppelTeken`, `mkVulKoppel`, `mkGevelMuur`

Stap 4 van `notities/plan-stad-maker.md`. In de groep **Huizen** naast de gevel: **Galerij** en **Trap**. Ze hangen aan het id
van een gevel, niet aan een plek:

| stuk | voorwerp | neerzetten | paneel (kopje) | naar `stad` |
| --- | --- | --- | --- | --- |
| galerij | `{k: 'galerij', van, tot, niveau, meer}` | druk op een gevel, sleep naar een andere (of dezelfde) | Galerij g1 tot g2: Niveau 1 tot 4, Extra links, Extra rechts (0 tot 4 Amir) | `galerijen: {van, tot, h, meer}` |
| trap | `{k: 'trap', gevel, kant, niveau, balkon}` | klik op een gevel; de helft kiest de kant (tot 0,8 cel ernaast telt ook) | Trap bij g2: Niveau 0 tot 3, Kant, Balkon (0 tot 4 Amir) | `trappen: {gevel, kant, niveau, balkon}` |

- **Niveau**: bij een galerij de verdieping van het dek (`stadVerdieping`: 1 is 401, 2 is 730, 3 is 1059, 4 is 1388), in het
  level als `h`; bij het slepen de verdieping die het dichtst bij je eerste druk ligt, hoogstens de laagste van de twee huizen.
  Bij een trap de vloer waar hij begint (0 de straat), net als `niveau` in het spel; bij een klik de verdieping waar je klikte,
  zodat hij onder het dak blijft. `meer` gaat alleen mee als het niet `[0, 0]` is. Balkon standaard 1,6 (`MK_TRAP_BALKON`).
- **De plek komt uit de gevels**: `mkGalerijMaat` en `mkTrapMaat` rekenen precies als `stadGalerijMaat` en `stadTrapMaat`, op
  laptopmaat (`MK_STAD_SCHAAL`), dus wat in het grid staat staat ook zo in de Test. De hoogtes tellen vanaf de grondlijn
  (`MK.ground`), net als in het spel vanaf de straat. `c` en `r` zijn alleen de ankercel van de linkse gevel; `mkStadKoppel`
  zet ze bij elke wijziging (`mkBewaar`, `mkBewaarNu`, laden en plakken), zodat een gebied kopiëren, rijen invoegen en
  weghalen ze vanzelf meenemen. Verslepen gaat dus niet: versleep het huis.
- **Een gevel weg**: zijn galerijen en trappen gaan mee weg (`mkStadKoppel`, na Delete, de gum, knippen, plakken erover of
  laden met een id dat er niet is), en ongedaan maken brengt ze samen terug. `mkNaarLevel` slaat er een zonder gevel ook nog
  over. De gum op de ankercel pakt de gevel, niet de galerij of trap die op dezelfde cel staat; die haal je weg met Delete.
- **Kopiëren en plakken**: een galerij of trap gaat alleen mee als al zijn gevels in het gebied zitten. In het klembord wijst
  hij naar hun kopie (`_gevels`), want een geplakte gevel krijgt vaak een nieuw id (`mkStadHeel`); `mkPlakZet` zet daarna de
  nieuwe id's. **Spiegelen** wisselt `meer` van kant en zet een trap aan de andere kant van zijn (gespiegelde) huis.
- **Tekenen** (`mkKoppelTeken`, in `mkStadTeken`, in de volgorde van het spel: trap, gevel, galerij): de galerij in 9-slice uit
  `galerij.png`, de trap uit `trap.png` (afgesneden zoals in het spel), en het balkon als strook galerij. Na de huizen een goud
  streepje op de opening waar je boven uitkomt, en tijdens het slepen een stippellijn op de hoogte waar je drukte.
- **Aanklikken**: op het plaatje (`mkKoppelVakken`; een trap op zijn treden en zijn balkon, niet op het huis ertussen), voor de
  gevel; de exacte cel van een galerij of trap telt niet, daar staat de gevel.
- De meldingen voor galerij en trap en de vijanden op daken: zie hieronder.

### Vijanden op daken en de meldingen van de stad

`MK_DAK_SOORTEN`, `mkDakSoort`, `mkStadVloeren`, `mkStadVloerOp`, `voetX` in `mkTrapMaat`

Stap 5 van `notities/plan-stad-maker.md` (daarmee is het plan klaar).

- **De vloeren van de stad** (`mkStadVloeren`, zoals `stadVloeren` in het spel, in cellen op laptopmaat): het dak van elke
  gevel over zijn muur (`stadGevelH`: 487, 816, 1145 of 1474 voor 1 tot 4 hoog), het dek van elke galerij (zonder de
  uiterste 15 procent van zijn eindstukken, zoals het spel) en het balkon van een trap (`ht`, alleen met een balkon).
- **Een vijand erop** (`mkStadVloerOp`): het midden van zijn cel ligt boven de vloer en zijn voet (de onderrand van zijn
  cel) ligt hoogstens een halve cel (75) van die vloer. Met cellen van 150 valt elke vloer zo in precies een rij: een vijand
  op de galerij van de eerste verdieping (401) zet je in de cel waarvan de onderrand op 450 ligt.
- **In `mkSpawn`**: zo'n vijand krijgt `dak` met de hoogte van die vloer (`dak: 401`), en geen `boven` of `y`; `stadDakPlek`
  zet hem in het spel op die vloer, binnen de rand. Alleen de soorten die `dak` lezen (`MK_DAK_SOORTEN`: bandiet,
  schildbandiet en kruisboogbandiet; de Maker heeft nog geen kruisboogbandiet) krijgen het. Een andere soort krijgt het
  niet en staat in de Test op de straat; `mkControle` meldt dat.

Meldingen in `mkControle` (allemaal klikbaar, ze springen naar de cel):

| melding | ernst |
| --- | --- |
| twee gevels waarvan de muren elkaar op laptopmaat overlappen (meer dan 0,05 cel; raken mag, dat is een rij daken) | LET OP |
| een galerij met zijn dek boven het dak van een van zijn huizen | LET OP |
| een trap die hoger uitkomt dan het dak van zijn huis (niveau gelijk aan of hoger dan de hoogte van het huis) | LET OP |
| een trap op niveau 0 met zijn voet (`voetX`, waar je E drukt) boven een ravijn of leegte op de grondlijn | LET OP |
| een trap hoger dan niveau 0 zonder galerij of balkon op zijn hoogte aan zijn voet | LET OP |
| een trap met balkon 0 en geen galerij of balkon op zijn uitgang (`gatX`): na E val je meteen naar beneden | FOUT |
| een vijand op een dak, galerij of balkon waarvan de soort `dak` niet kent (hij staat in de Test op de straat) | LET OP |

Een bandiet of schildbandiet op een dak krijgt geen melding (ook niet dat hij zweeft). `tools/makertest.js` (controle
`stadsstukken`) zet elk van deze meldingen een keer neer en kijkt `dak` na, en het proefgrid heeft de stad achter de start
(kolom 24 tot 35) met een bandiet op de galerij (`dak: 401`) en een schildbandiet op een dak (`dak: 816`).

## Sneltoetsen

Escape (selecteren, deselecteren), spatie (schuiven), Delete (voorwerp of vorm weg), Ctrl+Z en
Ctrl+Y (ongedaan en opnieuw), Ctrl+S (exporteren), F (passend), T (testen), + en - (zoomen),
pijltjes (schuiven, met Shift sneller), M (de minimap), G (Savanne of Stad in de legenda), Shift+slepen (rechthoek; in Selecteren een gebied),
Alt+klik (een aaneengesloten vlak vullen), Ctrl+C,
Ctrl+X en Ctrl+V (kopiëren, knippen, plakken), H (het klembord spiegelen), Delete (het gebied
leegmaken). Op een keuzelijst, knop of tekstvak blijven de toetsen van dat veld.

## De makertest: `tools/makertest.js`

Laadt de Maker in Chromium met een proefgrid waar alles op staat (gat, gang met treden, mesa,
zwever, muur door de grond, sneeuw, alle voorwerpen, een tweede ravijn met een rijzer van 2 breed die het zegel
stuurt, een masker, een zwarte cel, een vorm, en achter de start een straat met twee huizen, een galerij, een trap, een
kraam, voetdecor, het paleis en een bandiet op de galerij en een schildbandiet op een dak) en
kijkt na: de round-trip van export en import, de vertaling naar een spel-level, rijen invoegen en
weer weghalen, verkleinen, snel schilderen, de rechthoek, het aanklikken van brede voorwerpen,
ongedaan maken, een gebied kopiëren, spiegelen, plakken en knippen, een rijzer van even breedte spiegelen met
zijn zegel eraan, een poort met hek, regie en rotswand (round-trip, vertaling, spiegelen, de knop Poort met hek, levelcheck), de minimap en Test vanaf hier, het palet (elke tool en vijand in de boom, de kolom en de flyouts, en de maat: geen lijst of paneel langer dan `MK_PALET_MAX`), de vijand-knoppen, de controle, de Test starten en teruggaan,
de autosave, de schakelaar Savanne | Stad met de leemmuur en het uitzicht (controle `stad`), de stadsstukken (controle
`stadsstukken`: ids, een paleis, de JSON, het veld `stad`, de stroken, de twee meldingen, spiegelen, plakken, het paneel en
neerzetten met de muis; en galerij en trap: slepen van gevel naar gevel, de zijkant van een gevel, het paneel, aanklikken op
het plaatje, `stad.galerijen` en `stad.trappen`, de JSON, een rij erboven, kopiëren met spiegelen en plakken op nieuwe id's,
een gebied met maar een van de twee gevels, een gevel weg met ongedaan maken, en laden met een gevel die er niet is; en de
meldingen van stap 5 met hun cel, `dak` op de spawn, en de stad in het proefgrid), en of
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
alleen met muis en toetsen), geen prop-keuze (een prop is een aantekening; echt decor is alleen het rotsdecor), en een zegel kent
alleen een masker, Te zien (Open, Verborgen, Onzichtbaar) en een rijzer, niet de andere zegel-velden (`speerval`, `plafond`). Een rijzer
staat alleen in een ravijn op de grondlijn: een rijzer in een put onder de grond of een lift die vanaf de
gangvloer door de ingang omhoog komt is in het spel niet beproefd, en de Maker meldt zo'n plek als FOUT.

Bekende randen, nog niet opgelost: alleen de tegel Zwevende laag (F) en Zwart plafond zweven, een blok rots
of savanne met lucht eronder wordt een pilaar tot de grond; de holte is aan de startkant een cel breder dan
getekend (`gangRx + MK_CEL_PX`); `boven` leest het spel niet voor hyena en panter, en `y` niet voor scorp, bandiet en schildman; de knop Zicht doet niets voor panter, kooiman (duel)
en `bandiet:hurk`; één rotscel op de grondlijn maakt de hele bodem kale rots.
