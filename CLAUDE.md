# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Bestaande levels blijven met rust.** De leveldefinities in de HTML
(`RENEW_1` tot en met `RENEW_10`, `WINTER_1` en `WINTER_2`, `DIEP_1` tot en met
`DIEP_5`) zijn bevroren. De
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

**7. Vijanden komen niet over keien en ravijnen.** Slangen, fosforslangen, de
zwaardvechter en ook de panters worden tegengehouden door een kei om op te springen en
door de rand van een ravijn: niet lopend, niet met een sprong of een duik, en ze duiken
ook niet aan de overkant op. Zo is een kei of een ravijn voor de speler een schuilplek.
Een uitzondering mag alleen als de opdracht er expliciet om vraagt, of in een gevecht met
een eindbaas als je daar zelf voor kiest omdat het dat gevecht beter maakt; zeg dan
achteraf dat en waarom. Voor de panter is dat het veld `over: true` in zijn spawn
(`panBaan`); zonder dat veld blijft hij aan zijn kant.

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
| Episode De Diepte / Episode Renew / Episode Winter World | de leveldefinities |
| Episode De Diepte | `DIEP_1` tot en met `DIEP_5`: vijf zware levels met valschade, elk met een gang onder de grond en een trap terug naar boven, met een verhaal en een slot en de zwarte panter als eindbaas |
| het verhaal bij een episode | `VERHAAL` en `SLOT`, `verhaalToon()`: tekst op een zwart scherm voor elk level en na het laatste, alleen als je bij het eerste level begint. Op de naam van het level, dus een nieuwe episode hoeft alleen tekst toe te voegen en `verhaalAan` te zetten in zijn speelknop |
| Episode Test levels | `TEST_1` tot en met `TEST_10`: korte proefstukken, los van de echte episodes |
| lichtkaart: het licht onder de grond | `LK`, `drawLichtkaart`: een lichtbron (de hemel en de zon) voor alles onder de grond, per level een keer uitgerekend |
| terrassen en richels | `terraces`, `ledges`, klimmen |
| de rotswand rechts | `cliffs`, het einde van het level |
| grotten: rots als een raster van cellen | `grotten`: het raster, de randen, de verstrooiing, de botsingen |
| plafond: de rots boven je, als hoogtelijn | `plafond`: de lijn, de vulling, de band, de losse blokken |
| muur unlock: de rotswand met het rune-symbool | `MUUR`: de plaat, het gat, het schuifblok, het masker en de schijf; en de grot met de kei (`MUUR_GROT`, `muurGrotSet`, `drawMuurGrot`) |
| ravijn in de winter | `RAVIJN_WINTER`, `ravijnWandNu()`, `ravijnSneeuwRand()`: het openscheurende ravijn in een winterlevel, de wand bij het laden omgekleurd naar blauwgrijze steen (alleen kleur, per pixel op helderheid), een getekende sneeuwrand en het berijpte gras |
| zegel in de grond: de runeschijf plat, als schakelaar | `ZEGEL`, `zegelGrond`, `zegelUpdate`, `zegelDoe`: erop stappen zet hem aan of uit, en wat hij dan doet (nu: een ravijn openen) |
| skelet met speer | `SKELET`, `skeletTrek`, `skeletUpdate`, `skeletTeken`: E trekt de speer eruit, het skelet stort in (sheet van 30 frames op 25 fps, `sounds/skeletvalt.mp3`), daarna rolt de losse schedel weg als je ertegenaan loopt |
| runeschijf: het losse symbool | `runeSchijf(ctx, x, y, r, {aan, spiegel})`: de houten schijf met de rune, los te hergebruiken |
| vallen: schade bij een diepe val | hoe diep een val telt en wat hij kost |
| schorpioen, het projectiel, spannen en werpen, de geworpen speer | de speerworp; `speerNaastAmir` zet een speer waar Amir niet meer bij komt (achter of in een doornbos, boven op een terras dat hij van deze kant niet meer op komt) naast hem, nooit over een ravijn; `speerBereikbaar` rekent dat uit over de vloeren om hem heen |
| personages, dorpsdecor | NPC's, `VILLAGE`, de dorpsplaten |
| Amir zegt er iets van als hij geraakt wordt | `SFX_RAAK`, `playRaak()`: de twee kreten |
| stap voor stap leren spelen | het `tutorial`-systeem (staat klaar, geen level gebruikt het nu) |
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
| `worp` | `'schaal'` zet de schaalworp aan: de hoek loopt op zolang je vasthoudt, van vlak tot 30 graden (`THR_HOEK_MAX`); zonder dit veld de twee trappen. In de sandbox de knop Worp onder Speerworp |
| `rocks` | keien om op te springen: `{x, s}` |
| `spawns` | vijanden: `{x, k}` met `k` = `groen`, `zwart`, `scorp`, `hyenas`, `panter`, `zwaard` (met `c`), `fosfor`; een panter met `over: true` mag over keien en ravijnen (zie regel 7) |
| `props` | decor: `{x, k, s, f, v}`, `k` uit `PROPS`, `f` spiegelen, `v` verre laag |
| `village` | dorpsplaten uit `VILLAGE`: `{id, x, depth, flip}` |
| `gaps` | ravijnen: `{x, w}` |
| `water` | poelen: `{x, n}` met `n` = aantal middenstukken |
| `thickets` | doornbossen: `{x, n, seed}` |
| `terraces` | terrassen om op te klimmen: `{r, l, h}` (rechterrand, linkerrand, hoogte); met een negatieve `h` een trede in een gang |
| `holtes` | gangen onder de grond: `{r, l, diep}`, een ravijn erboven is de ingang, een gat met treden de uitgang (zie hieronder) |
| `ledges` | richels aan een wand: `{x, h, s}` |
| `grotten` | rotsgebieden als raster: `{x, cel, y, grid, ...}` (zie hieronder) |
| `plafond` | de rots boven je als hoogtelijn: `[{x, y}, ...]` (zie hieronder) |
| `muur` | de rotswand met het rune-symbool: `{x, speer}`, of met `soort: 'grot'` de rotsboog met de kei (zie hieronder) |
| `hppotions` | drinkkalebassen: `{x, y}` |
| `skeletten` | een zittend skelet met een speer erin: `{x, f}`, `x` is het midden van het skelet, `f` spiegelt; E bij de schacht trekt hem eruit (zie hieronder) |
| `zegels` | zegels plat in de grond: `{x, ravijn, sluit}`; erop stappen zet hem aan of uit, en met `ravijn` scheurt de grond daar open als hij aangaat. Met `sluit` gaat het open ravijn op die x juist weer dicht (staat er niets open, dan blijft hij donker) |
| `fg` | strook waarover de voorgrondbegroeiing ligt: `{from, to}` |
| `arena` | het veld van de eindbaas: `{c}` |
| `cliffs` | de afsluitende rotswand: `{x}`, staat altijd achter `ends` |
| `ends` | de fakkels die het level uitspelen: `{x}` |
| `npcs` | dorpelingen: `{x, k, f, s}` |
| `tips` | tekst onderweg: `{x, t}` |
| `tutorial` | stapjes met uitleg (nu door geen level gebruikt) |

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
staat naar de kant, of haalt het weg (behalve binnen een gang: daar staat het op de bodem). Reken daar niet op als ontwerper: zet het
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
Reken met Amir: hij is `CHAR_H` (251) hoog en springt 200 (zie "de sprong" hieronder). Boven de 460 merkt hij niets, op
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

