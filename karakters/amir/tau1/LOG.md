# Tau niveau 1 (jonge leeuw), nachtrun 22-11-2026

Plan: `claude/tau1_productieplan.md` (project). Gereedschap: `tools/tau1/` (tau.py, stokweg.py, plus raster.py,
uitlijn.py en speer_meet.py overgenomen uit `tools/mkuki/` van branch `claude/mkuki`). Werkmap tijdens de run:
`/home/claude/werk/` (niet in de repo).

## Welke frames het spel tekent (nagekeken in de HTML)
- Staan: `stokken/staan/staan_00.png` (stokBeeld, STOK.sets.staan = 1), stokken erin gebakken.
- Rennen: `stokken/rennen/rennen_00..11.png` (12), stokken erin gebakken. De ren is samengesteld (geen lijf-bron in de
  repo), dus de stokken haal ik eruit met het masker van `tools/stok_variant.py` (stokhoeken.json).
- Springen: `beweging/jump/jump/amirjump0staand..6landing.png` (7). In de sprong tekent het spel GEEN stokken (useJump
  gaat voor stokBeeld), dus deze frames zijn zonder stokken.
- Rollen: `beweging/rol/zonder/rol_1..28.png`. Ook zonder stokken (useRol gaat voor).

## Uitvoer
- `stokken/staan/staan_00.png`, `stokken/rennen/rennen_NN.png`: spelbeeld (Tau-kleuren) met de originele stokken er
  weer in, zelfde canvas als het spel (511x384). Daarnaast `_zones.png`, en in `lijf/` het lijf zonder stokken
  (Tau-kleuren, `_zones`, `_hulp`), zodat de stokken later opnieuw gebakken of vervangen kunnen worden.
- `beweging/jump/jump/*.png` en `beweging/rol/zonder/rol_N.png`: spelbeeld, `_zones`, `_hulp`.
- Zonekaart: vacht/kap (0,255,0), broek (0,0,255), krassen (255,255,0), tanden (255,255,255), ogen (255,128,0),
  de rest zwart. Omkleuren: doelkleur x V/Vref per zone (`tau.py kleur`, paletten TAU, WIT, ZWART).

## Hulpkleuren
Kap + vacht groen #00C040, broek blauw #2050FF, krassen geel #FFE000. Tanden blijven wit, ogen amber.
Referentie in hulpkleuren: Grok-bewerking van post 3e331009 -> `0ba1c513-842d-4d45-b651-2ab0ca4ede36`
(`bron/ref_hulp.png`, met de stokken; op 0,42 opgehaald). Origineel: `bron/ref_tau1.png`.
Tau-kleuren: vacht (218,180,139) en broek (88,67,105) gemeten in het origineel; krassen (226,196,150).

## Anker: staan (klaar)
- Lijf: het echte stokloze lijf uit `stokken/bron/lijf/staan_00.png` (Animeer-canvas, +1,+82 naar het spelcanvas).
- Grok: frame groot, referentie in hulpkleuren klein linksboven, prompt `tau_anker` (zie prompts.md).
  Post `fc5af9c9-712c-485f-8261-2d08a8f5a970`, IoU 0,93. Kap met tanden, amber ogen, twee krassen op het rechterbeen in
  beeld (het been met de voet naar ons toe, het dichtst bij de camera). Krassen iets langer en steiler dan in de
  referentie, maar netjes twee en op de goede plek: goedgekeurd.
