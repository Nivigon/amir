# De stokken

Een tweede wapenset voor Amir: twee slanke stokken met een leren greep (Nguni-stokvechten), in plaats van de speer.
Alleen in Test 74 (`stokken: true`) en de sandboxknop **Stokken**.

## Frames
- `karakters/amir/stokken/<set>/<set>_NN.png`, sets `rennen` (8), `staan` (1), `slag` (18), `draaislag` (15),
  `draaiterug` (6), `blok` (13). Een gedeeld canvas 440 x 328, anker 256, grond 323, schaal 1 (Amirs spelschaal),
  alles kijkt naar links. `metadata.json` heeft de ms per frame.
- De vechtsets (slag, draaislag, draaiterug, blok) kwamen uit de clips een kwart groter dan staan en rennen. Het spel
  tekent ze daarom op `STOK.maat` 0,8 (`stokMaat`, `stokSetNu`): dan is zijn hoofd even groot als in staan en in zijn
  gewone steek. Het hitpunt (`steekDX`, `steekY`) schaalt mee; `reik` niet.
- Gebakken uit de Animeer tool Amir stokken (https://claude.ai/artifact/W4e5eqpQ5PEfBRKZPzpWog): het lijf uit Grok-clips
  met groene stokken (verwijderd), de stok als item geplaatst door de opdrachtgever, en met de tool zelf samengesteld
  (dezelfde `compose`). `plaatsing.json` is de export van de tool (per frame stok_voor en stok_achter): de bron als de
  stok later een losse laag wordt om om te kleuren of te upgraden.

## Spel
- `STOK` (tempo, actieve frames, hitpunt en reik per slag, blok, venster, stun), `stokAanval`, `stokStap`,
  `stokBlokStap`, `stokBlokVang`, `stokBeeld`, `stokTreffer`.
- De slag loopt op `atkFrame` met `atkStok` (zoals `atkCombo`), dus `steekLive`, `steekDX`, `steekY`, `steekR` en
  `steekEind` gelden vanzelf voor elke vijand.
- Blok: C vasthouden (op een telefoon de schildknop). Vanaf blok-frame `STOK.blokOp` vangt `hurtPlayer` een klap van
  voren af (houtklap, duwtje). Projectielen met een eigen schade-ingang (bouten, de speer van de schildbandiet) vangt
  het nog niet.
- De stun-counter klinkt en voelt harder: een stapel lage houtklappen met een naklap en het bloedgeluid
  (`STOK.stunKlap`), meer hitstop en schok, en een kleine bloedspetter op de lens bij het trefpunt die binnen 0,7 s
  wegtrekt (`STOK.lens`, `stokLens`, `stokLensTeken`). De lens-code van Nyundo is daarvoor algemeen gemaakt
  (`lensSpatMaak`, `lensSpatTeken`). De gewone counter (`gewoon`) houdt de oude klap.
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
  Een druk tijdens de slag gaat verloren (geen buffer). Voor een licht wapen is dat traag; de tweede stok doet niets.
- Na een treffer staat de bandiet 1,15 s in dekking (`BAN_INV_T`). Een volle slagcyclus is korter, dus de tweede slag
  wordt bijna altijd gepareerd: raak, clang, raak. Met vijf levens voelt dat als tegen een muur slaan.
- De counter is gratis: elk blok dat je loslaat (vanaf frame 8) opent het venster, ook zonder gevangen klap.
- In de draaislag vallen de raakframes (3 tot 6) voor de zichtbare draai (8 tot 14); de draai is uitloop, en met
  draaiterug sta je ruim een seconde vast.
- Slag-frame 6 heeft een paarsroze stok (een vlek uit de clip).
