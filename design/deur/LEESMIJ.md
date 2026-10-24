# Deur (Amir, King of Africa)

Een verweerde houten plankdeur die opengaat en daarna open blijft staan. Werkt
in een houten hut of ingehakt in een rotswand. Gemaakt uit het deur-filmpje
(Grok Imagine), magenta weggesleuteld, roze rand schoongepoetst.

Alle beelden zijn even groot (351 bij 448, transparant). De scharnier zit links;
de deur zwaait naar binnen open. De onderkant van de deur staat onderaan het
canvas, dus zet die op de grondlijn.

## Wat zit erin

```
deur_00.png .. deur_19.png   20 frames: dicht -> opent -> blijft open
deur_dicht.png               de dichte deur (= deur_00, de beginstand)
deur_open.png                de open deur met donkere opening (= deur_19, de eindstand)
deur_open_transparant.png    dezelfde open stand, maar de opening is TRANSPARANT
metadata.json                maten, scharnierkant, afspeelinfo
```

De frames (`deur_00..19`) hebben een ingebouwde donkere opening met wat diepte.
`deur_open_transparant.png` is er alleen in de open eindstand; de losse open-frames
daarvan zijn niet geleverd. Wil je er zelf een laag achter (een kamer, een gang,
een fakkelgloed), dan zet je dat achter de transparante open-stand; voor de
animatie zelf gebruik je de gewone frames met het donkere gat.

## Hoe animeren

Speel `deur_00` t/m `deur_19` een keer af en stop op het laatste frame
(`deur_open`). De deur zwaait naar binnen open om de scharnier (links) en blijft
open staan.

- **Afspeelsnelheid bepaalt het gevoel:** snel afspelen = openvliegen (Amir trapt
  hem open, of een bandiet barst eruit), langzaam afspelen = langzaam krakend open.
- **Amir opent hem:** speel de animatie op zijn interactie, of als hij in de buurt komt.
- **Bandiet komt eruit:** speel de animatie en laat daarna de bandiet-sprite naar
  buiten lopen. De deur hoeft niks van de bandiet te weten.
- Weer dichtdoen: speel de frames achteruit af.

## Plaatsing

- **Scharnier zit links**, de deur opent naar binnen (de duisternis in).
- Zet de **onderkant op de grond** (niet laten zweven); de grondlijn zit onderaan
  het canvas.
- In een rotswand leest het het best als je de rots een heel klein stukje over de
  buitenrand van het kozijn laat vallen, dan oogt het uitgehakt in plaats van
  opgeplakt.
- Schaal naar wens; in de testscene stond hij op ongeveer 40% van de rotshoogte.
  Verhoudingen kloppen onderling.

## In het spel

In het spel staat de deur in de rotswand `design/rotswand_kaal.png`, geschaald op
Amir (zie `DEUR` in de HTML, kop "deur in de rotswand"). Op het moment dat hij
openvliegt klinkt `sounds/deurslam.mp3`. Onder de deur ligt een dun stenen
drempeltje: dat is de donkerbruine rotssokkel uit de fakkel-plaat (`design/einde.png`),
met zijn aflopende randen, geschaald tot een strook. Een level kan met de deur ook
eindigen (`uitgang`): na het gevecht speel je met E op de open deur uit, zonder
fakkels. Test 35 is het proefstuk: Amir loopt naar links, bij de rotswand vliegt de
deur open en een bandiet komt uit de deuropening op hem af; daarna loop je naar de
open deur en drukt op E. In de sandbox onder Terrein, Deur.
