# Poort: een stenen boog, decor of de plek waar een vijand uitkomt

`POORT`, `poortTeken`, `poortOpen`, `poortKlaar`, `poortVoorTeken`. De sectie in de HTML heet
`// ---- poort: een stenen boog, decor of de plek waar een vijand uitkomt ----`.

## Het levelveld

```
poorten: [ {id: 'b1', x: -2012, k: 'boog_rots', f: true, y: 450, s: 1, look: 'sneeuw'} ]
```

- `id` de naam waar een zegel of rune met `poort` naar wijst (zonder: `poort1`, `poort2`, ...)
- `x` het midden van de opening, `f` spiegelt
- `k` de boog uit `POORT.soorten`: `boog_steen`, `boog_rots`, `boog_laag_1` tot en met `boog_laag_4`
  (de plaatjes uit `design/boog/`, maat en opening uit `metadata.json`)
- `y` een vaste vloerhoogte (een zwever, het dak van een gang); zonder `y` staat hij op `terrainH`,
  dus ook op een terras of op de bodem van een gang
- `s` een schaal bovenop de standaardmaat: de opening is `hoog` Amir hoog (hoog 1,65, laag 1,15)
- `look` de kleur (`POORT.looks`): `steen` (grijs), `sneeuw` (met een sneeuwkap, `_sneeuw.png`) of `savanne`
  (de steen in de warme kleur van de savannegrond, `_savanne.png`, dezelfde tint als de richel met look savanne).
  Zonder `look` kiest `poortLook` vanzelf: in een winterlevel sneeuw, anders steen. Alleen het plaatje van de
  look die een poort gebruikt laadt (`poortLaadLevel`). De versies komen uit `tools/boog_vulling.py`: de sneeuwkap
  met `rock_snow` uit `tools/sneeuw.py`, en in beide blijft de opening het donker van de gewone boog

De onderkant van de opening staat op de vloer. Zonder meer is een poort decor.

## Een vijand uit de poort

Een spawn met `poort: 'b1'` wacht achter die poort (`poortKlaar` in de spawner). Een zegel of rune met
`poort: 'b1'` opent hem (`poortOpen`, vanuit `zegelSchakel` en `runeDoet`, ook bij een koppel-zegel of
koppel-rune met `stuurt`). Dan:

- komen zijn spawns een voor een, `POORT.tussen` seconden na elkaar, precies op de plek van de opening
  (de spawner gebruikt dan `sp.x` in plaats van `spawnPoint`), op de hoogte van de spawn (`boven`, `y`). Ook de
  kooiman, de meelman en de fosforgroep lezen `boven` (het dak van een gang: `bovenVloer`, niet de gang-bodem);
- wacht een spawn achter de opening tot Amir binnen zijn triggerafstand is (`triggerDist`), en telt zijn beurt
  (`poortWacht`) pas dan af: een zegel of regiepunt mag dus ver van de poort liggen. Eerst schreef de spawner hem
  als 'ver voorbij' af als Amir meer dan 2,5 scherm weg was, en kwam hij nooit, terwijl de hint hem beloofde;
- ligt het donker van de opening nog `POORT.uit` seconden over wie eruit stapt (`poortVoorTeken`, na
  de vijanden getekend): hij komt uit het donker;
- komt hij wakker: `zichtZet` zet `zWacht` uit voor een spawn met `poort`, want hij komt omdat Amir
  de poort opende. Ziet hij Amir daarna `ZICHT.vergeet` seconden niet, dan valt hij gewoon in rust.

Een poort gaat per potje een keer open; `poortReset` (in `restart`) sluit hem weer. Een hyena en een
panter komen van de rand van het beeld en niet uit de poort (levelcheck: LET OP); de Maker biedt ze
niet aan, net als de hinderlaag en het duel van de kooiman.

## Wat mag waar

Een poort is **vast** decor: nooit boven een ravijn, en waar later een ravijn openscheurt schuift hij
naar de rand (`schoonLevel`, `schoonKomend`, `ravijnDecor`, `ravijnDecorReset`, `levelcheck.py`). Een
poort met `y` slaan die over. Schuift hij, dan neemt `poortOpen` zijn nieuwe x mee voor zijn vijanden.

## levelcheck

