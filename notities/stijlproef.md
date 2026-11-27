# Stijlproef (Test 97)

Waar je elk nieuw omgevingsasset naast de stad en Amir zet voordat het het spel in mag. Hoort bij de stijlsheet
(claude.ai artifact "Amir stijlsheet": regels, palet, goed/fout, per landschap).

## Het level
- `TEST_97`: de rand van Ishmul (wit zand, daglicht) op dezelfde wereld-x als de linkeroever van Ishmul: een huis van twee,
  het hoge huis van drie, dan savanne met de goedgekeurde hutten (`hut_rond`, `hut_koepel_groot`, `hut_koepel_hoog`) en
  de rots. Amir begint bij -2900, vredig.
- De rijen huizen in de verte lopen hier door tot boven de hutten (in Ishmul niet); nog niet uitgezocht waarom
  (`stadAchterRanden`, met andere achterTot en een derde gevel bleef het zo). Voor de proef niet erg.

## Het paneel (STIJLPROEF)
Alleen in een level met `stijlproef: true` (via `readLevel`). `stijlproefZet` uit `setLevel`.
- **Bestand**: een PNG (transparant, recht van voren). Komt als `PROPS.proef` op 300 links van Amir te staan.
- **Zet bij Amir**, **Spiegel**, **Weg**.
- **Hoogte in Amir**: `PROPS.proef.h`, live. Een deur hoort ongeveer 1,2 Amir te zijn.
- **Kleur** (tint in graden), **Verzadiging**, **Licht**: het plaatje wordt per pixel omgekleurd (geen `ctx.filter`, zie
  "de tint van een level") en als gewone Image in `propImg.proef` gezet. Zo zie je of een asset in een andere kleurstreek
  nog in dezelfde wereld past.
- Niets wordt opgeslagen. Een goedgekeurd asset krijgt daarna een eigen regel in `PROPS` en een plek in `design/`.

## De check (uit de stijlsheet)
Recht van voren; even rustige vlakken als de stadsmuur; kleur binnen de familie; schaal klopt met Amir; geen lijnen die
de stad niet heeft; en niet te veel lijken op een ander landschap.

## Hutten en putten
`design/savanne/hutten/`: Grok eebf2583 (hut_rond) en 2fa55f54 (de twee koepels). Daarna in een keer verweerd (Grok
53cc987f): oker en roodbruin leem in de kleur van de savannegrond, strepen, afgebrokkeld met leemsteen eronder, grijs
riet. Wit en schoon leken ze op huizen van Ishmul; nu horen ze bij een klein, arm dorp. Zie de projectnotitie
savanne_hutten_2d.md.

Putten: `design/savanne/putten/` (put_leem, put_steen, put_shaduf), Grok 2b165ff8. Ze staan in Test 97 na de hutten.
In de sandbox onder Decor, rij **Savannedorp**: een knop per hut en put (`data-sdorp`).

## De loopput (LOOPPUT)
Een lage, brede put om op te staan en overheen te springen, in twee soorten (regel 9 van de stijlsheet: elk landschap
een eigen gezicht):
- **savanne** (de standaard, `design/savanne/putten/put_loop_savanne.png`, Grok d77b641d): de steenput van het dorp
  (put_steen) breed en laag gemaakt, met gevorkte takken, een houten deksel en een kruik ernaast, net zo rustig geschilderd
  als de rest. Een eerdere, verweerde versie (Grok 48c99908) zag er te echt uit naast de stad en is vervangen.
- **stad** (`soort: 'stad'`, `put_loop_stad.png`, Grok fee91518): de gepleisterde leemput met een rond houten deksel,
  rechte palen en een kuipemmer. Hoort eerder in Ishmul.

Beide zijn edits van dezelfde plaat (eerst put_leem met de galerij als referentie voor de kijkhoek), dus vorm en maat zijn
gelijk. Het bovenvlak is van schuin boven te zien, zodat Amir erin staat en niet op een streep. Het frame staat op de
achterrand en de hele plaat ligt achter de personages: Amir en zijn speer staan altijd voor het hout. De palen zijn bij het
knippen verlengd (een strook herhaald), zodat de balk boven Amirs hoofd uitkomt.

- Level: `loopPutten: [{x, s, f, soort}]`, `x` het midden, `s` de grootte, `f` spiegelen, `soort` `'stad'` of niets
  (savanne). Bij `s` 1 ligt de looplijn 160 boven de grond (de sprong haalt 208); per soort staan de maten in `LOOPPUT`.
- Botsing zoals bij de kruipstam: readLevel zet er een onzichtbare zwevende laag op (`loopputDak`, look `geen`, `onder: 0`).
  Amir loopt er tegenaan, springt erop en loopt er aan beide kanten af. Vijanden houdt hij tegen als een kei (regel 7): een
  slang bleef aan de linkerkant staan, een hyena aan de rechterkant.
