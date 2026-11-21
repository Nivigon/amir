# Ren: nabij en ver wisselen (gecorrigeerd in een andere chat, 21-11-2026 ~18:30)

Tom zag dat Mkuki in de rencyclus steeds met dezelfde kant naar voren rent. Dit is het open punt
"Voor- en achterkant van de ledematen" uit `rapport/TWIJFEL.md`, voor de ren opgelost in een aparte chat
(niet de productie-chat), om niet in LOG.md en TWIJFEL.md door elkaar te schrijven.

## Wat er aan de hand was
De ORIGINELE ren zelf is twee keer dezelfde halve cyclus: frame 1 t/m 6 en 7 t/m 12 hebben vrijwel hetzelfde silhouet
(gemiddeld verschil 3 tot 4 tegen 5 tot 8 tussen buren). In het origineel valt dat weg door de schaduw en de wijde broek;
in Mkuki (strakke pijpen, armbanden, beide benen even licht) zie je het meteen.

## Wat er gedaan is (`tools/mkuki/wissel.py`, `tools/mkuki/ledematen.py`)
- Per frame het silhouet gesplitst in voorbeen, achterbeen, voorarm, achterarm en romp (geodetische afstand vanaf voeten,
  polsbanden en borst; op de broekzone alleen de twee benen).
- Frame 1-6: ver = voorbeen + achterarm (donkerder, x0,70), nabij iets lichter (x1,06).
- Frame 7-12: omgekeerd: ver = achterbeen + voorarm.
- ren_sp: de voorarm (speerhand, met losse vuistlaag) blijft ongemoeid; alleen benen en achterarm.
- Zonekaarten ongewijzigd (alleen lichtheid veranderd).
- Voor/na: `rapport/ren_ns_wissel.gif`, `rapport/ren_sp_wissel.gif` (links oud, rechts nieuw) en de `_plaat.png`'s.
- Nog altijd zichtbaar: de schort valt in alle frames over hetzelfde dijbeen. Het dijbeen uit het origineel voor de schort
  plakken is geprobeerd maar gaf rafelige randen; dat vraagt nieuwe Grok-frames voor 7-12 (met de DEPTH-zin).
- In de kruisframes (4 en 10) is de splitsing grof; de benen overlappen daar en het verschil valt weinig op.

Draaien (vanuit `karakters/amir`): `python3 ../../tools/mkuki/wissel.py ren_ns <uitmap>` (en `ren_sp`), op de
ONGECORRIGEERDE frames. Niet twee keer over dezelfde frames halen.