De regel `poorten`: een onbekende boog, twee poorten met dezelfde naam, een zegel, rune of spawn die naar
een poort wijst die er niet is, en een poort met vijanden zonder schakelaar zijn FOUT. Daarnaast telt een
poort mee in `voorbij het einde`, `boven een ravijn`, `waar een ravijn openscheurt` en `onder de grond`
(door het dak van een gang).

## In de Maker

Objecten, **Poort (stenen boog)**, en **Poort met hek** (het gereedschap `poorthek`: `mkKlik` zet een poort met
`hek: true`). In het paneel: **Boog**, **Gespiegeld**, **Look** (vanzelf, steen, sneeuw,
savanne; vanzelf is sneeuw als de cel onder de poort sneeuw is, `mkPoortLook`), **Vijand eruit** (geen =
alleen decor), **Aantal** (1 tot 3, `MK_POORT_N`), **Schaal** (0,8 tot 1,5, `s`), **Hek**, **Regie** met **Zet regiepunt**
en **Wis regiepunt** (`mkBijMode`: de volgende klik op een kolom is `bij`, opgeslagen als kolom en in het spel het midden
van die kolom; een gele stippellijn op de kaart, `mkPoortRegieTeken`), en **Rotswand** (geen of een soort uit
`HEK_WANDEN`, `mkPoortWand`) met **Wand gespiegeld**, **Hoogte** (`HEK_WAND_H`) en **Verschuif** (`HEK_WAND_X`). Op de kaart
staan de rotswand (`mkPoortWandTeken`) en het hek (`mkPoortHekTeken`) zoals in het spel, alleen het tandwiel altijd op de
sluitsteen. Spiegelen van een gebied keert ook de rotswand, zijn verschuiving en het regiepunt om (`bijDc` in het klembord). Een zegel of rune krijgt **Opent poort**
(`mkVulPoortSelect`), net als Stuurt rijzer: een verwijzing naar het voorwerp (`poortObj`, `mkPoortVan`),
opgeslagen op celpositie (`poort: {c, r}`) en in het klembord als `poortRel`; spiegelen keert de poort om.
`mkNaarLevel` maakt er `poorten` van (`b1`, `b2`, ...) plus een spawn per vijand met `poort`. De controle
meldt een poort in een vaste cel of boven een ravijn zonder bodem (FOUT), een poort met een vijand maar
zonder schakelaar en zonder regie (LET OP), een regiepunt meer dan `MK_POORT_BIJ_VER` (4) cellen van zijn poort (LET OP: Amir
staat dan stil terwijl de poort buiten beeld opengaat), een schakelaar die een lege poort opent, een poort met regie
maar zonder vijand en een hek dat niets opent (info). Een level met alleen poortvijanden krijgt geen standaard-slang
meer achter het eind (die kwam er alleen voor een level zonder enige spawn, tegen de vrije slangen). `tools/poorttest.js`
speelt dit alles door (zie `notities/tools.md`).

## Sandbox

Decor, **Poort**: drie bogen, **Sneeuw**, **Savanne** en **Steen** (de look van de laatste poort), **+ slang erin**, **+ schorpioen erin**, **+ bandiet erin** (in de laatst
neergezette poort) en **Open de poort**.

## Het hek en de regie

`HEK`, `hekTeken`, `hekUpdate`, `hekOp`, `poortRegie`. De sectie heet `// ---- het hek van de poort: een ijzeren
valhek dat omhoog getakeld wordt ----`, direct na de poort.

```
poorten: [ {id: 'p1', x: -1900, k: 'boog_steen', hek: true, wand: true, wandF: true, regie: true, bij: -10500} ]
```

