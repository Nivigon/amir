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

## Sluipen zonder speer
Af, 28 frames (`sluip_ns_plaat.png`, `sluip_ns.gif`).
- **Diepte (zelfde punt als de ren)**: in het origineel is het verre been in een deel van de frames roodbruin/donker
  (o.a. 14, 17, 18, 27); in Mkuki zijn beide benen even donker door de zwarte broek, ook na de DEPTH-zin in de prompt.
  Kan met dezelfde aanpak als `wissel.py` (verre been en arm donkerder), maar dan met de verre kant per frame uit het
  origineel gemeten in plaats van de vaste indeling 1-6/7-12 van de ren.

## Voor- en achterkant van de ledematen (Tom, 21-11 17:51)
Tom zag in de rencyclus dat Amir steeds met dezelfde kant naar voren rent: niet allebei de kanten komen vooraan.
In de originelen zit de afwisseling vooral in de schaduw: het VERRE been en de verre arm zijn donkerder (roodbruine voet,
donkerder paars). Grok tekende die in de eerste sets niet, dus in Mkuki zijn beide benen even licht en lijken de twee
helften van een cyclus op elkaar. Gezien in ren_ns 4 en 10 en in sluipen 01; geldt waarschijnlijk ook voor ren_sp en
de andere sets van voor 17:51.
- Vanaf sluipen_07 staat in de prompts een DEPTH-zin ("keep exactly which leg and arm are NEAR and FAR ... far limbs
  darker in shadow, do NOT swap left and right"); sluipen_07 heeft het verre been daarna wel donker.
- De rencyclus wordt in een andere chat gecorrigeerd (Tom, 17:57). Deze run let alleen op de nieuwe frames: bij elke
  vergelijking kijken of het verre been en de verre arm achter en donker staan, zoals in het origineel.

## Rol zonder speer
- **Rol 25 (IoU 0,62)**: geknield met een hand naar de grond. In het origineel steekt de vacht ver achter de rug uit, wat
  de IoU drukt; de pose klopt grof, maar de hand reikt minder ver naar voren dan in het origineel. Een tweede poging met
  de hand uitgeschreven (f48b710c) was slechter (0,58).
- **Rol 15 en 23 (0,65)**: op de grens, pose volgt het origineel; 23 mist vooral de vacht achter de rug.
- **Rol 14-21**: de ondersteboven en rug-frames zijn gemaakt met een ORIENTATION-zin in de prompt. Ze volgen de omtrek,
  maar de handen en vuisten liggen niet overal precies waar ze in het origineel liggen (bv. 17 en 18 de vuisten hoger).
- Verre been en verre arm staan in alle frames achter, maar beide benen zijn even donker door de broek (zelfde als bij de
  andere sets).

## Speerstoot
- Frame 2-8 staan met de rug naar de camera (zoals het origineel), gemaakt met een FACING-zin. De IoU is lager
  (0,56-0,65) omdat de vacht in het origineel de omtrek groter maakt en bij 5 de voorste onderarm met de speer is
  weggehaald; de houding (draaiing, armen, benen) is per frame nagekeken.
- Frame 4 leunt iets minder voorover dan het origineel; frame 9 staat iets rechter.

## Speerworp
- Draaiing per frame nagekeken: 00-07 borst naar de camera, 08-09 driekwart naar rechts, 10-17 profiel/rug naar de camera,
  18 profiel, 19 driekwart. Frames waar Grok hem verkeerd draaide zijn afgekeurd (10, 14, 18).
- 08: de originele vuist om de schacht is niet geplakt (Grok's werkhand ligt er net naast); de speer loopt langs zijn
  eigen vuist.
- 12: voorste hand is een vuist in plaats van open; 15: achterarm te gestrekt; 16 en 17: voorste arm reikt minder ver.
- 00-02: het hoofd uit het origineel had resten van de speer; daarom overal het hoofd van Grok (--geenhoofd).

## Lage zwaai
- Grok laat de armen vaak korter of hoger dan het origineel: 8 (voorste arm hoort horizontaal naar links, Grok zette beide
  handen op de grond), 10 (armen reiken minder ver naar rechts), 6 (linkerarm korter).
- 13 (zijtrap): het been trapt hoger en het standbeen staat rechter dan het origineel; met de hand geplaatst. Even kijken of
  de overgang 12 naar 13 niet springt.
- 9: romp iets rechter dan het origineel (die ligt bijna plat voorover).
- 3, 5, 9: de speer draait mee en is op de plaat soms een korte schuine streep; de draaiende speerframes blijven handwerk.

## Combo
- 02 (armen recht omhoog): Grok zette de voeten smaller dan het origineel.
- 03: Grok tekende een stompje stok tussen de vuisten; dat valt achter de speer, maar even kijken.
- 07 en 08: de bovenste vuist zit wat lager en dichter bij het hoofd dan in het origineel.
- 12-14: de achterste vuist hangt bij de heup, in het origineel houdt die hand de speer schuin omlaag; met de speer erop
  klopt het, zonder speer ziet de arm er wat los uit.

## Stofsweep
- 07 en 08: Grok houdt hem hoger dan het origineel (dat zit diep op de hurken); IoU 0,67 en 0,71.
- 10-13: in het origineel ligt de speer schuin achter zijn rug en zie je de vuisten niet; Grok zet de vuisten zichtbaar
  voor het gezicht. Met de speer erop even kijken of dat klopt.

## Rol/worp
- 1: afgekeurd door Tom (rechtop, handen naar voren, voeten naast elkaar) en opnieuw gedaan; nu vuist bij de enkels en
  voeten verspringend.
- 5: hoogte klopt, voeten staan dichter bij elkaar dan in het origineel.
- 12: romp rechter en borst meer naar ons dan het origineel (twee pogingen gaven hetzelfde).
- 15-23 en 29-33: per groep een en hetzelfde Grok-beeld (het origineel houdt daar de houding vast); bij 15-23 zit de
  achterste vuist iets lager dan in het origineel.
- 24: voorste arm lager dan het origineel. 26: Grok-beeld van 24/25, het origineel buigt al naar links.
- 27: arm klopt, maar de borst staat nog naar ons waar het origineel al met de rug draait.
