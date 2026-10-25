# Laadpoort

## laadpoort: een level loopt pas als alles binnen is

`LAAD`, `laadOpen`, `laadPoort`, `laadStap`, `#laad`: het zetten van `src` op elk plaatje zet het vanzelf in `laadOpen` tot het binnen is of ontbreekt (een haakje op `HTMLImageElement.prototype`), dus een nieuwe lader hoeft niets aan te melden. `restart` zet de poort dicht; de lus staat stil (`dt` 0, geen toetsen) tot `laadOpen` twee beelden achter elkaar leeg is, met na `LAAD.toon` het scherm Laden en na `LAAD.max` gaat hij toch door. Bij een nieuw level (een andere naam dan `laadVorig`, `laadMin`) staat het scherm er meteen en minstens `LAAD.min` (5) seconden, met de naam van het level (`#laadnaam`); de balk (`laadToon`) loopt dan nooit sneller dan de tijd, dus kunstmatig door als alles al binnen is. Opnieuw in hetzelfde level wacht niet. In het menu wacht hij niet. Geluid telt niet mee. Daarna bakt `warmBouw` in stukjes van `WARM_BUDGET` ms per beeld vooraf wat anders een schok geeft; een taak die `false` teruggeeft is nog niet klaar, gaat achteraan en houdt het laadscherm dicht. Voorbij `LAAD.max` (40 s) geeft de poort het wachten op plaatjes op, maar zo'n taak blijft wachten zolang er nog plaatjes binnenkomen (`laadOpen` niet leeg), tot `LAAD.bak` (80 s); daarna valt hij af. Eerst viel hij meteen op `LAAD.max` (toen 25 s) af, en dan werd alles wat net te laat binnenkwam pas midden in het spel gebakken. Zo meet de baviaan zijn kaders per frame (`bavKaderVooraf`: uitpakken buiten de hoofddraad via `fetch` en `createImageBitmap`) in plaats van alle 200 in een ronde. Ook wat anders pas gemaakt werd als het in beeld kwam, zit erin: de lichtkaart onder de grond (`lkKaart`, dan de kolommen in stukjes van zes vanaf de startplek, `lkKolom`), het licht op elke runerots (`runeLichtMaak`), het effect van elk ravijn (`ravijnVastVoor`, met een keer `drawGap` zodat de wand naar de kaart gaat) en de canvassen van de rotswand (`muurSet`)

## de oude poort is weg

Naast `laadPoort` stond lang de poort uit het begin van het spel: een teller `loaded` in `load` en `loadAny`, een
handmatige som `total` van het aantal bestanden (`+ 48 + 36 + 12 + 88`) en in de tekenlus `if (loaded >= total)`,
met alleen de lichtlaag zolang hij niet vol was. Die som dwong de schorpioen en de dorpelingen af om altijd mee te
laden, want zonder hun telling kwam `total` nooit vol. Hij is eruit: `laadPoort` is het enige dat bepaalt of een
level mag beginnen, en `load`, `loadAny` en `loadQuiet` doen alleen nog de terugvalpaden en de melding `ontbreekt:`.
De drie verschillen nu nauwelijks: `load(x)` is `loadAny([x])` met de melding op `src` in plaats van op het eerste
pad, en `loadQuiet` is hetzelfde zonder de oude teller (die het nooit had). Ze zijn bewust nog niet samengevoegd.

## lui laden per level

Wat niet elk level gebruikt, komt pas binnen als een level het gebruikt: `laadLevel(lv)` loopt alle
`xxxLaadLevel`-functies langs, vanuit `setLevel` (het menu: al terwijl de speler het kaartje bekijkt) en vanuit
`mkTest` (de Test van de Maker nieuwstijl), zodat een getest level dezelfde weg volgt als een gewoon level.

| soort | kijkt naar | lader | lui sinds |
| --- | --- | --- | --- |
| winterplaatjes | `winter` | `loadWinter` | eerder |
| slangen, per kleur (`snk[k]`) | spawns `groen`/`zwart`/`knock`, `fosfor` (de groene); zonder spawns-lijst en zonder `bandietGolf` groen en zwart voor de vrije spawner (`nextKind`) | `slangLaad(k)`, `slangLaadLevel` | nu |
| schorpioen (`scp`) | spawns `scorp` | `scpLaad`, `scpLaadLevel` | nu |
| hyena (`hyImg`, in de winter ook `hySkins.wit`) | spawns `hyenas`, plus `winter` | `hyLoad`, `hyLoadSkin('wit')`, `hyLaadLevel` | nu |
| panter (`panImg`, in de winter ook `panSkins.wit`) | spawns `panter`, plus `winter` | `panLoad`, `panLoadSkin('wit')`, `panLaadLevel` | nu |
| dorpelingen (`NPCS[k].frames`, de cycli van de dorpelinge) | `npcs` | `npcLaad(kind)`, `npcLaadLevel` | nu |
| dorp (`villageImg[id]`) | `village`, per id (de winterplaten hebben hun eigen id) | `loadVillage(id)`, `dorpLaadLevel`; `villageList` laadt een id dat pas in het spel opduikt alsnog | nu |
| bandiet, kooiman, meelman, schildbandiet, vogel | spawns en vlaggen | `banLaadLevel`, `kooiLaadLevel`, `meelLaadLevel`, `schbLaadLevel`, `vogelLaadLevel` | eerder |
| baviaan, goudaap, skelet, speerteken, fakkel, deur, takel, grot, mes, bloed | wat het level heeft | eigen `xxxLaad`, vanuit `warmBouw` of bij het eerste gebruik | eerder |

