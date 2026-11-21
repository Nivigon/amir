# Water en regen per uitzicht: het plan

Een werkplan in stappen. Stap 1 loopt in de chat waar dit plan begon; elke volgende stap krijgt een eigen chat: lees
dit bestand, doe de eerste stap die nog open staat, en werk daarna de stand hieronder bij. Hoe het water nu in elkaar zit staat in `notities/water.md` (`WATER`,
`waterVul`, `waterLuchtKleur`, `waterRingen`); het weer in "het weer" (`WEER`, `weerNu`).

## Stand

| stap | wat | stand |
| --- | --- | --- |
| 1 | regen in het regenwoud: de kleur van het water en de gloed van de zon | **open**: de varianten liggen voor, de opdrachtgever kiest (zie hieronder) |
| 2 | plassen die vollopen en spetteren (lawaai voor sneak) | wacht op 1 |
| 3 | de rivier in het regenwoud: bruin, schuim, drijfhout, wortels | wacht op 1 |
| 4 | de rivier zwelt aan bij zware regen (waden, stam als brug, drijfhout dat duwt) | wacht op 3; nieuwe mechaniek, eerst sandbox |

## Waarom

In het regenwoud is al het water nu hetzelfde lichtblauw als op de savanne (`WATER.palet` is een palet voor alles):
de plassen lijken uit een zwembad te komen en de rivier is zwembadblauw met een blauwe val. In een donker, groen
bos valt dat uit de toon. Tegelijk regent het nu met de zon er vol bij, zonder dat de zon iets met het water doet.

## Stap 1: de kleur van het water en de gloed van de zon

Er zijn vier varianten bekeken op een echt beeld uit het spel (plas en poel in de regen, uitzicht `regenwoud`):

- **A** zoals nu, lichtblauw.
- **B** regenwoudwater: donker, thee en olijf (zoals echt bosriviertjes, gekleurd door blad), met een zweem van de
  horizonkleur erin (dat doet `waterLuchtKleur` al met `WATER.lucht`).
- **C** B plus een warme gloed van de zon: het sterkst op de verre rand van het water en aan de kant waar de zon
  staat, en naar voren toe weg; een paar warme glinsters in plaats van witte.
- **D** C op halve sterkte.

**Advies (Claude):** B als kleur, met de gloed van C, en de gloed die meegaat met het weer: lichte regen met de zon
erdoor geeft C (een "zonnige bui", dat is ook het mooiste moment), zware regen en onweer zakken naar D, en dikke mist
dooft hem bijna. Zo hoeft de zon niet weg bij regen en zegt het water toch wat voor weer het is.

**Te beslissen bij de start van de chat:** of de opdrachtgever dat advies volgt, of liever een andere variant.

Aanzet voor de bouw (stap 1):

1. Een veld `water` in een uitzicht van `SCENES` (of in `BIOMES`), bijvoorbeeld
   `water: { palet: {diep, midden, ondiep, glans}, lucht, gloed }`. Zonder dat veld blijft alles zoals het is
   (`WATER.palet`), zodat geen bestaand level verandert (regel 1). Alleen `regenwoud` krijgt het in deze stap.
2. De gloed rekent uit `sun` in het uitzicht (`[x, y, straal, kleur]`, voor het regenwoud `[0.30, 0.22, 0.075,
   '#ffd39a']`): een warm verloop over het water, sterk op de verre rand (`rug`) en onder de x van de zon, zwak
   vooraan. De kleur is die van de zon. Hij wordt getekend in `waterVul`, zodat plas, poel, rivier, val en bron hem
   allemaal krijgen.
3. De sterkte volgt het weer: `weerNu.regen` en de mist dempen hem (zie de lijst hierboven). Liefst in een tabel in
   `WATER` (`gloed: { droog, regen, onweer, mist }`), zodat het bij te stellen is.
4. De glinsters (`WATER.glinster`) krijgen de kleur van de zon in plaats van wit, alleen waar de gloed is.
5. Sandbox (regel 2): onder het tabblad met het water een knop om tussen het oude en het nieuwe palet te wisselen, en
   de gloed aan en uit. Nakijken in Test 67 (water) met het uitzicht op `regenwoud` en het weer op regen.
