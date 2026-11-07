# De stad: een Sahelstraat van leem

`STAD`, `stadAan`, `stadLaad`, `stadLees`, `stadPlats`, `stadAchter`, `stadTeken`, `stadVeer`, `stadSprong`

Een level met het veld `stad` speelt in een drukke straat van een Sahelstad, overdag (uitzicht `stad_dag`).
De onderdelen staan in `design/stad/`, met alle maten in `design/stad/metadata.json`. Stad 1 (de episode Test levels stad, eerst Test 59) is het proefstuk;
in de sandbox onder Terrein de knoppen **De stad** (Neerzetten, Weg).

```
stad: { paleis, seed, gevels: [{x, hoog, f}], galerijen: [{van, tot, h}],
        kramen: [{x, soort, f}], voet: [{x, stuk, f}] }
```

## De straat

`design/stad/straat.png` komt in de plaats van de grondrand (`bodemPic`). Het plaatje heeft precies de maten en
rijen van `EDGE` (1572x335, kruin 46, walk 95, solid 305), dus ravijnen, terrassen en de Maker werken er zonder
iets anders mee. Het is gemaakt door Grok de grondrand te laten overschilderen (image-to-image), zodat de vorm en
de looplijn gelijk bleven, en daarna naar een warme zandbruine tint gekleurd met behoud van licht en donker.

## Gevels

Een huis wordt gestapeld uit drie banden van `gevel.png`: het dak (`STAD.gevel.dak`), dan `hoog - 1` keer de
verdieping (`ver`), dan de begane grond (`bod`). De naden lopen net onder een balkenrij, dus de banden sluiten
naadloos. `x` is de linkerkant van het plaatje, `f` spiegelt. De maat hangt aan Amir: het deurgat is 1,3 Amir
hoog (`amir: 318` bronpixels per Amir), dus net als een kei schaalt de breedte mee met het scherm en liggen de
hoogtes vast in sprite-eenheden.

- Het dak is beloopbaar: een dun platform op `dakAchter` (de bovenkant van de balkkoppen, 57 bronpixels onder de
  kartels), over de muur (`muur`). Hoogtes: 1 hoog 442, 2 hoog 771, 3 hoog 1100, 4 hoog 1429 (`stadGevelH`). Een
  verdieping is 329. Wie op het dak staat, staat achter de kartels (zie "Achter de kartels" hieronder).
- Een gevel is decor op het vlak van de straat: Amir en de vijanden lopen ervoor langs, er botst niets.
- Contactschaduw aan de voet (`STAD.schaduw`), zodat de muur niet als een liniaal op de straat staat.
- Het deurgat is donker. De rechthoek staat in metadata.json (`deurgat`), en in `STAD_DEUR.gat`: daar stapt een vijand uit
  (zie "Deuren" hieronder).

## Achter de kartels

`STAD_KANTEEL`, `STAD.gevel.dakAchter`, `STAD.kanteelBreed`, `stadKanteelVoor`, `stadKanteelAmir`

Wie op een dak staat (Amir en de vijanden), staat achter de tanden, zoals op een echt Sahelhuis: het dak ligt op de
balkkoppen, de muur met de kartels loopt ervoor omhoog. In een kanteel zie je hem vanaf zijn enkels, achter een tand
tot aan zijn knie.

- Het dak ligt op `dakAchter` (125 bronpixels) in plaats van `dakLoop` (68, de onderkant van de kartels): 45 lager.
  Dat geldt voor elk dak in de stad, ook in de bestaande stadslevels. Een vijand met `dak: 487` of `dak: 816` (de oude
  hoogte) vindt zijn dak nog: `stadVloeren` geeft een dak ook zijn oude hoogte mee (`oud`), en `stadDakPlek` telt die.
- Na de personages tekent `stadKanteelVoor` de bovenkant van de gevel (rij 0 tot `dakAchter`) nog een keer, maar alleen
  in een strook van `kanteelBreed` (0,7 Amir) aan elke kant van wie op dat dak staat. Wie op de straat ervoor springt,
  komt er dus gewoon voorlangs.
- Amir telt pas als hij op het dak geland is (`stadKanteelAmir`, gezet als hij op de grond staat): van de straat omhoog
  spring je voor de muur langs, na de landing sta je erachter. Een vijand telt als zijn vloer (`base`) het dak is.
- Een galerij of trapbalkon hangt voor de gevel. Ligt het dek op dezelfde hoogte als een dak, dan staat wie op het dek
  staat toch voor de kartels: alleen wie echt op het dak staat, staat erachter.
- Een dode ligt languit: om hem heen is de strook breder (`STAD.kanteelLijk`, 1,6 Amir), anders steken zijn voeten
  links of rechts onder de tanden uit.
  De kruisboogbandiet ligt als lijk bijna 4 Amir lang en zakt 50 bronpixels onder zijn grondlijn, dus onder de
  dakrand: hij krijgt een eigen vak om zijn hele laatste frame (`KRB.lijk`, `krbLijkVak`), en daar tekent
  `stadKanteelVoor` ook het stukje muur onder de dakrand opnieuw. Sterft hij vlak bij de rand van een huis, dan schuift hij tijdens
  het vallen naar binnen tot zijn hele lijk op het dak past (`krbDakDoel`, `krbDakSchuif`): aan de zijkant steekt
  nooit iets de lucht in.
- Het dak is 45 lager, dus soms makkelijker te halen: vanaf het rieten dak van een kraam (263) haal je nu het dak van
  een huis van 1 hoog (442), dat lag eerst net buiten een sprong (208).
- In de sandbox onder Terrein, De stad: **Achter de kartels** (aan of uit, uit is de oude manier met iedereen voor de
  kartels) en **Bandiet op het dak** (op het huis van 2 hoog).

## Galerijen

Een houten looprichel langs een gevel, 9-slice uit `galerij.png` (links, het midden zo vaak als nodig, rechts).
`van` en `tot` zijn de index van een gevel, zodat hij altijd precies over die huizen loopt, ook als de breedte
meeschaalt. `h` is de hoogte van het dek (zonder `h` de tweede verdieping, 730, `stadVerdieping(2)`; de eerste is 401). Het dek is een dun platform: van
onderen spring je erdoorheen. De reling staat achteraan, Amir loopt ervoor.