De sandbox kan elke soort spawnen en roept daarom bij het openen (`startSandbox`) alle laders aan die lui zijn
geworden: de drie slangen, de schorpioen, de hyena en de panter. Het opstarten kiest de nieuwste test
(`setLevel(TEST_LEVELS.length - 1)`), niet meer de eerste van het blad (dat was Test 42, met de meelman), zodat het
menu geen vijand laadt die de speler misschien nooit ziet; de nieuwste test hoort licht te zijn.

Elke lader onthoudt of hij al gelopen heeft (`scpGeladen`, `hyGeladen`, `panGeladen`, `snk[k]`, `d.geladen`,
`villageImg[id]`), dus vaker aanroepen laadt niets dubbel. De laadpoort wacht vanzelf op wat de lader zet (het
haakje op `src`), en `warmBouw` bakt alleen de banken die er zijn. Een vijand die ontbreekt geeft nog steeds
`ontbreekt:` in de console (dat zit in `load`, `loadAny` en `loadQuiet`), en zonder frames tekent de lus niets:
`snakeImg`, `scpImg`, `hyFrameImg` en de dorpelingen geven dan `undefined` terug en de tekenlus slaat ze over.

Nameten (Chromium op 1280x720, een Playwright-script dat de verzoeken en bytes telt tot het menu staat en daarna tot een level loopt): het menu zakte van 996 verzoeken
en 153 MB naar 475 verzoeken en 90 MB; een level haalt zijn eigen soorten alsnog (Valse Koning 2 met hyena's,
slangen en schorpioenen: 70 MB erbij, Valse Koning 4 in de winter: 97 MB erbij).

**Een nieuwe soort lui laden:** een lader met een vlag (`xxxLaad`, idempotent, de frames met `loadQuiet` of
`loadAny` zodat `ontbreekt:` blijft werken), een `xxxLaadLevel(lv)` die in `spawns`, `npcs`, `village` of een
eigen veld kijkt (let op `s.kind || s.k`: na `readLevel` heet het veld `kind`), een regel in `laadLevel`, een
aanroep in `startSandbox` als de soort daar een knop krijgt, en in `warmBouw` de bank warmen als het level de
soort heeft. Zet de lader nergens anders neer: `laadLevel` is de ene plek. Laat hem zich ook melden met `laadNodig(soort)` (bovenaan, voor de vlag) en zet hem terug in `laadVrij`, anders
blijft hij na zijn level in het geheugen staan.

## geheugen vrijgeven bij een levelwissel

`laadNodig`, `laadNieuw`, `laadVrij`, `laadGebruik`. Lui laden haalde alleen binnen; wat een level eenmaal geladen
had bleef staan tot de pagina dicht ging, dus na de baviaan, een bandiet en de goudaap-arena zaten al die reeksen
tegelijk in het geheugen. Nu meldt elke grote vijandlader zich met `laadNodig(soort)`, ook als hij al geladen was
(de slangen per kleur, de schorpioen, de hyena en de panter met hun witte vacht, de bandiet per set en per variant,
de kooiman, de vogel, de meelman, de schildbandiet en zijn executie, de baviaan en het goudaapje). `setLevel` en
`mkTest` beginnen een nieuwe lijst (`laadNieuw`); daarna vragen `laadLevel`, `restart` (de baviaan, de arena, het
takelwiel, de bandiet-arena) en de spawns aan wat het level gebruikt. Aan het eind van `restart` is de wereld leeg,
en dan laat `laadVrij` los wat niet op de lijst staat: de Image-objecten gaan uit de banken (`delete`, of de `let`
op `null`) en de vlag van de lader gaat terug. Komt de soort in een later level terug, dan laadt de lader hem
gewoon opnieuw, achter de laadpoort zoals de eerste keer. De vooraf gemeten kaders van de baviaan komen dan ook
terug: `bavKaders` is een WeakMap op het plaatje en `warmBouw` meet de nieuwe plaatjes opnieuw (nagemeten: 160
kaders voor en na een omweg via Valse Koning 1).

Wat blijft: Amir, het decor, de dorpelingen, het dorp en wat elk level gebruikt. De sandbox laat niets los
(`laadVrij` kijkt naar `sandbox`), hij laadt zijn eigen soorten in `startSandbox` en met de knoppen; pas het
volgende level ruimt ze op. Hetzelfde level opnieuw (R) laat ook niets los, want de lijst loopt door tot het
volgende `setLevel`. De baviaan en het goudaapje gaan altijd allemaal tegelijk weg, want de tekencode gaat ervan
uit dat al hun reeksen er samen zijn; een level met `baviaan` of `apenArena` houdt ze. De schildbandiet alleen als
zijn JSON binnen is (een lopende fetch maakt zijn werk af), en dan gaan ook `schbLagen`, `exeData` en hun
`Bezig`-vlaggen terug, anders laadt hij niet opnieuw.

Nameten: Chromium op 1440x900, Baboon 1, Valse Koning 1, Baboon 4 en weer Baboon 1, na elke wissel een
GC en een gesimuleerde geheugendruk (`Memory.simulatePressureNotification`). De cijfers staan in de pull request
(geheugen vrijgeven bij een levelwissel). Let op bij zelf meten: `Runtime.queryObjects` houdt zijn lijst vast tot
je `Runtime.releaseObjectGroup` doet, en dan lijkt het alsof niets vrijkomt.


