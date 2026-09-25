# Waarom het ravijn als een rechthoek in het beeld ligt

Analyse, geen wijziging. Alles hieronder is nagemeten in de echte build (headless
Chromium, 1280x720, Renew 6 / Dark Africa 1 / Winter 2), niet geschat.

## Kort

Het ravijn is de laatste plek in het spel met een eigen steensoort. De grotten zijn
daar al vanaf gestapt ("rots is hetzelfde gesteente als een terras"), het plafond ook.
Het ravijn tekent nog altijd `design/rotstextuur.png` en `design/ravijn_rand.png`, en dat
is precies het probleem dat in CLAUDE.md bij `GROT_MASSA` beschreven staat: een eigen
massa in een andere kleur en een andere korrel leest als een rechthoek naast het level,
hoe je die kleur ook kiest.

Daar komen vier dingen bij die het erger maken dan bij de grotten, want een ravijn ligt
met zijn rand tegen `grondrand.png` aan, de meest verzadigde tegel van het hele spel.

## De vijf oorzaken, van zwaar naar licht

### 1. Er ligt een platte rechthoek in het gat, en dat is letterlijk zo

Regel in de bodemsectie:

    ctx.fillStyle = bodemDonker(); ctx.fillRect(0, groundY, W, ...)

Die vulling (`#2e211d`) loopt over de volle breedte van het scherm, ook over de gaten
heen. De tegel `grondrand.png` erna wordt wel netjes uit de gaten geknipt (`evenodd`
met `traceGap`), de vulling eronder niet. Gevolg: in elk ravijn ligt tussen de grondlijn
en de overkant een egale plak met een kaarsrechte bovenrand op precies `groundY`.

Bewijs: `bew_diag.png`. Daar staat dezelfde `bodemDonker()` even op magenta. Dat is de
band die je in het echte beeld als een donkere streep boven de overkant ziet liggen.

Op 720p is die band 41 px hoog (30 px boven de grondlijn plus 11 px eronder) van de
160 px ravijn die je in totaal ziet. Een kwart van het gat is dus geen rots maar
achtergrond en vulling, met een liniaal eroverheen.

### 2. Je kijkt door het gat heen naar de parallax

Boven `groundY` is de grondtegel uit het gat geknipt vanaf `top - 40`, dus daar zie je
de achtergrondlagen. Die schuiven met parallaxsnelheid, het gat schuift met
wereldsnelheid. De "overkant" beweegt dus ten opzichte van het ravijn waar hij in hoort
te liggen, en dat haalt elke dieptewerking onderuit.

Hetzelfde knipt de grasplukken van `ravijn_rand.png` vlak af: de clip begint op
`edgeCrust`, de plukken steken op de huidige schaal 69 px omhoog vanaf de overkant en
dus 58 px boven de grondlijn uit. In `bew_r6.png` en in jouw eigen schermafbeelding zie
je links een pluk met een rechte streep erdoorheen.

### 3. De steensoort past bij niets

Gemiddelde kleur, hele familie:

| bron | tint | verzadiging | helderheid |
| --- | --- | --- | --- |
| `design/rotstextuur.png` (ravijnwand) | 30 | **0,08** | **0,41** |
| `design/ravijn_rand.png` (overkant) | 30 | 0,08 | 0,38 |
| `design/klimmen/klif_bovenrand.png` | 22 | 0,10 | 0,38 |
| `design/grot/*` (keien, hangblokken) | 26 | 0,14 tot 0,34 | 0,28 tot 0,40 |
| `design/grondrand.png`, de wand | 27 | **0,51** | 0,38 |
| `design/grondrand.png`, het loopvlak | 29 | **0,66** | 0,57 |

De ravijnwand is de bleekste en de grijste steen van het spel, en hij staat direct
tegen de meest verzadigde tegel aan. De correctie die er nu op zit is

    g.globalCompositeOperation = 'source-atop';
    g.fillStyle = 'rgba(210,140,90,0.28)'; g.fillRect(...)

Een platte vulling van 28 procent. Die maakt het steen lichter, niet warmer: verzadiging
komt er nauwelijks bij. Over grijs heen met de nevelkleur van het level erbij wordt dat
lila, en dat is exact wat je ziet.

Bovendien heeft `gapArt()` maar twee sleutels, `winter` en `savanne`. Dark Africa krijgt
dus de savannebak: een warm getinte ravijnwand midden in een blauwe nacht. De globale
lichtlaag zet er daarna nog een multiply overheen, maar die kan een verkeerde tint niet
goedmaken.

Winter World is de uitzondering waar het wel werkt (`bew_win2.png`), en dat bewijst het
punt: daar valt de bleke grijze steen toevallig samen met de rest van het beeld.

### 4. De diepte gebeurt onder het scherm

De grondlijn ligt op `0,82 * H`. Je ziet dus `0,18 * H` ravijn, op 720p is dat 130 px.
Amir is op het scherm ongeveer `0,25 * H`, dus 180 px. De nevel en het donker zijn
uitgedrukt in veelvouden van Amir:

| effect | volle sterkte op | dat is | ligt op 720p |
| --- | --- | --- | --- |
| nevel (`hz`) | `groundY + 1,3 * amir` | +234 px | 104 px onder de schermrand |
| donker (`dg`) | `groundY + 1,25 * amir` | +225 px | 95 px onder de schermrand |
| helemaal zwart | `groundY + 2,2 * amir` | +396 px | ruim driemaal buiten beeld |

Bij de onderrand van het scherm is de nevel op ongeveer de helft en het donker op
ongeveer 0,20. Het hele verloop van "licht bij de rand" naar "je ziet niets meer" wordt
dus nooit gespeeld. Wat overblijft is een gelijkmatig verlichte plaat, en een plaat met
een rechte bovenrand is een rechthoek.

Ter vergelijking: `GAP_DEATH` is `1,6 * CHAR_H`. Speltechnisch is het gat 400 eenheden
diep, de tekening loopt door tot oneindig, en je ziet er 0,72 Amir van.

### 5. Twee stenen die elkaar raken zonder overgang

De rand van `grondrand.png` wordt met een grillige lijn afgekapt, er komt een zwarte
streep van 3 px langs, en daarachter begint meteen de vreemde grijze wand. Er is geen
dikte aan de lip, geen doorsnede van je eigen grond, geen schaduw van de overhangende
rand over de volle breedte (alleen twee kantjes van 34 px). De overkant ligt op
`groundY + 0,06 * amir`, dat is 11 px onder je voeten: dat leest als een richel net
onder de grond, niet als de andere kant van een kloof.

Kleinigheden in dezelfde hoek: de lichte hooglichtlijn bovenop `ravijn_rand.png` komt er
na de zwakke tint bijna wit uit (in de savanne leest dat als sneeuw), de randtegel
herhaalt elke 337 px met dezelfde vier grasplukken (op jouw schermafbeelding zie je de
herhaling), en zowel de streepdikte (3 px) als de amplitude van `gapJag` (ongeveer 6
plus of min 10) staan in schermpixels vast en schalen dus niet mee met het scherm.

## Wat er te winnen valt, op volgorde van effect

**A. De structuur kloppend maken.** De `bodemDonker`-vulling met dezelfde `evenodd`-clip
uit de gaten knippen, de overkant dieper leggen (ongeveer 0,18 tot 0,25 Amir onder de
grondlijn in plaats van 0,06) en de randtegel iets kleiner tekenen, zodat de grasplukken
niet meer boven de grondlijn uitsteken en niet meer vlak worden afgeknipt. Daarmee zijn
punt 1 en 2 weg en is er ook niets meer waardoor je de parallax ziet schuiven.

**B. De lip dikte geven.** De wand van `grondrand.png` zelf (bronrij 160 tot 305) een
strook naar binnen doortekenen, donkerder, met een schaduw van de overhang over de volle
breedte naar beneden. Dan gaat het van loopvlak naar jouw eigen steen in de schaduw naar
de overkant, in plaats van van ocher naar een zwarte streep naar grijs. Dit kost geen
nieuw plaatje en de kleur klopt per definitie.

**C. Dezelfde steen als de rest.** De grotdoctrine doortrekken: de overkant uit
`klif_bovenrand.png` (die heeft al een bovenvlak en een afbrokkelende rand) en de massa
uit `design/grot/rots_vulling.png` (naadloos in beide richtingen, wordt al voor het
plafond gebruikt). Dan is een ravijn van hetzelfde gesteente als de terrassen, de
kliffen en de grotten, en loopt winter vanzelf mee via `terPic()`. Het alternatief, als
je `rotstextuur.png` wilt houden, is hem echt gradueren (multiply naar de tint van de
grondwand, verzadiging naar ongeveer 0,3) in plaats van een platte vulling van 28
procent, en de cache per uitzicht bijhouden in plaats van alleen winter of savanne.

**D. De diepte op het zichtbare stuk leggen.** Nevel en donker niet in veelvouden van
Amir maar in delen van de zichtbare band (`groundY` tot `groundY + 0,18 * H`), zodat je
het verloop van scherpe rand naar niets echt ziet gebeuren. De kleur daarvan uit het
uitzicht halen (`mistColor`, `land`, de zon), niet uit een vaste bak.

**E. Detail.** De hooglichtlijn temperen, de randtegel per gat om en om spiegelen of met
een seed verschuiven zodat de herhaling verdwijnt, en de streepdikte en `gapJag` mee
laten schalen met het scherm.

Losse kans: `design/ravijn_bodem.png` (512 x 140, rotswand met keien en grasplukken)
staat er wel maar wordt nergens gebruikt. Dat is het plaatje voor een ondiep ravijn waar
je de bodem wel van ziet.

## Waar toestemming voor nodig is

De tekencode van het ravijn is gedeeld. Elke wijziging hierboven verandert hoe elk
bestaand level eruitziet, ook de bevroren reeksen. Dat is geen wijziging in een
leveldefinitie, maar het valt wel op, dus dat vraag ik eerst.

De sandbox heeft al knoppen onder "Ravijn" (Smal en Breed). Daar kunnen er een paar bij
om de diepte van de overkant en het verloop los aan en uit te zetten terwijl we het
bouwen.
