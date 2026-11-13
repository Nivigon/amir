# De stad: een Sahelstraat van leem

`STAD`, `stadAan`, `stadLaad`, `stadLees`, `stadPlats`, `stadAchter`, `stadTeken`, `stadVeer`, `stadSprong`

Een level met het veld `stad` speelt in een drukke straat van een Sahelstad, overdag (uitzicht `stad_dag`).
De onderdelen staan in `design/stad/`, met alle maten in `design/stad/metadata.json`. Stad 1 (de episode Test levels stad, eerst Test 59) is het proefstuk;
in de sandbox onder Terrein de knoppen **De stad** (Neerzetten, Weg).

```
stad: { paleis, seed, gevels: [{x, hoog, f, soort}], galerijen: [{van, tot, h}],
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

### Huizen tegen elkaar

`aan` in een gevel, `stadAanVan`, `stadGevelX`, `stadGevelXCache`; in de sandbox onder De stad **Huizen tegen elkaar**

Een huis schaalt mee met het scherm (zijn breedte hangt aan Amir), maar zijn `x` ligt vast. Twee huizen die op de laptop
(Amir 180, een muur van zo'n 500) net aansluiten, overlappen op 1920x1080 en staan op een telefoon (Amir 98, een muur van
zo'n 270) ver uit elkaar. Daarom staan de huizen in De Gouden Poort zo'n 900 uit elkaar: dat is de marge waarbij ze op geen
scherm over elkaar schuiven.

Met `aan` rekent het spel de plek van een huis op elk scherm opnieuw uit (`stadGevelX`, in `stadGevelMaat`): zijn muur
sluit aan op de muur van het vorige huis in de lijst, het huis rechts ervan.

- `aan: true`: strak ertegen, de muren raken elkaar.
- `aan: 0.5` (een getal): een steeg van zoveel Amir ertussen. Die schaalt mee, dus op een telefoon is hij net zo smal
  ten opzichte van Amir als op de laptop.
- De `x` van een huis met `aan` telt in het spel niet. Zet er wel de plek op de laptop neer: de tools (levelcheck) en
  `stadPlats` (welke daken in de buurt zijn) lezen hem nog.
- Een rij kan zo lang zijn als je wilt: het eerste huis zonder `aan` is het anker op zijn vaste `x`, de rest hangt eraan.
  Op een groter scherm groeit de rij dus naar links; laat er voor het volgende vaste huis wat ruimte, of geef dat ook `aan`.
- Galerijen, trappen, daken, deuren en vijanden op een dak lopen mee, want die lezen allemaal `stadGevelMaat`.
- In een stadje met een raster (`straatRaster`) doet `aan` niets: daar schuift `straatGevelX` de huizen al naar de poorten.
- De Maker nieuwstijl kent `aan` nog niet; geen bestaand level gebruikt het.

**De muur van een hoger buurhuis** (`stadMuren`, `stadMuurBlok`, `STAD.muurKier`): een dak is een dunne vloer zonder muren,
dus van een laag dak liep Amir dwars door de muur van het hogere huis ernaast en viel hij binnen dat huis naar de straat.
Staan twee huizen tegen elkaar (`aan: true`, of een kier tot `muurKier` Amir, 0,3), dan is de muur van het hogere nu een
wand van het lage dak tot het hoge: klimmen kan er niet, een sprong of springdoek over het hoge dak heen wel. Alleen vanaf
de kant van het lage dak; wie voor de gevel van het hoge huis staat (een galerij, een trapbalkon) merkt er niets van, en
binnen ook niet. Een steeg (`aan: 0.8` en meer) blijft een steeg waar je in valt.

Let op bij een nieuw level: een laag dak tussen twee hogere huizen die er strak tegen staan is nu een put. Een verdieping
(329) is hoger dan een sprong, dus geef zo'n dak een uitweg (een luifel, een trap) of zet er een steeg naast. Alleen Stad 9
heeft zo'n dak nog (huis 2), met de springdoek op de linkermuur van huis 1. Roofs 7 kreeg daar een steeg; in Roofs 2 is
huis 2 toen 3 hoog geworden, even hoog als zijn buren, omdat je er anders niet meer af kwam.

## Huistypes

`STAD.gevelSoort`, `stadGevelG`, `stadGevelDelen`, `stadSoortLaad`, `tools/gevel_soorten.py`

Naast `gevel.png` zijn er negen andere huizen, elk met een eigen plaat in `design/stad/`. Je kiest het type met `soort`
in een gevel: `gevels: [{x, hoog, f, soort}]`. Zonder `soort` blijft het de oude gevel, dus geen bestaand level verandert.

- `relief`: het reliefhuis, licht zand met rode en blauwe versiering rond de deur en de ramen (Hausa-stijl).
- `koopman`: het koopmanshuis, warm rossig zand met een houten erker op de eerste verdieping.
- `pilaren`: het pilarenhuis, donkerder leem met staande pilaren met punten erop en bundels stokken (Djenne-stijl).
- `vervallen`: het vervallen huis, kale baksteen, dichtgemetselde ramen, een hangend luik, een afgebrokkelde dakhoek. Nog
  bewoonbaar: het dak is beloopbaar.
- `toren`: het torenhuis, een ronde toren aan de rechterkant die een halve verdieping boven het dak uitsteekt. Het dak is
  beloopbaar, de toren is decor (wie op het dak staat, staat ervoor).
- `ruine` en `ruine2`: twee ruines, de ene met gaten in de bovenste verdiepingen, de andere met een V in het midden en een
  balk over het gat. Door de gaten zie je de lucht (`gaten` in het script: elk wit vlak in de muur wordt doorzichtig).
  Een ruine heeft **geen beloopbaar dak** (`ruine: true`, `stadGeenDak`): geen vloer in `stadPlats`, `stadVloeren` en
  `mkStadVloeren`, en geen kartels. Zet er dus geen galerij, trap, ton of vijand op het dak.
  In het deurgat staat geen houten deur en geen gordijn: het is leeg en donker.
- `winkel` en `winkel_dicht`: het winkelhuis, een brede lage opening met een luik op een stok, een rieten matje erboven en
  een leembank als toonbank; open of met het luik dicht. De twee platen liggen precies over elkaar. De winkel staat **op de
  plek van de deur**, want naast de deur paste hij niet in de breedte van een huis (`geenDeur: true`, `stadGeenDeur`): geen
  houten deur, geen gordijn, geen binnenkant en geen vijand uit de deur (`stadDeurMaat` geeft null).

De muren blijven zandkleurig, elk met een eigen tint (`zand` in `tools/gevel_soorten.py`, ten opzichte van `gevel.png`).
Grok gaf wit, roze en chocoladebruin: dat werd een kleurenfestival. De kleur in de straat hoort van doeken, was en
vaandels te komen (A3 in `notities/stad-verbeteren.md`), niet van de muren.

Elke plaat heeft dezelfde maat als `gevel.png`: 970 breed, de muur van x 44 tot 922, het midden van het deurgat op x 473,
en de verdieping (417) en de begane grond (508) even hoog. Het dak mag hoger zijn (puntige kartels), maar de looplijn
(`dakAchter`) ligt net zo ver boven de onderkant van het dak. Zo liggen daken, verdiepingen, galerijen, trappen en deuren op
precies dezelfde hoogte als bij een oud huis, en kun je de types vrij door elkaar zetten.

- **Twee soorten verdieping.** Elke plaat heeft naast `ver` ook `alt`: de bovenste verdieping uit de Grok-plaat. De eerste
  verdieping is `ver` (de erker, de stokbundels), alles erboven `alt` (`stadGevelDelen`). Een koopmanshuis van vier hoog
  heeft dus een erker en daarboven twee gewone ramen.
- **De ruine andersom.** Bij een ruine is het dak de hele ingestorte verdieping (600 bronpx hoog). Daaronder eerst `ver`, de
  verdieping met de gaten, en pas daaronder `alt`: de dichte verdieping van het vervallen huis, die het script onderaan de
  plaat van de ruine plakt. Zo staan er bij drie of vier hoog nooit twee keer dezelfde gaten boven elkaar, en wordt de
  ruine naar beneden toe heler. Een ruine van een hoog is de ingestorte verdieping op de begane grond.
- **De deur.** Voorlopig krijgt een huistype dezelfde houten deur als een oud huis, dicht of (soms) open, geschaald op
  zijn eigen deurgat (`deur` in `STAD.gevelSoort`, het gat ten opzichte van dat van `gevel.png`; ook `stadDeurMaat`
  rekent ermee). De latei van `gevel.png` komt er niet overheen, want elk type heeft zijn eigen kozijn.
- **Lui geladen.** Een plaat laadt pas als een gevel in het level hem gebruikt (`stadSoortLaad`, vanuit `stadLaadLevel`). Tot
  hij binnen is, tekent `stadGevelG` de oude gevel.
- **De platen maken.** `tools/gevel_soorten.py` maakt ze uit de Grok-platen in `design/stad/bron/` (`gevel_<soort>_grok.jpg`):
  wit weg, een strook kale muur eruit (links een smalle zodat de deur op x 473 valt, rechts een brede), en elke band op zijn
  maat. Het print de maten voor `STAD.gevelSoort` en zet ze in `metadata.json` (`gevel_soorten`). Daarna `gen-klein.py` en
  `gen-offline-manifest.py`.
- **Sandbox.** Onder Terrein, bij De stad, de knop **Nieuwe huizen**: het vervallen huis, het torenhuis, de twee ruines en het
  winkelhuis (open en dicht), elk in meer hoogtes, ook een verdieping, met een oud huis als maat. De knop **Huistypes**: een
  straat met de oude gevel en de drie eerste types door elkaar,
  in elke hoogte, met een galerij over een oud huis en een reliefhuis. Daarnaast **Dichte straat**: tien huizen muur
  tegen muur (10 bronpx over elkaar, de randen zijn niet kaarsrecht). De breedte van een huis schaalt mee met het scherm,
  dus de knop rekent met de schaal van dat moment.
- **In de Maker.** Een gevel heeft in het paneel naast Hoogte de keuze **Type** (`MK_GEVEL_TYPES`, `mkGevelSoort`): Oud
  huis, Reliefhuis, Koopmanshuis, Pilarenhuis, Vervallen huis, Torenhuis, Ruine met gaten, Ruine met V, of het Winkelhuis
  open of dicht. Het grid tekent het gekozen type, en `mkNaarLevel` zet `soort` in de gevel.
- **Een type erbij.** Een Grok-plaat in `design/stad/bron/`, een regel in `SOORTEN` van `tools/gevel_soorten.py` (de maten
  nameten op een raster; staat de deur links van het midden, dan plakt een negatieve knip kale muur bij in plaats van eruit
  te halen, en `schaal` maakt een plaat met te lage verdiepingen eerst groter), het script draaien, de uitvoer in `STAD.gevelSoort` en een regel in `MK_GEVEL_TYPES`, `KLEIN_FAM`
  en de lijst van `gen-klein.py`.
- Nog niet: de verre rijen achter de straat (`STAD.rijen`) blijven de oude gevel.

## Balkon

`STAD_BALKON`, `stadBalkonMaat`, `stadBalkonTeken`, `tools/balkon_knip.py`

Een ingebouwd balkon in een gevel, plat: er steekt niets uit, de diepte komt van de schaduw en van wat je erdoor ziet.
In een gevel: `balkon: 'nis'`, `'hoekL'` of `'hoekR'`, en `balkonV` de verdieping (1 = de eerste, standaard de bovenste).
Een huis van een hoog heeft geen balkon, een ruine ook niet, en een torenhuis geen hoekbalkon (daar staat de toren).

- **De nis** (`nis`): midden in de gevel, op de plek van het raam. Een donkere achterwand met schaduw bovenin en langs een
  zijwand, een dichte houten deur achterin (`STAD_BALKON.deur`, kleiner dan een voordeur, warm gekleurd door
  `stadDeurWarm`), een houten latei over de nis en de balustrade gelijk met de gevel.
- **De hoek** (`hoekL`, `hoekR`): de hoek van het huis is op die verdieping uitgespaard (een clip met `evenodd` over de banden),
  dus je kijkt erdoorheen naar de stad erachter. Een strook muurdikte langs de binnenrand, een plafondje, een latei en voorin de
  smalle balustrade. Op een gespiegeld huis blijft `hoekR` rechts in beeld.
- **De vloer** is de balkenrij van het huis zelf (`STAD_BALKON.vloer`): de vloerrand met balkkoppen uit de Grok-plaat is weg,
  anders staan er twee balkenrijen boven elkaar.
- **De platen** knipt `tools/balkon_knip.py` uit `design/stad/bron/balkon_grok.png`: de balustrade van de voorkant
  (`balkon_voor.png`) en van de smalle zijkant (`balkon_zij.png`). Ze laden pas als een gevel een balkon heeft (`stadSoortLaad`).
- **Sandbox**: onder De stad de knop **Balkons**: de nis en de hoek, links en rechts, op verschillende verdiepingen en types.
- **In de Maker**: bij een gevel de keuze **Balkon** (geen, de nis of de hoek links of rechts, op de bovenste of de eerste
  verdieping; `MK_BALKONS`).
- Met `stad.accenten` kiest het spel ook zelf balkons (zie "Accenten").

## Accenten

`STAD_TAKEL`, `STAD_RAMEN`, `STAD_ACCENT`, `stadAccenten`, `stadTakelTeken`, `stadRamenTeken`, `tools/takel_knip.py`,
`tools/ramen_knip.py`

Losse stukken die een huis anders maken zonder nieuwe gevelplaat (D2 in `notities/stad-verbeteren.md`).

- **De takel** (`takel: 'l'` of `'r'` in een gevel): een ruwe stam die op de bovenste balkenrij uit de zijkant van het huis
  steekt, met een schuine tak eronder, een katrol en een mand. De mand slingert om de katrol op dezelfde wind als de
  deurgordijnen (`gordijnWind`, de sandboxknop Wind): de vlagen van het spel (`windAt`) en de storm van het weer, bijna stil
  ertussen, verder uit bij een vlaag, elk huis in
  een eigen ritme. De stam begint op de muur van zijn eigen huistype (`STAD_TAKEL.muur`, gemeten op de platen; de oude
  `STAD.gevel.muur` liet een spleet, bij het pilarenhuis 15 px), steekt er `inMuur` in en loopt daar donker uit (`inzak`).
  De stam is een smalle vloer (`STAD_TAKEL.loop`, `stadTakelVloer`, in `stadPlats` en `stadVloeren`): van de muur tot net
  voorbij de katrol, een stapje onder het dak, dus je loopt van het dak zo de balk op en aan het eind val je eraf. Een vijand
  op het dak mag er ook op; een spawn met `dak` komt er niet op terecht. De mand is decor. Staat er aan die kant een buurhuis te dichtbij (`STAD_TAKEL.ruimte`),
  dan geen takel; ook niet op een ruine, en niet aan de torenkant van het torenhuis. `tools/takel_knip.py` knipt de arm en
  de mand uit `design/stad/bron/takel_grok.png` (de muurstrook links gaat eraf). In de Maker de keuze **Takel**.
- **Andere ramen** op het oude huis: zes stukken muur met een ander raam (spitsboog, doek over de vensterbank,
  dichtgemetseld, luiken half open, traliewerk, pot op de vensterbank), over het raam van `gevel.png` gelegd
  (`STAD_NACHT.ramen.gevel`). `tools/ramen_knip.py` zoekt per stuk het kozijn, laat een randje muur met een zachte rand staan
  en kleurt die naar de leem rond het raam van het oude huis. Alleen met `stad.accenten`; `ramen: false` in een gevel zet
  het daar uit. Een nis van een balkon vervangt het raam van die verdieping.
- **Zelf kiezen** (`stad.accenten: true`, `stadAccenten`): per seed vast. Ongeveer een op de vier huizen krijgt een balkon
  of een takel (`STAD_ACCENT`), hooguit een per huis en nooit twee huizen met een accent naast elkaar; een huis dat zelf
  een balkon of takel heeft telt mee. Op het oude huis wordt ongeveer 40 procent van de ramen een ander raam. Geen
  bestaand level heeft het; een nieuw stadslevel mag het aanzetten.
- **Sandbox**: onder De stad de knop **Accenten**: een straat met de accenten aan, elke klik een andere seed, en twee vaste
  takels vooraan om de mand te zien slingeren.

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
- De schildbandiet krijgt een strook om zijn hele huidige plaatje (`schbKanteelVak`, uit de bijgesneden lagen van
  lagen.json, nooit smaller dan `kanteelBreed`): in zijn sprongaanval waaien mantel en achterbeen ver uit, en die
  staken anders buiten de strook voor de kartels langs.
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

Het dek ligt schuin in beeld (de planken lopen in `galerij.png` van bronrij 104 tot 157), dus er zijn twee rijen:
`STAD.galerij.dek` (104) is de achterrand, de voet van de leuning, en `STAD.galerij.sta` (130) is waar je op staat, het
midden van de planken. Het plaatje komt met `sta` op de hoogte `h` (in `stadTeken`, `stadStrook`, de schaduw onder de
galerij in `stadSlagMuur` en in de Maker in `mkGalerijMaat` en `mkTrapMaat`); de opening in de leuning, de planknaden van
de doorgang en de achterrand die de doorgang zoekt (`stadDoorgangen`) blijven aan `dek` hangen. Eerst stond iedereen
met `dek` op de achterrand, tegen de leuning: met de planken nog voor zijn voeten leek Amir boven het dek te zweven.
Alleen het beeld veranderde: `h` en dus de sprong, de vijanden, de lift en de levels bleven hetzelfde. Het bordes boven
aan een stadstrap (`stadStrook` met `alleenTop`) is alleen beeld en sluit op de bovenste trede aan, dus dat ligt nog met
`dek` op `h`. Een lift bij een galerij (`TAKEL.galerijBoven`, 17) sluit nu bijna gelijk aan op de achterrand van het dek.

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
- De nevel, de straat onder de voorste rij en hoe donker de huizen daar zijn komen uit het uitzicht (`stadVerte` in
  `SCENES`, gelezen door `stadVerte()`); zonder dat veld de stad overdag (`STAD.nevel`, `STAD.verteStraat`). Alles wat
  met die nevel voorgebakken is (paleis, rijen, strook, pleinwand) heeft de sleutel ervan in zijn naam, dus een ander
  uitzicht bakt opnieuw. Na `stadAchter` komt ook in de stad de `dim`-laag van het uitzicht; die werd eerder overgeslagen.

## De stad bij namiddag, avond en nacht

Vijf uitzichten: `stad_ochtend` (het ochtendgloren uit De Rivierstad: een bleke lucht, roze en goud aan de horizon, de zon
laag links, een koele nevel en de laatste lampen nog aan, `nacht: 0.15`; in de sandbox de knop **Gloren**, alleen in de stad),
`stad_dag`, `stad_middag` (de zon lager, warme nevel), `stad_avond` (rozige nevel, paarsbruine
schaduwen, de helft van de lichten aan) en `stad_nacht` (blauwe lucht, de maan links en vrij hoog, de verte een
blauwe nevel met donkere huizen, een koele lichtlaag naar het voorbeeld van `winter_nacht`). Per uitzicht:

- `stadVerte: {nevel, straat, donker}`: de verte (zie hierboven).
- `slag: {kleur, alfa}`: kleur en sterkte van de slagschaduwen (`stadSlagKleur`); 's nachts koel en zwak.
- `nacht` (0 tot 1): steekt de lichten aan (`STAD_NACHT`, `stadNacht()`). Zonder het veld blijft alles uit.

De lichten (`STAD_NACHT`):

- **Ramen**: per gevelplaatje de raamvlakken in bronpx (`STAD_NACHT.ramen`); een raam hoort bij de band waar het in valt,
  dus alleen de verdiepingen die getekend worden. Een vaste helft brandt (`aan`, per raam uit `stadNachtHash` met de seed);
  een deur op een verdieping slaat dat raam over. Het raam licht op in de gevel (`stadNachtRamen`, in `stadTeken`, dus
  iedereen staat ervoor) en flakkert een beetje; de gloed eromheen komt na de lichtlaag.
- **De verte**: in `stadRijHuis` krijgt 's nachts een deel van de verdiepingen een oranje raam (`STAD_NACHT.verte`).
- **Een olielampje** onder het dak van elke kraam, bij de paal (`stadNachtLamp`, in `stadVoorTeken`), getekend met
  canvas. Het telt als licht op personages, net als een fakkel (`stadNachtLicht` in `plichtBronnen`).
- **De gloed** van ramen en lampen gaat op een lijst met de transformatie van dat moment, en `stadNachtNa` telt hem op
  na `drawLichtlaag`, anders dooft de lichtlaag hem weer uit.
- **Binnen** valt 's nachts zwak, koel maanlicht door het raam in plaats van de zonnebundel (`binnenNa`).
- Fakkels (`fakkels`) werken in de stad al gewoon, ook aan een leemmuur.

In de sandbox kiezen de knoppen onder **Tijd van de dag** in de stad het stad-uitzicht (`data-stad`; Ochtend heet daar
Dag). In de Maker staan onder **Uitzicht** ook Stad, namiddag, Stad, avond en Stad, nacht.

Nog niet: het stadsvolk, de kramen en de gordijnen hebben een vaste daglichttint (alleen de lichtlaag gaat erover), het
raamlicht op Amir binnen blijft warm, en de maan als lichtbron op personages volgt de zonregel van `PLICHT`.

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
- Het rieten dak (0,76 Amir boven de tafel) en de doek (0,78) liggen op de rand van een sprong vanaf de tafel: die haalt
  200 op 60 beelden per seconde, 184 op een traag toestel (`SPRONG_TRAAG` in `levelcheck.py`) en 178 met daarbij het
  speltempo op 1,2. Vooral de doek lukte daardoor vaak net niet, in elk level met kramen. Daarom haken je voeten erop
  zolang ze op het hoogste punt hooguit `STAD.kraamGrijp` (0,1 Amir) onder de rand blijven (`grijp` in `stadPlats`,
  gebruikt in `updateJump`). Van de straat haal je het dak zo nog steeds niet.
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

## De verhoogde straat

`STRAAT_TREDE`, `straatTredeTeken` (in `drawClimb`), `straatOnderVul`, `straatRandTeken`, `straatVoegen`, `stadOnderAan`;
`design/stad/straat_onder.png`

Een terras met `look: 'straat'`: `terraces: [{r, l, h, look: 'straat'}]`. Een stuk straat dat hoger ligt, als trede of als
een hele hoge wijk. De botsing is die van een terras: Amir springt erop, een vijand houdt er halt (regel 7, hij gaat geen
trede op), en een huis, kraam of vijand die erop staat krijgt vanzelf die hoogte (`terrainH`). Alleen het tekenen is anders:

- bovenop de rand van de straattegel (`straat.png`, rij 46 tot 182: loopvlak en randstenen), vast aan de wereld, die in
  18 bronpixels zacht uitloopt in de laag eronder;
- daaronder de onderlaag (`straat_onder.png`, een naadloze tegel uit Grok in de kleur van de aarde van de straattegel),
  vast aan de wereld en aan de grondlijn, zodat de rijen doorlopen van de straat via de treden naar de wijk; naar onder
  donkerder, gemeten vanaf de grondlijn;
- een open einde (geen even hoge of hogere straat ernaast) eindigt recht, op een voeg tussen twee randstenen (`straatVoegen`
  meet de voegen een keer in de randstrook, `straatOpVoeg` schuift het einde hooguit `voegZoek` bronpixels), met een kleine
  overstek (`over`), een slagschaduw onder de overstek en een zachte schaduw op de lagere grond ernaast.

Met `stad.onder: true` krijgt de straat zelf dezelfde onderlaag (in `sceneGrond`), zodat alles een laag is. Zonder dat veld
ziet de straat eruit zoals altijd: de bestaande stadslevels veranderen niet.

Treden zijn om op te springen, niet om op te lopen: een derde Amir (85) is een goede maat, en Amir heeft geen opstap voor
kleine hoogtes. Stad 8 (De hoge wijk) is het proefstuk: drie treden van 85 omhoog naar een wijk op 255 met twee huizen, en
twee treden weer omlaag. Daarna een tweede stuk met minder maar hogere treden: twee van 170 (twee derde Amir; de sprong
haalt zo'n 200, op een traag toestel 184) naar een wijk op 340 met een huis, een kraam en een bandiet, en een keer 170 omlaag. In de sandbox onder De stad **Hoge wijk met trap** (`sbtrap`, met `sbTrap` op de terrassen): drie
treden, een stuk wijk en twee treden omlaag voor je uit, en staat de stad er, dan ook de onderlaag onder de straat.

Hoort bij de stadsverbetering verticaliteit (H) in `notities/stad-verbeteren.md`.

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
  `vloer: 600` staat bij het begin op die hoogte (bandiet).
- In de Maker: **Vloer: hout** (Terrein, groep Stad, letter B; intern nog `balken`). Een blok boven de grondlijn wordt een
  zwever met deze look. In de sandbox onder De stad **Houten vloer**.
- De oude balkenvloer (`look: 'balken'`, een losse strook) is weg.

## Binnen: de binnenkant van een huis

`BINNEN`, `binnenBij`, `binnenEBij`, `binnenE`, `binnenKlem`, `binnenCamKlem`, `binnenVijandKlem`, `binnenAchter`, `binnenNa`,
`binnenLadder`, `binnenLaadLevel`, `binnenHeeftDeur`

```
binnen: [{ gevel, r, l, deur, ramen: [{x, h}], palen: [{x, h}], ladders: [{x, van, naar, f}], bogen: [{x, naar}] }]
```

Elk huis met een binnenkant is een eigen strook ver van de straat (van `r` tot `l`, in Stad 7 op -20000, -30000 en -40000).

- **Een deur boven** (`verdieping`, `deurH`, `binnenDeurV`, `binnenDeurH`, `stadDeurenBinnen`; in de sandbox **Deur boven naar
  binnen**): met `verdieping: 1` (of hoger) zit de deur naar buiten op die verdieping van de gevel. Buiten staat daar dan een
  open houten deur in het gat in plaats van het raam (`stadDeurenBoven`), en je komt er met E in vanaf de vloer ervoor: een
  galerij of balkon op die hoogte (`stadDeurVloer`). Binnen sta je bij `deur` op de houten vloer van die hoogte: `deurH`, of
  zonder `deurH` de zoveelste zwever van onder bij de deur (verdieping 1 is de eerste vloer boven de grond). E daar en je
  staat weer op de galerij. Het gordijn binnen hoort bij een deur op de straat en komt boven niet. `levelcheck.py` (regel
  `deuren`) meldt een deur boven zonder galerij of balkon ervoor, of op een verdieping die het huis niet heeft.
- **Meer deuren naar buiten** (`deuren: [{deur, verdieping, gevel, deurH}]`, `binnenDeuren`; in de sandbox **Beneden erin,
  boven eruit**): naast de hoofddeur nog deuren naar buiten, elk met een eigen plek binnen (`deur`), verdieping en vloer, en
  een eigen gevel (zonder `gevel` die van de kamer). Elke deur werkt twee kanten op. Zo ga je beneden naar binnen en kom je
  hoger op een galerij weer buiten, ook in het huis ernaast (een pand achter twee gevels, met `aan` strak tegen elkaar). In
  de sandbox: het deurgat van het rechter huis op de straat, de ladder op, en de deur op de eerste verdieping van het
  linker huis brengt je op een galerij die je van de straat niet haalt. `levelcheck.py` kijkt elke deur na.
- **In en uit**: voor het deurgat van gevel `gevel` (`stadDeurMaat`, verdieping 0) staat een E; E en het beeld wordt even
  zwart (`BINNEN.fade`, via `stadTrapFade` met `binnen: true`: de camera springt mee, geen glijvlucht) en je staat binnen bij
  de deur (`deur`, een wereld-x op de begane grond). E bij die deur en je staat weer buiten voor het deurgat. Niet in een
  gevecht (`stadInGevecht`), net als de stadstrap. Die deur is recht met een houten latei, net als het deurgat buiten
  (`binnen/deur_recht.png`, gemaakt uit de boogdeur en de latei van `gevel.png` met `tools/binnen_deur_recht.py`).
- **De binnenpoort**: de ronde boogdeur (`binnen/deur.png`) is de doorgang naar een volgende kamer in hetzelfde pand. Een boog
  op `x` (begane grond) brengt je met E naar de boog op `naar`, in een andere strook; je komt een stap de kamer in uit, met je
  gezicht ernaartoe. Dezelfde fade, en ook niet in een gevecht. Een kamer zonder `gevel` (`gevel: null`, geen `deur`) heeft geen
  deur naar buiten: je komt er alleen via een boog (`binnenHeeftDeur`). Zet een boog altijd in paren, een in elke kamer.
- **De ladder** werkt als de stadstrap: E bij de voet of bovenaan, het beeld dimt even en je staat aan de andere kant; niet
  in een gevecht. De voet staat op `x` op vloer `van`, de top leunt naar links (met `f` naar rechts) en `binnenLadder` geeft
  waar hij de hoek van de vloer erboven raakt (`rand`): daar hoort de rand van die vloer, zodat hij ertegen leunt (in Stad 7
  133 voorbij de voet bij een verdieping van 600). Hij wordt voor de vloer getekend (in `binnenNa`), met de vork erboven uit.
- **Vast in het huis**: Amir (`binnenKlem`, in plaats van de klif), de camera (`binnenCamKlem`) en de vijanden
  (`binnenVijandKlem`) blijven tussen `l` en `r`. Binnen geeft `endWall()` geen grens, anders hielden de botsingen van de
  vijanden ze tegen (het huis ligt voorbij de klif van de straat).
- **De speer binnen**: een geworpen speer botst op de muren van de kamer (in `javUpdate`, links `binnenLinks`, dus ook de
  toonbank) en blijft erin steken, zoals in een rotswand; na `JAV.muurT` wrikt hij los en valt hij binnen op de vloer.
  Begint de punt al voorbij de muur (Amir vlak ertegen), dan telt het huis van Amir. Zonder dit vloog hij de leegte in.
- **Een smalle kamer**: is een kamer smaller dan het scherm, dan zoomt de camera in tot hij het scherm precies vult
  (`binnenZoom`, in `viewZoom`). Zo valt de rand van de kamer altijd samen met de rand van het scherm, net als in een brede
  kamer, en zie je er nooit de straat naast. De sprong valt in de fade van de deur of de boog.
- **Vijanden**: een spawn in een huis komt pas als Amir in dat huis is, en dan meteen, op zijn eigen plek (`spawnPoint`
  duwt hem niet naar buiten beeld); dus allemaal tegelijk, al tijdens de fade.
- **Tekenen**: `binnenAchter` (voor de zwevers) tekent de binnenmuur (`binnen/wand.jpg`, getegeld en vast aan de wereld, tot
  het hoogste plafond; daarboven donker), een plint langs elke vloer, de ramen (`raam_1.png`), de gevorkte palen (`paal_1..5`,
  de vork en de voet op maat, de stam ertussen herhaald tot onder het plafond, `binnenPlafond`), en
  de boogdeur (`deur.png`). `binnenNa` (na de zwevers, voor de personages) tekent de ladders en legt het schemer over alles (`BINNEN.donker`, de
  personages blijven helder), donkere zijmuren, en dan het licht: het glas gloeit, een lichtbundel valt schuin naar de vloer
  (`BINNEN.bundel`) met een lichtvlek, en veel stofjes zweven door de kamer (`BINNEN.stof`), zacht in het schemer en helder in een
  bundel. Buiten tekent hij alleen de E bij het deurgat.
- **Amir in de bundel**: het licht valt ook op hem (en op de vijanden die op `persLicht` aangesloten zijn, zie `notities/licht-personages.md`). Na zijn frame legt `binnenLichtOp` een warme kopie ervan met 'lighter'
  over hem, geknipt op de vorm van de bundel (`binnenBundels`, `binnenBundelPad`), zodat de lichtgrens schuin over zijn lijf
  loopt als hij erdoor stapt. Waar hij de bundel afdekt (`binnenBundelDek`) ligt zijn silhouet in de lichtvlek op de vloer,
  van het raam af (`binnenBundelSchaduw`, vanuit `amirSchaduw`). Kleur, sterkte en schaduw in `BINNEN.licht`. De schaduw in de
  lichtvlek is alleen er voor Amir.
- `levelcheck.py` kent de stroken (`binnen_strook`): wat erin staat is niet "voorbij het einde", en tussen de zwevers van twee
  huizen hoeft niet gesprongen te worden.

Stad 7: Binnen is het proefstuk, met 450 vrije hoogte onder en boven een verdieping (drie huizen: een zaal op palen met achterin
een boog naar een kamer erachter, en twee met een verdieping en een ladder, een keer gespiegeld). In de sandbox onder De stad:
**Huis met binnenkant** (met een boog achterin en een kamer erachter). In de Maker nieuwstijl teken je een kamer als een blok
**Binnen**-cellen met houten vloeren erdoor, en zet je er de deur, bogen, ladders, ramen en palen in; de Test zet hem in zo'n strook
(zie "De binnenkant van een huis: kamers" in `notities/maker.md`).

## De winkel en de inrichting: een toonbank, een schap en planken met spullen

`WINKEL`, `winkelLaad`, `winkelOpbouw`, `winkelPlankOpbouw`, `winkelRij`, `winkelAchter`, `winkelVoor`, `binnenLinks`, `winkelUIOpen`

```
binnen: [{ ..., winkel: { x, seed, koopman }, planken: [{ x, h, soort, seed }] }]
```

- **De winkel** staat aan de linkerkant van een huis. `x` is het rechtereind van de toonbank, en daar loopt Amir tegenaan:
  de toonbank is de grens van wat je kunt belopen (`binnenLinks`, in `binnenKlem` en `binnenVijandKlem`). Hij staat niet
  op de achtergrond maar op de vloer, op dezelfde lijn als Amir: zo loopt Amir er nooit overheen, wat met de paar pixels
  diepte van de vloer binnen altijd las als "op de bar".
- **Achter de toonbank**, tegen de muur: het schap (`schap.png`, drie planken, de onderste zit achter de toonbank en blijft
  leeg), daarnaast 2 tot 4 speren die tegen de muur leunen (rechtop: liggend op het blad leken ze te zweven), en de
  marktman. Voorlopig is dat de dorpeling, gespiegeld zodat hij naar Amir kijkt; `koopman: false` laat hem weg.
- **Op het blad** een tot drie kalebassen, en soms nog een spul. Dat is wat je straks kunt krijgen.
- **Elke winkel is anders.** Wat er waar staat volgt uit `seed`: welke spullen op welke plank, de speren en hun hoek, of de
  toonbank en het schap gespiegeld zijn, de kalebassen, waar de marktman staat. Een vast level heeft een vaste seed en ziet
  er elke keer hetzelfde uit; een nieuw level krijgt een nieuwe seed (zonder seed volgt hij uit `x`). Elke klik op de
  sandbox-knop geeft een nieuwe.
- **Planken** hangen aan de muur: `x` het midden, `h` de bovenkant van de plank boven de vloer (wereld-eenheden, net als
  een raam), `soort` `touw` (met touw om de steunen) of `kaal`. Ook daarop volgen de spullen uit de seed, iets minder vol
  dan in een winkel, en zonder kalebassen: thuis lijkt een kalebas iets om te pakken.
- **De spullen** (`WINKEL.spullen`, `spul_*.png`): mand met deksel, mand, schalen, stof, rollen, kist, schaal, kruik en, alleen
  in een winkel, de kalebas (`items/potions/hppotion.png`). Hun hoogte staat in Amir, `spulMaat` maakt ze allemaal iets
  groter. Ze komen uit een vel van Grok in strikt zij-aanzicht op ooghoogte, zonder schaduw: een vel met de camera erboven
  (je ziet in de manden, de stof ligt plat) werkte niet.
- **Tekenen**: het schap met de speren en de planken worden een keer opgebouwd tot een beeld met een zachte schaduw op de
  muur eronder (`winkelMetSchaduw`), en getekend in `binnenAchter`, zodat het schemer van `binnenNa` erover valt. De
  toonbank komt na de personages van het level en voor Amir (`winkelVoor`), met de marktman ervoor; het schemer zit daarom
  al in zijn beeld gebakken (`BINNEN.donker`), en hij heeft een schaduw op de vloer.
- Platen: `toonbank.png`, `schap.png`, `plank_touw.png`, `plank.png` en `spul_*.png` in `design/stad/binnen/`, uit Grok
  (wit weggeknipt, lichte randpixels weg). `spul_kruik.png` is de kruik uit `voetdecor.png`. Net als de rest van `binnen/`
  hebben ze geen halve versie in `klein/`.
- **Het winkelscherm** (`winkelUIOpen`, `winkelUIDicht`, `#winkelui`): E vlak voor het eind van de toonbank (`WINKEL.eBij`)
  opent een simpel scherm en het spel staat stil (`paused`). Er is nog geen geld: elke klik op de kalebas geeft er een, zo vaak
  als je wilt, ook voorbij de 3 die Amir normaal draagt (`HPPOTION_MAX` geldt alleen voor oppakken). Escape, E of Verder
  sluit het, en de pauzeknop op de telefoon ook. Niet in een gevecht, net als de deur. In een level met `goud: true` (De Gouden
  Poort) kost een kalebas 5 goud en draag je er hooguit 3 (zie "goud" in `notities/episodes.md`).
