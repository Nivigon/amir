# Combinaties: wat werkt en wat niet

Een lijst van combinaties van dingen die al in het spel zitten (vijanden, decor, weer, terrein,
schakelaars). Hier houden we bij wat goed voelt en wat niet, zodat nieuwe levels op de goede
ideeën voortbouwen.

## Hoe het werkt

- **Jij** speelt een level (vooral de episode De Poorten) en zet achter een combinatie wat je ervan vond:
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

## Gespeeld in De Poorten

De episode Testrun is eruit; de combinaties die daar goed genoeg voor waren staan nu in De Poorten,
en de rest van de tabel is meegegaan zodat het oordeel niet verdwijnt.

| # | combinatie | waar | oordeel | waarom |
| --- | --- | --- | --- | --- |
| 1 | poel vlak voor een kei, slang erachter: je springt traag uit het water | Poort 2, -1300 tot -2500 | ? | |
| 2 | regen die overgaat in onweer halverwege het level | Poort 2, -9000 | ? | |
| 3 | zwarte slang boven op een terras van 150 | Poort 2, -3500 | ? | |
| 4 | skelet met een speer vlak na een rune (regel 9) | Poort 1, -6650 | ? | |
| 5 | kalebas aan een koordje in de regen (alleen met het mes los te snijden) | Poort 2, -8600 | ? | |
| 7 | zegel als val: de vijand stapt er zelf op en scheurt de grond onder zichzelf open | Poort 1, -3600 en Poort 5, -3400 | ? | |
| 8 | fosforslangen naast een schorpioen aan het eind van een level | Poort 2, -10800 | ? | |
| 9 | runeschijf op een rots die rijzende grond omhoog stuurt, met een skelet erachter | Poort 1, -5550 | ? | |
| 10 | val in een gang met valschade, via een richel, met een schorpioen en een vechter beneden | Poort 3, -2600 | ? | |
| 12 | drie zuilen in een ravijn, steeds hoger, en dan naar beneden de overkant op | Poort 2, -4700 | ? | |
| 13 | nachtuitzicht met de donkere muziek en onweer erbij | Poort 5 | ? | |
| 14 | zandstorm boven de grond, stilte in de gang eronder (contrast) | Poort 3 | ? | |
| 15 | zakkend plafond met een uitgang die dichtzakt: rennen, met twee vijanden in de kamer | Poort 3, -4050 tot -6950 | ? | |
| 16 | rijzende grond als lift naar een terras met een roedel erop | Poort 4, -6500 | ? | |
| 17 | dal van zuilen in de sneeuwstorm (omlaag en weer omhoog) | Poort 4, -4300 | ? | |
| 18 | brug van twee blokken steen die na zes seconden weer zakt | Poort 2, -9400 | ? | |
| 19 | de baviaan die je het hele level achtervolgt, met de speerval als enige uitweg | Poort 6 | ? | |
| 20 | de kooi (twee ravijnen) midden in een achtervolging, met een kei ervoor waar hij overheen springt | Poort 6, -1600 tot -3600 | ? | |

Uit Testrun, nog niet in een level terug:

| # | combinatie | waar stond het | oordeel | waarom |
| --- | --- | --- | --- | --- |
| 6 | schilden in een zandstorm, het stof stuift ertegen op | Testrun 2 | ? | |
| 11 | sneeuw die begint net als je uit de gang komt, rode grond wordt wit | Testrun 3 | ? | |

## Nog te proberen

Ideeën die er nog niet in zitten. Zet een oordeel of een sterretje bij wat je wilt zien.

- De baviaan in een level met een zegel: je sluit hem op door een ravijn open te laten scheuren.
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

## Runes op een rots: gooien op een doel

Een rune op een rots als doel (`runes` met `doel: true`) kan nu ook iets doen als je hem raakt, net als
een zegel: een ravijn openen op een andere plek (`ravijn`, `breed`), een open ravijn sluiten (`sluit`),
de rotswand openen (`muur`) of de speerval losschieten (`speerval`). De rots staat op de vloer onder
zijn midden: de savanne, een terras, of in een gang de bodem. Proeven in `notities/proeven/r*.json`,
beelden in `runes.jpg`.

