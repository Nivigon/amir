# Een gang onder de grond en hoogteverschil

### Een gang onder de grond

`holtes: [{r, l, diep}]` legt een gang onder de grondlijn, met de vloer `diep` sprite-eenheden
lager. Een ravijn uit `gaps` dat erboven ligt is de ingang: daarin val je niet dood maar kom je
op de vloer terecht. Met `valschade: true` kost een val van 600 twee levens (vanaf twee Amir,
502). Het dak is de onderkant van het grondpakket, `HOLTE_DAK` (190) onder de grondlijn.
Laat de gang aan de kant van het ravijn wat verder doorlopen dan het gat, anders staat de wand
onder de rand. Alles in de gang staat op de bodem, want `terrainH` geeft daar `-diep`.

Het licht onder de grond komt uit een plek: de lichtkaart (zie hieronder). De tegels van de
gang zijn zelf maar een beetje donker gezet (`HOLTE_LICHT`), de looprand van de vloer lichter
dan de vulling eronder. `Test 10` is het proefstuk voor het licht, `Test 4` voor de gang.

### Hoogteverschil onder de grond

Een gang die dieper wordt, of waar je klimt en weer daalt, is **één gang** met de diepste `diep`,
en de hogere stukken zijn treden: terrassen met een negatieve `h`, net als de trap naar buiten.
Je landt dan op een richel, loopt eraf naar de bodem, klimt met een kei of een richel weer op,
en daalt weer. Alles wat voor terrassen geldt, geldt hier ook; daarbovenop kapt het dak elke
sprong af op -441.

Wat niet werkt, en waarom. Elk hiervan is nagelopen met de speelrobot (zie hieronder) in een
proefgang, en `levelcheck.py` meldt ze:

- **Twee gangen tegen elkaar** (de ene dieper dan de andere). `holteBlok` houdt Amir in allebei
  tegelijk vast: op de naad duwt de ene wand hem terug en de andere ook, en daar staat hij voorgoed
  klem, ook als hij er net in is gevallen.
- **Een terras op de savanne boven een gang** (en een trede die boven de gang-vloer zweeft).
  Vroeger werd zijn wand tot onder in beeld getekend en hield hij Amir tegen, een onzichtbare
  stenen pilaar in de gang. Nu loopt Amir er onderdoor: `blockByPlatforms` slaat de wand van een
  terras over voor wie onder de grond in een gang loopt en met zijn kop onder de terras-bovenkant
  past (`ph < -40 && p.topH > ph + CHAR_H && holteAt`). Boven de grond blijft een mesa gewoon een
  wand, en een trede die je van onderaf opklimt (een trap in een gang, Test 4) blokkeert nog, want
  dan zit de volgende trede niet boven zijn kop maar op kniehoogte. Zo werkt een savanne-laag (of
  mesa) boven een gang uit de Maker nu gewoon.
- **Een kei in de gang die tot in het dak reikt.** Op een trede van -520 staat de bovenkant van
  een kei op -406, en daar mogen zijn voeten niet komen: hij komt er niet overheen en niet langs.
- **Decor dat hoger is dan de gang.** Alles staat op de bodem, ook een boom, en die steekt dan
  door het dak. Een doornbos of een dorpsplaat net zo.
- **Een ingang die maar half boven de gang ligt.** Wie aan de kant zonder gang erin stapt, valt
  recht naar beneden (in een val loop je niet meer) en is dood.
- **Een gang die de speer overdekt.** Aan het begin staat je speer op `SPEAR_AHEAD` (-260) in de
  grond; ligt daar een gang, dan staat hij beneden op de bodem en begin je zonder.
- **Een gang minder diep dan 441.** `readLevel` maakt er zonder iets te zeggen 441 van, en dan
  kloppen je treden niet meer.
- **Vallen met `valschade`.** De val door de ingang telt ook: een ingang boven een richel op -700
  kost al twee levens. Tel de vallen langs de hele route op tegen de drie levens en de kalebassen
  die onderweg liggen.

Wat het spel zelf regelt, zodat je er als ontwerper niet op hoeft te letten:

- **Water kijkt naar de hoogte.** `waterDepthAt(x, h)` geeft 0 voor wie beneden in een gang
  staat: een poel boven een gang maakt Amir daar niet nat, traag of zwak in de sprong.
- **Decor in een gang is donker.** Props, keien en doornbossen beneden in een gang krijgen
  hetzelfde licht als alles daar, want de lichtkaart ligt eroverheen. De personages krijgen er
  een deel van (`LK.personage`), zodat je ze in het donker altijd ziet.
- **Hyena's komen op de goede hoogte.** Hyena's in een gang worden pas losgelaten als Amir zelf
  beneden is, en komen dan uit de gang aanrennen (`hyBuitenBeeld`), niet van de savanne erboven.
- **Vijanden blijven in hun gang.** Voor wie beneden staat is de eindwand van de gang een rand
  (`dropAhead`): daar lopen ze niet doorheen naar boven.
