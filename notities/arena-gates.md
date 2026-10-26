# Arena gates: drie poorten in de rots

`SB_GATES`, `sbGates`, `sbGatesVeld`, `sbGatesUpdate`, `sbGatesLaat`, `gatesRand`, `gatesWeg`. De sectie in de HTML
heet `// ---- arena gates: drie poorten in de rots, elke ronde drie vijanden ----`.

## Wat het is

De derde keuze onder **Sandbox** in het menu (`startSandbox(true, true)`, naast de vrije sandbox en de arena-modus).
Het is de arena-modus (levens, de wizard, Onsterfelijk, de kalebassen, de teller, de afteller) met een eigen veld en
een eigen spawner: een arena van een scherm breed met drie stenen poorten, en elke ronde komt uit elke poort een
vijand. Niets ervan staat in een level; het is ontworpen in de sandbox (regel 2) en het veld is vast.

## Het veld (`sbGatesVeld`, uit `sbArenaVeld`)

Om het arena-midden (`arenaMidden()`), `SB_GATES.breed` (1600) wereld-px breed; de zoom volgt het scherm
(`sbGatesMaat`: `sbView = W / breed`, tussen `zoomMin` 0,5 en `zoomMax` 1), zodat de poorten op elk scherm aan de
randen staan. De knoppen Uitzoomen staan daarom in de gates niet in de wizard. Het uitzicht is het donkere hart
(`lagen: 'dark_hart'`), de fakkels doen het licht.

- Links een grote rots (het levelveld `rotsen`, de pieken op 4,8 Amir) waar een rotsplateau (`zwevers`, look rots,
  looplijn 560, onderkant 480) in snijdt alsof de rots hem draagt; rechts een kleinere rots (de spits op 2,8).
  Een rots uit `rotsen` wordt voor `drawClimb` getekend, dus achter het plateau (zie `notities/decor.md`).
- Drie poorten met het ijzeren valhek en zijn tandwieltje (`poorten` met `hek: true`, zie "Het hek en de regie" in
  `notities/poort.md`), hier met een eigen tempo (`hekDuur` op de poort, `SB_GATES.hekDuur` 2,2 s in plaats van
  `HEK.duur` 4,6): `l` en `r` laag
  aan de zijkanten (`boog_steen`, 640 links en 620 rechts van het midden) voor de rotsen, `h` hoog op het plateau
  (`boog_laag_1` op 0,8, op 720 links), half in de rots.
- Drie fakkels in het steen, botten en een gespleten schild op de vloer, een gebroken speerteken. Geen kei: een kei
  in het midden zou een schuilplek zijn (regel 7) en dat hoort niet in een arena.
- Het arena-object: `{ban: true, sb: true, gates: true, geenWand: true, ruimte: 0}`. `ban` zet de camera vast in
  het midden en klemt Amir op de schermranden (`arenaVast`), `sb` laat `arenaTick` en `arenaHudTeken` eruit stappen,
  `geenWand` laat `arenaAchtergrond` de middenrots en de zijwanden overslaan. `level.rechtsWall` ligt ver voorbij
  de rand, zodat een vijand van rechts buiten beeld kan opkomen.

Amir begint rechts van het midden met de speer in de hand en een reservespeer op de rug, zoals in de arena-modus.

## De rondes (`sbGatesUpdate`, in plaats van de stroom en de golven)

De stand staat in `sbArenaCfg.g` (dezelfde velden als de golven, zodat de teller en de kalebassen per ronde
werken; `modus` staat in de gates altijd op `golven`), de rest in `sbGatesSt`.

1. **kondig**: `SB_GOLF_KONDIG` seconden "Ronde n" groot in beeld. Daarna `sbGatesOpen`: de drie hekken gaan
   tegelijk omhoog (`hekOp`; `hekUpdate` takelt ze met het takelgeluid, op `HEK.open` gaat de poort open en boven
   klinkt de klap van het ijzer).
2. **golf**: zodra een poort open is komt zijn vijand eruit (`sbGatesLaat`, via `sbSpawn` op de x van de
   opening, dus de knoppen onder Gedrag in de wizard gelden ook hier; met `hoogte` zoekt `sbSpawn` de vloer vanaf
   het plateau), wakker (`zWacht = false`) en in het donker van de opening (`o.uitT`). `SB_GATES.dicht` seconden na
   het donker valt het hek weer dicht (`sbGatesSt.dicht`, `poortSluit`, `hekDicht`). `poortOpen` geeft in de gates
   geen melding per poort. De ronde is pas voorbij als alles dood is, ook
   wie beneden nog moet binnenkomen (`sbGatesSt.wacht`): dan `rust`, en `sbKalStap(1)` voor de kalebassen.
3. **rust**: `sbGatesCfg.rust` seconden (de knop **Rust tussen rondes**, de enige knop naast de soorten), dan
   `sbGatesVolgende`.

