# Reinier, de bijlveteraan (elite)

`REI`, `REI_DATA`, `reinieren`, `makeReinier`, `updateReinier`, `hitReinier`, `reiTeken`, `reiOpen`, `reiStart`. Reinier is
een codenaam. Een elite-vijand (regel 12: geen baas): een oudere bandiet met grijze baard, crème tulband, groene mantel en
een bijl met lange steel. In de sandbox (rij **Reinier (elite)**, met **AI uit**) en in Test Lab, Elite tests, Reinier,
**Reinier: Test 1** (`REI_1`).

## Spelen met de kit van Co-op

Spelen (of dubbelklik op het kaartje) start de map van Reinier zoals The Clay City: als solo Co-op episode (reeks `r` in
`MPC_EPS`, `reiSpeel`, `kleiCoopStart(i, 'r')`, `pvp.rei`). Geen tribe en geen talents, de kit van Co-op (stof in de ogen
met de speer, de grondklap met de stokken, een speer op de rug). Eerst het keuzescherm: Mkuki (speer) of Bhubesi (stokken),
en Lives of Invulnerable (`duoKeuze.onst`, in het level als `onsterfelijk`). Geen winkel en geen moeilijkheid. Escape en
het eindscherm brengen je terug naar de kaartjes van Reinier (`kleiCoopStop`).

## Het gevecht

- **Rust, ren, rem**: binnen `REI.zicht` rent hij op je af (de ren-clip, `REI.renV`), binnen `REI.remAf` remt hij (de
  stop-clip, die eindigt in de tell met de bijl hoog) en schuift `REI.remDuw` door.
- **Drie aanvallen** uit een knikkerzak (`reiTrek`, trekken zonder terugleggen): kap, kap, schijn, draai, draai. De lengte
  van de tell komt ook uit een zak (0,12, 0,28 of 0,5 s). Na een aanval pakt hij 2 van de 3 keer meteen door (`kettingZak`,
  `REI.ketting`): nauwelijks een adempauze.
  - **Uitvalskap** (`reiKap`, set `uit`): grote stap naar voren en de bijl diep in de grond op frame 13 (`reiKapRaak`, `reiInslagFx`: een
    zware dreun, een stofwolk met de deeltjes van Nyundo, gruis, kluiten aarde en stof dat nog even uit de kuil walmt). Kost
    `REI.kapSchade` (2) levens. Ontwijken: wegrollen. Daarna zit de bijl vast en trekt hij hem los.
  - **Schijnkap** (`reiSchijn`, set `feint`): een ruk naar voren; rolt of springt Amir dan al (`reiAmirWeg`), dan draait hij
    zijn rug naar de camera en wacht (`houd`) tot je landt, draait terug en doet de echte uitvalskap.
  - **Draaizwaai** (`reiDraai`, set `draai`): hij draait in met zijn rug naar de camera, bijl horizontaal, stap, en een vlakke
    zwaai op heuphoogte (frame 24, `reiZwaaiRaak`, met een wit veegspoor) die doordraait tot zijn borst naar de camera staat.
    Ontwijken: springen (raakt tot `REI.zwaaiHoog`). Daarna draait hij terug met de bijl op de schouder.
- **Het strafvenster** (`reiOpen`): als de bijl vastzit (uit 14 tot 18) en als hij na de zwaai open staat (draai 29 tot 37).
  Alleen de eerste treffer telt dan `REI.strafSchade` (2), met de crit-flits (`strafGehad`); de rest gewoon. Met de vakjes (H) wordt zijn vak geel.
- **Hij leest je**: geraakt in zijn rem of tell kapt hij meteen (`reiStart(s, 'snel')`); sta je `REI.achterTijd` achter
  hem (binnen `REI.achterAf`), dan draait hij om en kapt.
- **Geraakt**: alleen de eerste klap na een rustmoment laat hem wankelen (set `hit`); daarna slaat hij binnen `REI.wankelKoel` (4 s)
  op een treffer in zijn klaarstand of ren meteen terug met een snelle kap. In een aanval onderbreekt een treffer de aanval niet.
- **Dood**: bijl omlaag, leunen, door de knieën, opgekruld voorover met de bijl plat ernaast; hij blijft `REI.doodLig` s
  liggen en vaagt dan weg. Tijdelijk: hij krijgt later een andere doodscène.
- **Leven**: `REI.hp` 14, met de health-balk. Geraakt spat er bloed naar Amir toe (`reiBloed`, druppels die op de grond
  blijven liggen), na een treffer 0,42 s onkwetsbaar.
- **Geluid** (`reiGeluid`, alles al in `sounds/`): `kooigrr` bij 1 op 3 tells, `brutus_zwaai` als de bijl neerkomt,
  `brutus_inslag` plus `kooihitground` bij de inslag, `banditpijn` geraakt, `banditdeath` dood. Volumes in `REI.vol`.

## Maat en sprites

- 12 procent groter dan een bandiet (`REI.hShare` = `BAN_H_SHARE` maal 1,12).
- `enemies/reinier/reinier.json` en de webp's komen uit de speelbare proef (Grok-clips, gekeyd en uitgelijnd op tulband en
  voeten). Per frame staat de onderkant van de voeten precies op de grondlijn (dy in de json, het blad van de bijl telt niet
  mee); alleen de zweefframes van de ren staan erboven. Alles staat in spritepixels: proefpixels maal `K` (2,2); `fig` is de hoogte van tulband tot voeten. De gedrags-
  getallen in `REI` zijn proefpixels (`reiP`), de json-waarden spritepixels (`reiScale`).
- Sets: `run`, `stop`, `feint`, `uit` (uitvalskap met lostrekken), `draai` (0 tot 23 de aanloop, 24 tot 58 de volledige
  zwaai en het terugdraaien), `hit`, `dood`. Root motion zit in de sprites; na een aanval schuift het anker (`uitDisp`,
  `draaiDisp`) en kiest hij de klaarstand van die clip (`uitR`, `draaiR`).
- Het ontwerp en hoe de clips gemaakt zijn: het projectdocument `bijlveteraan_ontwerp.md`.

## Nog niet

- Geen Co-op/Multiplayer, geen sneak, gif, stofsweep of shove-reactie, geen eigen stem (hij leent de bandiet).
- Speer in zijn rug die blijft steken (en eruit trekken voor extra schade), de omslag op de helft (tulband af, hinken),
  idle en lopen: zie het ontwerp.

## Testen

`node tools/reinier_test.js [map]`: laadt Reinier: Test 1, volgt zijn toestanden, maakt afdrukken en raakt hem dood.
