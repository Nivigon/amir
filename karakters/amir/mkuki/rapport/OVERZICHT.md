# Mkuki: eindoverzicht (22-11-2026)

Alle sets uit het plan zijn opnieuw aangekleed in de Mkuki-outfit, met de speer los (plaatsing in `../plaatsing.json`).
Per set een plaat (boven het origineel, onder Mkuki) en een GIF in deze map. Wat nog nagekeken moet worden staat in
`TWIJFEL.md`; alle keuzes per frame (Grok-post, IoU, prompt) staan in `../LOG.md`. Geen recolours.

| set | frames | plaat / GIF |
| --- | --- | --- |
| idle met speer | 22 | idle_sp |
| idle zonder speer | 22 | idle_ns |
| ren met speer | 12 | ren_sp |
| ren zonder speer | 12 | ren_ns |
| springen met / zonder speer | 7 / 7 | jump_sp / jump_ns |
| bukken met / zonder speer | 12 / 12 | bukken_sp / buk_ns |
| sluipen met / zonder speer | 22 / 28 | sluipen_sp / sluip_ns |
| rol met / zonder speer | 28 / 28 | rol_sp / rol_ns |
| trap | 2 | trap_sp |
| speerstoot | 10 | strike_sp |
| speerworp | 20 | worp_sp |
| lage zwaai | 18 | sweep_sp |
| combo | 15 | combo_sp |
| stofsweep | 14 | stof_sp |
| rol/worp | 33 | rolworp_sp |

Overige platen (`*_wissel`, `*_onaf`, `ren_ns_grok`, `idle_sp_loop`) zijn tussenstappen en vergelijkingen uit eerdere
sessies.

## Wat handwerk vraagt (kort, details in TWIJFEL.md)
- Draaiende speerframes (rol 16-22) en de speer in de rol/worp 12-15: plaatsing nakijken.
- Frames waar Grok de draaiing of de armen net anders zette: lage zwaai 8, 10, 13; combo 2, 7, 8; stofsweep 7, 8;
  rol/worp 5, 12, 24, 26, 27.
- Vastgehouden houdingen gebruiken een Grok-beeld voor meerdere frames (rol/worp 15-23 en 29-33): in het spel staat
  het dan echt stil; als er beweging in moet, per frame een eigen beeld laten maken.
