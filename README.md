# Amir: King of Africa

Een browserspel in een enkel bestand: open `amir-king-of-africa.html` in de browser (via een lokale webserver, bijvoorbeeld `python3 -m http.server`, zodat de sprites geladen mogen worden).

Alle sprites, achtergronden en geluiden staan los op schijf. Het spel verwacht de mappenindeling hieronder; de paden staan letterlijk in de HTML.

Linksboven staat in heel kleine letters van wanneer de versie is die je speelt. Onder **Updates** in het menu staan de
laatste vijf updates, rechtstreeks van GitHub, met bij elke of hij al in jouw versie zit. Zonder internet zie je alleen de datum.

## Episodes

In het menu onder **Levels** staan drie knoppen: **Episodes** (met de episode **De Valse Koning**), de **Test levels** en **Baboon tests**. De episodes De Poorten, De Honingjacht, De Hoge Schijven, De Klim en De Diepte zijn eruit, net als eerder De Jagers, Testrun, De Runen, De Vorst, Renew en Winter World; wat ze gebruikten (de uitzichten, de nachtmuziek, de winteruitrusting, de witte panter, zegels, runes en de poort in de rots) zit nog in het spel. De Valse Koning gebruikt daar veel van; de poort in de rots zelf staat nog in Test 3 en Test 7. In **Test 47** liggen zes zegels verstopt onder het zand, heel licht zichtbaar als een gleuf, elk onder een rode pijl: buk en sla het zand eraf met de lage zwaai. Het beeld staat even stil, een stofwolk bolt op (drie trage en drie snelle, van klein naar groot), en als hij optrekt loopt het licht door het teken met een ring over de grond; daarna werkt het zegel. In de sandbox staan ze onder **Verstopt zegel**, **Veeg** en **Wolk**. De traag-middel-wolk is nu de standaard voor elk verstopt zegel. In de nieuwe Maker (nieuwe stijl) zet je bij een zegel het vinkje **Verborgen (onder het zand)** aan: dan ligt het in de test onder het zand en gaat het pas aan als je eerst de lage zwaai erop hebt gedaan, ook zonder masker. Het zand heeft de kleur van de vloer: savanne, het schemerige zand in een gang, de zwarte vloer, sneeuw of rots; op zwart is de gleuf extra verstopt, op rots iets beter te zien. In de sandbox kies je dat onder **Vloer**.

**De Valse Koning** is een episode van acht zware levels, de langste en moeilijkste reeks. Een roverhoofdman heeft zichzelf tot koning gekroond, en zijn horde roept Amir "False king!" toe. Je begint met de tribekeuze, er is een verhaal voor wie bij het begin begint, en er is een **Nightmare**. De bandieten lopen als een rode draad door de hele episode, in al hun vormen: gewoon, met de dolk die ze op kophoogte werpen (buk ervoor), gehurkt in een hinderlaag die opspringt, en vaultend over een kei heen, zodat een schuilplek daar geen schuilplek is. Daaromheen zit zowat alles wat het spel kan. In **Valse Koning 1** openen de eerste rovers de jacht, met een zegel als val en een schijf die een ravijn overbrugt. **Valse Koning 2** neemt je over drie zuilen en een brug van steen de kloof over, met een hinderlaag bij de kei en een roedel aan de overkant. In **Valse Koning 3** val je een gang in met valschade, waar het plafond op je af zakt en de uitgang dichtgaat: rennen, langs de rovers. **Valse Koning 4** is de witte overval: een sneeuwstorm, een dal van zuilen, een lift van steen naar een terras vol rovers, en nog een schijf op een rots. In **Valse Koning 5** sta je voor het hoge kamp op een savannelaag, met rovers die over hun eigen keien springen, en in het gras ervoor ligt de zwarte panter als strijdbeest van de koning. **Valse Koning 6** is de horde: de hele roverbende komt in een oplopende golf van twee kanten op je af, elk eerst met zijn dolk, en vier keien zijn je enige schuilplek op weg naar de fakkels. **Valse Koning 7** is de koning zelf, die zich blijkt te verschuilen achter zijn strijdbeest: de baviaan jaagt je het level door, en de speerval in de wand is je enige kans. En **Valse Koning 8** is het eindgevecht in de arena van de koning. Je staat op een plateau dat boven een ravijn hangt, de touwen schuin de lucht in, en vlak ernaast staat een takelwiel op de vaste grond. Loop naar de rand bij het wiel en sla het: dan takel je met het plateau omhoog en uit beeld, je hoort het takelen kraken, het scherm fadet naar zwart en je fadet weer in terwijl datzelfde plateau je van onderaf de arena in takelt. Daar vult het plateau het ravijn precies, als een brug waar je op vecht. Daar staan twee van de elite-garde (zwarte rovers met een goud accent, in plaats van de gewone bruine) in de hoeken, de een gehurkt en de ander rechtop, allebei met de rug naar je toe, en ze hebben je nog niet gezien. Je staat stil en kijkt toe tot ze je horen, over hun schouder kijken en je opmerken; dan pas gaat het gevecht los, en allebei openen ze met een dolkworp. Heb je die twee verslagen, dan komen er twee uit de lucht, een van links en een van rechts, terwijl het plateau weer wegzakt en drie tellen later met twee nieuwe garde terugkomt. Versla ook die, dan is de leugen voorbij: er is nooit een koning geweest, alleen rovers, een beest en een naam om naar te roepen.

Een vaste afspraak in de episode: een schijf die je met je speer moet raken staat altijd rechtop op een rots, en een zegel ligt altijd plat in de grond en daar stap je op. Er wordt nooit een zegel met een speer geraakt. Zo zie je elke worp aankomen, en elke schijf is op een telefoon net zo goed te raken als op een laptop: `tools/runecheck.js` rekent per schermformaat na of de strook waar je hem raakt ook echt in beeld ligt.

Sneeuw hoeft niet de hele winteruitrusting te zijn. Naast `winter: true` kan een level het veld `sneeuw` zetten, en dat is een andere vraag: niet "speelt dit hoog in de bergen", maar "ligt hier sneeuw op de grond, en op wat voor grond". Daar staan twee dingen los van elkaar. De bodem is `savanne` (de gewone rode grond) of `rots` (dezelfde grond als grijze steen, `design/grondrand_rots.png`). Het dek is de sneeuw die daar bovenop ligt, als losse laag in vier standen (`design/sneeuwlaag_25` tot `100`, uit `tools/sneeuwdek.py`). Rode grond blijft dus rood onder de sneeuw, want een ondergesneeuwde zandvlakte is nog altijd zand, en grijs is een keuze voor een rotsbodem in plaats van iets wat er vanzelf bij komt zodra het sneeuwt. Met `van` en `tot` loopt het dek onderweg op: `sneeuw: { soort: 'savanne', van: -1200, tot: -7000 }` begint kaal en eindigt dicht, met de eerste plekken in de kuiltjes en de sneeuwrand die over de breukrand gaat hangen. Zonder `van` en `tot` ligt overal evenveel (`dek`, standaard 1). In de sandbox staat het onder **Sneeuwdek**: geen, savanne of rotsbodem, minder of meer, en een overgang die vanaf waar je staat naar links oploopt. `winter: true` verandert er niet door en houdt zijn eigen ingebakken sneeuwgrond.

Elk level heeft een voorgrond, en die geeft het beeld diepte: droog gras dat dichter bij de camera staat dan het pad, in twee lagen. De verre laag is kleiner en scherper en schuift trager, de dichtbije is groot en onscherp. Zet een level er zelf geen, dan krijgt het een ijle standaard die wegblijft bij ravijnen, zegels, runes, de poort, de fakkels en de eindbaas; in de winter is het gras besneeuwd. Het schuift sneller dan de wereld, is onscherp en donkerder, en staat met zijn voet onder de rand van het scherm. Zakt de camera een gang in, dan glijdt het gras omhoog het beeld uit en valt het weg; onder de grond staat er tussen jou en Amir aarde, geen gras. Het wordt nergens doorzichtig: Amir loopt erachter, niet erdoorheen, dus het gras is laag genoeg om normaal alleen zijn voeten en schenen te bedekken. In de sandbox staat hij onder **Voorgrond** bij Beeld en geluid: uit, gras, dicht gras of gemengd, en scherp of onscherp om te vergelijken. Een level zet hem met het veld `voorgrond`: stroken waar het groeit (hoe dicht, en welk deel struik of kei is), met open plekken en dichte pollen die elkaar afwisselen, en losse stukken op een vaste plek, zoals een kei of een buffelschedel die half in het gras ligt. **Test 11: Voorgrond** is Test 10 met zo'n voorgrond: vol aan het begin, ijler naar het ravijn toe, weg onder de grond, en weer dicht als je boven komt, met een open plek rond de fakkels.

Of het sneeuwt, verschilt per potje. Bij de start wordt een weerplan geloot: de hele tijd sneeuw, helemaal geen, sneeuw die onderweg begint, sneeuw die onderweg ophoudt, of een bui midden in het level. Het plan hangt aan de afstand door het level, en begin en einde gaan langzaam: over ongeveer een tiende van het level dikt de sneeuw aan of dunt hij uit, en vlokken die weg moeten vallen gewoon uit beeld. Ook de dikte van de bui verschilt per potje (`planSnow` in de HTML).

Een level kan het weer ook zelf vastleggen, met het veld `weer`: een lijst punten `{x, soort, sterkte}`. Zodra je voorbij zo'n punt bent slaat het weer om, en de overgang loopt over een paar honderd pixels, dus je loopt de bui in. Er zijn zes soorten: `droog`, `regen`, `onweer`, `zandstorm`, `sneeuw` en `sneeuwstorm`. Regen valt in schuine strepen op drie diepten, met spatjes op de grond en een glansrandje op de looprand; het beeld wordt er niet donkerder van en er komt geen waas over de lucht, hooguit een zweem koeler. Onweer is regen met om de paar tellen een flits en een schicht, en een tel later de donder. In een zandstorm en een sneeuwstorm vliegen korrels of vlokken bijna vlak door het beeld, met Amir mee naar links, waaien stofslierten of stuifsneeuw laag over de grond, en gaat alles wat in de wind beweegt plat: de planten, het gras, de schilden en de doeken van de speertekens. De woestijnwind klinkt dan hard door zolang de storm duurt. Sneeuw valt ook buiten een winterlevel; zet er het veld `sneeuw` bij, dan wordt de grond onderweg wit. Onder de grond is er geen weer, en je hoort het er gedempt. Het geruis van de regen en de donder maakt het spel zelf uit ruis, daar is geen opname voor. In de sandbox staat het onder **Weer** bij Beeld en geluid. **Test 13: Het weer** laat alles na elkaar zien: vijf ravijnen, en na elk ravijn slaat het weer om, van droog naar regen, onweer, zandstorm, sneeuw en sneeuwstorm.

In de winter is al het stof sneeuwstof (de stofplaatjes worden bij het laden wit gemaakt), en bij een landing of een lage zwaai stuift de sneeuw echt op: een brede lage wolk die blijft hangen, een waaier glinsterende kristallen en klonten die in een boog wegvliegen en bij het neerkomen een wolkje geven. Hoe harder je neerkomt, hoe groter de plof.

Een level met `winter: true` krijgt sneeuw op alles wat je beklimt (de `_sneeuw`-versies van de rotsen en klimstukken), een besneeuwde grond met grijze rots eronder, bevroren gras, sneeuwval, een besneeuwd uitzicht (de `_sneeuw`-versies van de bergpanelen en de heuvelrij in `design/bg/`, uit `tools/sneeuw_bg.py`: witte toppen, sneeuw op de ruggen en de vlakte) en witte dieren: de witte hyena's uit `enemies/hyena_wit` en de witte panter uit `enemies/panter_wit`. Die winterplaatjes worden pas geladen als je zo'n level kiest (er staat nu geen winterlevel in het menu, maar het spel kan het nog). Van het dorp bestaat ook een winterversie: de zeven dorpsplaten hebben elk een `_sneeuw`-tegenhanger (`hut_round_arch_sneeuw`, `well_sneeuw`, enzovoort) die je in een leveldefinitie onder `village` neerzet. De witte panter jaagt anders dan de zwarte: hij vervaagt in de sneeuw zolang hij sluipt (let op zijn schaduw), en zijn sprong is een hoge sneeuwduik die neerkomt op de plek waar je stond toen hij afzette. Bukken helpt niet, opzij stappen wel, en daarna zit hij even tot zijn buik in de sneeuw: dan steek je. Vanaf zijn tweede fase wisselt hij de duik af met de lage tackle.

Een level kiest zelf zijn muziek. Met het veld `muziek` vraagt het om een nummer uit het muziekregister (`MUZIEK` in de HTML): `bg` voor het oude thema `music/bg.mp3`, en zonder dat veld loopt `music/darkafrica.mp3`, de basismuziek van het spel. Bij de start en in het menu klinkt ook Dark Africa, en het spel wisselt alleen als er echt een ander nummer hoort te spelen, zodat het deuntje bij een levelwissel binnen dezelfde episode gewoon doorloopt. Mist het deuntje van een level, dan valt het spel terug op Dark Africa, en mist dat ook, op `bg.mp3`, in plaats van stil te vallen. In de sandbox kies je zelf, onder **Muziek**: het oude thema of de nacht (standaard). Daar staat ook **Kreet bij een klap**, want Amir zegt er sinds kort iets van als hij geraakt wordt: twee korte kreten (`sounds/ahhit.mp3` en `sounds/stopit.mp3`), om en om, met een stilte van een paar seconden ertussen zodat hij niet de hele roedel doorpraat. En als hij een vijand doodt zegt hij soms iets terug (`sounds/tausouldrest.mp3`): na elke verslagen eindbaas altijd, en bij de andere vijanden ongeveer een op de zeven keer.

Een level kan ook de belichting bijstellen. De globale lichtlaag (een koele schaduwkant, warm licht richting de zon, en een onderkant die iets dieper wegzakt) ligt over het hele beeld heen. Met een veld `licht` in het uitzicht van een level (`SCENES`) zet je daar waarden overheen: dat is hoe de nachtuitzichten (de `dark_`-blokken) donker worden zonder dat er een tweede laag bij komt. Met **L** zet je de laag uit en met **,** en **.** stel je hem bij; die twee regelaars blijven gewoon van jou, ook in een level met een eigen belichting. De rotsen met een rune krijgen daarnaast hun eigen zonlicht, uit dezelfde richting als de zon in de lucht: de flank en de toppen aan de zonkant vangen een warme rand, de andere kant ligt in de schaduw, en op de grond valt een slagschaduw van de zon af (in de sneeuw blauwig). 's Nachts is het zwakker.

