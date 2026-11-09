# De kreten van Amir

## Amir zegt er iets van als hij geraakt wordt

`SFX_RAAK`, `playRaak()`: de twee kreten

## Amir zegt iets als een vijand sterft

`SFX_RUST`, `vijandDood(baas)` (het bestand is 9 dB harder gemaakt, met een limiter): "ta soul, rest" na elke verslagen eindbaas en na een op de `DOOD_KANS` (7) andere vijanden; elke plek waar een vijand sterft roept `vijandDood` aan

## De rol

`ROL.geluid`, `sounds/amirrol.mp3`: zwiep en plof van de gevechtsrol, gaat af bij `rolStart` (zie `notities/rol.md`)

## Amir zwijgt als een baas of een ander praat

`amirZwijg`, `praatBezig`, `baasBezig`, `praatStem`: in een baasgevecht (Nyundo, de panter met `boss`, de baviaan zodra hij afgezet heeft) en zolang een vijand of baas een zin zegt, roept Amir niets tussendoor. Dat geldt voor de kreten van `playRaak`, het "ta soul, rest" na een gewone kill en "don't need this" (`playNee`). Het "ta soul, rest" na een verslagen baas blijft, maar wacht tot diens laatste woorden uit zijn (hooguit 8 s). Een nieuwe gesproken zin meld je aan door de pool in `praatStem(...)` te zetten; nu zijn dat de strijdkreten van de bandiet, de roep en "dinnertime" van de kooiman, lach, "come here boy" en "feel my hurt" van de zweepman, en de opening, fase 2, fase 3 en laatste woorden van Nyundo.
