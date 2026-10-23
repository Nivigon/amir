# Ravijnen en de zon op de wand

### Een gewoon ravijn is een ravijn dat al open staat

Een ravijn uit `gaps` zonder gang eronder wordt getekend met dezelfde module als het ravijn dat
openscheurt: `ravijnVastVoor(g)` maakt er een `RavijnEffect` van dat meteen open staat
(`openInstantly`), en `ravijnenTeken()` geeft die samen met de openscheurende ravijnen aan de
ravijnlus in `scene()`. Zo heeft elk ravijn dezelfde wand, dezelfde rand van de overkant die
lager ligt dan de grond vooraan, de achtergrond erboven, het kleine gras en in de winter de
sneeuwrand. Het effect wordt per ravijn bewaard (`ravijnVast`) en pas opnieuw gemaakt als de
schaal, de wandplaat of het level verandert. Botsen gaat zoals altijd over `gaps`, daar is niets
aan veranderd.

Een gat boven een gang is hetzelfde ravijn, met dezelfde lage rand aan de overkant, maar de wand
houdt op bij het dak en daaronder zie je de gang. Dat tekent niet `scene()` maar de gatenlus, met
`ravijnGangTeken`: het effect (`ravijnTekenEen`, hetzelfde als in `scene()`) afgeknipt twee pixels onder
het dak, en daarover binnen de breuk `holteSchacht`, de overgang van aarde naar het steen van de gang.
De zon op de wand staat daar uit, want het licht komt uit de lichtkaart. Eerst had zo'n gat een eigen
tekening met de overkant op de kruin, en lag de rand in Jager 3, Test 4, Test 10 en Test 11 dus even
hoog als de grond vooraan. Dat geldt ook voor een ravijn dat boven een gang openscheurt (een rune of een
zegel): zolang het scheurt tekent het effect zichzelf in `scene()`, maar zodra het open staat is het een
gat in het dak (`ravijnBovenGang`) en telt het mee in `gatenTeken()` (met zijn effect in `g.fx`), de lijst
waar de gatenlus, `drawHolte` en de grond op tekenen. Botsen gaat nog steeds via `gatenMetRavijn` en `inGap`. Zonder dat bleef het
dak onder het gat dicht en zag je van boven een ondiepe kuil.

Een vijand die in een ravijn staat dat al openscheurde voor hij verscheen (zijn spawn ligt in
`ravijnGat`), komt niet meer: hij is erin gevallen. Anders stond hij boven het gat in de lucht. Wie
er al stond valt erin (`ravijnValt`). Zo werkte de valkuil in de oude Vorst 2 en 5: fosforslangen en
zwaardvechters blijven stil staan tot ze je zien, dus een rune die van verder weg de grond onder ze
openscheurt, neemt ze mee. Hyena's vallen hier buiten, want die komen van de rand van het beeld.

In de winter valt er geen sneeuw in een gang (`drawSnowfall` dooft onder de grondlijn met
`holteDiepT`), en treden in een gang (een terras met een negatieve `h`) krijgen de kale steen, niet
de besneeuwde.

In de bouwer is het precies hetzelfde ravijn, dus ook een level dat je daar maakt krijgt alleen de
nieuwe stijl. Twee dingen zijn er anders omdat je daar van verder weg kijkt (`viewZoom`): de ravijnen
worden rond het midden van de grondlijn geschaald, net als de grond (`ravijnZoom`, ook bij het vangen
van de achtergrond), en onder de wand komt de donkere bodem (`ravijnBodemVul`), want uitgezoomd reikt
het beeld dieper dan de wand. Versleep je een ravijn, dan wordt het effect opnieuw gemaakt; dat kost
minder dan een tiende milliseconde.

### De zon op de wand van een ravijn

De wand in een ravijn is de overkant: verder weg dan de grond vooraan, dus nooit lichter. De rand
aan de kant van de zon werpt er een schuine schaduw op, onder dezelfde hoek als waaronder de zon
in een gang binnenvalt (`LK.zonHoek`, `zonRechts`). Boven die lijn vangt de wand gedempt licht,
eronder ligt hij in de schaduw. Zo komt het licht in elk gat uit dezelfde richting als de zon in
de lucht. `ravijnZonLicht(g, x0, x1, top, onder, knik, open, atop)` tekent dat; de waarden staan
in `RAVIJN_ZON`.

| waar | hoe |
| --- | --- |
| gewoon ravijn en openscheurend ravijn | via het haakje `opLicht` van de module (`ravijn/ravijn-effect.js`), op het eigen canvas van de wand met `source-atop`: alleen op de wandpixels, nooit op de achtergrond erboven. `knik` is de verticale rek (`ravijnRek`), zodat de lijn in beeld de goede hoek heeft, en `open` is `fx.p`: de schaduw groeit mee met het openscheuren |
| gat boven een gang | niet: daar doet de lichtkaart het |

