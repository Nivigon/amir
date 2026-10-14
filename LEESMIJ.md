# Takelwiel met plateau (Amir, King of Africa)

Een houten tandwiel dat Amir met zijn speer kan slaan. Elke slag kantelt het wiel
een stuk, dat wikkelt twee touwen op of af, en daarmee zakt of stijgt een houten
plateau. Het plateau is op- en neer-verend (een soort luchtplatform naar een
volgend stuk grond).

Alle sprites zijn al transparant (magenta/roze weggesleuteld met `key_magenta.py`
uit het project). Niets bijsnijden of schalen nodig, behalve waar hieronder staat.

## Wat zit erin

```
wiel/           73 transparante frames (wiel_000..wiel_072), spritesheet, preview, uit jouw video
touw/           touw_tegel.png (naadloze tegel) + touw_vol.png (heel touw)
plateau/        plateau.png + plateau_links/midden/rechts.png (voor schalen)
spijkerknop/    spijkerknop.png (zwarte smeedkop over het touw op elk bevestigingspunt)
preview/        mechaniek_preview.gif (alles samen in de scene)
metadata.json   maten, hub, grondlijn, aanhechtpunten, snijlijnen, fps
```

Het wiel zelf en de spijkerknop kende je al. Hergebruik ze zoals ze hier staan.

## Het mechaniek

1. Amir slaat het rad met zijn speer.
2. Op de slag: er vliegen houtsplinters af. Gebruik dezelfde splinter-deeltjes als
   bij de doornbossen, die hebben we al. Geen nieuwe art nodig.
3. Tegelijk kantelt het rad een slag. Speel een stuk van de wiel-frames af en stop
   weer. In `metadata.json`:
   - `frames_per_kwartslag` = 18 (een kwart slag, zoals we het bespraken)
   - `frames_per_tand` = 6 (een tand, als je kleinere stapjes wilt)
   Het wiel is een volledige, naadloze omwenteling (73 frames, 12 tanden), dus je
   kiest zelf hoe groot een slag is.
4. Die draai wikkelt de touwen. Elke slag zakt of stijgt het plateau een stap. De
   staphoogte is een getal in de engine: koppel de plateauhoogte aan de draaistand
   van het rad, dan volgt de rest vanzelf.

## De twee touwen

- Het plateau hangt aan **twee aparte touwen**, een aan elk uiteinde. Met een touw in
  het midden zou het kantelen zodra Amir op de rand staat. Aanhechtpunten staan in
  `metadata.json` (`aanhechtpunt_links` / `aanhechtpunt_rechts`).
- De touwen komen van **boven het scherm** uit twee aparte verborgen katrollen, en
  lopen naar boven **uit elkaar** (niet samen in een punt). Zo lees je twee losse
  touwen in plaats van een V.
- Waterpas houden = beide touwen gelijk op- en afwikkelen. Wil je het juist laten
  kantelen (bijvoorbeeld een valstrik), wikkel ze dan ongelijk. Dat is gratis.
- De aanhechting bij het rad verdwijnt **achter het wiel**: teken het touw in de laag
  achter het wiel, dan hoeft niets precies uit te lijnen.
- Op elk aanhechtpunt van het plateau zet je de **spijkerknop** over het touw. Rond,
  dus de richting van het touw maakt niet uit.

## Touw tekenen

- `touw_tegel.png` is naadloos: herhaal hem langs de lengte voor elk touw, elke hoek,
  elke lengte. Geen zichtbare naden.
- Laat de draad meebewegen door de tegel langs de lengte te **scrollen**. Koppel de
  scrollsnelheid aan de draaistand van het rad, dan loopt het altijd synchroon.
- Tegelbreedte en pitch staan in `metadata.json` (voor het scrollen per tand).

## Plateau groter of kleiner maken (in de builder)

Het plateau is een 9-slice (horizontaal rekken):

- Gebruik `plateau_links.png`, `plateau_midden.png`, `plateau_rechts.png`, of
  `plateau.png` met `slice_left` / `slice_right` uit `metadata.json`.
- Rek alleen het **midden**. De uiteindes (met de steunen en de aanhechtpunten)
  blijven vast, zodat de touwen altijd op de steunen aangrijpen.

## Schaal

In de preview staat het wiel op ongeveer 185 px hoog en het plateau op 190 px breed,
als referentie voor spelschaal. Pas aan naar wens, de verhoudingen kloppen onderling.
De grondlijn van het wiel staat in `metadata.json` (`grondlijn`).