Amir springt 208 hoog. Een verdieping (329) is dus te hoog om zomaar te halen: een route naar boven gaat via de
kraam, de doek, of galerijen die tussen twee verdiepingen hangen (Stad 1 heeft er drie boven elkaar langs de toren).

### Lift bij een galerij

`takelGalerijStap`, `TAKEL.galerijBoven`, het veld `galerij` op een takel

Een galerij schaalt mee met het scherm, een takelplateau heeft een vaste breedte in wereld-px. Een vaste `px` sluit dus
maar op een schermmaat aan (Stad 1 overlapte op een laptop 125 px met het eind van de galerij, op 1920 lag er een gat van
364 px). Met `galerij` (de index in `stad.galerijen`) schuift het spel het plateau daarom tegen het eind van die galerij,
op elk scherm opnieuw (alleen als `nowScale()` verandert): zijn binnenrand op de looprand van de galerij (de rand die
`stadPlats` ook gebruikt, `0,15` van het eindstuk naar binnen), zodat de vloer doorloopt. Welk eind kiest de `px` uit het
level (de kant waar hij staat). De wielen schuiven evenveel mee, zodat de lift heel blijft. De hoogste stand wordt het dek
plus de looplijn van het plateau plus `TAKEL.galerijBoven` (17): boven staat het plateau net boven de galerij, je stapt
eraf en niet tegen een rand op. De paal (`stamZij`) komt aan de straatkant, want aan de galerijkant hield het begaanbare dek
op bij de paal en lag er een gat. `hoog` en `stamZij` uit het level tellen dan niet. Op een groot scherm schuift de hele lift
dus wat op; het wiel kan dan voor een kraam staan (decor, het werkt gewoon).

## Vijanden op een galerij of dak

Een galerij en een dak zijn ook de vloer van een vijand: `vloerBij` vraagt het aan `stadVloerBij` (na de zwever), dat
in `stadVloeren` de daken en galerijen kent (gecachet per schermmaat en level). Wie binnen hun rand staat en niet meer
dan `STAD.vijandMarge` (30) onder de looplijn, heeft die als vloer. Zo werkt de rest vanzelf: `dropAhead` houdt hem bij
de rand tegen (zoals een ravijnrand, regel 7), en `banZelfdeHoogte`, de kooiman/schildman en het zicht vergelijken de
vloer onder Amir op de galerij goed. Wie eronder loopt blijft op de straat (de marge is klein, en een dun platform is
geen muur in `blocksMonster`). De tafels, het rieten dak en de doek tellen niet mee.

Een spawn met `dak` staat erop (bandiet, schildbandiet en kruisboogbandiet, `stadDakPlek`): `dak: 401` kiest de galerij of het dak op
die hoogte dat het dichtst bij x ligt, `dak: true` het hoogste. Zijn x schuift ruim binnen de rand, want de huizen en
galerijen schalen mee met het scherm en een vaste x kan op een andere maat net naast een dak vallen. Een hyena komt
van de rand van het beeld en kent dit niet. In de sandbox: **Bandiet op de galerij** onder De stad. In de Maker
nieuwstijl krijgt een bandiet of schildbandiet die op een dak, galerij of balkon staat vanzelf `dak` (zie "Vijanden op daken
en de meldingen van de stad" in `notities/maker.md`); daar staan ook de gevels, galerijen en trappen (het plan
`notities/plan-stad-maker.md` is klaar).

Een galerij over meerdere huizen (`van` tot `tot`) loopt door over de kieren tussen de huizen, op elke schermmaat.
Dat is de lange looprand van Stad 1, met het gevecht erop. Een rij daken loopt alleen door als de huizen elkaar op
die schermmaat raken.

## De camera

In de stad klimt de camera mee (`updateCamera`, `stadAan()` telt als een klimlevel), anders liep je op een galerij of
dak boven uit beeld. Zakt de straat daarbij onder uit beeld, dan loopt onder de voorste achterrij een stoffige straat
in de verte door (`STAD.verteStraat` in `stadAchter`), in plaats van de lichte nevel.

## Kramen

- `riet`: de tafel (72) en het rieten dak (263) dragen allebei. Samen een trap: grond, tafel, dak, galerij.
- `doek`: de tafel draagt; de doek (267) veert. Na een val wip je terug (`terug` x de valsnelheid, vanaf `min`),
  sta je erop en spring je, of druk je springen net voor of vlak na het landen (`raam`), dan schiet je hoog
  (`hoog` x jumpV, ongeveer 900): tot op het dak van een huis van 2 hoog. De doek buigt mee (`stadDoekDip`).
- De kramen zijn wat rustiger gebakken (`kraamZacht`), zodat een vijand ervoor goed te lezen blijft.
- Ze zijn 1,06 Amir hoog: hoger kon niet, dan haal je het dak niet meer vanaf de tafel.

## Voetdecor

Losse stukjes uit `voetdecor.png` (`STAD.voet.stukken`): zandhoop, stenen, bakstenen, scherven, kruik, stro, puin.
Zandhoop, stenen en puin worden naar de kleur van de straat getint. Zet ze tegen de voet van een muur, daar breken
ze de rechte lijn tussen muur en straat.

## De verte

`stadAchter` tekent na de zon (in `sceneAchter`) het paleis en drie rijen huizen, in plaats van bergen en heuvels:

- Het paleis (`paleis.png`) is een heldlaag met bijna geen parallax (0,03), dus hij blijft de hele straat in
  beeld. `paleis` in het level is zijn wereld-x. Er is nevel overheen gebakken.
- De rijen worden gebouwd uit dezelfde `gevel.png`, kleiner en met nevel (`STAD.rijen`), voorgebakken op
  `STAD.bak` van de bronmaat. De hoogtes komen uit `stadReeks` met de `seed` van het level.
- Onder de verste rij loopt de nevelkleur door tot de grond, zodat er nergens lucht onder een huis zichtbaar is.

## De stadstrap

`STAD_TRAP`, `stadTrapMaat`, `stadTrapBij`, `stadTrapE`, `stadTrapStap`, `stadTrapAchter`, `stadTrapVoor`, `stadInGevecht`,
`stadTrapNabij`, `stadTrapCamX`, `stadTrapCamY`, `stadTrapAlfa`, `stadTrapUitLaag`

