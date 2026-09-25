# Voorbeeld: hoe het ravijn eruit zou kunnen zien

Dit is een mockup, geen wijziging. Aan `amir-king-of-africa.html` is niets veranderd.
De tekening is gemaakt door een kopie van de HTML in een tijdelijke map te patchen en
die te renderen in de echte browser, met de echte sprites, de echte achtergrond en de
echte lichtlaag. Zo zie je wat het in het spel zou doen, niet wat het in een tekenprogramma
zou doen.

| bestand | wat |
| --- | --- |
| `voorbeeld-renew6.png` | voor en na, Renew 6, het ravijn van dichtbij |
| `voorbeeld-dark1.png` | voor en na, Dark Africa 1 |
| `voorbeeld-winter2.png` | voor en na, Winter 2 |
| `voorbeeld-heelbeeld.png` | voor en na, het hele scherm, zodat je ziet hoe het in de compositie ligt |

## Wat er in de mockup gebeurt

Zes dingen, precies de punten uit `ravijn-analyse.md`.

1. **De vlakke bodemvulling wordt uit de gaten geknipt.** Dezelfde `evenodd`-clip die de
   grondtegel al gebruikt, nu ook op de `bodemDonker()`-vulling eronder. Daarmee is de
   rechthoek met de kaarsrechte bovenrand weg. Let op: zodra je dat doet moet het gat wel
   zelf dichtgetekend worden, anders kijk je door het canvas heen. Dat is in de mockup
   opgelost door de verre wand ondoorzichtig te beginnen.

2. **De steen wordt echt omgeverfd.** Niet een platte vulling van 28 procent, maar een
   `color`-blend: tint en verzadiging van de grond, helderheid van het steen, daarna de
   oorspronkelijke doorzichtigheid terug. Grijs steen wordt daarmee aarde in plaats van
   lila. `rots_vulling.png` gaat door dezelfde bewerking, zodat het diepste stuk meeloopt.

3. **De rand waar je op staat krijgt dikte.** Een ondoorzichtige band onder de kruin, met
   een grillige onderkant (niet kaarsrecht, anders ligt er weer een liniaal over het gat),
   en daaronder de slagschaduw van die rand over de volle breedte in plaats van alleen twee
   kantjes van 34 px.

4. **De overkant zakt onder je voeten.** Nu ligt hij 11 px lager, in de mockup ongeveer
   een twintigste Amir plus de dikte van de rand, en de plukken worden niet meer vlak
   afgeknipt.

5. **De diepte speelt zich af op het stuk dat je ziet.** Nevel en donker lopen van de
   grondlijn tot de onderrand van het beeld, niet tot anderhalve Amir daaronder. Daardoor
   loopt het gat werkelijk weg in het donker in plaats van als een gelijkmatig verlichte
   plaat te blijven liggen. De kleur komt uit `mistColor` van het uitzicht, dus Dark Africa
   krijgt zijn eigen ravijn en niet de savannebak.

6. **Detail.** De lichte streep bovenop de rand is getemperd, de randtegel wordt om en om
   gespiegeld zodat je de herhaling niet meer ziet, en de breuklijn is dunner en schaalt mee
   met het scherm.

## Wat nog open staat

De mockup houdt `rotstextuur.png` en `ravijn_rand.png`. Dat is bewust: zo zie je hoeveel
er alleen al te winnen valt met de opbouw en de gradatie, zonder ook nog van steensoort te
wisselen.

Ik heb ook geprobeerd de overkant uit `grondrand.png` zelf te tekenen (dezelfde grond,
verder weg). Dat werkte niet: het loopvlak van die tegel leest als een vloer waar je op
kunt staan, en dat is precies wat de andere kant van een ravijn niet moet uitstralen. Alleen
de wand van die tegel gebruiken kan wel, maar die heeft een eigen donkere onderrand en stopt
dus met een naad. Als je de steensoort wilt vervangen, is de grotroute (`klif_bovenrand.png`
plus `rots_vulling.png`) de betere.

Alles in de mockup zit aan getallen die je kunt draaien: hoe donker het onderin wordt, hoe
ver de overkant zakt, hoe zwaar de nevel is. Het "na" hier is aan de donkere kant. Dat helpt
de leesbaarheid (een gat ziet er gevaarlijk uit), maar het is een keuze, geen noodzaak.
