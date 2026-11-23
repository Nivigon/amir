# Vijanden uit elkaar houden

Staan er een paar vijanden van dezelfde soort op dezelfde plek, dan zie je er maar een. `scheidMobs` geeft ze elk
beeld een zacht duwtje uit elkaar, via hun eigen move (dus nooit over een kei, ravijn of wand, regel 7), met een
easing (`MOB_SCHEID_K`). Alleen wie op dezelfde vloer staat (`MOB_SCHEID_HOOG`) en alleen binnen een soort.

| soort | afstand | houding |
| --- | --- | --- |
| bandiet | `BAN_SCHEID` (290 canvas-px, ongeveer 1,0 Amir) | `banScheidHouding` |
| kooiman | `KOOI_SCHEID` (380 canvas-px, ongeveer 1,1 Amir) | `kooiScheidHouding` |
| schildbandiet | `SCHB_SCHEID` 0,9 Amir | `schbScheidHouding` |
| hyena | `HY_SCHEID` 0,8 Amir | `hyScheidHouding` |
| zandslang (`kind: 'groen'`) | `SLANG_SCHEID` 0,75 Amir | `slangScheidHouding`, move `slangScheidMove` |

De houding zegt per vijand: 0 gewoon (allebei de helft van de duw), 1 in zijn aanval (hij schuift niet, de ander krijgt
de hele duw), 2 uitgeschakeld of geregisseerd (geen scheiding, de ander loopt langs hem heen).

## Waarom de houding nodig is

Uitgezocht per soort voor de uitbreiding (november 2026):

- **Schildbandiet**: in de sprong (`strike` vanaf `SCHB.leapVan`, en `vault`) zet de engine zijn x elk beeld op de baan
  van `leapVan` naar `leapDoel`; de landing ligt al vast in `schbMik` (de speerpunt van Amir, hooguit `SCHB.sprongMax`).
  Een duw werd daar overschreven (haperen) of verschoof in de tell zijn afzet. Er is geen minimale afstand voor de
  inzet (`SCHB.aanval` 2,1 Amir), dus een duw naar voren kan de sprong niet onmogelijk maken. `flinch` en `stil` staan
  ook vast; `exe`, blind en stun doen niet mee.
- **Kooiman**: de klapzone van de smash rekent vanaf `s.x` (`KOOI_SMASH.near/far`); voor deze uitbreiding werd hij ook
  tijdens de smash geduwd. Nu is alleen `drag` en `duw` los. Het duel met de vogel en de freeze (`kooiVries`) staan in
  hun regie.
- **Hyena**: de uitval gaat een richting op (`s.dir`), geen afstand, dus een duw is daar onschuldig; `telegraaf` en
  `storm` staan toch vast. De roedel van Murghtaan heeft zijn eigen trapjes (`gapPlus`, `murcRoedelRij`) en doet niet mee,
  net als een hyena die wegrent of nog buiten beeld wacht.
- **Zandslang**: wie wacht en weer buiten `snakeStopGap + 18` geduwd werd, ging weer kruipen; `wait` en `bite` staan
  daarom vast. Patrouille, blind en sterven doen niet mee.

## Bewust erbuiten

- De spuwers (zwarte slang, knockslang) houden zelf afstand, de fosforslangen hebben hun eigen spreiding (`FOSFOR.achter`).
- De zweepman heeft een eigen houd-afstand (hij sluipt achteruit) en een gescripte fase 2 (`ZWM2`); een duw gaf gebibber.
- De kruisboogbandiet houdt zelf afstand (`KRB.dichtbij`, `KRB.afstand`) en in `slot` ligt zijn schietrichting vast.
- Schorpioen en goudaapje hebben geen move met botsing en komen zelden met veel tegelijk.
- Tussen soorten (een bandiet en een schildbandiet) scheidt het nog niet: `scheidMobs` heeft een afstand en een move per
  lijst. Dat is stap 2: een afstand per paar (de halve breedtes samen) en elke vijand met zijn eigen move.

Wat er overblijft (een maat die tegen de duw in loopt, rent of kruipt dan op zijn plek) is hetzelfde als bij de bandiet.

## Sandbox

Onder Vijanden, **Groepen**: 4 bandieten, 3 schildbandieten, 3 kooimannen, 3 hyena's of 4 zandslangen op precies
dezelfde plek (`SB_GROEP_N`). **Uit elkaar** zet `mobScheidAan` aan en uit, voor alle soorten, om het verschil te zien.