`stad.trappen: [{gevel, kant, niveau, balkon}]`: een oude houten buitentrap (`design/stad/trap.png`, plat van voren
gezien, net zo plat als de gevels) naast gevel `gevel`. Kant `'r'`: rechts van het huis, dus de kant waar je vandaan komt
(Amir loopt naar links); `'l'` links. Hij loopt van `niveau` (0 de straat, 1 de eerste verdieping 401, 2 de tweede 730)
een verdieping omhoog. De treden zijn altijd even groot (de schaal hangt aan de eerste verdieping); een kortere trap
(van 401 naar 730) wordt bovenaan afgesneden, achter het bordes.

- De trap staat met zijn binnenste balk achter de muur, met een schaduw van de muur op de treden. Bovenaan ligt een bordes
  (een dunne strook van de galerij met leuning) dat achter de muur doorloopt, achter de trap getekend.
- Aan de andere kant van het huis kom je boven uit: op een balkon (`balkon`: breedte in Amir, standaard 1,6, met twee
  schoren naar de muur), of met `balkon: 0` op een galerij die daar al loopt. Op die plek zit altijd een opening in de
  leuning (`gat`, 0,62 Amir); dat is ook de plek waar je weer naar beneden gaat.
- E bij de voet of in de opening (`eDruk`): Amir vervaagt (`STAD_TRAP.uit`, `stadTrapAlfa`), staat dan al aan de andere
  kant, met zijn gezicht van het huis af, en de camera glijdt in `glij` seconden zacht van waar hij stond naar waar hij bij de
  uitgang hoort (`stadTrapCamX` in de camEase-keten, `stadTrapCamY` in `updateCamera`, met het vooruitkijken van de
  meekijkende camera erbij). Het beeld wordt daarbij iets donkerder (`dim`, niet zwart: je ziet waar je heen gaat), en in
  `in` seconden komt Amir terug. De wereld staat stil zoals bij de executie (`stadTrapFade`, op echte tijd).
- Niet in een gevecht: een levende vijand binnen 950 en hoogstens 150 hoger of lager (`stadInGevecht`; een vijand op een
  andere etage telt niet). Dan zie je "Niet nu". En niet zonder speer (in de hand of op de rug).
- Dichtbij gloeit de trap of de opening zacht warm op, en er staat een E met een pijltje. De uitgang aan de andere kant
  gloeit dan ook (iets zachter), met twee gouden pijltjes erboven die op en neer gaan (`stadTrapNabij`, `stadTrapUitTeken`):
  zo zie je voor je E drukt waar je uitkomt. De pijltjes komen na de personages (`stadTrapUitLaag`), zodat een vijand op
  het balkon ze niet afdekt. Hoe dichtbij Amir staat komt uit `playerX()`, niet uit `world`: tijdens het tekenen is
  `world` de camera, en met de meekijkende camera lag de gloed en de E anders een eind naast Amir.
- Vijanden gebruiken de trap nooit. Een balkon telt wel als vloer voor een vijand met `dak` (en de kruisboogbandiet kan nu
  ook `dak` hebben).
- Een galerij kan met `meer: [links, rechts]` (in Amir) langer zijn dan zijn huizen, zodat hij voor de trap langs loopt.
- De doek van een kraam vangt elke val op: nooit valschade.
- Op de telefoon staat de E-knop erbij zodra je bij een trap staat (`eNodig`). Ligt er iets anders voor E (een losse speer,
  een skelet, een wankelende schildbandiet), dan gaat dat voor de trap (`eSpeerIets`).
- Na de glijvlucht staat de camera precies op de nieuwe hoogte en plek (daarna neemt de gewone camera het naadloos over),
  en een terugstoot of renstoot loopt niet door op het balkon.
- Een kalebas met een hoogte (`hppotions: {x, y}`) komt in de stad op de vloer van die hoogte die het dichtst bij ligt,
  net als een vijand met `dak` (`stadDakPlek` in `resetHppotions`): de galerijen schalen mee met het scherm, een vaste x
  viel op een telefoon naast het dek.

Stad 2 tot en met 4 zijn de proefstukken; in de sandbox staat er een trap naast het hoge huis van **De stad**.

## De doorgang

`STAD_DOORGANG`, `stadDoorgangen`, `stadDoorgangBeeld`, `stadDoorgangFase`

Bij de opening in de leuning waar een stadstrap boven op een galerij uitkomt (`balkon: 0`) loopt het dek in beeld door,
de diepte in: zo lijkt het alsof je daar achter het huis langs kunt, naar de trap. Alleen beeld, lopen en E blijven zoals
ze zijn.

- **De vorm.** De vloer ligt strak tegen de muur van het huis (`q.ander`) en is daar recht; aan de open kant loopt hij
  naar achteren smaller (`smal`, achterin 0,65 van vooraan), en hij is `diep` (0,2 Amir) hoog in beeld. Langs de open kant
  staat een hekje dat kleiner en vager wordt, en over het uiteinde een kort hekje (`hek`, 0,6 van de breedte) dat bij het
  huis een opening laat: daar draait de vloer achter het huis weg.
- **De planken** komen uit `galerij.png` (het middenstuk, rijen `band`) en lopen in dezelfde schuine lijn door als op het
  dek ervoor (`helling`, 0,95 bronpx per rij). `stadDoorgangFase` zoekt waar in het middenstuk de muur valt, zodat de naden
  precies aansluiten. Naar achteren worden ze korter en smaller (verkorting, `planken`: hoeveel dek er in de diepte past;
  minder is grotere planken en minder ver weg).
- **Licht.** Zacht, want de stad heeft weinig schaduw: naar achteren wat donkerder, een smalle schaduw langs de muur,
  achterin bij de muur wat donkerder waar de vloer wegdraait, en de lucht erboven tussen de huizen een tikje (`steeg`).
- **Spiegelen.** Alles hangt aan `q.uit`: staat de trap links van het huis (opening rechts ervan), dan zit de muur links
  en het hekje rechts. Alleen de schuinte van de planken spiegelt niet, want die moet aansluiten op het dek.
- **Niet bij een balkon.** Een balkon hangt aan schoren tegen de muur; een vloer erachter zou zweven.
- **Een huis ervoor.** Hij wordt voor de gevels getekend (`stadDoorgangen` in `stadTeken`, voor `stadTrapAchter`): staat er
  een huis direct naast de opening, dan dekt dat hem af en zie je alleen de opening in de leuning.
