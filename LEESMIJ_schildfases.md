# Schildbandiet: strike en flinch in alle schildfases

Gemaakt met de Animeer tool (export 24-10-2026). Alle frames 544 x 860, grondlijn 781,
anchorX 272, kijkrichting links, zelfde canvas als de bestaande sets.

## Sets in deze map

| set | frames | wat |
|---|---|---|
| strike_metschild | 30 | heel schild (vervangt de bestaande) |
| strike_fase1 | 30 | schild met één hap eruit (nieuw) |
| strike_fase2 | 30 | schild met twee happen eruit (nieuw) |
| strike_zonderschild | 30 | zonder schild (vervangt de bestaande) |
| flinch_metschild | 21 | heel schild (vervangt de bestaande) |
| flinch_fase1 | 21 | één hap (nieuw) |
| flinch_fase2 | 21 | twee happen (nieuw) |
| flinch_zonderschild | 21 | zonder schild (nieuw, stond al in metadata maar bestond nog niet) |

De loop zit hier bewust niet in: `loop_metschild` en `loop_zonderschild` blijven zoals ze zijn.

`metadata.json` is bijgewerkt met de nieuwe sets (zelfde framecount en `durations_ms` als
de bestaande strike en flinch) en met `schild_staat`.

## Welke set wanneer

| treffers op het schild | strike en flinch | loop |
|---|---|---|
| 0 | `*_metschild` | `loop_metschild` |
| 1 | `*_fase1` | `loop_metschild` (nog geen fase-loop) |
| 2 | `*_fase2` | `loop_metschild` (nog geen fase-loop) |
| 3, schild weg | `*_zonderschild` | `loop_zonderschild` |

Bij de flinch na treffer 1 en 2 kun je het best al de flinch van de nieuwe fase spelen:
dan zie je de hap verschijnen op het moment van de klap.

## Let op

- Teken elke set als het hele canvas van 544 x 860 met de grondlijn op dezelfde
  scherm-y, zoals de bestaande sets. Niet bijsnijden of op de randen passen.
- Het schild zit in deze sets in de frames gebakken (optie B). De gelaagde aanpak
  (optie C) komt later; deze map is de tussenstap.
- Geheugen: de vier nieuwe sets voegen samen ongeveer 190 MB uitgepakt toe aan de grote
  versie. Maak er ook de kleine versie van (zelfde route als de rest van de schildbandiet).
