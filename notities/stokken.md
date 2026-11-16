# De stokken

Een tweede wapenset voor Amir: twee slanke stokken met een leren greep (Nguni-stokvechten), in plaats van de speer.
In Test 74 (`stokken: true`), de sandboxknop **Stokken**, en in Multiplayer als keuze per speler (zie "Het wapen" in
`notities/multiplayer.md`).

## Frames
- `karakters/amir/stokken/<set>/<set>_NN.png`, sets `rennen` (12), `staan` (1), `slag` (18), `stapslag` (28), `slag2` (27), `draaislag` (15),
  `draaiterug` (6), `blok` (13). Een gedeeld canvas 440 x 328, anker 256, grond 323, schaal 1 (Amirs spelschaal),
  alles kijkt naar links. `metadata.json` heeft de ms per frame.
- De vechtsets (slag, draaislag, draaiterug, blok) zijn groter getekend dan staan en rennen. Het spel tekent ze op
  `STOK.maat` 0,9 (`stokMaat`, `stokSetNu`): gemeten op de hoofdbreedte (0,875), de voeten (0,85) en in het spel naast
  de speersteek (0,92). Eerst stond het op 0,8, gemeten op de hoogte van het hoofd, maar dat staat in de vechtframes
  schuin en gaf een te kleine Amir. Het hitpunt (`steekDX`, `steekY`) schaalt mee; `reik` niet.