### Van waar raak je de rune

Gemeten met de worp uit het spel (`runeStroken`, de stroken nagegooid met de echte speer), rotsen van
3,5 Amir, op 1280 bij 720: je ziet 640 px voor je uit. De getallen zijn de afstand van Amir tot de
schijf in px, vanaf de vloer en vanaf een kei (114 hoog) die op die afstand ligt. Vetgedrukt: de
schijf is dan niet in beeld.

| hoogte rune | spits | pieken | zuilen | scheve boog |
| --- | --- | --- | --- | --- |
| 0,75 Amir, vloer | 180-760 | 180-820 | 510-780 | 180-780 |
| 0,75, kei | **1040-1200** | **1020-1240** | **1060-1200** | **1000-1240** |
| 1,0, vloer | 170-360 | 170-280 | 170-410 | 170-290 |
| 1,0, kei | **740-1040** | **720-1040** | **740-1040** | **740-980** |
| 1,5, vloer | 390-460 | 410-460 | 390-460 | 390-460 |
| 1,5, kei | 180-280 | 180-280 | 180-280 | 180-280 |
| 2,0, vloer | 580-700 | 590-700 | 580-690 | 610-700 |
| 2,0, kei | 380-480 | 420-480 | 380-480 | 440-480 |
| 2,25, vloer | **720-820** | **720-870** | **690-870** | **770-870** |
| 2,25, kei | 520-560 | 500-600 | 480-600 | 560-600 |
| 2,5, vloer | **800-1040** | **970-1140** | **890-1080** | **890-1160** |
| 2,5, kei | 580-700 | **700-720** | 640-700 | 640-720 |

Daarnaast is er bij 1,5 tot 2,5 Amir een verre boog vanaf de vloer, rond 1500 tot 2300 px, ver buiten beeld.

Wat eruit volgt:

- Anders dan bij een rechte wand vangt de brede voet van de rots een verre vlakke worp op: een rune op
  1 Amir raak je vanaf de vloer alleen van dichtbij.
- Een rune op 2,25 Amir is de "eerst hoger"-hoogte: vanaf de vloer gooi je blind, vanaf een kei zie je
  hem. Op 2,5 is ook de kei krap.
- Een kei te dichtbij is net zo slecht als geen kei: dan kom je te hoog uit en gaat de boog erover.
- De maten van een rots hangen aan het scherm (zie `CLAUDE.md`), de afstanden hierboven dus ook.
  Ontwerp met ruimte, en kijk op een ander scherm na met de knoppen in de sandbox.

### De vijf proeven

| # | proef | de maten | uitkomst | oordeel |
| --- | --- | --- | --- | --- |
| R1 | de zuilen sluiten het ravijn dat een zegel opende | zegel -1150 met ravijn -1700 breed 450, zuilen met voet op -2848, rune op 0,75 met `sluit: -1700` | werkt: vlak vanaf 584 px, het ravijn gaat dicht | ? |
| R2 | pieken, alleen vanaf de kei | pieken met voet op -3000, rune op 2,25 met `muur`, kei op -1844 (550 px ervoor) | werkt vanaf de kei; vanaf de vloer op 640 px onder de schijf tegen de rots | ? |
| R3 | een kleine spits in een donkere gang opent het dak | gang -800 tot -3800 diep 700, spits van 1,5 met voet op -3700, rune op 1,0 met ravijn -3000 breed 400 | werkt: raak vanaf 225 px, licht in de gang | ? |
| R4 | de scheve boog op een terras, en een val daarachter | terras -1800 tot -3400 op 300, boog van 2,5 met voet op -2900, rune op 1,0 met ravijn -3675 breed 550, vechter op -3450 | werkt: raak vanaf het terras (220 px), de vechter valt, en vanaf het terras spring je over de 550 | ? |
| R5 | de spits van verre, een val onder een nietsvermoedende vechter | spits van 3,5 met voet op -3000, rune op 2,0 met ravijn -1750 breed 300, vechter op -1750, gooien vanaf 2000 px | werkt, maar blind, en alleen als de vechter al verschenen is | ? |