- Het beeld wordt een keer per maat, kant en plankfase getekend en bewaard (`stadDoorgangCache`).

In de sandbox: **Doorgang** onder De stad, drie huizen met een galerij en twee trappen die erop uitkomen, een keer met de
opening links en een keer rechts van een huis.

## De leemmuur

`LEEM`, `leemMuurTeken` (in `drawClimb`)

Een terras met `look: 'leem'`: `terraces: [{r, l, h, look: 'leem'}]`. De botsing is precies die van een terras: de
wand houdt Amir en elke vijand tegen (regel 7), de bovenkant draagt, en levelcheck en de speelrobot rekenen er gewoon
mee. Alleen het tekenen is anders: een naadloze wand van leem (`design/stad/leem_tegel.png`, rijen om en om verschoven
en vast aan de wereld) met de kartels en balken erop (`leem_rand.png`, rij 68 is de looplijn, op de schaal van de gevel),
een donker verloop naar beneden, schaduwranden aan de zijkanten en een contactschaduw op de straat. Hij staat op de
straat (houdt op de grondlijn op); een buur van leem die even hoog of hoger is dekt een zijkant af.

Zo maak je een straat doodlopend (een hoge muur), een lage muur om op te springen, of een hogere wijk. Een gevel kan
erop staan (`terrainH`). Stad 2 heeft er een lage tussen de twee straten; in de sandbox onder De stad **Lage leemmuur**
en **Doodlopend**. Beide plaatjes zijn uit de gevel gemaakt (geen nieuwe art).

## De houten vloer

`look: 'hout'` (in `savanneLaag`), `design/stad/binnen/vloer_hout.png`

De vloer van een huis, om een huis met verdiepingen te bouwen: een zwevende laag met `look: 'hout'`,
`zwevers: [{r, l, h, onder, look: 'hout'}]`. De botsing is precies die van een zwever (zie `notities/savannelaag.md`): je
landt erop, loopt eronderdoor als er ruimte is (`CHAR_H`), en stoot er je kop aan. Getekend door `savanneLaag`, net als een
savannelaag, maar met de houten tegel: planken bovenop, een dikke plank en een rij balkkoppen eronder. De tegel (Grok, naadloos
gemaakt met twaalf balkkoppen) heeft de rijen van de grondrand: bovenvlak van rij 10 tot 95, de looplijn op 95, de voorkant
tot 305. Een zwevende houten vloer schaalt de tegel naar zijn eigen dikte (`h - onder`), zodat de balkkoppen altijd onderaan
zitten. Het plafond van de kamer eronder en de vloer van de kamer erboven zijn zo dezelfde plaat.

- Het plaatje zit in de stadsset (`stadLaad`, sleutel `hout`) en laadt mee zodra een level een houten vloer heeft
  (`stadLaadLevel`).
- Een vijand loopt erop zoals op elke zwever. Liggen er twee boven elkaar (vloer en plafond), dan staat hij op de onderste
  waar hij hoort: `vloerBij` kijkt na de oude regel (de hoogste laag) ook naar een lagere houten vloer. Een spawn met
  `vloer: 450` staat bij het begin op die hoogte (bandiet).
- In de Maker: **Vloer: hout** (Terrein, groep Stad, letter B; intern nog `balken`). Een blok boven de grondlijn wordt een
  zwever met deze look. In de sandbox onder De stad **Houten vloer**.
- De oude balkenvloer (`look: 'balken'`, een losse strook) is weg.

## Binnen: de binnenkant van een huis

`BINNEN`, `binnenBij`, `binnenEBij`, `binnenE`, `binnenKlem`, `binnenCamKlem`, `binnenVijandKlem`, `binnenAchter`, `binnenNa`,
`binnenLadder`, `binnenLaadLevel`

```
binnen: [{ gevel, r, l, deur, ramen: [{x, h}], palen: [{x, h}], ladders: [{x, van, naar, f}] }]
```

Elk huis met een binnenkant is een eigen strook ver van de straat (van `r` tot `l`, in Stad 7 op -20000, -30000 en -40000).

- **In en uit**: voor het deurgat van gevel `gevel` (`stadDeurMaat`, verdieping 0) staat een E; E en het beeld wordt even
  zwart (`BINNEN.fade`, via `stadTrapFade` met `binnen: true`: de camera springt mee, geen glijvlucht) en je staat binnen bij
  de boogdeur (`deur`, een wereld-x op de begane grond). E bij die deur en je staat weer buiten voor het deurgat. Niet in een
  gevecht (`stadInGevecht`), net als de stadstrap.
- **De ladder** werkt als de stadstrap: E bij de voet of bovenaan, het beeld dimt even en je staat aan de andere kant; niet
  in een gevecht. De voet staat op `x` op vloer `van`, de top leunt naar links (met `f` naar rechts) en `binnenLadder` geeft
  waar hij uitkomt: de rand van de vloer erboven hoort daar (in Stad 7 ligt die 125 voorbij de voet bij een verdieping van 450).
- **Vast in het huis**: Amir (`binnenKlem`, in plaats van de klif), de camera (`binnenCamKlem`) en de vijanden
  (`binnenVijandKlem`) blijven tussen `l` en `r`. Binnen geeft `endWall()` geen grens, anders hielden de botsingen van de
  vijanden ze tegen (het huis ligt voorbij de klif van de straat).
- **Vijanden**: een spawn in een huis komt pas als Amir in dat huis is, en dan meteen, op zijn eigen plek (`spawnPoint`
  duwt hem niet naar buiten beeld); dus allemaal tegelijk, al tijdens de fade.
- **Tekenen**: `binnenAchter` (voor de zwevers) tekent de binnenmuur (`binnen/wand.jpg`, getegeld en vast aan de wereld, tot
  het hoogste plafond; daarboven donker), een plint langs elke vloer, de ramen (`raam_1.png`), de gevorkte palen (`paal_1..5`,
  de vork en de voet op maat, de stam ertussen herhaald tot onder het plafond, `binnenPlafond`), de ladders (`ladder_1..3`) en
  de boogdeur (`deur.png`). `binnenNa` (na de zwevers, voor de personages) legt het schemer over alles (`BINNEN.donker`, de
  personages blijven helder), donkere zijmuren, en dan het licht: het glas gloeit, een lichtbundel valt schuin naar de vloer
  (`BINNEN.bundel`) met een lichtvlek, en stofjes zweven door de kamer (`BINNEN.stof`), zacht in het schemer en helder in een
  bundel. Buiten tekent hij alleen de E bij het deurgat.
