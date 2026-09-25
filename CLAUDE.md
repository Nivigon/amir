# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Bestaande levels blijven met rust.** De leveldefinities in de HTML
(`ROSA_1` en `ROSA_2`, `RENEW_1` tot en met
`RENEW_10`, `WINTER_1` en `WINTER_2`, `DARK_1` tot en met `DARK_5`) zijn bevroren. De
levels in Episode Test levels (`TEST_1`) vallen daar niet onder: die zijn er juist om aan te rommelen. Er komt geen nieuwe vijand,
prop, tip, potion of aangepast getal in, ook niet even om iets te laten zien. Alleen
als de opdracht een level bij naam noemt ("zet dit in Renew 6") mag dat ene level
veranderen. Twijfel je of iets eronder valt, dan valt het eronder: vraag het.

**2. Nieuw werk test je in de sandbox.** Een nieuwe vijand, prop of mechaniek krijgt
knoppen in de sandbox, zodat het zonder level uit te proberen is. Dat is ook hoe de
speerworp erin kwam: knoppen onder "Speerworp", geen enkel bestaand level aangepast.

**3. Een nieuw testlevel alleen na toestemming.** Vraag het eerst, per geval. Mag
het, dan ontwerp je het level zelf: lengte, uitzicht, tegenstanders en opbouw zijn
aan jou, en je legt achteraf uit wat je gekozen hebt.

**4. Sluit aan op wat er is.** Er is al een laadsysteem, een decorregister, een
tekenlaag en een sandbox. Gebruik die in plaats van er een tweede naast te zetten.

**5. Nederlands, en geen em-dashes.** Code, commentaar, teksten in het spel, commits
en pull requests zijn Nederlands. Gebruik komma's of haakjes, nooit een lang
gedachtestreepje.

**6. Werk op een `claude/*`-branch.** Push daarheen en maak alleen een pull request
als daarom gevraagd wordt.

## Waar wat staat

De HTML is opgedeeld met commentaarkoppen (`// ---- ... ----`). Zoek daarop, niet op
regelnummer, want die schuiven bij elke wijziging.

| kop | wat er staat |
| --- | --- |
| globale lichtlaag | kleurwaas over het beeld, volgt de zon van het level; een level stelt hem bij met `licht` in `SCENES` |
| muziek per level | `MUZIEK`, `zetMuziek()`: welk deuntje onder welk level loopt |
| beeld: de grote of de kleine spriteset | `KLEIN_FAM`, de keuze groot of klein, `zetBron` |
| hppotion | de drinkkalebas |
| bukken, jump frames, tempo | Amir zijn bewegingen |
| rotsen om op te springen | `rocks`, en het automatisch bijgroeien |
| winter: episode Winter World | `WINTER_SRC`, `winterOn()`, `winterPic()` |
| bodem en sneeuwdek | het veld `sneeuw`: savanne of rots, en het dek in vier standen |
| levels voor Rosa / Episode Renew / Episode Winter World | de leveldefinities |
| Episode Dark Africa | `DARK_1` tot en met `DARK_5`: vijf levels in de nacht, op `darkafrica.mp3` |
| Episode Test levels | `TEST_1`: korte proefstukken, los van de echte episodes |
| terrassen en richels | `terraces`, `ledges`, klimmen |
| de rotswand rechts | `cliffs`, het einde van het level |
| grotten: rots als een raster van cellen | `grotten`: het raster, de randen, de verstrooiing, de botsingen |
| plafond: de rots boven je, als hoogtelijn | `plafond`: de lijn, de vulling, de band, de losse blokken |
| muur unlock: de rotswand met het rune-symbool | `MUUR`: de plaat, het gat, het schuifblok, het masker en de schijf |
| vallen: schade bij een diepe val | hoe diep een val telt en wat hij kost |
| schorpioen, het projectiel, spannen en werpen, de geworpen speer | de speerworp |
| personages, dorpsdecor | NPC's, `VILLAGE`, de dorpsplaten |
| Amir zegt er iets van als hij geraakt wordt | `SFX_RAAK`, `playRaak()`: de twee kreten |
| stap voor stap leren spelen | het `tutorial`-systeem van de Rosa-levels |
| gaten in de grond | `gaps`, de overkant, de nevel en de diepte; de laag die eronder doorloopt is `grondDoorlopen`, in de bodemsectie |
| stof, sneeuwval, het weer | deeltjes en het weerplan per potje |
| vegetatie, water, doornbos | `props`, `water`, `thickets` |
| slangen: kleur, zicht en patrouille | `SNAKE_DIRS`, `slangZiet`, `startPatrouille`, `slangSchuif` |
| zwarte panter, de witte panter, de hyena | de grote vijanden |
| achtergrondlagen, uitzicht per level | `SCENE0` en `SCENES` |
| startscherm, level maken, menu: kaartjes per level | menu en bouwer |
| elk level nakijken op decor boven een ravijn | `schoonLevel`, draait bij elk level |
| sandbox | de vrije testmodus |

