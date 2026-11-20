# Regenwoud (nog niet in het spel)

Vloertegels voor een nieuwe biome, sfeer ochtendmist. Alles 1572x335, zelfde opbouw en
looplijn als `design/grondrand.png` (EDGE walk 95, solid 305, kruin 46).

- `grondrand_regenwoud.png`: de basis
- `grondrand_regenwoud_bladeren.png`, `_wortels.png`, `_mos.png`: varianten tegen de herhaling
  (de mos-tegel is iets lichter, de wortels steken iets boven het loopvlak uit)
- `grondrand_overgang_lang.png`: 4716x335, drie tegels breed, savanne links naar regenwoud
  rechts. Links naadloos op `grondrand.png`, rechts op `grondrand_regenwoud.png`. De
  grondsoort-overgang van het spel (GRONDSOORT.rand, 88 px) is hiervoor te kort.
- `bron/sfeer_ochtendmist.png`: sfeerbeeld uit Grok (heeft perspectief, alleen voor kleur en licht)

Achtergrond (Grok-edit van de savannelagen, zelfde stijl, magenta weggekeyd):
- `midden_regenwoud_a.png` (1792x698): middenlaag, uit `design/bg/laag2/midden_4.png`. Paraplukronen, lianen, varens.
- `verre_regenwoud_a.png` (1792x367): verre laag, uit `design/bg/laag1/verre_bergen_2_ruggen.png`. Beboste heuvelruggen.
- de Grok-platen staan in `bron/` (`*_grok.png`).
Ingame getest op de savanne-ochtend (warm): het licht van het spel maakt ze vanzelf goudgroen.

Nog niet aangemeld in de code en niet in de offline-download.