- `levelcheck.py` kent de stroken (`binnen_strook`): wat erin staat is niet "voorbij het einde", en tussen de zwevers van twee
  huizen hoeft niet gesprongen te worden.

Stad 7: Binnen is het proefstuk (drie huizen: een zaal op palen, en twee met een verdieping en een ladder, een keer gespiegeld).
In de sandbox onder De stad: **Huis met binnenkant**.

## Straten en knooppunten (Sandville)

`straatRaster`, `straatUitgangen`, `straatKnoopX`, `straatUitgangBij`, `straatKnoopGa`, `straatKnoopToets`, `straatGevelX`,
`straatKnoopPoortTeken`, `straatKnoopVoor`, `straatPadZak`, `straatRasterKaart`, `SAND_STRATEN`, `STAD_5`, `sbKnoop`

Een uitbreiding van de straten van Oaktown (`STRATEN`, zie `notities/oaktown.md`): een veld `straten` met `raster: true`.
Alles van Oaktown blijft gelden (elke straat een eigen strook ver uit de buurt, `straatKlem`, `straatCamKlem`,
`straatVijandKlem`, het aanvullen, de spawns per straat), maar in plaats van hoekpoorten aan de uiteinden heeft een
straat knooppunten, met een poort de diepte in en een pad naar voren.

```
straten: { raster: true, start: 'kuiper', doel: 0, muur: 300,
           knopen: { nw: [0, 0], n: [0.5, 0], ..., zo: [1, 1] },
           lijst: [ { id: 'kuiper', naam: 'Kuiperstraat', knoop: ['o', 'm', 'w'], r: -200, l: -8200, m: -4200 }, ... ] }
```

- Een straat heeft twee of meer knopen: `knoop[0]` rechts (het begin), de laatste links (het eind), een middelste op `m`
  (of gelijk verdeeld). De knopen hebben een plek op de kaart: x naar rechts (oost), y naar beneden (zuid).
- **Welke uitgang waar.** Amir loopt naar links, dus de diepte in (de poort) is rechts af van zijn looprichting en naar de
  camera (het pad) links af. Een rij loopt naar het westen: poort noord, pad zuid. Een kolom loopt naar het noorden: poort
  oost, pad west. Per knoop komt er een poort of pad bij voor elke andere straat die daar die kant op verder loopt
  (`straatUitgangen`, uit de kaartplekken; niets met de hand). In Sandville: de noordrij en de oostkolom hebben alleen
  paden, de zuidrij en de westkolom alleen poorten, de twee middelste bij elke knoop allebei.
- **De uiteinden.** `muur` (px) is de breedte van een hoge leemmuur aan elk uiteinde; die staat gewoon als terras in het
  level (`look: 'leem'`, 1800 hoog, levelcheck weet dat een terras tegen het uiteinde van een straat doodlopend is). De
  poort van een eindknoop staat direct tegen die muur, de knoop (en het pad) op het midden van de boog (`straatKnoopX`).
- **De poort** is `poort_recht.png` op het vlak van de gevels, op de looplijn, op de schaal van `STRATEN.recht` (ongeveer
  zo hoog als een huis van drie). Hij schaalt mee met het scherm, de huizen staan op een vaste x: `straatGevelX` schuift
  per stuk straat tussen twee poorten het dichtstbijzijnde huis aan elke kant tegen de poort, schuift de rest alleen mee
  als hij anders overlapt, en houdt elk huis binnen zijn stuk (welk stuk volgt uit het ontwerpformaat, Amir 180). Zo
  valt er op geen schermmaat een huis over een poort; op 1920x1080 overlappen de huizen elkaar dan, zoals overal in de
  stad. `stadGevelMaat` geeft die x (`m.x`), dus galerijen, trappen, daken en vijanden op een dak gaan mee. Kramen,
  voetdecor en kalebassen schuiven niet: houd ze zo'n 300 px van een poort.
- **Het pad** is `kruis_voor.png` (het pad met de donkere, onscherpe voorgrondhuizen ernaast, randen in transparant), net
  onder de looplijn (`STRATEN.pad.zak`) en na de personages getekend, gecentreerd op de knoop. Daarbuiten blijft de
  gewone grond. In de plaat stond eerst een bordje met een straatnaam; dat is eruit geschilderd (de naam tekent het spel).
- **Kiezen.** Onder de boog (`poortVang` van de boogbreedte) pijl omhoog of E; bij het pad (`pad.vang` van de padbreedte)
  pijl omlaag of E. Staan er allebei, dan neemt E de poort (alleen dat bordje krijgt de E). Boven de poort en op het pad
  (zo laag als het beeld toelaat) een bordje `▲ Naam` of `▼ Naam`, goud als je erbij staat (`straatBordje`).
- **De wissel** is die van de stadstrap: `straatKnoopGa` zet `stadTrapFade` met `straat` en eigen tijden (`STRATEN.knoopFade`,
  donkerder dan de trap: `dim` 0,85). Midden in de fade doet `stadTrapStap` de boekhouding (`straatWisselBoek`, ook het
  aanvullen) en zet Amir bij dezelfde knoop in de andere straat, met zijn gezicht de kant op waar hij heen ging; de camera
  begint daar een stukje (`schuif`) achter zijn plek en glijdt mee (`stadTrapCamX`, binnen de nieuwe straat door
  `straatCamKlem`).
- **Niet in een gevecht**: `stadInGevecht`, "Niet nu". Met de pijltjes springt of bukt Amir dan gewoon (de hint komt wel),
  met E gebeurt er niets. Zonder speer: "Pak je speer eerst". Vijanden gaan nooit door een poort of over een pad.
- **De camera** zakt bij een pad tot `padZak` Amir (vanaf `padZie` Amir afstand, zacht), zodat je meer van het pad ziet
  (`straatPadZak` in de doelhoogte van `stadVloeren`).
- **De minimap** (`straatRasterKaart`, alleen op een laptop: `camTelefoon()`): een vierkant met de straten als lijnen, de
  knopen als stipjes, de huidige straat in goud, een bezochte licht, en een witte stip voor Amir die tussen de knopen van
  zijn straat schuift (op de x van de knopen, niet van r naar l).
