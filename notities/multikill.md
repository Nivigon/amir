# Multikill en het levelrapport

Kills kort na elkaar zijn een reeks, en een reeks geeft een goudstuk extra. Na het level laat het rapport zien hoe het ging.
Aan met `multikill: true` en `rapport: true` in een level; nu alleen Test 70. In de sandbox de knop **Multikill** onder
Vijanden (met **Goud bij een kill** erbij zie je de bonus vliegen). Code: de kop `// ---- multikill`, met `MKILL`,
`mkillKill`, `mkillStap`, `mkillAfsluit`, `mkillRapport`.

## De reeks

- Valt de volgende vijand binnen `MKILL.venster` (3 s) na de vorige, dan loopt de reeks door. De klok loopt op spel-tijd
  (`mkillStap(dt)` in de lus, na `straatStap`), dus een executie, sluipaanval of pauze die de wereld stilzet, kost niets.
- Elke kill gaat via `vijandDood`, en daar roept `mkillKill(wie)` voor `goudKill`, zodat `goudKill` met `mkillToon()` de
  toon van zijn tink kan lezen.
- Bij de tweede kill is het een multikill: in een level met goud (`goudTelt`) vliegt er `MKILL.bonus` (1) goud extra uit
  de vijand. Een keer per reeks, hoe lang hij ook wordt (keuze van de opdrachtgever).
- Is de reeks voorbij, dan telt `mkillAfsluit` hem bij zijn grootte (`dubbel`, `triple`, `multi` vanaf 4) en bij de
  langste reeks. `winLevel` sluit een lopende reeks ook af voor het rapport.

## Wat je ziet en hoort

Gekozen uit vijf schetsen (C: het snoer kralen), met de Engelse woorden (regel 5).

- **Het snoer**: `#mkill` midden boven, op 104 px, net onder de toetsenhint (`#hint`, die kan twee regels zijn). Vier
  kralen (`MKILL.kralen`); vanaf de tweede kill gaan er zoveel aan als de reeks lang is, de nieuwste springt op (`pop`).
  Loopt de reeks af, dan knapt het snoer (`knap`, `MKILL.knap` s) en verdwijnt het.
- **Het woord**: DOUBLE KILL, TRIPLE KILL, MULTI KILL (`MKILL.woorden`), groter per stap (`n2`, `n3`, `n4`), met
  een munt en +1 bij de bonus. Het springt erin, blijft even en zakt weg (`mkwoord`, 1,5 s).
- **De stinger**: `sounds/multikill2.mp3`, `multikill3.mp3` en `multikill4.mp3` (ElevenLabs Sound Effects:
  djembe, war drum, speerklank en munten). Lui geladen (`mkillLaad`, via `laadLevel` of de sandboxknop).
  Geknipt met ffmpeg, staart eraf (fade na 1,1 tot 1,3 s), onder 35 Hz weg, en oplopend in luidheid: -18,8, -17,7
  en -16,0 LUFS. Stuk 2 en 4 komen uit het eerste bestand (stuk 1 en 3), stuk 3 uit een tweede generatie met twee
  klappen, 4,5 dB zachter gezet zodat hij tussen de andere twee in zit.
- **De tink**: de goudtink (`goudTink(hoger)`) gaat per kill in de reeks omhoog: grondtoon, kleine terts, kwart, kwint
  (`MKILL.tink`). `goudVlieg` geeft de toon mee aan het vliegende goudstuk.

## Het levelrapport

Met `rapport: true` komt er in het winscherm (`#win`) een paneel tussen de naam en de knoppen (`#rapport`), en de kop
wordt "Level complete". Het telt (`mkStat`, op nul in `mkillReset`, na `goudReset` in `restart`):
Enemies defeated, Multikills met daaronder Double, Triple en Multi, Longest streak, Time (spel-tijd, zonder pauze) en
in een level met goud Gold earned (het goud nu min het goud bij het begin, dus ook kisten en kopgeld).
De knoppen eronder zijn nog de oude Nederlandse (regel 5: bestaande teksten blijven tot er om een vertaling gevraagd wordt).
Op een lage telefoon (`max-height: 500px`) wordt het winscherm compacter, zodat Hoofdmenu er nog op past.
Gekozen uit vijf schetsen: 1, de scorekaart.

## Test 70: Multikill

Vlakke savanne (`tafelbergen`) met goud en zes groepjes dicht op elkaar: twee slangen, drie hyena's, slang met
schorpioen en zwarte slang, twee bandieten (elk drie levens, dus een Double is werk), twee hyena's met een slang, en
vier slangen op een rij voor een Multi Kill. Twee kalebassen. De speelrobot speelt het uit zonder consolefouten.