Rotsformaties krijgen voortaan deze maat: 3,5 keer Amir hoog, even groot als deze rots in
Test 3. Zo staat ook de scheve spits met de rune bij het openscheurende ravijn in Test 6
(`RAVIJN_ROTS`).

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

**Amir loopt door de rots heen.** De hele rots is decor, ook de deur: uitspelen gaat met E als
de deur open staat en hij ervoor staat (`muurUitgang`). Er is dus niets dat hem tegenhoudt, en
een level dat bij de rots eindigt zonder klif erachter laat hem voorbij de rots eindeloos de lege
savanne in lopen. Zet er een klif een stuk achter, zoals in Diepte 3.

**Controleer na elke wijziging of de rune nog te raken is.** Dat is geen gevoelskwestie: simuleer
de boog vanaf elke plek waar Amir kan staan en kijk of er een aaneengesloten strook overblijft.
Op een scherm van 1280 bij 720 en Formaat 25 is die strook 141 pixels breed, van 94 tot 235
pixels voor de muurlijn, en vanaf de hele strook staat de rots in zijn geheel in beeld.

Het gras aan de voet staat niet in de plaat maar wordt er los voor gezet (`MUUR.gras`), met
dezelfde tekencode als al het andere gras, dus het buigt mee met de windvlagen. Ingebakken gras
schaalt mee met de rots, en dan staan er sprieten van een meter hoog zodra hij groter wordt. Dichterbij gaat de speer onder de rune door tegen het steen, verder weg zakt hij er al
voor. Er is nog een tweede strook op ruim tweeduizend pixels, maar daar staat de rots buiten
beeld, dus die telt niet mee.

