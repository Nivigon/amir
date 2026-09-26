# Amir: King of Africa

Een browserspel in een enkel bestand: open `amir-king-of-africa.html` in de browser (via een lokale webserver, bijvoorbeeld `python3 -m http.server`, zodat de sprites geladen mogen worden).

Alle sprites, achtergronden en geluiden staan los op schijf. Het spel verwacht de mappenindeling hieronder; de paden staan letterlijk in de HTML.

## Episodes

In het menu onder **Levels** staan vier reeksen: Episode Renew, Episode Winter World, Episode De Diepte (vijf zware levels die telkens onder de grond door gaan, met een verhaal en een slot als je bij level 1 begint), en Test levels.

Episode Renew is tien levels lang en loopt op van rustig naar zwaar: van het dorp bij de start en het eerste doornbos, via de poelen, het doornenpad, de heuvelrug, de hyenavlakte, het verdronken dorp en de bergpas, naar de nacht waarin alles tegelijk komt, en tot slot twee keer de zwarte panter als eindbaas. Elk level heeft zijn eigen uitzicht en gebruikt alles wat het spel heeft: drinkkalebassen, doornbossen, water, ravijnen, terrassen en richels, dorpen, botten, hyena's, slangen en schorpioenen. De leveldefinities staan in de HTML als `RENEW_1` tot en met `RENEW_10`.

Episode Winter World speelt hoog in de bergen. Een level met `winter: true` krijgt sneeuw op alles wat je beklimt (de `_sneeuw`-versies van de rotsen en klimstukken), een besneeuwde grond met grijze rots eronder, bevroren gras, sneeuwval, een besneeuwd uitzicht (de `_sneeuw`-versies van de bergpanelen en de heuvelrij in `design/bg/`, uit `tools/sneeuw_bg.py`: witte toppen, sneeuw op de ruggen en de vlakte) en witte dieren: de witte hyena's uit `enemies/hyena_wit` en de witte panter uit `enemies/panter_wit`. Die winterplaatjes worden pas geladen als je zo'n level kiest. Van het dorp bestaat ook een winterversie: de zeven dorpsplaten hebben elk een `_sneeuw`-tegenhanger (`hut_round_arch_sneeuw`, `well_sneeuw`, enzovoort) die je in een leveldefinitie onder `village` neerzet, en in de bouwer staan een besneeuwde hut, boom en struik. Het winterlevel begint bij een ingesneeuwd berggehucht. De witte panter jaagt anders dan de zwarte: hij vervaagt in de sneeuw zolang hij sluipt (let op zijn schaduw), en zijn sprong is een hoge sneeuwduik die neerkomt op de plek waar je stond toen hij afzette. Bukken helpt niet, opzij stappen wel, en daarna zit hij even tot zijn buik in de sneeuw: dan steek je. Vanaf zijn tweede fase wisselt hij de duik af met de lage tackle. De leveldefinities staan in de HTML als `WINTER_1` en `WINTER_2`.

Winter 2 (De ijskloof) is de zwaardere tocht: steeds bredere ravijnen (tot 300), een trap van drie terrassen, een steile wand met twee richels waar je aan de andere kant 600 diep vanaf springt, twee ingesneeuwde gehuchten, roedels witte hyena's van twee kanten, en aan het eind opnieuw de witte panter. Het level heeft zijn eigen uitzicht (`winter_kloof`): later op de dag, donkerder blauw en dikkere nevel.

Sneeuw hoeft niet de hele winteruitrusting te zijn. Naast `winter: true` kan een level het veld `sneeuw` zetten, en dat is een andere vraag: niet "speelt dit hoog in de bergen", maar "ligt hier sneeuw op de grond, en op wat voor grond". Daar staan twee dingen los van elkaar. De bodem is `savanne` (de gewone rode grond) of `rots` (dezelfde grond als grijze steen, `design/grondrand_rots.png`). Het dek is de sneeuw die daar bovenop ligt, als losse laag in vier standen (`design/sneeuwlaag_25` tot `100`, uit `tools/sneeuwdek.py`). Rode grond blijft dus rood onder de sneeuw, want een ondergesneeuwde zandvlakte is nog altijd zand, en grijs is een keuze voor een rotsbodem in plaats van iets wat er vanzelf bij komt zodra het sneeuwt. Met `van` en `tot` loopt het dek onderweg op: `sneeuw: { soort: 'savanne', van: -1200, tot: -7000 }` begint kaal en eindigt dicht, met de eerste plekken in de kuiltjes en de sneeuwrand die over de breukrand gaat hangen. Zonder `van` en `tot` ligt overal evenveel (`dek`, standaard 1). In de sandbox staat het onder **Sneeuwdek**: geen, savanne of rotsbodem, minder of meer, en een overgang die vanaf waar je staat naar links oploopt. `winter: true` verandert er niet door en houdt zijn eigen ingebakken sneeuwgrond.

Een voorgrond geeft het beeld diepte: droog gras dat dichter bij de camera staat dan het pad. Het schuift sneller dan de wereld, is onscherp en donkerder, en staat met zijn voet onder de rand van het scherm. Zakt de camera een gang in, dan glijdt het gras omhoog het beeld uit en valt het weg; onder de grond staat er tussen jou en Amir aarde, geen gras. Voor Amir langs wordt het even doorzichtig. In de sandbox staat hij onder **Voorgrond** bij Beeld en geluid: uit, gras, dicht gras of gemengd, en scherp of onscherp om te vergelijken. Een level zet hem met het veld `voorgrond`: stroken waar het groeit (hoe dicht, en welk deel struik of kei is), met open plekken en dichte pollen die elkaar afwisselen, en losse stukken op een vaste plek, zoals een kei of een buffelschedel. **Test 11: Voorgrond** is Test 10 met zo'n voorgrond: vol aan het begin, ijler naar het ravijn toe, weg onder de grond, en weer dicht als je boven komt, met een open plek rond de fakkels.

Of het sneeuwt, verschilt per potje. Bij de start wordt een weerplan geloot: de hele tijd sneeuw, helemaal geen, sneeuw die onderweg begint, sneeuw die onderweg ophoudt, of een bui midden in het level. Het plan hangt aan de afstand door het level, en begin en einde gaan langzaam: over ongeveer een tiende van het level dikt de sneeuw aan of dunt hij uit, en vlokken die weg moeten vallen gewoon uit beeld. Ook de dikte van de bui verschilt per potje (`planSnow` in de HTML).

In de winter is al het stof sneeuwstof (de stofplaatjes worden bij het laden wit gemaakt), en bij een landing of een lage zwaai stuift de sneeuw echt op: een brede lage wolk die blijft hangen, een waaier glinsterende kristallen en klonten die in een boog wegvliegen en bij het neerkomen een wolkje geven. Hoe harder je neerkomt, hoe groter de plof.

Episode De Diepte is vijf levels lang en is met opzet zwaar. Na een aardbeving loopt er een scheur door de savanne, de put van het dorp staat droog, en Amir gaat de diepte in. Elk level gaat onder de grond door: een ravijn dat te breed is om over te springen is de ingang, beneden loopt een gang in het donker, en een tweede gat in het dak met treden erin brengt je weer naar boven, waar het level eindigt. In alle vijf staat de valschade aan, dus de val door de ingang kost een leven. Onder de rand van elke ingang zit een richel die je opvangt, anders kostte de val er twee. Begin je bij level 1, dan lees je voor elk level een stukje van het verhaal, en na het laatste het slot.

De vijf: **Diepte 1: De scheur** begint in het dorp, met een zwaardvechter achter een kei, en gaat dan de scheur in: een gang met een groep fosforslangen, een schorpioen en een vechter, en boven wachten nog twee hyena's. **Diepte 2: Het zwarte water** heeft poelen met zwarte slangen, doornbossen en twee vechters achter een ravijn, en een gang van 900 diep met zelf hoogteverschil: een bult met een vechter erop, en hyena's die uit het donker komen. **Diepte 3: De rune in de diepte** loopt eerst onder een rotsdak waar je niet meer kunt springen, dan de gang door, en eindigt bij de rotswand met de rune, met twee vechters en een roedel hyena's ervoor. **Diepte 4: De lange nacht** speelt in het donker, op het nachtdeuntje (`music/darkafrica.mp3`): de langste gang, in drie stukken, en boven nog een wand die je alleen via een richel haalt. **Diepte 5: De koning onder de grond** is alles nog een keer, en als je weer boven komt wacht de zwarte panter in het hoge gras. De definities staan in de HTML als `DIEP_1` tot en met `DIEP_5`.