Op schijf: `karakters/` (Amir, dorpeling, dorpelinge), `enemies/`, `design/` (decor,
achtergronden, water, dorp, botten), `klein/` (dezelfde mappen op halve grootte),
`music/` en `sounds/`, `tools/` (de Python-scripts), `icons/`, `sw.js` en
`offline-assets.json` (de webapp).

## Een level lezen of schrijven

Amir loopt naar links, dus alle `x` zijn negatief en lopen op naarmate je verder
komt. Een leveldefinitie is een gewoon object; de bouwer in het spel exporteert
precies hetzelfde formaat naar JSON.

| veld | wat |
| --- | --- |
| `name` | naam op het kaartje in het menu |
| `lagen` | sleutel uit `SCENES`: welk uitzicht dit level krijgt |
| `muziek` | sleutel uit `MUZIEK`: welk deuntje eronder loopt (`darkafrica`); zonder dit veld `bg.mp3` |
| `winter` | `true` zet het hele level in de sneeuw (witte dieren, sneeuwversies van het decor) |
| `sneeuw` | sneeuw op de grond, los van `winter`: `{soort, dek, van, tot}` (zie hieronder) |
| `valschade` | `true` laat een diepe val een of twee levens kosten (standaard uit) |
| `rocks` | keien om op te springen: `{x, s}` |
| `spawns` | vijanden: `{x, k}` met `k` = `groen`, `zwart`, `scorp`, `hyenas`, `panter` |
| `props` | decor: `{x, k, s, f, v}`, `k` uit `PROPS`, `f` spiegelen, `v` verre laag |
| `village` | dorpsplaten uit `VILLAGE`: `{id, x, depth, flip}` |
| `gaps` | ravijnen: `{x, w}` |
| `water` | poelen: `{x, n}` met `n` = aantal middenstukken |
| `thickets` | doornbossen: `{x, n, seed}` |
| `terraces` | terrassen om op te klimmen: `{r, l, h}` (rechterrand, linkerrand, hoogte) |
| `ledges` | richels aan een wand: `{x, h, s}` |
| `grotten` | rotsgebieden als raster: `{x, cel, y, grid, ...}` (zie hieronder) |
| `plafond` | de rots boven je als hoogtelijn: `[{x, y}, ...]` (zie hieronder) |
| `muur` | de rotswand met het rune-symbool: `{x, speer}` (zie hieronder) |
| `hppotions` | drinkkalebassen: `{x, y}` |
| `fg` | strook waarover de voorgrondbegroeiing ligt: `{from, to}` |
| `arena` | het veld van de eindbaas: `{c}` |
| `cliffs` | de afsluitende rotswand: `{x}`, staat altijd achter `ends` |
| `ends` | de fakkels die het level uitspelen: `{x}` |
| `npcs` | dorpelingen: `{x, k, f, s}` |
| `tips` | tekst onderweg: `{x, t}` |
| `tutorial` | alleen de Rosa-levels: stapjes met uitleg |

### Bodem en sneeuwdek: grijs en rood zijn twee verschillende dingen

`winter: true` is de complete uitrusting van episode Winter World: witte dieren, sneeuw
op alles wat je beklimt, en een grond waarin sneeuw en grijze steen in één tegel zijn
gebakken. Dat is de bergversie en die blijft zoals hij is.

Het veld `sneeuw` beantwoordt een andere vraag: ligt hier sneeuw op de grond, en op wat
voor grond. Twee dingen die los van elkaar staan:

