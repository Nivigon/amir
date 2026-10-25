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
  (de spawner gebruikt dan `sp.x` in plaats van `spawnPoint`), op de hoogte van de spawn (`boven`, `y`);
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

Objecten, **Poort (stenen boog)**. In het paneel: **Boog**, **Gespiegeld**, **Look** (vanzelf, steen, sneeuw,
savanne; vanzelf is sneeuw als de cel onder de poort sneeuw is, `mkPoortLook`), **Vijand eruit** (geen =
alleen decor) en **Aantal** (1 tot 3, `MK_POORT_N`). Een zegel of rune krijgt **Opent poort**
(`mkVulPoortSelect`), net als Stuurt rijzer: een verwijzing naar het voorwerp (`poortObj`, `mkPoortVan`),
opgeslagen op celpositie (`poort: {c, r}`) en in het klembord als `poortRel`; spiegelen keert de poort om.
`mkNaarLevel` maakt er `poorten` van (`b1`, `b2`, ...) plus een spawn per vijand met `poort`. De controle
meldt een poort in een vaste cel of boven een ravijn zonder bodem (FOUT), een poort met een vijand maar
zonder schakelaar (LET OP) en een schakelaar die een lege poort opent (info).

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
  tot net in de grond reikt (`zak`). Op de sluitsteen het minitandwiel van het takelwiel (`tand`), met het touw
  (`touw_tegel.png`) naar de ring; zit de ring achter de stenen, dan loopt het touw tot de kruin. Opgaan duurt
  `duur` seconden: eerst kraakt het (`aanloop`), dan langzaam los en langzaam boven, met een schokje per tand
  (`schok`, `tanden`), het takelgeluid (`hekGeluid`, `sounds/takelen.mp3` herhaald), stof als de punten loskomen en
  een klap als hij boven is. Op `open` (0,8) gaat de poort echt open en komen de vijanden. Wie de poort ook opent
  (een zegel, een rune, de regie of de sandbox): `poortOpen` op een poort met hek takelt eerst het hek op (`hekOp`).
- `wand` de rotswand van de muur (`MUUR.src`, op `MUUR.hoogAmir`) achter de boog, met `HEK.wand.anker` achter het
  midden van de opening; `wandF` spiegelt hem. Decor, Amir loopt ervoor langs.
- `regie` de poort gaat vanzelf open als hij in beeld komt: op `HEK.inBeeld` van een half scherm van Amir, of
  dichterbij als hij dan nog niet heel in beeld is. Met `bij` (wereld-x) pas als Amir daar voorbij is; poorten die
  in hetzelfde beeld afgaan horen bij een regie en gaan samen open. Tijdens de regie staat Amir vast (`amirVast`),
  en springt geen schildbandiet (`cool`). Klaar is hij als elke poort open is, al zijn spawns eruit zijn en elke
  schildbandiet die eruit kwam (`m.uitPoort`) `uitLoop` Amir uit de opening staat; na `regieMax` seconden in elk
  geval. Een nieuwe regie wacht tot er geen levende schildbandiet meer is, zodat je niet midden in een gevecht
  vastgezet wordt. `levelcheck.py` telt `regie` als schakelaar.

Sandbox, Decor, Poort: **+ hek**, **+ rotswand**, **+ schildbandiet erin**, **Open de poort** (met hek: `hekOp`) en
**Hek dicht** (`hekDicht`, de vijanden gaan weer naar binnen). **Test 51: De poorten** is het proefstuk.

## Nog niet

De plaatjes staan nog niet in `klein/`: dat wacht tot hun maat op een telefoon gemeten is (zie
`design/boog/LEESMIJ.md`). Een poort zonder hek heeft nog geen geluid bij het opengaan, en geen echt level gebruikt een poort. De Maker kent het hek en de regie nog niet.