's Nachts is het verschil kleiner: de sterkte schaalt met `gloedSterkte` van het uitzicht (0,30
overdag), met `RAVIJN_ZON.nacht` als ondergrens. In de winter is de schaduw blauwig
(`RAVIJN_ZON.winter`): sneeuw en steen in de schaduw worden koel, niet grauw. De sneeuwrand van het
openscheurende ravijn komt na de wand en blijft dus wit.

De kaart hangt alleen af van de vorm van het level, dus elke cel wordt een keer uitgerekend. Wat
vast is gaat in een keer (`lkKaart`), de stralen per kolom zodra hij nodig is, en `lkVooruit`
rekent elk beeld `LK.budget` ms vooruit, vanaf Amir naar buiten: zo is de kaart af voor je
beneden bent. Het kaatslicht gaat met lopende sommen (`lkSom`), en de plaatjes worden eerst in
het geheugen gezet en per beeld een keer overgezet (`lkPlaatjes`). Zonder die twee kostte het
kaatslicht 1,2 seconde op Test 10, nu 70 ms; de hele kaart is een halve seconde, in stukjes.
Verandert de vorm (in de sandbox) of een regelaar, dan begint hij opnieuw (`lkSleutel`).

**De kaart wordt in twee delen getekend**, zodat de personages minder donker zijn dan hun
omgeving zonder dat hun tekencode iets van licht weet. Het eerste deel (`'wereld'`) komt vlak voor
Amir, na alles wat achter hem staat; het tweede (`'allen'`) komt na alles (na `drawWind`) en valt
dus ook over Amir, de vijanden en wat er voor hen langs komt, en daarin zit ook de zon. Per cel
worden de twee zo uitgerekend dat de wereld samen precies het hele donker `a` krijgt:
`a2 = LK.personage * a` voor iedereen, en `a1 = 1 - (1 - a) / (1 - a2)` voor de wereld eronder,
want `(1 - a1)(1 - a2) = 1 - a`. De personages krijgen alleen `a2`. Teken dus niets tussen Amir en
het tweede deel wat bij de wereld hoort, want dat mist het eerste deel. De ooggewenning ligt als
dekking over beide delen; dat is niet precies hetzelfde als het donker zelf verminderen, en in Test
10 scheelt het op de wand ongeveer een punt helderheid.

De regelaars staan in de sandbox onder **Licht onder de grond** (donker, ondergrens, gewenning,
personages, zon, kaatslicht, warm); elke klik laat ze allemaal zien, zodat je ze in `LK` kunt
overnemen.

**Ooggewenning** (`lkGewenning`): hoeveel licht er rond Amir is, staat al in de kaart (`lk.licht`,
het licht per cel zoals het getekend wordt), dus er wordt niets uit het beeld teruggelezen.
`lkRondAmir` neemt het gemiddelde van de luchtcellen om hem heen. Hoe donkerder daar, hoe meer van
het donker van de kaart wegvalt, tot `LK.gewenning`, en zijn ogen doen er `LK.gewenTijd` seconden
over (op de speltijd, dus ook de speelrobot ziet het). Diep in een gang wordt het zo na een paar
tellen lichter, en loop je naar een gat of een uitgang, dan komt het donker terug. Gemeten in Test 10:
zonder gewenning zakt het lange donkere stuk tot helderheid 30, met gewenning blijft het rond 44;
bij de uitgang komen beide weer bij elkaar uit. De zonnegloed in de kaart valt er niet onder.

**De ondergrens** (`LK.minLicht`) houdt het spel speelbaar: donkerder dan dat deel van het licht
wordt de kaart nergens, hoe weinig hemel een plek ook ziet. Zo blijven de vloer, de randen en de
treden te lezen. Het is een grens op het donker van de kaart, niet op het beeld: de tegels van de
gang zijn zelf al een beetje donker, en de lichtlaag komt er nog overheen.

**De schaduw van Amir** ligt op dezelfde vloer als waar zijn voeten op komen (`grondVloer`, net
als in `updateJump`), dus beneden in een gang op de bodem. Het gat eruit knippen gebeurt alleen
bovengronds: beneden is een gat erboven geen rand.

**Boven het dak loopt de aarde over in steen, en dat is materiaal, geen kleur.** Het grondpakket
boven een gang en de wand van het gat erboven zijn aarde, de gang is steen. Onderin het pakket
wordt de wandtegel van de gang zichtbaar (`holteOvergang`, over `HOLTE_OVERGANG` eenheden), op
precies hetzelfde ankerpunt in de wereld als de gangwand. Onder een gat ligt daardoor op de
daklijn aan beide kanten hetzelfde steen en loopt het patroon gewoon door; naast een gat hangen
er de tanden van het dak onder. Niet proberen de naad weg te poetsen met een tint of door kleuren
gelijk te trekken: dat is geprobeerd, en het gaat mis zodra het uitzicht of de lichtlaag anders
is. Meten deed het wel, en dat is de manier om een wijziging hier na te kijken: helderheid per
rij over de naad, en geen sprong van meer dan een paar punten.