| | |
| --- | --- |
| `soort: 'savanne'` | de rode grond van de savanne, en die blijft rood onder de sneeuw |
| `soort: 'rots'` | dezelfde grond als grijze steen: een rotsbodem, ook zonder sneeuw |
| `dek` | hoeveel sneeuw er ligt, 0 tot 1 (standaard 1) |
| `van` en `tot` | alleen samen: het dek loopt op van niets op `van` tot vol op `tot` |

Kies dus bewust. Grijs is een steensoort, geen gevolg van sneeuw: een ondergesneeuwde
zandvlakte is onder die sneeuw nog altijd rood zand, en dat zie je ook, want het dek
laat overal plekken grond vrij. Vraagt iemand om een besneeuwd savannelevel, dan is dat
`soort: 'savanne'`; gaat het om een kale steenvlakte of een hoogvlakte, dan `'rots'`.

Amir loopt naar links, dus `tot` is negatiever dan `van`:

```
sneeuw: { soort: 'savanne', van: -1200, tot: -7000 }
```

Het dek zelf zijn vier doorzichtige lagen (`design/sneeuwlaag_25` tot `100`) die genest
zijn: wat op 25 wit is, is dat op 50 ook. De overgang van de ene stand naar de volgende
is daardoor alleen sneeuw die erbij komt, en die grens loopt grillig, zodat je nergens
een rechte streep over de grond ziet. Zet je een nieuwe stand bij, houd die nesting dan
intact, anders knippert er sneeuw weg terwijl je loopt.

Wat nu nog niet meeloopt: de rotsen, de klimstukken, het gras en de dieren hebben alleen
een aan-of-uit sneeuwversie. Loop je door een overgang, dan springen die er in één keer
om. Dat is bewust buiten deze wijziging gelaten.

`schoonLevel` kijkt elk level bij het laden na en schuift decor dat boven een ravijn
staat naar de kant, of haalt het weg. Reken daar niet op als ontwerper: zet het
meteen goed.

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
niet meer te halen. Nu is een cel overal 150 eenheden en Amir zijn sprong overal 185, dus
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

### Het plafond als hoogtelijn

Het raster hierboven is terrein in cellen, en dat geeft rechte hoeken. Voor rots boven je
staat daarnaast de plafondlijn, en die is opgezet als de grond: `terrainH(x)` geeft per
wereld-x hoe hoog de bodem ligt, `plafondH(x)` geeft hoe hoog de onderkant van de rots hangt,
allebei in sprite-eenheden boven de grondlijn. Tussen twee punten loopt de lijn recht door,
dus een schuin stuk is niet meer dan twee punten op verschillende hoogte.

```
plafond: [ {x: -1000, y: 4000},    geen plafond: PLAFOND_WEG of hoger is open lucht
           {x: -2600, y: 360},     zakt schuin in beeld tot een gang
           {x: -5200, y: 280},     en knijpt verder dicht
           {x: -6600, y: 4000} ]   weer omhoog, uit beeld
```

De punten mogen in looprichting staan (x steeds negatiever); het spel zet ze zelf op volgorde.
Reken met Amir: hij is `CHAR_H` (251) hoog en springt 208. Boven de 460 merkt hij niets, op
400 loopt hij rechtop maar stoot hij bij elke sprong zijn hoofd, op 280 zit springen er niet
meer in, en onder de 251 kan hij er helemaal niet langs, want gebukt loopt hij niet.

Staat er iets onder de lijn om op te springen, tel dan door: een plafond knipt zijn sprong af,
dus de lijn moet minstens op de hoogte van dat ding plus 251 plus ongeveer 75 liggen. Op de kei
van Test 1 (114 hoog) is dat 440. Op 400 haalt hij het ook nog, maar alleen als hij precies op
tijd afzet, en dan sta je de halve tijd klem voor een kei van een halve meter. Dat is gemeten,
niet geschat: op 400 lukt de sprong vanaf 30 tot 180 px voor de kei, op 440 vanaf 30 tot 270.

Drie lagen, in deze volgorde:

1. **Vulling** (`plafondVulling`): alles boven de lijn, met de lijn als clippad. De tegel is
   `design/grot/rots_vulling.png`, uit het massieve deel van `plafond_strook` geknipt
   (`tools/rots_vulling.py`), en wordt op `grotSteen()` getekend: dezelfde schaal als de band,
   dus per definitie dezelfde korrel. Naadloos in beide richtingen, nooit uitgerekt, en hij
   loopt altijd door tot ruim voorbij de bovenrand van het scherm.
2. **Band** (`plafondBand`): dezelfde tandenrand als bij de grotten (`GROT.band`, de onderste
   160 bronrijen van `plafond_strook`), maar langs de lijn, en per stuk meegedraaid met de
   helling. Het patroon loopt door over de knikken heen (`plafondFase`), anders begint het bij
   elk stuk opnieuw en zie je de knik in het steen zitten. Die fase moet ook doorlopen buiten
   de lijn: het spel tekent anderhalve schermbreedte breder dan het beeld, dus aan het eind
   van een level ligt de rand van dat venster voorbij het eerste punt van de lijn. Daar is de
   lijn vlak (`plafondH` klemt), dus de lengte is gewoon de afstand, en `plafondFase` geeft
   hem negatief terug. Stopt hij daar op nul, dan staat de fase stil terwijl het stuk tussen
   de vensterrand en het eerste punt wel meegeteld wordt, en plakt de tandenrand aan het
   scherm in plaats van aan de wereld: hij schuift dan precies met je mee.
3. **Losse blokken** (`plafondDecorLijst`): om de `PLAFOND_STAP` wereld-px een plek, waar
   ongeveer een op de drie keer een hangblok of een richel hangt, met een seed uit de lijn zelf.
   Ze worden afgesneden op de lijn: wat erboven uitsteekt zit in het steen. Hoe krapper de
   ruimte onder de lijn, hoe kleiner ze uitvallen (`PLAFOND_HANG`), want je moet er niet
   doorheen hoeven lopen.

De band loopt aan zijn bovenkant uit in de vulling (`PLAFOND_VERVAAG`), en de vulling loopt
daarvoor even ver door onder de lijn. Zonder die overgang ligt er een lichte plaat met een
kaarsrechte bovenkant op de rots, en dat is precies wat er bij de grotset ook al misging.

Botsen: de ruimte boven de lijn is massief. `plafondKop` is de laagste lijn over zijn breedte
min zijn eigen lengte, en gaat samen met `grotKop` als plafond in `updateJump`. `plafondBlok`
duwt hem terug waar de lijn onder zijn kruin duikt, zoals `grotBlok` dat bij een celwand doet.
Hangblokken zijn decor; alleen `wand_richel` draagt, met dezelfde hitbox als in een grot
(`plafondPlats`).

`hoek_plafond_wand.png` en `wand_rand.png` worden nergens meer getekend. Ze blijven wel in
`design/grot/` staan, voor later, als er een ravijn komt waar je in afdaalt.

### De muur die je met je speer openkrijgt

Een rotswand die de weg verspert, met op het steen een houten schijf met een rune. Raakt de
punt van een geworpen speer die schijf, dan blijft die speer er voorgoed in zitten en schuift
het rotsblok in een halve seconde omhoog de berg in. Mis je, dan blijft de speer in de rots
steken en valt hij er na `JAV.muurT` vanzelf uit: dat is de gewone wandspeer, daar is niets
voor aangepast.

Een level zet hem neer met `muur: {x, speer}`. `x` is de rechterrand van de rots, de kant waar
Amir aankomt; `speer` is waar zijn speer steeds terugkomt, en dat telt vanaf de lijn waar de
wand hem tegenhoudt, niet vanaf een vaste plek in de wereld. Dat moet ook wel: de rots hangt aan
Amirs maat, dus op een ander scherm verschuift die lijn mee en kwam een vaste plek achter de
muur te liggen, waar je er niet meer bij kon. Verder staat er geen enkele positie in het level: waar de opening en
de schijf komen rekent `muurSet` uit de plaat zelf uit. Alles wat je kunt afstellen zijn maten
en verhoudingen, en die staan bij elkaar in `MUUR`.

