# Amir neer (co-op wacht op revive) en sterven, 27-11-2026

Nieuwe val-animatie: Amir grijpt naar zijn zij, zakt door zijn knieën, leunt voorover op een onderarm en glijdt dan neer op zijn zij, hand op zijn zij, hoofd iets opgetild. Hij leeft nog (co-op: wacht op revive). Ook bruikbaar als sterfanimatie in single player.

## Frames
- Mkuki (speer-tribe): `karakters/amir/mkuki_spel/beweging/neer/neer_00..45.png` (46 frames), klein in `klein/...`.
- Stokken-Amir (klassiek tenue, leeuwenvacht + paarse broek): `karakters/amir/beweging/neer/neer_00..56.png` (57 frames), klein in `klein/...`.
- Canvas 594x301 (klein 297x150), voeten op x=295, y=296, net als `idle/idle_ns.png`. Geen speer of stokken in de hand.
- De twee sets hebben een EIGEN beweging en een ander aantal frames (eigen Grok-video's). Niet als skin van elkaar gebruiken (`mkSkinVan` zoekt op dezelfde naam; dat klopt hier niet).
- Laatste frame = de neer-pose (ligt stil). Wacht-loop (ademen) volgt later.

## Timing (zoals in de preview)
- Mkuki: frames 0-20 ~42 ms, 21-45 ~63 ms (totaal ~2,5 s).
- Stokken: frames 0-21 ~42 ms, 22-56 ~50 ms (totaal ~2,7 s).

## Recolor
- Stokken: `node tools/vacht_bak.js` (map `beweging` wordt al meegenomen) maakt de maskers voor de zes stoktribe-outfits.
- Mkuki: zonekaarten (`<frame>_zones.png`) moeten nog gemaakt worden; deze frames komen niet uit de Mkuki animeer tool, dus `mkuki_spel_zones.py` werkt er niet direct op.

Herkomst en werkwijze: project-doc `claude/amir_neer_coop.md`.
