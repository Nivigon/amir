# Lag: wat er gemeten is, wat er gedaan is en wat er nog ligt

Onderzoek van november 2026. De conclusie: de lag komt bijna volledig van het aantal pixels dat per beeld
gevuld wordt, niet van de spelcode. Het eigen JavaScript kost minder dan 1 ms per beeld.

## Zo meet je

`tools/profiel.js` (de speelrobot met een profiler erbij) loopt een level uit en meldt de beeldtijd:

```
node tools/profiel.js "Valse Koning 1" --taai --max 20
node tools/profiel.js "Rivier 1" --taai --max 20 --zonder stadAchter     wat kost die functie?
node tools/profiel.js "Valse Koning 1" --taai --max 20 --dpr 2           een scherp scherm
```

- Er is hier geen grafische kaart: de milliseconden zijn hoger dan bij een speler, de verhoudingen kloppen
  en lijken het meest op een zwakke laptop of telefoon.
- Vergelijk altijd twee runs die tegelijk draaien (`a & b & wait`); een losse run is sneller dan een paar.
- Of het beeld gelijk blijft: `node tools/beeldgelijk.js --vlag NAAM` (de vlag moet een `var` zijn).
- In het spel zelf: F9 toont fps en beeldtijd op het apparaat van de speler.

## Wat een beeld kost (voor de wijzigingen, 1280x720 op 1x)

Per beeld wordt het scherm 4 tot 6 keer volledig overgeschilderd, in Test 10 (onder de grond) 21 keer.

| uitgezet als proef | level | beeldtijd | verschil |
| --- | --- | --- | --- |
| basis | Valse Koning 1 | 40 ms | |
| zelfde level op 2x resolutie | Valse Koning 1 | 119 ms | 3 keer zo traag |
| op 2x in de stand Soepel | Valse Koning 1 | 36 ms | |
| zonder verte (bergen, mist, zon) | Valse Koning 1 | 27 ms | 33% |
| zonder lichtlaag | Valse Koning 1 | 31 ms | 23% |
| zonder weer en voorgrond | Valse Koning 1 | 38 ms | 6% |
| zonder lichtlaag | Rivier 1 | 42 naar 33 ms | 22% |
| zonder achterste huizenrijen (`stadAchter`) | Rivier 1 | 42 naar 36 ms | 15% |
| zonder lichtranden en schaduwen | Rivier 1 | 42 naar 39 ms | 8% |
| zonder lichtkaart | Test 10 | 60 naar 41 ms | 31% |

## Gedaan (pull request 730)

- **De verte als platen** (`VERTE_PLAAT`): 18 tot 22% sneller in savannelevels, 12% in een klimlevel, niets
  in de stad. Zie "de verte als platen" in `notities/tekenlagen.md`.
- **De lichtlaag als platen** (`LICHT_PLAAT`): 5 tot 12% sneller, ook in de stad, niets onder de grond.
  Zie "de lichtlaag als platen" in `notities/tekenlagen.md`.

Geleerd: een kleiner plaatje uitrekken is in software trager dan een verloop tekenen; een plaat op de maat
van het doek is sneller. En mengstappen over het hele beeld (multiply, lighter) zijn zelf de kosten: minder
stappen helpt, een goedkopere stap nauwelijks.

## Wat er nog ligt, op volgorde van winst

1. **Resolutie sneller laten zakken** (`perfTick`, `DPR_MAX`, `dprCap`, `beeldModus`). De grootste hefboom,
   raakt elk level. Automatisch begint op 2x en zakt pas na twee trage vensters van 90 beelden (boven 21 ms),
   een halve stap per keer, op een laptop niet onder 1,25x en nooit meer omhoog. Soepel (1x) haalt op een
   2x-scherm 36 ms tegen 119. Opties: eerder en sneller zakken, de vloer op een laptop naar 1x. Kost scherpte
   op apparaten die het niet trekken.
2. **De lichtkaart in grotlevels** (`drawLichtkaart`). Ongeveer 30% in levels onder de grond. Twee tot drie
   grote vergrotingen van een kleine kaart per beeld met `imageSmoothingQuality 'high'`, plus een `lighter`
   met een evenodd-clip. Proberen: 'medium', en de kaart per camerastand bakken.
3. **De stad** (`stadAchter`, `stadRijStrookMaak`). De achterste huizenrijen kosten rond 15% en maken telkens
   een nieuw canvas van ruim twee schermen in plaats van een doek te hergebruiken (ook een bron van
   haperingen). In de nacht per beeld 60 radiale verlopen (`stadNachtNa`) en 30 lineaire (`stadNachtRamen`):
   dat kunnen vaste plaatjes worden.
4. **De korte haperingen**: losse beelden van 80 tot 240 ms als iets voor het eerst in beeld komt.
   - vegetatie: 65 tot 80 ms bij de eerste tekening van een grote plaat (`drawVeg`, `struik_sheet` is 4320 px)
   - een nieuw bergpaneel: 40 tot 55 ms, `onScale` zet het bij eerste zicht op schermmaat; kan achter het
     laadscherm (`warmBouw`)
   - rune-licht (`runeLichtMaak`, 50 ms) en lichtranden (`plichtRand`): pas gebakken als ze nodig zijn; de
     sleutel van `plichtRand` hangt aan de schermmaat van de figuur, dus elke zoomstap van de meekijkende
     camera bakt opnieuw. Kwantiseren helpt.
5. **Plaatjes voor telefoons.** Acht spritesheets zijn breder dan 4096 px (zes van de panter, tot 16800 px,
   de schorpioen-charge en `struik_sheet`). De kleine set (`KLEIN_FAM`, `beeldAuto`) krijgt alleen een
   telefoon; tablets en zwakke laptops krijgen groot. Zonder kleine versie: kruisboogbandiet, Murghtaan, de
   slangen, de achtergronden en de meeste stadsplaten. WebP scheelt in een steekproef 80% download, maar
   niets aan de lag tijdens het spelen.

Niet de moeite: de spellogica en de vijanden-AI (minder dan 1 ms), het weer en de voorgrond (samen 6%).

Advies: eerst 4 (schokjes vallen het meest op en het beeld verandert er niet door), dan 1. Punt 2 en 3
alleen als de lag vooral in grotten of in de stad zit. Nog niet bekend: op welk apparaat en in welke levels
de opdrachtgever de lag het meest merkt.

## Kleinere vondsten uit het lezen (niet gemeten)

- `filter: blur` per beeld: een verstopt zegel (`ZEGEL_VERBORGEN.kuil`), brekende tonnen.
- `shadowBlur` per beeld: `runeSchijf` (aan), `zegelGrond`, de woede van Amir, Brutus, fakkelvonken.
- `maskerTeken` maakt per beeld per masker een `createPattern` zonder cache.
- `ravijnAchterVangEen` tekent het hoofdcanvas naar een doek, per zichtbaar ravijn per beeld.
- Caches die nergens gewist worden: `stadBakken`, `vgCache`, `scaleCache`, `seqCache`.