Een level kiest zelf zijn muziek. Met het veld `muziek` vraagt het om een nummer uit het muziekregister (`MUZIEK` in de HTML): `darkafrica` voor `music/darkafrica.mp3`, en zonder dat veld loopt `music/bg.mp3` zoals altijd. In het menu en de bouwer klinkt altijd het gewone thema, en het spel wisselt alleen als er echt een ander nummer hoort te spelen, zodat het deuntje bij een levelwissel binnen dezelfde episode gewoon doorloopt. Mist het deuntje van een level, dan valt het spel terug op `bg.mp3` in plaats van stil te vallen. In de sandbox kies je zelf, onder **Muziek**: het thema of de nacht. Daar staat ook **Kreet bij een klap**, want Amir zegt er sinds kort iets van als hij geraakt wordt: twee korte kreten (`sounds/ahhit.mp3` en `sounds/stopit.mp3`), om en om, met een stilte van een paar seconden ertussen zodat hij niet de hele roedel doorpraat.

Een level kan ook de belichting bijstellen. De globale lichtlaag (een koele schaduwkant, warm licht richting de zon, en een onderkant die iets dieper wegzakt) ligt over het hele beeld heen. Met een veld `licht` in het uitzicht van een level (`SCENES`) zet je daar waarden overheen: dat is hoe de nachtlevels (Diepte 4 en 5) donker worden zonder dat er een tweede laag bij komt. Met **L** zet je de laag uit en met **,** en **.** stel je hem bij; die twee regelaars blijven gewoon van jou, ook in een level met een eigen belichting.

Test levels zijn korte proefstukken: een enkel level waarin je een mechaniek los kunt bekijken, zonder gevecht en zonder lange tocht eromheen. Ze staan met opzet apart van de echte episodes, zodat daar niets aan hoeft te veranderen om iets nieuws te kunnen proberen. **Test 1: Gang, dak en klimmen** loopt in drie stukken, met één plafondlijn die er overheen loopt en op twee plekken in beeld zakt. Eerst een dak van rots over de weg heen: boven de kei ligt het net hoog genoeg om erop te springen, en een stuk verder zakt het zo ver dat je met springen niets meer haalt. Dan een trap van drie terrassen omhoog en aan de andere kant weer omlaag, met het plafond dat er schuin overheen weer uit beeld loopt. En tot slot de gang: het plafond zakt schuin naar beneden tot er ruim een lichaamslengte over is, knijpt daarna dicht tot net boven je kruin, en gaat achterin weer omhoog. Daar, in de open lucht, staan de fakkels die het level uitspelen. De definitie staat in de HTML als `TEST_1`. **Test 2: De zwaardvechters** gaat over het nieuwe type tegenstander en verder nergens over: een vlakke strook over de open vlakte, zonder ravijnen en zonder klimwerk. Eerst een losse, zodat je zijn ritme kunt leren, dan een kalebas, en daarna twee die samen op je af komen: wie jou het eerst ziet roept de ander erbij. De definitie staat in de HTML als `TEST_2`. **Test 3: De rots met de rune** gaat over de rots die je met je speer openkrijgt: een lange vlakke strook naar links met een rotsboog en veel ruimte eromheen. In de boog zit een grot, en daarvoor een grote kei. De rots houdt je niet tegen: je loopt er gewoon doorheen. Op de linkerpoot van de boog zit een houten schijf met een rune. Raak je hem met de boogworp, dan blijft de speer er voorgoed in zitten, trilt de kei, en zakt hij met een wolk stof de grond in tot alleen zijn bovenkant nog als drempel in de vloer ligt. Ga voor de grot staan en druk op E: dan is het level uitgespeeld. Ondertussen staat er steeds een nieuwe speer in de grond op de vaste plek, dus je kunt zo vaak proberen als je wilt. De definitie staat in de HTML als `TEST_3`. **Test 4: De val in de grot** begint met een stukje savanne en dan een ravijn dat te breed is om over te springen. Je laat je erin vallen en belandt in een gang onder de grond, zes meter lager. Die val kost twee levens, dus beneden ligt een kalebas. Beneden is het donker: alleen de rand van de vloer vangt nog wat licht, en door het gat boven je valt een gedempte bundel daglicht. In de gang wachten een schorpioen en een zwaardvechter. Verderop zit een tweede gat in het dak, met treden van rots erin: daarlangs klim je weer naar boven, en op de savanne staan na nog een slang de fakkels. De definitie staat in de HTML als `TEST_4`. **Test 5: De fosforslangen** gaat over een nieuw soort slang: de fosforslang, donker mosgroen met geelgroene zadels en ogen die pulseren, een slag kleiner dan een gewone slang. Ze komen altijd met z'n drieën. Tot je in beeld komt kronkelen ze om elkaar heen; zien ze je, dan staan ze ineens stil, en even later komen ze snel op je af en bijten ze kort na elkaar. Eentje is gewoon te verslaan, met een steek of een lage zwaai, maar een zwaai raakt er maar één tegelijk. Twee lukt alleen met heel goede timing, drie niet. Hoe je ze dan wel verslaat zegt het level met opzet niet, dat mag je zelf uitzoeken. Je kunt er niet doodgaan, dus probeer maar wat. Hun beet kost normaal een half leven, en dat zie je dan als een half hartje. In de sandbox staan ze onder **3 fosforslangen**. De definitie staat in de HTML als `TEST_5`. **Test 6: Ravijn test** is een kort, vlak stuk savanne zonder vijanden, voor het ravijn dat openscheurt. Pak je speer op en loop door tot je een hoge, scheve rots ziet met op zijn flank een houten schijf met een rune. Gooi je speer ertegen: dat lukt met een gewone worp, en mis je, dan blijft hij in het steen steken. Raak je de rune, dan licht hij op en blijft je speer erin steken, en vlak achter de rots begint de grond te trillen, kruipt er een barst naar beneden, is het even stil en scheurt het ravijn open met een dreun en een wolk stof. Door het gat zie je de achtergrond van het level, net als bij een gewoon ravijn, en de rand van de overkant ligt even hoog als de grond waar Amir staat. Op die rand staat gras van het spel, dat meebuigt met de wind: kleiner dan het gras vooraan, iets in de kleur van de vlakte en met de voet achter de rand, zodat het op afstand staat. Het ingebakken gras uit de wandplaat is eruit, zodat een breed ravijn geen halve bosjes meer laat zien. In de winterlevels is de wand blauwgrijze steen, zoals de gewone ravijnen daar, ligt er sneeuw op de rand van de overkant met hier en daar een kale plek, en staat er berijpt gras dat net als het andere gras in de sneeuw stilstaat. Op een telefoon heeft het ravijn dezelfde maat ten opzichte van Amir als op een groot scherm, met minder stof. Je speer trek je er met E weer uit. Zolang de grond trilt en de barst loopt, kun je er nog overheen; is het ravijn open, dan val je erin, en ook als je er precies op stond. Er ligt hier niets onder, dus dat is dodelijk. Met een sprintsprong haal je de overkant. Vijanden stoppen aan de rand van het open ravijn, en wie op de plek stond toen het openging valt erin. Staat er iets op de plek waar het openscheurt, dan vallen kalebassen, botten en dorpelingen erin, en schuiven gras, struiken, keien en bomen met de rand mee opzij; staat er aan die rand al iets vlakbij, dan vervagen ze. Een speer in de grond, een kei om op te springen en een doornbos schuiven naar de rand. Een hut, een kei om op te springen en een doornbos mogen er niet staan waar later een ravijn openscheurt: het spel zet ze bij het laden aan de rand, en de bouwer laat je ze daar niet neerzetten. De definitie staat in de HTML als `TEST_6`. **Test 7: Werpen op gevoel** is het proefstuk voor de schaalworp (zie de speerworp hieronder): hoe langer je vasthoudt, hoe hoger en verder. Vier plekken, elk met een andere afstand of hoogte. Eerst een slang achter een kei, die er niet overheen kan: je gooit hem vanaf de kei, en een vlakke worp blijft in de kei steken. Dan een zwarte slang aan de overkant van een ravijn, die je eraf gooit voor je springt. Dan twee slangen achter een kei, de een dichtbij en de ander ver, dus twee hoeken na elkaar. En tot slot de rots met de rune zoals Test 3 hem eerst had, die hoog zit: daar is een hoge worp voor nodig. Staat de deur open, ga ervoor staan en druk op E. Je kunt hier niet doodgaan, dus een misser kost alleen tijd. De definitie staat in de HTML als `TEST_7`. **Test 8: Zegel test** gaat over het zegel in de grond: dezelfde houten schijf met de rune, maar plat in de savanne, in een ring van stenen. Het eerste zegel doet niets anders dan oplichten als je erop stapt en weer uitgaan als je er opnieuw op stapt, zodat je dat los kunt proberen. Het tweede scheurt de grond een stuk verderop open, precies zoals de rune in Test 6. Met een sprintsprong haal je de overkant. De definitie staat in de HTML als `TEST_8`. **Test 9: Brede ravijnen** laat zien dat het openscheurende ravijn op elke breedte werkt. Er staan drie rotsen met een rune, elk vlak voor zijn eigen ravijn: een gewoon, een dubbel en een driedubbel. Raak je een rune, dan scheurt dat ravijn open; hoe breder, hoe langer het barsten en openen duurt. Het gewone haal je open nog met een sprintsprong, het dubbele niet: daarvoor ligt er een zegel in de grond. Stap erop als het dubbele open is, dan licht het zegel op en gaat het ravijn weer dicht, en kun je door naar het driedubbele. In de sandbox staat zo'n zegel onder Zegel, Die het ravijn sluit. Is een ravijn weer dicht, dan gaan de rune en het zegel uit en kun je het opnieuw openen en opnieuw sluiten. Je kunt een rune ook raken als hij al aan is: de speer blijft er dan gewoon in hangen. De definitie staat in de HTML als `TEST_9`. **Test 10: Licht onder de grond** is een korte gang om het licht te bekijken: je valt door een brede ingang, loopt onder een smal gat in het dak door waar alleen licht doorheen valt, dan door een lang donker stuk waar je ogen aan het donker wennen en een schorpioen loopt, om te zien of je een vijand in het donker goed ziet, en klimt via een trap in een derde gat weer naar boven. Je kunt er niet doodvallen. De definitie staat in de HTML als `TEST_10`.

