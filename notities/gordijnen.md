# Deurgordijnen in de stad

Status: **ingebouwd** in `amir-king-of-africa.html`, onder de kop `// ---- gordijnen: ... ----` (na de deuren).
Nog geen level heeft het aan; te zien in de sandbox (De stad, **Gordijnen** en **Wind**) en in de Maker (gevel,
**Deur**). Hoort bij A3 (kleur uit doeken) en V2 (kleine beweging) in `notities/stad-verbeteren.md`.

## Zo zit het in de code

- `GORDIJN`: de namen, de gewichten, de kans per huistype, de maten buiten (`straat`) en binnen (`binnen`), de
  windsterkte, de rate en rijhoogte (laptop en telefoon) en de tell (`opzij`). `GORDIJN.wind`: 0 uit, 1 zacht, 2 vlagen.
- `stadGordijnVan(st, gi)` / `stadGordijn(gi)`: welk doek gevel `gi` heeft, of null (dan de houten deur). Het veld
  `gordijn` per gevel (een naam, of `false`) gaat voor; zonder veld alleen als de stad `gordijnen: true` heeft, dan
  een vaste keuze uit seed en index (`gordijnHash`). Zo verandert er in een bestaand level niets.
- `gordijnLaad(st)`, vanuit `stadSoortLaad`: laadt alleen de doeken die de stad echt gebruikt.
- `gordijnBron(n, w)`: het doek op stokbreedte, warm getint, met de gemeten spleet; een keer per naam en maat.
- `gordijnVlaag`, `gordijnDoek(n, gi, o, sleutel, st)`: de wind en het wapperende doek in een eigen canvas per deur,
  hooguit 30 keer per seconde opnieuw (15 op een telefoon, `camTelefoon`, met rijen van 4 in plaats van 2 px).
  Hangt het doek stil (wind en langslopen onder `GORDIJN.rustTot`, de tell niet bezig), dan maar `GORDIJN.fpsRust` (8)
  keer per seconde: het beweegt dan minder dan een pixel. Een nieuw doek is een paar honderd reepjes (binnen het dubbele),
  en met twee of drie deuren in beeld gaf dat lag op een laptop in De Gouden Poort en De Rivierstad.
- `stadGordijnTeken`: in `stadTeken`, op de straat (verdieping 0) in plaats van `stadDeurPlaatTeken`; latei en
  schaduw zoals bij de deur. Buiten beeld (`zichtVak`) rekent hij het doek niet opnieuw. Op een verdieping blijft
  het de houten deur.
- De tell: in `stadDeurUpdate` krijgt een deur met een gordijn `st.gordijn`; zijn vijanden wachten
  `GORDIJN.opzij.op + 0,15` s in plaats van de 20 frames van de deur, en `stadGordijnStap` schuift de banen opzij
  zolang er nog iemand uit moet of net uitstapt (`uitT`), laat ze dan terugvallen en zet het nazwaaien aan. Geen
  deurklap en geen schok.
- `binnenGordijnTeken`: in `binnenAchter`, na `binnen/deur_recht.png`: het donker en het doek van die gevel, gespiegeld.
- Sandbox: `sbGordijnen` (een dichte straat met alle zeven doeken, houten deuren en een open deur, het eerste huis met
  een binnenkant; **Uit de deur** stapt daar door het gordijn) en de knop Wind (`sbgordwind`).
- Maker: bij een gevel de keuze **Deur** (`MK_GORDIJNEN`, `mkgordijn`), die als `gordijn` in de gevel gaat.

## Wat het is

Een geweven katoenen doek in twee banen aan een ruwe houten stok, in het deurgat van een gevel in plaats van de
houten deur. De stok staat stil, de banen wapperen licht in de wind, met af en toe een vlaag. In rust vallen de
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
  de rekenregels en maten die werken (die staan nu in `GORDIJN` en `gordijnDoek`).
- Er is geen kleine versie: `gen-klein.py` neemt de map niet mee, het spel laadt de grote (zoals bij de tonnen).

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

## De wind en het langslopen

Eerst bewoog het doek altijd (een ademende wind van 0,3 tot 0,8 met vlagen erbovenop); Tom vond dat te constant.
Nu hangt het tussen de vlagen bijna stil, en beweegt het alleen echt bij een vlaag of als Amir erlangs loopt.

- `gordijnVlaag(t, ph, wx)`: in rust `GORDIJN.rust` (0,06, met een heel klein beetje adem), dan zo nu en dan een vlaag
  van een paar seconden (twee reeksen, `sin(0,31 u)^8` en `sin(0,17 u + 1)^10`, ongeveer een kwart van de tijd), elke keer
  anders sterk, tot ongeveer 1,2. `u = t + wx / GORDIJN.vlaagV`: een vlaag komt bij de volgende deur iets later aan, zodat
  hij door de straat trekt. Wind **zacht** (sandbox) geeft alleen een rustige `GORDIJN.rustZacht` zonder vlagen.
- `gordijnLangs(c, bij, t)`: een veer per deur (op het canvas van die deur). Loopt Amir binnen `langs.bereik` halve
  stokbreedtes langs het deurgat, op dezelfde vloer (`langs.hoog`, een dak erboven telt niet), dan duwt hij het doek in
  zijn looprichting, met een kracht die meegaat met zijn snelheid (`|v| / langs.v`, lopen 1, rennen tot `langs.max`) en
  met hoe dicht hij erbij is. De veer (`kracht`, `veer`, `demp`) laat het doek meegaan en een keer nazwaaien. Gemeten
  (wind uit): langzaam ongeveer 0,5, lopen 0,73, rennen 1,0. De uitslag telt in de zwaai, de wapper aan de zoom, de
  plooien, en boven 0,35 wijken de banen onderaan iets uiteen.
- Amirs plek: tijdens het tekenen kan `world` de camera zijn (meekijkende camera, binnen een huis); Amir zelf staat dan
  in `camSwap`. Binnen is het doek gespiegeld, dus de duw ook (`spiegel`).

## De vorm van de beweging (uit de proef)

- Elke deur een eigen fase (`gevel-index x 1,7`), zodat de zwaai niet overal gelijk loopt.
- Het doek in rijen van 2 px; rij `y` schuift opzij met `A k (zwaai + 0,6) + wapper`, `A = 8 x vlaag` (`GORDIJN.amp`,
  in canvas-px op stokbreedte 236), `k = ((y - stok) / (h - stok))^1,35` (bovenaan niets, onderaan het meest).
  `zwaai = 0,7 sin(1,1 t - 0,5 fr + ph) + 0,3 sin(1,9 t - 0,4 fr + 1,3 ph)`, met `fr` de plek van boven (0) naar
  onder (1): de hele baan zwaait mee, de onderkant iets achter de bovenkant aan. De `wapper` is klein en snel
  (`GORDIJN.wapper` 3 px, 8,5 en 12,7 rad/s) en zit alleen vlak boven de zoom (`fr^3`). Elke baan een eigen fase.
  De onderkant tilt iets op (`lift = 1 - 0,07 vlaag k`).
- Eerst liep er een golf langs het doek (`sin(1,8 t + 0,016 y)`, 20 px): dat zag eruit als golven in plaats van
  wapperen. Een golf die met `y` meeloopt dus niet terugzetten; houd de beweging in een stuk over de hele hoogte.
- Plooien: een horizontaal verloop van licht en donker, `source-atop` over het doek. De plooien staan stil en
  ademen alleen (geen strepen die opzij schuiven), sterkte mee met de vlaag.
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