**De grot met de kei** is een tweede soort muur: `muur: {x, speer, soort: 'grot'}` (nu alleen Test
3). Instellingen in `MUUR_GROT`, de canvassen in `muurGrotSet`, tekenen in `drawMuurGrot`. De rots is
de geschilderde boog `design/rotswand_boog.jpg`, met het wit eruit via `witKnip` (dezelfde functie
als de rots bij het ravijn); het donker in de grot is een vulling vanuit de voet van de boog, dus het
volgt de geschilderde rand. Voor de ingang staat `PROPS.boulder`, zo groot dat hij de grot dekt. Bij
een treffer trilt hij, zakt hij de grond in en blijft zijn bovenkant als drempel liggen (`kei.blijf`),
met stof (`puffPic()`) en gruis dat van de boog valt, allemaal op `muurKlok`. Zet hier geen gegumde
opening in: een getekend gat in een geschilderde rots blijft computertekenwerk, en daar is dit de
vervanger van. `muurSet` geeft voor de grot dezelfde velden terug (`l`, `r`, `t`, `b`, `symX`, `symY`,
`alfa`), dus de E voor de deur, de speer in de schijf en `muur.speer` werken gewoon door.

De schijf staat op `sym.hoog` 2,0 Amir, op de linkerpoot (`sym.u`). Dat is gemeten, niet gekozen: met
de huidige boogworp raak je hem op een scherm van 1280 bij 720 van 465 tot 770 pixels, waarvan 465 tot
620 met de schijf in beeld (de camera staat op Amir, dus je ziet 640 naar links). Op 2,28, de hoogte van
de kale rots, begint de strook pas op 590 en valt er bijna niets meer in beeld. Op 1440 bij 620 is het
400 tot 660, op 1920 bij 1080 690 tot 1155, op een telefoon van 844 bij 390 250 tot 420. Hoe lager de
schijf, hoe dichterbij: de boog stijgt nog als hij bij de schijf is.

Een speer blijft bij de grot pas in het steen steken als hij er van buitenaf in vliegt (`jav.buiten` in
`muurSteen`). Amir staat hier vaak voor de rots, onder de boog of voor de kei, en dan vertrekt de speer
al in het steen: met de gewone regel bleef hij er na een paar pixels in steken en was de schijf van
dichtbij niet te halen. Zolang de kei staat vangt die ook een speer (`keiAlfa`).

Let op: de getallen hierboven voor de kale rots (94 tot 235 pixels) kloppen niet meer met de huidige
worp. Met dezelfde meting raak je de schijf in Diepte 3 van 590 tot 1005 pixels.

Het geluid zit in `SFX_DEUR` (`sounds/deuropen.mp3`) en speelt af op het moment van de treffer.
De opname duurt 42 seconden en staat van begin tot eind even hard, terwijl het blok maar een
halve seconde schuift, dus er wordt alleen de kop van gebruikt: vol tot `duur`, dan wegzakken in
`uit`, samen zo'n drie seconden. Dezelfde aanpak als bij het windgeluid. `duur: 0` speelt hem
wel helemaal uit.

### Het skelet met de speer

De plaatjes staan in `design/botten/skelet/` en zijn allemaal op één schaal gemaakt: 0,19 bij een Amir van 237 px
(`SKELET.schaal`), dus het zittende skelet is 0,61 Amir. Rekenen gaat in skeletcoordinaten, met (0, 0) op de
linkerbovenhoek van het skelet zelf en de grond op 754.

