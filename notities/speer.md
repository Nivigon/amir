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
het richtstreepje en het glimmen beginnen. Het richtstreepje van de schaalworp (`drawThrowRicht`) wijst de hoek, en `looseSpear`
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
