# Tutorial: The First Hunt, de mentor en zijn tekstwolk

Kop in de HTML: `// ---- tutorial: de mentor en zijn tekstwolk (level.mentor, zie notities/tutorial.md) ----`, direct na
`checkTips`. Grep: `MENTOR`, `mentorReset`, `mentorUpdate`, `mentorTeken`, `mentorWolkTeken`, `mentorVal`, `mentorKleur`,
`mentorOpname`. Het level is `TUT_1` (The First Hunt, vroeger Test 89), in de reeks `TUT_LEVELS` en te spelen met de knop The First Hunt onder Single Player (`btnTutorial`; zolang hij nooit uitgespeeld is staat er "Start here" op, daarna een vinkje, `TUT_SLEUTEL`), de opname `tools/mentor_opname.js`, het spoor
`design/tutorial/mentor_spoor.json`.

## Wat het is

De eerste tutorial voor nieuwe spelers (ontwerp met de opdrachtgever, 22-11-2026): bewegen leren zonder speer en zonder
vijanden. Een andere jager loopt voor Amir uit. Voorlopig is dat een omgekleurde Amir: de broek in `MENTOR.broek` (turkoois,
via `broekBeeld`) en een donkerder huid (`MENTOR.huid`: de tinten van rood tot oranje, niet te licht, zodat het felle lint
blijft). Identiteit en verhaal komen later; dan kan hij eigen art krijgen.

Bij elk station doet hij het stuk eerst voor ("Watch."), draait zich om, en wacht in zijn idle tot de speler bij hem is
(`MENTOR.bij`, op de grond, en minstens een seconde na zijn aankomst) en gedaan heeft wat het station vraagt (`eis`: `rol`,
gemeld door `rolStart` via `mentorEvent`, of `sprint`, een halve seconde met Shift over de grond rennen). Staat de speler stil
bij hem zonder het gedaan te hebben, dan zegt hij `nog`. Dan "goed zo" (`ok`, met `okDuur` per station), en hij doet het
volgende voor. Voorbij hem lopen kan niet: zolang hij uitlegt, voordoet of aftelt houdt hij de speler `MENTOR.voor` achter
zich (niet in de race en niet bij het slot).

