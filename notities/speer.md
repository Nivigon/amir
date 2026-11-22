# De speer: werpen, draaien, renstoot

## renstoot: sprinten en dan stoten

`RENSTOOT`, `glijStart`, `glijUpdate`, `glijWolk`: vanuit een sprint neemt hij zijn vaart mee in de stoot en glijdt hij remmend door, met het stof van de lage zwaai bij zijn voeten; stopt voor een ravijn. In de sandbox onder Renstoot

## de draaiende speer: rollen om de lengteas in de vlucht

`DRAAI`, `draaiImgs`, `draaiBeeld(soort, t)`, `draaiTeken(img, soort, k)`: 36 frames per omwenteling in `design/speer/draai/`, `gewoon` (Amirs speer, even lang als `javImg`) en `val` (de speerval), op dezelfde schaal `k` als `javImg`, punt rechts op `tipY`. Amirs geworpen speer rolt alleen in de vlucht (`javSchacht`, op `jav.t`; met `vaanBlauw` ook blauw, en in `vaanVoorwerk`), de speerval alleen in de vlucht (op `sp.t`). Stilliggen, in een wand of in de grond is weer `javImg`. De frames komen uit `tools/draaispeer.py`, uit de video van Grok in `design/speer/bron/`: alleen frame 0 tot 17 daarvan was bruikbaar, de rest van de rol is dat stuk gespiegeld

## schorpioen, het projectiel, spannen en werpen, de geworpen speer

de speerworp; een geworpen speer raakt maar een vijand, ook als er twee op dezelfde plek staan (`javRaakt` met `javOp` en `jav.hit`), net als de steek (`swingUsed`), alleen de lage zwaai raakt er meer tegelijk; onder de grond houdt het dak van een gang de speer tegen (`javTegenDak`, hij valt terug) en een speer boven het dak heeft de savanne als vloer (`javFloor` met de hoogte van de speer, via `vloerBij`); de rode flits als Amir geraakt wordt gaat over een eigen doekje (`amirRood`), anders kleurt de hele rechthoek van zijn plaatje mee; wachten met een gespannen speer (ademen, trillen, glimmen) en afbreken met springen, bukken of de andere kant op staan in `WORP_WACHT`, `thrAfbreken`, `thrWachtBij`, `thrWachtZet`, en er wordt nooit vanzelf gegooid; `speerNaastAmir` zet een speer waar Amir niet meer bij komt (achter of in een doornbos, boven op een terras dat hij van deze kant niet meer op komt) naast hem, nooit over een ravijn; `speerBereikbaar` rekent dat uit over de vloeren om hem heen

## de vallende speer

`JAV.valHoek`, `javValDraai`, `javDirHoek`, `jav.kantel`: een speer in de toestand `val` (een vijand geraakt, uit een wand geschoten, tegen een gangdak) draait in de val met de punt voorover, in zijn eigen richting, tot `valHoek` graden. Op de grond raakt de punt eerst, en dan valt de schacht in `JAV.kantelT` seconden om de punt heen plat (`jav.kantel` in `javSchacht`), met een kleine natril. Vroeger bleef hij in de hoek van het moment hangen en sprong hij bij de landing in een beeld plat.

## omlaag mikken: van een hogere laag naar beneden (`worpOmlaag`, `THR_OMLAAG`, `thrOmlaag`)