**De rots wordt in zijn geheel getekend.** Niet gesneden, niet gespiegeld, niet uitgerekt: de
hele plaat met zijn volledige silhouet, geschaald tot hij past. Zijn maat hangt aan Amir
(`hoogAmir`, 1,6 keer zijn lengte) en niet aan het scherm, en dat is niet vrijblijvend: de
opening en de schijf worden uit Amir gerekend, dus hangt de rots aan het scherm, dan verspringt
die verhouding met elk venster. Op een breed en laag scherm werd de rots groot terwijl Amir
klein bleef, schoof de opening diep de rots in, en was de rune vanaf geen enkele plek meer te
raken. Aan Amir gekoppeld ligt alles op elk scherm hetzelfde. `hoog` en `breed` zijn alleen nog
een vangnet voor het geval hij niet past.

Omklappen kan met `spiegel`, maar staat uit, en dat is gemeten. Gespiegeld wijst de hoge flank
met de overhang naar Amir en komt de opening onder dat hoge steen te liggen. De schijf hangt
altijd net onder de bovenrand van de rots, dus daar hangt hij hoog, en een hoge schijf betekent
een lange worp: op 1280 bij 720 moet je dan van 480 pixels gooien en staat er nog maar een
strook rots in beeld, en op 1440 bij 620 is er helemaal geen plek meer waar je hem kunt raken.

**De plek van de opening komt uit de alfawaarden.** Per kolom wordt geteld hoe hoog het steen
vanaf de grond draagt (`massief`). Kleine gaten onderweg tellen daarbij niet als het einde: aan
de voet staan de keien los van elkaar met lucht ertussen, en een telling die daar stopt geeft
nul op kolommen waar in het beeld gewoon een muur van steen staat. Dat was precies waarom de
opening met de kale plaat ineens driehonderd pixels dieper ging liggen. Vanaf dat profiel en daarna wordt van de kant waar Amir
vandaan komt de eerste plek gezocht waar de opening past, met daar de hoogste deur die er nog
in kan. Zo dicht mogelijk bij zijn kant dus, en dat is niet alleen netjes: hoe dieper de
opening ligt, hoe verder je moet gaan staan om de rune te raken, en hoe minder er dan van de
rots in beeld past. Twee eisen tegelijk:

- over de volle breedte van de opening moet er genoeg steen staan (de deur plus de schijf
  erboven plus een randje);
- waar de schijf komt te hangen moet de bovenrand van de rots juist laag genoeg blijven, onder
  de top van de werpboog. Het spel rekent die top uit de worpconstanten uit. Ligt de rand
  hoger, dan kan de speer er per definitie nooit overheen en is de rune onraakbaar.

Past de opening nergens, dan krimpt hij tot hij wel past, tot Amirs eigen lengte. Dat is met
opzet: een deur die vasthoudt aan zijn maat belandt aan de rand van de rots, half in de lucht,
en dat is precies wat er niet mag.

**De schijf hangt aan de bovenrand, niet op een vaste hoogte.** In zijaanzicht is de rots een
massief silhouet: een punt onder de bovenrand zit in het steen, en daar komt geen speer ooit,
hoe je ook gooit. De schijf hangt dus net onder die rand (`onder`, 1 betekent dat haar
bovenkant hem raakt), zodat het hout helemaal op de rots ligt en de punt er toch bij kan door
er overheen te scheren. Daarom is het raakvlak (`raak`) ruimer dan het hout: de ruimte waar de
speer kan komen ligt boven de schijf. Dat raakvlak staat los van de straal, en met opzet: `r`
is hoe groot het hout eruitziet, `raak` is hoe nauw het luistert, allebei als deel van Amirs
lengte. Zo maakt een kleinere schijf het spel niet meteen ook moeilijker. De punt blijft steken waar hij binnenkwam, geklemd op de
rand van het hout, dus hij springt niet naar het midden.

**Gat en blok komen uit dezelfde pixels.** Uit de plaat op maat komen drie canvassen: de muur
met de vorm van de opening eruit gegumd (`destination-out`), het schuifblok dat precies dat
uitgegumde stuk is met een marge eromheen, en een masker dat die vorm doorsnijdt met de rots
zelf. Het masker is een pixel ruimer dan het gat, anders blijft er door de anti-aliasing een
haarlijntje op de rand staan.

