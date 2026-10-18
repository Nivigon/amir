# Kooibandiet: worstel (kooi zit vast)

Aanvulling op `kooibandiet_sprites.zip`. Kijkt naar links (spiegel in code voor rechts).

## Set

`struggle`: 12 frames, 15 ticks (0,63 s bij 24 fps), **lus**. Na een grondslag zit de kooi vast. Hij schraagt zich en rukt eraan, de kooi komt niet los. Dit is zijn kwetsbare moment: hier is hij te raken (jouw worp-raam).

Het is een ping-pong lus: inleunen, hard achteroverrukken, terug. Laat hem zo lang lopen als het worp-raam duurt.

## Canvas en uitlijning (belangrijk)

Deze set heeft een **ander, breder canvas** dan de drag-set, want de kooi ligt hier VOOR hem (links) in plaats van achter hem.

- canvas: zie `sprites.json` (`canvas`)
- `groundline`: de grondlijn in dit canvas
- `anchor_x`: de x van zijn voeten in dit canvas

Plaats de sprite zo dat (`anchor_x`, `groundline`) op dezelfde wereldpositie van de vijand valt als bij drag. Dan staat de bandiet op exact dezelfde plek en verspringt hij niet bij het wisselen drag <-> struggle. De kooi steekt dan links verder uit dan bij drag, dat hoort zo.

## Kooi

De kooi beweegt expres een klein stukje mee: bij de diepste ruk komt hij zo'n 14 px naar hem toe en zakt dan weer terug. Dat leest als spanning op een vastzittend ding (hij krijgt hem een stukje, maar het zakt terug). Hij komt dus niet echt los.

## Lostrekken / verder

De clip bevat alleen het vastzitten (hij rukt, de kooi komt niet los). Een echt "kooi schiet los" moment zit er niet in. Dus: als het worp-raam voorbij is, stop je de lus en ga je terug naar `drag`. Wil je een zichtbaar losschieten, dan is daar een kort apart clipje voor nodig.

## Bestanden

- `sprites.json`: frames, ticks, centroids, canvas, groundline, anchor_x
- `struggle/`: de PNG's
- `struggle_preview.gif`

## Bron

Clip `kooivast.mp4`, frames 1 tot 13 (ping-pong). Man op manhoogte van de drag-set geschaald (1,045x), voeten op de grondlijn.