In het pauzemenu (II of Escape) staat **Level overslaan**: die brengt je meteen naar het volgende level van dezelfde reeks. Onder **Instellingen** staan daar ook het tempo van het spel, het looptempo van Amir, het formaat van het beeld en de muziek. Tijdens een level is het speelveld verder leeg: de testbalk met schuifjes staat alleen in de bouwer en de sandbox (met B haal je hem er tijdens het spelen alsnog bij).

## Op je telefoon zetten

Het spel is een installeerbare webapp. Open de Pages-link in Safari, deel, "Zet op beginscherm". Daarna staat Amir als icoon tussen je apps en start hij zonder browserbalken, liggend.

Open hem vanaf het beginscherm en druk in het startmenu op **Download voor offline**. Dat haalt alle sprites en geluiden in een keer binnen (ruim 2200 bestanden, ongeveer 230 MB; het precieze aantal staat in `offline-assets.json`). Vanaf dat moment laadt het spel meteen en speelt het ook zonder internet.

Doe die download vanuit het beginscherm-icoon, niet vanuit Safari: iOS geeft een geinstalleerde webapp een eigen opslag, dus wat je in Safari downloadt telt daar niet mee.

Ook zonder op die knop te drukken wordt alles wat je tijdens het spelen tegenkomt bewaard, dus een tweede potje laadt sowieso sneller.

### Beeld: scherp of licht

Van een deel van de sprites staan twee versies op schijf: het origineel, en een halve versie met dezelfde mappen en namen in `klein/`. Het spel kiest bij het starten: een telefoon krijgt de kleine set, een laptop en een tablet de grote. In het startmenu staat onder **Beeld** een schakelaar (Automatisch, Scherp, Licht) om dat te overrulen; wisselen herlaadt de pagina, want de sprites zijn dan al geladen.

Waarom: de grote frames zijn op een telefoon vele malen groter dan ze getekend worden. Safari houdt ze niet allemaal uitgepakt in het geheugen en decodeert ze midden in het spel opnieuw, en dat zijn de hikjes. De tekencode rekt elk plaatje naar vaste maten, dus beide sets werken met dezelfde code. Ontbreekt een klein frame, dan valt het spel terug op het grote.

Welke plaatjes meedoen staat in `DOELEN` in `tools/gen-klein.py`, en dat is met opzet een korte lijst. Een plaatje halveren mag alleen als het op een telefoon nog steeds groter is dan het stukje scherm waar het op terechtkomt. Dat is per familie gemeten en de factor staat erbij. Meedoen: Amir, de hyena's, de panters, de schorpioen, de zwaardvechters (2,7x), de dorpeling, het droge gras, de kei, de verre hut, de botten en de grotset (7,3x: het plafond, de hoekstukken en de wandtegels zijn de grootste bronnen van het spel en worden tot een tiende getekend). Er juist buiten vallen de boom (1,0x), de struik (1,2x), het doornbos (0,9x), de dorpshutten (1,8x), de klif (1,9x) en de dorpelinge (1,9x): die staan al vrijwel op maat, dus halveren zou je meteen zien.

De download volgt de gekozen set: een telefoon haalt de kleine versies binnen en slaat de grote over, een laptop andersom. Dat scheelt ongeveer 64 MB.

Sprites toegevoegd of vervangen? Draai dan eerst de kleine set opnieuw en daarna de offline-lijst:

```
python3 tools/gen-klein.py
python3 tools/gen-offline-manifest.py
```

Het eerste script print aan het eind de lijst die in de HTML onder `KLEIN_FAM` hoort te staan. Loopt die niet gelijk, dan laadt een familie stilletjes de grote versie.

Op een aanraakscherm tekent het spel op anderhalve canvaspixel per schermpixel in plaats van twee: op zo'n klein scherm zie je dat niet, en het scheelt bijna de helft van het werk per frame. Haalt het toestel de frames dan nog niet, dan zakt het spel vanzelf nog een stap (naar 1) en blijft daar; in de console staat dan een regel met "resolutie omlaag".

### Hoe het werkt

| bestand | rol |
| --- | --- |
| `manifest.webmanifest` | naam, icoon, liggend scherm, start zonder browserbalken |
| `icons/` | app-iconen, gemaakt uit `amir.png` |
| `sw.js` | de service worker: bewaart het spel en de assets, en serveert ze offline |
| `offline-assets.json` | de lijst die de downloadknop afwerkt |
| `tools/gen-offline-manifest.py` | genereert die lijst uit de bestanden op schijf |

De service worker houdt twee caches uit elkaar. Het spel zelf (HTML, manifest, iconen) gaat network-first: online speel je altijd de nieuwste versie, offline de laatst bekende. De sprites en geluiden gaan cache-first en blijven staan, ook als je het spel update. Een nieuwe versie van de HTML kost dus geen nieuwe download van 230 MB.

**Assets toegevoegd of vervangen?** Draai daarna:

```
python3 tools/gen-offline-manifest.py
```

De versie in `offline-assets.json` verandert mee, en de service worker ziet daaraan dat de oude assetcache weg mag.

## Besturing

| | laptop | telefoon |
|---|---|---|
| lopen, rennen | pijltjes, Shift sprint | joystick (duim links) |
| springen | pijl omhoog | ▲ |
| bukken | pijl omlaag | joystick omlaag |
| stoten | spatie (korte tik) | ✦ (korte tik) |
| **speer recht vooruit** | **spatie vasthouden, loslaten** | **✦ vasthouden, loslaten** |
| **speer in een boog** | **langer vasthouden, dan loslaten** | **langer vasthouden, dan loslaten** |
| worp afbreken | tik in plaats van vasthouden | duim van ✦ af slepen en daar loslaten |
| speer oppakken | E, waar je ook langs de schacht staat | E (verschijnt als je er vlakbij staat) |
| door een open deur of grot | E, als je ervoor staat | E (verschijnt als je ervoor staat) |
| drinken | Q | het kalebasje |