Die snede met de rots gaat met de hand en niet met `destination-in`. Die rekent alfa maal alfa,
en waar de omtrek van de rots zelf door het gat loopt (langs de voet, bij de steentjes) werd het
blok daardoor doorzichtiger dan het steen eromheen. En zolang het blok stilstaat wordt de
ongeschonden plaat getekend en verder niets: de drie canvassen weer samenstellen levert op de
zachte randen 8-bits afrondingen op, en dat is precies het haarlijntje dat er niet mag zijn.

**De speer botst op de alfawaarde**, met de punt, en dat gaat vanzelf goed omdat `jav.x` en
`jav.h` in dit spel de punt zelf zijn. Lukt het uitlezen niet, dan telt de hele plaat als rots.

**Amir botst op een enkele verticale lijn**, de rand van de opening die naar hem toe wijst. De
rest van de rots is decor. Dat moet ook wel: de flank ervoor loopt schuin op en eindigt in losse
steentjes, en daar zou hij aan blijven hangen ver voordat hij bij de deur is.

**Controleer na elke wijziging of de rune nog te raken is.** Dat is geen gevoelskwestie: simuleer
de boog vanaf elke plek waar Amir kan staan en kijk of er een aaneengesloten strook overblijft.
Op een scherm van 1280 bij 720 en Formaat 25 is die strook 141 pixels breed, van 94 tot 235
pixels voor de muurlijn, en vanaf de hele strook staat de rots in zijn geheel in beeld.

Het gras aan de voet staat niet in de plaat maar wordt er los voor gezet (`MUUR.gras`), met
dezelfde tekencode als al het andere gras, dus het buigt mee met de windvlagen. Ingebakken gras
schaalt mee met de rots, en dan staan er sprieten van een meter hoog zodra hij groter wordt. Dichterbij gaat de speer onder de rune door tegen het steen, verder weg zakt hij er al
voor. Er is nog een tweede strook op ruim tweeduizend pixels, maar daar staat de rots buiten
beeld, dus die telt niet mee.

Het geluid zit in `SFX_DEUR` (`sounds/deuropen.mp3`) en speelt af op het moment van de treffer.
De opname duurt 42 seconden en staat van begin tot eind even hard, terwijl het blok maar een
halve seconde schuift, dus er wordt alleen de kop van gebruikt: vol tot `duur`, dan wegzakken in
`uit`, samen zo'n drie seconden. Dezelfde aanpak als bij het windgeluid. `duur: 0` speelt hem
wel helemaal uit.

### Een level donker maken

De lichtlaag ligt over het hele beeld, dus ook over de grond en over Amir. Een level dat
er anders uit moet zien zet in zijn `SCENES`-blok een veld `licht` met de waarden die
afwijken (zie `LICHT`), en dat is hoe Dark Africa donker wordt: een blauwgrijze
schaduw- en lichtkleur, een zwakkere gloed en een iets diepere onderkant. `aan` en
`sterkte` blijven van de regelaars (`L`, en `,` en `.`), ook in zo'n level: die zijn er
om te kunnen kijken wat de laag doet, en dat moet in elk level werken.

Het veld `dim` in `SCENES` is iets anders: dat zet alleen de achtergrond dieper, tot aan
de grondlijn. Wil je dat de hele wereld donkerder wordt, dan is `licht` het juiste veld;
wil je alleen dat de verte wegzakt, dan `dim`. Meestal gebruik je ze samen.

### Een level toevoegen (alleen na toestemming)

1. De definitie erbij, na de laatste van die reeks.
2. De naam in de array van die reeks (`LEVELS`, `ROSA_LEVELS`, `RENEW_LEVELS`,
   `WINTER_LEVELS`).
3. Een ondertitel in `SUBS`, op de naam van het level.
4. Een eigen uitzicht in `SCENES` als het level er anders uit moet zien.

### Een episode toevoegen

Die vier stappen, plus: een knop in `menuChoose`, een eigen `menuXxx`-blok in de
HTML naar het voorbeeld van `menuWinter`, en die aanmelden in `buildCards`,
`markCards` en `showMenu`.

### Een vijand of prop toevoegen

Tekencode en gedrag erbij, opnemen in `PROPS`, `VILLAGE` of de dierenlijst, en
knoppen in de sandbox. Pas daarna is de vraag aan de orde of er een level bij moet.

