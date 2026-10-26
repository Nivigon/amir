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

- `hek` met `true`: een traliehek voor de opening met een klein tandwiel in het steen erboven (`POORT.hek`,
  `poortHekTeken`, binnen `poortBeeld`; het wiel is het mini-tandwiel van de takelstam, `poortHekLaad`). Dicht staat
  het hek in de opening (`hekStand` 0); gaat de poort open, dan takelt `poortUpdate` het in `hek.duur` seconden omhoog
  (`hekDoel` 1, het wiel draait mee, het touw loopt van het wiel naar de bovenrand van het hek), en boven aangekomen
  klinkt de klap van `sounds/deurslam.mp3` (`deurSlamSpeel`, een keer voor hekken die tegelijk boven komen,
  `poortSlamT`) met een schok. De vijanden komen pas als het hek boven is (`poortOpen` telt `hek.duur` bij hun
  `poortWacht`). `poortSluit(id)` zet de poort weer dicht (het hek zakt, de poort kan opnieuw open): dat gebruikt de
  arena gates per ronde (zie `notities/arena-gates.md`). `poortReset` zet het hek dicht.

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

Een poort gaat per potje een keer open; `poortReset` (in `restart`) sluit hem weer, en `poortSluit(id)` tussendoor
(voor een arena die hem elke ronde opnieuw opent). Een hyena en een
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

## De arena gates

De sandbox-modus met drie poorten (een hoog op een plateau, twee laag) die elke ronde tegelijk opengaan, elk met
een hek: zie `notities/arena-gates.md`.

## Nog niet

De plaatjes staan nog niet in `klein/`: dat wacht tot hun maat op een telefoon gemeten is (zie
`design/boog/LEESMIJ.md`). Er is nog geen geluid bij het opengaan, en geen echt level gebruikt een poort.
