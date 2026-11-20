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

Een slang die geraakt wordt met de punt of de kling (steek, worp, lage zwaai met de speer) geeft een klein bloedgeluid,
ook bij een treffer die hem nog niet doodt (met `hpBalk`). Het is een kort stuk van `sounds/bloedspuit.mp3` (0,27 tot
0,62 s, zachter en op 1,25 keer het tempo, met een eigen Audio), zie `SLANG_BLOED` en `slangBloedSpeel`. Niet met de
stokken (die geven de houtklap), niet met de grondklap en niet met het mes (dat weert af). De fosforslang (`fosforRaak`)
heeft het niet.
