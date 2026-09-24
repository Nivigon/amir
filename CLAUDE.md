# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Bestaande levels blijven met rust.** De leveldefinities in de HTML
(`GIJS_LEVEL` tot en met `PANTER_PLUS`, `ROSA_1` en `ROSA_2`, `RENEW_1` tot en met
`RENEW_10`, `WINTER_1` en `WINTER_2`) zijn bevroren. De levels in Episode Test levels
(`TEST_1`) vallen daar niet onder: die zijn er juist om aan te rommelen. Er komt geen nieuwe vijand,
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
| globale lichtlaag | kleurwaas over het beeld, volgt de zon van het level |
| beeld: de grote of de kleine spriteset | `KLEIN_FAM`, de keuze groot of klein, `zetBron` |
| hppotion | de drinkkalebas |
| bukken, jump frames, tempo | Amir zijn bewegingen |
| rotsen om op te springen | `rocks`, en het automatisch bijgroeien |
| winter: episode Winter World | `WINTER_SRC`, `winterOn()`, `winterPic()` |
| bodem en sneeuwdek | het veld `sneeuw`: savanne of rots, en het dek in vier standen |
| levels voor Rosa / Episode Renew / Episode Winter World | de leveldefinities |
| Episode Test levels | `TEST_1`: korte proefstukken, los van de echte episodes |
| terrassen en richels | `terraces`, `ledges`, klimmen |
| de rotswand rechts | `cliffs`, het einde van het level |
| grotten: rots als een raster van cellen | `grotten`: het raster, de randen, de verstrooiing, de botsingen |
| schorpioen, het projectiel, spannen en werpen, de geworpen speer | de speerworp |
| personages, dorpsdecor | NPC's, `VILLAGE`, de dorpsplaten |
| stap voor stap leren spelen | het `tutorial`-systeem van de Rosa-levels |
| gaten in de grond | `gaps`, inclusief de overkant en de nevel |
| stof, sneeuwval, het weer | deeltjes en het weerplan per potje |
| vegetatie, water, doornbos | `props`, `water`, `thickets` |
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
| `winter` | `true` zet het hele level in de sneeuw (witte dieren, sneeuwversies van het decor) |
| `sneeuw` | sneeuw op de grond, los van `winter`: `{soort, dek, van, tot}` (zie hieronder) |
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
| `cel` | celgrootte in wereld-px (standaard `GROT_CEL`, 120) |
| `y` | onderrand van het raster boven de grondlijn, in cellen (standaard 0) |
| `grid` | de rijen van boven naar beneden; `#` is vol, al het andere leeg |
| `seed` | dezelfde seed geeft elke keer dezelfde verstrooiing |
| `strooi` | hangblokken, richels en keien vanzelf neerzetten (standaard `true`) |
| `massief` | de volle cellen blokkeren (standaard `true`) |
| `decor` | met de hand erbij: `[{k, x, y, f, s}]` |

Cellen zijn altijd vierkant op het scherm, ook als je aan de Formaat-schuif draait: `cel`
is een maat in wereld-px en die is gelijk aan schermpixels. De hoogte in sprite-eenheden
(waar `ph` in rekent) volgt daaruit, en dus uit de schaal.

Buiten het raster is het lucht, behalve onder de laatste rij: daar loopt de aarde door.
De bovenkant van je rots is dus ook de bovenkant van het level, met de hemel erboven.
Moet de massa doorlopen tot buiten beeld, maak het raster dan hoger.

De tekencode kijkt per volle cel welke buren leeg zijn:

| buur leeg | wat erop komt |
| --- | --- |
| onder | `plafond_strook.png`, horizontaal getegeld; de tanden hangen in de open ruimte |
| boven | de gewone grondrand van het spel, als korst die naar onderen in het steen uitvloeit |
| links of rechts | `wand_rand.png`, verticaal getegeld, gespiegeld voor de andere kant |
| binnenhoek | `hoek_plafond_wand.png`, uitgelijnd op `wand_binnenrand_x_onderaan` |

Alle volle cellen worden eerst dicht gelegd met `rotstextuur.png`. Wat de set niet heeft
vullen de brokken op: waar een vloer op een wand uitkomt komt een handvol keien over de
naad, en waar een rotspunt uitsteekt komt een richel of een hangblok overheen.

Drie dingen waar je op moet letten als je hieraan werkt:

Eén pixelschaal voor de hele grotset, uit de celgrootte (`grotS`): de plafondband is
precies één cel dik. Teken nooit een stuk op een andere schaal, want dan verspringt de
korrel van de rots halverwege. De grondrand komt uit een ander plaatje en heeft daarom
zijn eigen schaal (`grotEdgeS`), ook uit de celgrootte.

Geen tint, geen overlay, geen `globalCompositeOperation` op deze sprites. Ze zijn allemaal
hetzelfde warm grijsbruine gesteente; elke waas eroverheen maakt van de ene helft grijs en
van de andere bruin.

Tegels worden een keer op maat gezet (`grotTegelSet`) en daarna op hele pixels neergelegd.
Verklein je een naadloze tegel rechtstreeks met `drawImage`, dan klemt de resampler op de
rand en zie je de naad alsnog als een lijn door het steen lopen.

Alleen `wand_richel` draagt, met een hitbox die alleen de bovenkant van het brok beslaat.
Hangblokken en losse keien zijn puur decor.

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

De grotset in `design/grot/` hoort wel in de kleine set: die stukken zijn de grootste
bronnen van het spel en worden tot een tiende getekend. Dat mag hier omdat de tekencode
met de maten uit `grot.json` rekent en elk stuk naar die maat rekt; de ankerpunten
schuiven dus niet mee met de bronmaat. `grot.json` zelf blijft buiten de kleine set,
want `gen-klein.py` pakt alleen png's.

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
