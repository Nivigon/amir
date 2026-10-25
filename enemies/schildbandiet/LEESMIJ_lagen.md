# Schildbandiet: loop, strike en flinch als lagen

Vervangt de complete frames per schildfase (`schildbandiet_schildfases.zip`, optie B) en
de oude loop-sets; sinds 25-10-2026 is dit de enige versie in het spel (de oude mappen zijn
weg). Dit is optie C: het schild is een losse laag, de rest van de figuur is
samengevoegd tot zo weinig mogelijk lagen, alles bijgesneden tot de eigen randen.

## Inhoud

- `lagen.json`: per beweging (loop, strike, flinch), per frame, per schildstaat de lagen
  in tekenvolgorde.
- `lagen/schild/` (81) en `lagen/lijf/` (116): de plaatjes. Elk plaatje staat er één
  keer in, ook als het in meerdere frames, staten of bewegingen voorkomt (de loop gebruikt
  bijvoorbeeld per staat steeds hetzelfde schildplaatje). `lagen.json` verwijst ernaar.

## Schildstaten

| treffers | staat |
|---|---|
| 0 | metschild |
| 1 | fase1 |
| 2 | fase2 |
| 3 (schild weg, daarna in één klap dood) | zonderschild |

Loop, strike en flinch gebruiken alle drie dezelfde staat.

## Een frame tekenen

Elke laag heeft `src`, `dx`, `dy`, `w`, `h` en `schild`.

- `dx`, `dy`: linkerbovenhoek ten opzichte van anchorX (272) en de grondlijn (781), in
  pixels van de grote set. `w`, `h`: tekengrootte in pixels van de grote set.
- Teken de lagen van de huidige staat in de volgorde van de lijst, in dezelfde
  translate/scale als nu (spiegelen voor naar rechts blijft `ctx.scale(-1,1)` om het
  anker).
- Een frame heeft 1 tot 3 lagen. `schild: true` markeert het schildstuk; bij
  `zonderschild` zit er geen schild in.
- Omdat dx, dy, w en h in grote-set-pixels staan, werkt de kleine set vanzelf: dezelfde
  getallen, alleen een half zo groot plaatje.

## Timing

`durations_ms` per beweging staat in `lagen.json`: strike en flinch gelijk aan de oude
sets, de loop 100 ms per frame (10 fps, zoals nu) met `loop: true`.

## Geheugen

Loop, strike en flinch samen, grote versie, uitgepakt: ongeveer 67 MB voor alle vier de
staten (versie lagen-2; de eerste versie had dubbele plaatjes en kwam op 85 MB). Met complete frames per staat zou dat rond de 550 MB zijn.
