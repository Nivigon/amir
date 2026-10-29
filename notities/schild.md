# Het schild van Amir

`AMIR_SCHILD`, `amirSchild`, `SCHILD_AAN`, `schildStap`, `schildVang`, `schildTeken`, `schildBouw`, `krbPijlTerug`,
`schbWankel`. De sectie heet "het schild van Amir: omhoog houden, vangen en pareren" en staat vlak voor "het projectiel".
Niet te verwarren met `SCHILD` (de kapotte schilden in de wind, decor) en `sbSchild` (de decorknop in de sandbox).

## Wat het is

Een nepschild, in code getekend, geen plaatje: een Zulu-schild (isihlangu) van koeienhuid. Een spits ovaal in room met
zwarte en roodbruine vlekken en korte haarstreepjes, een houten stok door het midden met een plukje zwart haar bovenop,
een rij huidrepen die om en om licht en donker over de stok gevlochten zijn, en een donkere zoom. `schildBouw` tekent
het een keer op een eigen doekje (200 bij 560, een vaste reeks toevalsgetallen, dus elk potje hetzelfde schild), plus
een donker silhouet voor de dikte. `schildTeken` zet het bij Amir, twee keer per beeld: voor Amir (omlaag: aan zijn arm,
smal, schuin, achter zijn lijf) en na Amir (op: voor zijn borst, breder, de huid naar voren). De stand `op` (0 tot 1)
kiest welke van de twee tekent en schuift de plek, de hoek en de breedte. Komt er een echt plaatje, dan vervangt dat
alleen `schildBouw`; de rest blijft.

## Hoe het voelt (de afspraken)

- **Snel**: in 0,08 s op (`op`), 0,07 s neer (`neer`). Een stoot, worp of lage zwaai laat het meteen zakken, en wie C
  blijft vasthouden staat daarna vanzelf weer achter zijn schild. Vasthouden, tikken op de stoot, en weer dekken.
- **Een keuze**: met het schild op loop je op 0,42 van je tempo (`tempo`), zonder sprint; bukken en springen gaan niet
  (springen laat het zakken, gebukt komt het niet op). Omdraaien mag, maar dan zwaait het mee en dekt het 0,12 s niet (`draai`).
- **Alleen van voren**: alles wat van de kant komt waar Amir naar kijkt wordt gevangen, de rest is raak. In de duo-arena
  sta je dus altijd met je rug naar een van de twee.
- **De parade**: til je het op binnen 0,2 s voor de klap (`pareer`), en was het daarvoor minstens 0,3 s omlaag
  (`pareerRust`, rammelen helpt niet), dan is het een parade: staalklank (`banClang`), vonken (`banVonk`), een witte gloed
  en een langere hitstop. Een parade per keer optillen.

| klap | gevangen | parade |
|---|---|---|
| bout van de kruisboog | blijft in de huid steken (max 5, 7 s, trilt na), Amir schuift een stukje | kaatst terug langs zijn eigen baan (`b.terug`); raakt de schutter (`krbPijlTerug`, `hitKruisboog(s, 'pijl')`) of de schildman die ertussen staat (`vv`, de friendly fire) |
| speer van de schildbandiet | Amir schuift flink terug (560 px/s), de bouten in het schild breken eruit | Amir staat pal; de schildman wankelt een stapje terug (`schbWankel`, zijn flinch maal `wankel`) en staat `open` (0,9 s) zonder dekking: zijn dekking vanaf `dekVan` telt dan niet |
| elke andere klap (`hurtPlayer`) | ketst af, Amir schuift terug; dezelfde klap een beeld later wordt stil gevangen (`klapRust`) | idem, met de staalklank |

Gevangen kost niets en zet geen `invuln`: een tweede bout vlak na de eerste wordt gewoon ook gevangen. De duw loopt via
`knock`, dus nooit over een kei of ravijn.

## De haakjes

- de loop: `schildStap(dt, bezig)` na `if (attacking || throwing) dir = 0;`, `schildTempo()` in de loopsnelheid en de
  looppas, `schildOp()` in `loopFactor` (geen sprint) en `canDuck`.
- de bouten (de sectie "de bouten van de kruisboog" in het tekenen): eerst het schild (het raakvak `amirSchild.vak` of
  `pbox`, als de bout van voren komt), dan pas Amir. In `krbPijlUpdate` de teruggekaatste bout tegen de schutters.
- de schildbandiet: in de hit-frames van zijn strike eerst `schildVang(.., 'speer')`; `s.open` telt af in
  `updateSchildman` en schakelt de dekking in `hitSchildman` uit.
- `hurtPlayer`: meteen na de eerste regel `schildVang(fromLeft, 'klap')`.
- het level: `schild: true` (in `readLevel` doorgegeven), gezet in `restart` (`SCHILD_AAN`); in de sandbox de knop.

## Besturing en knoppen

- laptop: **C** vasthouden (de letter was vrij). Op een telefoon de schildknop (`TOUCH_BTNS`, id `schild`, met het
  schild zelf als icoon, `drawBtnSchild`), alleen zichtbaar als Amir een schild heeft; vasthouden zet `keys['c']`.
- sandbox: Speer en spullen, **Schild** (`sbschildamir`, `sbAmirSchild`), ook in de wizard van de arena-modus.
- level: **Test 56: Het schild**, de duo-arena van Test 55 met `schild: true`. Aan het begin een instelscherm (`duoKeuze`,
  `duoArena.keuze`): de lading van de kruisboogbandiet (`KRB_SALVO`: 2 en daarna 1, altijd 2, altijd 1; met een tweede
  bout schiet hij na `KRB.salvoNa` en `KRB.salvoSlot`, zo'n 0,47 s na het eerste schot) en makkelijk of moeilijk voor de
  schildbandiet. In de pauze **Arena instellen** (`pzduo`).

## Gemeten

Met Playwright in de sandbox: vier bouten van voren gevangen zonder treffer, een parade die de schutter doodde, en
tegen de schildbandiet (makkelijk) een parade waarna een directe steek zijn schild van 3 naar 2 bracht. Met `wankel` 1,3
schoof hij na de parade 345 px weg, buiten het bereik van de steek (zo'n 230 px); daarom 0,45 en staat Amir zelf pal.
