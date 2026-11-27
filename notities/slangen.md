# Slangen

## slangen: kleur, zicht en patrouille

`SNAKE_DIRS`, `slangZiet`, `startPatrouille`, `slangSchuif`. De zwarte slang (`k: 'zwart'`) en de knockslang (`k: 'knock'`) zijn spuwers: ze bijten niet maar spuwen gif (`spit`, `updateVenom`), blijven op afstand, draaien om bij een ravijn en volgen je ook buiten beeld. Of een slang een spuwer is beslist `spuwer(s)` (gebruik die, niet `=== 'zwart'`, voor nieuw spuwer-gedrag). De knockslang is jade/violet (`enemies/slang1_knock/`, een recolour van slang1) en zijn goo (`enemies/slang1_knock/venom.png`, `venomKnockImg`, `v.knock` op elke druppel) doet geen schade maar duwt Amir `KNOCK_CELLEN` level-maker cellen terug (`knockVenomRaak`, zet de bestaande `knock`-snelheid); die terugstoot duwt gewoon door, ook een ravijn in of een platform af. Test 43 is het proefstuk

## de dood van de slang

`SLANG_DOOD`, `slangDoodStap`, `slangDoodTeken`, `slangDoodImg`. Een slang die sterft speelt een doodsanimatie uit Grok: de kop zakt weg, de ogen gaan dicht en hij valt plat. De frames staan als `dood_00..16.png` in `enemies/slang1_zand/`, `enemies/slang2_roet/` en `enemies/slang1_knock/`, op een canvas van 380 x 140: het gewone frame (255 x 140) staat erin op x 45, zelfde schaal en grondlijn, omdat het lijk langer is dan de levende slang. Uit dezelfde frames komen twee sets: **gewoon** (14 frames, 83 ms) en **snel** (8 frames, 60 ms, hij klapt meteen neer). Welke, en wat het lijk krijgt, hangt af van de kill (`s.ddSoort`, gezet in het slangenblok van de tekenlus):

| kill | set | op het lijk |
| --- | --- | --- |
| speersteek (`steek`) | gewoon | snee recht, 7 druppels |
| lage zwaai (`laag`) | gewoon | snee dwars, lager op het lijf, 5 druppels |
| worp (`worp`) | snel | geen snee, 8 druppels |
| grondklap (`klap`) | snel | geen snee, 2 druppels |
| stokken (`stok`) | gewoon | geen snee, 1 druppel |
| al het andere (Nyundo, co-op) | gewoon | geen snee, 3 druppels |

De witte flits is de bestaande (`s.flash`). De druppels vliegen van Amir af en blijven als spatjes op de grond liggen. Het lijk ligt `SLANG_DOOD.lig` (3 s) en vervaagt dan in `SLANG_DOOD.vervaag` (0,8 s). Zijn de doodframes er niet (nog niet geladen), dan valt hij terug op de oude dood (wegglijden en vervagen). De fosforslang heeft zijn eigen update en houdt de oude dood.

Hoe de frames gemaakt zijn: een Grok-clip vanaf frame 46 van `enemies/slang1/snakemove.mp4`, gekeyd, het zwevende achterlijf per frame op de grond gezet, geschaald met 0,56 en uitgelijnd op `move_1` (IoU 0,95), daarna omgekleurd zoals `tools/slang_kleur.py` (op de grote clip, dan verkleind, zodat het oog klopt).

## Het bloedgeluid bij een treffer

Een slang die geraakt wordt met de punt of de kling (steek, worp, lage zwaai met de speer) geeft een bloedgeluid: een
stuk van `sounds/bloedspuit.mp3` vanaf 0,27 s, met een eigen Audio (`SLANG_BLOED`, `slangBloedSpeel(dood, soort)`). De
hardheid volgt de treffer: een treffer die hem nog niet doodt (met `hpBalk`) is klein, kort, zacht en wat hoger (`raak`);
de dodelijke is langer, voller en harder, per soort dood zoals de animatie (`dood`: de worp, die hem neerklapt, het hardst,
dan de steek, dan de lage zwaai). Niet met de stokken (die geven de houtklap), niet met de grondklap en niet met het mes
(dat weert af). De fosforslang (`fosforRaak`) heeft het niet.

Bij de dodelijke treffer komt daar de laatste sis achteraan (`SLANG_SIS`, `slangSisSpeel`): een slang heeft geen stem,
dus zijn doodskreet is zijn sis (`music/snakehiss.mp3`), maar stervend. Net na het bloed, lager afgespeeld, de toon zakt
tijdens het afspelen verder weg (`preservesPitch` uit) en hij fadet snel uit. Per soort: de worp kapt hem af (0,22 s), de
steek laat hem wegebben (0,65 s), de lage zwaai zit ertussen. Een plof van het lijf als hij neervalt zit er nog niet in.

## de slangenkop eraf (KOP, 27-11-2026)

