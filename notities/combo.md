# De derde slag (COMBO)

Drie steken kort na elkaar: de derde is geen steek maar een draaislag. Amir draait op de plek (even met zijn rug naar
de camera), de speer gaat in een cirkel over zijn hoofd en slaat voor hem neer tot op de grond, en hij eindigt laag
met de speer in een hand achter zich en de vrije hand naar voren. Een beloning voor ritme: hij telt dubbel en geeft
een flits op de treffer.

Aan met `combo: true` in een level (alleen Test 68) of de knop **Combo** in de sandbox (bij Stof). Grep: `COMBO`,
`comboStart`, `comboStap`, `comboKan`, `atkCombo`, `comboSoort`, `comboTerugNu`.

## Twee soorten: terugslag of schade

Welke derde slag beter is (controle of schade) proberen we uit. `comboSoort()` geeft er een:

- **Terugslag**: de slag telt enkel, maar zet de vijand ver terug. Een bandiet krijgt `COMBO.terug.v` (1500 px/s, dooft uit
  tot zo'n 380 px) in plaats van `BAN_KNOCK`, staat `COMBO.terug.rust` (1,2 s) stil en komt dan in `COMBO.terug.traag`
  (1,2 s) op gang, van `traagV` (0,4) van zijn tempo terug naar vol (`s.traag`, in de run van `updateBandiet`); een
  schildbandiet krijgt `COMBO.terug.schb` (3) keer zijn flinch-duw en staat na de flinch `schbRust` (1 s) in zijn wacht
  (`s.naTerug`, `s.stil`). Kei en ravijn houden hem tegen (regel 7, via `banMove` en `schbMove`). Op de treffer een
  stofwolk in plaats van de ster van de crit, en een doffe houtklap (`houtRaak` op `COMBO.terug.toon`, 0,75): de schacht
  op zijn lijf. Later misschien met de speer omgedraaid (zie de bijlage in `notities/kit-verbeteren.md`).
- **Schade**: de slag telt dubbel (`critNu`), met de ster, zoals hij eerst was.
- **Doorbraak**: telt dubbel zoals Schade, en lost de parade van de bandiet op (optie A). Pareert hij de tweede steek
  van een reeks, dan volgt de derde slag zonder afkoeling: al gedrukt (`comboBuf`) en hij start meteen, anders is de
  afkoeling weg en start de volgende druk hem (in de pareer-tak, `comboDoor`). Tot en met frame `COMBO.pantserTot` (9, de
  draai en de slag) raakt geen klap Amir (`comboPantser` in `hurtPlayer`), zodat zijn tegenklap (die na zo'n 0,07 s landt,
  tegen 0,43 s voor de slag met afkoeling) de reeks niet meer breekt.

Test 68 heeft `comboKeuze: true`: aan het begin en na elke R (`opnieuw`) staat het scherm van `duoKeuze` open met alleen
de rij Derde slag (terugslag, schade of doorbraak) (`dkcombo`, bewaard in `amir.duoKeuze`). Een level met `combo` zonder `comboKeuze` krijgt schade. In de
sandbox wisselt de knop Combo rond: uit, terugslag, schade, doorbraak (`sbComboSoort`). De terugslag werkt nu op de bandiet en de
schildbandiet (de vijanden van Test 68); bij andere vijanden telt hij gewoon als een treffer.

## Zo telt hij

- Elke steek met de speer telt mee (`comboTel` in `startAttack`). Begint een steek binnen `COMBO.keten` (0,45 s) na
  het eind van de vorige, dan hoort hij bij dezelfde reeks; anders begint de reeks opnieuw.
- Een druk tijdens een steek (vanaf `COMBO.buf`, frame 3) of in de afkoeling wordt onthouden (`comboBuf`): na de
  eerste steek komt de tweede dan meteen, zonder afkoeling.
- Is er tijdens de tweede steek al gedrukt, dan takt die op `COMBO.aftak` (frame 8, de uitgestoken speer) af naar de
  derde slag. De clip begint precies in die pose. Komt de derde druk pas na de tweede steek, dan start de slag vanaf
  frame 0.
- Alleen contact telt: een steek die niets raakt (`swingUsed` blijft uit) zet `comboTel` op nul aan het eind van de
  steek, en de tweede steek takt pas af naar de derde slag als hij al raak was. Een gepareerde steek telt wel
  (`comboSinds = 0` in de pareer-tak). Zo kun je niet eerst een keer in de lucht prikken om de derde slag klaar te
  zetten: tegen de bandiet is het raak, parade, en dan breekt de derde slag door zijn dekking.
- Een treffer op Amir breekt de reeks af (net als de steek zelf). Het mes doet niet mee.

## De slag

- 15 frames op eigen ticks (1/24 s): draai 0,25 s, slag, doorhalen, eindpose; in totaal 0,75 s.
- Raak op frame 6 tot 9 (`COMBO.actief`): de punt komt van borsthoogte voor hem naar de grond (`COMBO.punt`, canvas-px).
  De straal om de punt is `COMBO.reik` (60, de steek 40).
- Onder het draaien schuift hij `COMBO.stap` (110 sprite-eenheden) naar voren, verdeeld over frame 0 tot 5
  (`comboSchuif`, niet over een ravijn), zodat hij een vijand haalt die na twee steken iets is teruggestuiterd.
- Bij schade telt de treffer dubbel via `critNu` (dezelfde weg als True Flight: elke `hitX` met `critPak` haalt er een treffer
  extra uit). De eerste treffer geeft de witgouden ster van de crit op de speerpunt (`comboTreffer`), een hitstop
  (`COMBO.stop`) en een schok.
- De bandiet: de slag gaat door zijn dekking heen (`s.inv`), hij pareert hem niet (`hitBandiet`, en de pareer-tak).

## Frames

`karakters/amir/aanval/combo/combo_00..14.png`, canvas 534 x 440, grondlijn 420, anker (lijfmidden) 174, kijkt naar
links. Uit een Grok-clip (try2a) met als begin steekframe 8 (3x opgeschaald, de speer korter gemaakt) en als eind een
eigen pose; de clip staat op de schaal van de steek (`COMBO.schaal` 1,0025). Gekozen clipframes: 25, 31, 37, 43, 49,
55, 59, 61, 63, 81, 85, 87, 99, 103, 105. Gekeyd met de smalle ramp (0,92 / 0,62), spikkels onder 150 px weg; magenta
in de bewogen schacht terug naar bruin, in de punt naar grijs. Op frame 6 en 8 is de speerpunt nog wat paars.

## Open

- Tegen de bandiet: de tweede steek valt in zijn dekking en wordt gepareerd; dat telt als contact, maar met terugslag en
  schade breekt zijn counter de reeks bijna altijd af. Doorbraak is het antwoord daarop; uitproberen welke blijft.
- Het naar voren schuiven gebeurt terwijl de voeten in de frames staan: een beetje glijden.