De zon in de lucht is geen platte schijf meer. Hij heeft een lichte kern die naar de rand de kleur van het uitzicht krijgt, een zachte krans in de lucht en een brede gloed op de horizon eronder, en om de schijf zit een zachte ring die heel langzaam een klein beetje groter en weer kleiner wordt. Staat de zon laag, dan is zijn rand wat roder en platter. Er is nu ook een uitzicht voor midden op de dag, `middag`: de zon hoog en bijna wit, een blauwe lucht, een lichtere belichting en een korte schaduw onder Amir. De bergen zijn in avondkleuren geschilderd, dus daar ligt overdag een blauwige waas over, zoals de lucht in de verte doet; een uitzicht zet die met het veld `waas`. In de sandbox staat het onder **Tijd van de dag** bij Beeld en geluid (ochtend, middag, avond en nacht), en onder **Zon** stel je de gloed en het ademen van de ring bij.

Test levels zijn korte proefstukken: een enkel level waarin je een mechaniek los kunt bekijken, zonder gevecht en zonder lange tocht eromheen. Ze staan met opzet apart van de echte episodes, zodat daar niets aan hoeft te veranderen om iets nieuws te kunnen proberen. **Test 1: Gang, dak en klimmen** loopt in drie stukken, met één plafondlijn die er overheen loopt en op twee plekken in beeld zakt. Eerst een dak van rots over de weg heen: boven de kei ligt het net hoog genoeg om erop te springen, en een stuk verder zakt het zo ver dat je met springen niets meer haalt. Dan een trap van drie terrassen omhoog en aan de andere kant weer omlaag, met het plafond dat er schuin overheen weer uit beeld loopt. En tot slot de gang: het plafond zakt schuin naar beneden tot er ruim een lichaamslengte over is, knijpt daarna dicht tot net boven je kruin, en gaat achterin weer omhoog. Daar, in de open lucht, staan de fakkels die het level uitspelen. De definitie staat in de HTML als `TEST_1`. **Test 2: De lege vlakte** is een vlakke strook zonder tegenstanders, met een kalebas halverwege. Hier stonden de zwaardvechters; die zijn uit het spel, en het level is gebleven zodat de nummers van de andere tests niet verschuiven. De definitie staat in de HTML als `TEST_2`. **Test 3: De rots met de rune** gaat over de rots die je met je speer openkrijgt: een lange vlakke strook naar links met een rotsboog en veel ruimte eromheen. In de boog zit een grot, en daarvoor een grote kei. De rots houdt je niet tegen: je loopt er gewoon doorheen. Op de linkerpoot van de boog zit een houten schijf met een rune. Raak je hem met de boogworp, dan blijft de speer er voorgoed in zitten, trilt de kei, en zakt hij met een wolk stof de grond in tot alleen zijn bovenkant nog als drempel in de vloer ligt. Ga voor de grot staan en druk op E: dan is het level uitgespeeld. Ondertussen staat er steeds een nieuwe speer in de grond op de vaste plek, dus je kunt zo vaak proberen als je wilt. De definitie staat in de HTML als `TEST_3`. **Test 4: De val in de grot** begint met een stukje savanne en dan een ravijn dat te breed is om over te springen. Je laat je erin vallen en belandt in een gang onder de grond, zes meter lager. Die val kost twee levens, dus beneden ligt een kalebas. Beneden is het donker: alleen de rand van de vloer vangt nog wat licht, en door het gat boven je valt een gedempte bundel daglicht. In de gang wachten een schorpioen en een zwaardvechter. Verderop zit een tweede gat in het dak, met treden van rots erin: daarlangs klim je weer naar boven, en op de savanne staan na nog een slang de fakkels. De definitie staat in de HTML als `TEST_4`. **Test 5: De fosforslangen** gaat over een nieuw soort slang: de fosforslang, donker mosgroen met geelgroene zadels en ogen die pulseren, een slag kleiner dan een gewone slang. Ze komen altijd met z'n drieën. Tot je in beeld komt kronkelen ze om elkaar heen; zien ze je, dan staan ze ineens stil, en even later komen ze snel op je af en bijten ze kort na elkaar. Eentje is gewoon te verslaan, met een steek of een lage zwaai, maar een zwaai raakt er maar één tegelijk. Twee lukt alleen met heel goede timing, drie niet. Hoe je ze dan wel verslaat zegt het level met opzet niet, dat mag je zelf uitzoeken. Je kunt er niet doodgaan, dus probeer maar wat. Hun beet kost normaal een half leven, en dat zie je dan als een half hartje. In de sandbox staan ze onder **3 fosforslangen**. De definitie staat in de HTML als `TEST_5`. **Test 6: Ravijn test** is een kort, vlak stuk savanne zonder vijanden, voor het ravijn dat openscheurt. Pak je speer op en loop door tot je een hoge, scheve rots ziet met op zijn flank een houten schijf met een rune. Gooi je speer ertegen: dat lukt met een gewone worp, en mis je, dan blijft hij in het steen steken. Raak je de rune, dan licht hij op en blijft je speer erin steken, en vlak achter de rots begint de grond te trillen, kruipt er een barst naar beneden, is het even stil en scheurt het ravijn open met een dreun en een wolk stof. Door het gat zie je de achtergrond van het level, net als bij een gewoon ravijn, en de rand van de overkant ligt even hoog als de grond waar Amir staat. Op die rand staat gras van het spel, dat meebuigt met de wind: kleiner dan het gras vooraan, iets in de kleur van de vlakte en met de voet achter de rand, zodat het op afstand staat. Het ingebakken gras uit de wandplaat is eruit, zodat een breed ravijn geen halve bosjes meer laat zien. In de winterlevels is de wand blauwgrijze steen, zoals de gewone ravijnen daar, ligt er sneeuw op de rand van de overkant met hier en daar een kale plek, en staat er berijpt gras dat net als het andere gras in de sneeuw stilstaat. Op een telefoon heeft het ravijn dezelfde maat ten opzichte van Amir als op een groot scherm, met minder stof. Je speer blijft in de rune zitten: die krijg je er niet meer uit. Zolang de grond trilt en de barst loopt, kun je er nog overheen; is het ravijn open, dan val je erin, en ook als je er precies op stond. Er ligt hier niets onder, dus dat is dodelijk. Met een sprintsprong haal je de overkant. Vijanden stoppen aan de rand van het open ravijn, en wie op de plek stond toen het openging valt erin. Staat er iets op de plek waar het openscheurt, dan vallen kalebassen, botten en dorpelingen erin, en schuiven gras, struiken, keien en bomen met de rand mee opzij; staat er aan die rand al iets vlakbij, dan vervagen ze. Een speer in de grond, een kei om op te springen en een doornbos schuiven naar de rand. Een hut, een kei om op te springen en een doornbos mogen er niet staan waar later een ravijn openscheurt: het spel zet ze bij het laden aan de rand. De definitie staat in de HTML als `TEST_6`. **Test 7: Werpen op gevoel** is het proefstuk voor de schaalworp (zie de speerworp hieronder): hoe langer je vasthoudt, hoe hoger en verder. Vier plekken, elk met een andere afstand of hoogte. Eerst een slang achter een kei, die er niet overheen kan: je gooit hem vanaf de kei, en een vlakke worp blijft in de kei steken. Dan een zwarte slang aan de overkant van een ravijn, die je eraf gooit voor je springt. Dan twee slangen achter een kei, de een dichtbij en de ander ver, dus twee hoeken na elkaar. En tot slot de rots met de rune zoals Test 3 hem eerst had, die hoog zit: daar is een hoge worp voor nodig. Staat de deur open, ga ervoor staan en druk op E. Je kunt hier niet doodgaan, dus een misser kost alleen tijd. De definitie staat in de HTML als `TEST_7`. **Test 8: Zegel test** gaat over het zegel in de grond: dezelfde houten schijf met de rune, maar plat in de savanne, in een ring van stenen. Het eerste zegel doet niets anders dan oplichten als je erop stapt en weer uitgaan als je er opnieuw op stapt, zodat je dat los kunt proberen. Het tweede scheurt de grond een stuk verderop open, precies zoals de rune in Test 6. Met een sprintsprong haal je de overkant. Een zegel kan ook een ander teken op het hout hebben. De tekens betekenen niets, je leert ze kennen aan wat ze doen: de rune zet jij aan, en een zegel met het tweede teken (twee hoekige haken naast elkaar) is een val: ook een vijand die erop stapt zet hem aan. De andere zeven tekens hebben nog geen bestemming. Ligt het ravijn onder het zegel zelf, spring er dan overheen en laat een vijand achter je aan komen: stapt hij erop, dan scheurt de grond onder hem open, staat hij vast zolang het scheurt, en valt hij erin, samen met het zegel. Stap je er zelf op, dan heb je nog even om weg te rennen. In de sandbox staat dat onder Zegel, **Val voor vijanden**, en de tekens onder **Zegelteken**. De definitie staat in de HTML als `TEST_8`. **Test 9: Brede ravijnen** laat zien dat het openscheurende ravijn op elke breedte werkt. Er staan drie rotsen met een rune, elk vlak voor zijn eigen ravijn: een gewoon, een dubbel en een driedubbel. Raak je een rune, dan scheurt dat ravijn open; hoe breder, hoe langer het barsten en openen duurt. Het gewone haal je open nog met een sprintsprong, het dubbele niet: daarvoor ligt er een zegel in de grond. Stap erop als het dubbele open is, dan licht het zegel op en gaat het ravijn weer dicht, en kun je door naar het driedubbele. In de sandbox staat zo'n zegel onder Zegel, Die het ravijn sluit. Is een ravijn weer dicht, dan gaan de rune en het zegel uit en kun je het opnieuw openen en opnieuw sluiten. Je kunt een rune ook raken als hij al aan is: de speer blijft er dan gewoon in hangen. Een speer in een rune krijg je er niet meer uit, dus na de eerste en de tweede rots zit een skelet met een nieuwe. De definitie staat in de HTML als `TEST_9`. **Test 10: Licht onder de grond** is een korte gang om het licht te bekijken: je valt door een brede ingang, loopt onder een smal gat in het dak door waar alleen licht doorheen valt, dan door een lang donker stuk waar je ogen aan het donker wennen en een schorpioen loopt, om te zien of je een vijand in het donker goed ziet, en klimt via een trap in een derde gat weer naar boven. Je kunt er niet doodvallen. De definitie staat in de HTML als `TEST_10`. **Test 12: Mikken** heeft vijf rotsen achter elkaar, elk met een rune op een andere plek: een grote scheve spits, twee zuilen, een hoge rots met pieken, een scheve boog en een kleine spits, met de schijf steeds boven wat Amir springend haalt. Het level gebruikt de schaalworp, dus hoe langer je vasthoudt, hoe hoger. Raak je een schijf, dan gloeit hij fel op en blijft hij aan, en je speer blijft erin zitten. Na elke rots zit een skelet met een speer: houd E vast en je hebt een nieuwe. Mis je, dan valt je speer na een paar tellen uit het steen en raap je hem op. Je loopt door de rotsen heen, en gooi je van binnen een rots, dan vliegt de speer er gewoon uit. De definitie staat in de HTML als `TEST_12`. **Test 13: Het weer** is een vlakke tocht zonder vijanden met vijf ravijnen, en na elk ravijn slaat het weer om: regen, onweer, een zandstorm tussen veel planten, een schild en een speerteken, sneeuw waarbij de grond langzaam wit wordt, en een sneeuwstorm. De definitie staat in de HTML als `TEST_13`. **Test 14: De drie stammen** begint met een scherm waarop je zelf kiest welke talents er gelden: alle negen, een hele tribe of een paar losse, ook die van Impungushe. In het pauzemenu kies je met **Talents kiezen** opnieuw. Het level heeft een stuk per tribe: voor Mkuki een slang achter een ravijn om naar te gooien, een doornbos en twee slangen voor de lage zwaai; voor Bhubesi een rij vijanden om de woede te vullen en dan een roedel van drie; voor Impungushe kalebassen aan een koordje en een doornbos voor het mes, een rune die je speer vasthoudt zodat je met alleen het mes langs een schorpioen en een slang moet, een skelet met een nieuwe speer, en een zwaar slot met twee zwaardvechters en een roedel, waar Feign Death je kan redden. De definitie staat in de HTML als `TEST_14`. **Test 28: Hoog mikken** heeft vier runes op rotsen, allemaal hoog, en elk doet iets. Het zegel aan het begin scheurt verderop de grond open; de rune op de pieken sluit dat ravijn weer, maar hij zit zo hoog dat je hem van de grond alleen blind raakt, dus je klimt op de kei ervoor. Achter de twee zuilen raak je de tweede rune met een boog, en de grond erachter scheurt open. Op een hoog terras staat een spits: klim erop en raak hem, dan gaat de grond verderop open naar een gang, en alleen daar beneden staan de fakkels. In de donkere gang staat nog een rots, en die rune scheurt het dak open zodat er licht in valt. Na elke rune zit een skelet met een nieuwe speer. De definitie staat in de HTML als `TEST_28`. **Test 29: De bandieten** is het proefstuk voor de nieuwe tegenstander (zie **De bandiet** hieronder): een open, vlakke savanne zonder ravijnen, zodat ze altijd bij je komen. Er komt telkens een bandiet bij, net buiten beeld, om en om links en rechts, en het tempo loopt op, van een om de drie seconden naar een om de 0,8 seconde. Ze rennen op je af, halen uit met hun kromzwaard, en schieten in die uitval een stuk door met stof bij hun voeten: stap weg, laat ze voorbijglijden en steek ze in de rug voor ze zich omdraaien. Vier kalebassen onderweg om het vol te houden, en een teller in beeld houdt bij hoeveel je er verslaat en hoe lang je het redt. Het is een gauntlet naar de fakkels toe: haal je ze, dan is het level uit. De definitie staat in de HTML als `TEST_29`. **Test 30: De dolkwerpers** is dezelfde oplopende golf, maar nu gooien de bandieten eerst hun dolk: zodra er een je ziet blijft hij staan, slingert zijn dolk naar je romp, en rent dan pas in om uit te halen. De dolk tolt door de lucht en kost een leven als hij raakt, dus naast het wegstappen van de haal moet je nu ook de dolk ontwijken, met een sprong of een stap opzij. Een tandje rustiger dan Test 29, want dat gooien is een extra dreiging, op een aride hoogvlakte. De definitie staat in de HTML als `TEST_30`. **Test 32: Het takelwiel** gaat over een nieuw mechaniek: een houten tandwiel op de grond met een plateau dat eraan hangt, aan twee aparte touwen uit twee verborgen katrollen boven het scherm, die naar boven uit elkaar lopen zodat je twee losse touwen leest in plaats van een V. Sla het rad met je speer (de stoot of de lage zwaai): er vliegen houtsplinters af, er klinkt een houten tik, het rad houdt even in (een korte krak-hapering, alsof het hout vangt) en draait dan een kwartslag door, en het plateau zakt of stijgt een stap, want de hoogte van het plateau hangt recht aan de draaistand van het rad, en zolang het draait kraakt het touw. Aan de top draait de richting vanzelf om, zodat je het met hetzelfde rad ook weer omhoog draait. In het level hangt het plateau eerst hoog boven een smal ravijn; draai het omlaag tot het als brug over het ravijn staat en steek over. Op elk aanhechtpunt zit een spijkerknop over het touw, en het plateau is veerend: loop je erop, dan zakt het wat, maar spring je erop, dan zakt het dieper en schommelt het even na, naar de kant waar je landt. Zolang het op of neer takelt, kraakt het touw hoorbaar. Het ravijn is smal genoeg om er desnoods overheen te sprinten, dus je loopt nergens vast. In de sandbox staat het onder Terrein, **Takelwiel**: neerzetten, het rad slaan en weghalen. De definitie staat in de HTML als `TEST_32`. **Test 33: De bandieten op het plateau** bouwt daarop voort: je loopt naar links en komt bij een breed ravijn. Aan de overkant staat een bandiet bij een takelwiel, en zodra je in de buurt bent slaat hij het rad. Het plateau hangt met twee bandieten erop in het ravijn en stijgt stap voor stap tot het de hele kloof overbrugt. Boven aangekomen stormen de twee bandieten de brug af en vallen je aan op je eigen grond, elk op een eigen manier: de een zit gehurkt tijdens de rit en springt pas op als de brug er staat (en gooit dan zijn dolk), de ander staat rechtop en gooit zijn dolk meteen bij aankomst, dus buk ervoor. En zodra de brug er ligt steekt de takelaar zelf ook over en voegt zich erbij. Het plateau is een gewoon platform: je kunt erop springen en er weer af. Is de brug er eenmaal, dan kun je zelf ook oversteken naar de fakkels daarachter. De definitie staat in de HTML als `TEST_33`. **Test 34: De brug doorsnijden** heeft dezelfde opzet, een takelaar die twee bandieten op een plateau omhoog tilt, maar nu zijn de twee touwen van de brug door te snijden. Gooi je speer dwars door een van de touwen terwijl de bandieten erop staan, dan knapt het, kantelt de brug en stort hij met de bandieten erop het ravijn in: zo reken je ze in een keer af. Je speer vliegt gewoon verder en blijft in de overkant steken, dus je raakt hem niet kwijt. Alleen is het gat nu te breed om overheen te springen. Daarvoor is er een uitweg: zodra de brug gevallen is verschijnt er verderop een zegel in de grond, en stap je daarop, dan komt er rijzende grond omhoog die het ravijn dicht, zodat je toch door kunt. Wil je de bandieten liever gewoon bevechten, laat de touwen dan heel en steek over op de brug zoals in Test 33. De definitie staat in de HTML als `TEST_34`. **Test 40: Bloed** is het proefstuk voor het bloed-systeem: een vlak stuk savanne met twee gewone bandieten, die hier elk drie treffers nodig hebben. Elke rake klap laat een snee op hun lichaam achter, die op hun huid blijft kleven en meebeweegt, en treffer twee is groter dan treffer een. De derde klap is dodelijk: de bandiet reelt geraakt achterover, uit een snee op zijn borst spuit bloed opzij (met een geluid), en dan valt hij. De snedes blijven op het lijk zitten. In de sandbox staat het onder Vijanden, bij de bandiet: **Bloed aan** (en **Spuit: fel** of **donker** voor de twee varianten van de spuit). De definitie staat in de HTML als `TEST_40`. **Test 41: De lift** bouwt het takelwiel uit tot een lift met twee wielen: een naast het plateau beneden en een naast het plateau boven. Sla het onderste wiel en het plateau takelt in een keer helemaal omhoog, sla het bovenste en het zakt in een keer helemaal omlaag, anders dan het stap-voor-stap-rad van Test 32. Je takelt jezelf omhoog naar een rotsetage, verslaat daar een gehurkte bandiet en stapt op een zegel dat de strook tussen het plateau en de etage openscheurt: een gat in het dak van de gang eronder. Terug omlaag laat je je daarin vallen en loop je door de gang naar de trap aan de andere kant. Het plateau hangt zo hoog dat eraf vallen twee levens kost (maximale valschade). Amir heeft een reserve speer op zijn rug, net als in Test 39, en onderweg over de vlakte staan bandieten, hyena's en kooimannen. De definitie staat in de HTML als `TEST_41`.