- Gebakken uit de Animeer tool Amir stokken (https://claude.ai/artifact/W4e5eqpQ5PEfBRKZPzpWog): het lijf uit Grok-clips
  met groene stokken (verwijderd), de stok als item geplaatst door de opdrachtgever, en met de tool zelf samengesteld
  (dezelfde `compose`). `plaatsing.json` is de export van de tool (per frame stok_voor en stok_achter): de bron als de
  stok later een losse laag wordt om om te kleuren of te upgraden.

## De nieuwe stok (gebrand oker)
- Donker hardhout met drie lichte ringen bij de slagkant en een grip van doek in gebrand oker (170,108,40), waarvan de
  twee slippen aan de onderkant van de grip hangen. Uit Grok (`bron/stok_grok.jpg`, de grip en de slippen in egaal geel
  #FFFF00 zodat ze om te kleuren zijn), op de lijf-frames uit de Animeer tool (`bron/lijf/`, het lijf zonder stokken).
- `tools/stok_bak.py` bakt de speelframes: dezelfde samenstelling als de Animeer tool (`plaatsing.json`: de plek, de
  draaiing en de maskers per frame), de grip van de nieuwe stok in de vuist waar de oude grip zat, 155 px lang (1,35 keer
  de oude) en 1,15 keer zo dik. Opties `--kleur`, `--lengte`, `--dikte`, `--slip`; daarna `gen-klein.py` en
  `gen-offline-manifest.py`. Het script ruimt ook de olijfgroene en paarsroze resten uit de clips op.
- Gemeten koppeling Animeer naar spel: 41 px naar links en 26 px omlaag; de vechtsets staan in de Animeer tool gespiegeld
  (naar rechts), en draaiterug is draaislag 13, 11, 9, 6, 3 en 1. Het canvas groeide mee met de langere stok:
  498 x 354, anker 285, grond 349 (`STOK.W`, `H`, `ANKER`, `GROUND`).
- De slippen zitten niet in de frames: `slip.png` hangt aan de knoop (`STOK.slip.punt`, per frame per stok x, y en of
  die stok achter Amir valt, geschreven door `stok_bak.py`). Per stok een slinger (`stokSlipStap`, `stokSlipTeken`):
  de knoop die over het scherm versnelt zwaait hem de andere kant op, de rijwind (`STOK.lucht`) blaast hem naar achter,
  een vlaag (`windAt`, `STOK.wind`) neemt hem mee. Zwaarte, lengte en demping: `STOK.zwaar`, `lang`, `demp`.

## Spel
- `STOK` (tempo, actieve frames, hitpunt en reik per slag, blok, venster, stun), `stokAanval`, `stokStap`,
  `stokBlokStap`, `stokBlokVang`, `stokBeeld`, `stokTreffer`.
- De slag loopt op `atkFrame` met `atkStok` (zoals `atkCombo`), dus `steekLive`, `steekDX`, `steekY`, `steekR` en
  `steekEind` gelden vanzelf voor elke vijand.
- De stap: onder de opzwaai van de gewone slag schuift Amir naar voren, zodat hij in de klap stapt (`STOK.stap`,
  `stokSchuif`, `stokStapK`). 90 frame-px (zo'n derde Amir) verdeeld over slag-frames 0 tot 5, langzaam op gang en de
  meeste vaart vlak voor de treffer op frame 6, met een wolkje stof bij de voorvoet op frame 5. Een gebufferde tweede
  slag stapt `vervolg` (0,6) zo ver, de counter stapt niet. Niet in de lucht en niet over de rand van een ravijn
  (`gatOp`); muren en de klif klemmen daarna zoals bij lopen. Alleen de engine: de voeten in de frames blijven staan.
  In de sandbox de knop **Stokstap** (aan of uit) om te vergelijken.
- De stapslag (doorstap): de eerste slag (niet gebufferd) is `stapslag` (28 frames, Grok-clip 3.mp4, elke tweede
  clipframe van 8 tot 62, zonder eindframe gegenereerd: met een eindframe in de oude stand wisselde Grok de benen). Het
  achterste (rechter)been stapt door en landt voor, dan de slag van boven, de klap op frame 25-27. Hij stapt niet terug
  (Tom: een versie die achterstevoren terugstapte was te traag en ongewenst); na de laatste positie staat hij in zijn
  gewone houding op de plek waar de stap hem bracht (zo'n 74 wereld-px verder). `STOK.stapslag.seq` kiest per positie
  het frame (de stap om het andere frame, voor het tempo), `STOK.ms.stapslag` per positie: de klap na zo'n 0,36 s, klaar
  na 0,53 s. Root motion: `STOK.stapslag.root` (frame-px per frame, de geplante voet vastgezet; eerst de oude voorvoet,
  na de landing de nieuwe), `stokRoot` schuift per positie met het verschil. Een gebufferde tweede slag (vanaf positie
  `buf` 19, begint op `annuleer` 21) is de gewone `slag` op de plek. De stapslag duwt een bandiet echt terug (`STOK.stapslag.knock` 250, zo'n 65 px, in plaats van de verkleinde knock van
  de reeks), en de stap houdt op met schuiven als er een vijand binnen `stop` (0,45 Amir) voor hem staat (`stokVijandVoor`),
  zodat hij niet door hem heen stapt. Gemeten met een stilstaande bandiet op 90 en 150 px: de stapslag en de tweede slag
  raken allebei (tussen 79 en 99 px na de stap). Sandboxknop **Stapslag**.
  Het canvas groeide voor de opgeheven stok: 511 x 384, anker 298, grond 379 (links 13 en boven 30 erbij; de andere
  sets zijn daarvoor opgevuld en hun slip-knopen mee verschoven). Gebakken met `tools/stok_bak.py --alleen stapslag
  --canvas 511,384,298,379`. De vlekjes op de vacht zijn op de rugframes (19-27) weggehaald (Tom). Verwerking: zie het
  projectdocument `claude/animeer_tool_stokken.md`.
- Slag 2 (16-11-2026): een tweede slag vlak na de stapslag (gebufferd vanaf positie `STOK.stapslag.buf`, begint op
  `annuleer`) is `slag2` (27 frames, eigen set): het achterste been stapt nog een keer door, de linkerstok zakt horizontaal
  achter zijn rug en zwaait vlak, op borsthoogte, zijwaarts voor hem langs (een hook); de rechterstok gaat omhoog als
  dekking. Zelfde opzet als de stapslag: `STOK.slag2.seq` (16 posities, de stap om het andere frame), `STOK.ms.slag2`,
  `root` (stokRoot schuift de wereld mee), `buf` 11, `annuleer` 14, `landt`, `stop`. De klap (posities 11-13) komt na
  zo'n 0,19 s en hij is na 0,58 s klaar, ongeveer het tempo van de oude tweede slag (0,16 s en 0,65 s). Hij stapt wel
  verder: zo'n 140 wereld-px tegen 74 bij de stapslag. Een gebufferde derde slag is weer de gewone `slag`. Schade een
  halve, net als de slag; de reeks (STOK.reeks) telt hem als de tweede treffer. Sandboxknop **Slag 2** (aan of uit).
  Herkomst: Grok-clip 4 (start = doorstap-clipframe 62, 2,4x opgeschaald) voor de doorstap, Grok-clip 5 (start = een
  tussenframe met de stok schuin voor de borst, geen eindframe) voor de zwaai; de lijf-frames staan in
  `bron/lijf/slag2_NN.png` en de stokken in `plaatsing.json` (uit de Animeer tool). In de frames zit een schuif van 110
  Animeer-px naar achteren tijdens de stap, zodat de klap met de lange stok in het canvas past; die zit ook in `root`.
  Gebakken met `tools/stok_bak.py --alleen slag2`.
  Ramen (16-11-2026, Tom: bij F rammen zag je de linkerslag niet): de derde slag mocht al op positie 14 beginnen,
  zodat de klap maar zo'n 0,12 s in beeld stond, en bij elke overgang sprong Amir terug, omdat elke set anders in
  zijn canvas staat. Nu begint een gebufferde derde slag pas op `annuleer` 15 (de klap staat zo'n 0,2 s), en houdt
  `stokAnker` de voeten op hun plek bij de overgang van de ene slag in de volgende, van slag 2 en de stapslag in de
  houding, en van slag 2 of de stapslag in het blok: de wereld schuift het verschil van `STOK.voet` (het midden
  tussen de voeten per frame, gemeten op de speelframes) mee. Van staan naar een eerste slag schuift niets. Hoe de Grok-prompts liepen: projectdocument
  `claude/animeer_tool_stokken.md`.
- Blok: C vasthouden (op een telefoon de schildknop). Vanaf blok-frame `STOK.blokOp` vangt `hurtPlayer` een klap van
  voren af (houtklap, duwtje). Projectielen met een eigen schade-ingang (bouten, de speer van de schildbandiet) vangt
  het nog niet.
- De stun-counter klinkt en voelt harder: een stapel lage houtklappen met een naklap en het bloedgeluid
  (`STOK.stunKlap`), meer hitstop en schok, en een kleine bloedspetter op de lens bij het trefpunt die binnen 0,7 s
  wegtrekt (`STOK.lens`, `stokLens`, `stokLensTeken`). De lens-code van Nyundo is daarvoor algemeen gemaakt
  (`lensSpatMaak`, `lensSpatTeken`). De gewone counter (`gewoon`) houdt de oude klap.
- Twee keer slaan: na de eerste treffer met de slag wankelt een bandiet (`STOK.reeks`): geen dekking, geen aanval
  (`rust` 0,75 s) en minder ver terug (`reeks.knock` 0,7 van de gewone knockback; was 0,4, maar sinds de stap naar voren voelde dat als geen knockback), zodat de tweede slag erin gaat. Pas de tweede treffer binnen 1,1 s geeft de
  gewone dekking van 1,15 s (`BAN_INV_T`). Een druk vanaf slag-frame `STOK.buf` (6) staat klaar en de volgende slag
  begint al op frame `STOK.annuleer` (11), zonder de rest van het herstel (`stokBuf`, `stokBegin`). Gemeten met een
  robot die 8 s F ramt tegen de eerste elite: eerst 3 treffers, nu 5 en hij is dood.
- Het ritme: klap, klap, blok, counter. De slag is een halve treffer, de counter een hele (`STOK.schade`, `stokSchade`
  in `hitBandiet`; de sluipaanval blijft in een klap dood). De slag loopt op tempo 0,65 (was 0,75). Vanaf slag-frame
  `STOK.annuleer` breekt C het herstel af, zodat je na de tweede klap meteen kunt blokken. Na de reeks zet hij na
  `reeks.naRust` (0,2 s) in, het wankelen na de eerste klap is `reeks.rust` (0,5 s), en na de gewone counter wankelt hij
  `STOK.counterRust` (0,6 s), want Amir zit na de draaislag en het terugdraaien nog zo'n 0,85 s vast. Gemeten met een
  robot die het ritme speelt tegen de eerste elite (5 levens): drie rondes, Amir nooit geraakt. Van de tweede klap tot
  zijn kling op het blok zit zo'n 0,95 s, want hij moet na het terugduwtje eerst weer inlopen.
- Een bandiet die op het blok slaat glijdt niet meer door Amir heen: zijn doorschuif stopt en hij kaatst
  `STOK.blokTerug` terug (`stokBlokGestuit`, herkend aan `stokBlok.vang`, dat `stokBlokVang` ophoogt).
- De counter slaat ook in `hitBandiet` door zijn dekking (`doorDekking`), en `stokTreffer` (klap, stun) volgt alleen
  op een echte treffer.
- Counter: slaan tijdens het blok of binnen `STOK.venster` na het loslaten of na een gevangen klap. De draaislag gaat
  door de dekking van de bandiet heen (`stokDoor`), daarna speelt `draaiterug`. Met `stokKeuze` kies je
  `duoKeuze.stokCounter`: `stun` (bandiet `rust` 2 s, `knock` terug, `inv` 0 en sterretjes via `stokStun`) of `gewoon`.
  Zolang `stokStun` loopt staat hij in de staande idle (wankelen, niet rennen op zijn plek), ook terwijl hij terugglijdt;
  daarna weer `run` op Amir af (`stokStunIdle`, `banIdleKlaar`: alleen als de idle-frames binnen zijn).
  Boven zijn health-balk staat dan STUNNED in geel, dat zacht naklopt en in de laatste 0,3 s vervaagt, en eronder een geel
  balkje dat in de duur van de stun leegloopt (`stunLabelTeken`, in `vijandHpBalk`).
- Een spawn met `hp` (zonder aanvoerder) geeft een bandiet zoveel levens; Test 74 gebruikt de elite-garde met 5, zoals Co-op.

## Waarom het nog niet lekker voelt (analyse)
- Staan is ontspannen, elke slag en het blok beginnen in een diepe gevechtshouding: bij elke actie springt de pose.
  Een wachthouding als stilstaan (in gevecht) zou dat gladstrijken; daar is nog geen frame voor.
- De slag duurt 0,71 s, raakt pas na 0,19 s, en daarna 0,35 s herstel plus `rust` 0,12: bijna een halve seconde dood.
  De tweede stok doet niets. (Opgelost voor een tweede slag: de buffer, zie hierboven.)
- Na een treffer stond de bandiet 1,15 s in dekking (`BAN_INV_T`), dus de tweede slag werd bijna altijd gepareerd:
  raak, clang, raak. (Opgelost met de reeks, zie hierboven.)
- De counter is gratis: elk blok dat je loslaat (vanaf frame 8) opent het venster, ook zonder gevangen klap.
- In de draaislag vallen de raakframes (3 tot 6) voor de zichtbare draai (8 tot 14); de draai is uitloop, en met
  draaiterug sta je ruim een seconde vast.
- Slag-frame 6 had een paarsroze stok (een vlek uit de clip); met de nieuwe stok is die weg. Een paar paarsroze
  vlekjes bij de handen (slag 13, draaiterug) zitten nog in het lijf zelf.

## De ren met stokken (16-11-2026)

De oude renset (8 frames) zette de stokken per frame in een andere hoek, waardoor ze alle kanten op vlogen. Grok kon
geen guard vasthouden tijdens een ren (de armen gingen altijd pompen), dus de nieuwe renset is geknipt en geplakt:
- benen en heupen: de 12 frames van de nieuwe ren (`REN_NIEUW`, test4);
- bovenlijf: Toms guard-pose (voorste onderarm dwars voor de borst, stok schuin omhoog over de schouder; achterste arm
  achter op heuphoogte, stok schuin omlaag naar achteren), uit een Grok-still op 1728 px, op de tailleband gezet;
- leven: het bovenlijf kantelt 3 graden mee met de pas, de stokken veren 5 en 7 graden na (iets na het lijf).
Test 74 heeft `nieuweRen: true`, zodat de stokkenren gelijk oploopt met de looplus en het tempo de snelheid volgt.
Zonder nieuwe ren (de sandboxknop Stokken alleen) wordt de oude lus van 8 over de 12 frames uitgesmeerd (`stokBeeld`).
Scripts uit de sessie: /home/claude/stok/puppet2.py (tilt 3, stokken 5 en 7).
- Vuisten (16-11-2026): Grok had de vuisten om de gespiegelde diagonaal getekend. Nieuwe still van Grok vanaf een collage met de groene stokken al in de goede hoek (de handen om de stokken laten sluiten); lijf en vuisten daaruit, de vuisten als bovenste laag met gaten waar het groen zat, zodat de stok door de vuist loopt (/home/claude/stok/puppet3.py).

## Bukken en kruipen met de stokken (16-11-2026)

- Gebukt en kruipend tekent het spel met de stokken aan de sets `bukken` (12) en `sluipen` (28) uit de stokbank in plaats van
  de speerloze buk- en kruipframes (`stokLaag`, in de tekenlus gekozen waar anders `stokBeeld` niets geeft). Bukken: frame 0-7
  is het zakken (`duckT`, zoals `duckFrame`), 8-11 het vasthouden (`DUCK_HOLD_SEQ`); sluipen volgt `crawlFrame`.
- Het lijf is de bestaande speerloze set (`beweging/bukken/bukken`, `beweging/sluipen`), op schaal `JMP_S` (0,45) naar het
  Animeer-canvas gezet: midden op x 297, de grondrij (637 min `DUCK_DROP`, en 411 voor het kruipen) op y 297. Staat in
  `bron/lijf/bukken_NN.png` en `sluipen_NN.png`; de plaatsing uit de Animeer tool staat in `plaatsing.json`.
- Plaatsing (Tom): sluipen met beide stokken onderhands langs onderarm en dij naar achter, de borststok achter het lijf; als
  de hand op de grond steunt ligt de stok plat onder de hand. Bukken: de stokken hangen eerst omlaag, dan een stok bij de kin
  en de andere plat onder de geplante hand.
- Bakken: `python3 tools/stok_bak.py --alleen bukken,sluipen`, de regels `bukken` en `sluipen` in `STOK.slip.punt`.
- Open: in de vasthoudframes van het bukken (8-11) draait de kinstok van vlak naar voren tot rechtop; in de ademlus
  (`DUCK_HOLD_SEQ`) zwaait hij dus heen en weer.

## De grondklap (16-11-2026, Test 76)

Met de stokken in de lucht omlaag plus aanval (`GK`, `gkKan`, `gkStart`, `gkLucht`, `gkLand`, `gkStokStap`, `gkInslag`,
`gkUpdate`). Alleen in een level met `grondklap: true` of met de sandboxknop **Grondklap** (`sbGrondklap`), naast de stokken.
- Frames: set `grondklap` (26 frames, Grok-clip deze.mp4: begin lucht_links, tussenframe tussen_links met de armen geladen
  achter het hoofd, eind inslag_links met het hoofd tussen de stokken), gebakken met `tools/stok_bak.py --alleen grondklap`
  uit `bron/lijf/grondklap_NN.png` en de stokken uit `plaatsing.json` (startplaatsing uit het groen van de clip; op de
  laatste frames schuift de stok 28 px door de vuist omlaag, zodat de vuist bovenop zit en de punt bij de grond komt).
  `STOK.grondklap.seq` kiest per positie het frame: 0-8 de opzwaai, 9 het tussenframe, dan 17, 19, 21, 23, 24 en 25 (het
  contactframe). Frames 10-16 (het neerkomen van de benen) zitten in de set maar spelen niet: die vallen in de val.
  `STOK.grondklap.voet` zet in de luchtframes de voeten op de echte hoogte (de clip heeft de sprong erin).
- Verloop: in de opzwaai hangt hij stil (`pvh` 0, posities 0-8, zo'n 0,3 s), daarna houdt hij het tussenframe vast en valt
  hij met `GK.val`. Bij de landing (`updateJump`, `gkLand`) springt hij naar positie 10, en op positie 15 (het contactframe)
  is de klap (`gkInslag`): hitstop, schok, stof bij allebei de stokpunten (ook om te verbergen als een punt de grond net niet
  raakt), steentjes, het geluid, en de golf. Het contactframe blijft 320 ms staan, dan de gewone houding (geen opkomen: de
  freeze en de golf dekken de wissel), en `GK.koel` afkoeling: 8 s, een grondklap per 8 s. In de actiebalk staat hij
  als vak `grondklap` (toets ↓+F, de taartpunt telt af); probeer je hem te vroeg, dan schudt het vak en sla je gewoon.
  Geraakt worden breekt hem af.
- Het geluid (gerecycled): `brutus_inslag`, `kooihitground` en `ton_zwaar` tegelijk, twee lage houtklappen en een korte
  beving (`bavBeving`).
- De golf: begint bij de punt van de voorste stok (`STOK.punt.grondklap`), rolt met `GK.golfV` vooruit tot het gekozen
  bereik (`GK.bereik`, in Amir-hoogtes: kort 1, middel 2, lang 4) of tot een trede of terras (30 hoger of lager). Hij raakt
  via het vak van de lage zwaai (`gkVak` als `swbox`, met een nieuwe `sweepId`), dus elke vijandsoort met de lage zwaai
  doet mee, een keer per klap. Op de klap van vlak achter Amir tot de stokpunt, daarna alleen de strook die het front net
  passeert (wie er later inloopt krijgt niets). Schade via `fcHalf` (`gkSchadeOp`): de gekozen schade (0,5, 1 of 1,5) in
  plaats van de hele treffer van de handler, recht onder hem (tot `GK.onderR` voorbij de stokpunt) `GK.onder` erbij.
  Daarna (`gkNaTreffer`) terug met `GK.knock` (onder hem `knockOnder`), wankelen `GK.rust` en traag `GK.traag`; slangen en
  schorpioenen wippen omhoog (`gkH`, in hun tekencode).
- Beeld: de bult in de vloer is de truc van Nyundo (`gkGrondTeken`, voor Amir getekend), stof met de deeltjes van Nyundo
  (`bruStofDeeltje`/`bruStofStap`/`bruStofTeken` op `gkFx`) en eigen steentjes (`gkStofTeken`, na de vijanden).
- In Co-op (16-11-2026): elke stokspeler heeft de grondklap (`mpWapenLevel` zet `grondklap`), met 5 s afkoeling
  in plaats van 8 (`GK.koelCoop`, `gkKoelDuur`; het vak in de actiebalk volgt dat). Zie "Het wapen" in `notities/multiplayer.md`.
- Keuze in Test 76 (`gkKeuze`): `duoKeuze.gkBereik` en `duoKeuze.gkSchade` in het instellingenscherm.
- Het stof (16-11-2026): drie soorten, in Test 76 te kiezen onder **Slam dust** (`duoKeuze.gkStof`, `gkStofSoort`).
  `nu` (Current) is het oude stof (`gkKlapStofNu`). `kam` (Growing crest): een kleine kroon op de klap, en
  de golf gooit stof op dat hoger wordt naarmate hij verder rolt (aan het eind zo'n twee Amir), met een hoge pluim
  (tot zo'n drie Amir) waar hij ophoudt, ook tegen een trede (`gkGolfStof`, `gkPluim`). `kroon` (Crown and ring): het stof spuit in een V omhoog (55 tot 72 graden, sneller is hoger
  en verder), een lage ring rolt over de grond weg en de diepte in, en een lage stofrol loopt met de golf mee
  (`gkKlapStof`). De getallen komen uit de mock-ups (Amir 90 px hoog), `gkWolk` zet ze om naar de wereld.
  De diepte: een stofdeeltje kan een `z` hebben (-1 ver, +1 dichtbij, `GK.diep` Amir naar voren) en eigen `zw`
  (zwaarte), `rem` en `vz`; `bruStofTeken` met `kant` tekent de wolken achter de looplijn voor Amir (`gkStofAchter`) en de
  rest na de vijanden. Zonder die velden (Nyundo) is alles zoals het was.
- Sinds 16-11-2026 is `kam` (Growing crest) de standaard, en de wolken zijn per soort groter (`GK.stofMaat`: kam 1,1,
  kroon 1,2, nu 1), gekozen in de stofproef (een artifact met een beeld uit Test 76 en schuifbalken).
- **Afspraak voor later:** bij elke upgrade van de grondklap (een talent of een sterkere versie) groeien het stof en het
  geluid mee: grotere en hogere wolken (`GK.stofMaat`, en de hoogte van de kam en de pluim in `gkGolfStof`/`gkPluim`) en
  een zwaardere dreun (`GK.vol`, langer beven, meer schok en freeze). Een idee om erbij te nemen: hetzelfde laten
  meeschalen met hoe diep Amir valt voor de klap (een hupje 80%, van een terras tot 150%, niet verder).


## De zonnestraal (16-11-2026, Test 77)

Mediteren in een bundel zonlicht en dan even ontketend: de Sun Lion. Alleen met de stokken. `STRAAL` (de naam `ZON` is de
zonneschijf in de lucht), `straalUpdate`, `straalTeken`, `straalAmirTeken`, `straalBij`.
- Een level zet stralen met `zonnestralen: [{x, h}]` (`h` voor een straal op een galerij of dak, zonder op de grond); in de
  sandbox zet **Zonnestraal** er een anderhalve Amir voor Amir neer, **Zonnestralen weg** haalt ze weg.
- Mediteren: met zijn midden in de straal (`STRAAL.breed`), op de grond, stil (geen links of rechts), omlaag vasthouden,
  `STRAAL.medi` (3 s). Een treffer, een aanval, bewegen of loslaten zet het op nul. Stofjes trekken naar hem toe
  (`straalMotes`) en een ring boven zijn hoofd loopt vol. Het beeld is voorlopig het gewone bukken.
- Ontketend (`straalBurst`, `STRAAL.burst` 6 s, geluid `zegelontdek`): geen blok (in `stokBlokStap`, dus ook geen counter),
  `STRAAL.schade` 2 op elke stokslag (`stokSchade`) en de grondklap (`gkSchadeOp`), lopen maal `STRAAL.loop` 1,35, opsprong
  maal `STRAAL.sprong` 1,48 (in `takeOff` en de afzet in `updateJump`; de hoogte wordt 444, de galerij ligt op 401, gemeten),
  en `STRAAL.klappen` (2) grondklappen los van de afkoeling (`straalKlappen`, `gkZon`: zo'n klap zet `gkKoelT` niet), op het
  lange bereik. Gouden gloed om zijn rand (de truc van de woede, `straalGloed`), en SUN LION met de ring die leegloopt.
- Uitgeput (`straalMoe`, `STRAAL.moe` 3 s, geluid `brutus_adem`): geen grondklap (`gkKan`), lopen maal `moeLoop`, opsprong
  maal `moeSprong`, de rol maal `moeRol`, een slag `moeSlag` keer zo traag en het blok `moeBlok` keer zo traag. TIRED met een
  grijze ring. Daarna kan het in elke straal opnieuw; een gebruikte straal is zwakker zolang het loopt.
- De trance (16-11-2026, `straalTrance`): na `STRAAL.instap` (0,35 s) omlaag sluit Amir zich af van de wereld en roept hij Tau
  op, de leeuwengod (TAU boven de ring). Vanaf dan zit hij vast (`straalTrance` in `amirVast`, hij blijft geknield in `canDuck`,
  geen blok) tot hij losbarst; loslaten, bewegen of een treffer breken het niet meer af. Een treffer kost
  `STRAAL.trance.schade` (0,5) keer en duwt hem niet weg (in `hurtPlayer`, `straalTranceSchadeK`). De wereld om hem heen wordt
  donker (`STRAAL.trance.dim`, `straalDimNa`, na de lichtlaag; in `straalAmirTeken` tekende de wereld er weer overheen). Het idee
  van de opdrachtgever: een afweging, schade incasseren of eerst een plek zoeken waar niemand je ziet (Test 77 heeft `sneak`, en
  stilzitten is stil). Bij het losbarsten een gouden ring (`straalLosbarst`, `straalGolf`).
- Tau zelf (16-11-2026, `TAU`, `straalTauNa`, `tauBrul`): een leeuwenkop in grijswit tribal lijnwerk boven Amir, recht van
  voren. In de trance komt hij langzaam op (het rustige frame, tot `TAU.op`, en hij ademt), bij het losbarsten brult hij
  (`TAU.fps`), houdt de brul `TAU.vast` s vast, groeit iets (`TAU.groei`) en vervaagt omhoog (`TAU.weg`). Getekend na de
  verduistering (`straalDimNa`), zodat hij in het donker licht geeft, met een zachte gloed. De frames (`karakters/amir/tau/`)
  komen uit de Grok-clip `bron/tau_brul.mp4` via `tools/tau_leeuw.py`; een andere kleur is `KLEUR` in dat script.
- Twee kandidaat-talents, voorlopig alleen sandboxknoppen (`STRAAL.talent`, `sbzonterug`, `sbzonbarst`), nog niet in een boom:
  **Trance: schade terug** (`STRAAL.terug`, de helft van de trance-schade komt terug bij het losbarsten, tot het maximum) en
  **Trance: uitbarsting** (`STRAAL.uitbarst`: alles binnen 3,2 Amir op zijn hoogte vliegt weg en is even traag, zoals na de
  grondklap; slangen en schorpioenen wippen. Geen schade.)
- De grondklap heeft nu altijd `GK.koel` 8 s afkoeling (was 1 s), ook in Test 76.
- Test 77 (stad bij dag): een straal om te proberen, een lange galerij op 401 zonder kraam, trap of lift (alleen ontketend
  kom je erop, met een bandiet en een kalebas boven), een pleintje met drie bandieten en een straal in het midden, en een
  elite met vijf levens met een bandiet erachter.
- De dubbele schade geldt voor de bandieten (`hitBandiet`) en voor alles wat de grondklap raakt; een stokslag op een andere
  soort telt nog gewoon.

## Test levels sticks

Alle stoklevels staan in een eigen reeks, `STOK_LEVELS` (Test 74, 76 en 77), met een knop onder Levels (`btnStok`,
`menuStok`, `cardsStok`). Net als de Test levels zonder tribekeuze en met alle abilities (`testReeks`). Elk heeft
`onstKeuze`: aan het begin en na R kies je **Lives** of **Invulnerable** (`duoKeuze.onst`, in `onsterfelijk()`); dat kwam
in de plaats van de vaste `onsterfelijk: true` van Test 74 en 76.

## De stoktribe: Bhubesi met de stokken in de episodes (16-11-2026)

Een eigen kaart op het keuzescherm, `bhubesi_stok` in `TRIBE_CONFIG.tribes` (`stokken: true`, `blokKoel`, `zon`), naast Bhubesi
met de speer en zijn oude boom. Gekozen door de opdrachtgever: een tribe met de speer en de oude talents, een met de stokken
en nieuwe talents.
- `tribeStok()`: een run met een tribe met `stokken`, niet in de sandbox, Multiplayer (`pvp`), de Test van de Maker
  (`mkTestActief`) of de Test levels (`testReeks`). `stokTribeLevel(level)` zet bovenin `restart` `stokken`, `geenSpeer`,
  `rugMax: 0` en `grondklap` op het level (zoals `mpWapenLevel`), en laadt de stokken en de grondklap voor `laadPoort`;
  `stokLaadLevel` doet het ook al bij `setLevel` als de tribe dan al vastligt.
- Speren pakken doet hij niet: `rekBij`, `skeletBij` en `losBij` geven niets met de stoktribe.
- Talents gelden alleen in zo'n run (`stokTalent`, `stokTalentWaarde`): in de Test levels sticks doen ze niets, ook al
  geven die alle talents.
- Het blok: na het loslaten pas na `stokBlokKoel()` weer (`blokKoel` 4 s, min `koelMin` van Quick Guard en Ready Guard),
  `stokBlok.koel`, `stokBlok.vast`; een druk tijdens de afkoeling schudt het vak `schild` in de actiebalk, dat de taartpunt
  en de seconden toont. Elders (Test 74, Co-op) is de afkoeling 0.
- De grondklap: `GK.schade.licht` (0,5) vast, ook als `duoKeuze.gkSchade` anders staat; Heavy Slam `schade` 0,5 erbij en
  `knock` 1,25, Crushing Slam `knock` 1,2 (samen 1,5) en `traagK` 0,9 (`gkRaak.traagK`, `s.gkTraagK`, `s.traagK`: het
  tempo van de bandiet zolang hij traag is maal dit; alleen de bandiet kent `traag`).
- Mediteren zonder straal (`stokZonDruk`, G of de leeuwknop, `stokZonToets`): `straalVrijZ` is een straal op de plek van
  Amir die niet in `straalLijst` staat; geen omlaag nodig (anders begon elk bukken een trance). Bewegen of slaan voor
  `STRAAL.instap` breekt het af (`straalVrijZ` weer null). `straalVrijKeer` (gezet in `straalReset`, `stokZonKeer`: `zon.keer`
  plus Second Sun en Sun King) gaat eraf bij het losbarsten. De duur is `straalBurstDuur()` (`zon.burst` 5 plus Long Roar 2).
  Vak `zon` in de actiebalk met de teller; op de telefoon wordt de leeuwknop van de woede de meditatieknop. Een straal in het
  level (`zonnestralen`) werkt daarnaast gewoon, met omlaag en zonder dat het een keer kost.
- Ontketend geen dubbele schade voor de stoktribe (`straalSchadeK`); Sun King geeft een halve erbij op een stokslag
  (`stokSchade`, dus op de bandiet; een slag op een andere soort is al een hele) en `stokDoor()` laat dan elke slag door
  een parade.
- Houten plaatjes zijn er nog niet: het teken in `TB_TEKEN` (twee stokken, een golf, de zon).
