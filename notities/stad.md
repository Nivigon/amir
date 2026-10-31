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

- Het dak is beloopbaar: een dun platform op `dakLoop` (de onderkant van de kartels), over de muur (`muur`).
  Hoogtes: 1 hoog 487, 2 hoog 816, 3 hoog 1145, 4 hoog 1474 (`stadGevelH`). Een verdieping is 329.
- Een gevel is decor op het vlak van de straat: Amir en de vijanden lopen ervoor langs, er botst niets.
- Contactschaduw aan de voet (`STAD.schaduw`), zodat de muur niet als een liniaal op de straat staat.
- Het deurgat is donker. De rechthoek staat in metadata.json (`deurgat`): daar komen later losse deuren.

## Galerijen

Een houten looprichel langs een gevel, 9-slice uit `galerij.png` (links, het midden zo vaak als nodig, rechts).
`van` en `tot` zijn de index van een gevel, zodat hij altijd precies over die huizen loopt, ook als de breedte
meeschaalt. `h` is de hoogte van het dek (zonder `h` de tweede verdieping, 730, `stadVerdieping(2)`; de eerste is 401). Het dek is een dun platform: van
onderen spring je erdoorheen. De reling staat achteraan, Amir loopt ervoor.

Amir springt 208 hoog. Een verdieping (329) is dus te hoog om zomaar te halen: een route naar boven gaat via de
kraam, de doek, of galerijen die tussen twee verdiepingen hangen (Stad 1 heeft er drie boven elkaar langs de toren).

## Vijanden op een galerij of dak

Een galerij en een dak zijn ook de vloer van een vijand: `vloerBij` vraagt het aan `stadVloerBij` (na de zwever), dat
in `stadVloeren` de daken en galerijen kent (gecachet per schermmaat en level). Wie binnen hun rand staat en niet meer
dan `STAD.vijandMarge` (30) onder de looplijn, heeft die als vloer. Zo werkt de rest vanzelf: `dropAhead` houdt hem bij
de rand tegen (zoals een ravijnrand, regel 7), en `banZelfdeHoogte`, de kooiman/schildman en het zicht vergelijken de
vloer onder Amir op de galerij goed. Wie eronder loopt blijft op de straat (de marge is klein, en een dun platform is
geen muur in `blocksMonster`). De tafels, het rieten dak en de doek tellen niet mee.

Een spawn met `dak` staat erop (bandiet en schildbandiet, `stadDakPlek`): `dak: 401` kiest de galerij of het dak op
die hoogte dat het dichtst bij x ligt, `dak: true` het hoogste. Zijn x schuift ruim binnen de rand, want de huizen en
galerijen schalen mee met het scherm en een vaste x kan op een andere maat net naast een dak vallen. Een hyena komt
van de rand van het beeld en kent dit niet. In de sandbox: **Bandiet op de galerij** onder De stad.

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

## Nog niet

- Deuren in de deurgaten, en vijanden die uit een deur komen.
- De trap in de Maker.
- De Maker: galerijen en trappen als gereedschap. De leemmuur staat er al in (stand Stad, Terrein, **Muur van leem**),
  de straat als strook grondsoort (**Grond: straat**, zie `notities/grondsoort.md`), en gevels, kramen, voetdecor en het
  paleis onder Decor (zie "De losse stukken van de stad" in `notities/maker.md`); het plan voor de rest staat in
  `notities/plan-stad-maker.md`.
- Een lift (een takel) die zich naar de rand van een galerij voegt: het plateau heeft een vaste breedte, de galerij
  schaalt mee. In Stad 1 overlapt het plateau het eind van de galerij op een laptop; op een kleine telefoon is het
  een korte sprong opzij.
- Een subtiele gloed om de personages (in de mockups hielp dat tegen de bruine muren), en een kleine set (`klein/`).
