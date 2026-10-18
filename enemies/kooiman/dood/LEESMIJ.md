# Kooibandiet: dood

Aanvulling op `kooibandiet_sprites.zip`. Zelfde canvas (728x648), zelfde groundline (598), zelfde ankerpunt, kijkt naar links (spiegel in code voor rechts, net als de andere sets). De frames vallen precies over de sleepframes; er is geen extra offset nodig, ook de val past binnen het canvas.

## Set

`death`: 24 frames, 38 ticks (1,6 s bij 24 fps), eenmalig, laatste frame blijft staan als lijk.

| frames | wat | ticks |
|---|---|---|
| 0 | startpose (= drag frame 0), hier valt de witte flits op | 2 |
| 1 tot 7 | pijnscheut, hij krimpt in elkaar, hand gaat naar zijn borst | 1 tot 2 |
| 8 | grijpt naar zijn hart | 3 |
| 9 tot 14 | laat de kooi los, de kooi valt op zijn kant, hij zakt door zijn knieën | 1 |
| 15 | op zijn knieën, hand op zijn borst | 8 |
| 16 tot 21 | klapt voorover | 1 tot 2 |
| 22 | nastuiter | 2 |
| 23 | lijk, blijft liggen | rest |

## In de engine

- Bij dood: korte witte flits op frame 0 (zoals bij de bandiet), hitbox uit, start `death`.
- Vanuit elke toestand (slepen, smash, herstel, stamp) direct naar `death`; de flits verbergt de sprong naar de startpose.
- Na het laatste frame: niet terug naar een andere set, frame 23 blijft staan. Vervagen of opruimen doet de engine wanneer jij wilt.
- De kooi zit in de sprite en blijft na de val achter hem liggen.

## Bestanden

- `sprites.json`: frames, ticks, centroids en events (`kneel_frame` 15, `land_frame` 21)
- `death/`: de PNG's
- `death_preview.gif`: sleep, flits, dood, lijk

## Bron

Clip `death1.mp4`, frames 1 tot 132. Uitgelijnd via de kooi op drag frame 0 (96% overlap).
