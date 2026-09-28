# Combinaties: wat werkt en wat niet

Een lijst van combinaties van dingen die al in het spel zitten (vijanden, decor, weer, terrein,
schakelaars). Hier houden we bij wat goed voelt en wat niet, zodat nieuwe levels op de goede
ideeën voortbouwen.

## Hoe het werkt

- **Jij** speelt een level (vooral de episode Testrun) en zet achter een combinatie wat je ervan vond:
  een oordeel en eventueel een regel waarom. Zet er gerust nieuwe regels bij.
- **Claude** leest dit bestand voor een nieuw level, bouwt vooral op wat hier als goed staat, en doet
  wat als slecht staat niet opnieuw. Ziet Claude in een testrun (of met de speelrobot) iets wat een
  goed idee lijkt, dan komt het onder **Voorstellen** en vraagt Claude eerst of het erin mag.

Oordelen:

| teken | betekent |
| --- | --- |
| `goed` | werkt, vaker gebruiken |
| `ok` | werkt, maar niets bijzonders |
| `slecht` | niet meer doen (zeg waarom) |
| `?` | nog niet gespeeld |

## Gespeeld in Testrun

| # | combinatie | waar | oordeel | waarom |
| --- | --- | --- | --- | --- |
| 1 | poel vlak voor een kei, slang erachter: je springt traag uit het water | Testrun 1, -1500 tot -2700 | ? | |
| 2 | regen die overgaat in onweer net voor een gevecht met twee zwaardvechters | Testrun 1, -4800 | ? | |
| 3 | zwarte slang boven op een terras van 150 | Testrun 1, -3900 | ? | |
| 4 | skelet met een speer vlak voor een doornbos aan het eind | Testrun 1, -6700 | ? | |
| 5 | kalebas aan een koordje in de regen (alleen met het mes los te snijden) | Testrun 1, -6300 | ? | |
| 6 | schilden in een zandstorm, het stof stuift ertegen op | Testrun 2, -1200 | ? | |
| 7 | zegel dat een ravijn openscheurt terwijl er hyena's aankomen | Testrun 2, -2600 | ? | |
| 8 | fosforslangen net achter een ravijn | Testrun 2, -5400 | ? | |
| 9 | rune als doel aan het eind, skelet erachter voor een nieuwe speer | Testrun 2, -8600 | ? | |
| 10 | val in een donkere gang met valschade, schorpioen en vechter beneden | Testrun 3, -1000 | ? | |
| 11 | sneeuw die begint net als je uit de gang komt, rode grond wordt wit | Testrun 3, -5200 | ? | |
| 12 | laag plafond (460) boven een kei met een zwarte slang erachter | Testrun 3, -6000 | ? | |
| 13 | nachtuitzicht met de donkere muziek in een kort level | Testrun 3 | ? | |

## Nog te proberen

Ideeën die er nog niet in zitten. Zet een oordeel of een sterretje bij wat je wilt zien.

- De baviaan in een level met een zegel: je sluit hem op door een ravijn open te laten scheuren.
- Een zandstorm in een gang: onder de grond is het stil, boven raast het (contrast).
- Twee zwaardvechters aan de overkant van een ravijn dat pas later openscheurt (valkuil zoals de oude Vorst).
- Een poel onder een laag plafond: trager én geen sprong.
- Fosforslangen in de sneeuw, 's nachts: groene gloed op wit.
- Een rij kalebassen aan koordjes als beloning voor wie het mes meeneemt.
- Een terras met een richel waar een schorpioen op wacht.
- Onweer 's nachts (`dark_hart`) met hyena's.

## Proeven: combinaties die mechanieken op elkaar laten inwerken

Losse levels in `notities/proeven/` (hetzelfde JSON-formaat als de bouwer, dus te openen onder
Level maken). Ze staan niet in de HTML: het zijn metingen, geen levels. `overzicht.jpg` laat van
elke proef de belangrijke momenten zien. Opnieuw draaien:

```
node tools/speelrobot.js notities/proeven/p1_dakluik.json --taai --wacht -600:6
node tools/speelrobot.js notities/proeven/p2_luik_dicht.json --taai --wacht -600:6,-2200:4
node tools/speelrobot.js notities/proeven/p3_rotstop.json --taai
node tools/speelrobot.js notities/proeven/p5_val_voor_kei.json --taai --vredig --wacht -1200:14
```

Proef 4 haalt de robot niet (hij springt te vroeg van het terras); die is met de hand gemeten, zie
de sprongtabel hieronder.

