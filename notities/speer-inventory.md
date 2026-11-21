# Speersoorten in de inventory (ontwerp, nog niet gebouwd)

Uitgedacht met de opdrachtgever op 22 november 2026. Er is nog niets van gebouwd. Het bouwt voort op wat er al is:
de reserve-speren op de rug (`RUG`, zie `notities/rug-speren.md`), de winkel en de inventory (`notities/gif.md`) en het
wapenrek. Aanleiding: de Pathfinder Spear komt in de winkel, en er komen later meer speersoorten bij.

## Besloten

- **Meerdere speren, elk met een soort.** Je kunt verschillende speren hebben (gewone speer, Pathfinder, later meer), en
  ook meerdere van dezelfde soort.
- **Max 2 mee**: 1 in de hand en 1 op de rug, zoals nu (`RUG_STANDAARD`). Een derde speer (een extra plek) is te koop,
  of komt uit een talent (Third Spear van Mkuki bestaat al).
- **Volgorde in de inventory.** De speler zet zijn speren in een volgorde. De hand pakt altijd de hoogste uit die lijst
  die hij op dat moment echt bij zich heeft; de rest hangt op de rug.
- **Een speer houdt zijn plek.** Gooi je de speer uit je hand, dan blijft hij liggen of steken waar hij landt, en schuift
  de volgende in je hand. Raap je hem weer op, dan is hij nog steeds wat hij in de volgorde was: een hogere gaat terug
  naar de hand, de andere naar de rug.
- **Automatisch wisselen, plus een wisselknop.** Het spel wisselt vanzelf volgens de volgorde, en met een knop wissel je
  bewust welke speer in je hand zit (zodat je kiest welke je gooit).
- **Zichtbaar op de rug.** Per animatie een vaste plek aanwijzen in de animeer tool, net als de andere items: daar komen
  de tweede (en derde) speer, op elkaar gestapeld met de punten zichtbaar, alsof ze in een koker zitten. Geen echte koker
  tekenen. Alle speersoorten krijgen dezelfde maat, zodat een plek voor elke soort werkt.
- **Co-op: het is jouw speer.** Alleen de eigenaar raapt hem op.

## Mogelijke ideeën (in de gaten houden, niet bouwen)

- **Oppaktijd per speersoort.** Een zware of speciale speer kost langer om op te rapen (E vasthouden met een ringetje dat
  volloopt, afgebroken als je geraakt wordt). Zo wordt elke speer een afweging, ook in levels of groepen vijanden waar je
  bijna alleen maar kunt gooien en geen tijd hebt om op te rapen.
- **Lege handen.** Zonder speer kan Amir nu niets; voorlopig is de oplossing: zorg dat je een speer krijgt. Later kan er
  iets bij, zoals een zwakke trap of duw die ruimte maakt om te rapen, of de dolk.
- **Kwijtraken of kapotgaan.** Nog open: blijft een speer die je laat liggen weg, of zit hij aan het eind van het level
  weer in je inventory? Een idee is een kans per speersoort dat hij breekt, als tegenwicht voor wat hij oplevert (de oude
  speer breekt nu al na drie keer, `OUDE_SPEER`).
- **Co-op: elkaars speren gebruiken.** Elkaars speer oprapen en gooien zou ook vet kunnen zijn; eventueel als regel die
  de host in de lobby aan of uit zet.

## Waar het tegenaan loopt in de code

- Het spel houdt nu maar één speer in de wereld bij als "de jouwe" (`spearX`); een tweede wordt een losse speer
  (`eigenSpeerLos`). Met soorten moet elke speer in de wereld zijn soort en eigenaar onthouden.
- De rug tekent de speren nu in schermruimte (`rugSpeerTeken`); de per-frame plek uit de animeer tool komt in de plaats.
- De speer in de winkel geldt nu alleen voor dat level (`restart` begint met een volle rug); gekochte soorten moeten
  bewaard blijven, net als het goud en de inventory (`goudWin`, `goudVerder`).