- **Verkopen en je spullen** (`winkelVerkoop`, `winkelTerugkoop`, `winkelTasToon`, `GOUD.verkoop`): rechts in het scherm staat
  je tas (`.wktas`: de vijf plekken, hand en rug, het gif op je speren), op een smal scherm eronder. Met goud staat onder elk
  ding een verkoopknop (`.wkverkoop`, goudkleurig, de opbrengst erop); zonder goud zijn ze weg (`#winkelui.gratis`). Zie
  "verkopen" in `notities/episodes.md`.

In de sandbox onder De stad: **Winkel** en **Kamer ingericht**. De Gouden Poort heeft drie winkels (Goud 3, 6 en 9).

## Straten en knooppunten (Sandville)

`straatRaster`, `straatUitgangen`, `straatKnoopX`, `straatUitgangBij`, `straatKnoopGa`, `straatKnoopToets`, `straatGevelX`,
`straatKnoopPoortTeken`, `straatKnoopVoor`, `straatPadZak`, `straatRasterKaart`, `SAND_STRATEN`, `STAD_5`, `sbKnoop`

Een veld `straten` met `raster: true` (zie ook `notities/oaktown.md`): elke straat een eigen strook ver uit de buurt
(`straatKlem`, `straatCamKlem`, `straatVijandKlem`, het aanvullen, de spawns per straat), met knooppunten: een poort de
diepte in en een pad naar voren. Rechtdoor is gewoon de straat die doorloopt. Zo werken alle straten: Sandville, Oaktown
(sinds 08-11-2026) en elk nieuw level met straten. De oude hoekpoort (`poort_hoek`) gaat eruit; sinds De Kroonwijk is
omgezet (09-11-2026) gebruikt geen level hem nog. Twee straten in elkaars verlengde op dezelfde knoop (zoals in Oaktown en De
Kroonwijk) blijven aparte straten, maar hebben een **doorgang**: aan dat uiteinde staat geen leemmuur, en wie tegen de rand
van de straat aan loopt staat na de wissel aan de rand van de volgende straat (`straatUitgangen` geeft een uitgang met
`soort: 'door'` en `kant` -1 of 1, `straatDoorDruk` vanuit `straatKlem`, de maten in `STRATEN.door`). Er staat een bordje
met een pijl naar de rand. Niet in een gevecht, net als de poort en het pad. Laat aan zo'n uiteinde de leemmuur weg in het level.

