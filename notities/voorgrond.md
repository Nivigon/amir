# De voorgrond

### De voorgrond hoort bij elk level

Elk level heeft een voorgrond: de onscherpe laag vlak voor de camera die het beeld diepte geeft.
Dat is geen keuze per level maar standaard. Zet een level er zelf geen, dan krijgt het er een van
het spel (`vgStandaard`): ijl (`VG_STANDAARD.dicht`), over het hele level, met open plekken rond
alles waar je naar moet kunnen kijken: ravijnen en de plekken waar er later een openscheurt, zegels,
de rots met de rune (die reikt ver naar rechts, want de rots staat aan de kant waar Amir aankomt), de
poort (`muur`), de fakkels en het veld van de eindbaas. Zo verbergt hij nooit een rand, een schijf of
een vijand die je moet zien. De maten van die open plekken staan in `VG_STANDAARD`. De standaard hangt
aan het level zelf, dus ook een level uit de Maker krijgt hem.

Een eigen `voorgrond` in de definitie gaat voor de standaard (Test 11 heeft er een). Doe dat als een
level een plek heeft waar de voorgrond iets moet vertellen: dicht gras aan het begin, een schedel in
het gras bij een eindbaas. `voorgrond: false` zet hem uit; doe dat alleen met een reden.

De voorgrond heeft twee lagen (`VG_LAGEN`), van ver naar dichtbij, en daardoor zit er ook binnen de
voorgrond diepte:

| laag | schuift | grootte | onscherp | schaduw |
| --- | --- | --- | --- | --- |
| ver | 1,2 keer de wereld (1,4 verticaal) | 0,6 | een beetje (3) | 0,85 van de schaduw |
| dichtbij | 1,45 keer (1,8 verticaal) | 1 | veel (7) | de hele schaduw |

Beide lagen lezen dezelfde stroken; de verre laag heeft een eigen reeks, zodat de pollen niet op
elkaar staan, en staat wat dichter op elkaar omdat hij kleiner is. Losse stukken (`los`) staan alleen
in de dichtbije. In de winter staan er de besneeuwde versies (`winter` bij elke soort in `VG_SOORT`)
met een koelere, lichtere schaduw (`VOORGROND.schaduwWinter`), anders wordt de sneeuw bruin; 's nachts
staat hij dieper in de schaduw, naar de gloed van het uitzicht. De hele voorgrond kost zo'n 0,05 ms per
beeld: de plaatjes worden per soort, laag en tint een keer onscherp gemaakt en bewaard.

## voorgrond: de laag tussen de camera en Amir

`VOORGROND`, `VG_SOORT`, `VG_LAGEN`, `vgStandaard`, `drawVoorgrond`: onscherp gras, struiken, keien en een schedel vlak voor de camera, in twee lagen; schuift sneller dan de wereld, ook verticaal, en valt onder de grond weg. Elk level heeft er een (zie "de voorgrond hoort bij elk level")
