# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Bestaande levels blijven met rust.** De leveldefinities in de HTML
(`GIJS_LEVEL` tot en met `PANTER_PLUS`, `ROSA_1` en `ROSA_2`, `RENEW_1` tot en met
`RENEW_10`, `WINTER_1` en `WINTER_2`) zijn bevroren. Er komt geen nieuwe vijand,
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
| levels voor Rosa / Episode Renew / Episode Winter World | de leveldefinities |
| terrassen en richels | `terraces`, `ledges`, klimmen |
| de rotswand rechts | `cliffs`, het einde van het level |
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
| `rocks` | keien om op te springen: `{x, s}` |
| `spawns` | vijanden: `{x, k}` met `k` = `groen`, `zwart`, `scorp`, `hyenas`, `panter` |
| `props` | decor: `{x, k, s, f, v}`, `k` uit `PROPS`, `f` spiegelen, `v` verre laag |
| `village` | dorpsplaten uit `VILLAGE`: `{id, x, depth, flip}` |
| `gaps` | ravijnen: `{x, w}` |
| `water` | poelen: `{x, n}` met `n` = aantal middenstukken |
| `thickets` | doornbossen: `{x, n, seed}` |
| `terraces` | terrassen om op te klimmen: `{r, l, h}` (rechterrand, linkerrand, hoogte) |
| `ledges` | richels aan een wand: `{x, h, s}` |
| `hppotions` | drinkkalebassen: `{x, y}` |
| `fg` | strook waarover de voorgrondbegroeiing ligt: `{from, to}` |
| `arena` | het veld van de eindbaas: `{c}` |
| `cliffs` | de afsluitende rotswand: `{x}`, staat altijd achter `ends` |
| `ends` | de fakkels die het level uitspelen: `{x}` |
| `npcs` | dorpelingen: `{x, k, f, s}` |
| `tips` | tekst onderweg: `{x, t}` |
| `tutorial` | alleen de Rosa-levels: stapjes met uitleg |

`schoonLevel` kijkt elk level bij het laden na en schuift decor dat boven een ravijn
staat naar de kant, of haalt het weg. Reken daar niet op als ontwerper: zet het
meteen goed.

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