- **Zitten** zijn de negen losse botten uit `delen/` op hun plek, met daarover de speer,
  `skelet_voorste_botten` en het doekframe. De voorste botten zijn niet optioneel: zonder die laag ligt de speer op
  het skelet in plaats van erdoorheen. Tot de botten binnen zijn staat `skelet_met_speer.png` er.
- **Instorten** speelt het spel zelf met die botten (`SKELET.delen`, `skBotten`), op de valcurve van het pakket. De
  ingebakken sheet uit het pakket wordt niet gebruikt: daarin bleven de onderbenen met de knie in de lucht staan. Nu
  kantelt het bovenbeen om de heup en ploft het onderbeen plat (`a` en `laat` bij de benen). Een kind draait mee met
  zijn ouder, zoals in `onderdelen.json`.
- **De schedel** is na het instorten, of als hij eraf getikt is, een los ding (`s.kop`): hij valt, landt met stof,
  rolt met de hoek aan de afgelegde weg (weg gedeeld door de straal van 58) en ligt dan stil. Daarna is hij decor:
  tegenaan lopen of erop slaan doet niets.
- Wat Amir kan: E bij de schacht trekt de speer eruit, maar alleen met lege handen (anders wiebelt hij en speelt
  `sounds/dontneedthis.mp3`). Het skelet schudt dan (`schud`) en ploft in elkaar. Een steek of een worp tegen de schedel
  tikt die eraf (`skeletRaak`, aangeroepen vanuit de tekenlus waar ook de slangen geraakt worden). Een lage zwaai laat het
  meteen vallen, en de speer valt eruit en blijft liggen.
- De speer uit het skelet heeft een **blauw vaantje**. Het rode lint zit in Amirs sprites gebakken en wordt bij het
  tekenen omgekleurd (`vaanBlauw`), alleen fel verzadigd rood, zodat zijn huid blijft zoals hij is.
- **Losse speren** (`losseSperen`): er kan nu meer dan een speer zijn. Wat niet in je hand is en niet je eigen speer in
  de wereld, ligt daar. Pak je een andere speer terwijl de jouwe ergens ligt, dan wordt de jouwe een losse speer
  (`eigenSpeerNeer`), zodat hij niet verdwijnt.
- Het geluid `sounds/skeletvalt.mp3` start als het valt, niet bij het trekken, en gaat via een versterker op 3,6
  (vier keer 0,9), want een audio-element komt niet boven 1. Een tweede instorting start het opnieuw.
- Stof: eigen wolkjes per skelet (`SKELET.stof`), want `stofwolk.png` is ijl en `puffWorld` is voor een voetstap.
- De schaduw vermenigvuldigt de grond met (0,74, 0,80, 0,91) en ligt naar links, want de zon staat rechtsboven.

De plaatjes laden pas als er een skelet in het level staat (`skeletLaad`).

### Een gang onder de grond

`holtes: [{r, l, diep}]` legt een gang onder de grondlijn, met de vloer `diep` sprite-eenheden
lager. Een ravijn uit `gaps` dat erboven ligt is de ingang: daarin val je niet dood maar kom je
op de vloer terecht. Met `valschade: true` kost een val van 600 twee levens (vanaf twee Amir,
502). Het dak is de onderkant van het grondpakket, `HOLTE_DAK` (190) onder de grondlijn.
Laat de gang aan de kant van het ravijn wat verder doorlopen dan het gat, anders staat de wand
onder de rand. Alles in de gang staat op de bodem, want `terrainH` geeft daar `-diep`.

Het licht onder de grond komt uit een plek: de lichtkaart (zie hieronder). De tegels van de
gang zijn zelf maar een beetje donker gezet (`HOLTE_LICHT`), de looprand van de vloer lichter
dan de vulling eronder. `Test 10` is het proefstuk voor het licht, `Test 4` voor de gang.

### De lichtkaart: een lichtbron voor alles onder de grond

