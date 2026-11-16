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
- Keuze in Test 76 (`gkKeuze`): `duoKeuze.gkBereik` en `duoKeuze.gkSchade` in het instellingenscherm.
- Het stof (16-11-2026): drie soorten, in Test 76 te kiezen onder **Slam dust** (`duoKeuze.gkStof`, `gkStofSoort`).
  `nu` (Current, de standaard) is het oude stof (`gkKlapStofNu`). `kam` (Growing crest): een kleine kroon op de klap, en
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
