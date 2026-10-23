# Het weer

### Het weer

Een level zet het weer met `weer: [{x, soort, sterkte}]`. Voorbij `x` geldt die soort tot het
volgende punt, de overgang loopt over `WEER.overgang` px en voor het eerste punt is het droog.
Zonder het veld blijft het oude gedrag: in een winterlevel het sneeuwplan per potje (`planSnow`),
verder geen weer. `sterkte` is standaard 1, hoogstens 1,5.

Elke soort is een mengsel van zes lagen (`WEER.lagen`: regen, onweer, storm, zand, sneeuw, jacht),
zodat de ene soort in de andere overloopt. De sneeuw zijn de gewone vlokken: `updateSnowfall`
vraagt `weerDoel()` en sneeuwt dan ook buiten een winterlevel. Wil je de grond ook wit, zet er dan
het veld `sneeuw` bij met dezelfde `van`.

Drie keuzes die vastliggen:

- **Weer maakt het beeld niet donkerder.** Geen waas over de lucht en geen donkere laag: regen maakt
  het hooguit een zweem koeler (`WEER.koel`), een storm legt alleen vlak boven de grond een stuifband.
  Zo is het gevraagd.
- **Een storm is een vlaag die niet ophoudt.** `weerWind` zet `gust` op een vlaag over de hele kaart
  (`gust.weer`), met een amplitude die golft. Alles wat al op `windAt` reageert gaat zo vanzelf mee;
  de planten gaan in een storm verder plat en fladderen sneller (`WEER.storm.buig`, `fladder`, in
  `drawVeg`). Waait het harder dan 1, dan staat een doek strak (`tekenWind` klemt op 1). Een nieuw
  ding dat in de wind beweegt hoeft dus alleen `windAt` te gebruiken.
- **Geluid**: de storm is `music/woestijnwind.mp3` als lus door een versterker (`stormSnd`,
  `weerVersterker`), de regen en de donder zijn gefilterde ruis uit de Web Audio API. Alles hangt aan
  `weerAc`, die `geluidOntgrendel` bij een tik op gang zet. Onder de grond klinkt het gedempt, en er
  valt geen weer (`holteDiepT`, net als de sneeuw).

Nog niet: onder een plafond of in een grot regent het gewoon door, en planten en keien hebben in de
sneeuw alleen hun aan-of-uit sneeuwversie. In de sandbox onder **Weer**; Test 13 laat alles zien.