- `doel: 0`: geen kills-doel en geen teller, het level eindigt niet (levelcheck: een level met `straten` heeft geen `ends`
  nodig). Een `start` in het level zou met `rand` de rechtergrens vlak achter de start leggen, midden in de eerste straat;
  zonder `start` begin je in het midden van de startstraat (in Sandville op het kruispunt).
- De leveldefinitie (`SAND_STRATEN`, `SAND_STAD`, `SAND_TERRAS`, `SAND_KALEBAS`, `SAND_SPAWNS`) is gegenereerd uit een
  beschrijving per straat (afstanden vanaf `r`), net als Oaktown; levelcheck leest alleen letterlijke waarden.

### Sandville per straat

Elke straat is 8000 px, met de leemmuur van 300 aan elk eind en knopen op het midden van de eindpoorten en op `m`.

| straat | kaart | uitgangen | opbouw | kalebas |
| --- | --- | --- | --- | --- |
| Kuiperstraat (start) | middelste rij | poort en pad bij elke knoop | rieten kraam onder een galerij (401), een doek | op de galerij |
| Weversstraat | noordrij | alleen paden | de stadstrap naar een balkon (401) | op het balkon |
| Zoutstraat | zuidrij | alleen poorten | over de daken (487) via de doek | op het laatste dak |
| Smedenstraat | westkolom | alleen poorten | de toren: galerijen 401 en 730, via de doek | op 730 |
| Pottenbakkersstraat | middelste kolom | poort en pad bij elke knoop | galerij via rieten kraam, een lage leemmuur (170) | geen |
| Leerlooiersstraat | oostkolom | alleen paden | een trap op een lange galerij (401, `balkon: 0`) | op de galerij |

Vijanden: alleen mensen (bandiet, schildbandiet, kruisboogbandiet, zweepman), drie per straat, een paar op een galerij,
dak of balkon. Daarbij stappen er een paar uit een deur (zie "Deuren"): twee bandieten na elkaar uit een huis in de
Kuiperstraat, een zweepman in de Weversstraat, en boven op de galerij (401) een schildbandiet in de Smedenstraat en een
bandiet in de Leerlooiersstraat. Geen bazen.

Een deur rekent met `m.x` uit `stadGevelMaat`, dus in een raster schuift hij mee met een huis dat opzij gaat voor een poort.

### Sandbox

Onder De stad, **Knooppunten**: **Poort**, **Pad** en **Kruising** zetten voor je uit een knoop in de straat waar je staat,
met een tweede straat die er naar het noorden (poort), het zuiden (pad) of allebei (kruising) vandaan loopt, een paar
huizen ernaast (die opzij schuiven voor de poort) en de minimap. **Weg** haalt het weg.

## Deuren

`STAD_DEUR`, `stadDeurMaat`, `stadDeurVloer`, `stadDeurKlaar`, `stadDeurUpdate`, `stadDeurVoorTeken`, `stadDeurReset`, `stadDeurenBoven`

Een spawn met `deur: {gevel, verdieping}` stapt uit een deur van een huis: `gevel` is de index in `stad.gevels` (zoals bij een
galerij of trap), `verdieping` 0 de straat (het deurgat van `gevel.png`), 1 de eerste verdieping, en zo verder tot onder het dak.

```
spawns: [ {x: -1100, k: 'bandiet', deur: {gevel: 0, verdieping: 0}},
          {x: -1100, k: 'schildman', deur: {gevel: 0, verdieping: 1}} ]
```

- **Wanneer**: zodra de deur in beeld is (zijn midden `STAD_DEUR.marge` binnen de rand, met de camera die vooruitkijkt) en Amir
  binnen de triggerafstand van de vijand. Geen zegel of rune: een deur hoort bij het huis, en zo hoeft een level er niets voor te
  leggen. Meerdere spawns in dezelfde deur komen een voor een, `tussen` (1,1 s) na elkaar, en hun beurt telt alleen af als Amir in de
  buurt is (net als `poortWacht`). Een deur gaat per potje een keer open; `stadDeurReset` (in `restart`) sluit hem weer.
- **Waar**: precies in het gat (`stadDeurMaat`, met de schermmaat, want de huizen schalen mee): de spawner zet hem op `sp.x` net als
  bij een poort, en zonder wachten op zicht (`zichtZet`, zoals een poort). Het donker van het gat (`kleur`, egaal `rgb(38,24,22)`)
  ligt nog `uit` (0,9 s) over hem en vervaagt (`stadDeurVoorTeken`, na de vijanden, naast `poortVoorTeken`): hij stapt uit het donker.
- **Op een verdieping** staat in `gevel.png` een raam. Daar tekent `stadTeken` het deurgat van de begane grond (de latei, de posten en
  het donker, `latei` en `posten`) iets kleiner (`boven`, 0,9) in de plaats van het raam, met de drempel op de vloer en de bovenkant
  onder de balkenrij. Alleen een verdieping met een deurspawn krijgt die deur (`stadDeurenBoven`).
- **Een deur op elk huis**: elk huis heeft op de straat een houten deur, ook zonder deurspawn; die is dicht. Een open
  deur is de uitzondering: per huis vast (de seed van de stad en de index, `stadDeurVanzelfOpen`) staat zo'n een op de zeven
  open (`STAD_DEUR.openKans`, 0,15), op het laatste frame. Een deur met een spawn volgt gewoon zijn eigen staat hieronder.
  `warmBouw` laadt de deurframes daarom in elk level met gevels.
- **De houten deur**: in elk gat met een deurspawn (straat en verdieping, `stadDeurenAlle`) hangt de houten deur uit de rotswand
  (`design/deur/`, de frames van `DEUR`), getekend in de ruimte van de gevel (`stadDeurPlaatTeken`). Zijn kozijn (canvas-x 101 tot 351,
  de voet op 446) valt op dezelfde maat in bronpx op de posten en de latei van `gevel.png`: `plaatX` (247) is waar het canvas begint,
  de voet valt op de onderrand. Dicht tot de deur opengaat, dan de 20 frames op `DEUR.fps` met op het eind de klap (`deurSlamSpeel`,
  een kleine shake `schok`), en daarna blijft hij open. De eerste vijand wacht tot de deur open is (`deurWacht` begint op de duur van
  de frames). Een gespiegeld huis spiegelt de deur mee, met het scharnier rechts. Het grijze hout krijgt een warme tint (`warm`, multiply, een keer per frame in
  `stadDeurWarm`), de latei van de gevel valt over de bovenbalk van het kozijn met een zachte schaduw eronder, zodat de deur in de
  leem zit, en het donker over wie eruit stapt ligt alleen in de opening van de open deur (`opening`, via `stadDeurMaat(d, scale, gat)`). `laadLevel` laadt de frames in een stadslevel met
  een deurspawn.