| # | proef | de maten | uitkomst | oordeel |
| --- | --- | --- | --- | --- |
| P1 | dakluik: zegel op de savanne opent een ravijn boven een gang | zegel -600, ravijn -1500 breed 450, gang -1000 tot -3400 diep 600 | werkt: het gat wordt een luik, licht valt op de vechter beneden | ? |
| P2 | het luik gaat dicht: sluitzegel in de gang | als P1, plus zegel `sluit: -1500` op -2200 (gangbodem) | werkt: dicht in 1,3 s, de gang wordt donker, terug kan niet meer | ? |
| P3 | zegel op de top van een rotsraster opent de rotswand | raster x -2400, rijen `....##....` / `..######..` / `##########`, zegel -1800 op 452, `muur: true`, muur -3000 | werkte niet (zie lessen), na de fix wel | ? |
| P4 | zegel op een terras opent een ravijn dat je alleen vanaf het terras haalt | terras -1000 tot -1800 op 150, zegel -1500, ravijn -2050 breed 500 | werkt: geland op -2381, overkant begint op -2300 | ? |
| P5 | val-zegel voor de kei waar Amir op staat | kei -1200, zegel `vijand` met ravijn op -1650 breed 300, vechter op -1800 | werkt: hij rent op Amir af, stapt erop, staat vast en valt erin | ? |
| P5b | hetzelfde met hyena's | hyenas n 2 op -2200 | half: de eerste valt erin, de tweede komt van achteren | ? |

### Hoe breed mag een ravijn aan de rand van een terras zijn

Gemeten met de echte spelfysica, op 1280 bij 720, volle sprint, afzet op de rand (coyote),
stappen van 25:

| hoogte van het terras | breedste ravijn dat je haalt |
| --- | --- |
| 0 (savanne) | 425 |
| 150 | 525 |
| 300 | 575 |
| 450 | 600 |

Een ravijn van 450 tot 525 aan een terras van 150 is dus alleen vanaf het terras te halen.

## Schijven in de wand: gooien op een doel

Een schijf (`schijven` in een level, zie `CLAUDE.md`) is de runeschijf rechtop op een wand die naar
Amir kijkt, en dezelfde schakelaar als een zegel: je raakt hem met een geworpen speer in plaats van
erop te stappen. De speer blijft erin zitten (regel 9). Proeven in `notities/proeven/s*.json`,
beelden in `schijven.jpg`.

### Van waar raak je een schijf

Gemeten met de worp uit het spel (`schijfStroken`, en elke strook nagegooid met de echte speer), op
1280 bij 720: je ziet 640 px voor je uit. De getallen zijn de afstand van Amir tot de wand, in px.
Vlak is de korte tik, boog de lang vastgehouden worp. Vetgedrukt: de schijf is dan niet in beeld.

| hoogte schijf | vanaf de vloer | vanaf een kei (114) | vanaf een terras 150 hoger | vanaf een terras 300 hoger |
| --- | --- | --- | --- | --- |
| 0,5 Amir | vlak **760-1130** | vlak **1210-1450** | vlak **1310-1530** | vlak **1660-1840** |
| 0,75 | vlak 160-890, boog 170-200 | vlak **1000-1290** | vlak **1130-1380** | vlak **1530-1720** |
| 1,0 | vlak 150-530, boog 140-280 | vlak **700-1090** | vlak **880-1210** | vlak **1380-1590** |
| 1,25 | boog 240-370 | vlak 150-850, boog 150-210 | vlak 500-1000 | vlak **1190-1440** |
| 1,5 | boog 320-460, **2160-2300** | vlak 160-410, boog 150-290 | vlak 140-710, boog 140-250 | vlak **980-1280** |
| 1,75 | boog 420-570, **2050-2210** | boog 250-380 | boog 210-330 | vlak 680-1090 |
| 2,0 | boog 520-700, **1920-2100** | boog 340-480 | boog 300-420 | vlak 150-840, boog 150-220 |
| 2,25 | boog **640-870**, **1760-1980** | boog 440-590 | boog 380-530 | vlak 160-380, boog 150-300 |
| 2,5 | boog **790-1160**, **1460-1830** | boog 540-730 | boog 480-650 | boog 260-390 |
| 3,0 | niet | boog **820-1800** | boog **730-1010** | boog 440-600 |

Wat eruit volgt:

- Vlak gooien vanaf de vloer raakt alleen tot 1 Amir. Daarboven is het de boog, of hoger gaan staan.
- Vanaf 2,25 Amir moet je vanaf de vloer blind gooien; vanaf een kei zie je hem wel. Zo'n schijf
  dwingt je eerst hoger te komen. Op 3 Amir raak je hem vanaf de vloer helemaal niet.
- Een lage schijf (0,5) is juist lastig: de vlakke worp zakt, dus je moet ver weg staan.
- Een schijf moet helemaal op zijn wand passen: `levelcheck.py` meldt een schijf die boven zijn
  terras uitsteekt of niet aan een wand hangt.

### De vijf proeven

| # | proef | de maten | uitkomst | oordeel |
| --- | --- | --- | --- | --- |
| S1 | terug over het ravijn: een schijf met `sluit` achter een ravijn dat een zegel opende | terras -2000 tot -2800 op 300, richel op 150, zegel -1150 met ravijn -1750 breed 500, schijf -2000 op 0,75 | werkt: vlak vanaf 600 px, het ravijn gaat dicht | ? |
| S2 | boven de doorgang: een hoge schijf op een rotstoren opent de rotswand | rotsraster x -2600, drie kolommen, vier rijen rots boven twee rijen doorgang; kei -1740; schijf -2240 op 2,25 met `muur` | werkt vanaf de kei; vanaf de vloer op 600 px mis | ? |
| S3 | licht in de gang: een schijf op de eindwand opent het dak | gang -800 tot -3600 diep 600, schijf -3600 op 1,0 met ravijn -3050 breed 400 | werkt (na de twee reparaties hieronder) | ? |
| S4 | achter de vechter: een vijand tussen jou en de schijf | terras op 300, schijf -2000 op 1,0, vechter op -1850 | de speer raakt de vechter; de schijf is zo niet te raken | ? |
| S5 | van verre: de verre boog opent een ravijn onder een nietsvermoedende vechter | rotstoren als S2, schijf op 2,0 met ravijn -1940 breed 300, vechter op -1940, gooien vanaf 1940 px | werkt: hij valt erin zonder je te zien, maar je gooit blind | ? |

Opnieuw bekijken: zet een proef open in de bouwer, of gebruik de knoppen onder **Schijf in de wand**
in de sandbox (Speer en spullen): die zeggen na elke klik vanaf hoe ver je raakt.

## Voorstellen van Claude

Wat Claude uit een testrun haalt en voorstelt. Pas na een ja gaat het een level in.

- (nog leeg)

## Lessen

Wat we geleerd hebben en wat dus vast staat.

- Een vijand boven een gang zetten kan niet: `terrainH` zet hem op de bodem van de gang. Een vijand
  die door een dakluik naar beneden valt zit er dus niet in.
- Een zwaardvechter komt pas als hij Amir ziet, ongeveer een halve schermbreedte (640 op 1280).
  Staat hij verder van de val, dan blijft hij staan en gaat de val nooit af.
- Hyena's komen van beide kanten van het beeld. Een val aan een kant van de kei vangt er een; voor
  een roedel moet er aan elke kant een liggen.
- Een zegel op de hoogste kolom van een rotsraster lag eerst onder de rots op de savanne en ging
  nooit aan: `grotTerrein` gaf voor een kolom die tot bovenaan vol is geen vloer. Nu is de
  bovenkant van het raster daar de vloer (proef P3).
- Onder de treden van een rotsraster schemert op een paar plekken de lucht door (smalle kieren,
  zie P3 in `overzicht.jpg`). Tekenfout, nog niet opgelost.
- Het rode doorzichtige vlak (P1 en S3) was de rode flits als Amir geraakt wordt: die kleurde de
  hele rechthoek van zijn plaatje, ook bovengronds. Opgelost (`amirRood`).
- Een speer in een gang vloog met een boog dwars door het dak, en een speer die bovengronds boven
  een gang neerkwam zakte door de grond de gang in. Opgelost (`javTegenDak`, `javFloor` met de
  hoogte van de speer).
- Vijanden verschijnen pas als Amir op zo'n 1,1 schermbreedte van hun plek komt, en een vijand
  wiens plek dan al in een open ravijn ligt komt niet. Een val van verre werkt dus alleen op een
  vijand die al verschenen is (S5: eerst dichterbij komen, dan terug en gooien).
- Een schorpioen komt van de rand van het beeld, niet van zijn plek: hem voor een schijf zetten kan
  niet.
- Een doorgang onder een rotsraster maakt van de toren een zwevend blok zonder pijlers (S2). Werkt,
  maar ziet er niet uit als rots.
