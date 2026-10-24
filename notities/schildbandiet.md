# De schildbandiet

## de schildbandiet: loopt met zijn schild op en valt springend aan

`SCHB`, `makeSchildman`, `updateSchildman`, `hitSchildman`, `schbMik`, `schbSprongP`, `schbLand`. Het ritme van het gevecht, afgestemd met `tools/schildduel.js`: hij loopt op Amir af tot `houd` (1 Amir) en zet op `aanval` (2,1 Amir) de sprong in. De tell (frame 0..5, ~0,8 s) is tot `pantserVan` (3) te onderbreken; daarna zet hij door (een treffer kost schild maar onderbreekt niet). Tot `mikTot` (7, net na de afzet) stuurt hij bij naar Amir, zo dat zijn speerpunt (`speerVoor`, 0,62 Amir voor zijn midden) op Amir de grond in gaat; de sprong (6..16, ~0,57 s) is onaantastbaar en vloeit op de klok (`schbSprongP`). Hij raakt op 17..20 rond de punt (`speerR`) of onder zijn lijf (`lijfR`) en slaat Amir dan terug (`raakDuw`); de landing geeft een hitstop (`landStop`), schok en een zet die dichtbij harder is (`landDuw`). Het herstel (21..29, ~0,8 s) is het raam om te straffen. Een treffer geeft een korte hitstop (`raakStop`, `breekStop`) en een flinch die meteen begint (`flinchVan`) met een terugstoot (`flinchDuw`); vanaf `dekVan` in de flinch ketst je speer af (geen stunlock), en binnen `wraakT` slaat hij terug met een tell die al gepantserd is. Gemeten op 1280 bij 720: met 0,2 s reactie ontwijk je alles, met 0,35 s word je bij twee van de drie sprongen geraakt, blind steken of stilstaan kost meerdere levens; het gevecht duurt zo'n 8 tot 10 seconden. Dat is het niveau `moeilijk` (zonder veld). Met `niveau: 'makkelijk'` in zijn spawn (`SCHB_NIVEAU`, `schbN`, `schbDur`) heeft hij een langere tell, een tragere sprong en een langer herstel, mikt hij alleen tot de afzet, zet hij later door en slaat hij na een flinch niet gepantserd terug. Het tempo per niveau staat in `SCHB_TEMPO` (tell, aanval = sprong en inslag, herstel; hoger is sneller, `schbDur` deelt de frameduur erdoor en de sprong beweegt vanzelf mee) en is live af te stellen in de pauze onder **Schildbandiet: tempo** (`pzschb`, `SCHB_SCHUIF`, bewaard onder `SCHB_TEMPO_KEY`, de knop alleen in een level of sandbox met een schildbandiet, `schbTempoKnopToon`); aanval en herstel staan bij beide niveaus standaard op 150% (de tell op 100%). Bij het landen klinkt hetzelfde geluid als Amirs speerstoot (`schbLandGeluid`, `music/spearthrust.mp3`, eigen stemmen, verder weg zachter), niet meer het grondgeluid van de kooiman. De houtklap op het schild (`HOUT`, `houtRaak(toon, vol)`, `houtDuik`, `sounds/houtraak.mp3`) is de beloning van het gevecht en staat daarom boven de stoot: het bestand is genormaliseerd naar -1 dB (het zat 6 dB onder `spearthrust.mp3` en verdronk erin, zodat je bij een treffer geen hout hoorde), Amirs stoot (`#thrust`) duikt op de treffer naar `duik` (0,3; elke nieuwe stoot zet zijn volume zelf terug), elke volgende klap klinkt een slag lager (`toon` per schild dat er na de klap over is: 1, 0,93, 0,86, met `preservesPitch` uit zodat lager ook zwaarder is), de breuk krijgt `breek.na` (0,07 s) later een tweede, lagere klap, en het afketsen als hij zich dekt (`dekVan` in de flinch) speelt `kets` (hoger, 1,25, en zachter, 0,6), zodat te horen is dat die treffer niet telde. `wiebel` (5%) strooit wat in de toon tegen het mitrailleurgevoel. Nagemeten in Chromium met een patch op `HTMLMediaElement.play`: elke schildtreffer speelt het bestand, met de stoot op 0,3 op dat moment. Het verstopte zegel gebruikt dezelfde tik via `houtRaak(1, .3)`. Met `achter` (px) start een spawn op hetzelfde moment als de spawn op zijn x, maar zoveel verder weg, zodat hij een tel later het gevecht in loopt: zo komen er twee na elkaar (werkt ook voor de bandiet en de kooiman). Test 45 is het proefstuk, Test 46 loopt op van een makkelijke via twee makkelijke en een moeilijke naar twee moeilijke, dan een bandiet met een moeilijke en een moeilijke met de kooiman (gespeeld met `tools/schildduel.js --level "Test 46"`: met 0,35 s reactie 0, 2, 2 en 4 keer geraakt); in de sandbox onder Vijanden. In de Maker nieuwstijl staat hij onder Vijanden als Schildbandiet met twee varianten: Moeilijk (`schildman`) en Makkelijk (`schildman:makkelijk`, wordt in `mkSpawn` `niveau: 'makkelijk'`)


