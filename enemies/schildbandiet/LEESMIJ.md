# Schildbandiet (block and kill) - testlevel

Nieuwe vijand voor Amir, King of Africa. Hij loopt dreigend op Amir af met een
houten schild op, en valt aan door te springen. Dit pakket is een eerste
testversie, nog niet de eindkwaliteit (kleuren nog niet naar vast palet gesnapt,
schild-in-stukken en echte dood-animatie volgen later).

## Bestanden

- metadata.json          canvas, grondlijn, anchor, sets, fps, strike-timing, keyframes
- loop_metschild/        dreigende loop MET schild (walk_00..walk_21)
- loop_zonderschild/     zelfde loop ZONDER schild (na breuk)
- strike_metschild/      sprong-aanval MET schild (strike_00..strike_29)
- strike_zonderschild/   zelfde aanval ZONDER schild (na breuk)
- schild/                losse schild-sprites ter referentie
- speer/                 losse speer-sprite ter referentie

Alle frames staan op hetzelfde canvas (544x860) met dezelfde grondlijn (781) en
anchorX (272), zodat loop en strike naadloos wisselen zonder dat hij verspringt.
Kijkrichting is naar links; spiegel in code voor naar rechts.

## Gedrag (testlevel)

1. Hij loopt op Amir af met schild op -> set `loop_metschild` (loop, ~10 fps).
2. Amir raakt hem: witte flits over de sprite + een paar houtsnippers
   (hergebruik de doornbos/thornbush splinter-particles). Dit kan 3x.
3. Na de 3e treffer valt het schild weg: wissel naar de `*_zonderschild` sets.
   Vanaf nu is hij in 1 klap dood.
4. Zodra hij bij Amir staat, valt hij elke 2 seconden aan met de sprong-aanval
   (`strike_metschild`, of `strike_zonderschild` als het schild al weg is):
   - tell: hij zakt diep door zijn knieen en houdt zich kort laag
     (keyframes tell_crouch in metadata)
   - sprong: hij springt naar de plek waar Amir stond op het moment van inzetten
   - tijdens de sprong is hij ONSTUITBAAR en ONAANTASTBAAR
   - landing + herstel: daarna weer kwetsbaar
   Amir moet dus wegstappen om de sprong te ontwijken.

De sprongboog zit al in de frames (hij komt omhoog en weer neer binnen het canvas).
De horizontale verplaatsing naar Amir doet de engine: verplaats de sprite tijdens
de leap-frames naar de doelpositie.

## Timing

- loop: fps in metadata (pas aan naar gewenste loopsnelheid)
- strike: per-frame duur in metadata.sets.strike_metschild.durations_ms

## Later verfijnen (niet in deze test)

- Schild in 3 stappen laten breken (hap, half, weg) i.p.v. in 1 keer verdwijnen.
- Echte dood-animatie.
- Kleuren naar vast palet snappen voor recolor (losse scheidbare kleurvlakken).
- Schild als echte losse engine-laag met per-frame plaatsing (data is er al).