**Baboon tests** is de plek waar de baviaan stuk voor stuk uit elkaar gehaald wordt: drie proefstukken, met de tribekeuze voor het begin zoals elke episode. Ze stonden eerst tussen de Test levels; wat bij de baviaan hoort staat nu bij elkaar. Wat er in een level goed werkt en wat niet komt in `notities/combinaties.md`.

Er komt een nieuwe eindbaas aan: een baviaan. In **Baboon 1** hangt hij aan de rotswand en beweegt hij, en je begint zo ver van hem af dat je hem nog net ziet. Je hebt geen speer: die zit in een skelet tussen jou en hem in. Trek je hem eruit (E vasthouden), of kom je te dichtbij, dan springt hij neer. Verderop liggen twee ravijnen met een stuk grond ertussen: spring je daarop, dan springt hij over allebei heen en brult hij je van de overkant aan, en ga je eraf, dan landt hij voor je neus en brult weer. Zo houdt hij je op dat stuk vast. In de sandbox staat hij bij Vijanden onder **Baviaan**: **Neerzetten** zet hem een stukje voor je neer, met zijn gezicht naar Amir. Met de pijltjes schuif je hem naar links, rechts, omhoog en omlaag, met min en plus maak je hem kleiner of groter, en **Spiegel** draait hem om. Houd je een knop vast, dan gaat hij door, steeds sneller. Naast de knoppen staan de getallen: waar hij staat, hoe hoog hij boven de grond hangt en hoe groot hij is, allebei in Amir, zodat je ze kunt doorgeven als hij goed staat. Het plaatje is uit de magenta achtergrond geknipt met `tools/baviaan_knip.py` en staat in `enemies/baviaan/`.

In **Baboon 3: De speerval** is hij wel te verslaan. Hij hangt weer achter je aan de rotswand, springt neer, brult, schudt
twee keer zijn kop en stormt dan op je af. In de rotswand aan het eind zit een speer met de punt naar jou, met een zegel
ervoor (zie de speerval hieronder). Stap op het zegel als hij achter je aan komt en buk meteen: de speer vliegt over je
heen en recht in de borst van de baviaan, en daar blijft hij in zitten. Denk niet te snel dat je gewonnen hebt: hij deinst terug, gromt, brult je nog een keer
aan en twijfelt, met de speer nog in zijn borst, en pas dan zakt hij in elkaar, voorover op de speer. Zolang dat duurt sta je stil en kijkt de camera naar hem. De fakkels
staan voor het zegel en blijven dicht zolang hij leeft; daarna loop je terug. In de sandbox laat **Dood** (onder Baviaan)
het hele stuk zien, en **Dood door speerval** hetzelfde met de speer in zijn borst (of met **Spiegel** in zijn rug).

**Baboon 4: De arena** is een overlevingsronde. Twee grijze rotswanden houden je in het midden, en daaraan hangen kleine
gouden aapjes (honinggoud met een blauw gezicht, ruim een halve Amir groot): drie links en drie rechts, op wisselende
hoogtes, hoog en laag. Zolang ze hangen kun je proberen ze met een geworpen speer te raken. Af en toe laat er eentje zich
vallen, vlak voor de wand, en rent op je af; welke en wanneer is willekeurig. Beneden rennen ze op je af, dreigen soms kort
of lopen even, springen af en toe over je heen, en happen als ze dichtbij zijn, op een tempo waarop één aap goed te doen is.
Eén klap, een stoot of de lage zwaai, is genoeg: dan gaat hij dood. Springt er een naar beneden, dan kun je hem in de lucht
met een geworpen speer raken; op de grond vliegt de speer eroverheen. Een aap die je zo raakt valt met je speer in zich neer
en blijft liggen tot je met E je speer eruit trekt. Een lege plek aan de wand wordt na een tijdje weer gevuld, en het worden
er langzaam meer tegelijk, oneindig, tot je dood bent. Bovenaan lopen je kills en je tijd mee, en elke paar kills verdien je een
talentpunt dat je in de pauze onder Talents kunt uitgeven. Het level begint met de tribekeuze, net als de rest van Baboon.
In de sandbox staan de aapjes bij Vijanden onder **Goudaap**: **Los aapje** zet er een neer, **Arena aan/uit** start de
hele arena, en **Alle apen weg** ruimt ze op. De spriteset is de baviaan omgekleurd met `tools/goudaapje_kleur.js`.

In **Test 15: Het zakkende plafond** laat je je in een ravijn vallen en loop je onder de grond door een lage doorgang.
Vlak daarachter ligt een zegel, en daar kun je niet omheen: ook wie eroverheen springt, zet hem aan. Dan valt de doorgang
achter je dicht, zakt de doorgang aan het eind van de kamer tot een smalle spleet waar je niet onderdoor kunt, en komt het
plafond met een klap en daarna langzaam op je af. Na zo'n 23 seconden ben je geplet (bukken rekt het nog even). Door
de spleet zie je een tweede zegel liggen. Raak het met je speer: een vlakke worp (kort vasthouden) gaat onder de spleet
door, een boog raakt het plafond en valt terug. Hoe ver een vlakke worp komt hangt aan je scherm, dus zoek de plek in de
kamer waar hij precies op het zegel valt. Gooi je te kort, dan ligt je speer in de kamer en raap je hem op; gooi je te
ver, dan zet het spel hem naast je neer. Raak je het zegel, dan gaat alles weer omhoog en loop je door naar de fakkels.
In de sandbox staat het bij Terrein onder **Zakplafond**: **Neerzetten** zet de val in het klein voor je uit,

Er is een **masker**: een stuk level dat eruitziet als iets anders, zodat de speler niet doorheeft dat daar een doorgang of een zijpad ligt. Nu ziet het eruit als de ondergrondse rotswand, een stuk grijs gesteente over de savanne. Het houdt je niet tegen: je loopt er zo in, en dan valt het stil weg, en eenmaal gezien komt het niet meer terug. Een zegel of rune kan het ook onthullen, net zoals een tandwiel aan een zegel hangt: dan beeft het scherm en scheurt het weg met hetzelfde geluid als een ravijn dat openscheurt. Alles binnen het masker is verborgen: een vijand erbinnen staat bevroren tot het weg is en wordt dan pas actief, en een zegel of rune die zelf erbinnen ligt is onzichtbaar en niet te activeren tot het masker weg is, zodat je een hele keten kunt maken: onthul het masker, en pas dan ligt het zegel erachter klaar. Een zegel en een rune werken ook op een zwevende savannelaag. In de nieuwe Maker verf je het: onder **Verbergen** staat het gereedschap **Masker**, waarmee je cellen een groene tint geeft; je bewaart ze onder een naam (Verborgen1, Verborgen2, ...) en op een zegel of rune kies je bij **Onthult masker** welk masker hij wegneemt. Bij **Hoe het eruitziet** kies je waar het op lijkt (grotwand, rotswand, savanne of zwart), of **Onzichtbaar**: dan tekent het masker niets en zie je gewoon wat erachter ligt, maar een vijand, zegel, rune of kalebas erbinnen is weg tot het masker onthuld is. Loop erin of laat een zegel het onthullen, en de vijand staat er plots, of het voorwerp ligt er ineens. In de sandbox staat het ook los onder Terrein, **Masker**: met een bevroren slang erachter, met een grond-zegel dat het onthult, met een verborgen zegel erachter, en **Onzichtbaar met een slang**.

Voor wie levels bouwt zijn er twee nieuwe bouwstenen. Een rune op een rots kan een **opstelling** krijgen: een rots, een maat en een hoogte die gemeten zijn en waarvan bekend is van waar je hem raakt (vlak, zuilen, boog, op een kei, op een terras, in een gang en van ver). Een level zet hem met `opstelling` bij een rune, samen met wat hij doet: een ravijn openen of sluiten, de rotswand of een speerval, of rijzende grond. En rijzende grond kan andersom werken: een **zakkend platform** staat boven een ravijn en zakt weg zodra je erop staat, dus je moet er snel weer af. In de sandbox staan ze onder Terrein, Rijzende grond, **Zakt onder je**, en onder Rune, **Opstelling**.

