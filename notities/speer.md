# De speer: werpen, draaien, renstoot

## renstoot: sprinten en dan stoten

`RENSTOOT`, `glijStart`, `glijUpdate`, `glijWolk`: vanuit een sprint neemt hij zijn vaart mee in de stoot en glijdt hij remmend door, met het stof van de lage zwaai bij zijn voeten; stopt voor een ravijn. In de sandbox onder Renstoot

## de draaiende speer: rollen om de lengteas in de vlucht

`DRAAI`, `draaiImgs`, `draaiBeeld(soort, t)`, `draaiTeken(img, soort, k)`: 36 frames per omwenteling in `design/speer/draai/`, `gewoon` (Amirs speer, even lang als `javImg`) en `val` (de speerval), op dezelfde schaal `k` als `javImg`, punt rechts op `tipY`. Amirs geworpen speer rolt alleen in de vlucht (`javSchacht`, op `jav.t`; met `vaanBlauw` ook blauw, en in `vaanVoorwerk`), de speerval alleen in de vlucht (op `sp.t`). Stilliggen, in een wand of in de grond is weer `javImg`. De frames komen uit `tools/draaispeer.py`, uit de video van Grok in `design/speer/bron/`: alleen frame 0 tot 17 daarvan was bruikbaar, de rest van de rol is dat stuk gespiegeld

## schorpioen, het projectiel, spannen en werpen, de geworpen speer

de speerworp; onder de grond houdt het dak van een gang de speer tegen (`javTegenDak`, hij valt terug) en een speer boven het dak heeft de savanne als vloer (`javFloor` met de hoogte van de speer, via `vloerBij`); de rode flits als Amir geraakt wordt gaat over een eigen doekje (`amirRood`), anders kleurt de hele rechthoek van zijn plaatje mee; wachten met een gespannen speer (ademen, trillen, glimmen) en afbreken met springen, bukken of de andere kant op staan in `WORP_WACHT`, `thrAfbreken`, `thrWachtBij`, `thrWachtZet`, en er wordt nooit vanzelf gegooid; `speerNaastAmir` zet een speer waar Amir niet meer bij komt (achter of in een doornbos, boven op een terras dat hij van deze kant niet meer op komt) naast hem, nooit over een ravijn; `speerBereikbaar` rekent dat uit over de vloeren om hem heen