- **De vloer**: op een verdieping komt hij op de galerij of het balkon op die hoogte voor de deur (`stadDeurVloer`, via
  `stadVloerBij`); de spawner krijgt dan `dak` met die hoogte en de rest gaat zoals bij een vijand op een galerij. Zonder vloer komt hij
  niet (`deurGeen`), en ook niet als zijn soort geen galerij kent: op een verdieping alleen `bovenSoorten` (bandiet, schildbandiet,
  kruisboogbandiet en de slangen). Regel 7 en de treden blijven gelden: de rand van de galerij houdt hem tegen.
- **Nooit**: een baas (panter, `boss`, regel 12) of hyena; die spawns tellen de deur niet (`stadDeurTelt`). `levelcheck.py` (regel
  `deuren`) meldt een baas in een deur, een gevel of verdieping die er niet is, een soort die op een verdieping niet kan, en een deur op
  een verdieping zonder galerij op die hoogte langs dat huis als FOUT, een hyena als LET OP.
- Het veld heet `deur` op een spawn; `level.deur` is iets anders (de houten deur in de rotswand, `deurReset`, `sbDeur`).

Geen level van een episode of bestaand testlevel heeft een deur. In de sandbox onder De stad: **Uit de deur** (een bandiet uit het
deurgat van het eerste huis) en **Uit de deur boven** (uit een deur op de eerste verdieping, op de galerij); elke klik zet de deur
opnieuw open (`sbStadDeur`). In de Maker nieuwstijl: Decor, Huizen, **Deur** (zie "Deuren" in `notities/maker.md`).

## Het plein

`STAD.plein`, `stadPutMaat`, `stadPleinPoortMaat`, `stadPleinWandTeken`, `stadPleinPoortTeken`, `stadPutTeken`, `stadZachteSchaduw`, `sbPlein`

Een open plein in de stad, als arena voor een baas. Stad 6 (Het plein) is het proefstuk; in de sandbox onder De stad de
knop **Het plein**. Drie nieuwe velden in `stad`, en een grondsoort:

```
stad: { ..., pleinwanden: [{x, f}], putten: [{x, f}], pleinpoorten: [{x, f, hek}] }
grondSoort: [{van, tot, soort: 'plein'}]
```

- **De vloer** (`design/stad/plein.png`): versleten zandstenen platen met zand in de naden, een strook `grondSoort`
  met soort `plein`. De tegel is een Grok-overschildering van de straat, daarna rij voor rij teruggezet op de rijen van
  `EDGE` (1572x335, looplijn 95), met het alfa van `straat.png`. Net als de straat niet in `klein/`.
- **De pleinwand** (`pleinwand.png`): een lage leemwand met vijf bogen. Hij staat achteraan: kleiner (`amir: 250`, de
  bogen ongeveer 1,1 Amir), zijn voet `lift` (0,13 Amir) boven de looplijn en met `nevel` (0,22) naar de nevelkleur
  voorgebakken. Getekend voor de gevels, dus een huis staat ervoor. `x` is het midden, twee naast elkaar (een gespiegeld)
  geven een lange arcade. Er botst niets.
- **De put** (`put.png`): leemrand met een houten balk en een katrol. `x` is het midden. De rand (`rand`, 0,47 Amir)
  is een dunne trede zoals een kraamtafel (`stad: 'putrand'`), de balk (`balk`, 1,03 Amir) haal je vanaf de rand met een
  sprong (`stad: 'putbalk'`). Voor vijanden is het geen vloer, net als de kramen.
- **De poorten** (`pleinpoorten`): de rechte poort van de straten (`STRATEN.recht`, dezelfde maat als in Oaktown), als decor
  op het vlak van de straat, `x` is het midden. Met `hek: 'dicht'` staat het valhek (`HEK.src`) tot op de grond in de boog,
  met `hek: 'open'` is het voor `STAD.plein.hek.open` van de opening opgetrokken; het hek wordt op de vorm van de boog
  afgeknipt. De poort en het hek doen nog niets: geen E, geen botsing en geen animatie. Met `uit: true` is het de
  uitgang van de baas: Brutus (`notities/brutus.md`) zet hem dicht bij de start en open als hij sterft (in een klap,
  zonder takelen). De wanden van het gevecht komen uit `brutus.van` en `brutus.tot`, niet uit de poorten.

## De luifel bij de put

`STAD.plein.luifel`, `stadLuifelMaat`, `stadLuifelWorp`, `stadLuifelStap`, `stadLuifelVx`, `stadLuifelTeken`, `sbluifel`

Een schuine doek aan een paal (`design/stad/luifel.png`, uit een Grok-plaat: het doek korter gemaakt en schuiner gezet, de
paal recht gehouden). Hij hoort bij een put: `putten: [{x, luifel: 'r'}]` zet hem rechts van de put (`'l'` links), met de
paal `af` (2,3) Amir van het midden van de put en het lage eind `eind` (1,5) Amir boven de grond. Zo zit hij in Amir
gerekend altijd even ver van de balk: vanaf de balk te halen (0,5 Amir omhoog), vanaf de straat niet. Hij is aan de put
gekoppeld en niet aan de toren, omdat de toren van een pleinpoort met de schermgrootte mee schuift en de put niet.

- **Botsen**: de bovenkant van de doek (`opp`, bronpunten) wordt in `stadPlats` zes smalle dunne stukken, elk op zijn eigen
  hoogte (`stad: 'luifel'`). Alleen het onderste deel is vanaf de balk te halen; de kant bij de paal hangt te hoog.
- **De worp**: wie erop landt wordt meteen weggeworpen (`stadLuifelWorp`, vanuit de landing naast de kraamdoek), erop staan
  kan niet. Omhoog `worp.vy` x jumpV, opzij `worp.vx` Amir per seconde van de paal af, als eigen vaart (`stadLuifelVx`) die
  blijft tot hij weer staat. Geen valschade. De doek buigt mee in stroken (`dip`, `duur`), net als de kraamdoek.
