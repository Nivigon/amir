# Een level donker maken

### Een level donker maken

De lichtlaag ligt over het hele beeld, dus ook over de grond en over Amir. Een level dat
er anders uit moet zien zet in zijn `SCENES`-blok een veld `licht` met de waarden die
afwijken (zie `LICHT`), en dat is hoe de nachtuitzichten (`dark_rots`, `dark_hart` en de andere
`dark_`-blokken) donker worden: een blauwgrijze
schaduw- en lichtkleur, een zwakkere gloed en een iets diepere onderkant. `aan` en
`sterkte` blijven van de regelaars (`L`, en `,` en `.`), ook in zo'n level: die zijn er
om te kunnen kijken wat de laag doet, en dat moet in elk level werken.

Het veld `dim` in `SCENES` is iets anders: dat zet alleen de achtergrond dieper, tot aan
de grondlijn. Wil je dat de hele wereld donkerder wordt, dan is `licht` het juiste veld;
wil je alleen dat de verte wegzakt, dan `dim`. Meestal gebruik je ze samen.
