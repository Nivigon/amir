# Straten: een stadje van losse straten met poorten (Oaktown)

`STRATEN`, `straatAan`, `straatHier`, `straatPoorten`, `straatPoortBij`, `straatE`, `straatWissel`, `straatAanvul`,
`straatKill`, `straatKlem`, `straatCamKlem`, `straatVijandKlem`, `straatPoortTeken`, `straatPoortVoor`, `straatHudTeken`,
`straatFadeTeken`, `straatReset`, `stadKalebasPlek`, `OAK_STRATEN`, `OAK_LEVELS`

Het systeem is algemeen: elk level met een veld `straten` (en een `stad`) speelt zo. Oaktown is het eerste.

## Het veld

```
straten: { start: 'kasuwa', doel: 50, aanvul: 30,
           knopen: { tl: [0, 0], tr: [1, 0], ml: [0, 0.5], mr: [1, 0.5], bl: [0, 1], br: [1, 1] },
           lijst: [ { id: 'kasuwa', naam: 'Kasuwastraat', knoop: ['mr', 'ml'], r: -200, l: -7500 }, ... ] }
```

- Elke straat is een eigen strook van de wereld, van `r` (rechts, het begin) naar `l` (links, het eind). De stroken liggen
  ver uit elkaar (Oaktown: 16000 px); Amir en de camera blijven in de strook van de straat waar hij is (`straatKlem`,
  `straatCamKlem`), dus je ziet nooit de lege wereld ertussen. Gevels, galerijen, kramen, leemmuren, kalebassen en
  spawns staan gewoon op hun wereld-x in de strook van hun straat.
- `knopen` zijn de kruispunten, met hun plek op de minimap (0 tot 1). Een straat begint bij `knoop[0]` en eindigt bij
  `knoop[1]`. Aan een uiteinde komt een poort voor elke andere straat op dezelfde knoop (`straatUit`, in de volgorde
  van de lijst): de eerste is de hoekpoort (rechtdoor), een tweede de rechte poort ernaast (rechts af). Een knoop waar
  geen andere straat op uitkomt geeft een dicht uiteinde zonder poort.
- `start` de straat waar je begint (in het midden, of op `level.start`), `doel` het aantal kills (standaard 50),
  `aanvul` hoeveel seconden een straat leeg moet zijn geweest voor hij zich aanvult (standaard 30).
- Een level met `straten` heeft geen `ends` nodig; levelcheck slaat de regel `einde` dan over.

## De poorten

Twee platen uit `design/stad/` (maten in `metadata.json`), lui geladen met de stad (`stadLaad`):

- **poort_hoek** (de vleugel in 3/4) staat aan de rand van de straat, links gewoon en rechts gespiegeld. Amir loopt de
  boog in tot achter de voorkant (`gang`); tussen `doorzicht[0]` en `doorzicht[1]` wordt de voorkant half doorzichtig
  over hem heen getekend (`straatPoortVoor`, na de personages). Vanaf `vraag` (halverwege) staat er "Naar de ...?  E".
- **poort_recht** (de achterwand met de boog) staat direct ernaast, met zijn toren over het verre eind van de hoek
  (`ver`, `toren`). E werkt onder de boog (`onder`: dat deel van de boogbreedte).