- **De paal**: staat hij voor de toren van een pleinpoort, dan hangt hij daaraan. Op een klein scherm staat de toren verder
  weg; dan loopt de paal door tot de grond (`stadLuifelTeken`).
- **Stad 6**: de put staat op -3200 met de luifel rechts, tegen de toren van de rechterpoort, met tonnen eronder
  (`notities/tonnen.md`). Amir begint net binnen de rechterpoort (-2500, `rand` 800 zodat de rechtergrens gelijk blijft)
  en loopt dus langs de put. Op een telefoon (852x393) springt Amir verhoudingsgewijs verder (lopen is 330 wereld-px per seconde
  op elk scherm): daar spring je recht omhoog met een kort tikje naar rechts, anders ga je onder de doek door.
- **Zonder put**: `stad.luifels: [{x, kant}]` zet dezelfde luifel neer zonder put eronder. `x` is waar het midden van de
  put zou staan en `kant` is wat `luifel` bij een put is, zodat hij net zo ver van de toren hangt (`stadLuifelPlats` doet
  de botsing voor allebei). Zonder put en balk komt Amir er vanaf de grond niet bij (het lage eind hangt 1,5 Amir hoog,
  de sprong haalt zo'n 0,8). Stad 6 heeft er een op -6000 met `kant: 'l'`, gespiegeld tegen de toren van de linkerpoort, met de stapel tonnen eronder
  die Nyundo in de opening kapotslaat.
- **Sandbox**: onder De stad de knop **Luifel**: het plein met de put zo neergezet dat de paal tegen de toren staat.

## Geen outline op de stadsplaatjes

Een donkere outline om de stadsplaatjes is geprobeerd (2 november 2026) en weer teruggedraaid: Tom vond het lelijk.
De stadsplaatjes hebben dus geen extra outline. Niet opnieuw toevoegen zonder dat Tom erom vraagt.

## Nog niet

- Een subtiele gloed om de personages (in de mockups hielp dat tegen de bruine muren), en een kleine set (`klein/`).

## De huizenrijen in de verte als strook (`stadRijStrookTeken`, `STAD_STROOK`, `STROOK`)

`stadAchter` tekende de drie achterrijen huis voor huis: per huis een save, een spiegeling en een stapel strookjes
muur tot de grond, zo'n 66 tot 150 tekenopdrachten per beeld. Op een telefoon was dat twee derde van elk beeld
(gemeten in Stad 6 op 852x393 met een vier keer tragere CPU: 333 ms per beeld, zonder de achterrijen 117 ms).

Nu tekent `stadRijStrookMaak` elke rij een keer in een eigen canvas op schermresolutie (`DPR`), met de muur onder de
huizen `STROOK.diep` schermhoogtes diep, en `STROOK.marge` schermbreedtes extra aan elke kant. Per beeld zet
`stadRijStrookTeken` alleen het stuk dat in beeld valt neer, op hele schermpixels en zonder gladmaakfilter (het is 1 op
1, dus er valt niets te verzachten, en het kopieren is zo veel goedkoper). Klimt de camera dieper dan de strook, dan
herhaalt hij de onderste verdieping. Een nieuwe strook komt er als de rij uit de strook schuift, `DPR` verandert, het
level wisselt, of de maat (de meekijkende camera zoomt) `STROOK.rust` beelden vast staat op een andere waarde; tot dan
blijft de oude verschaald staan. `laadVrij` gooit de stroken weg in een level zonder stad (samen zo'n 30 MB).

Gemeten (zelfde opstelling, mediaan per beeld): Stad 1 van 450 naar 167 ms, Stad 6 van 367 naar 150 ms, Stad 6
lopend van 533 naar 250 ms. Het beeld verschilt alleen in de randen van de huizen, omdat ze nu op hele pixels staan in
plaats van een fractie ernaast: `node tools/beeldgelijk.js --vlag STAD_STROOK` zet de oude weg (`STAD_STROOK = false`)
ernaast.

## De speer op een dak of galerij

`javFloor` slaat dunne platforms over (richels, de speer zelf), maar de platforms van de stad (`p.stad`: dak, galerij,
balkon, putrand, putbalk) tellen voor een speer als vloer zodra hij erboven zit (`h >= p.topH`). Zo landt een
geworpen of vallende speer erop in plaats van door alle lagen tot de straat te zakken, en van onderen vliegt hij er gewoon
doorheen, net als Amir. De doek (`veer`) en de luifel tellen niet: die werpen meteen terug. Een kraam (`tafel`,
`riet`) telt ook niet: een speer vliegt over of langs een kraam tot de straat, anders viel een vlakke worp op straat al
na een paar passen op de toonbank.

## De stoep: een strook straat over de voet van de huizen

`STAD_STOEP`, `stadStoep`, `stadStoepH`, `stadVoorTeken`. De gevels en poorten staan met hun voet op de looplijn
(`EDGE.walk`, rij 95 van de straattegel), terwijl de straat in de tegel vanaf rij 48 naar achteren doorloopt. Daardoor
stond wie op straat loopt precies op de muurvoet en leek het, vooral op een groot Formaat, of hij op het huis stond of
ervoor zweefde. Na de gevels, galerijen en poorten (en voor de kramen, de put en het voetdecor, die nu in
`stadVoorTeken` staan) tekent `stadStoep` de straat over hun voet heen, tot `diep` (0,16 Amir, minstens de straat
die al in de tegel zit) boven de looplijn: de tegelrijen van `van` (46, de achterrand) tot de looplijn, over die diepte
uitgerekt, met een contactschaduw op de nieuwe muurvoet. Zo staan de huizen een stuk naar achteren, met hun onderkant
achter de vloer, en ligt de straat voor ze open; omdat `diep` in Amir is, groeit die open vloer mee met het Formaat.
Niet over een ravijn, en een leemmuur (`look: 'leem'`, een echt terras) komt er gewoon overheen. Alleen het beeld:
daken, galerijen, deuren en de looplijn houden hun hoogte. Het voetdecor staat niet op de nieuwe muurvoet maar op de stoep
ervoor (`STAD.voet.stoep`, 0,4 van `stadStoepH` boven de looplijn), met een zachte contactschaduw (`STAD.voet.schaduw`):
op de muurvoet zelf leek het boven de straat te hangen.
