# Straten: een stadje van losse straten met knooppunten (Oaktown)

`STRATEN`, `straatAan`, `straatHier`, `straatPoorten`, `straatPoortBij`, `straatE`, `straatWissel`, `straatAanvul`,
`straatKill`, `straatKlem`, `straatCamKlem`, `straatVijandKlem`, `straatPoortTeken`, `straatHudTeken`,
`straatReset`, `stadKalebasPlek`, `straatRaster`, `OAK_STRATEN`, `OAK_LEVELS`

Het systeem is algemeen: elk level met een veld `straten` (en een `stad`) speelt zo. Oaktown was het eerste; sinds
08-11-2026 is het een raster met knooppunten, net als Sandville.

## Het veld

```
straten: { raster: true, start: 'kasuwa', doel: 50, aanvul: 30, muur: 300,
           knopen: { tl: [0, 0], tr: [1, 0], ml: [0, 0.5], mr: [1, 0.5], bl: [0, 1], br: [1, 1] },
           lijst: [ { id: 'kasuwa', naam: 'Kasuwastraat', knoop: ['mr', 'ml'], r: -200, l: -7500 }, ... ] }
```

- Elke straat is een eigen strook van de wereld, van `r` (rechts, het begin) naar `l` (links, het eind). De stroken liggen
  ver uit elkaar (Oaktown: 16000 px); Amir en de camera blijven in de strook van de straat waar hij is (`straatKlem`,
  `straatCamKlem`), dus je ziet nooit de lege wereld ertussen. Gevels, galerijen, kramen, leemmuren, kalebassen en
  spawns staan gewoon op hun wereld-x in de strook van hun straat.
- `knopen` zijn de kruispunten, met hun plek op de minimap (0 tot 1, x naar rechts, y naar beneden). Een straat begint
  bij `knoop[0]` en eindigt bij de laatste; met drie knopen ligt de middelste op `m`.
  Alleen rechte straten: alle knopen van een straat op dezelfde rij of dezelfde kolom, nooit schuin.
- `raster: true` en `muur`: de knooppunten van Sandville. Bij elke knoop een poort de diepte in of een pad naar voren
  naar elke straat die daar die kant op verder loopt, aan elk uiteinde een hoge leemmuur. Hoe dat werkt (welke uitgang
  waar, de poort, het pad, de wissel, de minimap) staat in "Straten en knooppunten (Sandville)" in `notities/stad.md`.
- `start` de straat waar je begint (in het midden), `doel` het aantal kills (standaard 50, `0` is geen einde),
  `aanvul` hoeveel seconden een straat leeg moet zijn geweest voor hij zich aanvult (standaard 30).
- Een level met `straten` heeft geen `ends` nodig; levelcheck slaat de regel `einde` dan over.

## De hoekpoort gaat eruit

Eerst had een straat zonder `raster` aan elk uiteinde een hoekpoort (`poort_hoek.png`, een vleugel in 3/4 die je
inliep, voor rechtdoor) en op een splitsing de rechte poort ernaast (`straatPoorten`, `straatPoortVoor`, `straatEind`,
`straatFade`). Een poort rechtdoor bleek in zijaanzicht niet goed te maken, en op een kruising is hij ook niet nodig:
rechtdoor is gewoon de straat die doorloopt. Sinds 08-11-2026 werken alle straten met knooppunten; Oaktown is omgezet.
Alleen De Kroonwijk (`GP_5_STRATEN`, schuine straten) gebruikt hem nog, tot er een raster voor is; daarna gaat de
hoekpoort met alle code die alleen voor hem bestond eruit. Zet hem in geen nieuw level.

## Vijanden, aanvullen en het einde

- Een spawn telt alleen in de straat waar je bent (`updateSnakes` slaat de rest over, en `spawnPoint` zoekt een plek
  buiten beeld binnen de straat). Slangen in een andere straat worden niet opgeruimd als je ver weg bent.