## de schildstaat: het schild gaat zichtbaar kapot

`SCHB_STAAT`, `SCHB_SETS`, `schbStaat`, `schbBankVoor`, `schbFrameImg`. Het schild zit in de frames gebakken, in vier standen: 0 treffers `metschild`, 1 `fase1` (een hap eruit), 2 `fase2` (twee happen), 3 `zonderschild` (weg, daarna in een klap dood). `schbStaat` leidt de stand af uit `s.schild` en `s.metSchild`; omdat `hitSchildman` het schild al verlaagt voor de flinch begint, speelt de flinch meteen in de nieuwe stand en verschijnt de hap op het moment van de klap. Bij een gepantserde treffer (late tell) wisselt de strike midden in de animatie van set; dat verspringt niet, want het lijf is in alle sets pixel voor pixel hetzelfde (zelfde canvas 544x860, grondlijn 781, anker 272, zelfde timing). De loop blijft `loop_metschild` tot het schild weg is.

Welke sets er op schijf staan, staat in `SCHB_SETS` (per animatie de lijst `standen`). Een stand zonder eigen set valt terug op de stand ervoor (`schbBankVoor`). Nu ontbreekt alleen `flinch_fase1`: de strike toont na de eerste treffer de ene hap (`strike_fase1`), maar de flinch van die eerste treffer speelt nog met een heel schild. Komt hij erbij: frames in `enemies/schildbandiet/flinch_fase1/`, `'fase1'` in de lijst `standen` van `flinch`, dan `gen-klein.py` en `gen-offline-manifest.py`. Upload frames altijd in hun eigen map (of als zip): de sets hebben dezelfde bestandsnamen en overschrijven elkaar in de hoofdmap. Laden, `warmBouw` en de laadpoort volgen vanzelf (alles in `schbBank`). De bron staat in `enemies/schildbandiet/LEESMIJ_schildfases.md` en `metadata.json` (`schild_staat`).
## de nieuwe stijl: het schild als losse laag (lagen.json)

`SCHB_LAGEN`, `schbLagen`, `schbLagenLaad`, `schbLagenLijst`, `schbLaadBasis`, `schbBank.lagen`. Op proef naast de complete
sets, uit de Animeer tool (export 24-10-2026, versie lagen-2; de bron staat in `enemies/schildbandiet/LEESMIJ_lagen.md`).
Het schild is een eigen plaatje en de rest van de figuur is tot zo weinig mogelijk lagen samengevoegd, elk bijgesneden tot
zijn eigen randen. `enemies/schildbandiet/lagen.json` geeft per beweging (`loop`, `strike`, `flinch`), per frame en per
schildstaat (`metschild`, `fase1`, `fase2`, `zonderschild`) de lagen in tekenvolgorde, elk `{src, dx, dy, w, h, schild}`:
`dx`, `dy` de linkerbovenhoek ten opzichte van het anker (272) en de grondlijn (781), `w`, `h` de tekenmaat, allemaal in
pixels van de grote set. De tekencode doet daarom na de `translate` naar de voeten en de spiegeling gewoon
`drawImage(img, dx * gs, dy * gs, w * gs, h * gs)` per laag; de kleine set (`klein/`) tekent met dezelfde getallen een half
zo groot plaatje. De plaatjes staan in `lagen/lijf/` (116) en `lagen/schild/` (81); elk staat er een keer, ook als het in
meerdere frames of staten terugkomt (de loop gebruikt per staat steeds hetzelfde schildplaatje), en `schbLagenLaad` maakt per
`src` een Image die in `schbBank.lagen` gedeeld wordt (zo warmt `warmBouw` ze mee). De flits (`whiteCopy`) gaat per laag.

