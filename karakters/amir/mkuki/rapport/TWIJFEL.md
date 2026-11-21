# Mkuki: twijfelgevallen en open punten (nachtrun 21-11-2026)

## Gestopt na de idle en een deel van de ren
Rond 04:00 hing Grok in Chrome bij bijna elke stap: de Imagine-pagina laadde pas na 60-90 s, en klikken en
scripts liepen tegen de time-out van 30-45 s aan. Dat is de stopregel uit de opdracht. Daarnaast ging veel tijd
naar het opnieuw maken van de idle met het goede doek (zie LOG.md, 03:00).

Af: **idle** (idle_ns, idle_sp, idle_sp/00-19): Mkuki-kleuren, zonekaarten, vuistlaag, speerplaatsing, plaat en GIF.
Ochtend (09:30, Tom: "ga verder"): de **ren met speer** is af (12 frames), zie `rapport/ren_sp_plaat.png` en `ren_sp.gif`.

## Twijfel
- **idle_sp_10 en 12**: Grok zette eerst de verre hand op de heup; opnieuw gedaan met drie ankers, nu goed, maar het
  hoofd kijkt in Grok iets omhoog. Het hoofd komt uit het origineel, dus in het spelbeeld zie je dat niet. Graag even kijken.
- **ren_sp_4 en ren_sp_10 (niet goed)**: de gekruiste benen tekent Grok steeds als een wandelpas (vier keer geprobeerd, ook
  met de nieuwe aanpak). Nu een noodgreep: bovenlijf en doek van Grok, benen uit het origineel met de broek omgekleurd.
  Ook frame 10 los met een prompt over de kruisende knie: weer een wandelpas (post `a233bda1-...`). In de noodversie
  is de voorste vuist rafelig en zijn de voeten rood-paars. Voorstel: deze twee met de hand (of via de rig) aankleden,
  of in het spel overslaan (de loop is 12 frames; 4 en 10 zijn de kruismomenten).
- **ren_sp_3**: het onderbeen achter de speer is iets afgeknipt (schacht liep over het been).
- **ren_sp_3**: bovenlijf staat iets rechter dan het origineel (IoU 0,72).
- De groene band met gesp: Grok tekent hem donkergroen (V 0,35); de zonekaart pakt hem, maar de gesp zelf zit soms
  in de band-zone en soms niet.

## Voeten
In de ren laat ik de voeten van Grok staan (strak); terugzetten uit het origineel gaf rafelige, verkleurde voeten.
In de idle komen de voeten nog uit het origineel.

## Draaiende speerframes
Nog niet aan toegekomen (rol met speer, draaislag, rol-worp).
