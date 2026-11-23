# Het aanvalsticket

`TICKET`, `tkStand`, `ticketAan`, `ticketCfg`, `ticketMag`, `ticketWacht`, `ticketSchuifel`, `ticketStap`, `ticketLos`,
`ticketTeken`, `banTicketWacht`. De sectie in de HTML heet `// ---- het aanvalsticket ----` (na de scheiding, zie
`notities/scheiden.md`).

Zoals in de Arkham-spellen, God of War en Doom: niet iedereen die bij Amir staat valt tegelijk aan. Het loste op dat
schildbandieten binnen springafstand vrij sprongen, soms twee tegelijk, en dan allebei op de speerpunt landden.

## Hoe het werkt

- **Tickets per kant.** `TICKET.voor` aan de kant waar Amir heen kijkt (`facing`), `TICKET.achter` erachter, en
  `TICKET.afstand` voor een aanval op afstand (de dolkworp; later de kruisboog). Alleen wie een ticket heeft zet zijn
  aanval in. `ticketKant` kijkt bij het pakken; draait Amir om, dan houdt wie al een ticket heeft het zijne.
- **Het ticket gaat mee met de tell**, niet met het aanlopen: `ticketMag` wordt gevraagd op het moment dat de aanval
  zou beginnen (de slag van de bandiet, de strike van de schildbandiet, de dolkworp). Het komt terug als de aanval en
  het herstel voorbij zijn (`ticketBezig`: bandiet `slag`, `worp` of `rust`; schildbandiet `strike`, met het herstel
  erin), plus `TICKET.pauze` (0,5 s) voor die plek weer open is (`tkStand.pauze`). Een ticket is voor een aanval: wie
  het nog heeft maar klaar is, geeft het eerst terug (`ticketLos`), ook als hij zijn volgende slag in hetzelfde beeld
  vraagt. `tkBeeld` houdt bij in welk beeld hij het kreeg (de bandiet vraagt het twee keer in een beeld).
- **Om de beurt.** `ticketStap` geeft per kant zoveel wachters voorrang (`tkVoorrang`) als er plekken vrij zijn: wie het
  langst in beeld wacht (`tkWachtT`), bij gelijk de dichtstbijzijnde. Een vrije plek gaat alleen naar wie voorrang heeft.
  Zonder die volgorde sprong steeds dezelfde (de voorste). Wie voorrang heeft loopt langs de wachters heen
  (`ticketDoorloop`, houding 2 in `scheidMobs`): op een lijn duwde hij anders de wachter voor hem Amir in.
- **Wachten.** Wie geen ticket en geen voorrang heeft blijft op `TICKET.rand` (1,2) keer zijn eigen bereik staan en
  schuifelt daar heen en weer (`TICKET.zwaai`, `schuifelV`, ieder zijn eigen ritme). De bandiet in zijn loopgang (`walk`,
  achteruit speelt hij die terug) of zijn idle (`banTicketWacht`, `tkSchuifel`), de schildbandiet in zijn loop met het
  schild op, op het tempo van zijn stap. Eenmaal wachtend is de rand ruimer (1,5 keer), anders flitst hij tussen rennen en schuifelen. Na zijn eigen
  aanval stapt hij sneller terug (`TICKET.terug`, `terugV`) zolang hij nog binnen zijn bereik staat.
- **Geen gratis plek.** Staat Amir langer dan `TICKET.wacht` (0,8 s) binnen het bereik van een wachter (`tkBinnen`), dan
  slaat die toch, zonder ticket (`tkGratis`, een rood ruitje). Niet terwijl een maat aan die kant nog in zijn aanval zit
  (`ticketKantBezig`), anders landden ze weer op elkaar. De tijd na zijn eigen aanval (het terugstappen) telt niet.
- **In beeld.** Wie niet in beeld is (`ticketInBeeld`, de halve schermbreedte om `kijkMidden`) krijgt geen ticket en geen
  voorrang.

Doet mee: de bandiet (ook de dolkman) en de schildbandiet. Erbuiten: hyena's (eigen beurten), slangen, schorpioen,
bazen, en voorlopig de kooiman, zweepman en kruisboog. Ook buiten het ticket om: de parade-tegenklap van de bandiet
(een reactie), de hinderlaag (`hurk`, een regie), de vault en de galerijsprong (bewegen, geen aanval) en de razernij van
een aanvoerder. In Co-op en Duel staat het uit (twee doelen).

## Instellen

- `TICKET` bovenaan de sectie: alle getallen. `TICKET.standaard` (nu `false`) zet het in elk level aan zonder levelvlag.
- Een level: `tickets: true` zet het aan, `tickets: false` uit, en `tickets: {voor: 2, pauze: 1, ...}` aan met eigen
  getallen (ook `achter`, `afstand`, `gratis`, `wacht`, `rand`, `toon`; `Infinity` is onbeperkt).
- `ticketKeuze: true`: aan het begin en na R het keuzescherm (in `duoKeuze`): tickets aan of uit, per kant 1, 2 of
  onbeperkt, de pauze 0, 0,5 of 1 s, de geen-gratis-plek-regel, de scheiding (`scheidMobs` slaat dan over) en de ruitjes.
  In de pauze onder **Attack tickets: settings**.
- Sandbox: onder Vijanden, rij Tickets, **Attack tickets** (`sbTicketAan`). Met de standaardgetallen en altijd de
  ruitjes. Samen met de Groepen erboven.
- `ticketTeken` (in `vijandHpBalk`): een gouden ruitje boven wie een ticket voor of achter heeft, blauw voor afstand,
  rood voor een aanval zonder ticket.

## Test 95: Attack tickets

Op verzoek, zelf ontworpen. Vlakke savanne (geen keien of ravijnen, zodat alleen de groep telt), de standaardvelden van
een nieuw level en `ticketKeuze`. Vier groepen met kalebassen ertussen:

1. Drie schildbandieten tegelijk op dezelfde plek (twee makkelijk, een moeilijk): het oude probleem.
2. Een mix: twee bandieten (een met dolk, voor het afstandsticket) en twee schildbandieten, kort na elkaar (`achter`).
3. Van twee kanten: voor je een schildbandiet en een bandiet, en een zegel dat de poort achter je opent (`poort:
   'achter'`, met hek), waar er nog een bandiet en een schildbandiet uitkomen.
4. De grote groep: drie bandieten (een met dolk) en twee schildbandieten.

## Gemeten

Met een proefscript (Amir staat stil, levens vast op 3; niet in `tools/`) op 1280 bij 720, 50 s:

| groep | tickets uit | tickets aan |
| --- | --- | --- |
| drie schildbandieten | 11 sprongen, tot 3 tegelijk, 86 beelden met twee in de lucht | 8 tot 11 sprongen, om de beurt, 0 beelden met twee in de lucht |
| de mix | 29 aanvallen, tot 4 tegelijk, 59 beelden met twee in de lucht | 13 aanvallen, hooguit 2 tegelijk (de ticket en een gratis) |

Staat Amir stil, dan duwt de landing van de ticketvijand soms een wachter binnen zijn bereik, en slaat die na 0,8 s toch:
dat is de geen-gratis-plek-regel, nu pas als de ander geland is.

## Open

- De kooiman, zweepman en kruisboog (de kruisboog op het afstandsticket).
- Op een lijn kan een wachter niet om Amir heen; Arkham laat ze cirkelen. Hier schuifelen ze heen en weer op hun plek.