### De speerworp

Er wordt niet gemikt. Hoe lang je de knop vasthoudt bepaalt de worp, en de
animatie vertelt zelf welke je krijgt, want hij trekt in twee trappen uit:

| vasthouden | wat er gebeurt |
|---|---|
| tot 0,16 s | de oude stoot, ongewijzigd |
| tot ongeveer 0,77 s | eerste trap: hij trekt uit tot frame 4 en wacht daar. Loslaten geeft de vlakke worp |
| langer | tweede trap: frames 5 en 6 lopen alsnog door en daar wacht hij. Loslaten geeft de boog |

Die twee frames ertussen zijn de aankondiging. Zijn voorste arm komt omhoog en
naar voren, hij zakt dieper door zijn knieën, en er glinstert even iets op de
speerpunt. Daarom is er geen balkje en geen richtpijltje nodig.

De boog gaat 30 graden omhoog maar met 78 procent van de worpkracht: een lob,
geen verdragende worp. Vlak komt ongeveer 0,8 scherm verderop neer, de boog
piekt bijna drie keer Amirs lengte en landt rond 1,6 scherm. Lang vasthouden is
daarmee niet gewoon beter, want de boog zeilt over alles heen wat dichtbij
staat en je staat er een halve seconde langer kwetsbaar voor stil.

#### De schaalworp (proef)

Er is een tweede manier van werpen, voor wie meer zelf wil kiezen. In plaats van
twee vaste worpen loopt de hoek op zolang je vasthoudt. Hij trekt eerst helemaal
uit en legt de speer vlak; laat je dan los, dan gooit hij vlak. Blijf je
vasthouden, dan tilt hij de punt langzaam op, tot 30 graden in een halve seconde
(eerst langzaam, dan sneller, zodat je de lage hoeken fijn kunt kiezen). Daar
blijft hij staan, met een glinstering op de punt. Hoe hoger, hoe minder kracht,
net als bij de boog: tot 30 graden komt de speer steeds verder, van ongeveer 6,5
tot 14 keer Amirs lengte, en de volle 30 graden is precies de boog van hierboven.

Een vaag streepje voor de speerpunt wijst de hoek aan, niet de landing: waar hij
neerkomt moet je zelf leren inschatten. Een tik blijft de stoot.

Probeer het in **Test 7: Werpen op gevoel**, of zet het in de sandbox aan met de
knop **Worp** onder "Speerworp". In de episodes werp je nog in twee trappen.

Amir staat vast zolang hij spant en werpt: niet lopen, niet springen, en de hele
animatie is kwetsbaar. Tot en met frame 6 kan de worp nog afgebroken worden en
houdt hij zijn speer; vanaf frame 7 gaat hij door. Laat je los in de laatste 0,1
seconde voordat Amir geraakt wordt, dan gaat de speer alsnog weg.

De geworpen speer zakt door onder een derde van de zwaartekracht op Amir en
wijst elk frame de kant van zijn snelheid op. Raakt hij een dier, dan doet hij
schade en valt hij neer. Raakt hij grond of muur, dan blijft hij steken en
natrillen, en een speer die in een muur steekt is een dun platform waar je op
kunt staan (alleen van bovenaf; de schacht buigt 3 px door onder Amir). In een
doornbos richt hij niets aan: hij zakt de takken in tot iets minder dan de helft
van zijn lengte, het uiteinde hangt door en steekt eruit, en je trekt hem er met
E weer uit. Hak je het struweel daarna om, dan valt hij op de grond. Een speer
die ergens in steekt wordt achter Amir langs getekend, dus hij loopt nooit meer
dwars door hem heen als je ernaast gaat staan om hem te pakken.

Oppakken doe je bij de schacht, niet bij de punt: de E verschijnt zodra je bij
het stuk staat waar je hem vastpakt, en dat is meestal het stompe uiteinde.

Soms kom je niet meer bij je speer. Zonder speer hak je een doornbos niet weg en
springen er overheen kan niet, dus een speer achter een bos of ertussen op de grond is
kwijt. Hetzelfde geldt voor een speer die je terug gooit op een terras of berg waar je
net vanaf kwam en waar je van deze kant niet meer op komt. In al die gevallen staat hij
meteen naast je in de grond. Nooit aan de overkant van een ravijn, niet in het water en
niet op een ander terras. Blijft hij in een wand steken, dan wacht het spel gewoon tot
hij er vanzelf uit schiet.

Een speer blijft alleen zitten in de grond en in een houten runeschijf. In een
wand, een kei of de rand van het level wrikt hij zichzelf na vier seconden los
en valt hij naar beneden. De laatste seconde trilt hij, dus je ziet het
aankomen. Sta je erop, dan houdt hij het: de klok loopt alleen als je er niet
op staat, en hij gaat verder waar hij was zodra je eraf stapt. Zo blijft een
speer die te hoog in een steile wand terechtkomt nooit hangen waar je niet bij
kunt.

Je raakt hem nooit kwijt. Komt hij in het water of buiten de wereld terecht, dan
ligt hij na drie seconden weer op de laatste vaste grond waar Amir stond. Valt
hij in een ravijn, dan duikt hij na drie seconden aan de overkant op, net buiten
beeld: je loopt er vanzelf tegenaan zodra je de oversteek gehaald hebt. Gooi je
hem tijdens een bazengevecht het veld uit, dan telt dat net zo: je kunt de arena
niet uit, dus hij komt na drie seconden terug bij jou. Alles los te testen met
de knoppen onder "Speerworp" in de sandbox; onder "Ravijn" zet je er een breuk
naast om de rand te bekijken.

Tegen een panter geldt dezelfde regel als voor de stoot en de lage zwaai: raak
is hij alleen in zijn herstel, na een sprong, een duik of een tackle. Ziet hij
je de speer uittrekken terwijl hij op zijn poten staat, dan springt hij opzij,
en een speer die hem daarbuiten raakt ketst af op zijn vacht. De duik van de
witte panter zet hem tot zijn buik in de sneeuw: dat is het langste venster en
je staat er ver genoeg vanaf om te werpen.

## De slangen

Er zijn er twee, en ze zien er anders uit dan eerst. De eerste is de **zandslang**: bleek zand
met roestbruine zadels en een amberen oog, de kleur van de grond waar hij op ligt. Hij kruipt
naar je toe en bijt van dichtbij. De tweede is de **zwarte slang**: roetzwart met leisteengrijze
zadels, en die spuwt gif over een flinke afstand, dus die hoeft niet eens in de buurt te komen.
Waar het eerst fel groengeel tegenover fel zwartrood was, schelen ze nu in helderheid en niet in
schreeuwkleur, en staan ze allebei in de aardetinten van het landschap.

De frames komen uit `tools/slang_kleur.py`. Dat script kleurt de twee originele spritesets
(`enemies/slang1/` en `enemies/slang2/`) om naar `enemies/slang1_zand/` en `enemies/slang2_roet/`;
de tekening blijft staan, want per kleurvlak worden alleen de tint en de verzadiging vervangen.
Twee dingen houden met opzet hun eigen kleur: het amberen oog van de zandslang en het vlees in de
muil van de zwarte. In een leveldefinitie heten ze nog steeds `k: 'groen'` en `k: 'zwart'`.

**Ze verdwijnen niet meer bij een rots, en ze kunnen je kwijtraken.** Loopt een slang tegen een
kei of een wand, dan blijft hij daar duwen tot jij dichtbij genoeg komt. Vroeger gaf hij het na
vijf seconden op en loste hij ter plekke op, en dat was precies wat je zag gebeuren als er een
kei tussen jullie in stond. Ben je vijf seconden uit zijn gezichtsveld, dan draait hij om en gaat
hij patrouilleren: rustig heen en weer over een stuk zo lang als hijzelf, rond de plek waar hij je
kwijtraakte. Ziet hij je weer, dan gaat hij er meteen weer op af. Voor de zwarte telt niet het
beeld maar zijn schootsafstand: zolang jij binnen zijn spuugbereik bent houdt hij je in de gaten,
ook van buiten beeld, en pas vijf seconden daarbuiten gaat ook hij patrouilleren.