- `hek` een ijzeren valhek in de opening (`design/boog/hek.png`). Het hek is breder dan de opening (`breder`) en
  wordt afgeknipt op de vorm van het gat (`<boog>_gat.png`, uit `tools/boog_vulling.py --gat`): de dwarsbanden lopen
  achter de pijlers door en het hek verdwijnt achter de stenen als het opgaat. Bovenin een schaduwverloop
  (`schaduw`, `schaduwA`), alleen op het ijzer. Het plaatje is een raster (`hekRaster`): links en rechts een vast stuk,
  daartussen een oneven aantal kolommen met de ring in het midden, en boven en onder een vast stuk met daartussen
  rijen, zodat de staven in elke boog even ver uit elkaar staan (`spatie`, in Amir) en het hek precies van de kruin
  tot net in de grond reikt (`zak`). Het minitandwiel van het takelwiel (`tand`) zit met een rotswand boven de
  boog op de rots (`tand.boven`), zonder rotswand op de sluitsteen (`tand.y`). Het touw (`touw_tegel.png`) ligt
  nooit over de rand van de boog: het stuk van het tandwiel naar beneden wordt voor de boog getekend
  (`hekAchterTouw`) en valt dus achter de stenen weg, en in de opening hangt het van onder de kruin naar de ring.
  Zit de ring achter de stenen, dan is daar geen touw meer. Opgaan duurt
  `duur` seconden: eerst kraakt het (`aanloop`), dan langzaam los en langzaam boven, met een schokje per tand
  (`schok`, `tanden`), het takelgeluid (`hekGeluid`, `sounds/takelen.mp3` herhaald), stof als de punten loskomen en
  een klap als hij boven is. Op `open` (0,8) gaat de poort echt open en komen de vijanden. Wie de poort ook opent
  (een zegel, een rune, de regie of de sandbox): `poortOpen` op een poort met hek takelt eerst het hek op (`hekOp`).
- `wand` een rotswand achter de boog; `wandF` spiegelt hem. Decor, Amir loopt ervoor langs. `wand: true` (en `'kaal'`)
  is de rotswand van de muur (`MUUR.src`, op `MUUR.hoogAmir`) met `HEK.wand.anker` achter het midden van de opening,
  zoals Test 51 hem heeft. In plaats daarvan kan `wand` een soort uit `HEK_WANDEN` zijn: de vier rotsen van de runes
  (`spits`, `pieken`, `zuilen`, `boog`, dezelfde platen als `RUNE_ROTSEN`, via `runeBeeld`) of de grotboog (`grot`,
  `MUUR_GROT`, via `grotMuurBeeld`). Per soort staat in `HEK_WANDEN` de hoogte zonder `wandH` (`hoog`, in Amir) en
  welk deel van de plaat achter het midden van de boog staat (`anker`). `wandH` zet de hoogte (in Amir), `wandX`
  schuift de rots opzij (in Amir, rechts is +). `hekWandBeeld`, `hekWandMaat`, `hekWandTeken`.
  Het minitandwiel zit alleen op de rots als die daar hoog genoeg is (`hekTandOpRots`: de alfa van de plaat boven het
  midden van de boog); anders, zoals tussen de twee zuilen of bij een lage rots, zit het op de sluitsteen en hangt er
  geen touw achter de stenen. De kale wand op zijn eigen maat en plek telt altijd als hoog genoeg, zodat Test 51 bleef
  zoals hij was. `levelcheck.py` meldt een onbekende soort als FOUT.
- `regie` de poort gaat vanzelf open als hij in beeld komt: op `HEK.inBeeld` van een half scherm van Amir, of
  dichterbij als hij dan nog niet heel in beeld is. Met `bij` (wereld-x) pas als Amir daar voorbij is; poorten die
  in hetzelfde beeld afgaan horen bij een regie en gaan samen open. Tijdens de regie staat Amir vast (`amirVast`),
  en springt geen schildbandiet (`cool`). Klaar is hij als elke poort open is, al zijn spawns eruit zijn (een spawn die buiten bereik achter de poort blijft telt
  niet mee, zie hierboven) en elke
  schildbandiet die eruit kwam (`m.uitPoort`) `uitLoop` Amir uit de opening staat; na `regieMax` seconden in elk
  geval. Een nieuwe regie wacht tot er geen levende schildbandiet meer is, zodat je niet midden in een gevecht
  vastgezet wordt. `levelcheck.py` telt `regie` als schakelaar.

Sandbox, Decor, Poort: **+ hek**, **+ rotswand** (elke klik de volgende soort uit `HEK_WANDEN`, en dan weer geen), **+ schildbandiet erin**, **Open de poort** (met hek: `hekOp`) en
**Hek dicht** (`hekDicht`, de vijanden gaan weer naar binnen). **Test 51: De poorten** is het proefstuk.

## Nog niet

De plaatjes staan nog niet in `klein/`: dat wacht tot hun maat op een telefoon gemeten is (zie
`design/boog/LEESMIJ.md`). Een poort zonder hek heeft nog geen geluid bij het opengaan, en geen echt level gebruikt een poort.
