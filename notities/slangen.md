# Slangen

## slangen: kleur, zicht en patrouille

`SNAKE_DIRS`, `slangZiet`, `startPatrouille`, `slangSchuif`. De zwarte slang (`k: 'zwart'`) en de knockslang (`k: 'knock'`) zijn spuwers: ze bijten niet maar spuwen gif (`spit`, `updateVenom`), blijven op afstand, draaien om bij een ravijn en volgen je ook buiten beeld. Of een slang een spuwer is beslist `spuwer(s)` (gebruik die, niet `=== 'zwart'`, voor nieuw spuwer-gedrag). De knockslang is jade/violet (`enemies/slang1_knock/`, een recolour van slang1) en zijn goo (`enemies/slang1_knock/venom.png`, `venomKnockImg`, `v.knock` op elke druppel) doet geen schade maar duwt Amir `KNOCK_CELLEN` level-maker cellen terug (`knockVenomRaak`, zet de bestaande `knock`-snelheid); die terugstoot duwt gewoon door, ook een ravijn in of een platform af. Test 43 is het proefstuk
