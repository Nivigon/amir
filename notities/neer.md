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
- Stokken: `node tools/vacht_bak.js` (map `beweging` wordt al meegenomen) maakt de maskers voor de zes stoktribe-outfits, in `karakters/amir_vacht/beweging/neer/`. Het spel kleurt ze via `broekLap`, op de framenaam (`beweging/neer/neer_NN.png`).
- Mkuki: `python3 tools/neer_zones.py [--toon uit.png]` maakt per frame `<frame>_zones.png` (en de helft in `klein/`). Deze frames komen niet uit de Mkuki animeer tool, dus `mkuki_spel_zones.py` werkt er niet op; de zones gaan op kleur (broek donkergrijs, of blauwpaars in de frames met een paarse Grok-zweem; schort zand, die doorgroeit in zijn vale randen; kralen rood, alleen de grote stukken; armbanden koper; leer bij de schort is de riem). De schuine band is bijna zo bruin als de huid: die staat per sleutelframe als lijn van de kralen door de gesp (`BAND_LIJN`, op het oog gezet), de frames ertussen schuiven mee. Elk kledingstuk groeit 2 px over de donkere omtrek, zodat er na het omkleuren geen randje in de oude kleur blijft. Nagekeken met `tools/outfittest.js --frames mkuki_spel/beweging/neer/neer_00.png,...` (alle zes outfits).
- Omdat de val van Mkuki een eigen frame is en niet uit de skin komt, slaat `broekBeeld` voor deze frames `mkSkinVan` over (`neerMk`) en kleurt het frame zelf met `mkLap`.

## In het spel (`NEER`)
- `amirSterf(lig)` vervangt `dead = true; deadEl...` op de plekken waar Amir sterft (een klap, een val, de fosforbeet). De set volgt de outfit (`neerSetVan`: een outfit van Mkuki met skin is `mk`, de rest `stok`). `neerStap` loopt de frames af met de timing hierboven.
- Single player: het doodscherm komt `NEER.scherm` (0,35 s) na het laatste frame. In een ravijn gestort (`fallDeath`): meteen de neer-pose en meteen het scherm, zonder val.
- Co-op Survival en de Co-op episode: is iedereen dood, dan komt het eindscherm pas na de val (`mpcEindWacht`, zie "Eerst de val, dan het eindscherm" in `notities/multiplayer.md`).
- Co-op en Duel: geen doodscherm; de neer-pose blijft liggen tot de revive. `mpcLig` (het oude omkantelen) alleen nog als de frames er niet zijn. Teamgenoten krijgen het pad van het frame mee (`pvpVang`), dus zelfde moment en zelfde set, in hun outfit (`neerIs` houdt bij hen `mpcLig` weg). Silver Pride, de veren en de revive-ton werken op de plek van de speler, niet op het beeld, dus die lopen gewoon door; de veren van de zelf-revive stijgen op uit het midden van het liggende lijf (`lijkX` in `bnZelfTeken`).
- Laden: `neerLaadLevel` in `laadLevel` (single player de set van nu, met een teamgenoot beide), en de set van nu wordt bijgeladen als je van wapen wisselt. De sandbox laadt beide.
- Sandbox: **Fall: Mkuki** en **Fall: sticks** (naast Speel dood) spelen de val, laten hem `NEER.sbLig` liggen en zetten hem weer overeind (`neerSandbox`).
- Testen: `node tools/mptest.js --neer --stokken host --spelers 2` (de gast valt als Mkuki, de host als de stokken-Amir, de ander ziet dezelfde frames in de juiste set, het hart en de veren brengen ze terug); `--sterf gast` en `--bennu` lopen ook nog.
- Nog niet: een wachtloop (ademen) in de neer-pose. De oefenteamgenoot van Test 91 en 94 ligt nog omgekanteld (`zhPopTeken`).

Herkomst en werkwijze: project-doc `claude/amir_neer_coop.md`.