- Verlaat je een straat, dan onthoudt hij wanneer (`straatStand[id].weg`, op de speelklok `straatKlok`). Kom je terug
  na minstens `aanvul` seconden, dan maakt `straatAanvul` zoveel opgebruikte spawns weer scherp als er vijanden
  ontbreken tot het startaantal (de verste eerst), en komen de kalebassen die je daar oppakte terug
  (`p.straatBron`). Eerder terug: niets. Zo kun je niet farmen door heen en weer te stappen.
- In een stadje van straten komen de vijanden van een straat vaak tegelijk; `spawnPoint` zet er dan geen twee binnen
  90 px van elkaar (eerst landden er twee slangen precies op elkaar).
- Elke kill telt (`vijandDood` roept `straatKill`); bij `doel` wacht het spel `winWacht` seconden en speelt dan
  `winLevel`, hetzelfde einde als de fakkels. Vanaf de laatste kill is Amir onkwetsbaar tot het einde (zonder te knipperen), anders kon hij in die
  `winWacht` nog sterven en begon alles opnieuw. Dood is het hele level opnieuw (`restart` → `straatReset`), kills op 0.
- Bovenaan staat "kills: n / 50" (`hudPil`).

## De minimap

Rechtsonder, alleen op een laptop (`camTelefoon()` is de detectie van de camera): de kaart van het raster
(`straatRasterKaart`, zie `notities/stad.md`). Maat in `STRATEN.kaart`.

## Oaktown

Een dobbelsteen met zes ogen: de ogen zijn de kruispunten, de straten de lijnen ertussen, als een rechthoek met een
balk door het midden. Op het raster zijn dat drie rijen (Dala boven, Kasuwa in het midden, Zango onder) en twee kolommen
van elk twee straten (links Jakara en Makera, rechts Karofi en Rumfa, allebei van boven naar beneden). Een rij heeft zijn
poorten naar het noorden en zijn paden naar het zuiden; een kolom die naar het zuiden loopt heeft zijn poorten naar het
westen en zijn paden naar het oosten. Dus:

| straat | kaart | uitgangen |
| --- | --- | --- |
| Kasuwastraat (start) | middelste rij | bij elk eind een poort (Karofi, Jakara) en een pad (Rumfa, Makera) |
| Dalastraat | bovenste rij | alleen paden (Karofi, Jakara) |
| Zangosteeg | onderste rij | alleen poorten (Rumfa, Makera) |
| Jakarasteeg, Makerasteeg | linkerkolom | alleen paden (Dala en Kasuwa, Kasuwa en Zango) |
| Karofistraat, Rumfastraat | rechterkolom | alleen poorten (Dala en Kasuwa, Kasuwa en Zango) |

Jakara en Makera liggen in elkaars verlengde, net als Karofi en Rumfa: daar is geen uitgang tussen, want rechtdoor is
geen poort. Van Jakara naar Makera ga je via de Kasuwastraat, die op dezelfde knoop een poort en een pad heeft: het pad
naar Kasuwa en meteen weer het pad naar Makera, zonder te lopen.

De namen komen uit de oude stad Kano. Beide levels delen `OAK_STRATEN`, `OAK_STAD`, `OAK_TERRAS` (met de hoge
leemmuren aan de uiteinden) en `OAK_KALEBAS`; alleen `OAK_SPAWNS_1` (zandslangen) en `OAK_SPAWNS_2` (bandiet,
schildbandiet, kooiman zonder duel, kruisboogbandiet, zweepman) verschillen. Per straat:

| straat | opbouw | kalebas |
| --- | --- | --- |
| Kasuwastraat (start) | kramen, een hoge galerij (730) | via tafel en doek, met de getimede veer |
| Dalastraat | getrapte leemmuren 170, 340, 510; van links via de doek van de kraam op het lage dak | bovenop de hoogste muur |
| Jakarasteeg | galerij over de hele lengte (401) | via tafel en rieten dak naar de galerij |
| Karofistraat | houten trap achter het hoge huis | op het balkon (E bij de trap) |
| Makerasteeg | de toren: galerijen 401 en 780 over twee huizen, 590 over het rechter; recht omhoog | bovenin |
| Rumfastraat | hogere wijk op een lage leemmuur, met een huis erop; van links via de rieten kraam | op de hoge muur (340) |
| Zangosteeg | over de daken (487) | via kraam, galerij of doek op het laatste dak |

