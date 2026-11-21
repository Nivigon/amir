# Mkuki: de basisskin van de speer-tribe (productieplan)

Goedgekeurd door Tom op 21-11-2026. Uitvoeren in een verse chat, onbewaakt (Tom slaapt).
Kwaliteit is het allerbelangrijkste; liever minder sets af dan sets die er slecht uitzien.

## Context

- Elke tribe krijgt uiteindelijk 3 outfits die je verdient, per stap epischer. Tau (de stoktribe) heeft de huidige
  look als basis. Mkuki is de speer-tribe; dit is zijn eerste, eenvoudige basisskin.
- Een outfit is een complete skin (alle frames opnieuw aangekleed). Variatie daarna via recolours, dus alles moet
  goed om te kleuren zijn.

## Het ontwerp: Mkuki 1

Referentie: `karakters/amir/mkuki/bron/mkuki1_referentie.png` (Grok post `5a9a65d3-6ac9-4321-bdea-71e08db075db`,
afgeleid van `112f29be-56a4-4c0d-acae-bf3a6f6a9bd1`). Startbeeld van het ontwerp: `mkuki/bron/idle_los_startbeeld.png`.

- kaal hoofd, blote borst
- schuine leren band van de verre schouder naar de heup, met een klein metalen ringetje (aan de rug hangt later een speer)
- kralenketting van rode kralen om de nek
- koperen bovenarmbanden en polsbanden
- zandkleurige schort (lendendoek) met een leren riem
- donkergrijze broek tot halverwege de kuit, omgeslagen
- blote voeten
- alles heel, niet gescheurd, geen vacht, geen verf, geen schedels

## De speer los, net als de stokken

De speer zit NIET in de frames. Tom wil hem altijd kunnen vervangen door een andere speer.

- Haal in elk frame met speer eerst de speer weg (masker van de speer, gat met magenta) en laat Grok het lijf in
  grijphouding aanvullen terwijl het aankleedt. Schrijf in de prompt niets over een speer of stok (elk woord over een
  voorwerp zet het in beeld, zie de skill grok-imagine-prompts): beschrijf de handen als gesloten vuisten.
- Meet per frame in het ORIGINELE frame de speer: handpunt(en), hoek, lengte en wat voor of achter het lijf ligt.
  Sla dat op als `karakters/amir/mkuki/plaatsing.json`, in de vorm van `karakters/amir/stokken/plaatsing.json`.
- De vuist die om de speer sluit wordt een losse bovenste laag met een gat waar de speer doorloopt (methode van de
  stokken, zie `notities/stokken.md`, "Vuisten" en "slip").
- Draaiende sets (rol met speer, draaislag, rol-worp): de speer wordt korter als hij naar je toe draait. Schaal de
  lengte mee en markeer die frames in het rapport voor Tom.

## Wat er gemaakt wordt (ongeveer 260 frames), in deze volgorde

1. Proef: idle zonder speer (`idle/idle_ns.png`) en idle met speer (`idle/idle_sp.png` plus `idle/idle_sp/` 20 frames).
   Hiermee kalibreer je de hulpkleuren, het weghalen van de speer en de vuistlaag. Pas door als dit echt goed is.
2. Basis met speer: rennen 12 (`beweging/run/nieuw/ren_sp_`), springen 7 (`beweging/jump/jumpspeer/`), bukken 12
   (`beweging/bukken/bukkenspeer/`), sluipen 22 (`beweging/sluipen/sluipen_speer_`), rol 28 (`beweging/rol/met/`),
   trap 2 (`beweging/trap/`).
3. Basis zonder speer: rennen 12 (`ren_ns_`), springen 7 (`jump/jump/`), bukken 12 (`bukken/bukken/`), sluipen 28
   (`sluipen_NN`), rol 28 (`rol/zonder/`).
4. Aanvallen: speerstoot 10 (`aanval/speerstrike/`), speerworp 20 (`speerworp_NN`, map in `THR_DIRS`), lage zwaai 18
   (`aanval/lowsweep/`), draaislag 15 (`aanval/combo/`), stofveeg 14 (`aanval/stofsweep/`), rol-worp 33
   (`beweging/rol/worp/`).