- Getekend in `drawClimb` na de kruipstam, dus achter de personages (`loopputTeken`).
- Nagekeken met Playwright: tegen de muur, de sprong, staan, de steek en de worp bovenop, eraf lopen.
- In Test 97 de savanneversie na de drie putten (x -7150). In de sandbox in de rij **Savannedorp**: **Loopput**,
  **Loopput stad** (elke klik een verder) en **Weg**.

## De oude 3/4-hutten vervangen
De hut bij de rotswand aan de start (`HUT`), de verre hut (prop `hut`) en de dorpsplaten (`VILLAGE`: de vijf hutten, de
voorgrondhut en de put) wijzen nu naar het savannedorp (hut_rond, hut_koepel_groot, hut_koepel_hoog, put_steen). De namen
blijven, dus levels en de Maker veranderen niet; alleen The First Hunt gebruikt de dorpsplaten. Nog oud en 3/4: het
kookafdak (`cooking_shelter`) en alle winterversies (`*_sneeuw`, `villeaghut_sneeuw`); de oude platen staan nog op schijf.

## Op te ruimen zodra het kan (de oude 3/4-hutten)
Na deze vervanging gebruikt geen savannelevel de oude platen nog. Ze blijven voorlopig op schijf, omdat de oude episodes
eruit gaan en er nog naar kunnen wijzen. Zodra die weg zijn:
- Weghalen: `design/villeaghut.png`, `klein/design/villeaghut.png`, en in `design/village/` (en `klein/`) `hut_round_arch`,
  `hut_round_door_left`, `hut_round_back`, `hut_rect_porch`, `hut_rect_back`, `well`, `foreground/hut_round_back_closeup`.
- Eerst nakijken: `grep -n "villeaghut\|design/village/" amir-king-of-africa.html tools/*.py` geeft geen treffer meer behalve
  de winterplaten (`*_sneeuw`, `villeaghut_sneeuw`, prop `hut_sneeuw`).
- Mee aanpassen: de lijst bovenaan de HTML met `design/villeaghut.png` (de kleine set), `tools/gen-klein.py` (de regels voor
  `villeaghut`), en de bronnen in `tools/sneeuw_dorp.py`.
- Nog te beslissen: het kookafdak (`cooking_shelter`, 3/4, door geen level gebruikt) en de winterversies. Die laatste kunnen
  opnieuw uit de nieuwe hutten met `tools/sneeuw_dorp.py`, daarna kunnen de oude sneeuwplaten ook weg.
- Daarna `python3 tools/gen-offline-manifest.py`.

## De rotsen warmer (27-11)

De kei (`boulder.png`), de platte rots (`flatrock.png`, `PLAT`) en de rotswand (`cliff.png`, `CLIFF`) waren koel grijs
met een dikke zwarte omlijning en vielen daardoor uit de toon naast de hutten, de putten en Ishmul. Een nieuwe, gladde
stijl uit Grok (zonder lijnen) is geprobeerd en afgekeurd: naast de huizen van Ishmul te glad en naast de oranje hutten
te bleek, en de rotswand ging op in de witte stad. De textuur mag dus blijven, net als bij de huizen.

Wat er nu is: dezelfde platen, alleen warmer grijsbruin en met warm donkerbruine lijnen in plaats van zwart (de
buitenrand 1 pixel dunner). Vorm, textuur en maten zijn gelijk, dus geen getal in de code veranderd.

Dezelfde behandeling hebben ook gekregen: de rotswand van de muur (`rotswand_kaal.png`), de runerotsen
(`rotswand_spits/pieken/zuilen/boog/boog_scheef.jpg`, het wit blijft wit voor `witKnip`), de rots van een ravijn
(`rotstextuur.png`), de grot (`design/grot/`: keien, hangblokken en de tegels, zonder de rand dunner te maken zodat ze
naadloos blijven) en het rotsdecor (`design/rotsdecor/`, `ROTS_FAM`). Die waren al warmer en dunner omlijnd, dus daar is
het verschil klein; het gaat erom dat alle rots uit dezelfde kleur komt.

- De originelen staan in `design/bron/rotsen_oud/` (en `klein/design/bron/rotsen_oud/`), op hetzelfde pad als in het spel.
- `python3 tools/rots_warm.py` maakt van alles daarin de speelversie opnieuw, daarna `tools/gen-offline-manifest.py`.
- Maakt `tools/rotsdecor_knip.py` of `tools/rots_vulling.py` een plaat opnieuw, kopieer die dan eerst naar
  `bron/rotsen_oud/` en draai `rots_warm.py` erna, anders is hij weer koel grijs.
- Nog niet gedaan: de winterversies (`*_sneeuw.png`).
