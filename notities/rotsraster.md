# Rots als raster en als terras

### Rots als een raster van cellen

Een rotsgebied is geen kamer maar terrein: een raster waarin elke cel vol of leeg is.
Amir loopt door de lege cellen, en rots kan net zo goed boven of naast hem zitten als
eronder. Je tekent het met de hand uit.

| veld | wat |
| --- | --- |
| `x` | wereld-x van de linkerrand van het raster (dus negatief) |
| `cel` | celbreedte in wereld-px (standaard `GROT_CEL`, 120) |
| `hoog` | celhoogte, als factor op de standaard (standaard 1 = 150 eenheden) |
| `y` | onderrand van het raster boven de grondlijn, in cellen (standaard 0) |
| `grid` | de rijen van boven naar beneden; `#` is vol, al het andere leeg |
| `seed` | dezelfde seed geeft elke keer dezelfde verstrooiing |
| `strooi` | hangblokken, richels en keien vanzelf neerzetten (standaard `true`) |
| `massief` | de volle cellen blokkeren (standaard `true`) |
| `decor` | met de hand erbij: `[{k, x, y, f, s}]` |

Een cel heeft twee maten, en dat is met opzet, want het spel rekent zo overal. De
**breedte** staat in wereld-px en ligt dus vast, net als bij `gaps`, `terraces` en `rocks`,
en net als Amir zijn looptempo. De **hoogte** staat in sprite-eenheden (`GROT_HOOG * CHAR_H`
= 150, precies een terrastrede) en schaalt dus mee met Amir, net als `terraces.h`.

Dat verschil is niet vrijblijvend. Zou de hoogte ook in wereld-px staan, dan komt Amir op
een kort scherm kleiner uit terwijl de cel gelijk blijft, en is een blok van één cel ineens
niet meer te halen. Nu is een cel overal 150 eenheden en Amir zijn sprong overal 200, dus
één cel klim je altijd, twee cellen nooit. Op een telefoon zijn cellen daardoor breder dan
hoog en op een groot scherm hoger dan breed; rond het standaardformaat zijn ze vierkant.
De losse stukken worden allemaal op één schaal getekend (zie hieronder), dus er wordt
nergens iets uitgerekt.

Wat dat voor het ontwerp betekent: één cel is een trede, twee cellen is een gang waar je
rechtop door loopt maar je hoofd stoot als je springt, drie cellen is ruim, en een gat van
één cel hoogte kun je niet in.

Buiten het raster is het lucht, behalve onder de laatste rij: daar loopt de aarde door.
De bovenkant van je rots is dus ook de bovenkant van het level, met de hemel erboven.
Moet de massa doorlopen tot buiten beeld, maak het raster dan hoger.

### Rots is hetzelfde gesteente als een terras

Dit is de kern, en het is de derde poging: een rotsgebied krijgt geen eigen steensoort.
Elke volle cel hangt onder precies een cel waarvan de buur boven leeg is (loop je van een
volle cel omhoog, dan kom je daar altijd uit), en zo'n bovenrand met de massa eronder is
niets anders dan een terras van een paar cellen breed. Daarom tekent `grotMassa` de massa
met `klif_bovenrand.png` zelf, op `terScale(scale)`, precies zoals `drawClimb` een terras
tekent: middenstukken om en om gespiegeld, en aan een open kant de afbrokkelende rand van
het plaatje. Een rotsblok is daarmee van hetzelfde steen als de terrassen ernaast, en de
winterversie loopt automatisch mee, want `terPic()` regelt dat al.

Wat daarvoor stond, klopte niet: een eigen vlakke massa (`GROT_MASSA`) met een lichte band
eronder, in een andere kleur en een andere korrel dan de vloer. Dat leest als een grijze
rechthoek naast het level, hoe je die kleur ook kiest. Een getegelde textuur in plaats van
die vlakke kleur is niet beter: elk ander plaatje is net iets lichter of donkerder dan de
band, en dan ligt elke rand als een rechthoek in de rots.

Wat een terras niet heeft is een onderkant, want daar kom je bij een terras nooit. Dat is
het enige waar de grotset nog voor nodig is:

| buur leeg | wat erop komt |
| --- | --- |
| boven | het bovenvlak van het terrasplaatje: je loopt erop zoals je op een terras loopt |
| links of rechts | de afbrokkelende rand van datzelfde plaatje, over de rijen waar die kant echt open ligt |
| onder | de tanden van `plafond_strook.png`, horizontaal getegeld |

De zijkanten staan niet kaarsrecht: `grotSilPad` breekt ze open met `terJag`, dezelfde golf
die de zijkant van een terras openbreekt, geklemd op `GROT_JAG` (0,16) van een cel. De
botsing blijft wel op de celrand liggen, dus die hap mag niet groter worden. Waar de rots
zijdelings doorloopt blijft de naad recht en valt hij onder het buurstuk.

De ribbels van de wand liggen op een raster dat aan het hele gebied hangt, niet aan een los
stuk massa. Doe je dat niet, dan zet een stuk de wand halverwege opnieuw in en loopt er een
naad door het steen. Hetzelfde geldt voor de fase van de plafondtanden.

Van `plafond_strook.png` komt alleen wat onder de plafondlijn hangt in beeld: rij 433 tot
508 is massief steen (`GROT.band.dicht`) en dat deel wordt weggeknipt, rij 509 tot 592 is
de tandenrand en die hangt in de open ruimte, met een donkere contour eronder
(`grotSilhouet`), zoals de aardlaag van de grond er ook een heeft. Teken je dat massieve
deel wel, dan ligt er een lichte plaat met een kaarsrechte bovenkant op de wand, en precies
dat leest als een rechthoek op de rots.

De band wordt op `grotSteen()` getekend, 1,35 keer de schaal van de grondrand: groot genoeg
om als rots te lezen, en lichter dan de grondband. Op 2,1 zijn de brokken boven en onder
precies even groot, maar dan wordt de band twee keer zo zwaar als de vloer en vult hij het
halve scherm.

De rijen van `GROT.band` staan in de maten van `grot.json`, dus in de grote bron. Op een
telefoon komt hetzelfde plaatje op halve grootte uit `klein/`, en dan ligt rij 433 buiten
het plaatje. `grotTegelSet` schaalt die snee daarom mee met de werkelijke bronbreedte. Sla
je dat over, dan valt op een telefoon de hele band weg en hangt er niets aan het plafond,
zonder dat er iets in de console staat.

Wat de set niet heeft vullen de brokken op:

- waar een vloer op een wand uitkomt komt een handvol keien over de naad;
- waar een plafond tegen een wand aan loopt die verder naar beneden doorloopt, zit een hoek
  van 90 graden: daar hangt een hangblok in, want `hoek_plafond_wand.png` past niet in een
  raster en wordt niet gebruikt;
- waar een rotspunt in de open ruimte steekt komen keien of een hangblok overheen.

`wand_richel` zit met opzet niet in de verstrooiing: dat is een plank om op te springen, en
tegen een losse celrand geplakt hangt hij als een plaat in de lucht. Zet hem met de hand
neer, daar waar je hem als opstap wilt. `wand_rand.png` wordt sinds de terrasmassa niet meer
gebruikt: als tegel over een cel van 120 px leest dat stuk als een lichte rechthoek.

De losse stukken (hangblokken, richels, keien) hangen aan Amir (`grotDecorS`), niet aan de
steenschaal: daarop zou een hangblok zes keer zo hoog worden als hij.

Geen tint, geen overlay, geen `globalCompositeOperation` op deze sprites. Ze zijn allemaal
hetzelfde warm grijsbruine gesteente; elke waas eroverheen maakt van de ene helft grijs en
van de andere bruin.

Tegels worden een keer op maat gezet (`grotBandSet`) en daarna op hele pixels neergelegd.
Verklein je een naadloze tegel rechtstreeks met `drawImage`, dan klemt de resampler op de
rand en zie je de naad alsnog als een lijn door het steen lopen.

Alleen `wand_richel` draagt, met een hitbox die alleen de bovenkant van het brok beslaat.
Hangblokken en losse keien zijn puur decor.

## terrassen en richels

`terraces`, `ledges`, klimmen. Een richel kan gespiegeld (`drawLedge` met `o.f`, de botsing in `terracePlats`) en achter de schacht-wand (`o.achter`, getekend in `drawGrotten` voor de massa); zie "De schacht"

## grotten: rots als een raster van cellen

`grotten`: het raster, de randen, de verstrooiing, de botsingen