Elke straat is in beide richtingen te doorlopen. In de Dala- en Rumfastraat kon dat eerst niet: van links stond je voor
een muur van 510 of 340 hoog (de sprong is 200). Nu staat er links een kraam: in Dala de doek (van de tafel recht omhoog
op de doek springen, dan met een sprong naar rechts over het lage dak de muur op), in Rumfa een rieten kraam (tafel,
rieten dak, muur). Nagemeten op 1280x720, 1920x1080 en 852x393.

Een straat is drie tot vier schermen breed: de middenzone met de huizen is ongeveer anderhalf scherm, de rest zijn de
poorten en paden aan de uiteinden. Bij het omzetten naar het raster (08-11-2026) bleef elke straat op zijn strook; alleen
de Zangosteeg werd 1100 px langer (`l` van -101900 naar -103000) en alles erin schoof 700 naar links, zodat de rieten
kraam en de galerij op 1920x1080 niet tegen de poort vallen. Vijf stukken voetdecor schoven een stukje op en een
kruik in de Zangosteeg ging weg. Nagemeten op 852x393, 1280x720, 1366x768 en 1920x1080: geen huis, galerij of kraam
over een poort, voetdecor en kalebassen minstens 300 px van een poort en van het open stuk van een pad. Alleen op
1920x1080 staat de rieten kraam in de Rumfastraat 64 px van de poort (hij raakt hem niet; hij hoort tegen de lage muur).
De huizen naast een poort schuiven opzij (`straatGevelX`); verschuif je iets, houd dan kramen en voetdecor buiten de
poorten en paden.

## Een kalebas op een leemmuur

In de stad kwam een kalebas met een hoogte altijd op de dichtstbijzijnde galerij of het dichtstbijzijnde dak
(`stadDakPlek`), ook als hij op een leemmuur van die hoogte hoorde. `stadKalebasPlek` laat hem nu op het terras als
dat daar even hoog is. Voor de bestaande stadlevels verandert er niets (daar ligt geen kalebas op een muur).

## Nakijken

- `python3 tools/levelcheck.py Oaktown`.
- `node tools/speelrobot.js "Oaktown (makk" --taai`: in een level met straten drukt de robot E onder een poort naar
  een straat die hij nog niet zag, en altijd aan het eind; hij meldt welke straten hij bezocht en hoeveel kills.
  Hij steekt nu ook naar mensen (bandieten en de rest) die voor hem staan.
- Of een kalebas te halen is, ziet levelcheck niet (hij kent de vloeren van de stad niet). Dat is bij de bouw nagemeten
  met een klimtest in Chromium: per kalebas de route over de echte vloeren (straat, tafel, rieten dak, doek, galerij,
  balkon, dak, leemmuur) en elke sprong echt gemaakt, op 852×393 (telefoon), 1280×720, 1366×768 en 1920×1080:
  alle zeven te halen. Let op de telefoon: de huizen en galerijen worden smaller, maar staan op dezelfde wereld-x,
  dus een gat tussen twee huizen wordt daar relatief groter. In de Makerasteeg lag de bovenste galerij eerst alleen
  op het linker huis; op een telefoon was dat een gat van 3,5 Amir. Nu loopt hij over beide huizen en spring je
  recht omhoog door de galerij erboven, zoals in de toren van Stad 1.

## Sandbox

Onder De stad, **Knooppunten** (zie `notities/stad.md`). De oude knop **Straten**, **Drie straten** (met de hoekpoort)
is weg: **Kruising** doet hetzelfde op de manier van nu.
