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

## Hutten
`design/savanne/hutten/`: Grok eebf2583 (hut_rond) en 2fa55f54 (de twee koepels). Zie de projectnotitie
savanne_hutten_2d.md.