De **Maker nieuwstijl** (een grid waarin je per cel schildert wat er is) kan nu **ongedaan maken** (Ctrl+Z, Ctrl+Y, of de twee pijltjes in de balk): elke streek, sleep of schuifbeweging is een stap, tot honderd terug. Met **Shift+slepen** vul je een rechthoek in plaats van een streek te trekken, met **Alt+klik** vul je een heel aaneengesloten vlak (de vulemmer), en een snelle streek laat geen cellen meer over. In Selecteren kiest Shift+slepen een **gebied**: kopieer het (Ctrl+C), knip het (Ctrl+X), spiegel het klembord (H) en plak het (Ctrl+V) als een stempel die de muis volgt, met de voorwerpen, maskers en zwarte cellen erin; de knoppen staan ook in het paneel rechts. Bij zo'n gebied staat ook **Test vanaf hier**: het level speelt dan met Amir op die plek, zodat je in een lang level niet elke keer vanaf het begin hoeft. Linksonder op de kaart staat een **minimap** van het hele grid met het stuk dat je ziet als kader; klik of sleep erop om ernaartoe te gaan, M verbergt hem. De knop **Controle** kijkt het grid na voor je op Test drukt: een start of eind zonder vloer, een vijand in de lucht of onder de grond zonder gang, een platform zonder doelhoogte, een tandwiel zonder platform, een ravijn of gang op de verkeerde rij, een gang zonder ingang, een dodelijke val naast een rand; klik op een melding en de kaart springt ernaartoe, en de lijst blijft bij zolang hij open staat. **Spel-JSON** zet het grid als echt level in het tekstvak, voor `tools/levelcheck.py` of de speelrobot. Een vijand heeft in het paneel rechts nu de knoppen die het spel kent: de snelheid van een slang, een of twee hyena's, of een bandiet over een kei vault (standaard wel), of de panter over keien en ravijnen komt (standaard niet), en of hij je alleen met vrij zicht opmerkt. Elke vijand heeft op het grid en in het palet zijn eigen **icoon** in het gekleurde rondje in plaats van een letter: een kronkelende slang (de fosforslang met een vonk), de schorpioen met scharen en angel, een pootafdruk voor de hyena, een kattenkop voor de panter, een hangende kooi voor de kooiman, een zak voor de meelman, het kromzwaard voor de bandiet en een schild voor de schildbandiet. Een variant of een knop die aanstaat zie je aan een klein badge rechtsonder (de dolk, het smash-blokje, het vogeltje, de 2 van twee hyena's, het pijltje van de panter die over keien komt); de elite heeft een gouden ring, de gehurkte bandiet een platgedrukt rondje, en de makkelijke schildbandiet alleen de omtrek van het schild. Een platform of overhang klik je overal op zijn balk aan, niet alleen op zijn eigen cel. Een richel heeft in het paneel een keuze **Kleur**: steen (de gewone richel), sneeuw of savanne, en op het grid zie je die kleur terug. Onder Objecten staat ook een **Rijzer (grond die stijgt)**: de rijzende grond uit Test 17 en Test 21, een blok steen dat op een zegel uit een ravijn omhoog komt. Zet hem op een ravijn op de grondlijn, kies met **Breedte** hoeveel cellen breed hij is (net als bij het platform) en met **Zet doelhoogte** tot waar hij komt (de grondlijn, of hoger als lift naar een terras); met de schuifjes stel je de snelheid, de wachttijd en hoe lang hij boven blijft in, en met **Zakt onder je weg** is het andersom een platform dat wegzakt zodra je erop staat. Op een zegel of rune kies je bij **Stuurt rijzer** welke hij omhoog stuurt. Met **Look** kies je zijn bovenrand (savanne, rots, sneeuw of zwart) en met **Zet kleurhoogte** de rij vanaf waar hij die kleur heeft: daaronder blijft hij zwart, zoals een blok dat uit de diepte komt. De Controle meldt een rijzer die niet in een ravijn staat of geen zegel heeft. **Kei (laag obstakel)** is in de Test een echte kei om op te springen, een trede op de onderste rij van een gang telt weer mee, en rijen boven invoegen schuift ook maskers, zwarte cellen en vormen mee. Een vijand in een gang loopt onder een muur, rots of terras op het oppervlak gewoon door en ziet je er ook doorheen (eerst bleef hij onder zo'n kolom staan), en een zegel dat je op de grondlijn boven een gang zet ligt in de Test ook echt op de savanne, niet op de gang-bodem. Sneltoetsen: F passend, T testen, + en - zoomen, pijltjes schuiven, Ctrl+S exporteren. De balk past op elk scherm, op een smal scherm in twee regels. **Kei (laag obstakel)** is in de Test een echte kei om op te springen, een trede op de onderste rij van een gang telt weer mee, en rijen boven invoegen schuift ook maskers, zwarte cellen en vormen mee. Een vijand in een gang loopt onder een muur, rots of terras op het oppervlak gewoon door en ziet je er ook doorheen (eerst bleef hij onder zo'n kolom staan), en een zegel dat je op de grondlijn boven een gang zet ligt in de Test ook echt op de savanne, niet op de gang-bodem. Sneltoetsen: F passend, T testen, + en - zoomen, pijltjes schuiven, Ctrl+S exporteren. De balk past op elk scherm, op een smal scherm in twee regels.

De **rots boven je** (het plafond met de tandenrand) zet een level neer met `plafond`: een rij punten, elk met een plek en een hoogte. Twee punten op dezelfde hoogte geven een recht plafond, twee op verschillende hoogte een schuin of dieper hangend stuk, en een punt op 4000 of hoger betekent "hier hangt geen rots", zodat de lucht ertussen doorkomt. Alles boven de lijn wordt vanzelf vol gesteente tot buiten beeld, dus het grote rotsvlak erboven hoef je niet apart te maken. Een plafond heeft minstens twee punten; wat de hoogte voor Amir betekent: boven 460 merkt hij niets, op 400 stoot hij zijn hoofd, onder 280 kan hij niet meer springen, onder 251 past hij er niet langs.
**Zakken** laat hem meteen dichtgaan, **Omhoog** haalt hem op en **Weg** ruimt hem op. Een level zet het met
`zakplafond: [ {r, l, rust, dicht, v, schok, duw} ]` en twee zegels, `{x, plafond: 'zak'}` en `{x, plafond: 'op'}`.

Bij het zakkende plafond komt het stof van boven: zolang het steen beweegt maakt er zich fijn stof van de onderkant
los dat licht en langzaam naar beneden dwarrelt, in de kleur van het steen, en als het stilvalt komt er een vlaag bij en
schokt het scherm. Alleen de poort die op de vloer slaat geeft daar een wolk. Dat gebeurt bij het zakken en ook als het
weer omhooggaat, en zolang er iets beweegt trilt het scherm licht.

In **Test 17: De rijzende grond** gaat het andersom: drie ravijnen die te breed zijn om over te springen, en elke keer
komt er steen uit de diepte omhoog. Op een blok dat nog stijgt kun je al landen: het neemt je mee naar boven. Bij het
eerste ravijn stap je op een zegel en komt er in het midden een blok omhoog, met aan weerszijden een gat dat je met een
sprong haalt. Bij het tweede staat aan jouw kant een rots met een houten schijf erop: raak die met je speer en het blok
komt omhoog. Je speer blijft in de schijf zitten, dus aan de overkant zit een skelet met een nieuwe. Bij het derde komen
twee blokken na elkaar omhoog die samen een brug vormen, maar zes seconden later zakt die weer: ren. Wie blijft staan,
zakt mee het ravijn in. Stap je opnieuw op het zegel, dan komt hij terug. Het steen komt met gerommel, stof langs de
rand van het ravijn en een trillend scherm, en boven een klap. In de sandbox staat het bij Terrein onder **Rijzende
grond**: **Neerzetten** zet een ravijn met een zegel voor je uit, **Zakt weer** hetzelfde met een blok dat na een tijd
terugzakt, **Omhoog** laat het meteen komen, **Met een slang erop** zet een lift op grondniveau met een slang die
meerijdt, en **Weg** ruimt het op. Niet alleen jij rijdt mee: een vijand die er met zijn midden op staat gaat ook mee
omhoog en weer omlaag. Dat is de enige manier waarop een vijand van niveau wisselt, want treden stapt hij niet op. Een
level zet het met
`rijzers: [ {id, r, l, tot, van, v, wacht, duur} ]` en een zegel `{x, rijs: 'id'}` (met `speer: true` gaat het zegel
alleen aan met een speer, niet door erop te stappen), of een rune op een rots als doel met `rijs: 'id'`.

In **Test 48: Rijzer in de put** komt de rijzende grond onder de grond uit: je laat je in een ravijn vallen en beneden
in de gang liggen twee putten in de vloer, elk met een blok erin. De eerste put is te breed om onder het dak over te
springen; stap op het zegel ervoor en er komt een blok steen omhoog dat de put precies vult. Het blok begint diep en
zwart, en pas boven een vaste hoogte krijgt het zijn kleur: je ziet het zwart uit de diepte komen en bovenaan steen
worden. Is de put dicht, dan komt de slang aan de overkant er gewoon overheen. De tweede put is een lift: het blok
komt tot boven de vloer, in de sneeuwkleur (de kleur is per blok, los van winter of sneeuw in het level), met de stam
in de put zwart. Stap links af op de trede, want na acht seconden zakt hij terug en wie blijft staan valt mee. Een
level zet dat met `look` (savanne, rots, sneeuw of zwart) en `kleurVanaf` (een hoogte: daaronder blijft het blok
zwart) bij een rijzer, en een rijzer in een put rekent vanaf de vloer van de gang.

Het Test levels-scherm toont de zes nieuwste tests. De knop **Oude tests** eronder klapt het archief met alle oudere open.
Omdat dat venster uit de volgorde van de lijst komt, duwt elk nieuw testlevel vanzelf het oudste uit de zes het archief in.

**Test 16: De zuil** gaat over precies springen. Midden in een ravijn is een smalle zuil grond blijven staan, en daar moet
je op landen. Een sprong die net te kort is, wordt hier niet gered: bij de overkant van een gewoon ravijn zet het spel je
weer op de rand als je er net onder zakt, maar de zijkant van een zuil is een wand, en daar glijd je langs naar beneden.
Eerst een brede zuil over twee gaten die je lopend haalt. Dan een zuil van een halve Amir breed achter een gat dat je
alleen met Shift haalt: zet vlak voor de rand af, want wie te vroeg springt komt tegen de wand en wie te laat springt
vliegt eroverheen. Tot slot twee van die zuilen achter elkaar, en de tweede staat zo dichtbij dat je daar juist niet
moet sprinten. Elke strook grond van hoogstens 300 px tussen twee ravijnen werkt zo. In de sandbox zet **Zuil** (bij
Terrein) er een neer, smal of breed.

**Test 18: De zuil in de sneeuw** is Test 16 op een besneeuwde bergvlakte (`winter: true`): de wanden van de ravijnen en
de zuilen zijn blauwgrijze steen met sneeuw op de rand. De sprongen zijn precies even lang.

**Test 19: De zuil onder de grond** begint met een ravijn waar je in valt, en beneden in de gang liggen de ravijnen in
de vloer: putten, in het donkere steen van de gang, die naar beneden in het zwart weglopen. Eerst een brede zuil tussen
twee putten, dan een smalle achter een put waar je alleen met Shift overheen komt. Het dak zit vlak boven je, maar de
sprong past eronder. Daarna ligt er een zegel in de vloer: stap erop en de vloer verderop scheurt open, met de barst,
het stof en de brokken in het grijs van de gang in plaats van de rode aarde. Die put spring je over met Shift. De
fakkels staan onder de grond.

**Test 20: Hoog en laag** heeft zuilen van verschillende hoogte. Eerst een trap van zuilen omhoog, steeds hoger dan de
grond, en dan een sprong naar beneden naar de overkant. Dan een dal: de zuilen liggen lager dan de grond, je springt
omlaag, nog verder omlaag, en via een lage zuil weer omhoog naar de grond; die laatste sprong gaat alleen met Shift.
En tot slot onder de grond een put met een hoge en een lage zuil erin, met het dak vlak boven je. Zo heeft een level
drie niveaus boven elkaar. Spring je te kort of te laag tegen een zuil, dan glijd je langs de wand naar beneden.
Een level zet zo'n zuil met `zuilen: [ {x, w, h} ]` in een ravijn of een put, met `h` hoe hoog hij boven de grond
staat (negatief is lager). In de sandbox zetten **Hoger** en **Lager** (bij Terrein, Zuil) er een neer.

**Test 21: Vijf niveaus** gaat niet alleen naar links maar ook vier keer een verdieping omhoog: eerst de grond, dan

**Test 22: De hoge savanne** doet hetzelfde, maar de niveaus zijn geen rotsplateaus. Een terras is normaal grijze rots, en dat klopt voor een klif, maar niet als een level twee of drie savannes boven elkaar heeft: je rijdt dan met een blok savanne omhoog en stapt boven op steen. Met het veld `grond: true` wordt een terras een hogere savannelaag: dezelfde grondtegel als de vlakte waar je vandaan komt, met daaronder de aarde in doorsnede die wegzakt in het donker, en dezelfde grillige randen als een terras. Aan het spel verandert er niets: je loopt erop, springt eraf, vijanden stoppen aan de rand (regel 7) en `levelcheck.py` rekent hem na als het terras dat hij is. Het level heeft de lage savanne, een laag op 300 en een op 600, en de enige weg omhoog is het steen dat op een zegel uit het ravijn komt: dat blok is dezelfde tegel als de laag waar het je heen brengt, dus de naad is onzichtbaar. Op elke laag staan gras, een struik en een vijand, zodat je ziet dat decor en dieren daar op de grond staan. In de sandbox staat het onder **Savannelaag** bij Terrein: op 300, op 600, of met een lift erheen, die er het ravijn, het blok en het zegel bij zet.
terrassen op 300, 600, 900 en 1200, elk met vijanden. Zo'n stap is te hoog om te springen. Aan het eind van elk niveau
ligt een zegel, en daarachter een ravijn: stap op het zegel en uit het ravijn komt een blok steen omhoog dat doorgaat
tot het niveau erboven. Spring erop terwijl het langskomt, dan neemt het je mee naar boven en stap je het volgende terras
op. Wacht je te lang, dan is het al te hoog en spring je ertegenaan; mis je het, dan zakt het na een paar tellen terug
en kun je opnieuw op het zegel stappen. Een level maakt zo'n lift met rijzende grond (`rijzers`) waarvan `tot` hoger
ligt dan de grond, tegen de wand van het terras erboven.

**Test 23: De klim** zet die twee manieren om omhoog te gaan naast elkaar in een savanneklim, en overal geldt: mis je een sprong, dan val je in het ravijn en ben je dood. Vanaf de grond spring je van zuil naar zuil (losse verhoginkjes boven een dodelijk ravijn) omhoog naar de eerste laag. Daar tilt een lift (het steen dat op een zegel omhoog komt) je naar de tweede laag. Op die laag spring je over een dodelijk gat naar het volgende plateau, en een laatste lift brengt je naar de top met de fakkels. Zo klim je door savannelagen met beide middelen door elkaar. `levelcheck.py` kent nu ook een plateau dat je met een sprong van een buurplateau over een gat bereikt.

**Test 24: De hoogvlakten** gaat over hoe een hoge laag eruit hoort te zien. Je klimt via twee liften door drie dikke grondlagen boven elkaar, en elke hogere laag ziet eruit als een volle savanne, niet van de basis te onderscheiden: dezelfde dikke aardrand, en het gebergte, de heuvels en de zon staan er gewoon achter. Dat komt door het veld `hoogUitzicht`: op zo'n level klemt de camera tegen de laag waar je op staat (dus je kijkt niet in een zwarte diepte eronder), de achtergrond blijft staan in plaats van weg te zakken als je klimt, en een grondlaag krijgt geen donkere onderkant. Zo voelt elke verdieping als een eigen hoogvlakte met uitzicht. Het veld staat per level aan, dus de bestaande levels blijven zoals ze waren.

**Test 27: De schacht** is een smalle kloof tussen twee schermbrede rotswanden waar je van onderaf uit klimt. Amir begint onderin tussen de wanden, en je springt om en om naar links en naar rechts naar de richels omhoog, als in een schoorsteen. De richels liggen met een echte afstand uit elkaar, dus je moet ook in de breedte hoppen: je springt van een richel, stuurt in de lucht naar de volgende en landt op de daalboog (op loopsnelheid, niet sprintend, anders schiet je de wand in). De wanden zijn hetzelfde gesteente als de grot en het plafond (de getande rotsvulling), met dezelfde tanden als aan een plafond langs de binnenranden, die de kloof in steken; de richels worden er gespiegeld overheen getekend en dekken de tanden erachter af, en steken uit elke wand en zitten achter de wandlaag, zodat ze er echt uit lijken te groeien. De bovenkant van de rots is savanne-grond: bovenaan stap je de wand op en loop je links over de savanne. Waar die savannekap aan de kloofkant op de rotswand uitkomt, rondt een geschilderd hoekstuk de rand af over de tanden heen, zodat de hoek niet recht afgesneden oogt maar als een kap boven op de wand. Daar trek je een speer uit een skelet, spring je over een kei (een schuilplek, want vijanden komen er niet voorbij) en versla je een paar vijanden (twee slangen en een schorpioen) voordat je bij de fakkels komt die het level uitspelen. De bodem van de schacht is savanne, dus een gemiste sprong laat je gewoon terugvallen om het opnieuw te proberen. Het is geen nieuw systeem maar een samenstelling van wat er al is (een grot-raster voor de wanden, richels voor de treden), zodat de bestaande episodes er niets van merken. De definitie staat in de HTML als `TEST_27`.

In de episode **Baboon tests** staan drie proefstukken voor de baviaan, met de tribekeuze voor het begin. In
**Baboon 2: De speerbeet** (dezelfde vlakte als Baboon 1) hangt hij niet aan de wand maar staat hij grommend op de grond,
een stuk voor je uit, en kijkt je aan. Pak je speer en loop naar hem toe. Steek je naar hem, of kom je met je speer in de
hand te dichtbij, dan pakt hij je speer: je staat even vast en steekt vanzelf, hij bijt op de punt, rukt de speer uit je
handen, schudt hem grommend kapot, en smijt de punt recht naar je toe: het blad komt met een aanzwellende zoef op je af tot het groot en donker in de lens slaat. Loop je gewoon door zonder te steken, dan grijpt hij pas als je wat dichterbij bent. Buk je en zwaai je laag, dan slaat hij met zijn poot op je speer: die breekt onder zijn poot, de punt vliegt op je af, en je laat de stomp vallen. In de sandbox laat **Pootslag lang** de langzame versie met de arm hoog zien, die nog niet in het spel zit. De
schacht blijft in het zand liggen. Daarna loop je zonder speer verder, over twee ravijnen naar de fakkels. In de sandbox
zet **Speerbeet** (bij Vijanden, onder Baviaan) hem zo op de grond, een stuk voor je, en geeft je je speer terug.

In het pauzemenu (II of Escape) staat **Level overslaan**: die brengt je meteen naar het volgende level van dezelfde reeks. Onder **Instellingen** staan daar ook het tempo van het spel, het looptempo van Amir, het formaat van het beeld en de muziek. Tijdens een level is het speelveld verder leeg: de testbalk met schuifjes staat alleen in de sandbox (met B haal je hem er tijdens het spelen alsnog bij). Het menu van de sandbox klap je weg met **Verberg** rechtsboven in het paneel, en met **Toon** haal je het terug; het spel onthoudt hoe je het liet. Op een telefoon staat het onder de pauzeknop, zonder de uitlegregel, en weggeklapt ligt de joystick vrij.

## Tribes

Een run van De Valse Koning of Baboon tests (elke episode) begint met het kiezen van een tribe: druk je in het menu op Spelen (of Nightmare), dan komt eerst het keuzescherm. De Test levels hebben geen tribekeuze; daar heb je alle abilities, zodat je alles kunt proberen. Kiezen is verplicht en ligt vast voor de hele run. Te kiezen zijn **Mkuki, Tribe of the Spear** en **Bhubesi, Tribe of the Lion**; **Impungushe, Tribe of the Jackal** staat er al, grijs en op slot (Coming soon). Tik of klik je op een tribe, dan zie je eerst zijn talent tree; met **Back to tribes** ga je terug en bekijk je een andere. De keuze ligt pas vast als je op **Join** drukt. Je krijgt meteen bij het kiezen een talentpunt, dus je keuze telt vanaf level 1, en na elk uitgespeeld level komt er een punt bij. De boom van Impungushe is al te bekijken, met drie lege plekken, maar er valt nog niets te kiezen. Met de pijltjes en Enter kies je met het toetsenbord, op een telefoon tik je.

Elke tribe heeft een **talent tree**: een verticale boom zoals in World of Warcraft, die van onder naar boven groeit, met Tier I onderaan (zijtakken komen later). Hij heeft het thema van je tribe: bij Bhubesi zit elk talent in een krans van leeuwenmanen, met klauwhalen ertussen die opgloeien onder wat je geleerd hebt; bij Mkuki is het een krans van speerpunten, met een speerschacht die rood omwonden raakt. Naast de boom staat wat het talent doet, met een vergelijking zonder en met (bijvoorbeeld 10 kills tot een volle meter, met Blood Rush 7). Je leert niets vanzelf: je krijgt een **talentpunt** en geeft dat zelf uit door op het volgende talent te klikken of te tikken (met het toetsenbord pijl op en neer en Enter). Pas als je punt op is kun je verder. Bij elke tribe krijg je het eerste punt na het eerste uitgespeelde level, het tweede na het tweede en het derde na het derde. In het pauzemenu staat de boom onder **Talents**, om te kijken wat je hebt. Tot dan doet een ability die je nog niet hebt niets. Tijdens het spelen staan je talents niet in beeld, alleen wat je ervan moet weten: de lage zwaai en de woedemeter. Ga je dood, dan begin je het level opnieuw met je tribe en de abilities die je al had. Pas als je in het menu opnieuw op Spelen drukt, begint een nieuwe run en kies je opnieuw.

| ability | wat hij doet |
|---|---|
| **Quick Hand** | na een speerworp sta je korter vast: het herstel na het loslaten gaat 1,6 keer zo snel (0,47 in plaats van 0,75 seconde) |
| **Thorn Breaker** | een doornbos gaat in een klap om in plaats van drie |
| **Twin Sweep** | de lage zwaai heeft twee ladingen in plaats van een: de tweede is een reserve terwijl de eerste herlaadt |

De lage zwaai zelf (bukken en aanvallen) heeft iedereen, bij elke tribe. Hij raakt slangen, fosforslangen, de schorpioen, hyena's en de panter als hij na een sprong plat ligt. Na een zwaai herlaadt hij 1,4 seconde voor je hem opnieuw kunt doen; dat zie je rechtsboven, links van de kalebas, aan het icoon met de speer in de wervel, dat donker wordt en weer vrijdraait. Met Twin Sweep staan er twee stipjes naast: een per lading. De ladingen laden een voor een bij, en een misser kost er ook een.

### Bhubesi en de woede

| ability | wat hij doet |
|---|---|
| **Long Breath** | geeft de woedemeter, en de woede duurt 8 seconden in plaats van 5 |
| **Blood Rush** | de meter vult 1,6 keer zo snel, per kill en per treffer op een eindbaas. Heb je Long Breath nog niet, dan geeft Blood Rush zelf de meter, met 5 seconden |
| **Fourth Life** | je begint elk level met vier levens in plaats van drie (het vierde hartje heeft een gouden randje). Het gaat eraf zoals de andere, en een kalebas vult het ook weer aan |

De woedemeter staat onder de kalebas, met het leeuwenlogo en een balk. Hij is er alleen met Long Breath of Blood Rush. Elke gedode vijand vult een tiende, en elke rake klap op een eindbaas die hem nog niet doodt 0,08. Hij blijft staan tussen levels en na game over, en gaat pas terug naar nul bij een nieuwe run uit het menu. Is hij vol, dan pulseert hij, licht de leeuw op en klinkt er een trommelslag, maar hij gaat niet vanzelf af: druk op **G** (of klik op de meter), op de telefoon op de ronde knop met de leeuw links van ✦. Dan neemt Amir een tijd geen schade, van beten, klappen, vallen en de fosforslang, en loopt de meter leeg als aflopende tijd. Hij wordt er niet sterker van. Om hem heen hangt een warme gloed met opstijgende vonkjes, die aan het eind flakkert. Een val in een ravijn blijft het einde. Is de meter niet vol, ben je al in de woede of ben je dood, dan doet G niets.

### Impungushe, nog op slot

Impungushe staat op het keuzescherm nog op slot, maar zijn drie talents zijn er al om te proberen: in de sandbox en in **Test 14**. Zijn boom is te bekijken, met de talents erin, maar dicht.

| ability | wat hij doet |
|---|---|
| **Jackal Fang** | Amir heeft een mes. **E** wisselt rond: met een speer van speer naar mes naar niets en weer terug, zonder speer tussen niets en het mes. Het mes is eerst gereedschap: het snijdt een kalebas los die aan een koordje aan een speer in de grond hangt (hij valt, en je raapt hem op zoals een gewone kalebas), en het kapt doornbossen, trager dan de speer (twee steken per klap). Het doodt niets: een steek duwt een vijand terug en breekt zijn aanval af, maar hij komt meteen weer, en dezelfde vijand kun je daarna even niet opnieuw afweren. De panter weer je niet af. Geen lage zwaai en geen worp met het mes |
| **Bared Teeth** | de dreighouding. Met het mes in je hand en een vijand voor je in de buurt kijkt Amir hem vanzelf aan en loopt hij langzaam; hij kan achteruit lopen zonder zich om te draaien, en sprinten kan niet (Shift breekt de houding). De vijand houdt afstand: stap je naar hem toe, dan schiet hij een stuk terug, loop je achteruit, dan komt hij langzaam mee. Zijn moed groeit, het snelst als je terugloopt, en een steek met het mes maakt hem weer banger. Is hij moedig genoeg, of staat hij met zijn rug tegen een kei, een ravijn of een wand (kat in het nauw), dan valt hij aan, en laat de houding hem even met rust. Wie achter je staat, doet gewoon zijn eigen ding, dus tegen een groep hou je het niet. De zwarte slang, de fosforslangen en de panter trekken zich er niets van aan. Erlangs kom je door over hem heen te springen |
| **Feign Death** | een keer per level wordt de klap die je laatste leven zou kosten een schijndood: Amir valt om, ligt een paar tellen stil met een leven over, en kan zolang en even daarna niet geraakt worden. Rechtsboven staat een tegeltje met een gesloten oog, dat grijs wordt als hij op is. Een val in een ravijn blijft het einde |

In de boom staat naast Jackal Fang een **T-splitsing** met de mogelijke varianten waarin het talent later kan opsplitsen: **Thorn Knife** (alleen doornbossen, maar snel) en **Gourd Knife** (alleen kalebassen, en je vindt er meer). Kiezen kan nog niet; het laat zien waar het heen kan. De varianten staan per talent in `TRIBE_CONFIG` (`varianten`).

Hoe het mes precies reageert stel je in het spel zelf bij: druk op **Escape**, kies **Instellingen** en dan **Mes: reacties**. Daar staan de duw, hoe lang een vijand stilstaat van de klap, de afkoeltijd en de rust tussen twee steken, en met Bared Teeth ook je tempo in de houding, de afstand die een vijand houdt, hoe snel hij terugschiet en meekomt, en hoe snel zijn moed groeit als je stilstaat of terugloopt. Het geldt meteen als je op **Verder** drukt, ook voor een vijand die al voor je staat. Je browser onthoudt het, en **Mes: standaard** zet alles terug. De knop staat er alleen als je het mes hebt, dus in Test 14 en in de sandbox.

Voor nu is het mes een tijdelijke tekening: er zijn nog geen frames van Amir met een mes. Het mes is de punt van zijn eigen speer met het leren riempje als heft (`tools/mes.py`), en bij een steek schiet zijn hele lijf even naar voren. Liggen is zijn gewone frame, gekanteld.

Alle getallen en teksten staan in `TRIBE_CONFIG`, bovenin de HTML. In de sandbox staan de abilities los aan en uit onder **Tribe Mkuki**, **Tribe Bhubesi** en **Tribe Impungushe**, met **Woede vol** om de meter meteen te vullen, **Mes in de hand** en **Speel dood**, en onder **Lage zwaai** hoe lang een lading herlaadt.

## Op je telefoon zetten

Het spel is een installeerbare webapp. Open de Pages-link in Safari, deel, "Zet op beginscherm". Daarna staat Amir als icoon tussen je apps en start hij zonder browserbalken, liggend.

Open hem vanaf het beginscherm en druk onder **Instellingen** op **Download voor offline**. Dat haalt alle sprites en geluiden in een keer binnen (ruim 2200 bestanden, ongeveer 230 MB; het precieze aantal staat in `offline-assets.json`). Vanaf dat moment laadt het spel meteen en speelt het ook zonder internet.

Lukt een deel niet, dan zegt de knop **Probeer opnieuw** en staat eronder hoeveel bestanden er nog ontbreken, en of dat komt doordat de opslag op je toestel vol is of doordat de verbinding wegviel. Een volgende poging haalt alleen die ontbrekende bestanden op.

Doe die download vanuit het beginscherm-icoon, niet vanuit Safari: iOS geeft een geinstalleerde webapp een eigen opslag, dus wat je in Safari downloadt telt daar niet mee.

Ook zonder op die knop te drukken wordt alles wat je tijdens het spelen tegenkomt bewaard, dus een tweede potje laadt sowieso sneller.

Het menu zelf laadt licht: alleen wat elk level nodig heeft (Amir, de bodem, het uitzicht). De vijanden, de dorpelingen en het dorp komen pas binnen bij het level dat ze gebruikt, al terwijl je het kaartje bekijkt. Zo start het spel met ongeveer 90 MB in plaats van 150, en dat merk je vooral op een telefoon zonder de offline-download.

### De hoogte van het beeld

Het spel vult de hele hoogte van je scherm. In Safari staat bovenin de adresbalk, en die schuift weg zodra je gaat spelen. Het spel groeit daarin mee, zodat er onderin geen bruine strook overblijft; eerder rekende het zijn hoogte een keer uit terwijl de adresbalk er nog stond en bleef er zo'n 46 punten leeg. Onderaan blijft alleen het smalle stukje dat iOS vrijhoudt voor het veegstreepje. Zet je het spel op je beginscherm, dan is er helemaal geen adresbalk en speel je van rand tot rand op dat streepje na.

Een level begint pas als alle plaatjes binnen zijn. Is er nog iets onderweg (op een trage verbinding, of bij een level dat eigen plaatjes heeft, zoals de baviaan), dan staat het spel stil en zie je **Laden** met een balk tot alles er is. Begin je een nieuw level, dan staat het laadscherm er altijd minstens 5 seconden, met de naam van het level eronder: is alles eerder binnen, dan loopt de balk rustig door tot het einde. Begin je opnieuw in hetzelfde level, dan zie je er niets van als het vlot loopt. Na 40 seconden gaat het spel toch verder, met wat er dan is; alleen het klaarmaken van plaatjes die dan nog net binnenkomen wacht het nog af (tot hoogstens 80 seconden), zodat die niet midden in het spel een hapering geven.

### Geluid op een telefoon

Een telefoon laat geluid pas toe nadat je het scherm hebt aangeraakt, en dan nog per geluid apart. Het spel geeft daarom bij je eerste tik elk geluid stilletjes even zijn beurt, zodat het later gewoon klinkt als het aan de beurt is: de brul van de baviaan, het instortende skelet, de aardbeving als een ravijn openscheurt, de rotswand die opengaat, de storm, de hyena's, de panter, het water, en Amir die het uitschreeuwt.

Leg je je telefoon weg, komt er een telefoontje tussendoor of ga je naar een andere app, dan zet iOS het geluid stil. Daarna doet je eerstvolgende aanraking het weer aan, en kom je terug op het scherm dan probeert het spel het uit zichzelf. Eerder bleven juist de harde geluiden (de brul, het skelet, de aardbeving, de storm) daarna de rest van het potje weg, terwijl de rest gewoon doorspeelde.

### Beeld: scherp of licht

Van een deel van de sprites staan twee versies op schijf: het origineel, en een halve versie met dezelfde mappen en namen in `klein/`. Het spel kiest bij het starten: een telefoon krijgt de kleine set, een laptop en een tablet de grote. Onder **Instellingen** staat bij **Beeld** een schakelaar (Automatisch, Scherp, Licht) om dat te overrulen; wisselen herlaadt de pagina, want de sprites zijn dan al geladen.

Waarom: de grote frames zijn op een telefoon vele malen groter dan ze getekend worden. Safari houdt ze niet allemaal uitgepakt in het geheugen en decodeert ze midden in het spel opnieuw, en dat zijn de hikjes. De tekencode rekt elk plaatje naar vaste maten, dus beide sets werken met dezelfde code. Ontbreekt een klein frame, dan valt het spel terug op het grote.

Welke plaatjes meedoen staat in `DOELEN` in `tools/gen-klein.py`, en dat is met opzet een korte lijst. Een plaatje halveren mag alleen als het op een telefoon nog steeds groter is dan het stukje scherm waar het op terechtkomt. Dat is per familie gemeten en de factor staat erbij. Meedoen: Amir, de hyena's, de panters, de schorpioen, de bandiet, de dorpeling, het droge gras, de kei, de verre hut, de botten en de grotset (7,3x: het plafond, de hoekstukken en de wandtegels zijn de grootste bronnen van het spel en worden tot een tiende getekend). Er juist buiten vallen de boom (1,0x), de struik (1,2x), het doornbos (0,9x), de dorpshutten (1,8x), de klif (1,9x) en de dorpelinge (1,9x): die staan al vrijwel op maat, dus halveren zou je meteen zien.

De download volgt de gekozen set: een telefoon haalt de kleine versies binnen en slaat de grote over, een laptop andersom. Dat scheelt ongeveer 64 MB.

Sprites toegevoegd of vervangen? Draai dan eerst de kleine set opnieuw en daarna de offline-lijst:

```
python3 tools/gen-klein.py
python3 tools/gen-offline-manifest.py
```

Het eerste script print aan het eind de lijst die in de HTML onder `KLEIN_FAM` hoort te staan. Loopt die niet gelijk, dan laadt een familie stilletjes de grote versie.

Op een aanraakscherm tekent het spel op anderhalve canvaspixel per schermpixel in plaats van twee: op zo'n klein scherm zie je dat niet, en het scheelt bijna de helft van het werk per frame. Haalt het toestel de frames dan nog niet, dan zakt het spel vanzelf nog een stap (naar 1) en blijft daar; in de console staat dan een regel met "resolutie omlaag".

### Waarom het soms haperde

Er zat een echte hapering in, en die zat niet in de resolutie maar in de tekencode. Bijna elke laag wordt op wereldmaat getekend en daarna door een clip op zijn plek gehouden: de donkere grondvulling was drie schermen breed, een gang werd over zijn hele lengte getegeld, en de wand van een schacht liep door tot ver onder het beeld. Voor een enkele vulling kost dat weinig, want het canvas knipt het overschot zelf al weg. Voor een tegellus kost het wel: die zet duizenden pixels per stap, en liep dus honderden stappen voor niets. En de wand van een schacht zette elk beeld vier verse doeken klaar op de maat van de hele wand.

In de schachtlevels liep dat helemaal vast. Gemeten in Chromium, met Amir die het level afloopt:

| level | was | nu |
| --- | --- | --- |
| Klim 9: De grote schacht | 145 ms per beeld | 9 ms |
| Test 27: De schacht | 137 ms per beeld | 9 ms |
| Diepte 1: De afdaling | 30 ms | 29 ms, met een kortere staart |
| Poort 1: Het rode zand | 12 ms | 12 ms |

Dus: wie De Klim, Valse Koning 6 tot 8, Diepte 6 en 7 of de schacht-tests speelde (De Klim en De Diepte zitten er inmiddels niet meer in), zat in het zwaarste geval van het spel. Een vlak savannelevel merkte er weinig van, en dat klopt met waar het haperen opviel.

Wat eraan gedaan is, allemaal zonder dat het beeld verandert:

- `zichtVak()` geeft het stuk dat echt in beeld komt, met de zoom en de schok van het schudden erin verrekend. De tegellussen van een gang, de grondtegel, de achtergrondpanelen en de wand van een schacht lopen daar nu tegenaan in plaats van tot aan het eind van de wereld.
- `vulVak()` is een vulling die daar niet buiten reikt, voor de paar lagen die het hele beeld dekken.
- `werkDoek()` houdt de doeken vast in plaats van er elk beeld nieuwe te maken. Een nieuw canvas per beeld kost een nieuwe textuur en straks opruimwerk, en dat zijn precies de hikjes.
- `grotRaster()` plakte het hele raster elke aanroep tot een string aan elkaar om te kijken of zijn sleutel nog klopte. Op een schacht is dat kilobytes, en het raster wordt tientallen keren per beeld gevraagd: in Klim 9 was dat een negende van alle rekentijd. Nu vergelijkt hij de lijst zelf.
- De vaultframes van de bandiet (68 stuks) kwamen in een golflevel pas binnen toen de eerste rover opkwam, dus midden in het spel. Nu laden ze mee achter het laadscherm.

Dat het beeld niet verandert is nagemeten, niet aangenomen: `tools/beeldgelijk.js` tekent hetzelfde bevroren beeld twee keer, een keer langs de oude weg en een keer langs de nieuwe, en vergelijkt pixel voor pixel.

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
| springen | pijl omhoog | ▲, of joystick omhoog |
| bukken | pijl omlaag | joystick omlaag |
| kruipen | gebukt een pijltje links of rechts | joystick omlaag en opzij |
| lage zwaai | bukken en spatie | joystick omlaag en ✦ |
| stoten | spatie (korte tik) | ✦ (korte tik) |
| stoten vanuit een sprint | Shift en een pijltje, dan spatie: hij glijdt remmend door | joystick ver uit, dan ✦ |
| **speer recht vooruit** | **spatie vasthouden, loslaten** | **✦ vasthouden, loslaten** |
| **speer in een boog** | **langer vasthouden, dan loslaten** | **langer vasthouden, dan loslaten** |
| worp afbreken | tijdens het spannen springen, bukken of de andere kant op | duim van ✦ af slepen en daar loslaten, of springen, bukken of de andere kant op |
| speer oppakken | E, waar je ook langs de schacht staat | E (verschijnt als je er vlakbij staat) |
| door een open deur of grot | E, als je ervoor staat | E (verschijnt als je ervoor staat) |
| drinken | Q | het kalebasje |
| woede (Bhubesi, meter vol) | G | de knop met de leeuw |

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

Een geworpen speer raakt maar een tegenstander. Staan er twee op dezelfde plek,
dan houdt de eerste hem op en loopt de tweede ongedeerd door. Dat geldt ook voor
een gewone stoot; alleen de lage zwaai raakt alles wat binnen zijn bereik staat.

Je hoeft niet te gooien als je eenmaal spant. Spring, buk of loop de andere kant op
en de worp gaat niet door: je houdt je speer en Amir doet meteen wat je vraagt. Er
wordt ook nooit vanzelf gegooid, hoe lang je ook vasthoudt. Wacht je met een
gespannen speer, dan staat hij niet stil: hij ademt, na ruim een seconde gaat hij
licht trillen van de spanning, steeds iets meer, en is hij helemaal uitgetrokken,
dan glimt de punt af en toe. In de sandbox zet de knop **Spannen** onder
"Speerworp" dit uit, om het te vergelijken met hoe het was.

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
wijst elk frame de kant van zijn snelheid op. In de vlucht rolt hij om zijn eigen as, zodat je het
blad zo nu en dan plat en dan weer op zijn kant ziet; zodra hij ergens in steekt ligt hij stil. Raakt hij een dier, dan doet hij
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

Er is een derde spuwer: de **knockslang** (`k: 'knock'`), jade met violette zadels. Hij doet
precies hetzelfde als de zwarte slang (blijft op afstand, draait om bij een ravijn, volgt je ook
buiten beeld), maar zijn gif is jade/violet en doet geen schade: een druppel duwt je 6 cellen (zo'n
900 eenheden) naar achter. Die terugstoot duwt gewoon door, dus bij een ravijn of een platformrand
kan hij je er echt in of af duwen, net als elke andere terugstoot. Zijn frames komen ook uit
`tools/slang_kleur.py` (`enemies/slang1_knock/`, met een eigen `venom.png` in jade/violet). In de
sandbox staat hij onder **Knockslang**, en je zet hem neer in de Maker net als de
andere slangen. **Test 43: De knockslang** is het proefstuk: een op open vlakte om de worp te
leren, en een voorbij een ravijn zodat de terugstoot je naar de rand kan duwen.

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
op 55 procent van de band (`PROP_ACHTER`). Dorpsplaten niet: die hebben hun eigen stukje
grond ingetekend, en dat moet over de zandband vallen, waar het met een zachte voet
(`VILLAGE_VOET`) in het zand van het level overloopt. Met de stap erbij eindigde die grond
precies op de bovenrand van de band, en lag de overgang als een rechte lijn in het zand. Een
hut op `depth: 0` staat dus op de looplijn; alleen `depth` zet hem naar achteren
(`VILLAGE_DIEP`), zodat een hut op `depth: 0.85` ook echt verder weg staat in plaats van
alleen kleiner te zijn. De voorgrondhut blijft waar hij staat, want die hoort juist vóór Amir
langs.

Zonder die stap stonden gras, struiken, keien, putten en hutten op exact dezelfde lijn als
Amir, en dan sta je letterlijk in de planten: een pol gras komt dan tussen je voeten omhoog,
en een gevallen lichaam krijgt een struik door zijn borst. In de ontwerptekening van het
dorp staat het decor ongeveer 9 procent van Amirs lengte hoger dan zijn voeten, en op 0,55
van de band kom je daar precies uit. Verder terug kan niet: dieper is de tegel niet.

Klimrotsen, terrassen en richels blijven waar ze staan, want daar loop je op. Alleen decor
zonder botsing schuift mee.

## De bandiet

De tweede menselijke tegenstander, en een snellere: een gemaskerde rover met een kromzwaard.
De frames staan in `enemies/bandiet/`, met `sprites.json`, `sprites_los.json`, `dolk/dolk.json`
en de `LEESMIJ`-bestanden als bron. Hij heeft vijf sets: **rennen** (een lus), de **slag**
(eenmalig), het **rondkijken** over de schouder (een taunt als hij op zijn beurt wacht), de
**worp** (eenmalig) en de **dood** (eenmalig, 63 frames: hij zakt in elkaar en blijft liggen).
Geen idle en geen pijnpose: hij rent altijd, en een treffer die hem niet velt is een flits met
een duw die zijn slag afbreekt.

Hij wacht nergens op: hij rent meteen op je af, remt, en haalt
uit met een neerwaartse haal. Terwijl hij die haal maakt schiet hij naar voren en glijdt hij
remmend door (de "doorschuif" loopt dus mee met de slag zelf, niet erna), met een duidelijke
opstuivende zandwolk bij zijn voeten, zoals bij een landing. Dat doorschieten is je opening:
stap of spring weg, laat hem voorbijglijden, en steek hem in de rug terwijl hij nahijgt en zich
omdraait. Daarna komt hij
weer. Zijn kromzwaard reikt korter dan je speer, dus je speer komt
er makkelijk langs; hij houdt twee treffers, en de eerste breekt zijn haal af. Raak je hem,
dan stuitert hij terug en herstelt hij even voor hij weer inzet: dat venster is net lang genoeg
om weg te stappen, maar niet om meteen nog een keer te steken. Blijf je staan om door te rammen,
dan staat hij op je als zijn tegenklap valt, dus het ritme is raken, even uit zijn bereik, en dan
weer raken. Hij rent net
iets langzamer dan jij sprint, maar in een groep komt hij van twee kanten, dus wegrennen
helpt maar half. Staan er meer bij elkaar, dan vecht wie het dichtst bij je staat en kijken de
anderen rond (de look-set) tot het hun beurt is. Een kei en een ravijn houden hem tegen zoals
elke vijand (regel 7): een kei is ook voor hem een schuilplek, en voor een ravijn stopt zijn
uitval. Zodra hij op je af gaat rennen, slaakt hij een strijdkreet ("Die!" of "False king!"),
en als je hem velt klinkt zijn doodskreet. Onder het rennen hoor je zijn voetstappen op de grond,
zachter naarmate hij verder weg is, zodat je hem hoort aankomen.

**Zijn lijk blijft liggen.** Vel je een bandiet, dan zakt hij in elkaar en
blijft het lijk liggen waar het valt, de rest van het level. Alleen de lage zwaai veegt het weg: een
lijk ligt te laag voor je stoot of je speer, dus je ruimt het op met een zwaai over de grond, en dan
zakt het weg. Zo blijft een slagveld een slagveld.

**De dolk.** Met de optie `dolk` wil een bandiet altijd eerst zijn dolk werpen voor hij met het
zwaard aanvalt: zodra hij je in beeld binnen werpbereik ziet, blijft hij staan, slingert zijn dolk
op kophoogte naar je toe (de worp-set, met het release-frame waarop hij loslaat), en rent dan pas in
om uit te halen. Dat werpen gaat voor: ook van dichtbij, en ook als je hem raakte voor de dolk weg
was, wil hij hem er eerst uit gooien, en pas daarna komt het zwaard. Hij gooit pas als hij echt in beeld staat, ook op
een telefoon (waar je maar een smalle strook opzij ziet), zodat de dolk nooit van buiten beeld
komt aanvliegen. Hij gooit maar één keer. De dolk tolt niet: hij vliegt met de punt vooruit
in een bijna vlakke baan, en raakt hij je, dan kost dat een leven; mist hij, dan steekt
hij in de grond (`dolk_recht`) en vervaagt. Ontwijken doe je door te bukken: hij vliegt op
kophoogte, dus staand raakt hij je en gebukt scheert hij over je heen. Je moet er net op kunnen
reageren. Om hem ook op een telefoon goed te kunnen volgen is hij wat groter getekend en heeft hij
een kort spoor; de botsing blijft op de echte maat van de dolk. De dolkplaatjes zijn afgestemd op
de hoofdset, dus ze worden op de maat van de bandiet getekend.

**De hinderlaag.** Met de optie `hurk` zit een bandiet gehurkt met de rug naar je op een vaste
plek. Kom je dichtbij, dan hoort hij je, kijkt over zijn schouder, springt vlot op en keert zich naar
je toe, en werpt zijn dolk op kophoogte: buk ervoor. Je kunt hem nog neersteken terwijl hij overeind
komt, maar hij komt sneller op dan voorheen, dus je moet er vlotter bij zijn. En raak je hem voor de
dolk weg is, dan werpt hij hem er alsnog eerst uit voor hij met het zwaard komt. Daarna wacht hij een
kwart seconde en rent op je af als een gewone bandiet. In een level zet je er een
neer met `{x, k: 'bandiet', hurk: true}`; in de sandbox met de knop **Hinderlaag**. Test 31
(De hinderlaag) is het proefstuk.

**Over een kei heen vaulten.** Een kei houdt een bandiet gewoon tegen (regel 7), en zo is hij voor
jou een schuilplek. Maar met de optie `vault` is dat anders: zolang er een kei tussen jullie in ligt
en jij aan de overkant staat, erop zit, of hem al voorbij bent, zet hij zich bij de kei op de grond af
en vliegt hij er in een eenhandige radslag in een boog overheen (met stof bij het afzetten en bij het
neerkomen), landt vlak voor je en gaat meteen weer in de aanval. Er is geen afkoeling: blijf je achter
of op de kei, dan springt hij er zo vaak als nodig overheen, en een tweede bandiet staat niet te
wachten. Een kei is voor hem dus nergens een veilige plek: je moet hem van je af houden of neersteken,
niet erachter wegkruipen. In de lucht raak je hem niet. Je zet het aan met
`{x, k: 'bandiet', vault: true}` (ook samen met `hurk`), en in de sandbox met de knop **Vault**. In
Test 31 staat elke hinderlaag tussen twee keien, dus hij vault of je er nu voor schuilt, erop staat of
hem al voorbij bent.

In de sandbox staat hij onder **Bandiet**: neerzetten, **Hinderlaag** voor de gehurkte variant,
**AI uit** om de stekker eruit te
trekken, **Dolk aan** om hem eerst te laten gooien, **Vault aan** zodat hij over een kei heen springt
als jij aan de overkant staat, en onder **Zijn animaties** de set die hij
dan speelt (rennen, dolk gooien, slag, rondkijken, dood, de hurk-sets: hurken, gehurkt,
schouder, opspringen, en de vault: de radslag over een obstakel). Met **Golf aan** komen er, net als in
het testlevel, telkens meer bij, van twee kanten en steeds sneller. In een leveldefinitie zet je
een losse neer met `{x: -1900, k: 'bandiet'}` (met `dolk: true` gooit hij eerst), en een
oplopende golf met het veld `bandietGolf: {van, tot, ramp, max, dolk}`: om de zoveel seconden een
bandiet net buiten beeld, om en om links en rechts, met een interval dat van `van` naar `tot`
seconden krimpt over `ramp` seconden, en hoogstens `max` tegelijk in leven; met `dolk: true`
gooien ze allemaal eerst. Een teller in beeld houdt bij hoeveel je er verslagen hebt en hoe lang
je het volhoudt.

## Wat een vijand ziet

In een nieuw level merkt een vijand je pas op als hij je echt kan zien. Kijkt hij jouw kant op, dan
ziet hij je zolang er geen grond of rots tussen jullie zit: loop je recht boven hem over een terras of
een zwevende laag, of onder hem door een gang, dan blijft hij rustig staan. Een kei of een richel
verbergt je niet. Sta je achter hem, dan merkt hij je alleen op als je op zijn eigen hoogte staat. Is hij
je drie seconden kwijt, dan vergeet hij je en gaat hij terug naar zijn plek. De oudere levels werken
nog zoals vroeger. In de sandbox staat het onder Vijanden, bij **Zicht**, en **Toon zicht** laat zien
waar hij kijkt.

## De health-balk

In een level met de health-balk heeft elke vijand drie levens, met een balkje boven zijn hoofd dat bij
elke klap een derde korter wordt en van groen naar rood kleurt. Amir heeft er dan ook een: hetzelfde
balkje boven zijn hoofd, gevuld met de levens die hij nog heeft, naast de hartjes in de hoek. Alle
nieuwe levels hebben hem, en ook de proefstukken van de schildbandiet (Test 45 en Test 46).

In de sandbox staat onder Schildbandiet naast Neerzetten ook **Neerzetten nieuwe stijl**: dezelfde
schildbandiet, maar getekend uit losse lagen, met het schild als een eigen plaatje op het lijf in plaats
van in elk frame meegebakken. Hij ziet er hetzelfde uit en doet hetzelfde; het is de proef voor hoe de
animaties voortaan gemaakt worden.

De schildbandiet is de uitzondering: zijn schild vangt de klappen op, hij zelf niet. Boven zijn
groene balk staat daarom een houten schildbalk met drie vakjes. Elke klap op het schild kost een
vakje, zijn eigen balk blijft vol, en je ziet het aan het schild zelf: na de eerste klap is er een hap
uit, na de tweede twee. Is het schild gebroken, dan verdwijnt die houten balk, en de
volgende klap is in een keer van vol naar dood. De panter en de baviaan houden hun eigen balk
bovenin beeld.

Bij die laatste klap valt zijn speer uit zijn hand, en die valt echt: hij stuit even op de grond en
blijft voor zijn voeten liggen, ligt scheef als hij op een kei of de rand van een terras terechtkomt,
en kantelt een ravijn in als hij op de rand sterft. Daarna valt hij achterover en blijft hij met zijn
rug op de grond liggen.

## De kooiman

De derde menselijke tegenstander is een heel ander soort vijand: een gebukte man die een zware
kooi aan een handvat achter zich aan sleept. Hij is een kleiner, tengerder mannetje dan de normale
bandiet: zijn grootte staat tov de bandiet in `KOOI_VS_BAN` (0,72, oftewel een kop kleiner), en in
de sandbox onder Vijanden, Kooiman stel je hem bij met **kleiner** en **groter**, met **Bandiet
ernaast** om te vergelijken; de hint toont de waarde die je dan in `KOOI_VS_BAN` zet. Dat slepen is
tegelijk zijn gang en zijn rust, hij staat nooit echt stil. Hij is traag, dus wegrennen kan altijd, maar hij houdt de grond voor zich
bezet. Kom je binnen bereik, dan tilt hij de kooi boven zijn hoofd en ramt hem neer op de grond
voor hem. Die smash heeft twee snelheden, maar is één aanval. Op afstand is het een trage, harde
klap met een lange, leesbare aanloop (hij zakt eerst diep door, houdt daar even in, komt dan omhoog
en slaat neer): dat is zoning, loop weg tijdens die aanloop en de klap mist. Maar point-blank, of
als je er tijdens die trage klap recht in loopt, versnelt de aanloop en komt de kooi snel neer (de
snelle slag). Zo loop je niet zomaar door hem heen zoals bij de gewone bandiet: probeer je er vlak
langs te glippen, dan snauwt de kooi neer voor je voorbij bent. De klap zelf en het herstel blijven
even snel, dus het strafvenster is gelijk: de slag baiten en in zijn herstel langs glippen kan nog
steeds. Hij raakt je op het moment dat de kooi de grond raakt, met een zware dreun, een wolk stof
langs de grond (opspattend gruis erbij) en een schok. De trage harde klap kost een heel leven; de
snelle slag, die je tegenhoudt als je te dicht langs loopt, kost er een half. Onder het slepen schraapt de kooi hoorbaar over de grond (een
zachte lus, luider naarmate hij dichterbij komt) en stuift er af en toe een plukje stof op achter
hem. Vrij vaak gromt hij er laag bij (een grr, elke 2,5 tot 5 seconden, luider van dichtbij). Hij begint altijd met een van twee kreten zodra hij in beeld komt ("down you go" of "weak boy"); "dinner time" is er alleen voor als de kooi opengaat en de vogel eruit schiet.

Het bijzondere is hoe je hem verslaat. Tijdens het slepen en de hele smash is hij gepantserd door
de kooi: je stoot, je lage zwaai en een geworpen speer doen hem niets, en de speer ketst af op de
kooi en valt gewoon terug op de grond (je raakt hem niet kwijt). Alleen in het trage herstel na de
klap, als hij uitgezakt over de kooi hangt en hem terugsleept, ligt hij open. Daar sla je toe, en
vier rake klappen in dat venster vellen hem. Hij is dus strafbaar, maar niet gratis: je moet de
smash afwachten en dan snel zijn.

Een kooiman kan ook als **duel** staan (dat is de standaard als je hem in een level zet): een
geënsceneerd 1-op-1 gevecht op open vlakte. Hij komt op met de kooi dicht achter zich, slepend.
Zodra je hem half in beeld hebt staat de wereld even stil, stapt hij de rest in beeld, en ramt hij
de kooi op de grond: het luik klapt open en er schiet een vogel uit. Vanaf dat moment **duwt hij de
nu lege kooi vóór zich uit**, als een schild, en komt zo op je af. Door die kooi raak je hem niet:
een stoot of lage zwaai klinkt af op het traliewerk, en gooi je een speer, dan mept hij hem uit de
lucht (zit hij net midden in een slag, dan versnelt die) en stuitert de speer licht een klein stukje
vóór hem op de grond, waar je hem alleen met gevaar weer oppakt. De enige opening is zijn **herstel**
na een slag: lok een slag uit, stap terug zodat hij misslaat, en steek of gooi terwijl hij uitgezakt
over de kooi hangt. Eén rake treffer in dat venster is in het duel dodelijk. In de sandbox staat de
duw-houding onder Zijn animaties, **Duwen**, en **Duel aan/uit** kiest wat een neergezette kooiman
wordt.

Net als de andere grondvijanden komt hij niet over een kei of een ravijn (regel 7). Een kei tussen
jou en hem is een echte schuilplek: hij stopt ervoor en slaat er niet overheen. Een ravijn houdt
hem net zo tegen. In een leveldefinitie zet je hem neer met `{x: -1500, k: 'kooiman'}`. In de
sandbox staat hij onder Vijanden, **Kooiman**: neerzetten, de AI uit om zijn drie sets (slepen,
smash, herstel) los te bekijken. **Test 37: De kooiman** is het proefstuk: eerst eentje op de open
vlakte om het ritme te leren, dan een kei als schuilplek met een speer die erop afketst, en tot
slot een ravijn dat hem tegenhoudt met twee kooimannen aan de overkant. Hij sleept de kooi naar
links, dus gespiegeld sleept hij naar rechts. De frames staan in `enemies/kooiman/` (onder meer
drag/, duw/, smash/, recovery/ en dood/, met de losse kooi-plaat in kooi/, en `sprites.json` plus de
`LEESMIJ.md`-bestanden als bron). De duw-set is alleen de man; de kooi komt er in de tekenlus als
losse laag over.

### De vogel uit de kooi

Een kooiman met `vogel: true` doet er een tweede, bijzondere aanval bij. Zodra hij volledig in beeld
staat, blijft hij even staan, opent de kooi (hij roept "dinner time") en er schiet een secretarisvogel
uit. Die stijgt op en cirkelt een seconde of drie hoog in de lucht: in die fase is hij ongevaarlijk,
puur de telegraaf. Dan stopt hij, legt de plek vast waar jij op dat moment staat, en duikt daar snel
op af. Blijf in beweging, dan mist hij en slaat hij kapot op de grond (veren en stof); raakt hij je,
dan kost dat een leven en is hij weg. De vogel is niet te raken: wegduiken is het enige antwoord, en
het is eenmalig per kooiman (daarna is de kooi leeg en gaat hij door als de gewone kooi-rammer). De
frames staan in `enemies/vogel/` (fly/ als lus, dive/ voor de duik; de crash doet het spel met stof,
want crash-frames zijn er nog niet). In een leveldefinitie zet je hem aan met `{x, k: 'kooiman',
vogel: true}`; in de sandbox is er bij Kooiman een knop **Vogel aan/uit**. In Test 37 heeft de eerste
kooiman een vogel.

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

Een zegel ligt op de vloer waar hij staat: de savanne, een terras, de vloer van een rotsgebied, of onder de grond op de
bodem van een gang of op een trede van de trap naar buiten. Op een kei om op te springen of een richel ligt hij niet.

Een zegel is een schakelaar: wat er gebeurt als hij aangaat, zet een level erbij. Nu kan hij de grond openscheuren, met
hetzelfde ravijn als in Test 6: `zegels: [ {x: -900, ravijn: -1350} ]`. Dat gebeurt een keer per potje; zet je hem weer
uit, dan blijft het gat open. Zonder `ravijn` licht hij alleen op.

In de sandbox staat hij onder **Zegel**: **Neerzetten** legt er een voor je neer, **Met ravijn erachter** een die de
grond verderop openscheurt.

## Een rune op een rots als schakelaar

Een rune op een rots (de scheve spits, de pieken, de twee zuilen of de scheve boog) was een doel: raak je
hem, dan gloeit hij. Nu kan hij ook iets doen, net als een zegel in de grond: de grond verderop openscheuren
(ook het dak van een gang, dan valt er licht in), een open ravijn weer dichtdoen, de rotswand openen of de
speerval losschieten. Je speer blijft in het hout zitten. De rots staat op de vloer waar hij staat: op een
terras erbovenop, en in een gang op de bodem, dan een kleinere. Hoe hoger de rune, hoe lastiger: tot een
lichaamslengte raak je hem met een gewone worp van dichtbij, en een rune op ruim twee lichaamslengtes raak je
vanaf de grond alleen blind, maar vanaf een kei ervoor zie je hem wel. Een vijand tussen jou en de rune vangt de
speer op.

In de sandbox staat hij onder **Rune op een rots** (Speer en spullen): kies de rots, de maat en de hoogte, en met
**Doet** wat hij doet. Na het neerzetten zegt het spel vanaf hoe ver je hem raakt.

Onder de grond houdt het dak van een gang nu ook je speer tegen: een boog valt er terug de gang in, en een speer die
je bovengronds boven een gang gooit, blijft op de savanne liggen in plaats van door de grond te zakken. En als Amir
geraakt wordt kleurt alleen hij nog even rood, niet meer een heel vlak om hem heen.

## De speerval

Een speer zit horizontaal in de rotswand aan het eind van het level, met de punt naar jou toe. Het is niet Amirs
speer maar een oude valspeer uit de verloren stad: een gekarteld blad van zwart staal met een lichte, geslepen snede,
en wat goud om de schacht. In de vlucht draait hij om zijn eigen as. Stap je op het zegel dat
erbij hoort, dan licht het op, hoor je hem kraken en spannen, trilt de speer even in de wand en schiet hij dan met een klap
recht op je af, op heuphoogte van een
staande Amir. Buk (pijl omlaag of S): dan vliegt hij over je heen. Blijf je staan, dan raakt hij jou, en springen helpt
niet. Wat achter je loopt raakt hij wel: de baviaan, die verder niet te verslaan is, gaat er dood van. Raakt hij hem van
voren, dan blijft de speer in zijn borst steken tot hij als lijk ligt; raakt hij hem van achteren (hij had zich net
omgedraaid), dan blijft hij schuin in zijn rug steken. Mist de speer, dan
valt hij na een eind neer, ligt hij even, en zit hij daarna weer in de wand; het zegel gaat dan uit en werkt opnieuw.

Een level zet hem met `speervallen: [ {x: -2900} ]` (de x van de klif waar hij in zit) en een zegel dat ernaar wijst:
`zegels: [ {x: -2400, speerval: -2900} ]`. Staat er een baviaan in het level, dan gaan de fakkels pas open als hij dood
is. In de sandbox staat hij bij Speer en spullen onder **Speerval**: **Neerzetten** zet een stuk rotswand met de speer
voor je uit en een zegel daartussen, **Losschieten** schiet hem meteen los. Met de baviaan achter je (Van rechts,
Neerzetten, dan J) kun je zo de hele truc proberen.

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

## Het speerteken

Een speer schuin in de grond, met een zwart doek onder de punt en schedels erop of eromheen. Iemand heeft hier ooit een
grens getrokken. Het is decor: je kunt er doorheen lopen en er niets van oppakken. Het doek wappert sneller en buigt
opzij als er een windvlaag langskomt, net als het gras.

Er zijn vijf varianten:

- **Het teken:** twee mensenschedels op de schacht, de een kijkt naar links en de ander naar rechts.
- **Gebroken:** de schacht is afgeknapt en het bovenstuk ligt in het gras, er zit een schedel op de stomp en er ligt er
  een aan de voet. Het doek is verbleekt.
- **Gekruist:** twee speren als een X, met een schedel in het kruis en een in het zand.
- **Jagers:** een buffelschedel met leren riempjes aan de schacht gebonden, een jakhals aan de voet en een rood doek.
- **Kalebas:** een kalebas aan een koordje, op borsthoogte aan de schacht geknoopt. Hij slingert in de wind, en met het
  mes snijd je hem los.

Een level zet het neer met `tekens: [ {x: -900, v: 'gebroken'} ]`, met `f: true` gespiegeld. Nog geen level gebruikt het.
In de sandbox staat het onder het tabblad **Decor**, bij **Speerteken**.

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

Een gewoon ravijn ziet er nu precies zo uit als een ravijn dat openscheurt, maar dan al open: de
rand van de overkant ligt lager dan de grond waar je staat, met klein gras erop en in de winter
een rand van sneeuw, en boven die rand zie je de achtergrond van het level. Een gat boven een gang
onder de grond houdt zijn eigen wand, die doorloopt tot het dak. Een level dat je
zelf maakt krijgt ook deze stijl.

De wand in een ravijn staat verder weg dan de grond waar jij staat, en ligt deels in de schaduw.
De rand aan de kant van de zon werpt een schuine schaduw op de wand, uit dezelfde richting als
waaronder de zon in een gang onder de grond naar binnen valt. Dat geldt voor een gewoon ravijn en
voor een ravijn dat openscheurt (de schaduw groeit dan mee), 's nachts zachter, en in de winter
koel en blauwig.

Amir zijn eigen schaduw is geen ronde vlek meer maar zijn silhouet, plat op de grond: je ziet zijn
benen, zijn speer en een worp erin terug. Hij volgt de zon die je in de lucht ziet. Die staat achter
het landschap, dus de schaduw valt naar voren, naar jou toe, en opzij van de zon af: staat de zon ver
naar rechts, dan valt hij lang naar links, staat hij bijna achter Amir, dan vooral naar voren. Hoe
lager de zon, hoe langer de schaduw, tot iets meer dan zijn eigen lengte. Bij de voeten is hij het
donkerst, naar zijn hoofd toe ijler. Daarnaast ligt er altijd een zachte schaduw recht onder hem, ook
in de vorm van zijn voeten en benen (geen ronde vlek): het licht dat van alle kanten komt. Die is er
ook onder de grond, even sterk als het licht daar. Springt hij, dan vervaagt de zonneschaduw snel en
blijft de zachte schaduw recht onder hem: zo zie je waar je neerkomt. Op een kei, een terras of een
trede ligt hij op het bovenvlak. Onder de grond komt de zonneschaduw er alleen bij waar de zon door een
gat naar binnen valt. 's Nachts is hij zwakker en in de sneeuw koel blauw.

Het licht onder de grond volgt het uitzicht: in de winter valt er koel wit zonlicht door een gat in
plaats van oranje, en 's nachts is het zwakker. En ook buiten werkt het licht: loop je onder een
rotsdak of een overhang, dan wordt het daar geleidelijk wat donkerder, en aan de open kant valt de
zon schuin naar binnen, uit dezelfde richting als waar hij in de lucht staat. Dat is te zien in
Test 1, onder het rotsdak.

In de sandbox staat het onder **Ravijn**: **Smal** en **Breed** zetten een breuk neer waar je
staat. Onder **Zuil** staan twee ravijnen met een smalle strook grond ertussen (zie Test 16).

## Onder de grond

Een gang kan zelf ook ravijnen in zijn vloer hebben: putten. Val je erin, dan ben je dood, net als in een ravijn op de
savanne, en een smalle strook vloer tussen twee putten is een zuil (zie Test 16 en Test 19). Een zegel dat in een gang
ligt en een ravijn in diezelfde gang opent, scheurt de vloer open in plaats van het dak. Een level zet een put met
`putten: [ {x, w} ]`, binnen een gang. In de sandbox staat het onder **Put in de gang**: een put, een zuil, of een zegel
dat de vloer verderop openscheurt; is er nog geen gang, dan komt die er eerst.

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

## Zelf een level maken

In het startmenu staat **Maker nieuwstijl**: een grid waarin je per cel schildert wat er is (grond,
rots, gang, ravijn, een hogere laag), met daarop de voorwerpen, vijanden en schakelaars. **Test** speelt
het grid meteen als level, **Spel-JSON** zet het om naar het formaat van een leveldefinitie in de HTML,
voor `tools/levelcheck.py` of de speelrobot. Wat de Maker allemaal kan staat hierboven bij de updates
over de Maker nieuwstijl, en voor wie eraan werkt in `notities/maker.md`.

De oude bouwer (Level maken, dezelfde wereld als het spel met een laag bediening eroverheen) is weg:
de Maker nieuwstijl is de enige bouwer.

## Mappenstructuur

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

enemies/
  slang1/                  de originele groengele slang: idle_1..8, move_1..8, attack_1..8.png (+ mp4 referenties)
  slang1_zand/             de zandslang die het spel tekent (uit slang1/, via tools/slang_kleur.py)
  slang1_knock/            de knockslang: jade met violette zadels (uit slang1/, via tools/slang_kleur.py), met een eigen venom.png in jade/violet
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
  bandiet/                 de bandiet: een gemaskerde rover met een kromzwaard
                           run/ (14, lus), slag/ (33) en look/ (48) op een canvas van
                           461x504; worp/ (81, de dolkworp) en dood/ (63) op een eigen
                           canvas met een eigen maat (sprites_los.json); dolk/ (het
                           projectiel: dolk_spin_00..07, dolk_recht, met dolk.json). Plus
                           sprites.json en de LEESMIJ-bestanden als bron. De frames kijken
                           naar links; het spel spiegelt ze als hij naar rechts kijkt. De
                           maten staan opgemeten in de HTML (BAN, BAN_SETGEO, BAN_DOLK)
  kooiman/                 de kooiman: een gebukte man die een zware kooi meesleept en neerramt
                           drag/ (29, lus: slepen/rust), smash/ (31, de aanval met holds per
                           frame) en recovery/ (21, het herstel) op een canvas van 726x648,
                           grondlijn rij 598. Plus sprites.json (per frame de ticks, het
                           bronframe en het zwaartepunt) en LEESMIJ.md als bron. De frames
                           kijken naar links; het spel spiegelt ze als hij naar rechts kijkt.
                           De maten staan opgemeten in de HTML (KOOI, KOOI_SMASH, KOOI_LIJF)
  hyena/
    loop/                  loop_00..19.png (aankomen en achteruit stappen)
    dreigen/               dreigen_00..21.png (op afstand blijven grommen)
    ren_lijf/              ren_lijf_00..11.png (onderlaag van de aanvalsren, 16 fps)
    ren_kop/               ren_kop_00..26.png (bovenlaag: de happende kop, 8 fps)
    metadata.json          canvas, grondlijn, aantallen, fps en de kop-offset per lijfframe

amir runc/
  amir_sprites/design/amir/
    speerworp/             speerworp_00..19.png (eenmalige worp, 20 frames, 12 fps),
                           metadata.json (canvas 984x814, grondlijn rij 803, anker_x 330,
                           Amir 620 px hoog, spannen 0-6, uithaal 7-10, los op 10, herstel 11-19)
    speer_projectiel.png   de geworpen speer, 624x67, punt naar rechts op pixel (623, 33)

design/speer/
  draai/                   gewoon_00..35.png (Amirs speer, 624x140) en val_00..35.png (de speerval,
                           758x140, zwart staal met goud): een hele rol om de lengteas, frame 0 plat,
                           punt rechts op (w-1, 70)
  bron/draaispeer.mp4      de video van Grok waar tools/draaispeer.py de frames uit maakt

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
  vegetatie/               boom_sheet, drygrass_sheet, struik_sheet (bewegende vegetatie)
  water/                   pool_links/midden/rechts, rimpel_01..08, spetter_01..08

sounds/                    hyena_bite.mp3 (lange opname; alleen 14,0-16,0 s is de hap die het spel
                           afspeelt), hyena_laugh.mp3 (de lach), en ahhit.mp3 en stopit.mp3: de twee
                           kreten van Amir als hij geraakt wordt (om en om, met een stilte ertussen,
                           zodat hij niet de hele roedel doorpraat)

music/                     bg.mp3 (het oude thema), darkafrica.mp3 (de basismuziek),
                           stemmen van Amir (iamtheking, iamamir, iamamirfatherson,
                           hellomyfriend, ikill, protectinnocent, godsforsaken), snakehiss, spearthrust, scatter,
                           watersplash (de volle plons: instappen en landen) en waterstep (de korte knip
                           uit diezelfde plons, voor de voetstappen in het water)
```

De `*_magenta.png` en `*_sheet.png` bestanden die nog in de mappen staan zijn bronmateriaal; het spel gebruikt de losse frames (behalve bij de vegetatie, die juist van de sheets komt).