In de sandbox staat onder **Slangen** de knop **Op patrouille**: die zet alles wat er kruipt
meteen op patrouille en houdt het daar, zodat je het kunt bekijken zonder zelf uit beeld te
lopen. Nog een keer drukken en ze komen weer op je af.

## Het decor staat een stap naar achteren

De grond is geen lijn maar een band. De tegel `design/grondrand.png` heeft 49 rijen
grondoppervlak boven de looplijn, en dat is de strook waarop je van voor naar achter diepte
kunt maken. Amir en de dieren lopen op de voorrand van die band; het decor staat erachter,
op 55 procent van de band (`PROP_ACHTER`). Dorpsplaten gaan mee, en daar telt `depth` er
bovenop mee (`VILLAGE_DIEP`), zodat een hut op `depth: 0.85` ook echt verder weg staat in
plaats van alleen kleiner te zijn. De voorgrondhut blijft waar hij staat, want die hoort
juist vóór Amir langs.

Zonder die stap stonden gras, struiken, keien, putten en hutten op exact dezelfde lijn als
Amir, en dan sta je letterlijk in de planten: een pol gras komt dan tussen je voeten omhoog,
en een gevallen lichaam krijgt een struik door zijn borst. In de ontwerptekening van het
dorp staat het decor ongeveer 9 procent van Amirs lengte hoger dan zijn voeten, en op 0,55
van de band kom je daar precies uit. Verder terug kan niet: dieper is de tegel niet.

Klimrotsen, terrassen en richels blijven waar ze staan, want daar loop je op. Alleen decor
zonder botsing schuift mee.

## De zwaardvechter

De eerste menselijke tegenstander: een man met een zwaard, in drie kleuren (rood, blauw en
groen) die verder exact hetzelfde personage zijn. De frames staan in
`enemies/zwaardvechter/`, per kleur een map met zes animatiesets en een `metadata.json`
waarin het canvas, de grondlijn, het ankerpunt, de tempo's en de raakframes staan. Het spel
leest dat bestand bij het starten in; lukt dat niet, dan gelden de waarden die in de HTML
staan.

Hij is een volwassen man en Amir is zestien, dus hij is een kop groter: precies zo groot als
de dorpeling, ofwel 1,18 keer Amirs zichtbare lengte. Let op als je aan dat getal draait:
`CHAR_H` is niet Amirs kruin maar zijn hitboxhoogte, dus `ZW_H_SHARE: 1.00` zou hem juist
kleiner maken dan Amir.

Hij werkt in vier standen. Hij staat te wachten (**idle**) tot je in zicht komt, **dreigt**
dan een korte lus, **rent** op je af (sneller dan jij kunt sprinten, dus weglopen alleen
helpt niet), en **haalt uit** zodra hij dicht genoeg bij is. Die haal is zijn zwakke plek:
hij duurt anderhalve seconde, de klap valt na acht tiende, en zolang hij loopt staat de man
vast. Je hoort hem ook: zijn zwaai speelt hetzelfde geluid als jouw stoot, maar lager en
zachter, want het is dezelfde klap van staal door de lucht. Jouw speer reikt bovendien
verder dan zijn zwaard, dus er is altijd een stuk waarin jij hem wel kunt raken en hij jou
nog niet. Raak je hem, dan flitst hij wit op, stuitert hij een stukje achteruit en staat hij
even in zijn pijnpose; na drie treffers gaat hij neer. Het lichaam blijft zes seconden
liggen en zakt dan weg.

De metadata geeft alle zes de sets op 12 beelden per seconde. Twee daarvan spelen op dat
tempo te sloom en draaien daarom sneller (`ZW_SET_FPS`): de slag op 18 en zijn dood op 20.
Dat is een spelkeuze en geen correctie op de maker. Eén set wordt ook verticaal
bijgestuurd: de renframes staan 21 tot 105 px boven de grondlijn die voor alle sets geldt,
dus geen enkele voet raakte de grond. `ZW_ZAK` zakt die set terug tot het diepste frame
plant; de zweeffase blijft, want die hoort in een ren.

Staan er meer bij elkaar, dan roept de eerste die je ziet zijn maten erbij, en houden ze
onderling een lijf afstand: wie het dichtst bij je staat vecht, de rest wacht dreigend zijn
beurt af. Zonder die twee regels kom je ze een voor een tegen, of staan ze in elkaar.

In de sandbox staat hij onder **Zwaardvechter**: rood, blauw of groen neerzetten, en met
**AI uit** haal je de stekker uit zijn kop. Daarnaast, onder **Zijn animaties**, kies je de
set die hij dan speelt: idle, dreigen, rennen, slag, geraakt of dood. Een lus loopt rond, een
eenmalige set blijft op zijn laatste frame staan, zodat je de pose kunt bekijken. In een
leveldefinitie zet je hem neer met `{x: -1900, k: 'zwaard', c: 'rood'}`, waarbij `c` de kleur
is (`rood`, `blauw` of `groen`; zonder `c` wordt het rood). Voorlopig staat overal `rood`,
ook in het testlevel: de blauwe en de groene recolour zijn nog niet goed genoeg.

## Rots boven en naast je

Een rotsgebied is geen losse grotkamer maar terrein: een raster waarin elke cel vol of
leeg is. Amir loopt door de lege cellen als door een uitgehakte gang, en rots kan net zo
goed boven of naast hem zitten als eronder. Waar een cel leeg is zie je gewoon de lucht en
de savanne erdoorheen, dus een rotsmassa kan ook de bovenkant van een level zijn.

Het gesteente is hetzelfde gesteente als een terras. Rots is in dit spel al iets dat je
beklimt, met een bovenvlak om op te lopen en een geribbelde wand eronder, en een rotsgebied
gebruikt precies dat: een blok rots is van hetzelfde steen als de terrassen ernaast, en in
een winterlevel ligt er dezelfde sneeuw op. De zijkanten staan niet kaarsrecht maar breken
open, net als de zijkant van een terras.

De onderkant heeft een terras niet, want daar kom je bij een terras nooit. Rots met open
ruimte eronder krijgt daarom de tandenrand uit de grotset: een rij grillige punten die met
hun aanzet in het steen staan en met hun punten in de open ruimte hangen. Een rotsdak leest
daardoor als de onderkant van dezelfde berg waar de grond de bovenkant van is, of je nu
ergens onderdoor loopt of door een vallei met rots boven je.

Twee randen heeft de set niet, en die worden opgevuld met losse brokken: waar een vloer op
een wand uitkomt ligt een handvol keien over de naad, en waar een plafond tegen een hogere
wand aan loopt hangt er een blok in de hoek. Verder krijgt ongeveer een op de drie randen
iets mee, verstrooid met een vaste seed: hangblokken onder het plafond en keien op de
vloeren. Dezelfde seed geeft elke keer precies hetzelfde, maar niets staat op een
regelmatige afstand. Een richel om op te springen wordt niet verstrooid: die zet een level
neer waar hij als opstap bedoeld is.

Een cel is precies zo hoog als een terrastrede, en die hoogte schaalt mee met Amir. Op elk
scherm klim je dus wel op een blok van één cel en nooit op een blok van twee, en loop je
rechtop door een gang van twee cellen maar stoot je je hoofd als je springt.

De volle cellen zijn massief: je stoot je hoofd tegen het plafond, je loopt niet door een
wand heen en je staat op de vloeren. Een richel is een plankje waar je op kunt staan, met
een hitbox die alleen de bovenkant van het brok beslaat. Losse keien en hangblokken zijn
puur decor.

Alles los te proberen met de knoppen onder **Rots** in de sandbox: een gang met rots boven
en naast je, een dak om je hoofd aan te stoten, een uitstekende pilaar en een trap om op te
klimmen. Elke druk geeft een andere seed. Met **Hitboxen aan** zie je welke cellen vol zijn.

