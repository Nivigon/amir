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
De binnenkant van de kooi is puur zwart (0,0,0), licht opgevoerd in alpha (van zo'n
40-65% naar 55-80%) zodat je er nog vaag doorheen kijkt maar niet ziet wat erin zit.
De weef-variatie in de alpha blijft behouden.

## Kleuren: het bandietpalet
De speelframes in drag/, smash/ en recovery/ worden gemaakt uit de aangeleverde
frames in bron/ met `tools/kooiman_kleur.py`, zodat de kooiman in dezelfde kleuren
loopt als de bandiet (enemies/bandiet). Dezelfde aanpak als `tools/slang_kleur.py`
(`hertint`): de tekening zelf blijft staan, per kleurvlak worden alleen de tint en
de verzadiging vervangen en de helderheid over een nieuw bereik uitgesmeerd, dus de
inktlijnen, de plooien en de schaduwen blijven precies zoals ze getekend zijn.

- hoofddoek en gewaad: marineblauw (de bandietjas, #201f3c);
- broek: kaki-olijf (de bandietbroek, #534b39);
- de rode sjerp, de huid en de sandalen blijven ongemoeid (de zwarte contour, met
  lage verzadiging, valt vanzelf buiten de maskers);
- de kooivulling gaat naar zwart en wordt iets minder doorschijnend;
- het geel/tan van de tralies en de kooirand (restant van de oude gele kooi) wordt
  geneutraliseerd naar een taupe tint (hue 34-80, op hue gescheiden van de roodbruine
  huid en sandalen die lager in hue zitten, dus die blijven ongemoeid).

De bron (teal doek, blauw gewaad, groene broek, grijze kooivulling) staat in
bron/ en wordt door het spel nooit geladen. Verander je een bronframe, draai dan
`tools/kooiman_kleur.py` opnieuw, en daarna `tools/gen-klein.py` en
`tools/gen-offline-manifest.py`.

## Hitbox
Per frame staat het zwaartepunt (centroid) in sprites.json, als startpunt voor de
collisionbox.

## Stamp + vogel loslaten (aanvulling, 2026-10-18)

Drie extra sets voor de beweging waarbij de kooiman stampt en er een vogel uit de kooi
vliegt. Nog niet in de spelcode verwerkt (dat gebeurt apart); dit zijn de frames en de
metadata, klaar om op aan te sluiten. De sets staan in dezelfde `sprites.json` onder
`sets`, met de volgorde van gebeurtenissen in `events` en de placeringsgegevens van de
stofwolk in `dust`.

Net als drag/smash/recovery komen de speelframes uit `bron/<set>/` via
`tools/kooiman_kleur.py` (de bron is nog teal/blauw/groen; het script hertint naar het
bandietpalet en haalt de magenta-gloed eraf). De drie sets zijn aan dat script
toegevoegd. Verander je een bronframe, draai het dan opnieuw, en daarna `gen-klein.py` en
`gen-offline-manifest.py`.

| set | frames | soort | duur | wanneer |
|---|---|---|---|---|
| stomp | 13 | one-shot | 16 ticks (0,67 s) | start alleen vanaf **drag frame 0** (stomp_00 sluit daar exact op aan) |
| hatch | 19 | one-shot | 57 ticks (2,4 s) | direct na de stamp, speelt **tijdens de freeze** |
| stomp_out | 2 | one-shot | 2 ticks | na de freeze, korte uitloop |

### Verloop
1. De kooiman sleept (drag).
2. Hij heft zijn knie en stampt hard op de grond. `stomp` frame 8 (knie omhoog) blijft 4
   ticks staan: dat is de tell voor de speler dat er een vogel aankomt.
3. Op `stomp` frame 12 (impact): speel het kooislag-geluid (hetzelfde als bij de smash),
   spawn de stofwolk op de groundline onder de stampende voet, en **bevries de wereld**
   (Amir, vijanden, projectielen, physics, timers, input). Start dan `hatch`.
4. Tijdens de freeze lopen alleen door: `hatch`, de stofwolk en de vogel.
5. `hatch` frame 0 houdt het deurtje verstopt, daarna klapt het open en veert na. Op
   frame 9 staat het deurtje open (36 ticks = 1,5 s); hier spawnt de vogel. Frame 10 tot
   18 slaat het deurtje weer dicht. Aan het einde van frame 18: **unfreeze**, start
   `stomp_out`.
6. Na `stomp_out`: terug naar `drag`, maar start op **drag frame 11** (niet 0) en schuif
   de kooiman 24 px naar voren (x -24 bij links kijken, +24 bij rechts). Hij heeft tijdens
   de stamp een stapje gezet, zo loopt het naadloos door.

### De vogel
Spawnt op `hatch` frame 9, op canvaspunt (592, 464), net in het luikje. Hij vliegt schuin
omhoog weg van de kooi (richting 0.488, -0.873; x omdraaien bij spiegelen) en groeit uit de
kooi: van schaal ~0,12 naar normaal in de eerste 0,35 s. Hij beweegt al tijdens de freeze
(hij hoort bij het moment); zijn eigen AI (cirkelen, dive) begint pas bij de unfreeze.
Gebruik de `fly`-set uit `enemies/vogel/`.

### De stofwolk
De stamp gebruikt de stofwolk die al in het spel zit (de geleverde dust-frames zijn
bewust weggelaten). In `sprites.json` staan onder `dust` alleen de plaatsingsgegevens:
anker (280, 206) in de wolk op canvaspunt (343, 598), op de groundline onder de voet.

### Het deurgeluid
`sounds/kooideur.mp3` (het aangeleverde "openmetaldoor"): het metalen luikje dat openklapt
en dichtslaat. Af te spelen op het openklappen (begin `hatch`) en op het dichtslaan (rond
`hatch` frame 10).

### Let op: canvasbreedte
De nieuwe frames (stomp, hatch, stomp_out) zijn **728 x 648**, de bestaande sets (drag,
smash, recovery) zijn **726 x 648**. De `sprites.json` houdt `canvas` op 726 (wat het spel
nu voor de kooiman gebruikt). Twee pixels verschil in de breedte, dus bij het aansluiten
even nalopen of de nieuwe sets goed op het anker vallen, of de frames gelijktrekken naar
726.

### Preview
`preview/stomp_chain_preview.gif` toont de hele keten (stamp, stof, vogel, deur) zoals het
ingame moet ogen. Niet geladen door het spel.

### Bron
Clip `stapvooropen.mp4`, frames 1 tot 24 (frame 22 is het freezeframe). Het deurtje komt
uit `deur_dicht.mp4` (frames 1 tot 19), met de scharnieren op dezelfde rail van de kooi.
