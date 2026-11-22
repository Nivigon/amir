# Tau niveau 1 (jonge leeuw), nachtrun 22-11-2026

Plan: `claude/tau1_productieplan.md` (project). Gereedschap: `tools/tau1/` (tau.py, stokweg.py, plus raster.py,
uitlijn.py en speer_meet.py overgenomen uit `tools/mkuki/` van branch `claude/mkuki`). Werkmap tijdens de run:
`/home/claude/werk/` (niet in de repo).

## Welke frames het spel tekent (nagekeken in de HTML)
- Staan: `stokken/staan/staan_00.png` (stokBeeld, STOK.sets.staan = 1), stokken erin gebakken.
- Rennen: `stokken/rennen/rennen_00..11.png` (12), stokken erin gebakken. De ren is samengesteld (geen lijf-bron in de
  repo), dus de stokken haal ik eruit met het masker van `tools/stok_variant.py` (stokhoeken.json).
- Springen: `beweging/jump/jump/amirjump0staand..6landing.png` (7). In de sprong tekent het spel GEEN stokken (useJump
  gaat voor stokBeeld), dus deze frames zijn zonder stokken.
- Rollen: `beweging/rol/zonder/rol_1..28.png`. Ook zonder stokken (useRol gaat voor).

## Uitvoer
- `stokken/staan/staan_00.png`, `stokken/rennen/rennen_NN.png`: spelbeeld (Tau-kleuren) met de originele stokken er
  weer in, zelfde canvas als het spel (511x384). Daarnaast `_zones.png`, en in `lijf/` het lijf zonder stokken
  (Tau-kleuren, `_zones`, `_hulp`), zodat de stokken later opnieuw gebakken of vervangen kunnen worden.
- `beweging/jump/jump/*.png` en `beweging/rol/zonder/rol_N.png`: spelbeeld, `_zones`, `_hulp`.
- Zonekaart: vacht/kap (0,255,0), broek (0,0,255), krassen (255,255,0), tanden (255,255,255), ogen (255,128,0),
  de rest zwart. Omkleuren: doelkleur x V/Vref per zone (`tau.py kleur`, paletten TAU, WIT, ZWART).

## Hulpkleuren
Kap + vacht groen #00C040, broek blauw #2050FF, krassen geel #FFE000. Tanden blijven wit, ogen amber.
Referentie in hulpkleuren: Grok-bewerking van post 3e331009 -> `0ba1c513-842d-4d45-b651-2ab0ca4ede36`
(`bron/ref_hulp.png`, met de stokken; op 0,42 opgehaald). Origineel: `bron/ref_tau1.png`.
Tau-kleuren: vacht (218,180,139) en broek (88,67,105) gemeten in het origineel; krassen (226,196,150).

## Anker: staan (klaar)
- Lijf: het echte stokloze lijf uit `stokken/bron/lijf/staan_00.png` (Animeer-canvas, +1,+82 naar het spelcanvas).
- Grok: frame groot, referentie in hulpkleuren klein linksboven, prompt `tau_anker` (zie prompts.md).
  Post `fc5af9c9-712c-485f-8261-2d08a8f5a970`, IoU 0,93. Kap met tanden, amber ogen, twee krassen op het rechterbeen in
  beeld (het been met de voet naar ons toe, het dichtst bij de camera). Krassen iets langer en steiler dan in de
  referentie, maar netjes twee en op de goede plek: goedgekeurd.

## Andere aanpak (02:30): alleen de kap uit Grok, de rest blijft het origineel
- Eerst de ren hetzelfde als het anker geprobeerd (hele figuur aankleden). Afgekeurd: Grok kan de guard met stokken
  niet vasthouden tijdens een ren (vuist omhoog in plaats van voor de borst, post `783b36b5`; met de stokken in de invoer
  haalde hij de stokken zelf weg en ging pompen, post `c7665909`, krassen op het verkeerde been). IoU 0,52-0,70.
- Wat wel werkt: Tau 1 verandert alleen het hoofd (de kap) en voegt krassen toe; vacht en paarse broek blijven zoals ze
  zijn. Dus per frame alleen kop en schouders (crop 200x200 van het echte frame, stokken erin) naar Grok met prompt
  `tau_kop` ("Change ONLY his head: he now wears a hood ..."). Grok houdt dan alles op zijn plek (IoU op het crop
  0,90-0,95). Uit dat beeld knip ik alleen de kap (convex omhulsel van groen + tanden + ogen, nooit Grok-broek) en zet
  die op het originele frame (`tau.py kop_plak`). Daarna de originele stokken er weer overheen.