Met `worpOmlaag: true` in een level (alleen Test 71) of de sandboxknop **Aim down** (`sbWorpOmlaag`, onder Speerworp)
breekt pijl omlaag tijdens het spannen de worp niet af (`thrAfbreken` in de lus slaat het dan over), maar laat hij de
punt zakken: zodra de eerste trap uitgetrokken is (`THR_DRAW1`) loopt `thr.om` zolang de pijl ingedrukt is van 0 tot
`THR_OMLAAG.max` (60 graden) in `t` (0,9 s), en losgelaten blijft de hoek staan. Hij houdt de pose van frame
`THR_WIND`, maar met de speer schuin omlaag: vier houdposes (`THR_OMLAAG_FR`, `speerworp_omlaag_08`, `_18`, `_30` en
`_45` in de map van de speerworp, lui geladen met `thrOmLaad`), en `thrOmBeeld` kiest de dichtstbijzijnde (onder de 4
graden het gewone frame, boven de 45 blijft de laatste staan). De 18 is een Grok-beeld (image-to-image vanaf
`speerworp_06`), de 8, 30 en 45 zijn die pose met de speer om zijn hoofd gedraaid; elk heeft zijn eigen speerpunt, waar
het richtstreepje en het glimmen beginnen. Laat hij los vanaf 4 graden omlaag, dan speelt hij niet de gewone frames 7 tot 19 maar
de worp omlaag (`THR_OMW`, `speerworp_omlaag_worp_00` tot `_06` en `speerworp_omlaag_op_00` tot `_12`): uit een
Grok-clip (test3, vanaf de 18-graden pose) zakt hij in een diepe uitval en gaat de speer op worp 4 weg (`thrOmWLos`),
daarna komt hij omhoog uit een tweede clip (restand, met begin- en eindbeeld: het eind is `speerworp_19`, 96% overlap).
`thr.frame` telt gewoon door tot `thrOmWEind`. De speer vertrekt van zijn punt op het losframe (`THR_OMW.punt`, laag
voor hem, zo'n 0,7 Amir vooruit) in plaats van `THR_TIP` op hoofdhoogte: hij komt dus lager uit zijn hand en raakt van
boven dichterbij dan de metingen hieronder (die zijn van voor deze worp). Na de worp omlaag is er geen tweede speer
(DUBBEL). Zonder de plaatjes binnen (`thrOmWKlaar`) gooit hij met de gewone frames.

Hoe het mikken omlaag werkt is een keuze (`MIK`, `mikModus`): in Test 71 (`mikKeuze: true`) aan het begin en na R op
het scherm van `duoKeuze` (rij Aiming down, `duoKeuze.mik`, onthouden in localStorage), in de sandbox met de knop
**Aim** naast Aim down (`sbMikModus`). Vijf versies, om te vergelijken of het streepje het niet te makkelijk maakt:
`streep` (zoals het was), `zonder` (geen streepje, de houdpose zegt de hoek), `kort` (het streepje alleen de eerste
`kortZie` s na het eerste omlaag, dan vervaagt het in `kortWeg` s; `thr.omStart`), `wiebel` (een keer omlaag en de punt
gaat vanzelf heen en weer tussen 0 en `wiebelMax` graden, `wiebelT` s per kant, geen streepje: loslaten op het goede
moment) en `tril` (het streepje blijft, maar wie langer dan `trilNa` s gespannen staat wijkt af, tot `trilMax` graden
na `trilVol` s, willekeurig; `thr.losWacht`, want `thr.wacht` begint opnieuw bij frame 7). Nagemeten in Chromium: de
wiebel loopt 0 tot 45 en terug, en tril geeft na 3,5 s gespannen 3 tot 6 graden afwijking, na 0,7 s geen. Het richtstreepje van de schaalworp (`drawThrowRicht`) wijst de hoek, en `looseSpear`
gooit onder vlak met de volle snelheid van de vlakke worp (geen boog, `thr.lob` blijft uit). Bukken kan tijdens het
spannen toch niet (`canDuck` vraagt `!throwing`).

Waarom: vlak vliegt de speer van boven ver over iedereen heen. Nagemeten op 1280x720 vanaf een laag van 300 hoog, Amir
op de rand: lijfhoogte (100 tot 250) op 1500 tot 1800 px vlak, 700 tot 930 op 18 graden, 525 tot 680 op 30, 350 tot 490
op 50. Dichter dan zo'n 250 px is niet te raken, want de speer komt pas zo'n 185 px voor Amir uit zijn hand: een vijand
die vlak onder de rand staat raak je van boven niet. Vanaf 450 hoog raakt rond 11 graden op zo'n 700 px.

In Test 71 (Playwright, 1280x720): gebukt aan de rand blijft de bandiet op 700 px in rust; opstaan, 17 graden omlaag,
treffer (3 naar 2 levens), hij wordt wakker en rent naar de wand; terug van de rand en bukken, na zo'n 3 s is hij weer in
rust. Hij blijft dan op zo'n 140 px van de wand staan, en daar is hij van boven niet te raken; terugkruipen naar de rand
wekt hem op zo'n 375 px weer, want hij kijkt omhoog naar de rand. De speelrobot loopt het level zonder vijanden uit en komt
met vijanden vechtend tot de schildbandiet (zoals in Test 61). Op 852x393 raakt dezelfde worp ook.


## de mik-rig: vrij mikken met losse delen (`RIG`, `rigMik`, Test 72)

Een proef voor de jacht, waar mikken de kern wordt. In plaats van een plaatje per hoek tekent het spel Amir tijdens het
spannen uit losse delen (`karakters/amir/mikrig/`, geknipt uit de Grok-pose van 18 graden omlaag): het lijf
(`rig_lijf`), de werparm (`rig_arm`, draait om de schouder `RIG.sch` met `RIG.elleboog` keer de hoek, zodat de elleboog
omhoog gaat als hij omlaag mikt), het hoofd (`rig_hoofd`, knikt `RIG.kop` keer mee, hooguit `RIG.maxKop`) en de speer: het
projectiel-plaatje (`javImg`) op 0,867, dat achter zijn hoofd om `RIG.piv` draait en dus op elke hoek heel is. Pijl op en
neer tijdens het spannen kiest de hoek (`thr.rigH`, plus is omlaag) van `RIG.min` (-30) tot `RIG.max` (45) met `RIG.snel`
graden per seconde (`rigMikStap`); pijl omhoog springt dan niet en pijl omlaag breekt niet af.

Loslaten speelt de worp (`thr.rigW`): vanaf `RIG.omlaagVanaf` (28) graden de worp omlaag (de Grok-clip test3: twee frames
met de speer in de hand, dan worp 5 en 6 en het opstaan uit `THR_OMW`), daaronder de gewone worp (frame 7 tot 19, met frame
10 zonder de veeg van de speer). In de frames met de speer in de hand (`gewoon_*`, `omlaag_*`, met `_lijf`, `_speer` en bij
de gewone ook `_voor`: hoofd en vuist erover) draait de speer om de vuist naar de mikhoek, en de vliegende speer vertrekt
waar die punt staat (`thr.rigTip`). Het beeld wordt elk frame in een eigen canvas samengesteld (`rigCv`, `rigBeeld`) en als
worpframe getekend; schaduw en licht worden daarom elk beeld opnieuw gebakken.

Test 72 (Aim rig) is een proefveld: een trap van 150 tot 600 hoog en weer terug, geen vijanden (`vredig`), geen einde
(`geenEinde`, eruit via het menu) en na elke worp meteen een nieuwe speer (`speerOneindig`). In de sandbox de knop
**Aim rig** onder Speerworp. Om de rig los van het spel te bekijken is er ook een artifact (Amir mik-rig proef).
Nagekeken in Chromium: de hoeken -20, 0, 16, 37 en 45 gooien op die hoek, het pad wisselt op 28 graden, geen fouten.

## De sprintgreep (kit-lijst W1, in de maak)

In volle sprint (495 px/s) was het raam om E te drukken bij je speer maar ongeveer een tiende seconde. Met de
sprintgreep (`SPRINTGREEP`, `sgDruk`, `sgStap`, `sgDuikZet`) mag E eerder: ligt je eigen speer of een losse speer
tot `vooruit` (170 px) plus de reik voor je, dan onthoudt het spel de druk `buffer` (0,3 s) en pakt Amir hem zodra
hij binnen bereik is, met `extra` (45 px) meer reik en zonder af te remmen. Hij leunt even voorover (`duik`, `hoek`,
`zak`; alleen in beeld, met de frames die er zijn). Het pakken loopt door `losTrek` en `eigenSpeerPak`, dus een
skelet, een speer in een runeschijf en een volle hand en rug gaan zoals altijd.

Nu alleen in de sandbox, knop **Sprint grab** onder Speerworp (`sbSprintGreep`), of een level met `sprintGreep: true`
(geen level heeft het). Gemeten in Chromium: zonder greep mist E op 211 px, met greep pakt E op 121 tot 211 px.

## de Pathfinder Spear: het rode vaantje en de prooi (`PATHFINDER`, `PROOI`, `javTeken`, `pfStap`, `prooiRaak`)

Gevraagd (22-11-2026): een lichte upgrade van de speer voor de winkel van Co-op, naar een groep binnen de speerstam
(Mkuki) die meerdere krijgers dragen. Het werd de vleugelspeer met een houten schacht, een rood-witte kralengrip, een
rood bandje om de binding en een rood vaantje dat meewaait. De art komt uit Grok (`design/speer/pathfinder/bron/`), door
`tools/pathfinder_speer.py` op de lengte en dikte van `speer_projectiel.png` gezet (624 px lang, schacht 17 px tegen 15):
de dop, de greep en de kop houden hun vorm en het hout ertussen rekt mee, want de bron op een schaal geschaald gaf
een schacht twee keer zo dik en dan leek hij korter dan de gewone; het vaantje is los,
in vier standen (stil, licht wiegen, wind, harde wind).

De rand (22-11-2026): verkleind in het spel viel de schacht weg tegen het zand, want de Grok-plaat had een dunne,
half doorzichtige bovenlijn en geen glimlijn of schaduw. `pathfinder_speer.py` (`rand`) legt er nu de rand van de gewone
speer op: een dekkende donkere lijn om het hele silhouet (`RAND_LIJN`), boven een lichte glimlijn (`RAND_GLIM`) en onder een
zachte schaduw (`RAND_SCHADUW`), dezelfde waarden als in `speer_projectiel.png`. De punt wordt gemeten zonder die schaduw,
dus `PATHFINDER` bleef gelijk.

De kleuren (22-11-2026, op verzoek): ook met de rand bleef hij in de vlucht op een gewone speer lijken (bruine schacht,
rood vlekje bij de kop). `pathfinder_speer.py` (`kleur`) kleurt de bron nu per stuk om met zijn eigen licht en schaduw: de
schacht ivoor (`IVOOR`), het blad creme (`CREME`, vanaf `BLAD`) en de greep effen rood (`ROOD`, een gladde ronding in plaats
van de rood-witte kralen). Dop, dwarsstuk, bandje en vaantje blijven zoals ze waren.

- **De soort.** `SPEER_SOORTEN.pathfinder`, in het veld van het vaantje (`speerBlauw`, `rugSperen[].blauw`, `jav.blauw`,
  `losseSperen[].blauw`). Je koopt er een per speerplek (`koop.pathfinder` telt, `pfAantal`; in de sandbox de knop: een).
  `pfStap` maakt elk beeld zoveel gewone speren die je draagt Pathfinder-speren als je er bezit min wat er al is (`pfTel`:
  hand, rug, in de lucht, los op de grond), de rug eerst; een rekspeer blijft gewoon zolang je ze allemaal hebt. Welke in je
  hand zit kiest de speervolgorde (zie `notities/speer-inventory.md`).
- **Het beeld.** `javTeken(soort, k, wind, windX)` vervangt overal het tekenen van `javImg`: op de rug, in de worp (zonder
  de draai-frames), liggend, in een wand, in een oefendoel, het baken en de losse speren van een teamgenoot. In Amirs handen
  zit nog de gewone speer in zijn sprites, tot de speer los over de animaties komt (daar wordt aan gewerkt).
- **Het vaantje.** `pfVaanTeken` hangt het aan het knoopje (`PATHFINDER.knoop`) en draait het altijd naar beneden in de
  wereld (de inverse van de transformatie), en spiegelt het als het de andere kant op moet waaien. De sterkte: in de vlucht
  1, vallend 0,6, vast 0,15, op de rug de vaart van Amir (`pfV`, `PATHFINDER.wind`), liggend plat langs de schacht.
- **De prooi.** Een geworpen Pathfinder-speer die raakt (`worpTref` en `jav.blauw`, in `gifRaak`) markeert de vijand
  `PROOI.duur` (3) s. Hij loopt `PROOI.traag` (20%) trager (`prooiTraag`: van wat hij dit beeld opschoof gaat dat deel er
  weer af; gemeten: een rennende bandiet 8,0 px per beeld, gemarkeerd met 0,1 was het 7,2), en elke treffer op hem kost
  `PROOI.extra` (een half) leven meer (`prooiExtra`, in `fcHalf`, dus bij elke soort die `fcHalf` aanroept; de schildbandiet
  niet, die telt in schildstanden). Te zien: een rode rand om zijn silhouet (`prooiGloed`: zolang de lus van zijn soort hem
  tekent, krijgt elk plaatje een rode rand eronder; niet als het doorzichtig is, zoals zijn schaduw. De rand wordt per
  plaatje, uitsnede en maat een keer gebakken met de drop-shadow (`prooiRandBak`, `PROOI_RAND`) en daarna gewoon
  getekend: een live filter op elk plaatje maakte City Survival traag) en het vaantje op een stokje
  boven zijn hoofd (`prooiTeken`, vanuit `vijandHpBalk`), knipperend in de laatste seconde, feller op een extra treffer.
- **Sandbox:** Speer en spullen, Gif, **Pathfinder Spear** (`sbPathfinder`).

