# Schildbandiet: knielen, wankelen, vallen en de special execution (optie C, lagen)

Map in de repo: `enemies/schildbandiet/executie/` met `executie.json` en `lagen/` (127 unieke plaatjes,
~29 MB uitgepakt voor de grote set). Zelfde opzet als `lagen.json` van loop, strike en flinch.

## Een frame tekenen
`executie.json` > `bewegingen` > `<naam>` > `frames[i]` is een lijst lagen in tekenvolgorde. Elke laag heeft
`src`, `dx`, `dy`, `w`, `h` en `item`.
- `dx`, `dy`: linkerbovenhoek t.o.v. anchorX (272) en de grondlijn (781), in pixels van de grote set.
- Teken in dezelfde translate/scale als de andere schildbandiet-lagen:
  `ctx.drawImage(img, ANCHOR + dx, GROND + dy, w, h)`. Spiegelen voor naar rechts blijft `ctx.scale(-1,1)` om het
  anker. Alle art kijkt naar links (schildman rechts, Amir links van hem).
- `item`: `lijf`, `speer` (Amirs speer), `wond`, en in de executie `schildman`, `amir`, `speer_voor` (het stuk
  schacht dat voor hem langs loopt tot de wond). Speer en wond zijn losse lagen zodat dezelfde lijf-frames later
  ook zonder speer (Dood laag) kunnen; dat hoeft nu niet.
- Timing: `durations_ms` per beweging. De kleine set: laat gen-klein.py / KLEIN_FAM ook deze `lagen/` halveren;
  dx, dy, w en h blijven ongewijzigd.

## Bewegingen
- `knielen` (20): na de dodelijke treffer zakt hij op zijn knieën, Amirs speer horizontaal in zijn borst, met wond.
  Zijn eigen speer valt en blijft op de grond liggen.
- `wankel` (16, loop, 12 fps): geknield, zwaar ademend. Frame 0 sluit exact aan op het laatste knielen-frame.
- `val` (16): vanaf de knieën voorover, plat op zijn buik. Amirs speer glijdt uit de wond en ligt vanaf frame 7 op
  de grond (`speer_ligt_op`). Laatste frame blijft liggen.
- `executie` (17): Amir rukt de speer eruit en landt. Per frame de lagen schildman, amir en speer. De schildman-laag
  is in frame 1 nog met zijn eigen speer op de grond, daarna zonder. Gegevens: `amir_start_x`, `amir_eind_x`
  (t.o.v. het anker) en `snijlijn` (door de wond en de kruin van zijn hoofd).

## Wanneer (gewone schildbandiet)
- **Speersteek-kill, kans 1 op 5**: `knielen`, en zodra dat klaar is direct de executie (zie onder).
- **Speerworp-kill, kans 1 op 3**: `knielen`, dan `wankel` in een loop gedurende 3 seconden. Amir kan naar hem toe
  lopen; staat hij in de buurt van `amir_start_x` (ruim, ongeveer een halve Amir-breedte), toon een E-hint, met E
  start de executie. Na 3 seconden zonder E: hij maakt de lopende wankel-loop af en speelt `val`. Vanaf het frame
  waarop Amirs speer op de grond ligt, wordt die het echte oppakbare voorwerp op `speer_ligt_op` (zoals na een worp)
  en teken je de `speer`-laag niet meer.
- De andere kills (4 op 5 steek, 2 op 3 worp, en elke lage zwaai) zijn de gewone dood, uit dezelfde lagen: `knielen` en
  direct daarna `val`, zonder wankelen en zonder E. Na een worp met de lagen `speer` en `wond` en de speer die vanaf
  frame 7 van de val echt op de grond ligt (Dood hoog); anders zonder die twee lagen, Amir houdt zijn speer (Dood laag).
  De oude dood-set (`dood/`) is weg.

## De executie
- **Time freeze**: alles behalve de executie staat stil (andere vijanden, projectielen, deeltjes, timers). Amir is
  onkwetsbaar. Geen slowmotion: de frames zijn met de hand gekozen sleutelframes met holds en spelen op normale
  snelheid.
- Zet Amir op `amir_start_x`, verberg de echte Amir en de schildman, en teken de executie-lagen op de plek van de
  schildman, met zijn schaal.
- Na het laatste frame (de landing, 600 ms): **splijten**. Knip de `schildman`-laag langs de `snijlijn` (doorgetrokken
  over zijn hele lijf) in twee helften die uit elkaar gaan en vallen of vervagen; gebruik het bestaande bloedsysteem
  (spurt langs de lijn, druppels, lens). Teken de `amir`- en `speer`-lagen van het laatste frame er bovenop.
- **Daarna**: Amir staat direct gewoon rechtop in zijn idle (geen opsta-animatie) op `amir_eind_x`, kijkend van de
  schildman af, met zijn speer in de hand. De freeze eindigt.

## Effecten en geluid
Komen later. Laat haakjes achter bij: begin freeze (E of de steek), de ruk (overgang executie frame 5 naar 6), de
landing (frame 16) en het splijten.

## Testen
Eerst in de sandbox: maak een manier om de execution te forceren (100%), voor steek en worp, en een worp-kill
waarbij je geen E drukt (val). Controleer ook gespiegeld en op de kleine set, en meet het geheugen.
