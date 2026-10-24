# Zicht: een vijand ziet je alleen als er niets tussen zit

Kop in de HTML: `// ---- zicht: een vijand ziet je alleen als er niets tussen zit (level.zicht) ----`,
vlak voor `TRIGGER`. Grep: `ZICHT`, `vijandZiet`, `zichtWaak`, `zichtKwijt`, `zichtZet`.

## Waarom

Vroeger merkte een vijand Amir op zodra die dichtbij genoeg was op x (of in beeld stond). Loop je
boven hem over een terras of een zwevende laag, of onder hem door een gang, dan werd hij toch wakker:
hij stond te dreigen, liep onder je heen en weer of duwde tegen de wand, en een spuwer bleef gif omhoog
lobben. Met het veld `zicht: true` kijkt hij echt.

## Hoe hij kijkt (`vijandZiet(s, bereik, kijk, oog)`)

- **Voor hem** (in zijn kijkrichting `kijk`, in wereld-x: 1 is naar rechts): een halve cirkel met straal
  `bereik`, en een zichtlijn van zijn ogen (`ZICHT.oog`, per soort in CHAR_H boven zijn vloer) naar het
  hoofd en naar het midden van Amir. Is een van de twee vrij, dan ziet hij je. De lijn wordt om de
  `ZICHT.stap` px nagelopen met `zichtVast`: `lkVastPunt` (dezelfde vraag als de lichtkaart: grond,
  terrassen, zuilen, de grond boven een gang, het plafond en de grotten) plus de zwevende lagen. Een kei,
  een richel, een doornbos en decor houden niets tegen, zodat een kei een schuilplek blijft (regel 7) en
  geen plek om onzichtbaar te zijn. De lijn wordt hoogstens elke `ZICHT.ververs` s opnieuw uitgerekend.
- **Achter hem**: de oude afstand op x, maar alleen als Amir op zijn niveau staat (`zichtNiveau`: de vloer
  onder Amir ligt binnen `ZICHT.niveau` van zijn eigen vloer, dezelfde vraag als `zwZelfdeHoogte`). Een
  muur achter hem houdt dus niets tegen; zo is het afgesproken.
- **Een treffer** maakt hem altijd wakker (`zichtZiet` kijkt ook naar `s.flash`).
- **Vergeten**: ziet hij je `ZICHT.vergeet` (3) seconden niet, dan gaat hij terug in rust (`zichtKwijt`).
  Een wakkere vijand kijkt verder (meestal twee keer zijn bereik), zodat hij je niet kwijtraakt omdat je
  net een stap te ver staat.

Er zit geen hoek in: de rand van een terras of laag maakt vanzelf een dode zone. Recht boven hem zie
je de grond tussen jullie, verder weg gaat de lijn schuin over de rand heen. Een man op de grond ziet je
op een terras van één trede (150) dus meestal wel: zijn ogen zitten hoger dan die trede.

## Wie kijkt zo

Alleen vijanden met `s.zicht === true`, en alleen als `ZICHT_AAN` (uit `level.zicht`, of de sandboxknop).
`zichtZet(o, sp)` zet dat bij het spawnen, in `updateSnakes` (de spawnlus) en in `sbSpawn`. Een spawn met
`zicht: false` houdt in een zicht-level de oude manier: daarvoor is die vlag, voor een testlevel dat het
nodig heeft. Wat niet uit de spawns komt kijkt niet zo: de bandietgolf, de bandiet-arena, de goudaap-arena,
het kooiduel, de baas-panter en de baviaan zijn geensceneerd en horen je te vinden. Ook de hinderlaag-bandiet
(`hurk`) en wie van boven invalt (`neer`) houden hun eigen opmaat.

| soort | rust | wakker worden | vergeten |
| --- | --- | --- | --- |
| zandslang, spuwers | begint op patrouille (`startPatrouille`) | `slangZiet`, bereik een half scherm (spuwer `SPUUG_ZICHT`) | na 3 s op patrouille; een spuwer spuwt niet blind |
| schorpioen | zijn patrouille | `stance` alleen als hij je ziet (naast de oude hoogtecheck) | gaat na zijn aanval vanzelf terug |
| fosforslangen | `rond` | een van de groep ziet je | de groep gaat terug naar `rond` |
| hyena | geen: ze komen op je af | | ziet hij je 3 s niet, dan druipt hij af (`weg`) en komt terug als hij je weer ziet; stormt niet blind; een maat stormt alleen mee op Amirs niveau |
| panter | `walk` rond zijn plek | `notice`/`spot` | terug naar `walk` met een nieuwe thuis |
| zwaardvechter | `idle`, kijkt zijn eigen kant op | `dreigen` | terug naar `idle`; `zwRoep` wekt alleen maten op Amirs niveau |
| bandiet | `idle` (de staande idle-set, `banLaadIdle`, geladen in `banLaadLevel`) | `run` | terug naar `idle` |
| schildbandiet | in zijn wacht (loop-frame 0) | `loop` | terug in zijn wacht |
| kooiman | slepen op zijn plek | slepen naar je toe | weer op zijn plek |
| meelman | wacht aan de rand | slaan, slepen of gooien alleen als hij je ziet; naar beneden over de rand kan dat | |

## Sandbox

Onder Vijanden, de rij **Zicht**: **Zicht aan/uit** (`sbzicht`) zet `ZICHT_AAN`, en elke nieuwe vijand
in de sandbox kijkt dan zo. **Toon zicht** (`sbzichttoon`, `zichtTeken`) tekent per vijand de halve
cirkel (geel als hij je nu ziet, grijs anders), de stippellijn achter hem op zijn vloer, en de zichtlijn
naar Amir (groen vrij, rood dicht). Zet er een Terras of een zwevende laag bij om het te zien.

## Nagemeten

In de sandbox, met een zwevende laag van 420 hoog en Amir eronder: elke soort blijft in rust zolang hij
boven staat (en de rand tussen hen en Amir zit), en komt in actie zodra hij op Amirs niveau staat. Een
zwaardvechter waar een blok tussen komt is na 3 s terug in `idle`. De Poorten speelt voor de speelrobot
precies als voor deze wijziging (het veld staat er niet in).
