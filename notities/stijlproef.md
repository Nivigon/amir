# Stijlproef (Test 97)

Waar je elk nieuw omgevingsasset naast de stad en Amir zet voordat het het spel in mag. Hoort bij de stijlsheet
(claude.ai artifact "Amir stijlsheet": regels, palet, goed/fout, per landschap).

## Het level
- `TEST_97`: de rand van Ishmul (wit zand, daglicht) op dezelfde wereld-x als de linkeroever van Ishmul: een huis van twee,
  het hoge huis van drie, dan savanne met de goedgekeurde hutten (`hut_rond`, `hut_koepel_groot`, `hut_koepel_hoog`) en
  de rots. Amir begint bij -2900, vredig.
- De rijen huizen in de verte lopen hier door tot boven de hutten (in Ishmul niet); nog niet uitgezocht waarom
  (`stadAchterRanden`, met andere achterTot en een derde gevel bleef het zo). Voor de proef niet erg.

## Het paneel (STIJLPROEF)
Alleen in een level met `stijlproef: true` (via `readLevel`). `stijlproefZet` uit `setLevel`.
- **Bestand**: een PNG (transparant, recht van voren). Komt als `PROPS.proef` op 300 links van Amir te staan.
- **Zet bij Amir**, **Spiegel**, **Weg**.
- **Hoogte in Amir**: `PROPS.proef.h`, live. Een deur hoort ongeveer 1,2 Amir te zijn.
- **Kleur** (tint in graden), **Verzadiging**, **Licht**: het plaatje wordt per pixel omgekleurd (geen `ctx.filter`, zie
  "de tint van een level") en als gewone Image in `propImg.proef` gezet. Zo zie je of een asset in een andere kleurstreek
  nog in dezelfde wereld past.
- Niets wordt opgeslagen. Een goedgekeurd asset krijgt daarna een eigen regel in `PROPS` en een plek in `design/`.

## De check (uit de stijlsheet)
Recht van voren; even rustige vlakken als de stadsmuur; kleur binnen de familie; schaal klopt met Amir; geen lijnen die
de stad niet heeft; en niet te veel lijken op een ander landschap.

## Hutten en putten
`design/savanne/hutten/`: Grok eebf2583 (hut_rond) en 2fa55f54 (de twee koepels). Zie de projectnotitie
savanne_hutten_2d.md.

Putten: `design/savanne/putten/` (put_leem, put_steen, put_shaduf), Grok 2b165ff8. Ze staan in Test 97 na de hutten.
In de sandbox onder Decor, rij **Savannedorp**: een knop per hut en put (`data-sdorp`).

## De loopput (LOOPPUT)
Een lage, brede leemput met een rond houten deksel, om op te staan en overheen te springen: `design/savanne/putten/put_loop.png`,
Grok 4c665996 (een edit van put_leem met de galerij als referentie voor de kijkhoek). Het bovenvlak is van schuin boven te zien,
zodat Amir erin staat en niet op een streep. Het frame (twee palen, de balk met het touw, Grok fee91518) staat op de
achterrand en de emmer op de grond: de hele plaat ligt achter de personages, dus Amir en zijn speer staan altijd voor het hout.
De palen zijn bij het knippen 230 px verlengd (een strook herhaald), zodat de balk boven Amirs hoofd uitkomt.

- Level: `loopPutten: [{x, s, f}]`, `x` het midden, `s` de grootte, `f` spiegelen. Bij `s` 1 ligt de looplijn 160 boven de grond
  (de sprong haalt 208) en is hij ruim 1,7 Amir breed (`LOOPPUT.k`).
- Botsing zoals bij de kruipstam: readLevel zet er een onzichtbare zwevende laag op (`loopputDak`, look `geen`, `onder: 0`).
  Amir loopt er tegenaan, springt erop en loopt er aan beide kanten af. Vijanden houdt hij tegen als een kei (regel 7): een
  slang bleef aan de linkerkant staan, een hyena aan de rechterkant.
- Getekend in `drawClimb` na de kruipstam, dus achter de personages (`loopputTeken`).
- Nagekeken met Playwright: tegen de muur, de sprong, staan, de steek en de worp bovenop, eraf lopen. De voeten staan in het
  vlak, ook in de brede steekhouding.
- In Test 97 na de drie putten (x -7150). In de sandbox in de rij **Savannedorp**: **Loopput** (elke klik een verder) en **Weg**.
