# Kooimannetje (vijand met kooi) - spriteset

Datum: 2026-10-16

Drie animatiesets, allemaal RGBA PNG op hetzelfde canvas en dezelfde grondlijn,
uitgelijnd op de sleephouding zodat de sets naadloos aan elkaar schakelen.

## Canvas
- Canvasformaat: 726 x 648
- Grondlijn: rij 598 (voeten staan hier)
- fps_base: 24 (tick-duur = 1/24 s)
- Bestandspad suggestie: enemies/kooiman/<set>/<set>_NN.png
- Metadata met per frame de ticks, bronframe, grondlijn en zwaartepunt: sprites.json

## Sets

| set | frames | soort | duur (ticks) |
|---|---|---|---|
| drag | 29 | loop (slepen) | 29 |
| smash | 31 | one-shot (aanval) | ~46 incl. holds |
| recovery | 21 | one-shot (herstel) | 21 |

### drag (loop)
Het mannetje sleept de zware kooi achter zich aan, gebukt, in de sleephouding.
Loopt naadloos rond. Dit is tevens zijn rusttoestand: hij staat nooit echt stil.

### smash (one-shot, aanval)
Fasering (set-frames, 0-based):
- 0-9  : wind-up, kooi laag naar achter. Frame 9 is de diepste coil met een
         anticipatie-hold (extra ticks).
- 10-25: kooi omhoog tot kophoogte en neerwaartse smash.
- 25   : impact_frame. De kooi raakt de grond. Hier zit een korte hitstop
         (extra ticks). Spawn op dit frame de grondstof + korte speler-stagger.
- 26-30: uitzakken tot gebukt over de kooi. Frame 30 heeft een end-hold; dit is
         het kwetsbare straf-window en sluit aan op recovery.

Hij blijft de hele aanval gebukt en met beide voeten op de grond.

### recovery (one-shot, herstel)
Vanaf gebukt over de kooi vooraan sleept hij de kooi terug naar achter, de kooi
kantelt mee van liggend naar de sleephouding, en hij eindigt in de sleephouding.
Bewust kort gehouden (~0,9 s) zodat hij strafbaar is maar niet gratis. Tune via
de ticks in sprites.json.

## Keten en aansluitingen
```
drag (loop)  --start aanval-->  smash  --> recovery  --> drag (loop)
```
- smash-frame 0 = de sleephouding, gelijk aan drag. Walk -> aanval is naadloos.
- recovery laatste frame = de sleephouding. Herstel -> drag is naadloos.
- smash laatste frame (gebukt over kooi) sluit aan op recovery frame 0. Kleine
  rest wordt verbloemd door de stofwolk op impact.

## Kooi
De binnenkant van de kooi is donker (32,32,38) op 50 procent alpha, dus
doorschijnend: je ziet er vaag doorheen maar niet of er iets in zit. Pas de alpha
desgewenst aan per achtergrond.

## Hitbox
Per frame staat het zwaartepunt (centroid) in sprites.json, als startpunt voor de
collisionbox.