Er is een lichtbron onder de grond: de hemel, met de zon als vaste richting. Voor elke cel van
`LK.cel` bij `LK.cel` rekent `lkKolom` uit hoeveel hemel hij ziet (stralen omhoog die grond en
rots tegenhouden, `lkZicht`) en of de zon hem raakt (`lkZon`, een smalle kegel, dus een zachte
schaduwrand). De zon staat aan de kant waar hij in de lucht van het level staat (`zonRechts`),
`LK.zonHoek` graden van recht boven. Daaruit volgt vanzelf wat je wilt zien: een gat is licht,
de rand werpt een schuine schaduw van de zon af, en hoe verder de gang van een gat af loopt,
hoe donkerder, zonder rechte streep. Vaste grond is een doorsnede: die krijgt het licht van de
oppervlakte erboven en wordt dieper eronder donkerder (`LK.diepte`, `LK.bodem`). Lucht die zelf
weinig hemel ziet, krijgt kaatslicht van wat eromheen ligt (`LK.kaatsR` cellen in het rond), en
dat is warm waar de zon in de buurt iets raakt.

Dit vervangt alle losse lagen die er eerst waren: de getekende lichtbundel door een gat, de
schaduw tegen de eindwanden, het verloop in het grondpakket, `holteFilter` en `holteHelder`
voor decor en treden, en een vervaagde donkerlaag over de rots. Die gaven elk hun eigen licht
en dus rechte randen. Teken er dus geen nieuwe bij: een nieuw soort terrein hoeft alleen in
`lkVastPunt` te zeggen wat vast is.

Twee regels die ertoe doen:

- **De zonnegloed van de lichtlaag schijnt niet door de rots.** `drawLichtlaag` telt de gloed rond
  de zon op in schermruimte; onder de grond (`holteDiepT`) gaat die uit. Deed hij dat niet, dan lag
  er in de gang zo'n 40 punten helderheid bovenop, en daar was het steen vlak en oranje van.
- **Vaste grond wordt pas donker als de camera zakt.** Het plaatje met de grond (`lk.grond`)
  krijgt `holteDiepT` als dekking: van bovenaf ziet de savanne eruit zoals altijd. Wat lucht is,
  een gat of een gang, is altijd zo licht als het is.

De kaart hangt alleen af van de vorm van het level, dus elke cel wordt een keer uitgerekend. Wat
vast is gaat in een keer (`lkKaart`), de stralen per kolom zodra hij nodig is, en `lkVooruit`
rekent elk beeld `LK.budget` ms vooruit, vanaf Amir naar buiten: zo is de kaart af voor je
beneden bent. Het kaatslicht gaat met lopende sommen (`lkSom`), en de plaatjes worden eerst in
het geheugen gezet en per beeld een keer overgezet (`lkPlaatjes`). Zonder die twee kostte het
kaatslicht 1,2 seconde op Test 10, nu 70 ms; de hele kaart is een halve seconde, in stukjes.
Verandert de vorm (in de sandbox) of een regelaar, dan begint hij opnieuw (`lkSleutel`).

De kaart ligt na alles in de wereld (na `drawWind`), dus ook over Amir, de vijanden en het decor.
De vier regelaars staan in de sandbox onder **Licht onder de grond** (donker, zon, kaatslicht,
warm); elke klik laat alle vier zien, zodat je ze in `LK` kunt overnemen.

**Boven het dak loopt de aarde over in steen, en dat is materiaal, geen kleur.** Het grondpakket
boven een gang en de wand van het gat erboven zijn aarde, de gang is steen. Onderin het pakket
wordt de wandtegel van de gang zichtbaar (`holteOvergang`, over `HOLTE_OVERGANG` eenheden), op
precies hetzelfde ankerpunt in de wereld als de gangwand. Onder een gat ligt daardoor op de
daklijn aan beide kanten hetzelfde steen en loopt het patroon gewoon door; naast een gat hangen
er de tanden van het dak onder. Niet proberen de naad weg te poetsen met een tint of door kleuren
gelijk te trekken: dat is geprobeerd, en het gaat mis zodra het uitzicht of de lichtlaag anders
is. Meten deed het wel, en dat is de manier om een wijziging hier na te kijken: helderheid per
rij over de naad, en geen sprong van meer dan een paar punten.

De opbouw, van boven naar onder:

| waar | wat |
| --- | --- |
| naast een gat | de vloer van de savanne, dan aarde die overloopt in steen, en dan de tanden |
| in een gat (`holteSchacht`) | de wand van het ravijn zonder de nevel en het zwart van een afgrond, onderaan de overgang naar steen |
| buiten de gang | dichte rots, onder het dak |