## Het plafond als hoogtelijn

Rots boven je hoeft geen raster te zijn. De grond van het spel is een hoogtelijn: per plek
in de wereld ligt vast hoe hoog de bodem daar zit. Een level kan het plafond op precies
dezelfde manier neerzetten, maar dan van bovenaf: een rij punten met een x en een hoogte,
en daartussen loopt de lijn recht door. Zo zakt de rots geleidelijk, loopt hij schuin, en
staat er nergens een hoek van negentig graden. Een punt ver boven de bovenrand van het
scherm betekent: hier is geen plafond, dus dezelfde lijn loopt over het hele level en komt
alleen in beeld waar je hem wilt hebben.

Het steen wordt in drie lagen getekend. Alles boven de lijn is gevuld met een rotstegel die
uit de plafondband zelf geknipt is, dus dezelfde brokken in dezelfde maat, naadloos en
altijd doorlopend tot voorbij de bovenrand van het scherm. Op de lijn hangt de band met de
grillige tandenrand, die met de helling meedraait. En langs de lijn hangen hier en daar
blokken en richels die er onderuit steken: die breken de lijn, zodat je geen rechte streep
over het steen ziet lopen. Ze staan op vaste plekken per level (een seed), en hoe verder de
lijn zakt, hoe kleiner ze worden, want je moet er niet doorheen hoeven lopen.

De ruimte boven de lijn is massief. Je stoot je hoofd tegen de lijn zelf, ook tegen een
schuin stuk, en waar de lijn onder je kruin duikt houdt het steen je tegen. De hangblokken
zijn puur decor; alleen een richel is een plankje waar je op kunt staan.

Los te proberen met de knoppen onder **Plafond** in de sandbox: een ruime gang, een krappe
gang waar springen niet meer lukt, een schuin zakkend stuk en een golvende lijn.

## De muur die je met je speer openkrijgt

Een rotswand die de weg verspert, met op het steen een houten schijf met een rune. Raak je die schijf met een geworpen
speer, dan licht de rune op, blijft de speer er voorgoed in zitten en schuift het rotsblok in een halve seconde omhoog de
berg in. Als hij opengaat hoor je de rots kraken en schuiven, en daarachter ligt een donkere gang waar je in kunt lopen.
Mis je, dan gebeurt er wat er altijd gebeurt als je een wand raakt: de speer blijft in het steen steken en valt er na een
tijdje vanzelf uit. Ondertussen staat er weer een nieuwe in de grond, dus je kunt zo vaak proberen als je wilt.

Zolang de muur dicht is zie je er niets van. Geen naad, geen contour, geen scheurtje in de vorm van een deur: de rots is
gewoon een rots, en het enige wat je opvalt is die houten schijf. Wat die doet moet je zelf bedenken.

Dat komt doordat gat en blok uit dezelfde pixels komen. Bij het laden wordt de plaat een keer op maat gezet, en daaruit
worden drie dingen gemaakt: de muur met de vorm van de opening eruit gegumd, het schuifblok dat precies dat uitgegumde
stuk is, en een masker dat de opening doorsnijdt met de rots zelf, zodat er nooit iets buiten de rots kan uitsteken.
Zolang het blok stilstaat wordt de plaat zelf getekend en verder niets, en dan is er per definitie niets te zien.

Waar de opening zit staat nergens als getal: het spel leest de doorzichtigheid van de rots uit en zoekt zelf de plek waar
het steen van de grond tot boven de deur massief is, en waar de bovenrand tegelijk laag genoeg is om je speer eroverheen
te krijgen. Op deze rots ligt dat een eind naar binnen, want de flank loopt schuin op. De schijf hangt net onder die
bovenrand, want in zijaanzicht is de rots massief: alles onder de rand zit in het steen, en daar komt geen speer ooit.

De rots staat altijd in zijn geheel in beeld, met zijn hele silhouet: hij wordt als geheel geschaald tot hij past, want
de camera staat op jou en laat een halve schermbreedte naast je zien. Hoe groot hij lijkt hangt daardoor aan het Formaat.
Op 25 is hij twee keer Amir, op 15 ruim drie en een half keer.

Je raakt de schijf alleen door er precies overheen te scheren, en dat lukt maar vanaf een strook van ongeveer honderd
pixels breed. Sta je dichter bij de deur, dan gaat de speer eronderdoor tegen de wand; sta je verder weg, dan zakt hij al
voor de rots. Springen en steken halen de schijf niet, en met de vlakke worp kom je er ook niet bij: alleen de volle boog
gaat eroverheen, dus je moet de werpknop helemaal uittrekken en goed kijken waar je staat.

### De grot met de kei

In Test 3 staat een tweede soort: geen rots met een deur erin, maar een rotsboog met een grot, en voor de ingang een
grote kei die hem helemaal afsluit. De houten schijf met de rune zit op de linkerpoot van de boog, naast de kei. Raak je
hem met de boogworp, dan licht de rune op, trilt de kei even, valt er gruis van de boog, en zakt de kei de grond in.
Langs zijn voet komt stof op dat opstijgt en uitwaait, en in de grotmond blijft een waas hangen die daarna zakt. De
bovenkant van de kei blijft als drempel in de vloer liggen. Ga voor de grot staan en druk op E.

Alles wat je ziet komt uit geschilderde platen: de rotsboog, de kei en het stof. Alleen het donker in de grot is erbij
gezet, en dat volgt precies de geschilderde rand van de boog.

De schijf hangt twee keer Amirs lengte hoog, zo dat je hem raakt van een plek waar hij nog in beeld staat: op een scherm
van 1280 bij 720 van ongeveer 465 tot 620 pixels ervoor. Sta je voor de rots of onder de boog, dan gooi je er gewoon
langs; mis je, dan blijft je speer pas steken waar hij van buitenaf het steen in vliegt.

## Het zegel in de grond

Een houten schijf met een rune, plat in de grond, in een ring van platte stenen met wat zand over de voorste. Stap je
erop, dan licht de rune op en gloeit het hout warm; stap je er later nog eens op, dan gaat hij weer uit. Eraf stappen doet
niets, dus wie blijft staan zet hem maar een keer om. Opgesprongen telt niet: je voeten moeten op de grond staan.

Een zegel is een schakelaar: wat er gebeurt als hij aangaat, zet een level erbij. Nu kan hij de grond openscheuren, met
hetzelfde ravijn als in Test 6: `zegels: [ {x: -900, ravijn: -1350} ]`. Dat gebeurt een keer per potje; zet je hem weer
uit, dan blijft het gat open. Zonder `ravijn` licht hij alleen op.

In de sandbox staat hij onder **Zegel**: **Neerzetten** legt er een voor je neer, **Met ravijn erachter** een die de
grond verderop openscheurt.

## Het skelet met de speer

Een zittend skelet tegen de grond, met een speer dwars door zijn borstkas en een blauw doek dat aan de schacht wappert.

- **De speer eruit trekken:** ga met lege handen bij de schacht staan en houd E vast (of de E-knop). Het skelet schudt
  steeds harder en de speer schuift eruit; rond de E loopt een ring vol. Na twee seconden laat hij los en ploft het
  skelet met een klap en een wolk stof in elkaar; de schedel rolt nog een stuk door. Laat je eerder los, dan blijft hij
  erin. De speer is nu de jouwe, met een blauw vaantje in plaats van het rode.
- **Heb je al een speer,** ook als je hem met E hebt weggestoken, dan kun je er geen tweede bij pakken: de speer wiebelt
  alleen en Amir laat weten dat hij hem niet nodig heeft. Dat geldt ook voor een speer die los op de grond ligt. Heb je
  je speer weggegooid, dan kan het wel, en blijft die van jou liggen waar hij ligt.
- **Een steek of een worp tegen de schedel** tikt hem eraf: hij valt, rolt even door en blijft liggen.
- **Een lage zwaai** laat het skelet meteen uit elkaar vallen, en de speer valt op de grond. Daar kun je hem later met
  E oprapen.
- De schedel is daarna gewoon decor: tegenaan lopen of erop slaan doet niets.

Pak je een speer terwijl die van jou ergens anders ligt, dan blijft de jouwe daar liggen.

