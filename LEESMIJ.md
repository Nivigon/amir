# Deur (Amir, King of Africa)

Een verweerde houten plankdeur die opengaat en daarna open blijft staan. Werkt
in een houten hut of ingehakt in een rotswand. Gemaakt uit het deur-filmpje
(Grok Imagine), magenta weggesleuteld, roze rand schoongepoetst.

## Wat zit erin

```
deur_dicht.png            de dichte deur (beginstand)
deur_open.png             de open deur met donkere opening (eindstand, blijft zo staan)
animatie/deur_00..19.png  20 frames: dicht -> opent -> blijft open (opening met diepte)
transparant/              zelfde frames, maar de opening is TRANSPARANT (zet er zelf iets achter)
deur_preview.gif          de open-animatie
metadata.json             maten, scharnierkant, afspeelinfo
```

## Hoe animeren

Speel `animatie/deur_00` t/m `deur_19` een keer af en stop op het laatste frame
(`deur_open`). De deur zwaait naar binnen open om de scharnier (links) en blijft
open staan.

- **Afspeelsnelheid bepaalt het gevoel:** snel afspelen = openvliegen (Amir trapt
  hem open, of een bandiet barst eruit), langzaam afspelen = langzaam krakend open.
- **Amir opent hem:** speel de animatie op zijn interactie.
- **Bandiet komt eruit:** speel dezelfde animatie, laat daarna de bandiet-sprite
  naar buiten lopen. De deur hoeft niks van de bandiet te weten.
- Weer dichtdoen: speel de frames achteruit af.

## De opening (donker gat)

Twee smaken, kies per situatie:

1. **Ingebouwde opening (`deur_open.png` en `animatie/`).** De opening heeft al
   wat diepte: donker bovenin, warm donkerbruin onderin, met een vage vloer. Ziet
   er altijd goed uit, geen extra werk.
2. **Transparante opening (`transparant/`).** De opening is doorzichtig. Zet er in
   de engine zelf een laag achter: een kamer, een grot, een warme fakkelgloed, of
   een bandiet die eruit loopt. Flexibelst.

Wil je het nog rijker: zet achter de transparante versie een klein beetje
randlicht of een fakkelgloed diep in de gang, dat haalt het laatste beetje
"plat gat" weg.

## Plaatsing

- **Scharnier zit links**, de deur opent naar binnen (de duisternis in).
- Zet de **onderkant op de grond** (niet laten zweven).
- In een rotswand leest het het best als je de rots een heel klein stukje over de
  buitenrand van het kozijn laat vallen, dan oogt het uitgehakt in plaats van
  opgeplakt.
- Schaal naar wens; in de testscene stond hij op ongeveer 40% van de rotshoogte.
  Verhoudingen kloppen onderling.
