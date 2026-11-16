# De stokken

Een tweede wapenset voor Amir: twee slanke stokken met een leren greep (Nguni-stokvechten), in plaats van de speer.
Alleen in Test 74 (`stokken: true`) en de sandboxknop **Stokken**.

## Frames
- `karakters/amir/stokken/<set>/<set>_NN.png`, sets `rennen` (12), `staan` (1), `slag` (18), `draaislag` (15),
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