Hoe licht of donker elk daarvan is, komt uit de lichtkaart. Het steen zit alleen boven een gang
en loopt voorbij de uiteinden over `HOLTE_UITLOOP` uit. Het ravijn boven een gang houdt twee
pixels onder het dak op, op een hele beeldpixel (`heelPx`): waar twee zachte randen op dezelfde
lijn liggen schijnt er anders een haarlijn doorheen.

Alles wat binnen `r` en `l` van een gang staat, staat op de bodem: vijanden, decor,
kalebassen en de fakkels. Een level kan dus onder de grond eindigen; de wand van
de gang houdt je dan achter de fakkels tegen, een klif is niet nodig. Dat werkt omdat
`grotTerrein` zonder raster `-Infinity` geeft en geen 0: gaf hij 0, dan trok `terrainH` alles in
de gang weer naar de savanne, en dat is precies waarom de vijanden in een gang eerst boven
stonden en de fakkels daar niet te halen waren.

Twee hulpjes houden boven en beneden uit elkaar. `gatOp(x, base)` is `inGap` voor wie op
hoogte `base` staat: beneden in een gang is een gat erboven geen rand, dus een vijand loopt er
onderdoor. `vloerBij(x, h)` is de vloer voor wie op hoogte `h` staat: boven een gang de
savanne, erin de bodem. De vijanden rekenen hun vloer daarmee uit, en de sandbox zet een vijand
daarmee op jouw hoogte neer. Gebruik ze in plaats van `inGap` en `terrainH` als het om iets gaat
dat zowel boven als beneden kan staan.

**Terug naar boven** gaat via een tweede gat in het dak met treden erin. Een trede is een gewoon
terras met een negatieve `h`, dus de klimstukken van de terrassen, en `drawClimb` tekent ze in
een tweede ronde na de ravijnen (anders tekent de overkant van het gat over de bovenste heen).
Hoe licht ze zijn komt uit de lichtkaart. Reken zo:

- het dak ligt op 190, dus onder het dak mogen zijn voeten niet hoger dan -441 (`-HOLTE_DAK -
  CHAR_H`). Een trede hoger dan dat moet helemaal onder het gat staan;
- zijn rechterrand ligt minstens een halve Amir binnen het gat, anders staat hij bij het
  afzetten nog onder het dak en haalt hij hem niet;
- elke stap is minder dan de sprong (200); 150 is ruim;
- de bovenste ligt binnen een sprong van de grondlijn en loopt door tot de linkerrand van het
  gat: daar stapt hij de savanne op.

Zolang zijn voeten tussen het dak en de grondlijn zitten, houdt `holteBlok` hem binnen het gat,
want zijwaarts zit daar het grondpakket. Op de savanne boven een gang dragen de treden eronder
niet (`supportHeight`). Test 4 heeft zo'n trap: van 900 diep in zes stappen van 150 naar boven.

```
gaps:     [ {x: -1000, w: 620}, {x: -3400, w: 900} ],       ingang, en de uitgang van -3850 tot -2950
holtes:   [ {r: -540, l: -3850, diep: 900} ],
terraces: [ {r: -2850, l: -3850, h: -750}, {r: -3050, l: -3850, h: -600}, ... {r: -3650, l: -3850, h: -150} ]
```

`levelcheck.py` kijkt dit na onder `onder de grond`.

### Hoogteverschil onder de grond

Een gang die dieper wordt, of waar je klimt en weer daalt, is **één gang** met de diepste `diep`,
en de hogere stukken zijn treden: terrassen met een negatieve `h`, net als de trap naar buiten.
Je landt dan op een richel, loopt eraf naar de bodem, klimt met een kei of een richel weer op,
en daalt weer. Alles wat voor terrassen geldt, geldt hier ook; daarbovenop kapt het dak elke
sprong af op -441.

Wat niet werkt, en waarom. Elk hiervan is nagelopen met de speelrobot (zie hieronder) in een
proefgang, en `levelcheck.py` meldt ze:

- **Twee gangen tegen elkaar** (de ene dieper dan de andere). `holteBlok` houdt Amir in allebei
  tegelijk vast: op de naad duwt de ene wand hem terug en de andere ook, en daar staat hij voorgoed
  klem, ook als hij er net in is gevallen.