Alleen de tekenlaag is anders. De bewegingen, de frametelling (22, 30, 21) en de timing zijn die van de complete sets
(`schbAnim`, `SCHB.strikeDur`, `SCHB.flinchDur`), `schbStaat` kiest de staat, de vault hergebruikt de strike-lagen, en de dood
blijft de eigen set in `dood/` (`schbLaadBasis` laadt die en de losse speer voor beide stijlen). Een schildbandiet tekent zo
met `lagen: true` in zijn spawn (`schbLaadLevel` laadt dan de lagen in plaats van de complete sets; `laadJsonOpen` houdt de
laadpoort dicht tot `lagen.json` binnen is en de plaatjes aangevraagd zijn), en in de sandbox met **Nieuwe stijl** onder
Schildbandiet (naast Moeilijk en Makkelijk) (`sbSpawn('schildman_lagen')`). Nagemeten in de sandbox op 1280 bij 720: oude en nieuwe stijl op
dezelfde plek in dezelfde houding en staat (loop, tell, inslag, herstel, flinch, met heel, aangeslagen en zonder schild)
geven hetzelfde beeld op hooguit randpixels na.

Geheugen: de drie bewegingen in alle vier de staten zijn als lagen ongeveer 67 MB uitgepakt (grote set), tegen zo'n 550 MB
als complete frames per staat zouden zijn. `tools/gen-klein.py` halveert de lagen met een eigen doel
(`enemies/schildbandiet/lagen`, drempel 60, voor de map `enemies/schildbandiet` zodat die drempel wint), want de bijgesneden
stukken zijn lager dan de gewone drempel van 400.

**Bevalt het, dan gaat de oude manier eruit.** Dat is: de mappen `loop_*`, `strike_*` en `flinch_*` (en hun kleine versies,
via `gen-klein.py` en `gen-offline-manifest.py`), `SCHB_SETS`, `schbBankVoor` en de set-tak van `schbFrameImg` en `schbLaad`
(de dood en de speer blijven, in `schbLaadBasis`), het veld `lagen` en de tweede sandbox-knop (dan is de lagen-stijl de
enige), de `sets` in `metadata.json` en de notitie hierboven over de schildstaat per set.

## de dood

`SCHB.dood`, `schbSterf`, `schbGeo`, `SCHB_SPEER`, `schbSpeerLos`, `schbSpeerStap`, `schbSpeerTeken`. Na de schildbreuk is hij in een klap dood: `schbSterf` geeft de witte flits en de hitstop (`breekStop`), speelt de doodskreet van de bandiet (`banSterf`, `sounds/banditdeath.mp3`) en zet de dood-set aan. Die staat in `enemies/schildbandiet/dood/` (`dood_00..36`, met `dood.json`, `LEESMIJ.md` en `preview.gif`). De set heeft een eigen canvas (544 bij 560, grondlijn 481, hetzelfde anker 272 en dezelfde schaal), dus de tekencode pakt de maat via `schbGeo`. Hij speelt even snel als de dood van de bandiet: 37 frames in de totale duur van de bandiet (`BAN.n.dood` frames op `BAN.fps.dood`, 2,1 s), zo'n 17,6 fps. Daarna blijft `dood_36` liggen als lijk; hij vervaagt niet. Na het laatste frame loopt `s.ligT`: voorbij `SCHB.dood.lig` (7 s) vervaagt hij via `s.alpha` in `SCHB.dood.vervaag` (0,8 s), zijn losse speer tekent met dezelfde alpha mee, en op nul gaat hij naar `weg` (opgeruimd in `updateSchildmannen`). Geldt voor elke schildbandiet, in elk level.

