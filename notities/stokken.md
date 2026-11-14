# De stokken

Een tweede wapenset voor Amir: twee slanke stokken met een leren greep (Nguni-stokvechten), in plaats van de speer.
Alleen in Test 74 (`stokken: true`) en de sandboxknop **Stokken**.

## Frames
- `karakters/amir/stokken/<set>/<set>_NN.png`, sets `rennen` (8), `staan` (1), `slag` (18), `draaislag` (15),
  `draaiterug` (6), `blok` (13). Een gedeeld canvas 440 x 328, anker 256, grond 323, schaal 1 (Amirs spelschaal),
  alles kijkt naar links. `metadata.json` heeft de ms per frame.
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
- Counter: slaan tijdens het blok of binnen `STOK.venster` na het loslaten of na een gevangen klap. De draaislag gaat
  door de dekking van de bandiet heen (`stokDoor`), daarna speelt `draaiterug`. Met `stokKeuze` kies je
  `duoKeuze.stokCounter`: `stun` (bandiet `rust` 2 s, `knock` terug, `inv` 0 en sterretjes via `stokStun`) of `gewoon`.
- Een spawn met `hp` (zonder aanvoerder) geeft een bandiet zoveel levens; Test 74 gebruikt de elite-garde met 5, zoals Co-op.