Een level zet hem neer met `skeletten: [ {x: -900} ]`, met `f: true` wijst de schacht de andere kant op. Nog geen level
gebruikt hem. In de sandbox staat hij onder het tabblad **Decor**, bij **Skelet**: **Met speer**, **Gespiegeld**,
**Weer overeind** zet ze allemaal terug, en **Speer neerleggen** legt jouw speer naast je neer, zodat je met lege
handen een skelet kunt leegtrekken.

## Vallen doet pijn

Een diepe val kan een leven kosten. Dat staat standaard uit: de levels die er al waren zijn
ontworpen zonder valschade en spelen precies zoals je gewend bent. Een level zet het zelf
aan, en in de sandbox doe je het met een knop.

Staat het aan, dan telt niet hoe hard je neerkomt maar hoe diep je gevallen bent, gemeten
van de vloer waar je van losliet tot de vloer waar je landt. Je eigen sprong telt dus niet
mee: op je eigen niveau landen is altijd gratis, en van een kei of een lage trede afstappen
ook.

| hoe diep | wat het kost |
| --- | --- |
| minder dan een Amir | niets |
| een tot twee Amir | 1 leven |
| dieper dan twee Amir | 2 levens, en nooit meer |

In water landen kost niets: dat breekt je val. Een bodemloos ravijn blijft wat het was, daar
overleef je niets van.

Los te proberen met de knoppen onder **Vallen** in de sandbox. De knop zet de regel aan, en
de drie terrassen zetten je meteen boven op een wand van een, twee of drie Amir hoog.
Eraf stappen laat in beeld zien wat de val gekost zou hebben; levens raak je in de sandbox
nog steeds niet kwijt.

## Het uitzicht als je hoog staat

De achtergrond bestaat uit lagen die met verschillende snelheden meeschuiven: de verre bergen,
een tweede bergrij ervoor, en de savanneheuvels het dichtst bij. Klim je een terras op, dan zakt
jouw grond op het scherm mee met de camera, maar die lagen blijven achter, elk op hun eigen
tempo. De heuvels houden zich nu vast aan de voet van de bergen in plaats van aan jouw grond, dus
de bergrij blijft één geheel en de ruimte die het klimmen oplevert valt eronder: de vlakte waar
je vanaf het terras op neerkijkt, met de verre hutjes en acacia's erin. Wat daar geen geschilderd
paneel heeft, loopt van de nevelkleur van het level naar de grondkleur, zodat het als afstand
leest. Vroeger stond daar één effen kleur, en die lag er op een hoog terras als een blauwe balk
dwars door het landschap.

In de sandbox staan de knoppen onder **Uitzicht**: ze zetten je meteen op een terras van een tot
vier Amir hoog, zonder valschade, zodat je het uitzicht op hoogte kunt bekijken zonder een level
te klimmen. **Terug op de vlakte** haalt de terrassen weer weg.

## In een ravijn kijken

Een ravijn is een gat in de grond, en daar hoort je eigen wereld in door te lopen. Dat deed
het niet. De achtergrond houdt op de grondlijn op en daaronder lag een vlakke vulling over de
volle breedte van het scherm. Zolang de grond dicht is zie je daar niets van, maar door een
breuk hing die vulling als een donkere balk boven de overkant, met een kaarsrechte bovenrand
dwars over het gat. Dat is nu de eerste plek waar je naar keek, en het was het duidelijkste
teken dat het gat er als een rechthoek in lag geplakt.

Nu loopt de laag die op de grondlijn ligt naar beneden door, wat daar ook staat: de heuvels,
de nevel, het water, het uitzicht van dit level. Per kolom precies dezelfde kleur, dus er is
geen overgang te zien en er hoeft niets over de achtergrond geraden te worden. Daarna zakt het
weg, zodat je in het gat kijkt en niet door een gleuf naar de lucht erachter. Een aparte rand
met dikte en een slagschaduw zijn daardoor niet nodig: de achtergrond zelf doet het werk.

Twee dingen aan de kleur horen daarbij. Het steen van de overkant was de bleekste en de grijste
van het spel, met een verzadiging van 0,08, en het stond tegen de grondrand aan, de meest
verzadigde tegel die er is (0,51 voor de wand, 0,66 voor het loopvlak). Daar lag een waas
overheen die het wel lichter maakte maar niet warmer, en over grijs met de nevel van het level
erbij werd dat lila. Het wordt nu omgeverfd in plaats van overgoten: tint en verzadiging van de
grond, helderheid van het steen. En de nevel en het donker in het gat liepen tot anderhalve Amir
onder de grondlijn, terwijl je er maar 0,18 van de schermhoogte van ziet. Het hele verloop van
scherpe rand naar niets meer zien gebeurde dus buiten beeld. Het speelt zich nu af op het stuk
dat werkelijk in beeld staat.

De wand in een ravijn staat verder weg dan de grond waar jij staat, en ligt deels in de schaduw.
De rand aan de kant van de zon werpt een schuine schaduw op de wand, uit dezelfde richting als
waaronder de zon in een gang onder de grond naar binnen valt. Dat geldt voor een gewoon ravijn en
voor een ravijn dat openscheurt (de schaduw groeit dan mee), 's nachts zachter, en in de winter
koel en blauwig.

In de sandbox staat het onder **Ravijn**: **Smal** en **Breed** zetten een breuk neer waar je
staat.

## Onder de grond

Een ravijn kan een gang eronder hebben. Dan val je er niet dood in maar kom je beneden op de
vloer terecht, in het donker, met alleen het daglicht dat door het gat naar binnen valt. Wat
een level in die gang zet, staat ook echt beneden: de vijanden wachten je daar op, de
kalebassen liggen op de vloer, en de fakkels kunnen er ook staan, zodat een level onder de
grond kan eindigen. Een vijand in de gang loopt onder
een gat gewoon door, want voor hem is daar vloer; wie boven op de savanne staat, blijft boven.

Naar beneden toe gaat de aarde geleidelijk over in het steen van de gang. Naast een gat zie je
bovenop de vloer van de savanne, daaronder de aarde die donkerder wordt en overloopt in steen,
en onderaan hangen de tanden van het dak. In het gat zelf loopt de wand zonder tanden door
tot in de gang, met het daglicht erlangs, zodat je nergens een rechte streep ziet waar de
savanne ophoudt en de gang begint.

Het licht onder de grond komt van de hemel en de zon, en nergens anders vandaan. De zon staat
waar hij in de lucht van het level staat, en valt schuin door de gaten naar binnen: de rand van
een gat werpt een schaduw, de treden en jij vangen zon waar die echt binnenvalt, en hoe verder
de gang van een gat af loopt, hoe donkerder het wordt. Pikdonker wordt het nergens: er is een
ondergrens, zodat je de vloer, de randen en de treden altijd ziet. En je ogen wennen eraan: sta
je een paar tellen in het donker, dan wordt het vanzelf wat lichter, en loop je naar een gat of
een uitgang, dan zakt het weer, zodat je het verschil merkt. Jij en de vijanden staan in de
schaduw, maar minder donker dan de rots om je heen, zodat je een slang of een schorpioen in het
donker altijd op tijd ziet. Je schaduw ligt beneden ook gewoon onder je voeten op de bodem van de
gang. In de sandbox staan onder **Licht onder de grond** regelaars om dat bij te stellen: hoe
donker het wordt, waar de ondergrens ligt, hoe sterk je ogen wennen, hoeveel van het donker de
personages krijgen, hoe fel de zon naar binnen valt, hoeveel licht er van de wanden kaatst, en hoe
warm dat kaatslicht is.

Terug naar boven gaat niet via het gat waar je in viel, maar wel via een tweede gat in het dak
met treden erin. Die treden zijn van hetzelfde steen als de terrassen, en hoe dieper ze liggen,
hoe donkerder. Je springt van trede naar trede de schacht in, en van de bovenste stap je de
savanne op. Zolang je in de schacht staat, kun je niet zijwaarts de rots in: pas boven de
grondlijn kom je eruit. **Test 4** is het voorbeeld.