De rem (`MENTOR.rem`, `mentorRemLijn`, `mentorRem`): zolang hij uitlegt, "goed zo" zegt of voordoet houdt hij je verder weg,
`rem.afstand` (200, altijd binnen `bij`), zodat je ziet wat hij doet in plaats van op zijn neus te staan. Bij het voordoen
telt de plek waar hij begon (`demoX`), dus je loopt hem niet achterna; is hij verder dan `rem.volg` (520) weg, dan mag je
op die afstand volgen, zodat jullie samen in beeld blijven. Wie al dichterbij stond wordt niet teruggeduwd maar komt niet
verder, terugstappen mag. In de lucht houdt hij je alleen tegen als je daar veilig neerkomt (geen ravijn onder de lijn,
geen hogere grond), anders mag de sprong door. Loop je er tijdens het voordoen tegenaan, dan zegt hij om de beurt een
regel uit `rem.zeg` (hooguit eens per `rem.opnieuw` s, nog zonder stem). Een station met `kijk: false` (station 0, "Keep
up!") is meelopen: daar geen rem bij het voordoen. Waarom zo en niet vastzetten: de speler houdt de controle, en een
ervaren speler wacht alleen zolang het voordoen duurt.

De camera houdt hem in beeld zolang hij voordoet, uitlegt of wacht (niet in de race en niet bij het slot): horizontaal
schuift het midden alleen zover als nodig is tot hij binnen `MENTOR.cam.marge` van de rand staat (`mentorCamKlem`, in de
meekijkende camera), en in de hoogte kijkt de camera naar de laagste vloer van de twee, zolang de hoogste nog in beeld past
(`mentorCamH`, in `updateCamera`). Zo zie je hem ook van het hoge terras springen en onder de stam door kruipen als je
boven blijft staan.

Hij wordt getekend vlak voor Amir (na de lichtkaart), in dezelfde stand van de camera; eerder in het beeld stond hij op
een hogere laag te zweven.

## De gids (27-11-2026): de Mkuki-ranger in plaats van de omgekleurde Amir

De mentor heeft nu eigen art: de nomadische Mkuki-ranger uit Grok (teal jas, roestrode sjaal en sjerp, speer). Het
spoor blijft dat van Amir (waar hij staat, hoe hoog, welke kant op, wanneer hij op de grond is); per beeld van het spoor
zegt `design/tutorial/gids/gids.json` welk frame van de gids erbij hoort. Kop in de HTML: `// ---- de gids: ...`, grep
`GIDS`, `gidsLaad`, `gidsNu`, `gidsTeken`, `gidsFx`, `gidsRenGeluid`. Zonder gids.json tekent hij weer de omgekleurde Amir.

- Bouwen: `python3 tools/gids_bouw.py` (leest de mp4's van Tom uit `design/tutorial/gids/bron/`, keyt ze, kleurt de groene
  speer om, maakt per animatie een blad en koppelt het spoor). **Neem je het spoor opnieuw op (`tools/mentor_opname.js`),
  draai dit daarna ook**, anders klopt de koppeling niet meer. Daarna `gen-offline-manifest.py`.
- Resolutie en geheugen (27-11-2026): de vellen staan op de resolutie van Amirs sprites. Amir staand is 276 px
  (`idle_ns.png`), de gids in zijn vellen 1,15 keer zo hoog (318 px; `AMIR_H`, `GIDS_KEER`). In de wereld blijft hij
  `LENGTE` (1,2 keer Amir); `px` in gids.json zegt hoeveel wereld-eenheden een pixel van het vel is. Elk frame staat strak
  ingepakt met een eigen rechthoek (`f`: x, y, breed, hoog, ankerX, ankerY) in vellen van hooguit 4096 breed. Het script
  maakt ook de halve set in `klein/design/tutorial/gids/` (Beeld: Licht); `gen-klein.py` laat die staan (`EIGEN`).
  Uitgepakt: 134,5 MiB voor de verkleining, nu 103,4 MiB, en 25,9 MiB met Licht. Moet het nog lichter, dan houdt `STAP`
  per animatie alleen elk zoveelste frame (bijvoorbeeld `{'idle': 2, 'verteller': 2, 'sprong': 2}`, rond 70 MiB).
- Animaties: idle (heen en terug), verteller (een keer als hij wacht en iets uitlegt: alleen handgebaren, mond dicht, kijkt
  niet naar de camera), ren (lus van 24 op afstand, sprinten gaat sneller door de lus), sprong (de hoge korte sprong;
  uit de ren zonder het rechtop staan; sinds 27-11-2026 ook bij het ravijn en in de race, op verzoek van de
  opdrachtgever, omdat die het meest op Amirs sprong lijkt: `SPRINT` in `gids_bouw.py` staat uit), groot (de
  sprintsprong, zit nog in de vellen maar het spoor gebruikt hem niet meer; terug met `SPRINT = 380`), buk, sluip (lus van 58), rol (roll1, roll2 en roll3 achter elkaar).
- Het roze in het haar: Grok tekent een paarse glans in het donkere haar en de knot. Het keyen haalt dat weg met despill
  (waar rood en blauw samen boven groen uitkomen gaat dat eraf).
- De speer is in de bron egaal groen (#00C800), zodat hij weg of te vervangen is. `SPEER` in het script kleurt hem om (de
  punt staal: het brede eind van de speer; de rest hout); `SPEER = None` haalt hem eruit.
- Schaal: per clip geijkt op het hoofd (`SCHAAL`), de gids staand 1,2 x Amir (ongeveer bandietmaat).
- Stof en geluid: de renlus van Amir (`amirren.mp3`), zachter naarmate hij verder van je af is; stof bij de afzet en de
  landing, en bij een landing van minstens `GIDS.geluid.landMin` hoog een zachte plof (`bavland.mp3`, zoals de chaser);
  bij de rol het rolgeluid en het stof van `ROL_STOF`.
- Schaduw (27-11-2026): dezelfde als die van Amir (`drawAmirSchaduw`, omgevingsschaduw en zonneschaduw, ijler in een
  sprong), via `gidsSchaduw`. amirSilhouet wil een los plaatje, dus elk frame wordt een keer klein uit het vel geknipt
  (`gidsSchaduwFrame`, `GIDS.schaduw.maat` hoog). Zonder gids.json blijft het oude ovaaltje.
- **De idle zoomde in (27-11-2026).** In de Grok-clip werd de gids van het eerste tot het laatste idle-frame 5 tot 6%
  groter (de hele figuur). De idle speelt heen en weer, dus hij zwol op en kromp weer, en bij de wissel naar de verteller
  (die even groot blijft) sprong hij tot 13 px kleiner. `ZOOM_VAST` in `gids_bouw.py` meet per frame de lijfhoogte, legt
  er een gladde kromme door en schaalt elk frame terug naar frame 0. Nu staan idle en verteller allebei op 316 tot 320 px
  in het vel. Alleen een animatie opnieuw bouwen: `python3 tools/gids_bouw.py idle` (het spoor blijft staan), dan
  `tools/gids_glad.py`.
- **Maat in beweging (27-11-2026).** Eerst ren, sprong, buk, sluip en rol op 1,135 gezet (hij leek rennend te krimpen),
  daarna leek hij rennend juist te groot. Gemeten met het idle-hoofd als sjabloon: op 1 is zijn hoofd in elke animatie even
  groot als in de idle, en bij Amir is dat ook zo. Rennend is hij lager door de houding, niet door de maat. Het krimpen kwam
  vooral van de inzoomende idle (ZOOM_VAST). Nu alles op 1, de sprintsprong op 1,05 (iets kleiner hoofd). `GROOTTE` in
  `gids_bouw.py`, `k` in gids.json. Les: ijk de maat op het hoofd, niet op de lichaamshoogte. Tool:
  https://claude.ai/artifact/SpQZiaU7nnS4NmwNtANnzQ
- **Rennend weer groter (28-11-2026).** Tom: rennend werd hij te veel kleiner dan in de idle. `GROOTTE['ren']` op 1,1
  (eerder 1,135 voelde te groot); alleen `k` verandert, het blad is opnieuw gebouwd met `gids_bouw.py ren`.
- Nog niet gebruikt: `gahurk`, `hurk_en_omkijk`, `hurkenwenk` (voor de panter-sluiples) en `deelsbruikbaar_vertellen`.
- Open: de speer los (nu omgekleurd in de frames), een klim voor de richel (hij springt nu), een rustig loopje.

## De stem van de gids (27-11-2026)

De gids praat: ingesproken regels uit ElevenLabs (stem "Guide": jonge Mkuki-krijger, zwaar Nigeriaans accent), in
`design/tutorial/stem/`. Kop in de HTML: `// ---- de stem van de gids`, grep `GIDS_STEM`, `gidsStemSpeel`, `gidsStemStap`,
`gidsStemBezig`, `mentorZegNu`, `mentorDelen`. Hij noemt Amir "little spear" (Amir begint als Mkuki zonder speer; de
payoff komt als hij de speer krijgt). Alle teksten staan in het project: `claude/tutorial_stemteksten.md`.

- Per station `stem` (de uitleg) en `okStem` (de lof). `zeg` mag een rij zijn: dan toont de wolk steeds het deel dat hij
  nu zegt, met per deel een bestand in `stem` (station 0: twee regels).
- De uitleg klinkt pas als de speler binnen `GIDS_STEM.bij` van hem is, een keer per station (na een val niet opnieuw).
- Hij gaat pas verder (het "goed zo" en voordoen) als hij uitgepraat is, en zegt `nog` niet door zijn uitleg heen. Het
  "goed zo" blijft minstens zo lang staan als `okStem` duurt.
- Nooit twee regels tegelijk; bij pauze stil en daarna verder; buiten het level weg (`gidsStemStap`, elk beeld). De
  regels tellen mee in `PRAAT_STEMMEN`, zodat Amir er niet doorheen roept.
- Niet achter het laadscherm: zolang `laadWacht` loopt begint hij niet, en een regel die al klinkt pauzeert.
- De wolk is de ondertitel (keuze 27-11-2026, uit de richtlijnen voor ondertitels in games): de tekst bij de spreker, in een
  keer als blok (geen meeschrijvende letters bij ingesproken tekst), donkere ondergrond, het naambordje als wie-praat, en
  buiten beeld aan de rand met een pijltje naar hem. Erbij: het spreekteken, drie golvende streepjes achter HUNTER
  zolang zijn stem klinkt (in `mentorWolkTeken`).
- Nu ingesproken (27-11-2026): alle stations van deel 1 (uitleg en lof), de race (station, aankondiging, aftellen, winst,
  verlies), de nog-regels en de valgrappen. Nog niet: de regels bij stilstaan (de functie bestaat nog niet) en deel 2.
- `nogStem` per station: de stem bij `nog`, hooguit eens per `GIDS_STEM.nogOpnieuw` (8 s) zolang de speler stilstaat.
  `valStem` op de mentor hoort per plek bij `vallen`; de grap komt uit een knikkerzak, nooit twee keer dezelfde achter
  elkaar.
- Nieuwe regel: mp3 in `design/tutorial/stem/` (stilte eraf, genormaliseerd), `stem`/`okStem` op het station, de `zeg`
  gelijk aan wat hij zegt (zonder tags als [chuckles]), dan `tools/gen-offline-manifest.py`.

## De gids beweegt glad (27-11-2026)

De opdrachtgever vond de gids naast Amir slecht bewegen. Gemeten (niet geschat) wat er mis was, en rechtgezet:

- **Hij hing aan Amirs anker.** `gidsTeken` zette hem per beeld op het anker van Amirs plaatje van dat moment. In Amirs
  renlus komen zijn voeten los: de gids huppelde 30 tot 36 eenheden op en neer en schoof 4 tot 20 opzij, op Amirs ritme in
  plaats van dat van zijn eigen benen. Nu staan zijn voeten op zijn eigen plek: de x van het spoor en `voet` (zijn hoogte).
- **Zijn anker was het midden van het hele plaatje,** speer en wapperende sjaal erbij: bij elke wissel van animatie sprong
  hij opzij, en in de renlus schoof zijn hoofd 23 eenheden heen en weer. `tools/gids_glad.py` zet het anker op het
  zwaartepunt van zijn silhouet; in de renlus nog 8.
- **De renlus hakkelde.** Het vel heeft 24 frames, maar het zijn 12 houdingen die elk twee keer staan, en het spoor gaf 24
  frames over 30 beelden: om en om 2 en 3 beelden per houding. Nu loopt hij op afgelegde afstand (`gidsRenFrame`,
  `GIDS.pas` 344: Amirs lus is 287, de gids is 1,2 keer zo groot), met de 12 oneven frames.
- **De sprong hing en jaagde.** Tien beelden dezelfde stijgende houding, dan frame 26 tot 62 in vier beelden. `gids_glad.py`
  verdeelt elk luchtstuk (sprong, groot) gelijkmatig over de tijd in de lucht.
- **In de lucht hing hij als een mediterende monnik.** De clip `jump_and_land` zelf zet af en zweeft dan bijna twee
  seconden met de knieen op (frame 24 tot 68 is een houding). Nu volgt de houding in de lucht zijn verticale snelheid, net
  als bij Amir: `gidsLuchtFrame`, `GIDS.vMax` en `GIDS.lucht` (sprong: strekken 16 tot 21, top 22 tot 40, vallen 66 tot
  76; groot: gestrekt, dan intrekken). Afzet en landing op de grond blijven uit het spoor. De gelijkmatige verdeling van
  `gids_glad.py` geldt nu alleen nog waar de snelheid niets kiest.
- **De grootte klopte wel.** Gemeten op zijn haarknot (rond, dus vanuit elke hoek even groot): 17 tot 19 eenheden in idle,
  ren, buk, sluip en groot. Lichaamshoogte zegt hier niets (een ren is lager), en een hoofd als maat ook niet (breder of
  smaller per kijkhoek). De les: meet schaal op iets ronds of iets dat in elke houding gelijk blijft.

Draai `tools/gids_glad.py` na `tools/gids_bouw.py` (en dus ook na een nieuwe opname van het spoor).

## Het spoor: opgenomen, niet nagebouwd

**Les (27-11-2026): interpoleer het spoor.** Het spoor heeft 30 beelden per seconde, het spel tekent er 60. Zonder
tussenstap stond de gids elk tweede beeld stil en sprong hij dan 11 px: schokkerig naast Amir, die elk beeld schuift.
`mentorFrame` vult x en h nu in tussen dit beeld en het volgende. Bij een nieuw spoor of een andere opname: meet per
getekend beeld hoeveel hij verschuift (gelijkmatig, geen 0 en dubbel om en om).

De mentor heeft geen eigen natuurkunde. `tools/mentor_opname.js` speelt het level in Chromium met Amir (op vaste 60 fps,
met echte toetsaanslagen) en de haak `mentorOpname` (naast `pvpVang`) legt per beeld vast welk plaatje waar stond. Het spel
speelt dat terug op 30 fps. Elk stuk (`segs[i]`) eindigt met omdraaien en een idle; vanaf `lus` speelt hij die idle in een
lus. Per beeld: `[x, h, beeld, dx, dy, dw, dh, spiegel, opDeGrond]`, in sprite-eenheden zoals bij PvP.

Verander je het level (een kei, een gat, een terras), neem dan opnieuw op: `node tools/mentor_opname.js` (met `--spoor` zie
je per tiende seconde x, hoogte en op de grond, om de opdrachten bovenin het script af te stellen). Loopt hij ergens vast,
dan meldt het script FOUT en schrijft het niets weg. Verandert er iets aan Amirs sprites, dan ook.

## Het level: `mentor`

Het sprintstuk ("Run like the wind", seg 6) is sinds 28-11-2026 1200 lang in plaats van 400 (van -4700 tot -5900): alles
erachter (het brede ravijn, de race, de treden, de fakkels, finish en `terug`) schoof 800 naar links, en het spoor is
opnieuw opgenomen.

```
mentor: { spoor, finish, prijs: {x, h}, win, verlies, vallen: [grappen], stations: [
  { zeg, seg, ok, eis, nog, kijk, terug, race } ] }
```

- `zeg`: wat hij zegt terwijl hij wacht. Toetsen als `[LEFT]`, `[RIGHT]`, `[UP]`, `[DOWN]`, `[SHIFT]`, `[SPACE]`, `[V]`,
  `[E]` worden knopjes in de wolk (`MENTOR_TOETS`).
- `seg`: welk stuk hij daarna voordoet. Zonder `seg` (maar met `ok`) gaat hij meteen door naar het volgende station.
- `eis` en `nog`: wat de speler eerst moet doen, en wat hij zegt als de speler bij hem is zonder het gedaan te hebben.
- `kijk`: de tekst aan het begin van het voordoen (standaard "Watch.", `false` voor geen).
- `terug`: een veilige plek voor een stuk. Een val (`fallDeath`, via `mentorVal`) zet de speler op de dichtstbijzijnde
  `terug` achter hem (op plek, niet op station: in de race loopt het station al vooruit), met een korte fade
  (`MENTOR.val`) en een grap uit `vallen`; de uitleg van het station blijft achter de grap staan.
- `race`: aftellen (3, 2, 1, Go!), dan speelt hij zijn stuk op `MENTOR.race.tempo` (iets trager dan opgenomen). Wie het
  eerst voorbij `finish` is wint; wint de speler, dan komt er een kalebas op `prijs`.

`readLevel` neemt het veld over. In de sandbox doet de mentor niets.

## De kruipstam (`kruipstammen`)

**Vervangen (26-11-2026):** The First Hunt heeft nu op beide plekken (-3175 en -7730) een korte holle stam van droog
savannehout met een boma erop (`holstamSoort: 'savanne'`, `holstammen: [{x, s: 0.45, n: 0.5, boma: true}]`, zie "de
holle stam" in `notities/wegwijzers.md`). De kruipstam hieronder zit nog in de code, maar geen level gebruikt hem.

Geen zwevende rots meer (de opdrachtgever wil niets dat nergens aan vastzit): een omgevallen dode stam op twee keien, een
Grok-plaat (`design/tutorial/stam_keien.png`, gemaakt met de stijl van `design/tree.png` en `design/boulder.png`, wit
weggeknipt). `kruipstammen: [{x, s}]`, `x` het midden. readLevel zet er een onzichtbare zwevende laag onder
(`look: 'geen'`, `kruipstamDak`) met de onderkant van de stam als `onder` (163): staand loop je ertegenaan, kruipend kom
je eronder door. De keien staan net achter het pad. levelcheck telt zo'n kruipdak niet mee in de sprongen tussen zwevende
lagen.

## De wolk

`mentorWolkTeken` tekent na alles (bij de HUD), op de plek boven zijn hoofd die `mentorTeken` in schermpixels vastlegt: een
donker vlak met een gouden rand, een staartje naar zijn hoofd, het naambordje HUNTER, en de tekst met knopjes. Hij poppt even
op als de tekst wisselt. De grootte schaalt met de hoogte van het scherm. De balk met de toetsen bovenin gaat in dit level weg.

## Open

- De panter aan het eind (de sluiples: hoog gras, omkijken met een tell, de speer van de mentor, steken): het volgende stuk.
- De stem bij stilstaan (de wachtregels uit `claude/tutorial_stemteksten.md`) en deel 2 met de panter.
- Op een telefoon staan er nog toetsen in de wolk in plaats van de knoppen.
- `offline-assets.json` kent het spoor nog niet: draai `tools/gen-offline-manifest.py` op een volledige checkout. Zonder het
  spoor is het level gewoon speelbaar, alleen zonder mentor.
- Het level staat nu in Test levels; als het af is, krijgt het een eigen plek in Campaign.
- De klim: een laag savanneterras, dan een plateau van rots (een hoge savannelaag wordt onderin zwart) met een richel aan
  de wand.
