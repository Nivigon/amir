# Zegeltekens: wat elk teken doet

De tekens op een zegel betekenen met opzet niets: geen dier, geen ding, geen letter. De speler
leert ze herkennen aan wat ze doen. Dat werkt alleen als een teken altijd hetzelfde doet, dus
elk teken krijgt een bestemming, en die blijft.

De vormen staan in `ZEGEL_TEKENS` in de HTML. In de sandbox zet de rij Zegelteken ze op alle
zegels die er liggen.

| teken | bestemming |
| --- | --- |
| `rune` | de speler activeert iets. Zo zijn de zegels begonnen, en ook de runeschijf op een rots of in de rotswand, die een ravijn of een grot opent |
| `teken2` | ook een vijand of een dorpeling activeert hem, en de speler ook (`vijand: true`): de val. Dorpelingen lopen nu niet, dus in de praktijk zijn het de vijanden |
| `teken1` | nog open |
| `teken3` | nog open |
| `teken4` | nog open |
| `teken5` | nog open |
| `teken6` | nog open |
| `teken7` | nog open |
| `teken8` | nog open |

## Een teken aanwijzen

Wijs een open teken pas aan als er een nieuwe manier van activeren is, en dan voor precies dat
ene ding. Zet het in deze tabel en in het commentaar boven `ZEGEL_TEKENS`, en laat het spel dat
teken dan vanzelf kiezen, zoals `zegelTekenVan` nu `teken2` kiest bij `vijand`.

Twee zegels met een ander teken vlak na elkaar: kies dan tekens met een heel andere omtrek.
5 en 7 zijn een doorlopende lijn, 2, 3 en 4 twee losse stukken naast elkaar, 6 is de enige met
een stip. 2 en 3 lijken van ver op elkaar.

Mogelijke bestemmingen, nog niet gekozen: iets dat alleen aangaat zolang je erop staat (een
drukplaat), iets met een tijd, iets waar een speer in moet, iets dat alleen de baviaan of een
kei zwaar genoeg voor is.