De opbouw, van boven naar onder:

| waar | wat |
| --- | --- |
| naast een gat | de vloer van de savanne, dan aarde die overloopt in steen, en dan de tanden |
| in een gat (`holteSchacht`) | de wand van het ravijn zonder de nevel en het zwart van een afgrond, onderaan de overgang naar steen |
| buiten de gang | dichte rots, onder het dak |

Hoe licht of donker elk daarvan is, komt uit de lichtkaart. Het steen zit alleen boven een gang
en loopt voorbij de uiteinden over `HOLTE_UITLOOP` uit. Het ravijn boven een gang houdt twee
pixels onder het dak op, op een hele beeldpixel (`heelPx`): waar twee zachte randen op dezelfde
lijn liggen schijnt er anders een haarlijn doorheen.

Alles wat binnen `r` en `l` van een gang staat, staat op de bodem: vijanden, decor,
kalebassen en de fakkels. Een level kan dus onder de grond eindigen; de wand van
de gang houdt je dan achter de fakkels tegen, een klif is niet nodig. Dat werkt omdat
`grotTerrein` zonder raster `-Infinity` geeft en geen 0: gaf hij 0, dan trok `terrainH` alles in
de gang weer naar de savanne, en dat is precies waarom de vijanden in een gang eerst boven
stonden en de fakkels daar niet te halen waren.

Twee hulpjes houden boven en beneden uit elkaar. `gatOp(x, base)` is `inGap` voor wie op
hoogte `base` staat: beneden in een gang is een gat erboven geen rand, dus een vijand loopt er
onderdoor. `vloerBij(x, h)` is de vloer voor wie op hoogte `h` staat: boven een gang de
savanne, erin de bodem. De vijanden rekenen hun vloer daarmee uit, en de sandbox zet een vijand
daarmee op jouw hoogte neer. Gebruik ze in plaats van `inGap` en `terrainH` als het om iets gaat
dat zowel boven als beneden kan staan.

**Terug naar boven** gaat via een tweede gat in het dak met treden erin. Een trede is een gewoon
terras met een negatieve `h`, dus de klimstukken van de terrassen, en `drawClimb` tekent ze in
een tweede ronde na de ravijnen (anders tekent de overkant van het gat over de bovenste heen).
Hoe licht ze zijn komt uit de lichtkaart. Reken zo:

- het dak ligt op 190, dus onder het dak mogen zijn voeten niet hoger dan -441 (`-HOLTE_DAK -
  CHAR_H`). Een trede hoger dan dat moet helemaal onder het gat staan;
- zijn rechterrand ligt minstens een halve Amir binnen het gat, anders staat hij bij het
  afzetten nog onder het dak en haalt hij hem niet;
- elke stap is minder dan de sprong (200); 150 is ruim;
- de bovenste ligt binnen een sprong van de grondlijn en loopt door tot de linkerrand van het
  gat: daar stapt hij de savanne op.

Zolang zijn voeten tussen het dak en de grondlijn zitten, houdt `holteBlok` hem binnen het gat,
want zijwaarts zit daar het grondpakket. Op de savanne boven een gang dragen de treden eronder
niet (`supportHeight`). Test 4 heeft zo'n trap: van 900 diep in zes stappen van 150 naar boven.

```
gaps:     [ {x: -1000, w: 620}, {x: -3400, w: 900} ],       ingang, en de uitgang van -3850 tot -2950
holtes:   [ {r: -540, l: -3850, diep: 900} ],
terraces: [ {r: -2850, l: -3850, h: -750}, {r: -3050, l: -3850, h: -600}, ... {r: -3650, l: -3850, h: -150} ]
```

`levelcheck.py` kijkt dit na onder `onder de grond`.

## ravijn in de winter

`RAVIJN_WINTER`, `ravijnWandNu()`, `ravijnSneeuwRand()`: het openscheurende ravijn in een winterlevel, de wand bij het laden omgekleurd naar blauwgrijze steen (alleen kleur, per pixel op helderheid), een getekende sneeuwrand en het berijpte gras

## elk level nakijken op decor boven een ravijn

`schoonLevel`, draait bij elk level; `schoonKomend` en `komendeRavijnen` houden hutten, keien, doornbossen, skeletten en speertekens weg waar later een ravijn openscheurt (rune of zegel), en `placeProblem` in de bouwer ook

## wat er staat waar een ravijn openscheurt

`RAVIJN_DECOR`, `ravijnDecor`, `ravijnDecorStap`: kalebassen, botten en dorpelingen vallen erin, planten, keien, doornbossen en de speer schuiven naar de rand of vervagen; alles in `rv` of `x0`, dus `ravijnReset` zet het terug
