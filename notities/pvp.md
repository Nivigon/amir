# PvP: een tegen een over internet

`PVP`, `PVP_LEVEL`, `pvpHost`, `pvpJoin`, `pvpVerbonden`, `pvpStap`, `pvpVang`, `pvpTeken`, `pvpRondeUit`, `pvpStop`

De knop **PvP** in het hoofdmenu (`btnpvp`, het scherm `menuPvp`). De een drukt op **Host a duel** en krijgt een code van
vier letters, de ander tikt die in en drukt op **Join**. Daarna spelen ze allebei het stadje `PVP_LEVEL`.

## De verbinding

- WebRTC met PeerJS (`PVP.lib`, van jsdelivr, pas geladen bij Host of Join met `pvpLib`, zodat het menu er niet op wacht).
  De openbare PeerJS-server koppelt de twee een keer: de host heet daar `PVP.pre` plus de code. Daarna gaan de berichten
  rechtstreeks. Geen eigen server, geen account. Thuis werkt dat bijna altijd; achter een strenge router kan het mislukken
  (dan zie je een foutmelding), en dan is een TURN-server of een eigen doorgeefluik de volgende stap.
- De service worker laat andere hosts met rust (`sw.js`, `url.origin`), dus de bibliotheek komt altijd van internet. Offline
  is er geen PvP.
- Deze sandbox (de cloud waar Claude in werkt) mag PeerJS niet bereiken; daar is het getest met een nagebootste `Peer` die
  de berichten tussen twee browservensters doorgeeft.

## Wat er over de lijn gaat

- `s`, 20 keer per seconde (`PVP.hz`): plek (`x`, `h`), kijkrichting, het plaatje waarmee Amir net getekend is
  (`pvpVang`, vlak voor de `drawImage` van zijn lijf: het pad van het plaatje en de rechthoek in sprite-eenheden vanaf zijn
  voeten, en of het gespiegeld is), `hurt` (de rode flits), de steek (`sf` het frame, `sl` of hij raakt, `sn` een teller
  per steek), de lage zwaai (`sw`, `wn`), de geworpen speer (`j`, met een teller `n` per worp) en de levens.
- `au` (ik ben geraakt), `speerRaak` (jouw speer zit in mij: die valt dan neer), `ko` (ik ben dood), `ronde` (de host
  start een ronde of meldt het einde), `rematch`, `bye`.

## Wie beslist

De laptop van wie geraakt wordt. `pvpTeken` (in het tekenblok, na `hitBy` en `pbox`, voor de slangen) tekent de andere Amir
en kijkt of zijn steek (de punt uit `TIP_DX`/`TIP_Y`, net als bij een vijand), zijn lage zwaai (`SWEEP_REACH`,
`SWEEP_HIGH`) of zijn speer de eigen `pbox` raakt, en roept dan gewoon `hurtPlayer`. Zo telt de rol (onkwetsbaar via
`invuln`) vanzelf mee. Voor de speer telt het hele stuk sinds het vorige bericht, anders vloog een snelle speer tussen
twee berichten door hem heen. Elke steek, zwaai en worp raakt een keer (`raakSteek`, `raakZwaai`, `raakSpeer`).

De andere Amir schuift naar zijn doorgestuurde plek (`PVP.volg`); springt hij meer dan 500 (een nieuwe ronde), dan staat
hij er meteen. Boven zijn hoofd een rood pijltje en zijn drie levens.

## Rondes

Best of 3 (`PVP.winst`), elke ronde 3 levens. Wie doodgaat stuurt `ko`; de host telt de stand, wacht `PVP.pauze` en
start de volgende ronde (`restart`, dan `pvpPlaats`: de host rechts op `-250`, de gast links op `-2550`). Tussen twee
rondes is iedereen onkwetsbaar (`godMode`). Na het duel vraagt R een rematch; die begint pas als allebei R drukten
(`opnieuw` stuurt in PvP naar `pvpRematchDruk`). Het dood-scherm komt in PvP niet.

## De kit

Basis plus de rol: lopen, sprinten, springen, bukken, steken, lage zwaai, werpen (een speer in de hand, een op de rug) en
de rol. Geen talents (`runReset`, en `levelList` is `PVP_LEVELS`, niet `TEST_LEVELS`, want die geeft alle talents en een
vierde leven), geen draaislag (`combo: false`). De rol heeft in PvP een afkoeling van 1,2 s in plaats van 0,5 (`PVP.rolKoel`,
in `pvpVerbonden` gezet en in `pvpStop` teruggezet), zodat je niet elke worp wegrolt.

## Het stadje (`PVP_LEVEL`)

Drie huizen: twee lage (twee hoog) aan de kanten en een hoog koopmanshuis in het midden, steegjes van 1,4 Amir. Een
galerij op 401 loopt over alle drie. Een rieten kraam aan elke kant: van het dak (264) spring je op de galerij. In de
steegjes een stadstrap (E) van de galerij naar een balkon op 730 aan de buitenkant van de lage huizen, en van daar het
dak op (771). Het hoge middenhuis heeft geen weg omhoog. Een ton met een kalebas in het midden van de straat. Nagemeten:
beide kramen naar de galerij en beide trappen. `geenEinde`: het duel eindigt op de rondes, niet bij fakkels.

## Wat nog kan

- De andere Amir heeft dezelfde kleuren als jij; alleen het pijltje maakt het verschil.
- Zijn speren op de rug, de schaduw en het licht op hem worden niet getekend.
- Een TURN-server als vangnet als de verbinding niet lukt.
