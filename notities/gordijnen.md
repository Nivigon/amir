# Deurgordijnen in de stad

Status: **klaargezet, nog niet ingebouwd.** De plaatjes, het knipscript en een werkende proef staan in de repo;
het inbouwen in `amir-king-of-africa.html` is de volgende stap. Hoort bij A3 (kleur uit doeken) en V2 (kleine
beweging) in `notities/stad-verbeteren.md`.

## Wat het is

Een geweven katoenen doek in twee banen aan een ruwe houten stok, in het deurgat van een gevel in plaats van de
houten deur. De stok staat stil, de banen golven zacht in de wind, met af en toe een vlaag. In rust vallen de
twee banen over elkaar (dicht); bij een vlaag wijken ze onderaan even uiteen. Binnen hangt hetzelfde doek in de
deur naar buiten, gespiegeld (je ziet de achterkant), met donker erachter.

Voorbeelden uit de proef (het echte spel, sandbox): `notities/proeven/gordijn_straat.jpg` (deuren, een open deur
en gordijnen door elkaar), `gordijn_binnen_rust.jpg` en `gordijn_binnen_vlaag.jpg`.

## Bestanden

- `design/stad/gordijn/<naam>.png`, zeven stuks, ongeveer 520 x 830, alfa, stok bovenaan, rafels onderaan:
  - effen: `geel`, `olijf`, `terracotta`
  - patroon: `indigo_streep`, `adire` (indigo met witte cirkels), `bogolan` (crème met bruine tekens), `rood_oker`
    (de banen van de kraamdoek)
- `design/stad/gordijn/bron/`: de Grok-platen (drie gordijnen per plaat op wit) en `gordijn_referentie.png`
  (de stijlreferentie die Grok meekreeg: de kraamdoek en het deurgat van `gevel.png`).
- `tools/gordijn_knip.py`: maakt de zeven PNG's uit de platen (wit weg, ook de witte stukjes onder de stok,
  losknippen, het middenstuk 1,14 keer langer zodat het de verhouding van het deurgat krijgt). Daarna
  `gen-klein.py` en `gen-offline-manifest.py`.
- `notities/proeven/gordijn_proef.js`: de proef, als script in het draaiende spel geplakt. Geen eindcode, wel
  de rekenregels en maten die werken.

## Maten (uit de proef)

- Buiten tekent de proef het gordijn in de ruimte van het deur-canvas (`DEUR.canvas`, 351 x 448, de grondlijn
  `DEUR.grond` 446), precies zoals `stadDeurPlaatTeken` de houten deur tekent. Het deurgat ligt in dat canvas op
  x 119, y 30, 214 x 413 (`STAD_DEUR.gat` min `plaatX` 247, en de voet 1505 op 446).
- De stok is 236 breed (iets breder dan het gat, de uiteinden vallen op de posten), het midden op x 226, de
  bovenkant op y 32: net onder de latei, die er daarna overheen komt. Het doek hangt dan tot ongeveer 0,9 van het
  gat; onderaan blijft een strookje donker.
- Een warme tint over het doek (multiply `rgba(214,170,128,0.45)`), net als `STAD_DEUR.warm` bij het hout; zonder
  die tint stak vooral de bogolan te wit af tegen de leem.
- Binnen: `binnen/deur_recht.png` (772 x 892) heeft de opening op x 155 tot 615, y 218 tot 820. De stok 480 breed,
  midden 386, bovenkant 206 (valt samen met de latei), het doek 0,8 keer platter zodat het tot net boven de vloer
  hangt. Eerst de opening donker vullen (verloop `rgba(14,8,6,0.97)` naar `rgba(26,16,12,0.92)`), dan het doek
  gespiegeld erover. Tom wil het **donker** achter het doek, geen daglicht.

## De wind (uit de proef)

- `vlaag = 0.55 + 0.25 sin(0.45 t + ph) + 0.35 max(0, sin(0.23 t + ph/2))^3`, met `ph = gevel-index x 1,7`, zodat
  niet alle deuren tegelijk bewegen.
- Het doek in rijen van 2 px; rij `y` schuift opzij met `A k (golf + 0,9)`, `A = 20 x vlaag` (in canvas-px op
  stokbreedte 236), `k = ((y - stok) / (h - stok))^1,35` (bovenaan niets, onderaan het meest),
  `golf = 0,65 sin(1,8 t + 0,016 y + ph) + 0,35 sin(3,3 t + 0,045 y + 2 ph)`. Elke baan een eigen fase (+1,3 voor
  de rechter). De onderkant tilt iets op (`lift = 1 - 0,07 vlaag k`).
- Bewegende plooien: een horizontaal verloop van licht en donker, `source-atop` over het doek, sterkte mee met
  de vlaag.
- Dicht in rust: elke baan wordt naar het midden breder getrokken met de halve spleet plus 3 px (de spleet
  gemeten uit de alfa rond het midden), de linker over de rechter; de buitenranden blijven staan. Bij een vlaag
  (`open = clamp((vlaag - 0,85) / 0,35)`) neemt dat onderaan af, zodat de banen even uiteen gaan.
- De proef tekent elk beeld opnieuw in een eigen canvas per deur. In het spel: alleen voor deuren in beeld
  (`zichtVak`), en het mag op een lagere rate (15 fps is genoeg) of met grotere rijen op een telefoon.

## Waar wel, waar niet (Toms keuze na de proef)

- Ongeveer een op de drie deuropeningen, vooral bij de gewone gevel en het pilarenhuis. Het reliefhuis en het
  koopmanshuis (rijke huizen met een versierd kozijn) houden de houten deur.
- Vooral de effen kleuren en indigo; de bogolan en de rood-okerstrepen spaarzaam, want die trekken het meest
  aandacht (de bogolan is de lichtste).
- Vast per huis (seed en index), net als `stadDeurVanzelfOpen`, zodat het niet flikkert.
- Komt er een vijand uit een deur met een gordijn (`deur` in een spawn), dan gaat het doek opzij in plaats van
  dat er een deur openzwaait: de banen wijken uiteen (een sterke `open`), de vijand stapt erdoor, het doek valt
  terug en zwaait na. Dat is zijn tell, net als het opengaan van de deur.
