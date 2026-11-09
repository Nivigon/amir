# De oude speer

Code: de sectie `// ---- de oude speer: gespalkt en verweerd, na drie keer gebruiken breekt hij ----` (`OUDE_SPEER`,
`oudSoort`, `oudWorp`, `oudBreek`, `oudSteekStap`, `oudeSperenNeer`, `oudLos`, `oudLaad`, `oudLaadLevel`, `oudHint`).
Art in `design/speer/oud/`, uit `tools/oude_speer.py`.

## Hoe hij in de staat zit

Geen eigen vlag: de oude speer is een speersoort in `SPEER_SOORTEN` (`oud3`, `oud2`, `oud1`, het cijfer is hoe vaak
hij nog kan). Die soort-id gaat mee in het veld dat al het vaantje droeg: `speerBlauw` (de hand), `rugSperen[].blauw`,
`losseSperen[].blauw`, `jav.blauw`, `javLostBlauw`. `vaanBlauw(img, aan)` en `speerSoortId` lezen een string als soort,
`true` als de blauwe skeletspeer en `false` als de gewone. Overal waar het vaantje met `!!` platgeslagen werd, staat nu
`|| false`, zodat de stand niet verloren gaat.

## Gebruik en breken

- **Worp** (`oudWorp` in `looseSpear`): de geworpen speer krijgt de stand na de worp. Was het de laatste (`oud1`), dan
  krijgt hij `jav.breek` en valt hij in `javStick` in stukken (`oudBreek`: splinters van het takelwiel en `houtraak.mp3`),
  waar hij ook neerkomt. In een ravijn komt hij niet terug (`javLostBlauw` `'kapot'`).
- **Steek** (`oudSteekStap`, elk beeld na `rugUpdate`): de eerste keer dat `swingUsed` in een stoot aangaat telt, een keer
  per stoot (`oudSteekGeteld`, terug op false in `startAttack`). Ook een parade van een bandiet telt: je speer kreeg een tik.
  Het mes (`atkMes`) en de lage zwaai tellen niet. De laatste breekt in je hand; heb je er een op je rug, dan trek je die.
- Raap je je eigen geworpen speer weer op (`eigenSpeerPak`, de vangnet-terugkeer, `javStick`), dan houdt hij zijn stand.

## Het beeld

`speerKleur` geeft voor een oude soort bij `javImg` (liggend: de worp, de rug, een losse speer) en `spearImg` (in de
grond) het eigen plaatje `jav_n.png` / `grond_n.png`. In Amirs handen zit de speer in zijn sprites, dus daar kleurt
`speerVerf` alleen het lint vaal bruin (`vaan` met `dof`). De draaiende speer (de draai-frames) slaat hij over: de oude
speer vliegt plat.

Stand 3 is verweerd met een touw om een barst, 2 heeft een tweede touw en meer roest, 1 is gebroken onder het touw en
de punt is geschilferd. Uit de keuze van 09-11-2026: ontwerp 2 (gespalkt) met de roest van 3.

## In een level

`oudeSperen: [{x, n, f}]`: losse oude speren op de grond, `n` hoe vaak nog (standaard 3). Zo'n level begint met een
lege rug. Alleen Test 64 heeft het (met `geenSpeer` en `rugMax: 2`).

## Sandbox

Speer en spullen, **Oude speer**: **In de hand** (`sboudhand`), **Drie voor je** (`sboudlos`, met nog 3, 2 en 1 keer) en
**Rug vol oude** (`sboudrug`, zet eerst de rug aan).

## Later

De winkel: een oude speer te koop, die op je rug gaat als daar plek is (de oorspronkelijke vraag).
