# De golvende rand

### Waar het om gaat

Een terreinmassa in het spel had altijd een rechte rand: de grondrand als tegel, een terras als
plaat met gebroken zijkanten, een zwart blok als rechthoek met driehoekige tandjes eronder. Dat leest
als uitgeknipt papier, zeker bij het zwarte terrein uit de Maker. De golvende rand (`GOLF`, kop
"golvende rand: terreinmassa's met een organische omtrek") doet het anders, en is opt-in per level
met `golf: true` of `golf: {ruw}` (Test 49). Zonder het veld tekent elk bestaand level zoals het
tekende; er is geen gedeelde code gewijzigd, alleen een aftakking op vier plekken.

Het recept, voor elke rand hetzelfde:

1. **De lijn golft.** Drie lagen ruis over elkaar (`golfRuis`, een som van sinussen): een lange
   deining, een middelgolf en een fijne rimpel (`golfLijn`). De seed komt uit de wereld-x, dus de
   rand hangt aan de wereld en golft niet mee als je loopt. `ruw` in het levelveld schaalt alle
   amplitudes; 1 is de maat uit `GOLF`.
2. **Druipstenen groeien uit de lijn** (`golfDruipLijst`, `golfDruip`): om de `stap` wereld-px met
   een kans een bult onder de lijn, in dezelfde polylijn, zodat de contour er gewoon omheen loopt.
   Hoe minder ruimte eronder (Amir plus `GOLF.vrij`), hoe korter hij wordt; onder de 12 eenheden
   valt hij weg.
3. **De textuur vult de vorm.** De lijn is een clippad, de tegel (`golfTegel`, gebakken met
   `grotTegelMaak` zodat hij naadloos blijft, en zo nodig donkerder) ligt eronder, vast aan het
   wereldanker. Breedte van een tegel in eenheden (`GOLF.tegel`), dus de korrel schaalt mee met Amir.
4. **Een dunne laag van een ander materiaal langs de rand**, die de golf volgt (`golfBandPad`): zand
   op de grond en als kap op een mesa, aarde onder een dak, de lichte looprand op een gangvloer. Met
   een dunne naad eronder (`golfContour` 1,2 px).
5. **Schaduw aan weerskanten** (`golfStreep`: een paar steeds bredere, steeds lichtere strepen over
   elkaar, geen filter): donker in de massa naar de rand toe, een zachte schaduw op wat erachter
   ligt (de achterwand onder het dak, de grond naast een mesa), en bovengronds een lichtrand op de
   kruin. En een contourlijn van 2,5 px.
6. **Stukken die de lijn kruisen** (`golfKeien`, `golfHangblokken`): keien uit de grotset met hun
   voet een deel van hun hoogte in de massa (`zak`), hangblokken met hun vlakke bovenkant in het
   steen (getekend voor de massa, zodat het steen dat stuk afdekt). Seeded, met `golfStrooi`.

Textuur: `design/golf/rots_grijs.png` (naadloos in beide richtingen, voor terras en gang) en
`design/golf/rots_bruin.jpg` (alleen links-rechts naadloos, voor de grond; verticaal verankerd aan de
kruin en nooit verticaal herhaald, zie `tools/golf_textuur.py`), plus `design/savannesand.jpg` als
zand. Ze laden lui (`golfLaad`, `golfLaadLevel` in `laadLevel`), samen met de grotset voor de keien.

### De vier plekken

| rand | waar | functie |
| --- | --- | --- |
| de kruin van de savanne | `scene()`, in plaats van de grondrand-tegels, binnen dezelfde gaten-clip | `golfGrondTeken` |
| het dak, de vloer en de wand van een gang | `drawHolte`, plus de overgang boven het dak en de schacht van een gat | `golfHolteSet`, `golfDakTeken`, `golfVloerTeken` |
| een rotsterras (mesa, trede) | `drawClimb`, in plaats van `terTeken` | `golfTerrasTeken` |
| zwart terrein | `rotsLaag`, in plaats van de kartel en `zwartTanden` | `golfZwartTeken` |

De botsing verandert nergens: de looplijn ligt op `groundY`, de kruin golft daar `GOLF.grond.amp`
eenheden omheen boven de zichtbare kruin (`edgeCrust`), en Amir staat met zijn voeten in het zand
zoals altijd. De zijkanten van een terras golven naar binnen (de botsing blijft op `xl` en `xr`), de
onderkant van een dak hangt 0 tot twee keer de amplitude onder de daklijn, het dak en de vloer
botsen waar ze botsten. Onder een zwart plafond geldt `ZWART_TAND_KOP` zoals bij de tandjes.

In de gang is het steen grijs in drie helderheden (`GOLF.licht`): de achterwand diep, het dak en het
grondpakket erboven lichter (dichterbij), de vloer ertussenin met een bijna lichte looprand. Het dak
en de overgang van aarde naar steen (`holteOvergangStrook`) gebruiken dezelfde tegel op hetzelfde
anker, dus daar zit geen naad; daarom krijgt die buffer de naam van de tegel in zijn sleutel.

Nog niet golvend: de savannelagen (`grond: true`), de grotten (`grotten`), de plafondlijn
(`plafond`), de rijzers, het zakplafond, de zuilen en de putten. Die tekenen in een golf-level zoals
altijd. Ook de Maker toont de golf nog niet op het grid; een level uit de Maker krijgt hem met
`golf: true` in de Spel-JSON.

### Afstellen

Alles staat in `GOLF`: per rand `amp` (eenheden), `lang` en `kort` (golflengtes in wereld-px), de
laagdikte (`zand`, `aarde`, `loop`), de druipstenen (`stap`, `kans`, `breed` in wereld-px, `diep` in
eenheden), de keien (`stap`, `kans`, schaal `s`, `zak`), de contour en de schaduwen. `GOLF.stap` is
om de hoeveel schermpixels de lijn een punt krijgt (4).

Test 49 laat alles zien, zonder vijanden. `tools/speelrobot.js "Test 49" --shots map` geeft
schermafdrukken onderweg.

## golvende rand: terreinmassa's met een organische omtrek

`golf`: het levelveld, de vier haakpunten, de texturen