**De speer valt los.** In de oorspronkelijke frames zat de speer in de tekening (hij glipt uit zijn hand en ligt plat voor zijn voeten), ook als hij op de rand van een ravijn of naast een kei stierf. `tools/schildbandiet_dood.py` haalt hem eruit: vanaf frame 7 is de speer weg (de schoenen erachter komen uit een frame waar ze vrij stonden), en de twee bron-frames waarin hij voor de tuniek langs viel zijn eruit, want wat erachter zat was niet netjes terug te halen (39 werd 37 frames). Het spel laat zijn eigen speer vallen (`enemies/schildbandiet/speer/speer_overlay.png`): `schbSpeerLos` zet hem op frame `SCHB.dood.speer.los` (7) op de plek waar hij hem op frame 6 vasthield (`punt`, `eind` in canvas-px), en `schbSpeerStap` laat hem vallen als een staaf met vijf steunpunten (`SCHB_SPEER.steun`) die elk op de vloer onder zich botsen (`schbSpeerVloer`: de grond, een terras of gang, een kei of richel; boven een ravijn niets). Zo stuit hij even, ligt hij plat of scheef, en kantelt hij over de rand een ravijn in; dieper dan `SCHB_SPEER.weg` is hij weg. Hij ligt `voor` canvas-px voor de voeten, zoals in de tekening, en flitst mee met de doodklap.

**Na de flits meteen los.** `SCHB.dood.start` (7): na de witte flits begint de dood op het eerste frame waarop de speer al niet meer voor zijn lijf hangt, en valt de losse speer meteen. Met `start: 0` speelt hij de klap ervoor weer (frame 0 tot 6, waarin hij de speer nog vasthoudt).

**Het lijf op de grond.** In de bron lag hij na de val zo'n 15 tot 30 canvas-px boven de grondlijn: hij zweefde boven zijn schaduw. Het script zet elk frame vanaf de landing zo ver omlaag dat de onderkant van het brede deel van zijn lijf op de grondlijn ligt (`LIG`), met de landing verdeeld over de twee frames ervoor; hoeveel per frame staat in `dood.json` (`omlaag`). De schaduw wordt breder vanaf `SCHB.dood.ligVan`.

Een nieuwe dood-animatie zonder speer erin past zonder het script: zet de frames in de map, `n` op het aantal, `speer.los` op het frame waarop zijn hand opengaat en `punt`/`eind` op de plek van de speer in het frame ervoor. Teken het liggende lijf dan met zijn onderkant op de grondlijn (481). In de sandbox laat de knop **Dood** onder Schildbandiet elke schildbandiet meteen zo sterven.

## de executie: knielen, wankelen, vallen en de special execution

`EXE`, `exeLaad`, `exeKans`, `exeStart`, `exeTick`, `exeVries`, `exeTeken`, `exeHelften`, `sbExeNu`. De lagen staan in
`enemies/schildbandiet/executie/` (`executie.json`, `LEESMIJ.md`, `lagen/` met 127 plaatjes): optie C, zoals `lagen.json`,
per beweging per frame een lijst lagen `{src, dx, dy, w, h, item}` in tekenvolgorde, `dx` en `dy` vanaf het anker (272) en
de grondlijn (781) in pixels van de grote set. De bewegingen: `knielen` (20), `wankel` (16, loop), `val` (16, met
`speer_ligt_op`) en `executie` (17, met `amir_start_x`, `amir_eind_x` en de `snijlijn`). `exeLaad` laadt ze zoals
`schbLagenLaad` (via de laadpoort, de plaatjes in `schbBank.executie` zodat `warmBouw` ze meebakt) en wordt door
`makeSchildman` aangeroepen, dus voor elke schildbandiet, ook in een level. `hitSchildman(s, wijze)` weet nu waar de klap
vandaan komt (`steek`, `worp` of `zwaai`); is het schild weg, dan beslist `exeKans` of de kill een executie wordt
(`EXE.kansSteek` 1 op 5, `EXE.kansWorp` 1 op 3, alleen als de lagen binnen zijn) en anders is het de gewone dood
(`schbSterf`). Een schildbandiet in de executie heeft `s.state === 'exe'` en in `s.exe.bew` de beweging.