- Boven elke boog hangt een bordje met de naam van de straat erachter; onder de boog wordt het goud met de vraag.
- E werkt alleen op de straat, op de grond, buiten gevecht (`stadInGevecht`, net als de stadstrap: "Niet nu: er staat
  een vijand in de buurt") en met een speer (in de hand of op de rug), anders "Pak je speer eerst".
- De wissel (`straatFade`): de wereld staat stil, het beeld gaat helemaal zwart (`fade.uit`, `zwart`, `in`), en midden in
  het zwart staat Amir in de nieuwe straat bij de poort die terug leidt (buiten de hoek, of onder de rechte boog), met
  zijn gezicht de straat in. De camera springt mee (`camEase = null`).
- Vijanden gaan nooit door een poort: alleen Amir wisselt van strook, en `straatVijandKlem` houdt elke vijand in zijn
  eigen straat (`vijandRand` van de rand) en vóór de boog van een hoekpoort: de gang in loopt hij niet. Staat hij daar
  vlak voor, dan ben je nog in gevecht en gaat de poort niet.
- Op 720 hoog is een hoekpoort zo'n 1330 px breed en een splitsing (hoek plus rechte poort) zo'n 2150 px. Ze schalen
  mee met het scherm, net als de gevels; houd daarom zo'n 250 px vrij tussen een poort en het eerste huis.

## Vijanden, aanvullen en het einde

- Een spawn telt alleen in de straat waar je bent (`updateSnakes` slaat de rest over, en `spawnPoint` zoekt een plek
  buiten beeld binnen de straat). Slangen in een andere straat worden niet opgeruimd als je ver weg bent.
- Verlaat je een straat, dan onthoudt hij wanneer (`straatStand[id].weg`, op de speelklok `straatKlok`). Kom je terug
  na minstens `aanvul` seconden, dan maakt `straatAanvul` zoveel opgebruikte spawns weer scherp als er vijanden
  ontbreken tot het startaantal (de verste eerst), en komen de kalebassen die je daar oppakte terug
  (`p.straatBron`). Eerder terug: niets. Zo kun je niet farmen door heen en weer te stappen.
- Elke kill telt (`vijandDood` roept `straatKill`); bij `doel` wacht het spel `winWacht` seconden en speelt dan
  `winLevel`, hetzelfde einde als de fakkels. Dood is het hele level opnieuw (`restart` → `straatReset`), kills op 0.
- Bovenaan staat "kills: n / 50" (`hudPil`).

## De minimap

Rechtsonder, alleen op een laptop (`camTelefoon()` is de detectie van de camera). De straten zijn lijnen tussen hun
knopen: de huidige in goud, een bezochte licht, de rest bijna onzichtbaar; een witte stip voor Amir schuift langs zijn
straat (van `r` naar `l`). Maat in `STRATEN.kaart`.

## Oaktown

Een dobbelsteen met zes ogen: de ogen zijn de kruispunten, de straten de lijnen ertussen, als een rechthoek met een
balk door het midden. Vier hoeken met een poort, twee splitsingen met twee poorten, en drie rondjes (boven, onder en
het grote). De namen komen uit de oude stad Kano. Beide levels delen `OAK_STRATEN`, `OAK_STAD`, `OAK_TERRAS` en
`OAK_KALEBAS`; alleen `OAK_SPAWNS_1` (zandslangen) en `OAK_SPAWNS_2` (bandiet, schildbandiet, kooiman zonder duel,
kruisboogbandiet, zweepman) verschillen. Per straat:

| straat | kaart | opbouw | kalebas |
| --- | --- | --- | --- |
| Kasuwastraat (start) | midden | kramen, een hoge galerij (730) | via tafel en doek, met de getimede veer |
| Dalastraat | boven | getrapte leemmuren 170, 340, 510 | bovenop de hoogste muur |
| Jakarasteeg | links boven | galerij over de hele lengte (401) | via tafel en rieten dak naar de galerij |
| Karofistraat | rechts boven | houten trap achter het hoge huis | op het balkon (E bij de trap) |
| Makerasteeg | links onder | de toren: galerijen 401 en 780 over twee huizen, 590 over het rechter; recht omhoog | bovenin |
| Rumfastraat | rechts onder | hogere wijk op een lage leemmuur, met een huis erop | op de hoge muur (340) |
| Zangosteeg | onder | over de daken (487) | via kraam, galerij of doek op het laatste dak |

Een straat is drie tot vier schermen breed: de middenzone met de huizen is ongeveer anderhalf scherm, de rest zijn de
poorten aan de uiteinden. De definitie is gegenereerd uit een korte beschrijving per straat (afstanden vanaf de
poorten); verschuif je iets, houd dan de huizen en kramen buiten de poorten.

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

Onder De stad, **Straten**: **Drie straten** zet drie korte straten rond een splitsing neer (aan het eind van de
straat waar je staat een hoekpoort en een rechte poort, in de andere twee de poorten terug), met de minimap;
**Weg** haalt ze weg.