**Alleen rechte straten.** Een straat is een rij of een kolom op de kaart: al zijn knopen liggen op dezelfde y (een rij)
of dezelfde x (een kolom). Schuine straten, zoals de punten van de oude Kroonwijk, komen er niet meer bij; een raster kent
alleen links, rechts, de diepte in en naar voren, dus een schuine straat geeft geen goede poort of pad.

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
  een kleine shake `schok`; het geluid gaat door een versterker, `SFX_SLAM.vol`, met drie stemmen en de muziek die even wijkt, zodat hij
  in elk level boven de muziek uitkomt), en daarna blijft hij open. De eerste vijand wacht tot de deur open is (`deurWacht` begint op de duur van
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

Een fontein voor het plein staat bij het water, als `wateren: [{k: 'fontein', x}]`: zie "de fontein" in `notities/water.md`
(sandbox: **Fontein** onder De stad).

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

## De springdoek

`STAD_SPRINGDOEK`, `stadLuifelBeeld`, `stadKleurMat`, `stadLuifelMaat`, `stadLuifelTeken`, `sbSpringdoek`, `sbspringdoek`

De luifel van het plein, maar aan de muur van een huis in plaats van bij een put: `stad.luifels: [{gevel, wand, h, voet, maat,
kleur, zak, worp}]`. De paal staat net buiten de muur van gevel `gevel` (`wand` `'r'` de rechtermuur, `'l'` de linker) en de
doek steekt van het huis af de straat in; wie erop landt wordt van het huis af weggeworpen (wand `'r'` naar rechts).

- `h`: de hoogte van het lage eind, `voet`: waar de paal ophoudt (met een touwbinding), beide in sprite-eenheden boven de grond.
  Op een balkon is `voet` de vloer van het balkon, op een dak het dak.
- `maat`: de grootte (0,85 in Stad 9), `zak`: hoe ver hij in Amir doorzakt, het diepst iets voorbij het midden. De stukken om op
  te landen zakken mee (`lm.zak` in `stadLuifelPlats`). Met `zak` krijgt hij ook een donkere onderrand: dezelfde doek, donker,
  iets lager en naar het lage eind dikker (`STAD_SPRINGDOEK.dik`). Die onderrand laat de paal en de schoor weg (`schoor`), anders
  staat de schoor er twee keer.
- `kleur: 'indigo'`: de doek omgekleurd (hue-rotate en saturate per pixel, `stadKleurMat`, een keer gebakken met `stadGebakken`);
  de paal en de schoor blijven hout. Geen `ctx.filter`, dat kent Safari niet.
- `worp`: de opsprong in plaats van `worp.vy` (0,8) van het plein. Opzij blijft het 4 Amir per seconde, dus de boog is in Amir op
  elk scherm hetzelfde; de hoogte in sprite-eenheden ook. Een steeg tussen de huizen (`aan` in Amir) schaalt mee, dus zet de
  huizen die bij een worp horen met `aan` tegen elkaar.
- Geen slagschaduw op straat: hij hangt daar te hoog voor.
- **Bereikbaar**: landen kan alleen van boven. Een sprong haalt zo'n 208 boven je vloer, dus het lage eind hangt hooguit
  ongeveer 150 boven het balkon of dak (Stad 9: 155). Bij de muur hangt hij boven je hoofd en spring je eronder door; onder het
  lage eind recht omhoog springen werkt. Met een aanloop spring je er voorbij. Van een hoger dak eraf stappen en erop vallen werkt
  ook, behalve op een telefoon, waar Amir zo ver per stap komt dat hij de korte doek mist: dan landt hij op het dak eronder en
  springt hij van daar omhoog.
- **Recht** (`recht: true`): de rechte springdoek. Het plaatje wordt per kolom omlaag geschoven (`stadLuifelSchuif`, gebakken
  in `stadLuifelBeeld(kleur, onder, true)`), zodat de bovenkant van de doek overal op `h` ligt; de paal zakt mee en de schoor
  wordt zo vanzelf een steun schuin omhoog. Hij gooit je niet weg maar veert zoals de doek van een kraam (`stadVeer`, met
  `veer: true` en `springdoek` in `stadLuifelPlats`): zacht neerkomen en je blijft staan, hard neerkomen en je wipt recht
  terug, en springen erop staand of net bij het landen (`STAD.veer.raam`) geeft de hoge sprong. Die is dan `worp` maal jumpV
  in plaats van `STAD.veer.hoog`. Opzij stuur je zelf in de lucht, zoals bij elke sprong; er is geen eigen zijvaart.
- **Stad 9** (recht): op het balkon van de tweede trap (`h` 885 boven vloer 730, `worp` 1,85, je stuurt naar het dak van 1429)
  en op het lage huis 2, nu strak tegen huis 1, tegen de muur van huis 1 (`h` 926 boven dak 771, `worp` 1,4, je stuurt naar
  het dak van 1100). Vroeger hing die tweede tegen de muur van huis 3 en gooide hij je over het hele lage dak; recht omhoog
  met sturen haalt die afstand niet. Nagemeten op 852x393, 1280x720 en 1920x1080.
- **Kozijn** (`kozijn: true`, alleen met `recht`): de losse luifel boven een raam. Geen paal: die is uit het gebakken plaatje
  geknipt (`stadLuifelBeeld(kleur, onder, true, kaal)`) en er loopt niets naar `voet`. De schoor steunt tegen de muur, en
  onder de doek staat een smalle houten lat met een vensterbankje, de zijkant van een kozijn (in `stadLuifelTeken`). De regel
  erachter: een luifel moet je onder kunnen staan, of hij hangt waar niemand loopt. Hang hem dus boven een steeg, niet boven
  een balkon of dak: Amir springt 208 hoog en is 251 lang, dus een luifel boven een vloer die je vanaf die vloer haalt, hangt
  altijd op borsthoogte.
- **Stad 10**: de strakke luifel (zie hieronder) op de linkermuur van huis 1 (`h` 515, `maat` 0,85, `worp` 1,95), boven de
  steeg naast een kort balkon (de trap van huis 2, `balkon` 0,6, vloer 401; de steeg is 2,4 Amir, zodat de doek niet boven het
  balkon hangt). Van de rand van het balkon spring je schuin op de doek, en met de hoge sprong stuur je het dak van 1100 op.
  Nagemeten op 852x393, 1280x720 en 1920x1080: op een telefoon moet je pijl rechts loslaten boven de doek, anders schiet je
  erover. De kozijn-luifel van hierboven staat nu in geen level meer.
- **Sandbox**: onder De stad de knop **Bounce cloth** (de schuine doek die je wegwerpt) en **Straight cloth** (de rechte):
  een trap naar een balkon met de doek erboven en een hoger huis ernaast.

## De strakke luifel

`STAD.plein.luifelStrak`, `stadLuifelStrakMaat`, `stadStalY`, `stadKuilStap`, `stadKuil`, `stadLuifelStrakTeken`,
`stadLuifelStrakKolommen`, `stadLuifelVoor`, `stadOpStrak`, `stadAmirX`

`stad.luifels: [{gevel, wand, h, maat, worp, stijl: 'strak'}]`: een indigo doek in een houten raam (`design/stad/luifel_strak.png`,
een Grok-plaat), los aan de muur van gevel `gevel`, de muurkant (`wand` in de constanten) op de muur, de doek de steeg in.
`h` is de hoogte van de stallijn aan het lage eind. Hij veert zoals de rechte springdoek (`stadVeer`, `worp`).

Het probleem dat hij oplost: op een doek van opzij leek Amir altijd te zweven. Twee oorzaken. Een dunne rand heeft geen
bovenvlak, dus zijn achterste voet (in zijaanzicht iets hoger) stond in de lucht; en Amir wordt een paar pixels boven zijn
eigenlijke voethoogte getekend, wat op de straat wegvalt in de strook bovenkant maar op een dunne rand niet. Daarom:

- **De plaat toont het bovenvlak**: de doek is een strook, en Amir staat niet op de bovenrand maar op de **stallijn** in die
  strook (`stal`, een derde vanaf de voorrand, gemeten in bron-px).
- **Eén stuk dat de hoogte onder zijn midden neemt** (`stadLuifelPlats`): met smalle stukken pakte `supportHeight` de hoogste
  plek onder zijn voeten, op de helling de bergopwaartse kant. `stap` laat hem lopend een paar eenheden opstappen.
- **De kuil**: waar hij staat zakt de doek in (`kuil.diep` en `kuil.breed` in Amir), hij zakt `kuil.amir` daarvan mee, en
  bij een landing veert de kuil na (`veer`, via `luifelT`). Alleen de doek zakt: wat onder de onderrand ligt (`onder`, het hout
  van de steun) blijft staan.
- **Diep genoeg om weg te zakken**: de kuil is 0,12 Amir diep, hij zakt 0,6 daarvan mee, en de onderkant van de doek rekt
  verder uit dan de bovenkant (`kuil.buik`), zodat je onder de doek een uitgezakte buik ziet. Gebukt staan zijn voeten verder
  uit elkaar, dus dan is de kuil breder (`kuil.buk`, `stadKuilBreed`). Het stuk is een halve Amir-breedte korter dan de
  stallijn aan elke kant: voorbij het eind val je eraf in plaats van te zweven.
- **Twee lagen**: de doek met de kuil voor Amir, en na Amir alleen de voorrand rond zijn voeten (`stadLuifelVoor`, in de
  render-lus voor `critFxTeken`), minder diep ingezakt (`kuil.voor`), vanaf `kuil.rand` boven de stallijn. Zo vallen zijn
  zolen en tenen achter de voorrand en loopt de doek achter hem omhoog.
- **Schaduw**: geen harde schaduw van Amir op de luifel (`amirSchaduw` slaat over), wel een zachte vlek in de kuil.
- **Let op**: tijdens het tekenen is `world` het midden van de camera, niet Amir (`pWorld`). Daarom legt `stadKuilStap`
  (in `stadLuifelStap`, de spelstap) vast of en waar hij erop staat (`kuilOp`, `kuilX`, `stadAmirX`), en leest het tekenen
  alleen dat.
- **Kleur** (`kleur: 'oker'`): de doek omgekleurd naar rode oker, alleen de blauwe pixels (het hout blijft), een keer gebakken
  (`stadLuifelStrakBeeld`, de kleuren in `luifelStrak.kleuren`).
- **De trampoline** (`ritme: true`, `stadRitme`, `stadRitmeV`, `stadVeerVin`): hoogte bouw je op. Val je erop, dan stuiter je
  vanzelf terug met `ritme.demp` (0,6) keer de valsnelheid; onder `ritme.rust` (0,45 jumpV) blijf je staan, dus niets doen
  stuitert uit in een stuit of twee. Spring je op tijd bij een landing (binnen `ritme.raam`, 0,2 s ervoor of erna), dan is de
  volgende stuit `ritme.stap` (0,25 jumpV) sneller, tot `ritme.max` (1,42: ongeveer 1,3 verdieping, zie hieronder). Vanaf stilstand springen is een gewone sprong
  (`stadVeerHoogte` geeft 1). Het naveren van de kuil schaalt met hoe hard de stuit was (`p.sterk` in `stadKuil`).
- **Hoe hoog**: een verdieping is 1,31 Amir (329 eenheden), een gewone sprong ongeveer 0,6 verdieping. Een stuit blijft
  realistisch onder anderhalve verdieping: de indigo luifel (`worp` 1,38) geeft ongeveer 1,2 verdieping, de trampoline
  hooguit 1,3 (`ritme.max` 1,42; met 1,55 kwam je in Stad 10 op het dak van de toren, en daar kun je niet bij de deur). Zo haal je met een luifel de volgende verdieping, en kom je hoger via de volgende luifel. Grijpen en optrekken
  (aan de voorste paal, een galerij of een reling) is nog niet gebouwd; komt het, dan op vaste grijpplekken, zodat deze
  routes niet te makkelijk worden.
- **Stad 10** (de zigzag-steeg): de toren (vier hoog, de deur op de derde verdieping met de galerij van 1059 alleen voor zijn
  gevel) en over een steeg van 1,7 Amir een huis van vier hoog. Twee stadstrappen (zoals in Stad 9) naar een kort balkon op
  de eerste verdieping (730), in de steeg. De indigo luifel hangt aan de toren boven het raam van de eerste verdieping
  (staan op 682): van de rand van het balkon spring je erop. Met een sprong op tijd stuiter je naar de rode trampoline aan de
  overkant, boven het raam van de tweede verdieping (993; hij hangt een kleine Amir boven het balkon, je kunt er net onder
  staan). Nu zijn ze allebei een trampoline: op blauw een goede stuit om rood te halen, op rood naar de galerij. Daar stuiter je hoger en stuur je de steeg over naar de galerij (toppen 320 en 410 boven de doek). Let op: opzij gaat
  Amir in wereld-px even snel op elk scherm (330 px/s), maar hij is groter op een groot scherm, dus in Amir gerekend komt hij
  op 1920x1080 minder ver dan op 1280x720 en op een telefoon veel verder. Nagemeten: op 1280x720 haal je de galerij met een
  goede stuit, op 1920x1080 met twee, op 852x393 al met een gewone sprong. Met een steeg van 2 Amir lukte het op 1920 niet.
- **Sandbox**: onder De stad de knop **Trampoline**: een trap naar een kort balkon, de rode trampoline ertegenover en een huis
  van drie hoog om op te stuiteren. Eronder verschijnen drie schuifjes om af te stellen (`sbLuifelPaneel`): **Awning size**
  (`maat` van de luifels in de sandbox), **Shutter height** (`raamZij.hoog`) en **Gap under awning** (`raamZij.onder`,
  negatief: het luik loopt tot achter de luifel). Ze werken meteen, en de regel eronder geeft de waarden zoals ze in de code
  horen; die zet je daarna in het level en in `luifelStrak.raamZij`.
- **Stad 11: Awning tuning**: hetzelfde paneel, maar in een eigen testlevel (gevraagd, in plaats van de sandbox): de opbouw
  van Stad 10 zonder vijanden (`vredig`), met `luifelAfstel: true`. Het paneel zweeft linksboven (`#sbluifelpaneel`, getoond
  in `beginPlay`, weg in `toMenu` met `luifelPaneelUit`), en de schuifjes houden hun stand bij een herstart.
- **Het raam** (`raam: k` of `raam: true`, `stadRaamZijTeken`, de maten in `luifelStrak.raamZij`): een luifel hangt niet zomaar aan een muur,
  dus onder de doek zit een raam in de zijmuur. De zijmuur zie je van opzij niet, dus je ziet het luik dat naar buiten is
  opengeklapt recht van voren (de rechtervleugel uit `raam_luiken.png`, met de scharnieren aan de muur), met de kozijnrand
  langs de muur, een vensterbankje en bovenin de schaduw van de luifel. Getekend voor de luifel, die er dus overheen valt.
  Met `raam: k` (een verdieping) zit het raam op de hoogte van de voorramen: het midden van het luik `raamZij.midden` (0,752
  Amir) boven de vloer van verdieping k, net als het midden van het voorraam (`STAD_NACHT.ramen.gevel`), en de luifel hangt
  `raamZij.onder` erboven: zijn hoogte volgt uit het raam, `h` doet dan niets. Een raam in de zijmuur op een andere hoogte dan
  de voorramen viel op. De maten komen uit Stad 11: luik 0,66 Amir, 0,10 ertussen.
  Een luifel aan een muur hangt altijd boven een raam (wens van de opdrachtgever): `levelcheck.py` geeft FOUT op een luifel
  zonder `raam` in een echte episode, en LET OP in de testreeks Stad (Stad 9 heeft nog de rechte springdoeken).
- **Zweven aan de uiteinden** (opgelost): Amir staat op de hoogte van zijn laagste voet (`kuil.voet`, een halve
  voetafstand), zijn beide voeten blijven boven de stallijn (het stuk is `kuil.voet` korter aan elke kant), de voorste laag
  tekent alleen de doek zelf (niet de paal of de franje), en de kuil schaalt mee met de luifel (`stadKuilDiep`: op maat 0,45
  is de doek maar een paar pixels dik, en een kuil van volle diepte zakte ver onder zijn voeten weg).
- **Geluid** (`stadLuifelPlof`, de maten in `luifelStrak.plof`, geen bestand): een doffe plof van strakke stof (een
  sinustoon die zakt), wat ruis voor de klap van het doek, en bij een harde landing een zacht kraken van hout en touw. Het
  volume volgt hoe hard je landt, en op de trampoline klinkt elke goede stuit hoger (`plof.trede`), zodat je hoort dat je
  hoogte opbouwt. Uitstuiteren geeft ploffen die zachter worden.
- **Landingsplek**: de hele doek (van het eerste tot het laatste punt van `stal`), zonder inkorting: aan het eind mag een voet
  over de rand hangen, pas met zijn midden ervan af valt hij. Met de inkorting bleef er een derde Amir over en viel je er na
  een stap af.
- **Kleur**: blauw en rood zijn allebei een trampoline (`ritme`); de kleur doet nu nog niets. Idee voor later (opdrachtgever):
  een kleur die na een paar stuiten voorgoed scheurt, zodat je het in een keer goed moet doen of erdoorheen zakt.
- **Maat**: in Stad 10, Stad 11 en de sandbox `maat` 0,55 (0,45 uit Stad 11 gaf te weinig landingsruimte). Het stuk om op te staan is aan elke kant
  0,4 halve Amir-breedte korter dan de stallijn; een hele halve breedte liet op zo'n kleine luifel maar 0,27 Amir over.
- Alleen Stad 10. De plaat laadt pas als een stad hem gebruikt (`stadSoortLaad`).

## De einddeur

`eindDeur`, `eindDeurBij`, `eindDeurUit`, `eindDeurTeken`

`eindDeur: {gevel, verdieping}` in een stadslevel: die deur staat open (`stadDeurenBinnen` neemt hem mee), met gouden pijltjes
erboven die je van ver al ziet (`stadTrapUitTeken`), en E ervoor speelt het level uit (`eindDeurUit` in `eDruk`, dan `winLevel`).
Op een verdieping hoort er een galerij op die hoogte voor te lopen (`stadDeurVloer`), anders kom je er niet. Zo kan het einde
hoog in een huis liggen in plaats van bij de fakkels; het level heeft dan `ends: []`. `levelcheck.py` kent hem (regels `einde`
en `einddeur`). Alleen Stad 9.

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

Een losse speer op een galerij viel weg tegen de reling, en op een dak was hij een dun streepje. Ligt een losse speer
`SPEER_BAKEN.boven` (60) hoger dan Amir, dan zweeft erboven de speer zelf in het klein (`speerBakenTeken`, vanuit
`skETeken`): dezelfde sprite, op elke as even veel verkleind, ondersteboven met de punt naar de speer, voor een
lichtvlek die van wit naar amber loopt en zacht ademt. Is de speer `wacht` (3) seconden in beeld, dan zwelt in `aanzwel`
(1) seconde een puls aan: zacht en weer fel, een keer per `puls` (1,2) seconde, en zolang hij blijft liggen. Gaat hij uit
beeld, dan begint de klok opnieuw (`sp.bakenVan`). Staat Amir erbij, dan neemt de E het over. Alleen in de stad.
Eerder geprobeerd en afgekeurd: een donkere omlijning met een schittering, een gloed, pijltjes, een icoon in een rondje
of vakje, en de speer anders neerleggen (rechtop, met een wimpel, in een kruik).

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

## Slagschaduwen

`STAD_SLAG`, `stadSlagMuur`, `stadSlagStraat`, `stadSlagScheef`, `STAD_SLAG_AAN`. Stap L1 uit `notities/stad-verbeteren.md`.

De stad werpt schaduw, in de richting van de zon van het uitzicht: dezelfde `zonSchaduw` als de schaduw van Amir,
omgerekend naar een schuinte (opzij per stap naar voren) en begrensd op `scheefMax`. In `stad_dag` staat de zon
rechts, dus alles valt naar links; in de ochtend (`ochtend`, zon links) valt alles naar rechts. Hoe lager de zon (de
hoogte uit `sun`), hoe langer en schuiner, tot `lengMax` keer die van de hoge middagzon van `stad_dag` (`lengHoog`).
Een uitzicht met `dim` (de avond, de nacht) maakt de schaduw zachter (`dimZacht`).

- **Op de muur** (`stadSlagMuur`, in `stadTeken` na de gevels en de pleinpoorten, voor de galerijen): onder een
  galerij een band op de muur, vol tot de onderste balk en dan vervagend over `galerij.diep` Amir, schuin weg van de
  zon. Alleen op de muur van een voorgevel: in een opening tussen twee huizen staat niets dat hem vangt (een zwakke
  schaduw daar viel ook op de lucht). De galerij zelf blijft in het licht:
  daarom komt de schaduw voor de galerij. Staat een hoger huis aan de zonkant pal naast een lager huis, dan valt er een
  schuine wig (`buur`) op de muur van het lagere, onder de kartels (`kanteel`, bronpx van `gevel.png`).
- **Op de straat** (`stadSlagStraat`, bovenaan `stadVoorTeken`: na de stoep, voor de kramen en Amir): elk huis legt een
  schuine baan over de straat, van de muurvoet tot `straat.voor` Amir voorbij de looplijn, vooraan lichter. Tussen de
  huizen blijft de straat in de zon. Een kraam krijgt een zachte vlek recht eronder en de schaduw van zijn dak schuin
  ernaast (`kraam`).

Ook op de straat: een pleinpoort en een trap van de straat af (`trap`, zwakker, want de treden laten licht door) leggen een
baan zoals een huis; de put, de doek van een luifel en een ton (`put`, `luifel`, `ton`, in `tonTeken`) een schuine vlek
zoals een kraam (`stadSlagVlek`). De pleinwand niet: die staat achteraan in de nevel, voorbij de straat. Het voetdecor
houdt alleen zijn eigen contactschaduw.

In de sandbox onder De stad: **Slagschaduw: aan/uit** (`sbslag`) om te vergelijken.


## Stadsvolk: mensen op de stoep

`STAD_VOLK`, `volkTeken`, `volkUpdate`, `volkRustig`, `volkKleur`, `npcStap`. Het veld `stad.volk: [{x, k, kleur, f}]` zet de
dorpelingen uit `NPCS` (`k` is `dorpelinge` of `dorpeling`, met hun eigen animatie) in de stad, als achtergrond die niet meedoet.
Elk frame in zijn kleur bakt vooraf op het laadscherm (`warmBouw`): `volkBeeld` leest daarvoor de pixels terug, en dat gaf midden in het spel een korte stop bij elk nieuw frame.

- **De laag**: de voeten staan op de stoep, op `stoep` (0,6) van `stadStoepH` boven de looplijn: voor de muurvoet, achter de straat
  waar Amir en de vijanden lopen, en iets dieper dan het voetdecor (0,4). Getekend in `stadVoorTeken` na de slagschaduw op de straat
  en voor de kramen, dus wie achter een kraam staat, staat erachter (een verkoper). Met een zachte contactschaduw.
- **Achtergrond**: iets kleiner (`maat` 0,72 van een dorpeling, ongeveer 0,9 Amir), iets donkerder (`licht`) en met wat waas, zodat
  een vijand ervoor goed te lezen blijft. Geen botsing, niet te raken.
- **Kleur**: het blauw van de kleren gaat naar `rood`, `groen`, `indigo`, `oker` of `wit` (`STAD_VOLK.kleuren`, gebakken met
  `stadBak`, een keer per plaatje en kleur). Zo lijken twee sprites meer mensen. De herhaling blijft wel te zien: eigen
  stadsfiguren (suggestie 2 van V1 in `stad-verbeteren.md`) zijn de volgende stap.
- **Niet waar gevochten wordt**: komt er een levende vijand binnen `weg` (1100) van iemand en ook van Amir (een vijand die verderop
  wacht telt dus nog niet), dan vervaagt hij in `vervaag` s; na `terug` (6) s zonder vijand komt hij terug. Zet ze op rustige plekken.
- **In de levels**: Stad 1 (een verkoopster achter de eerste kraam, iemand bij de deur, een bij de doek, een bij het eind) en Sandville
  (aan de rustige uiteinden van de Kuiperstraat, niet op het kruispunt waar je begint en vecht, en in de Pottenbakkersstraat).
- **Sandbox**: onder Terrein, De stad, de knop **Stadsvolk**: vijf figuren in vijf kleuren op de stoep voor je uit (zet eerst de stad
  neer als die er niet is). Zet er een vijand bij om ze te zien verdwijnen.
- **Maker nieuwstijl**: onder Decor, Straat, **Stadsvolk**, met soort en kleur (zie "Tonnen en stadsvolk" in `notities/maker.md`).
