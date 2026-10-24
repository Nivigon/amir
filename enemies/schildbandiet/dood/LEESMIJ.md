# Schildbandiet: dood

Let op: deze frames zijn bewerkt door `tools/schildbandiet_dood.py` (de bron staat in commit 54bca24, 39
frames). De speer is er vanaf frame 07 uit (het spel laat zijn eigen speer vallen), de twee bron-frames
waarin hij voor de tuniek langs viel zijn eruit (nu 37 frames, dood_00..36), en vanaf de landing staat het
lijf omlaag op de grondlijn (per frame in `dood.json`, `omlaag`). Hieronder de oorspronkelijke uitleg.

39 frames, RGBA, canvas 544 x 560. Kijkrichting links. One-shot, geen loop.
Elk frame 2 ticks op 24 fps (dus 12 fps), totaal 3,25 s. Ticks staan per frame in `dood.json`.

## Canvas (hard)
Teken elk frame als het HELE canvas van 544 x 560, op dezelfde schermschaal als de andere
schildbandiet-sets, met de grondlijn op dezelfde scherm-y. Niet bijsnijden, niet inzoomen op
de bounding box van een frame.

- Grondlijn (voeten): y 481.
- De speer ligt iets voor hem (dichter bij de camera) en reikt tot y 511. Dat is bewust.

## Keten
- Start na de laatste treffer zonder schild (schild is dan al weg).
- Speel 00 tot en met 38 een keer af.
- Daarna dood_38 vasthouden als lijk (ligt tot op de pixel stil).
- Witte flits plus een paar frames hitstop op frame 00 verkopen de klap.

## Fasering
| frames | wat |
|---|---|
| 00-08 | klap, komt uit zijn guard omhoog |
| 09-12 | speer glipt uit zijn hand en valt plat naast zijn voeten |
| 13-23 | staat wankelend, leunt steeds verder achterover |
| 24-32 | valt achterover op zijn rug |
| 33-38 | ligt na, komt tot rust |
| 38 | lijkframe |

De speer zit in deze frames (geen losse laag). Hij valt naar rechts (weg van de speler);
liggend loopt hij van x 56 tot 511.