In de sandbox staat het onder **Onder de grond**: **Gang** legt een ravijn met een gang eronder
voor je neer, **Gang met trap omhoog** ook, met verderop een tweede gat met treden om weer
boven te komen, en **Gang weg** haalt het weer weg. Zet je een vijand neer terwijl je beneden
staat, dan komt die ook beneden.

## Mappenstructuur## Mappenstructuur

```
amir-king-of-africa.html   het spel
amir.png                   omslag / poster

karakters/
  amir/
    idle/                  idle_ns.png (zonder speer), idle_sp.png (met speer)
    aanval/
      speerstrike/         attack_sp_1..10.png
      lowsweep/            sweep_1..18.png (lage zwaai vanuit gebukt)
    beweging/
      run/run/             run_ns_1..8.png
      run/speerrun/        run_sp_1..8.png
      jump/jump/           amirjump0staand .. amirjump6landing.png
      jump/jumpspeer/      amirjumpspear0staand .. amirjumpspear6landing.png
      bukken/bukken/       bukken_in_1..8.png, bukken_hold_1..4.png
      bukken/bukkenspeer/  bukken_in_1..8_speer.png, bukken_hold_1..4_speer.png
  dorpeling1/
    dorpelingidle/         idle_01..12.png
  dorpelinge/              sfeerkarakter met kruik, 204x360, grondlijn rij 353, 12 fps
    idle/                  idle_00..17.png (lus)
    neerzetten/            neerzetten_00..25.png (eenmalig, gaat over in gehurkt)
    gehurkt/               gehurkt_00..17.png (lus)
    oppakken/              oppakken_00..25.png (eenmalig, gaat over in idle)
    metadata.json          framecounts en bounding boxes per frame
    preview/               sheets en preview-gifs, bronmateriaal

enemies/
  slang1/                  de originele groengele slang: idle_1..8, move_1..8, attack_1..8.png (+ mp4 referenties)
  slang1_zand/             de zandslang die het spel tekent (uit slang1/, via tools/slang_kleur.py)
  slang2/                  de originele zwartrode slang: idem, plus venom.png (het gif) en sprite sheets
  slang2_roet/             de zwarte slang die het spel tekent; venom.png blijft uit slang2/ komen
  schorpioen1/
    schorpioen_walk_12/    walk_01..12.png
    charge/schorpioen_charge_12/  charge_01..12.png
    schorpioen_curl_12frames/  curl_01..12.png
  blackpanther/
    blackpanther/          walk/, turn/, prowl/, pounce/, run/ (frames _00.. en sprite sheets)
    lowstrike/             claw_00..13.png (klauwhaal)
    pantherroar.mp3, panter snarl.mp3, panter_snarl_lang.mp3   pantergeluiden
  panter_wit/              de witte panter (Winter World): dezelfde frames, wit gemaakt met tools/winter_art.py
    panter_wit/            walk/, turn/, prowl/, pounce/, run/
    lowstrike/             claw_00..13.png
  hyena_wit/               de witte hyena (Winter World): loop/, dreigen/, ren_lijf/, ren_kop/, uit tools/winter_art.py
  zwaardvechter/           de zwaardvechter, in drie kleuren met identieke frames en maten
    basisacteur/           rode tunic (de bron)
    vijand_blauw/          blauwe tunic
    vijand_groen/          groene tunic
                           elk met idle/ (34), dreigen/ (12), rennen/ (10), slag/ (26),
                           geraakt/ (1) en dood/ (24), genummerd _00.. op 12 fps, plus
                           metadata.json (canvas 1150x981, grondlijn rij 925, anker_x 443,
                           figuur 800 px hoog, raakframes 15-17 van de slag). De frames
                           kijken naar rechts; het spel spiegelt ze als hij naar links kijkt
  hyena/
    loop/                  loop_00..19.png (aankomen en achteruit stappen)
    dreigen/               dreigen_00..21.png (op afstand blijven grommen)
    ren_lijf/              ren_lijf_00..11.png (onderlaag van de aanvalsren, 16 fps)
    ren_kop/               ren_kop_00..26.png (bovenlaag: de happende kop, 8 fps)
    metadata.json          canvas, grondlijn, aantallen, fps en de kop-offset per lijfframe
    preview/               sprite sheets en preview-gifs (bronmateriaal)

amir runc/
  amir_sprites/design/amir/
    speerworp/             speerworp_00..19.png (eenmalige worp, 20 frames, 12 fps),
                           metadata.json (canvas 984x814, grondlijn rij 803, anker_x 330,
                           Amir 620 px hoog, spannen 0-6, uithaal 7-10, los op 10, herstel 11-19)
    speer_projectiel.png   de geworpen speer, 624x67, punt naar rechts op pixel (623, 33)

items/
  potions/                 hppotion.png (de drinkkalebas die gezondheid teruggeeft)

design/
  *.png / *.jpg            losse props en texturen: boulder, tree, struik, villeaghut, drygrass,
                           cliff, flatrock, grondrand, rotstextuur, savannesand, speer, stofwolk, stofsliert, einde
  bg/laag1/                verre bergen (parallax laag 1); *_sneeuw.png = de winterversie (tools/sneeuw_bg.py)
  bg/laag2/                savanneheuvels (parallax laag 2); *_sneeuw.png = idem, met sneeuw op de ruggen en de vlakte
  botten/                  botten en schedels om op de grond te leggen
  grot/                    de grot- en ravijnset: plafond_strook, rots_vulling, hoek_plafond_wand, wand_rand,
                           wand_richel, hangblok_01..03, kei_01..07, kei_rond_01..08. In grot.json
                           staan de maten en de ankerpunten van elk onderdeel; de tekencode rekent
                           daarmee, dus de kleine versies in klein/ vallen precies op hun plek.
                           rots_vulling is het steen boven een plafondlijn en komt uit het massieve
                           deel van plafond_strook zelf (tools/rots_vulling.py); hoek_plafond_wand en
                           wand_rand worden niet meer getekend en blijven liggen voor later
  klimmen/                 klif_bovenrand, klif_richel, klif_binnenhoek
  *_sneeuw.png             winterversies van flatrock, boulder, cliff en de drie klimstukken; gemaakt
                           met tools/sneeuw.py (draai dat opnieuw als een origineel verandert).
                           grondrand_sneeuw en drygrass_sneeuw komen uit tools/winter_art.py.
                           villeaghut_sneeuw, tree_sneeuw, struik_sneeuw en de zeven platen in
                           village/*_sneeuw.png (sneeuw op het dak, de randen en de grond, bevroren
                           gras) komen uit tools/sneeuw_dorp.py
  grondrand_rots.png       de grond als grijze steen, zonder sneeuw: de rotsbodem van het veld sneeuw
  sneeuwlaag_25..100.png   het sneeuwdek als doorzichtige laag, in vier standen. Past op allebei de
                           bodems en is genest (wat op 25 wit is, is dat op 50 ook), zodat een level
                           onderweg van stand kan wisselen zonder dat er sneeuw verdwijnt.
                           Allebei uit tools/sneeuwdek.py
  vegetatie/               boom_sheet, drygrass_sheet, struik_sheet (bewegende vegetatie) en de losse frames
  water/                   pool_links/midden/rechts, rimpel_01..08, spetter_01..08

sounds/                    hyena_bite.mp3 (lange opname; alleen 14,0-16,0 s is de hap die het spel
                           afspeelt), hyena_laugh.mp3 (de lach), en ahhit.mp3 en stopit.mp3: de twee
                           kreten van Amir als hij geraakt wordt (om en om, met een stilte ertussen,
                           zodat hij niet de hele roedel doorpraat)

music/                     bg.mp3 (achtergrond), darkafrica.mp3 (het nachtdeuntje, onder Diepte 4 en 5),
                           stemmen van Amir (iamtheking, iamamir, iamamirfatherson,
                           hellomyfriend, ikill, protectinnocent, godsforsaken), snakehiss, spearthrust, scatter,
                           watersplash (de volle plons: instappen en landen) en waterstep (de korte knip
                           uit diezelfde plons, voor de voetstappen in het water)
```

De `*_magenta.png`, `*_preview.gif`, `*_sheet.png` en `*_spritesheet*.png` bestanden zijn bronmateriaal en voorbeelden; het spel gebruikt de losse frames.
