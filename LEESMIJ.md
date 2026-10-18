# Kooibandiet: parry (afweer)

Aanvulling op `kooibandiet_sprites.zip`. Zelfde canvas (728x648), zelfde groundline (598), zelfde ankerpunt, kijkt naar links (spiegel in code voor rechts).

## Set

`parry`: 11 frames, 15 ticks (0,63 s bij 24 fps), eenmalig. Verveelde backhand: hij slaat met de rug van zijn vrije hand jouw speer weg alsof het een vlieg is.

| frames | wat | ticks |
|---|---|---|
| 0 | ruststand (vrije hand laag) | 1 |
| 1 tot 2 | arm laadt naar binnen | 1 |
| 3 | snelle mep, arm volledig gestrekt naar links | 1 |
| 4 | gestrekt, actief raam | 4 |
| 5 tot 6 | arm trekt terug | 1 |
| 7 tot 10 | arm bergt op, terug naar ruststand | 1 tot 2 |

## In de engine

- One-shot: onderbreek wat hij doet, speel `parry`, keer daarna terug naar `drag`.
- **Actief raam:** frame 3 tot 4. Raakt Amirs speer de bandiet in dat venster, dan wordt de speer weggeslagen (jouw spear-break). Daarbuiten is de parry niet actief.
- De kooihand blijft de ring vasthouden. De kooi staat helemaal stil: ik bevries de hele kooi (barrel, rand en ring) op frame 1 en plak die op elk frame, pixel voor pixel identiek.

## Let op

- Deze clip komt uit een losse pose waarin zijn romp iets meer naar de kijker is gedraaid dan in de sleep-loop. Bij de overgang sleep naar parry zie je dus een klein sprongetje in zijn houding. Voor een one-shot afweer is dat meestal prima; wil je het strakker, dan trek ik de parry op het zuivere zijaanzicht.
- Grok tekende tijdens de mep speedlines. Die frames (34 tot 37) gebruik ik niet; de mep springt nu in 1 beeld naar de gestrekte arm. Een effect voeg je zelf toe als je dat wilt.

## Bestanden

- `sprites.json`: frames, ticks, centroids, events (active_frames)
- `parry/`: de PNG's
- `parry_preview.gif`: sleep, parry, terug naar sleep

## Bron

Clip `parry1.mp4`, frames 30 tot 145. Uitgelijnd via de kooi op drag frame 0 (97% overlap).
