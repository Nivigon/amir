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

## Rol met speer (21-11, middag)
- **Draaiende speerframes: rol 16 tot 22.** De speer draait hier mee met de rol (16 en 18 bijna rechtop, 19-22 schuin
  over het lijf). Plaatsing staat in `plaatsing.json` met de lengte van het origineel; in 16 en 18 is de lengte uit de
  setmediaan aangevuld (de punt of kont viel achter het lijf), dus graag nakijken of de speer daar niet te lang is.
  Een korter wordende speer (naar je toe gedraaid) zie ik in deze set niet; de originele speer blijft even lang.
- **Rol 11 tot 28: het hoofd is van Grok**, niet uit het origineel (in deze poses pakte het terugzetten vachtresten en
  speerstukken mee). Gezicht kan iets afwijken van de rest van de sets.
- **Rol 3 en 19: geen vuistlaag** op een (3) of alle (19) handpunten: Grok tekende de hand op een andere plek, dus de
  speer loopt daar niet door een vuist heen. Handwerk: vuist met de hand zetten of de speer daar achter de hand leggen.
- **Rol 17 en 18**: armen naar links gezet met een eigen prompt (`mk_rol7`); de vuisten liggen niet precies op de
  originele handpunten. Even kijken in de GIF.
- **Rol 22**: IoU 0,64, de benen iets anders dan het origineel.

## Trap met speer
Geen twijfel; twee losse poses.

## Ren zonder speer
Af, 12 frames (`ren_ns_plaat.png`, `ren_ns.gif`).
- **ren_ns_10**: IoU 0,64, derde poging met de pose uitgeschreven in de prompt. Volgt de omtrek, maar even kijken in de GIF.

## Springen zonder speer
Af, 7 frames (`jump_ns_plaat.png`, `jump_ns.gif`).
- **jump 2 (afzet)**: hoofd van Grok in plaats van het origineel (dubbel gezicht anders); even naast de rest leggen.
- **jump 3 en 4**: IoU 0,66 en 0,64, pose wel goed.

## Bukken zonder speer
Af, 12 frames (`buk_ns_plaat.png`, `buk_ns.gif`). Geen twijfel.

## Sluipen zonder speer (onaf)
00 tot en met 02 af (`sluip_ns_onaf_plaat.png`). Gestopt op een Grok-limiet.

## Voor- en achterkant van de ledematen (Tom, 21-11 17:51)
Tom zag in de rencyclus dat Amir steeds met dezelfde kant naar voren rent: niet allebei de kanten komen vooraan.
In de originelen zit de afwisseling vooral in de schaduw: het VERRE been en de verre arm zijn donkerder (roodbruine voet,
donkerder paars). Grok tekende die in de eerste sets niet, dus in Mkuki zijn beide benen even licht en lijken de twee
helften van een cyclus op elkaar. Gezien in ren_ns 4 en 10 en in sluipen 01; geldt waarschijnlijk ook voor ren_sp en
de andere sets van voor 17:51.
- Vanaf sluipen_07 staat in de prompts een DEPTH-zin ("keep exactly which leg and arm are NEAR and FAR ... far limbs
  darker in shadow, do NOT swap left and right"); sluipen_07 heeft het verre been daarna wel donker.
- Nog te doen: een schaduwstap voor de bestaande frames (het verre been en de verre arm uit het origineel als masker
  donkerder maken). Een eerste proef met een drempel op lichtheid pakte ook de huid mee, dus per zone (broek, huid)
  apart meten. Of de betreffende frames opnieuw door Grok met de DEPTH-zin.
