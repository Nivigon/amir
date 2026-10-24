# Meelman - vijand voor Amir, King of Africa

Een korte, gedrongen bandiet met een buikje en een mondmasker die meelzakken naar
Amir gooit. Hij is vooral gevaarlijk op afstand (zakken gooien vanaf een verhoging);
in close combat slaat hij simpel, net als de kooiman (de niet-duel vorm).

Aanzicht: driekwart, kijkt naar links (spiegel in code voor de andere richting).
Levens: 3.

## Mapstructuur

```
enemies/meelman/
  idle/        1 frame   (loop)      staande 3/4 idle, armen over elkaar
  opricht/     30 frames (one-shot)  van hurk naar staande idle, na de worp
  worp/        43 frames (one-shot)  zak-zwaai, dubbelt als melee-slag
  ren/         23 frames (loop)      gedrongen looppas
  drag/        18 frames (loop)      sleept een zak, gebukt
  metadata.json
items/meelzak/
  zak_projectiel.png   de gegooide zak (los object, engine animeert)
  zak_vol.png          staande zak, vol/rechtop   (stapel-variant)
  zak_breed.png        staande zak, laag en breed (stapel-variant)
  zak_smal.png         staande zak, smaller/hoger (stapel-variant)
```

De opricht- en worp-set hebben bewust geen sprite sheet: te veel frames voor een
bruikbare strip. Gebruik daar de losse PNG's.

## Canvas en grondlijn

Alle animatiesets staan op hetzelfde canvas en dezelfde grondlijn, zodat ze naadloos
in elkaar overgaan:

- canvas: 744 x 469
- grondlijn (voeten): y = 435
- anker-x (voeten, horizontaal midden van de man): x = 259

De man is op gelijke schaal in alle sets (gematcht op kophoogte). De zak in de worp-
en drag-set zit in het sprite; de losse projectiel-zak staat apart in items/.

## De sets

Frames en fps zijn startpunten, stel ze gerust bij in de engine.

**idle** (loop, 1 frame) - staande rusthouding, driekwart, armen over elkaar, harde
blik. Nog een enkel frame; een echte ademhaling-loop kan later.

**opricht** (one-shot, 30 frames, ~38 fps) - komt na de worp van de hurk omhoog naar
de idle. Oprichten: frames 0-18. Settelen in de idle: 18-29. Het eindframe is exact
de idle-pose, dus idle sluit er naadloos op aan.

**worp** (one-shot, 43 frames, ~27 fps) - de zak-zwaai van laag-achter, over het hoofd,
naar voren. Dit sprite dubbelt als de melee-slag.
- wind-up (tell): frames 0-26, sleept de zak laag naar achter en tilt op
- zak boven het hoofd: frame 27
- raak-/release-venster: frames 27-41, de zak veegt omhoog en naar voren door de
  ruimte voor hem
- release-frame voor de worp: rond frame 30 (zak hoog en vooruit); vanaf hier kun je
  de zak loskoppelen en als los projectiel laten vliegen (zie hieronder)
- follow-through / kwetsbaar herstel: frames 41-42, zak komt laag voor hem neer, hij
  staat overstrekt open

**ren** (loop, 23 frames, ~38 fps) - gedrongen, gehaaste looppas. Lopen op de plek,
de engine verplaatst hem.

**drag** (loop, 18 frames, ~16 fps) - sleept een zak mee, gebukt, zwaar. Lopen op de
plek, de engine verplaatst hem.

## De gegooide zak (projectiel)

`items/meelzak/zak_projectiel.png` is een los object. De beweging doet de engine, geen
frame-animatie nodig:

- vliegt in een RECHTE lijn naar Amir (geen boog), rekt iets uit door de snelheid
- dikt in (squash) bij de inslag en ketst daarna terug + valt op de grond
- het doel (Amir) krijgt knockback: schuift bij de inslag de andere kant op
- thema: het is meel, dus bij impact kan de zak uiteenspatten in een witte meelwolk
  (nog te maken; die wolk kan Amir ook even hinderen/staggeren)

De drie staande zakken (vol / breed / smal) zijn vorm-varianten om naast elkaar als
stapel neer te zetten, en om op te laten pakken of neer te zetten.

## Idee voor een testlevel

- De meelman staat op een verhoging en gooit een zak naar Amir. De zak ketst af zoals
  hierboven beschreven, Amir moet eronderuit (ontwijken).
- Daarna pakt de meelman een nieuwe zak (uit een stapeltje naast hem).
- Amir kan omhoog klimmen via een paar plateautjes terwijl de meelman een nieuwe zak
  haalt, en zo bij hem komen.
- Boven aangekomen gaat Amir het gevecht aan. In close combat slaat de meelman simpel
  met de zak (de worp-set dient als melee-slag, de niet-duel vorm zoals de kooiman).
- De meelman heeft 3 levens.

(Oppakken-animatie is bewust overgeslagen voor nu. De opricht achteruit afgespeeld kan
later als oppakken dienen.)

## Aandachtspunten

- Bronresolutie is beperkt (Grok-downloadlimiet); de meelman is netto klein in de
  clips. Voor scherpere assets later groter in het frame genereren.
- fps per set zijn richtwaarden; de worp mag als zware, getelegrafeerde aanval gerust
  wat trager.
- De meelwolk bij inslag is er nog niet; nu kan de engine een simpele stofwolk doen.