Niet in deze ronde: sluipaanval, executie, mediteren, de oude ren (`run/run`, `run/speerrun`), alle stoksets.

## Alles omkleurbaar, met kwaliteit

Grok tekent de kleding in felle hulpkleuren, een per onderdeel, ver weg van magenta en van zijn huid. Zes zones:
broek, schort, riem, schuine band met ring, kralen, armbanden. De gewone Mkuki-look is zelf een recolour
(lichtheid en schaduw behouden, alleen de kleur vervangen; de kleuren uit de referentie). Kies de precieze
hulpkleuren in de proef. Lijkt de Mkuki-recolour van de proef niet net zo goed als de referentie, pas het aan
voor de rest begint (desnoods natuurlijke kleuren met handwerk aan de maskers; beslis en noteer waarom).

Lever per frame: de Mkuki-kleuren (het spelbeeld) en de zonekaart (een PNG met per zone een vaste indexkleur),
zodat het spel of een script later elke kleurvariant maakt.

## Aankleden: de rastermethode

Zie de projectnotitie `claude/outfit_raster_methode.md` (de monnik-rol, Test 85) en `tools/mkuki/`. Kort:

- 3x2 raster op magenta 1800x1100 (tegels 600x550, frames 1,56x vergroot), eerst een aangekleed anker plus 5 nieuwe.
- Ondersteboven-frames (rol) eerst 180 graden draaien.
- Terug naar het eigen canvas, daarna uitlijnen op IoU met het origineel.
- Gezicht en voeten na afloop terug uit het originele frame.

## Grok bedienen (Claude in Chrome)

- grok.com/imagine, het verborgen file-input via `file_upload`, prompt typen als een alinea, versturen met Enter.
  Bewerken van een bestaand beeld: het vak "Beschrijf uw bewerking" onder een post.
- Ophalen op volle resolutie (geen screenshot van het verkleinde beeld): open
  `https://assets.grok.com/users/cd0c0caa-675a-4fe6-b7fe-024cc6e0663f/generated/<postid>/image.jpg` in een eigen tab,
  zet met javascript het `img` op ware grootte (1728x1152, `position:absolute`, `left`/`top` negatief) en maak met de
  `zoom`-actie op `scale: 1` en `save_to_disk` tegels (devicePixelRatio 1,25, dus 440 CSS-px wordt 550 px). Plak de
  tegels aan elkaar. `fetch` van de assets-url werkt niet (Failed to fetch). Sluit de tab daarna.
- De postid haal je uit de url van de post-pagina of uit de `img`-bronnen op de pagina.

## Kwaliteitscontrole per frame en per set

1. Omtrek over het origineel (IoU), geen verspringing ten opzichte van de buren, elke hulpkleur aanwezig waar hij hoort,
   geen magenta-rand.
2. Afgekeurd: opnieuw naar Grok, hooguit drie keer, daarna markeren voor Tom.
3. Per set zelf kijken naar een overzichtsplaat en een afgespeelde loop met de speer erin, voor je doorgaat.

## Opslag en logboek

- Alles op de branch `claude/mkuki` (bestaat al, met de referentie en `tools/mkuki/`). Geen pull request, niet live.
  Push na elke afgeronde set, zodat niets verloren gaat als de chat stopt.
- Frames: `karakters/amir/mkuki/<zelfde submap en naam als het origineel>`, zonekaarten ernaast met `_zones`.
- Logboek: `karakters/amir/mkuki/LOG.md`, na elke stap bijwerken (welke set, welke frames af, welke Grok-posts,
  wat afgekeurd en waarom). Na een onderbreking eerst het logboek lezen.
- Bij een limiet of moderatie van Grok: netjes stoppen, in het logboek zetten waar het bleef.

## Wat Tom 's ochtends krijgt

- Per set een overzichtsplaat en een GIF naast het origineel (in `karakters/amir/mkuki/rapport/`).
- Mkuki in zijn eigen kleuren plus twee voorbeeld-recolours.
- De speerplaatsing per frame.
- `rapport/TWIJFEL.md`: de frames waar je aan twijfelt, en de draaiende speerframes.