- De krassen teken ik zelf (`tau.py krassen`, maten in `KRAS`): twee korte schuine halen, spits aan beide kanten, op de
  dij van het been dichtst bij de camera. De dij per frame (heup naar knie) staat in `tools/tau1/dij.json`, afgelezen op
  een raster en daarna automatisch naar het diepste stuk broek in de buurt geschoven. Grok zette ze telkens op het
  voorste been; zo staan ze gegarandeerd op hetzelfde fysieke been (zijn linkerbeen, dat naar de camera wijst).
- Welk been dichtst bij de camera is in de ren: de 12 frames zijn een hele cyclus (frame k en k+6 zelfde houding, benen
  gewisseld). Het verre been heeft de roodbruine voet (frame 1, 3). Daaruit: 11, 0, 1 achterste been; 2, 3 het
  opgetrokken been; 4 de knie naar voren; 5, 6, 7 het voorste been; 8, 9 het standbeen; 10 het afzetbeen. Let op: in
  het origineel is de schaduw van de benen in de tweede helft niet consistent (Grok-ren), dus in 6-11 is het
  gekraste been soms het donkerdere. Zie TWIJFEL.md.
- Staan opnieuw op dezelfde manier (kap uit het anker `fc5af9c9`, krassen getekend), zodat staan en rennen dezelfde
  krassen hebben. De vacht van staan komt wel uit Grok (zonder de oogvlekjes), omdat de kap daar uit de vacht groeit.

### Rennen (klaar, 12)
Kap-posts per frame in `bron/grok_posts.json` (kop_ren0..11). IoU kop 0,90-0,95.
- rennen_03: het origineel heeft een gat in de broek (bovenaan de linkerdij in beeld, met een harde trap in de
  omtrek; Tom zag het). Gerepareerd met Grok (post `fbf44475-96a7-4918-8d10-db489ea9bb94`, alleen dat stuk erin
  geplakt), bron in `bron/rennen_03_hersteld.png`. Het origineel in het spel heeft dit gat nog.
- Uitvoer: `stokken/rennen/rennen_NN.png` (spelbeeld met stokken), `_zones.png`, `recolour/*_wit.png` en `*_zwart.png`.
- Rapport: `rapport/rennen_plaat.png`, `rapport/rennen.gif` (origineel links, Tau 1 rechts).

### 02:55 krassen opnieuw (Tom: "flauwe streepjes", ze moeten zoals op de tekening)
- Nieuwe krassen naar de referentie (post 3e331009): twee lange sikkelvormige halen, licht gebogen, evenwijdig, spits
  aan beide einden, schuin (55 graden) over de dij, goudbeige (208,162,108) met een donkere rand van gescheurde stof.
  Lengte de helft van de dij (20 tot 29 px), dik 3,8 px, 7 px uit elkaar.
- Tom bevestigt: zelfde fysieke been (dus in de ren wisselen ze van voor naar achter in beeld).
- Fout gevonden en hersteld: het spelbeeld van rennen_03 werd over de gerepareerde bron geschreven; nu schrijft alles
  naar `tau1/`, de bron opnieuw uit de Grok-reparatie gemaakt.

### 03:00 krassen als losse laag (Tom: "moeten we die per frame los plaatsen? dan kun je door")
- Ja. De frames zelf zijn nu ZONDER krassen. Per frame `krassen/<frame>_kras.png` (de laag op hetzelfde canvas) en
  `krassen/<frame>_voorbeeld.png` (frame met krassen, alleen om te kijken). Plek, hoek, lengte, afstand, dikte en boog
  per frame in `tau1/krassen_plaatsing.json`: dat is een startwaarde, Tom zet ze later per frame goed.

### Springen (klaar, 7)
Kap per frame op kop en schouders (prompt `tau_kop2`, met "viewing direction exactly as drawn"). IoU kop 0,94-0,97.
Posts in `bron/grok_posts.json` (kop_jump0..6). De krassen zijn 2x zo groot (de sprongframes zijn op 2x getekend).
De vacht houdt hier de oogvlekjes op de borst (origineel), alleen de kap is nieuw.

### Rollen (klaar, 28)
Zelfde aanpak, prompt `tau_rol` (met "caught mid-movement in a forward roll ... even upside down"), frames NIET
gedraaid aangeboden (de kap kwam ook ondersteboven goed). IoU kop 0,91-0,97. Posts in `bron/grok_posts.json`.
Geen krassen in de rol (zie TWIJFEL.md).

## Stand 03:45: alles uit de eerste ronde af
- Staan 1, rennen 12, springen 7, rollen 28. Zonekaarten, recolours (wit, zwart met goud) per frame in `recolour/`.
- Rapport: `rapport/*_plaat.png`, `*.gif`, `idle_tau_wit_zwart.png`, `TWIJFEL.md`.
- Nog niet in het spel gezet (geen pull request, niets live).