**De steek-kill**: `exeStart` zet hem naar Amir toe (`s.face`), begint `knielen` en bevriest meteen de wereld
(`exeBevries`): `exeVries` is de schildbandiet van wie de executie loopt, en `loop` zet dan `dt` op nul en laat alleen
`exeTick` op echte tijd lopen, zoals `kooiVries`. Amir staat op `amir_start_x` (`exeAmirX`, met de spiegeling in
`s.exe.dir`), kijkt naar hem, zonder lopende stoot of worp, en is onkwetsbaar (`hurtPlayer`, `amirVast`, `startSweep`
en `dir = 0` in `loop` kijken naar `exeVries`). Tijdens het knielen is de echte Amir nog te zien maar zonder speer
(`exeSpeerWeg`, die zit in de schildbandiet); zodra `executie` begint is hij weg (`exeAmirWeg`: geen sprite, schaduw, rug
of health-balk) en tekenen de lagen hem, op de plek en de schaal van de schildbandiet, gespiegeld als die naar rechts
kijkt. Na het laatste frame (de landing, 600 ms) splijt hij (`exeSplijtStart`): de `schildman`-laag van het laatste
frame wordt langs de snijlijn, doorgetrokken over de hele laag, in twee helften geclipt (`exeHelften`) die uit elkaar
schuiven, om hun voet kantelen, zakken en vervagen (`EXE.splijt`), met de spuit van het bloedsysteem op de wond langs de
lijn omhoog (`exeSpuitTeken`, `bloedSpuitStap`) en druppels die langs de lijn wegspatten en op de grondlijn blijven
liggen (`exeDruppelsTeken`; de lens en de plas bestaan nog niet in het bloedsysteem); de `amir`- en `speer`-lagen van het
laatste frame blijven er bovenop. Daarna (`exeEinde`) staat Amir meteen in zijn idle op `amir_eind_x` (niet boven een
ravijn, anders op `amir_start_x`), van hem af gekeerd, met zijn speer in de hand, en loopt de wereld weer; het bloed
blijft nog `EXE.lijk` en vervaagt dan.

**De worp-kill**: `exeStart` haalt de geworpen speer weg (`jav = null`, de lagen tekenen hem in zijn borst), de wereld
loopt gewoon door: `knielen`, dan `wankel` in een loop, `EXE.wankelDuur` (3 s) lang. Staat Amir binnen `EXE.eReik` (ruim een
Amir) van hem, aan beide kanten, op dezelfde vloer (`exeBij`), dan staat er een E boven hem (staat Amir achter hem, dan
draait hij bij E eerst naar hem toe) (`exeETeken`, via `skE`; `eNodig` zet de E-knop
op de telefoon erbij) en start E de executie (`exeTrek`, vooraan in `toggleSpear`). Zonder E maakt hij de lopende loop af
en speelt hij `val`; vanaf frame `EXE.speerLigtVan` (7) ligt Amirs speer echt op de grond (`exeSpeerNeer`: een `jav` op
de grond op `speer_ligt_op`, de punt naar zijn voorkant, op te pakken met E zoals na een worp; is je hand al weer vol van
de rug, dan een losse speer), en tekent de `speer`-laag niet meer. Daarna blijft hij liggen en vervaagt hij zoals de
gewone dood (`SCHB.dood.lig`, `vervaag`).

**Effecten en geluid komen later.** De haakjes staan klaar: `exeHaakFreeze` (begin van de freeze, de steek of E),
`exeHaakRuk` (executie frame 5 naar 6), `exeHaakLanding` (frame 16) en `exeHaakSplijt`. De executie speelt nu zonder de
doodskreet en zonder het geluid van de bloedspuit.

**Kleine set en geheugen.** `tools/gen-klein.py` halveert `enemies/schildbandiet/executie/lagen` met drempel 60 (zoals de
lagen van loop, strike en flinch); `dx`, `dy`, `w` en `h` blijven, het spel rekt het halve plaatje naar die maat.
Gemeten in de sandbox: de 127 lagen zijn uitgepakt 27,4 MB op de grote set en 7,3 MB op de kleine (5,3 MB en 1,6 MB op
schijf). Ze laden mee zodra er een schildbandiet is.

**Sandbox**, onder Schildbandiet: **Executie: kans/altijd** (`sbExeAltijd`, elke steek- en worp-kill wordt een
executie), **Wankel: E aan/geen E (val)** (`sbExeGeenE`: de worp-kill krijgt geen E en eindigt in de val), **Steek-kill**
en **Worp-kill** (`sbExeNu`: de eerste levende schildbandiet meteen zo doden; bij de steek krijgt Amir zijn speer in de
hand, bij de worp zit zijn speer in de schildbandiet). Nagekeken op 1280 bij 720, groot en klein, naar links en
gespiegeld: de steek, de worp met E, de worp zonder E (de speer ligt naast hem en is op te pakken), zonder consolefouten.
