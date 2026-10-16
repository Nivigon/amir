# Vogel (secretarisvogel) - minimale spriteset

Datum: 2026-10-16

Twee sets, RGBA PNG op hetzelfde canvas, gecentreerd op de pivot (lichaamszwaartepunt).
De vogel kijkt naar LINKS; spiegel in code voor rechts.

## Canvas
- Canvasformaat: 536 x 405
- Pivot (positioneerpunt): 279, 207
- fps_base: 24
- Helderheid genormaliseerd per frame (de wasbleek-drift van de bron is eruit).
- Bestandspad suggestie: enemies/vogel/<set>/<set>_NN.png
- Metadata: sprites.json (per frame file, bronframe, ticks)

## Sets
| set | frames | soort |
|---|---|---|
| fly | 25 | loop |
| dive | 25 | one-shot |

### fly (loop)
De universele vlieg-animatie. Gebruik deze voor alles:
- uit de kooi schieten / opstijgen: engine beweegt hem omhoog terwijl de loop speelt.
- cirkelen: engine beweegt hem op een cirkelbaan; spiegel/draai in code voor richting.

### dive (one-shot)
De duik-aanval. Vleugels naar achteren, klauwen vooruit, duikend. De engine stuurt
de baan (richting Amir); de clip levert de duikpose. Speelt snel.

## Nog te doen (later)
- crash/dood en eventuele extra animaties.
- de dreigpose/screech als duik-tell (optioneel).

## Opmerkingen
- De vogel wordt in de engine vaak gedupliceerd; hou de sprite klein.
- Geen grondlijn (vliegend wezen); positioneren op de pivot.
