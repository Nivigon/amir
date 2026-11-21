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
- In de kruisframes (4 en 10) is de splitsing grof; de benen overlappen daar en het verschil valt weinig op.

Draaien (vanuit `karakters/amir`): `python3 ../../tools/mkuki/wissel.py ren_ns <uitmap>` (en `ren_sp`), op de
ONGECORRIGEERDE frames. Niet twee keer over dezelfde frames halen.

## Update 21-11 ~19:00: armen via Grok (ren zonder speer)
- ren_ns 7-12 zijn opnieuw door Grok getekend (image-to-image vanaf de oude Mkuki-frames, figuur 760 px op magenta
  1650x1100): de voorste arm komt van achter de borst (ver, donker), de achterste arm met de koperen band ligt voor
  het lijf (nabij). Posts: 7 e502a156, 8 79d47a46 (eerste poging 4f9445cd: lichte huid op de achterarm, afgekeurd),
  9 583ce35e, 10 e88b3488, 11 8ef5a85b (eerste poging 0aecb27b: lichte huid, afgekeurd), 12 d12ef567.
  IoU met het oude frame 0,83 tot 0,96. Verwerkt met `tools/mkuki/wissel_grok_verwerk.py` (tegels beeld-x 400-1350,
  y 100-750 en 600-1150; netjes verkleinen, uitlijnen op IoU; zonekaart per pixel uit kleur en plek in het oude frame).
- ren_ns 1-6 houden de schaduwcorrectie (die klopt daar al: voorarm nabij, achterarm ver).
- Prompt die werkte (de huidzin erbij is nodig, anders werd de achterarm twee keer zandkleurig):
  "... Only his ARMS change in depth. ... The arm that reaches FORWARD to the LEFT of the picture is his FAR arm: its
  shoulder is HIDDEN behind his chest, the upper arm comes out from BEHIND the front edge of his chest, and the whole
  arm is darker, in shadow. The arm that swings BACK to the RIGHT of the picture is his NEAR arm: its shoulder with the
  copper arm band sits on the side of his body nearest the viewer, fully visible, and the upper arm hangs in FRONT of
  his torso, normally lit. The skin of BOTH arms and hands is the same dark brown as his chest and face, never light,
  never sand-coloured. ..."
- Een prompt over benen en armen tegelijk (eerste poging, c313244c) veranderde bijna niets.
- ren_sp: GEEN armwissel. De speer zit altijd in de voorste hand, dus die arm is in elk frame de nabije arm; anders
  wisselt de speer van hand. Alleen de benen wisselen, de achterarm is in alle frames ver (donker). Opnieuw gedraaid
  vanaf de originele frames met de aangepaste `wissel.py`.
- De schort over het voorste dijbeen is geen fout: een lendendoek hangt voor het lijf, over welk been er ook voor zit.
- Al aanwezig in de productie (niet door deze stap): donkere vlekken bij de voeten in ren_sp 4 en 10.
