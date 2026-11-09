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

## de stadsvoorgrond

`VG_STAD`, `vgStad`, `vgMixKies`, `vgStadKnoopVrij`, `vgLaadLevel`: met `voorgrond: 'stad'` krijgt een level in plaats
van gras spullen uit de straat. Alle tien de levels van De Gouden Poort hebben het (gevraagd, "Gemengd" uit drie
proefbeelden: markt, steeg en muurtje); de andere stadslevels houden `voorgrond: false`.

- **De soorten** staan gewoon in `VG_SOORT`, met `lui: true`, zodat ze pas laden als een level ze gebruikt
  (`vgLaadLevel` in `laadLevel`): `kruik`, `mand`, `potten`, `stenen` (uit `design/stad/voorgrond/`, geknipt uit
  `voetdecor.png` door `tools/stad_voorgrond.py`), `muur` (`leem_rand.png`), `rek` (het wapenrek) en `gordijn`,
  `gordijn2` (twee doeken uit `design/stad/gordijn/`). Nieuw in een soort: `alleen` (alleen in die laag van
  `VG_LAGEN`, 0 ver en 1 dichtbij; het rek staat alleen ver, de doeken alleen dichtbij) en `boven` (hangt van de
  bovenrand het beeld in, zwaait om zijn bovenkant; `onder` is dan het deel boven de rand).
- **Gemengd.** `vgStad` hakt het level om de `VG_STAD.stuk` (1500) in stukken en geeft elk een thema uit
  `VG_STAD.themas` (markt, muur of kaal, met hun kans), vast per level: het zaad komt uit de naam. Twee gelijke
  stukken naast elkaar worden een strook. Een strook heeft een `mix` (soort en gewicht) in plaats van `struik`
  en `kei`, en een eigen `dicht` (het muurtje dichter, zodat het een muur wordt).
- **Open plekken**: het einde, een poort (`poorten`), de binnenkant van een huis (`binnen`, een eigen strook),
  het veld van Nyundo (`brutus.van` tot `tot`) en een arena (`VG_STAD.open`). Bij een knooppunt van een stadje
  (`straten`) slaat `drawVoorgrond` de plek over (`vgStadKnoopVrij`): het pad `kruis_voor.png` heeft al zijn eigen
  donkere voorgrond.
- **De zoom.** Een stadslevel speelt uitgezoomd; de stadsvoorgrond schaalt en schuift met `viewZoom()` mee, zodat hij
  zich tot de straat verhoudt zoals het gras tot de savanne. De gewone voorgrond doet dat niet (zoals voorheen).
- **Donker**: `VG_STAD.donker` (0,6) maakt hem donkerder dan het gras, een silhouet in de felle straat; het
  voorbakken in `warmBouw` gebruikt dezelfde tint.
- **De hoogte in**: zodra de camera omhoog gaat (`camY` boven nul: een galerij, een trap, een dak) vervagen de
  hangende doeken over een halve Amir, anders hangen ze voor de daken. De rest schuift zoals altijd onder de rand weg.