Na de afteller van Start begint ronde 1 meteen (`sbArenaGo` roept `sbGatesVolgende` en `sbGatesOpen`).

## Wie er komt (`sbGatesInhoud`)

Uit de soorten die aan staan (`sbGatesCfg.per`, bij het openen van de modus alles aan; klik uit wat je niet wilt).
Door een poort kunnen `SB_GATES_SOORTEN`: zandslang, zwarte slang, knockslang, schorpioen, de fosforgroep, bandiet,
schildbandiet (makkelijk en moeilijk) en meelman. Hyena en panter komen van de beeldrand en niet uit een poort, de
kooiman heeft zijn eigen entree: die drie staan niet in de lijst (en de rij Kooiman onder Gedrag is weg).

- Per lage poort een uit alles wat aan staat en al meedoet; door de bovenpoort (de lage boog) alleen wat kruipt
  (`SB_GATES_BOVEN`: de drie slangen en de schorpioen).
- **Zwaarder per ronde**: een soort doet mee vanaf de ronde `vanaf` uit `SB_ARENA_SOORTEN`, naar verhouding: de
  lichtste soort die aan staat doet vanaf ronde 1 mee, de rest zoveel rondes later als hun `vanaf` hoger ligt
  (staan alleen de zwarte slang en de schorpioen aan, dan komt de schorpioen in ronde 1 en de zwarte in ronde 2).
  Wie mag weegt zwaarder naarmate zijn `vanaf` hoger is.
- **Nooit drie snelle tegelijk**: hoogstens `SB_GATES.snelMax` (2) uit `SB_GATES_SNEL` (bandiet, schildbandiet,
  de fosforgroep) per ronde.
- Een poort zonder geschikte soort blijft dicht die ronde (staat alleen een bandiet aan, dan blijft de bovenpoort
  dicht); staat niets aan, dan zegt de teller "Zet een vijand aan".

## Boven: de schieter wacht, de rest loopt de rots in

- Een schieter (`SB_GATES_RANGED`: de zwarte slang en de knockslang) krijgt `gatesRand`: hij kruipt naar de rand
  van het plateau (hij stopt niet eerder op zijn gewone afstand), blijft daar staan (aan de rand keert een spuwer
  anders om en loopt weg) en vuurt alleen met een vrije zichtlijn naar Amir (`sbGatesZichtlijn`, vanaf zijn kop
  die op de rand ligt; het plateau zelf houdt het zicht tegen als Amir eronder staat), ook als de knop Zicht van
  de sandbox uit staat. Hij daalt niet af: een vijand komt nooit zelf van een zwever (regel 7).
- Al het andere krijgt `gatesWeg` (in `updateSnake` en `updateScorp`): hij loopt over het plateau naar links,
  zonder naar Amir of de rand te kijken, tot hij voorbij `SB_GATES.wegGrens` in de rots is (`state 'gone'`), en
  komt `SB_GATES.terug` (2) seconden later beneden binnen, links of rechts, net buiten beeld (`SB_GATES.buiten`)
  en naar binnen lopend (`sbGatesTerug`, `sbGatesSt.wacht`). Zo zie je eerst wat eraan komt.

## De wizard, de teller en de opslag

In de gates verbergt `sbGatesToon` de knoppen Stroom/Golven en de kant, de getallen per soort en de +1 (de lijst
krijgt de klasse `gates`: twee kolommen met alleen de aan/uit-knoppen) en toont de rij **Rust tussen rondes**;
`sbWizToon` zet de titel op Arena gates en verbergt de kaartjes (het veld ligt vast), Ruimte, Uitzoomen en de rij
Kooiman. De rest van de arena-modus blijft: Onsterfelijk, Kalebassen (per ronde), de speerknoppen, de tribes,
tijd van de dag, weer en muziek. De teller zegt Ronde in plaats van Golf, en het record staat apart
(`sbGatesBest`, `amir.gatesBestGolf`); de beste tijd van de arena-modus wordt in de gates niet bijgewerkt
(`sbArenaDood`). De opzet wordt onthouden onder `amir.gatesCfg` (welke soorten, de rust, Onsterfelijk, de
kalebassen en de verhuisde knoppen), los van `amir.arenaCfg`. R begint bij ronde 1 (`restart` bouwt het veld
opnieuw, `poortReset` zet de hekken dicht, `sbGatesReset` leegt de wachtrijen).

## Nog niet

Geen level en geen Maker: de arena leeft alleen in de sandbox. De rots achter een poort kan in een level ook met
`wand` op de poort (zie `notities/poort.md`); de gates gebruiken `rotsen`, omdat dat voor de plateaus getekend wordt. Een poortarena uit de Maker (een instelling op het
level, de controle op drie poorten, een plateau tot aan de rand) is het volgende stuk van het plan, en de
afwerking van een dun plateau (de aardrand-plaat met ronde hoeken) en een fade over de bovenrand ook.