Test 28 (Hoog mikken) zet vier hoge runes achter elkaar in een level: de pieken op 2,25 met een kei ervoor
(`kei: 3.05`, ligt op 1280 bij 720 op 549 px, op 1920 bij 1080 op 824, op een telefoon op 300: telkens in de
strook en met de schijf in beeld), de zuilen op 2,0 vanaf de grond, de spits op 2,0 op een terras van 300, en
de scheve boog op 2,0 in een gang van 800. Alle vier geraakt op de drie schermen.

Opnieuw bekijken: zet een proef open in de bouwer, of gebruik de knoppen onder **Rune op een rots** in de
sandbox: de knop **Doet** kiest wat de rune doet, en na het neerzetten zegt de hint vanaf hoe ver je raakt.

## Voorstellen van Claude

Wat Claude uit een testrun haalt en voorstelt. Pas na een ja gaat het een level in.

- **Opgeslagen als bouwsteen (gebouwd):** de opstellingen die werken staan in `RUNE_OPSTELLINGEN`:
  `vlak`, `zuilen`, `boog`, `kei`, `terras`, `gang` en `ver`, met de rots, `groot`, `hoog`, de kei en de strook.
  Een level zet `opstelling: 'kei'` bij een rune, de bouwer kiest hem in het venster van een rune.
- **Hoger of lager komen (schets, nog niets gebouwd):** zes opties in `proeven/opties_hoger_lager.jpg`,
  alle zes goedgekeurd. Een opstap is nooit een rots met een rune en geen vergrote kei, maar iets wat er al
  is. Op main bestaan al: de rijzende grond (`rijzers`, ook te starten met een rune als doel) voor optie 1,
  en de zuilen met een hoogte uit Test 20 (Hoog en laag) voor optie 2: hop naar de zuil van waar je de rune
  raakt. Kan op deze branch al: eerst op een kei (Test 28), een rots in een kuil of gang, en een rots
  met een hoge en een lage rune. Optie 6 (een platform dat zakt) is nu een rijzer met `zak: true`: hij zakt als je erop staat.
- **Voor de PR, let op:** main is sinds deze branch ver doorgegroeid (tot Test 27, met rijzers, zuilen,
  savannelagen en liften). Bij het samenvoegen: mijn Test 28 (Hoog mikken) krijgt een nieuw nummer, want
  main heeft al een Test 17 (De rijzende grond); en mijn `runeDoet` (een rune als schakelaar) moet samen
  met wat main al met een rune doet (`rijs`), zodat er geen twee manieren naast elkaar komen.

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
- Het rode doorzichtige vlak (P1 en een eerdere proef in de gang) was de rode flits als Amir geraakt wordt: die kleurde de
  hele rechthoek van zijn plaatje, ook bovengronds. Opgelost (`amirRood`).
- Een speer in een gang vloog met een boog dwars door het dak, en een speer die bovengronds boven
  een gang neerkwam zakte door de grond de gang in. Opgelost (`javTegenDak`, `javFloor` met de
  hoogte van de speer).
- Vijanden verschijnen pas als Amir op zo'n 1,1 schermbreedte van hun plek komt, en een vijand
  wiens plek dan al in een open ravijn ligt komt niet. Een val van verre werkt dus alleen op een
  vijand die al verschenen is (R5: eerst dichterbij komen, dan terug en gooien). Die grens is scherp:
  in R4 stond de vechter eerst op 1427 px van Amir, net buiten de 1408, en verscheen hij pas later.
- Een schorpioen komt van de rand van het beeld, niet van zijn plek: hem voor een schijf zetten kan
  niet.
- Een rune op een terras is van de grond soms toch te raken, blind met de verre boog (R4: 770 tot 820 px).
- Afstanden in dit spel lopen in twee soorten: wat aan Amir hangt (rotsen, de worp, de sprong in hoogte)
  schaalt mee met het scherm, wat in het level staat (keien, ravijnen, vijanden) niet. Een kei die bij een
  rune hoort, moet daarom aan de rune hangen (`kei`), anders ligt hij op een groot scherm in de rots en op
  een telefoon te ver. Het zegel dat op 1280 vrij lag, lag op 1920 onder die kei.