6. Schermafdrukken voor en na met Playwright (zie hieronder), en de opdrachtgever laten kiezen of bijsturen.

Niet in stap 1: de lucht bewolkt maken of de zon weghalen bij regen, de druppelstralen uit het bladerdak en de
spetterkroon. Die stonden in de eerste schets en kunnen er later bij, als eigen stap.

## Stap 2: plassen die vollopen

- Een plas in een regenwoud-uitzicht groeit met het weer (van een kuil in het mos tot een volle plas) en krimpt weer
  als het droog wordt. Een kuil die nog leeg is, is een donkere vlek in het mos.
- Door een plas lopen geeft een lawaaipuls voor sneak (`lawaaiPuls`): een bandiet hoort je spetteren, kruipen blijft
  stil. Lees eerst `notities/sneak.md`.
- De plas spiegelt wat erboven staat (bomen, een vijand op een tak of terras), platgedrukt, zoals in de schets.
- Misschien: door een volle plas sprinten laat je een stukje doorglijden. Pas als de rest goed is.

## Stap 3: de rivier in het regenwoud

- Bruin en troebel water (een eigen palet in het `water`-veld van stap 1, warmer dan de plassen), schuim op de val in
  plaats van helder blauw, bladeren en een stam die meedrijven (eerst decor), wortels langs de oever.
- Opletten: de rivier met waterval is af en mag in elk nieuw level (`notities/water.md`); een rivier op de savanne
  houdt zijn kleur.

## Stap 4: de rivier zwelt aan

Een nieuwe mechaniek, dus eerst knoppen in de sandbox, en een testlevel alleen na toestemming (regel 3).

- Bij zware regen of onweer stijgt het water over de oevers: Amir waadt (zoals in een poel: trager, lager springen).
- Een omgevallen stam als brug. De hangende stam (`HSTAM`, Test 82) die in de rivier valt is een kandidaat.
- Drijfhout dat meestroomt en je wegduwt.
- Regel 7 nalopen: houdt hoog water een vijand tegen, en mag een slang erdoor?

## Water in andere levels: zou het daar ook anders moeten?

Ja, en het veld `water` van stap 1 maakt dat per uitzicht mogelijk zonder iets te forceren. Een voorstel, niet om
nu te bouwen (de echte episodes blijven met rust tot de opdrachtgever het vraagt):

| uitzicht | water | gloed |
| --- | --- | --- |
| savanne overdag | het blauw van nu past, iets meer lucht erin | zwak, wit-geel |
| ochtend, avond | het blauw, maar warmer | sterk en goudoranje, de zon staat laag: hier valt het meeste te winnen |
| nacht | bijna zwart, blauwgrijs | geen zon; een zilveren streep van de maan, als die er is |
| winter | koud grijsblauw, een dunne ijsrand langs de oever, geen regenringen maar sneeuwvlokken die verdwijnen | wit en zwak |
| regenwoud | thee en olijf (plassen), bruin (rivier) | warm, gedempt door regen en mist (stap 1) |
| stad | de rivier oker en lemig, zoals een Sahelrivier; de fontein blijft helder (die wordt onderhouden) | warm, middag |
| onder de grond, in een gang | zwart, met alleen de fakkels en de lichtkaart erin weerspiegeld | geen zon, wel fakkels |

## Schetsen en schermafdrukken

De schetsen uit de chat van 21-11-2026 staan niet in de repo. Zo zijn ze gemaakt, om ze opnieuw te maken:

- Een proeflevel als object (geen nieuw level in de HTML): `lagen: 'regenwoud'`, `vredig: true`, `weer: [{x: 400,
  soort: 'regen', sterkte: 1}]`, en `wateren` met een plas, een poel en een rivier. Laden met
  `setLevel(0, [def]); beginPlay('medium')`, wachten tot het laadscherm weg is, `world` op een x zetten en een
  schermafdruk maken. De HUD weg met de stijl `*{visibility:hidden} canvas{visibility:visible}`.
- De server en de Playwright-opzet zoals in `tools/speelrobot.js`.