`KOP`, `kopMag`, `kopStart`, `kopRustig`, `kopKnikker`, `kopTraagNu`, `kopStap`, `kopLensPos`, `kopLensTeken`, `kopWereldTeken`,
`kopStompTeken`, `kopZoef`, `kopReset`. Ontwerp van Tom; zie ook het projectdocument `claude/slang_onthoofding.md`.

- **Wanneer**: alleen een kill met slag 2 van de stokken (`atkStok === 'slag2'`, de zijwaartse hook) op een zand-, zwarte of
  knockslang (`SNAKE_DIRS`; de fosforslang heeft een eigen update en doet niet mee), niet in PvP. Is het rustig, dan gaat de
  kop er altijd af (de grote versie, Tom 27-11); is het druk, dan uit een knikkerzak `KOP.kans` 1 op 6 de kleine (regel 16). De stapslag (de eerste slag) doodt een slang die opkomt om te bijten al in een klap; Tom
  koos (27-11) om het toch alleen bij slag 2 te houden. Slag 2 stapt een eind door, dus een slang net buiten het bereik van
  de stapslag is de kans.
- **Rustig of druk** (`kopRustig`): rustig is geen levende vijand binnen `KOP.rust` (600) wereld-px op Amirs niveau
  (`KOP.laag`), geen Nyundo, en geen gif, bout of dolk in de lucht (`venom`, `krbPijlen`, `banDolken`).
  - Rustig, de grote versie: hitstop 0,09 s en de wereld 0,6 s op 0,35 met een korte ramp terug (`kopTraagNu`, in `loop`
    naast `dubbelTraagNu`). De kop vliegt op echte tijd (`kopStap`), in schermcoordinaten zoals `TON.lens` (plek in het
    beeldvlak plus diepte d, op het scherm 1/d groter), getekend na `tonLensTeken`. Altijd recht door de camera (`door`: d = 0,02^(u^1,25), zodat er genoeg beelden zijn waarin hij het beeld vult; onscherp; voorbij
    als hij 2,6x de beeldhoogte is). De versie rakelings langs (`langs`) zit alleen nog in de sandbox (Tom: de kop vliegt
    altijd naar de camera). Hij stopt nooit op de lens (Tom). Door de camera: een rode flits van 0,06 s en spatten op de
    lens (`lensSpatMaak`/`lensSpatTeken` met `KOP.lens`) die in 0,6 s weg zijn, een schok en het bloedgeluid.
  - Druk, de kleine versie (`klein`): hitstop 0,06 s en 0,3 s traag, de kop in de wereldlaag (`kopWereldTeken`, voor de
    slangen): een boog van 0,7 s een stukje naar de camera (1,3x groter, landt `KOP.klein.voor` Amir voor de grondlijn),
    een keer stuiteren en liggen tot het lijk vervaagt.
- **Geluid** (`KOP.geluid`, `kopLaadGeluid`, lui in `kopReset` als het level slangen kan hebben): bij de klap de bats
  (`sounds/houtraak.mp3`, bij de kleine zachter), bij de grote de zoef `sounds/kop_zoef.mp3` (ElevenLabs, "Airy rushing
  whoosh of an object tumbling through the air toward the listener..."); is die er niet, dan de oude ruis (`kopZoef`).
- **De kop**: vier aanzichten (zij, schuin, voor met open bek, rug), `enemies/slang_kop/<groen|zwart|knock>/kop_*.png`,
  geladen met de slang (`slangLaad`, `snk[k].kop`). Bron: een Grok-blad (post 422e6582-...), gekeyd naar
  `enemies/slang_kop/bron/`, met een fel groene nekstomp (om de moderatie); `tools/slang_kop.py` maakt de stomp vlees en
  kleurt de zwarte en knockslang om. De koppen kijken naar rechts: vliegt hij naar rechts weg, dan gespiegeld.
- **Het lijk**: de gewone doodsanimatie (`SLANG_DOOD.soort.kop`) met een gat om de kop (`destination-out` in het werkdoek,
  `KOP.gat` om `SLANG_DOOD.kop[f]`, de kop per doodframe), een nekstomp en de donkere spuit (`bloedSpuitCache.donker`) van
  het lijf af (`kopStompTeken`). Het gat is in de engine, er is geen eigen Grok-lijf zonder kop (nog te doen als het moet).
- **Test 98: Snake heads** (`STOK_LEVELS`, `slangKop: 1`: elke kill met slag 2, de rust beslist de versie). Sandbox, bij de
  stokken: **Snake head** (1 op 6, altijd, door de camera, langs, klein; `kopSb`, `KOP_SB`). Proefrit:
  `node tools/slang_kop_test.js [map]` (met `CHROME=/pad/naar/chrome` als Playwright geen eigen browser heeft).
- Nog niet: Co-op (de gast ziet het niet), en de lessen voor de grok-skill staan in het projectdocument.