- **Een terras op de savanne boven een gang.** Zijn wand wordt tot onder in beeld getekend en
  houdt hem ook tegen, dus in de gang staat een lichte stenen pilaar waar hij niet langs komt.
- **Een kei in de gang die tot in het dak reikt.** Op een trede van -520 staat de bovenkant van
  een kei op -406, en daar mogen zijn voeten niet komen: hij komt er niet overheen en niet langs.
- **Decor dat hoger is dan de gang.** Alles staat op de bodem, ook een boom, en die steekt dan
  door het dak. Een doornbos of een dorpsplaat net zo.
- **Een ingang die maar half boven de gang ligt.** Wie aan de kant zonder gang erin stapt, valt
  recht naar beneden (in een val loop je niet meer) en is dood.
- **Een gang die de speer overdekt.** Aan het begin staat je speer op `SPEAR_AHEAD` (-260) in de
  grond; ligt daar een gang, dan staat hij beneden op de bodem en begin je zonder.
- **Een gang minder diep dan 441.** `readLevel` maakt er zonder iets te zeggen 441 van, en dan
  kloppen je treden niet meer.
- **Vallen met `valschade`.** De val door de ingang telt ook: een ingang boven een richel op -700
  kost al twee levens. Tel de vallen langs de hele route op tegen de drie levens en de kalebassen
  die onderweg liggen.

Wat het spel zelf regelt, zodat je er als ontwerper niet op hoeft te letten:

- **Water kijkt naar de hoogte.** `waterDepthAt(x, h)` geeft 0 voor wie beneden in een gang
  staat: een poel boven een gang maakt Amir daar niet nat, traag of zwak in de sprong.
- **Decor in een gang is donker.** Props, keien, doornbossen en de personages beneden in een
  gang krijgen hetzelfde licht als alles daar, want de lichtkaart ligt eroverheen.
- **Hyena's komen op de goede hoogte.** Hyena's in een gang worden pas losgelaten als Amir zelf
  beneden is, en komen dan uit de gang aanrennen (`hyBuitenBeeld`), niet van de savanne erboven.
- **Vijanden blijven in hun gang.** Voor wie beneden staat is de eindwand van de gang een rand
  (`dropAhead`): daar lopen ze niet doorheen naar boven.

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

### Een level toevoegen (alleen na toestemming)

1. De definitie erbij, na de laatste van die reeks.
2. De naam in de array van die reeks (`LEVELS`, `DIEP_LEVELS`, `RENEW_LEVELS`, `WINTER_LEVELS`).
3. Een ondertitel in `SUBS`, op de naam van het level.
4. Een eigen uitzicht in `SCENES` als het level er anders uit moet zien.
5. `python3 tools/levelcheck.py` draaien, en elke FOUT oplossen voor je commit (zie
   hieronder).

### Een episode toevoegen

Die vijf stappen, plus: een knop in `menuChoose`, een eigen `menuXxx`-blok in de
HTML naar het voorbeeld van `menuWinter`, en die aanmelden in `buildCards`,
`markCards` en `showMenu`.

### Een vijand of prop toevoegen

Tekencode en gedrag erbij, opnemen in `PROPS`, `VILLAGE` of de dierenlijst, en
knoppen in de sandbox. Pas daarna is de vraag aan de orde of er een level bij moet.

## Sandbox

De sandbox start met vlakke grond en een leeg level, geen automatische vijanden en
geen levens. Een knop erbij is twee dingen: een `<button>` in `<div id="sandbox">`
(een eigen `.row` met een `<label>` als het een nieuw onderwerp is) en de afhandeling
in de sandbox-sectie van de code. De rijen staan in tabbladen per categorie (`.sbcat`:
Vijanden, Speer en spullen, Decor, Terrein, Beeld en geluid), want alles onder elkaar past
niet meer op het scherm. Zet een nieuwe rij in de categorie waar hij hoort; een nieuwe
categorie is een `.sbcat` met een `data-cat` en een knop met dezelfde `data-sbcat` in `#sbtabs`.
Van rechts, Alles weg en Terug naar menu staan eronder, buiten de tabbladen. Spawnen gebeurt net binnen beeld aan de gekozen
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

## Levels nakijken: tools/levelcheck.py

Na elk nieuw level, en na elke wijziging aan een level, draai je:

```
python3 tools/levelcheck.py            alle levels
python3 tools/levelcheck.py "Test 4"   alleen de levels waarvan de naam dit bevat
python3 tools/levelcheck.py -v         ook de info-regels
python3 tools/levelcheck.py level.json een level uit de bouwer, voor het in de HTML staat
```

Het script leest de leveldefinities uit de HTML, samen met de getallen waar het spel
zelf mee rekent (`CHAR_H`, `JUMP_V`, `GRAVITY`, de loopsnelheid en de sprint, `PLAFOND_WEG`,
de maten van keien, klif en fakkels). Het verandert niets aan de levels, het meldt alleen.
FOUT betekent: stuk, of tegen een regel uit dit document in. LET OP betekent: het werkt,
maar krap, of het spel lost het stilletjes voor je op. Een nieuw level gaat pas de deur uit
zonder FOUT. Wat het nakijkt: velden die `readLevel` niet kent, ravijnen tegen de echte
sprong (met het plafond en het water erbij), decor boven een ravijn met dezelfde maten als
`schoonLevel`, het plafond boven keien en treden, rechtop kunnen lopen, of elke trede met
een sprong, een richel of een kei te halen is, of de klif achter de fakkels staat, alles
rond een gang onder de grond (zie "hoogteverschil onder de grond"), en met `valschade` of Amir
de vallen langs de route overleeft.

**De sprong.** `JUMP_V` en `GRAVITY` geven op papier 208, maar het spel rekent per beeld (eerst
de zwaartekracht, dan de hoogte), en dan komt hij lager uit: op 60 beelden per seconde 200, op het
traagste toestel (het spel neemt hoogstens 0,05 seconde per beeld) 184. Gemeten: een trede van
199 haalt hij, een van 203 niet. Het script rekent daarom met 200, en de sprong over een ravijn
ook per beeld.

**De route.** Voor de vallen loopt het script het level af zoals een speler dat doet: naar links,
over een gewoon ravijn springend, tegen een wand of kei op, en van een rand af op looptempo. Van
een kei of een richel springt hij liever dan dat hij valt, als hij dan hoger uitkomt. Waar hij
neerkomt rekent het per beeld uit, dus een val van een terras op een lagere trede die net verderop
begint, telt als de kleine stap die het in het spel ook is.

Maten die aan het scherm hangen rekent het uit voor 1280 bij 720 op Formaat 25; met `--hoog`
en `--formaat` kijk je een ander scherm na.

**Meldt iemand iets in een level dat niet samen kan** (een laag plafond boven een kei om op
te springen, een poel vlak voor een ravijn), dan komt dat er als regel bij: een functie met
`@regel('naam')` in `tools/levelcheck.py`, met de getallen uit de code en niet uit het hoofd.
Draai daarna alle levels opnieuw en meld wat de nieuwe regel in de bestaande levels vindt,
zonder die levels aan te passen (regel 1).

## De speelrobot: tools/speelrobot.js

`levelcheck.py` rekent, de speelrobot speelt. Hij laadt het echte spel in Chromium, zet een level
klaar en loopt het naar links uit op een vaste 60 beelden per seconde, los van hoe snel de
computer is. Hij springt als hij vastloopt, springt over een ravijn zonder gang eronder, laat zich
in een ingang vallen, pakt zijn speer, steekt naar doornbossen en vijanden voor hem, en blijft op
een kei staan om er vanaf te springen. Hij meldt waar hij landt, wat een val kost, waar hij
vastloopt en wat er in de console staat.

```
node tools/speelrobot.js "Test 4"               een level uit de HTML, op naam
node tools/speelrobot.js level.json --taai      een level uit de bouwer; --taai: levens komen terug
node tools/speelrobot.js "Test 4" --shots map   elke anderhalve seconde een schermafdruk
```

Hij heeft Node en Playwright nodig (`npm i -g playwright`), en start zelf een webserver. Hij is
geen speler: een eindbaas verslaat hij niet, en een sprong die precies getimed moet worden mist
hij. Loopt hij vast waar `levelcheck.py` niets meldt, kijk dan wat daar staat. Is het de robot,
laat het dan; is het het level, dan hoort er een regel bij. Zo zijn de regels onder de grond
ontstaan.

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