## Sandbox

De sandbox start met vlakke grond en een leeg level, geen automatische vijanden en
geen levens. Een knop erbij is twee dingen: een `<button>` in `<div id="sandbox">`
(een eigen `.row` met een `<label>` als het een nieuw onderwerp is) en de afhandeling
in de sandbox-sectie van de code. Spawnen gebeurt net binnen beeld aan de gekozen
kant (`sbFromRight`), altijd geklemd tussen `endWall()` en `cliffAt().wall`.

## Assets

Sprites toegevoegd, vervangen of weggehaald? Draai daarna, in deze volgorde:

```
python3 tools/gen-klein.py
python3 tools/gen-offline-manifest.py
```

Het eerste script print de lijst die in `KLEIN_FAM` hoort te staan. Loopt die niet
gelijk, dan laadt een telefoon stilletjes de grote versie. Het tweede werkt de lijst
bij die de downloadknop afwerkt; sla je dat over, dan mist de offline-download
bestanden.

Een plaatje hoort alleen in de kleine set als het op een telefoon nog steeds groter
is dan het stukje scherm waar het terechtkomt. De afweging per familie staat in
`DOELEN` in `tools/gen-klein.py` en in de README.

De bodem en het dek van het veld `sneeuw` komen uit `tools/sneeuwdek.py`
(`grondrand_rots.png` en `sneeuwlaag_25..100.png`). Die staan met opzet niet in de kleine
set: `grondrand.png` staat daar ook niet in, en een dek dat anders geschaald wordt dan de
bodem eronder gaat schuiven.

`design/grot/rots_vulling.png` (het steen boven een plafondlijn) komt uit `tools/rots_vulling.py`:
dat knipt het massieve deel uit `plafond_strook.png`, haalt het licht-donkerverloop eruit en
maakt de boven- en onderrand op elkaar aansluitend. Verandert de strook, draai het dan opnieuw.

De grotset in `design/grot/` hoort wel in de kleine set: die stukken zijn de grootste
bronnen van het spel en worden tot een tiende getekend. Dat mag hier omdat de tekencode
met de maten uit `grot.json` rekent en elk stuk naar die maat rekt; de ankerpunten
schuiven dus niet mee met de bronmaat. `grot.json` zelf blijft buiten de kleine set,
want `gen-klein.py` pakt alleen png's.

Geluid staat in `music/` en `sounds/`. De achtergrondnummers staan in `music/` en worden
aangemeld in `MUZIEK`; korte geluiden van personages en dieren horen in `sounds/`. Zo staan
`ahhit.mp3` en `stopit.mp3`, de twee kreten van Amir, bij de hyenageluiden en niet bij de
muziek. Beide mappen zitten in de offline-download, dus draai na een nieuw bestand
`tools/gen-offline-manifest.py` opnieuw.

De twee slangen komen uit `tools/slang_kleur.py`: dat kleurt `enemies/slang1/` om naar de
zandslang in `enemies/slang1_zand/` en `enemies/slang2/` naar de zwarte in
`enemies/slang2_roet/`. Het spel tekent alleen die twee omgekleurde mappen (`SNAKE_DIRS`); de
originelen blijven staan als bron, en `venom.png` komt nog steeds uit `slang2/`. Verandert er
een frame, draai het script dan opnieuw. Ze staan niet in de kleine set.

Winterversies komen uit `tools/sneeuw.py` (rotsen en klimstukken), `sneeuw_bg.py`
(achtergrondpanelen), `sneeuw_dorp.py` (hutten, boom, struik) en `winter_art.py`
(dieren, grond, gras). Verandert een origineel, draai het bijbehorende script dan
opnieuw.

## Testen en afronden

Het spel wil van een webserver komen, anders weigert de browser de sprites:

```
python3 -m http.server
```

Er zijn geen tests en geen linter, dus kijk zelf na wat je aangeraakt hebt: speelt
het level uit, blijft de speer vindbaar, staat er niets in de lucht, en geeft de
console geen 404. Merkt de speler iets van je wijziging, werk dan `README.md` bij.
Commit in het Nederlands, in dezelfde toon als de bestaande geschiedenis: één regel
die zegt wat er nu anders is, en daaronder de uitleg.
