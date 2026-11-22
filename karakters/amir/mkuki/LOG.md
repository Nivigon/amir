# Mkuki nachtrun, logboek

Plan: `notities/mkuki.md`. Werkmap tijdens de run: `/home/claude/werk/` (niet in de repo); alles wat af is staat hier.

## 21-11-2026, start 02:17

- Repo op branch `claude/mkuki` (stond: referentie, `tools/mkuki/`).
- Nieuw: `tools/mkuki/speer_meet.py` (meet de speer in een origineel frame: grijze kop als startpunt, schacht langs de
  lijn tot hij ophoudt, masker = band van 6,5 px plus kop en lint) en `tools/mkuki/raster.py` (raster 3x2 bouwen met de
  speer eruit, en het Grok-resultaat terugzetten op het eigen canvas).
- Speermeting op de idle (21 frames): alle 21 goed, kop tot kont, ook door de hand heen.

### Keuze hulpkleuren (proef)
Zes zones, elk een eigen tint ver van magenta (300 graden) en de donkerbruine huid:
broek blauw #2050FF, schort geel #FFE000, riem rood #E01010, schuine band met ring groen #00B050,
kralen cyaan #00E0E0, armbanden oranje #FF7A00.

### Proef idle (klaar, 22 frames: idle_ns, idle_sp, idle_sp/00-19)
Grok-posts: `3c16c134-c75e-4b35-882c-deff4d428927` (eerste raster, vuisten nog te dicht bij de buik, niet gebruikt),
`10d7d9d4-d4eb-40c0-a779-25b05ce08ef2` (raster 1: ns, sp, 00, 05, 10, 15), daarna met anker:
`5d3718ae-cde3-4a75-8ee3-39bf3638a244` (01-04, anker 00), `83253d09-6761-4fcd-b5fe-733a1dd856cd` (06-09, anker 05),
`d91216e1-1c92-4059-a789-9e98a5c591ec` (11-14, anker 10), `0e06bae1-7c47-4bb8-9b74-a8f7d895b6fe` (16-19, anker 15).
Afgekeurd: `312319e1-...` (proefprompt "a hand ... is a closed fist": Grok maakte van alle handen vuisten langs het lijf).
IoU met het origineel 0,80-0,86.

Beslissingen uit de proef:
- **De speer gaat er alleen uit waar hij te zien is.** Eerst haalde ik de hele band langs de schacht weg, ook de vuist
  eromheen; Grok tekende de vuist dan opnieuw, maar dichter bij de buik (8-10 px naast de speerlijn). Nu meet
  `speer_meet.py` waar het silhouet dwars op de schacht breder is dan de schacht (een vuist, 8 px tot 22% van de lengte)
  en laat die staan. Grok kleedt de vuist dan op zijn plek aan en de speer loopt er later precies doorheen.
- **Vuistlaag** = het aangeklede frame binnen een cirkel (straal 4,5% van de speerlengte) om het handpunt, zonder de
  pixels waar de speer te zien was. In deze idle omsluit de vuist de schacht helemaal, dus er is geen apart gat nodig.
  Tekenvolgorde in het rapport: lijf, speer (uit het origineel), vuist.
- **Prompt**: niet "a hand is a closed fist" (dan worden alle handen vuisten), maar per figuur zeggen wat de armen doen
  en "every hand keeps exactly its place and shape". Met anker: "The first figure, top left, is already dressed ...
  Do NOT change the first figure", vijf figuren per raster.
- **Gezicht en voeten terug uit het origineel** (`afwerk.py`): boven de bovenrand van de kralen het originele hoofd
  (zonder vacht en de randen van de vacht), onder de laagste rand van de broek de originele voeten (zonder de oude
  paarse broek). Losse snippers onder 1% van het lijf gaan weg.
- **Hulpkleuren werken**: de zones zijn schoon te scheiden op tint (huid: tint 10-25, V rond 0,31; oranje V > 0,62).
  De kralen tekent Grok als losse bolletjes met donkere randen; de zone pakt de bolletjes, de randen blijven donker. Prima.
- **Mkuki-kleuren** (kleur.py, `MKUKI`): broek (60,56,57), schort (185,140,98), riem (88,52,34), band (78,48,34),
  kralen (150,42,36), armbanden koper (186,98,52); helderheid = doelkleur x V/Vref per zone, Vref vast (geen geflikker).
  Naast de referentie gelegd: zelfde look, dus geen handwerk aan de maskers nodig.
- Geflikker gemeten (gemiddeld pixelverschil tussen opeenvolgende frames): Mkuki 2,5-9,1 tegen origineel 1,7-7,6. Goed.
- Ophalen: zes zoom-tegels van 484x444 CSS-px (605x555 px) per beeld, geplakt met `tools/mkuki/plak.py`. De prompt zet ik
  met `document.execCommand('insertText')` in het tiptap-vak; typen van 2000 tekens liep tegen de time-out van 30 s.

### 03:00 Tom: het schort moet een omgeslagen doek met split zijn (zoals de referentie). Idle opnieuw.
De eerste versie (los geel schortpaneel) was fout: ik had het doek in woorden beschreven en Grok vulde zelf in.
Nu zo, en dit is de werkwijze voor de rest van de run:
1. De referentie zelf omgekleurd naar de hulpkleuren met Grok, vormen ongewijzigd: post `d0bb0d1c-5942-47dd-830d-0d74fe2467da`
   (`/home/claude/werk/een/ref_hulp.png`; zit niet in de repo, wel de beschrijving hier).
2. Eerste anker: idle_ns groot met die omgekleurde referentie klein linksboven als voorbeeld (`tools/mkuki/paar.py`),
   post `6e1f7054-a307-42a6-8caa-65992b0e09db`, IoU 0,85. Zelfde voor idle_sp_00 (post `37a9d7eb-c882-4c51-9499-12da3b3bb895`).
   Let op: met de referentie op ware grootte ernaast tekende Grok de referentiehouding na (post `8508dc25-...`, afgekeurd).
3. Daarna rasters met een aangekleed anker linksboven (prompt in `tools/mkuki/prompts.md`): `28fb983e-...` (sp, 01-04),
   `8e554fdf-...` (05-09), `9673410e-...` (10-14), `fa233733-...` (15-19).
4. Afgekeurd: in `9673410e` zette Grok bij 10 en 12 de verre hand op de heup. Opnieuw met drie ankers bovenaan:
   `1734dfd8-...` (nu ook de vuist weg, afgekeurd), `b24b194e-17d3-4b7b-b196-d13184762e7b` (goed).
Andere fixes: de groene band tekent Grok nu donker (V 0,35), zone 4 accepteert dat. Vref per zone opnieuw gemeten.
Kralen (138,36,32) en koper (200,132,92) iets dichter bij de referentie.

### Ren met speer (begonnen, niet af)
Aanpak per frame los (`tools/mkuki/paar.py`): frame groot, omgekleurde referentie klein linksboven. Rasters met
een anker gaven bij de ren te vaak gelijkgetrokken poses (IoU 0,61-0,64), los per frame 0,72-0,81.
- ren_sp_7 (anker): post `6677ff21-1646-45fe-8421-cb5e3115393e`, IoU 0,81.
- raster `3d905c1e-fe51-4999-a0e0-140a37f7a42a`: alleen ren_sp_1 goed (0,72), de rest afgekeurd.
- ren_sp_2: `fb13bccd-afda-48c9-bf61-462bb64865b9` (0,80). ren_sp_3: `30f79b0f-568a-4187-bd3d-a83fd09d3842` (0,72).
- ren_sp_4: `829d5e73-62f6-491e-8abb-10a62724fd69` (0,60, wandelpas): noodgreep met de originele benen, zie TWIJFEL.md.
- Een generatie voor ren_sp_4 tussendoor is kwijt (history.back ging een post te ver).

### 04:05 gestopt
Grok-pagina hangt (laden 60-90 s, time-outs op klikken en scripts). Gestopt volgens de opdracht. Verder:
de ren afmaken (5, 6, 8-12), dan de rest van het plan. Werkmap (niet in de repo): `/home/claude/werk/`.
Handig voor de volgende keer: Enter verstuurt niet altijd, de verzendknop wel; na een generatie de pagina opnieuw laden
duurt lang, dus liever een nieuw tabblad per generatie.

### 09:30 verder (Tom: "ga verder"; recolours hoeven nog niet)
Ren met speer af (12 frames), elk frame los met de omgekleurde referentie klein linksboven:
5 `c7297677-526c-4a5d-a4f0-80788375eacb` (0,73), 6 `4c6eda77-d5a8-4cc6-8b74-167b0c85f575` (0,72),
8 `ca804ee0-9eba-4c12-90d5-165a2027f8c2` (0,79), 9 `6c7abee6-d6c8-48e9-9557-43de82a58020` (0,76),
11 `a010247c-1688-4712-87a7-2ef05aaf3417` (0,75), 12 `57bcae44-0d1c-4c52-b4c1-070e9c1d3e09` (0,78).
10 `a233bda1-124b-4372-9484-417be281f621` (0,58, wandelpas): noodgreep, zie TWIJFEL.md, net als 4.
Keuzes: voeten in de ren van Grok (niet terug uit het origineel). Speerlaag in het rapport zonder oude broek en vacht.
Grok laadt weer normaal (zo'n 18 s per pagina).

### Springen met speer (7 frames, af)
Elk frame los (paar.py). Posts: 0 `93d6b601-495d-45ef-a204-51fe25d162e5`, 1 `9d2bf22d-71a6-4b20-9496-fa4dc24ffbe1`,
2 `d99213b3-2101-4592-aa87-5516410833ac`, 3 `9dd3f31f-70b0-4dff-ad55-92d1e31e596e`, 4 `15f68bc0-42b6-47fb-a257-d83cb54a6884`,
5 `c5fa4936-5065-4ed2-a1e2-71b8990e2bd3`, 6 `2dd1eaa9-d36c-4fc7-942a-4decd99b6284`. IoU 0,63-0,88.
Speermeting werkt nu op elke figuurgrootte (eerst verkleinen naar ~290 px, masker meeschalen en verbreden);
bij 4 (top) zijn de handen met de hand gezet in `tools/mkuki/overrides.json`. Bij 6 tekende Grok ook de referentie
groot na; terug kiest nu de figuur die het best op het origineel past.

## Bukken met speer (12 frames)

- Posts: hold_1 caeb28d4, hold_2 046aa398, hold_3 7db7a5ce (de eerste poging d450304a gaf een foutpagina), hold_4 4dbcb4bf, in_1 bf4e64ec, in_2 b0873b3c, in_3 1155e4a2, in_4 0cde5d69, in_5 9e60d66e, in_6 4fb2f6e1, in_7 716b6d97, in_8 bc2ff5f8.
- IoU met het origineel 0,70 tot 0,83. in_1 leek eerst de referentiepose na te tekenen, maar het origineel staat daar ook nog bijna rechtop: goedgekeurd.
- Voeten van Grok, hoofd en vuist uit het origineel. Volgorde in de export: in_1..8, dan hold_1..4.
- Export: bukken_sp, 12 fps, plaat en GIF in rapport/.

## Sluipen met speer (22 frames)

- Prompt mk_sluip: de bukprompt met "sneaking forward in a low crouch, one foot in front of the other; keep his exact step and crouch as drawn".
- De speermeting was eerst te kort (lintresten en steelresten); met de mediane lengte (set_lengte, zoals speercheck) ging hij er schoon uit. paar.py bouw leest overrides.json, waar die lengtes nu staan.
- Grok gaf bij s12 tot s21 eerst geen beeld (foutpagina op assets, de post-url bleef staan). Opnieuw verstuurd met een controle in de lus: het beeld moet laden voor de id telt. Les: na elke post het beeld controleren.
- s6 kwam terug op 1248x832; geplakt met tools/mkuki/plakmaat.sh.
- IoU 0,67 tot 0,82. Posts staan in werk/sluip/ids.json (niet in de repo); s0 62bb1310, s12 2c621ddc, s21 d97a911d.
- Export sluipen_sp, 12 fps.

## 21-11-2026, 11:00 verder (nieuwe chat): rol met speer (28 frames, af)

- De werkmap van de vorige chat was weg. De omgekleurde referentie opnieuw opgehaald uit Grok (post `d0bb0d1c`,
  1648x1200) en gekeyd naar `/home/claude/werk/een/ref_hulp.png`.
- Ophalen nu met twee tegels van 1209x576 (rechterdeel vanaf x=519, waar de grote figuur staat): `tools/mkuki/tegel2.sh`,
  en `tools/mkuki/verwerk.sh` (plakken, terugzetten, post-id in ids.json). `tegelxy.sh` als de figuur verder links staat.
- Speermeting: rol 23 en 24 lijn gefit op de schacht (`tools/mkuki/fitlijn.py`), rol 23-25 band 9,5 px breed.
- Prompts (localStorage op grok.com): `mk_rol3` (basis: "caught mid-movement in a forward roll", vuisten), `mk_rol4`
  (armen lang naar voren en omlaag, voor 4 en 5), `mk_rol5` (hoofd laag tussen de armen, 8 en 9), `mk_rol6` (opgerold, vuisten
  voor het gezicht, 13-16), `mk_rol7` (opgerold, armen ver naar links, 17 en 18), `mk_rol_lig` (op de rug, 22),
  `mk_rol_zit` (zittend, 23 en 24), `mk_rol_kniel` (geknield, 25-28).
- Keuze: ondersteboven-frames (11-19) worden NIET gedraaid aangeboden. Rechtop gezet ("draai") gaf in de proef van 11 een
  rechtopstaande figuur (IoU 0,39): Grok maakt van een omgedraaide handstand een staande man. Zo aangeboden zoals ze zijn
  lukt het wel (0,65-0,75). `"draai": true` blijft alleen voor het afwerken (klaar1.py `--draai`), zodat hoofd en voeten
  in de goede richting gezocht worden.
- Posts (laatste = gebruikt): 1 20c63994, 2 13238ef8, 3 06efa016, 4 acbdd7d8, 5 5ca8acdc, 6 77693cba, 7 20cfe7fe,
  8 0ee63858, 9 d3433ed3, 10 be5a672e, 11 b3f1f0c8, 12 037c7a9e, 13 eeaf7ef7, 14 14ea1598, 15 d0a39eec, 16 eb454482,
  17 48e25a19, 18 31b87283, 19 59516103, 20 9370854c, 21 a357b6ee, 22 73cf25e5, 23 09f68af4, 24 1cc85608, 25 82222ee0,
  26 c7f85e19, 27 b689b5a6, 28 5bf9cc24. Afgekeurd: 3 (470a0d9e, ff70105e: vuist en speerresten), 4 (29778e83), 5 (dedd73ea),
  8 (4037bd7b, kleiner), 9 (9c06b540), 11 (0cba6fea: rechtop), 13 (28309b74), 17 (b2711f72: armen omhoog), 18 (1fbae8d6),
  22 (efeb885d: staand). IoU 0,63-0,82.
- Afwerken in de rol: vanaf 11 geen hoofd uit het origineel (`--geenhoofd`), want in de liggende en ondersteboven poses
  pakte de hoofdzone vachtresten en speerstukken mee; het hoofd van Grok is daar schoon. `--schoon` haalt dunne losse
  sliertjes weg. Vuist uit het origineel alleen als de hand van Grok er ook zit (anders zweefde er een losse vuist);
  niet geplakt in 3 (een van de drie handstukken) en 19.
- kleur.py: de regel "blauw boven de riem is ketting" pakte in de rol de hele broek (die ligt daar boven de riem); nu
  alleen kleine stukjes die tegen de kralen aan liggen.
- Export rol_sp, 12 fps.

## Trap met speer (2 frames, af)
- Prompt `mk_trap`: de bukprompt met "He stands upright on a stair step, one foot placed higher than the other; keep his
  exact stance". Posts: trap_af 1c0245bd (IoU 0,74), trap_op 3da6e5f4 (0,77). Hoofd en vuist uit het origineel.
- Export trap_sp, 4 fps (twee losse poses, geen loop).
- Grok laadt sinds ~12:15 weer traag (60-90 s per pagina, soms time-outs van scripts). Werkt wel; ik wacht langer per stap.

## Ren zonder speer (begonnen)
- Prompt `mk_paar_ren`, frame los met de referentie. ren_ns_1 8db3317a (0,78), ren_ns_2 596e951b (0,80). Voorlopig
  geexporteerd als `ren_ns_onaf`.

### Gestopt (middag)
De chat liep tegen zijn eigen lengte aan (elke Grok-generatie kost hier ruim twee minuten en veel stappen, omdat Grok
sinds ~12:15 weer 60-90 s per pagina laadt). Netjes gestopt na rol, trap en twee frames van de ren zonder speer.
OVERDRACHT.md en rapport/TWIJFEL.md bijgewerkt. Verder in een nieuwe chat met ren_ns_3.

## 21-11-2026, 16:00 verder (nieuwe chat): ren zonder speer (12 frames, af)
- Werkmap opnieuw opgebouwd: `ref_hulp.png` uit post d0bb0d1c met vier tegels van 824x600 (let op: elke opgeslagen tegel
  op `scale: 1`, een kleinere schaal bewaart ook een kleiner bestand). Muis buiten de zoomregio zetten (`hover`), anders
  staat de cursor in de tegel.
- Prompt `mk_paar_ren` voor 3-9, 11, 12. Posts: 3 bcfc041d (0,81), 4 1d37b17a (0,74), 5 c3cfb0bd (0,74), 6 57d26476 (0,80),
  7 fe8f738f (0,78), 8 6937d641 (0,82), 9 e1524d20 (0,80), 11 8482acb4 (0,75), 12 83dda860 (0,83).
- Frame 10 is een compacte afzetpose (voorknie naar voren, beide voeten laag, benen dicht bij elkaar). Grok maakte er twee
  keer iets anders van: a2a02fe6 (wandelpas met beide voeten neer, 0,52) en 97985cfe (met `mk_ren_pass`, zwevende
  doorzwaaifase, 0,51). Met `mk_ren_af` (de pose uitgeschreven: "pushing off ... compact stance, NOT a wide stride")
  311ea178, 0,64: volgt de omtrek, gebruikt. Net onder de 0,65, staat in TWIJFEL.md.
- export.py: als de werkdata van een frame uit een eerdere chat weg is (hier ren_ns_1 en 2) en het frame zonder speer al
  in de repo staat, gebruikt het rapport dat beeld. Export ren_ns, 12 fps; `ren_ns_onaf` weggehaald.

## Springen zonder speer (7 frames, af)
- Prompt `mk_paar`. Posts: 0 3ed9ec30 (0,77), 1 e1692e62 (0,82), 5 6ec1405e (0,85), 6 f1df817a (0,87; de eerste poging
  7ee08306 gaf geen beeld, opnieuw verstuurd).
- 2 (afzet): eerste poging 80c32724 rechtop (0,61). Met `mk_jump_af` (sterk voorover leunen uitgeschreven) 79a15027, 0,69.
  Het hoofd uit het origineel viel naast dat van Grok (dubbel gezicht, figuur 11 px verschoven): afgewerkt met
  `--geenhoofd --schoon`, het hoofd van Grok is schoon.
- 3 (stijgen): eerste poging 3a92631d plat op de voeten (0,67). Met `mk_jump_lucht` (hangende benen, tenen gestrekt)
  a8500f77, 0,66 maar de pose klopt nu: gebruikt.
- 4 (top): 5d3529a8, 0,64. Pose klopt (gehurkt in de lucht, arm vooruit); het verschil zit in de vachtzone. Gebruikt.
- Les: bij een verschuiving van meer dan ~10 px in `terug` het afgewerkte hoofd nakijken op een dubbel gezicht.
- Export jump_ns, 12 fps.

## Bukken zonder speer (12 frames, af)
- in_1 t/m in_3 met `mk_paar`, in_4 t/m hold_4 met `mk_buk`. Posts: in_1 e9222d76 (0,75), in_2 6c001b70 (0,77),
  in_3 1ef8a8b8 (0,78), in_4 5c03b247 (0,82), in_5 38740fd9 (0,80), in_6 dd1055e6 (0,73), in_7 bda6c6b4 (0,70),
  in_8 9975dfcc (0,77), hold_1 b2462bb1 (0,76), hold_2 e534d283 (0,76), hold_3 c86428c1 (0,82), hold_4 722f0372 (0,80).
- hold_3: eerste poging 69b51dff had geen schortdoek (alleen een gele band), IoU 0,81 maar afgekeurd op het kostuum.
- Ophalen sinds in_2 met een tegel van het hele beeld (op 0,6, 1036x691) en `tools/mkuki/verwerk1.sh`; scherpte gelijk
  aan twee tegels (vergeleken op in_1 en in_2), een ronde minder per frame.
- Grok laadde rond 17:30 weer traag (tot 60 s voor de pagina); een keer gaf het assets-tabblad een venster van 0x0 en
  hing de renderer: tabblad gesloten en een nieuw gemaakt.
- Export buk_ns, 12 fps (volgorde in_1..8, hold_1..4).

## Sluipen zonder speer (begonnen, 3 van 28)
- `mk_sluip` zette bij 00 een hand op de grond (643e36df, 0,60, afgekeurd). Drie posevarianten in localStorage, elk met
  "NO hand touches the ground":
  `mk_sluip_lunge` (diepe lunge, achterbeen lang gestrekt, vuisten voor de borst),
  `mk_sluip_kort` (compact gehurkt, voeten bij elkaar),
  `mk_sluip_stap` (sluipstap: rug krom, vuisten laag voor de buik, achterste voet op de tenen, smalle stand).
- Af: 00 70a51f5a (lunge, 0,80), 01 3a1f4f18 (lunge, 0,78), 02 0b088e52 (kort, 0,74; eerst 5c2fc454 met lunge, 0,43).
- 03: met lunge 9fd9bc09, 0,51 (te diep); met `mk_sluip_stap` verstuurd, toen gaf Grok "Gebruikslimiet bereikt".
- Indeling voor de rest (op het oog, nog niet gecontroleerd): stap voor 3-7, 10, 14-21; kort voor 8, 9, 22, 23;
  `mk_sluip` (hand naar de grond) voor 11-13 en 24-27. Bij een lage IoU de andere variant proberen.
- Grok-tabblad: na een tijd hangt de renderer (scripts lopen tegen 45 s). Een vers tabblad laadt in ~30 s; per frame
  een verse `grok.com/imagine` of bij hangen het tabblad sluiten en een nieuw maken. De post-id staat ook in de tab-url
  in de tab-context, zonder script.
- Voorlopig geexporteerd als `sluip_ns_onaf`.

### Gestopt (21-11, ~19:00): Grok-limiet
Grok gaf "Gebruikslimiet bereikt" (met Upgraden/Credits toevoegen; niet aangeklikt). Volgens de afspraak gestopt.

## Sluipen zonder speer (28 frames, af)
- Vier posevarianten (alle met "NO hand touches the ground", behalve `mk_sluip` zelf):
  `mk_sluip_lunge` (00, 01), `mk_sluip_kort` (02, 08, 09, 22, 23), `mk_sluip_diep` (03-07, 10, 14-21; diep gehurkt,
  dijen bijna horizontaal, romp ver voorover) en `mk_sluip` (11-13, 24-27, hand naar de grond). `mk_sluip_stap` (03,
  a7bfeede, 0,53) was te rechtop en is niet meer gebruikt.
- Vanaf 07 een DEPTH-zin in alle prompts (welk been en welke arm nabij/ver, ver donkerder, niet links en rechts wisselen).
- IoU 0,70-0,83. Posts in /home/claude/werk/sluip_ns/ids.json; o.a. 03 1468b208, 07 90f61409, 14 9dcae121, 27 1ebc0648.
- Klikken op de verzendknop: de knop verschuift met de modus-rij (Afbeelding/Video); positie per keer meten met
  `button[type=submit]`. Grok stond bij het begin op Video: eerst Afbeelding aanzetten.
- Export sluip_ns, 12 fps; `sluip_ns_onaf` weg.

## Rol zonder speer (28 frames, af)
- Zelfde poses als de rol met speer, dus dezelfde prompts (`mk_rol3` ... `mk_rol_kniel`, nu met de DEPTH-zin); frame 1
  met `mk_paar`. Posts: 1 0bc5f742 (0,68), 2 6392f4d8 (0,78), 3 2f4fa651 (0,81), 4 7c5b0a1d (0,81).
- Indeling voor de rest (als bij rol_sp): mk_rol4 voor 5, mk_rol3 voor 6, 7, 10-12, 19-21, mk_rol5 voor 8, 9, mk_rol6 voor
  13-16, mk_rol7 voor 17, 18, mk_rol_lig 22, mk_rol_zit 23, 24, mk_rol_kniel 25-28. Afwerken vanaf 11 met `--geenhoofd
  --schoon` (zie rol_sp).
- Gestopt rond 18:45: de Chrome-tabbladen verdwenen steeds (tab-groep weg, ids ongeldig), waarschijnlijk omdat een
  andere chat tegelijk Chrome bestuurt. Voorlopig geexporteerd als `rol_ns_onaf`.

### 21-11, 19:00 verder (nieuwe chat): rol 5 t/m 28 af
- Werkmap opnieuw opgebouwd. Let op bij het ophalen van een beeld op assets.grok.com: de viewer zet een `height`-attribuut
  op de img; zonder `height:auto` in de stijl wordt het beeld platgedrukt (eerste ref_hulp was daardoor fout). Alle
  ophaalscripts zetten nu `height:auto`.
- Posts (gebruikt): 5 a2296b80 (0,74), 6 66298931 (0,73), 7 b164f7ec (mk_rol5, 0,79), 8 3c7fbcd2 (0,69),
  9 ce14b7d3 (0,69), 10 94d3f13b (0,68), 11 39561d73 (0,67), 12 762a217e (0,74), 13 aee19733 (mk_rol3, 0,73),
  14 4986055a (0,68), 15 23b1c4a1 (0,65), 16 83e04c1c (0,71), 17 367a958a (0,72), 18 75d3d3c8 (0,72),
  19 575394d6 (0,70), 20 22b261eb (0,75), 21 90a84956 (0,74), 22 adbc6f8c (0,68), 23 da31f398 (0,65),
  24 159528e9 (0,70), 25 1a6ece5e (0,62), 26 c72f1fb2 (0,75), 27 1645593a (0,76), 28 f38527ad (0,72).
- Afgekeurd: 7 30fbbff8 (mk_rol3, hoofd te hoog, 0,59), 12 7ae50bea (broek bleef paars), 13 ce978ed9 (mk_rol6, vuisten
  waar de voeten horen, 0,61), 14 0ec1a06b en f926a5ab (mk_rol3 en mk_rol6: rechtop gezet), 17 56e96b69 (rechtop) en
  0a38f91d (plat op de rug, 0,51), 18 f5837471 (gespiegeld, 0,46) en 830f6cd8 (mk_rol7: rechtop), 25 f48b710c (0,58).
- Nieuwe prompts in localStorage, elk de oude plus een ORIENTATION-zin: `mk_rol6_om` (ondersteboven houden; 14-16),
  `mk_rol7_om` (half ondersteboven, schouders op de grond; 17, 18), `mk_rol7_rug` (niet gebruikt), `mk_rol3_rug`
  (over de rug rollen, hoofd rechts laag; 19-21), `mk_rol_kniel_hand` (25, slechter, niet gebruikt).
  Zonder die zin zet Grok de ondersteboven-frames rechtop; met de zin lukt het in een keer.
- Indeling anders dan gepland: 13 met mk_rol3 (mk_rol6 faalde), 19-21 met mk_rol3_rug.
- Voor/achter gecontroleerd per frame: verre arm en verre been staan overal achter. In Mkuki zijn beide benen even donker
  (zwarte broek), zie TWIJFEL.md.
- Afgewerkt vanaf 11 met `--geenhoofd --schoon`. Export rol_ns, 12 fps; `rol_ns_onaf` weg.
- Chrome: twee keer gaf het assets-tabblad een venster van 0x0 (ook na een stille id-wissel); sluiten en een nieuw tabblad
  maken loste het op. Het Grok-tabblad bleef een keer leeg na herladen: ook sluiten en vernieuwen.

## Speerstoot (10 frames, af)
- Tom (20:08): Grok draaide hem in frame 2 en 3 met de borst naar de camera, terwijl hij in het origineel met zijn rug
  naar de camera staat. Vanaf nu bij elk frame de 3D-houding controleren (zie OVERDRACHT.md, "Houding in 3D").
- Prompts (localStorage): `mk_strike` (mk_buk met een gevechtshouding-zin en de DEPTH-zin), `mk_strike_rug` (plus
  FACING: rug naar de camera, band over de rug, geen stok), daarop `_hef` (verre vuist hoog), `_sch` (beide vuisten bij de
  schouders), `_borst` (vooroverleunend, vuisten op borsthoogte), `mk_strike_rug_steek2` (lunge, voorste arm gestrekt,
  verre elleboog naar achter, rug krom) en `mk_strike_half` (half afgewend, rechtop).
- Speermeting: overrides voor 3, 5, 6, 7, 8 en 9 (de automatische meting pakte een te korte of verkeerde lijn).
- klaar1.py heeft nu `--eiland`: losse stukjes (vachtresten) naast het lijf weg. Standaard meegegeven voor deze set.
- Posts en keuzes:
  1 fd9ae486 0,71 mk_strike (borst naar camera, als origineel)
  2 744e7977 0,64 mk_strike_rug_hef; afgekeurd 08267e71 (verre arm laag), e3074c79 (borst naar camera)
  3 d9e6e4e5 0,65 mk_strike_rug_sch; afgekeurd 67bb0265 (borst naar camera, stok achter nek)
  4 b2376889 0,60 mk_strike_rug_borst; afgekeurd 2fea8d3d (verre arm bij heup, 0,57), 21eb0e10 (vuisten te laag, 0,61). Leunt iets minder voorover dan origineel.
  5 13d297b3 0,56 mk_strike_rug_steek2; afgekeurd c2666673 (te rechtop, 0,53). Lage IoU: in het bronframe is de voorste onderarm met de speer weggehaald, Grok tekent hem erbij.
  6 9c83c4fb 0,65 mk_strike_rug_steek2
  7 2f3fcc61 0,64 mk_strike_rug_steek2 (--eiland: losse vachtrest weg)
  8 d0664a54 0,60 mk_strike_rug_steek2
  9 e6403f04 0,65 mk_strike_half; iets rechtop vergeleken met origineel
  10 3094bf84 0,78 mk_strike
- Export strike_sp, 12 fps.

## Speerworp (20 frames, af)
- Bronframes staan in `amir runc/amir_sprites/design/amir/speerworp/` (map in `THR_DIRS`). Lokaal een symlink
  `karakters/amir/speerworp` naar die map (in .git/info/exclude, niet gecommit), zodat de tools een pad onder
  `karakters/amir/` krijgen; de uitvoer staat in `karakters/amir/mkuki/speerworp/`.
- Speer zit in 00-10; 11-19 zijn zonder speer (override `geen: true`, klaar1.py en export.py slaan de speer dan over).
- Speermeting: overrides voor 00, 03-07, 09, 10 (tip/kont), 00 en 01 `kopmax`/`lintzijde` (het hoofd naast het blad werd als
  lint gezien), handen vastgezet voor 01-06 en 08 (de speer over het hoofd werd als hand gezien: witte vlek op het hoofd),
  10 met `breed: 16` (bewegingsstreep). speer_meet.py kent nu `kopmax` en `lintzijde`.
- Alles met `--eiland --geenhoofd` (het hoofd uit het origineel had resten van de speer).
- Nieuw: `tools/mkuki/schedel.py` (hap in de schedel dichten; uiteindelijk niet gebruikt, de oplossing was de hand-override).
- Prompts: `mk_worp_voor`(`_hoofd`), `mk_worp_hand`, `mk_worp_mik`, `mk_worp_spreid`, `mk_worp_lunge`, `mk_worp_los`,
  `mk_worp_profiel`, `mk_worp_na`(`_open`), `mk_worp_rugzwaai`, `mk_worp_rughoog`, `mk_worp_rugzak`.
- Posts en keuzes:
  00 90f11e31 0,76 mk_worp_voor; --geenhoofd (kruin had resten)
  01 32c86a21 0,77 mk_worp_voor; handen-override (de speer door het hoofd werd als hand gezien), --geenhoofd
  02 0ef3a970 0,76 mk_worp_voor_hoofd, aangeboden met dichtgemaakte schedel; afgekeurd f82d705f (hap in de schedel)
  03 cf9a0b88 0,73 mk_worp_hand(-zin); 04 afe01ed6 0,72 mk_worp_hand; 05 40f2e1c1 0,68 mk_worp_hand (vuist achter het oor); 06 29041614 0,62 mk_worp_mik; 07 7f3d955b 0,75 mk_worp_spreid; 08 aa3d4cb7 0,78 mk_worp_lunge. Handen vastgezet voor 03-06 en 08 (valse hand op het hoofd gaf een witte vlek).
  09 1159ad4d 0,74 mk_worp_lunge
  10 f2ee8cbc 0,82 mk_worp_profiel (strikt profiel, rug half naar ons); afgekeurd d3ca02da (te veel borst naar de camera, 0,75). Speer-override met breed 16 om de bewegingsstreep weg te halen.
  11 62c01726 0,83 mk_worp_profiel
  12 2c76d011 0,69 mk_worp_na (voorste hand vuist i.p.v. open; verre arm zichtbaar achter de rug)
  13 fc1b3765 0,68 mk_worp_na_open
  14 ce7692f7 0,67 mk_worp_rugzwaai; afgekeurd 56992d06 (borst naar de camera)
  15 9ee0d934 0,54 mk_worp_rughoog; afgekeurd 7534d266 (achterarm bij de heup i.p.v. achter op borsthoogte). Achterarm nu te gestrekt.
  16 afgekeurd 2b10ab7c (voorste arm te hoog, 0,50); volgende poging met mk_worp_rugzak (arm omlaag)
  16 afgekeurd 2b10ab7c (voorste arm te hoog, 0,50); volgende poging met mk_worp_rugzak (arm omlaag)
  16 726205c5 0,54 mk_worp_rugzak; voorste arm reikt minder ver dan origineel
  17 2bc67d6f 0,57 mk_worp_hand_neer; voorste hand iets minder ver
  18 6c659d72 0,81 mk_worp_loop; afgekeurd cda0d2a2 (te frontaal, 0,61)
  19 37c42c67 0,75 mk_worp_staan2; afgekeurd fa614249 (vechthouding met vuisten omhoog)
- Prompts erbij: `mk_worp_hand_neer`, `mk_worp_loop`, `mk_worp_staan2` (de gevechtszin van mk_strike vervangen door 'standing calmly').
- Export worp_sp, 12 fps; `worp_onaf` weg.
- Op grok.com stonden tussendoor posts van een andere sessie ("Masked Bandit ... Landing"); de tabbladen van deze run verdwenen af en toe. Geen invloed op de frames.

## Lage zwaai (af, 18 van 18)
- Speer draait mee en staat vaak verkort of achter het lijf; overrides (tip/kont) voor 3-7, 9, 10, 12 (breed 12) en 13.
- Prompts: `mk_sw_voorL` (borst half naar ons, kijkt links), `mk_sw_rugL`/`mk_sw_rugR` (rug naar ons), `mk_sw_front`,
  `mk_sw_voorR`, `mk_sw_profR` (profiel naar rechts, voorover), `mk_sw_rugveeg`, `mk_sw_rugvoor` (rug, armen naar voren op
  borsthoogte). Basis: mk_strike met "deep low crouch sweeping low" in plaats van de gevechtszin.
- Draaiing per frame (uit het origineel): 1-2 borst half naar ons, kijkt links; 3 profiel rechts, voorover; 4 rug naar ons;
  5 rug, kijkt links; 6 front; 7 rug; 8 half rug; 9 profiel rechts; 10 rug; 11 rug, kijkt links; 12 driekwart rechts;
  13-18 borst half naar ons, kijkt links.
- Posts:
  1 9e7ea321 0,78 mk_sw_rugL (Grok gaf toch borst half naar ons, zoals origineel)
  2 efca18f5 0,76 mk_sw_voorL
  3 5a9bee07 0,52 mk_sw_profR; afgekeurd 70dd9937 (te ver achterom gedraaid, 0,48)
  4 264fb60f 0,65 mk_sw_rugvoor; afgekeurd 5287e0f7 (armen naar de grond i.p.v. naar voren)
  5 5bd85721 0,53 mk_sw_rug5 (rug, kijkt links)
  6 a2c4600d 0,54 mk_sw_front6 (front, lichte ogen zoals origineel); linkerarm reikt minder ver; eerste poging 0f9c80a1 gaf geen beeld
  7 cc00f299 0,46 mk_sw_rug7; houding klopt, figuur iets korter dan origineel
  8 4de6fae7 0,60 mk_sw_half8; voorste arm hoort horizontaal naar links (speerarm), Grok zette beide handen op de grond
  9 3e936b90 0,57 mk_sw_prof9; profiel rechts klopt, romp iets rechter dan origineel
  10 f08749f2 0,39 mk_sw_rug10b; rug en hurkzit kloppen, armen iets korter; eerste poging 848ce9b4 0,31 (te rechtop)
  11 9914a979 0,56 mk_sw_rug11; rug, hoofd links, klopt; eerste poging 5868aa8d (mk_sw_half8) gaf borst en gezicht, afgekeurd
  12 d1a70380 0,53 mk_sw_drie12; driekwart rechts, gebogen, handen op de grond, klopt
  13 d7b5d375 0,23 mk_sw_v13c (zijtrap op een been, met de hand geplaatst: /home/claude/handplaats.py, het IoU-zoeken zette hem te laag); afgekeurd 35a9a10f (hurkzit), df554c7e (geen trap)
  14 2221ab35 0,76 mk_sw_v14
  15 b8326895 0,67 mk_sw_v15
  16 1ccbcbb3 0,75 mk_sw_v16
  17 938265f2 0,81 mk_sw_v16
  18 b0909d8a 0,77 mk_sw_v16
- Nieuwe prompts: `mk_sw_rug5`, `mk_sw_front6`, `mk_sw_rug7`, `mk_sw_half8`, `mk_sw_prof9`, `mk_sw_rug10b`, `mk_sw_rug11`
  ("seen FROM BEHIND ... his face is hidden"; zonder die zin gaf Grok borst en gezicht), `mk_sw_drie12`, `mk_sw_v13c`
  ("SIDE KICK ... only ONE foot touches the ground"), `mk_sw_v14`, `mk_sw_v15`, `mk_sw_v16` (ook voor 17 en 18).
- paar.py terug: kandidaat linksboven (het voorbeeld) telt niet meer mee; hij won bij frame 13 op IoU. Nieuwe
  omgevingsvariabelen `PAAR_SCHAAL` ("0.7,1.05,15") en `PAAR_BEREIK` (zoekbereik in px) voor een lastig frame.
- Frame 13 is met de hand geplaatst (onderkant figuur op onderkant origineel, midden op de mediaan-x): het origineel heeft
  een veeg onder de voeten en een speerstreep, waardoor het IoU-zoeken hem te laag zette. Lage IoU (0,23) komt door het
  andere silhouet (Grok trapt hoger en staat rechter), de houding zelf klopt.
- Zoomtegel nu op 822 px breed (venster 1360x549); verwerk1 schaalt toch op naar 1728, dus geen verschil.
- Export sweep_sp, 12 fps.

## Combo (af, 15 van 15)
- Origineel: `aanval/combo/combo_00..14`, speer in elk frame; overrides (tip/kont) voor 01, 06, 11 (de speer kruist het hoofd
  of de romp en werd slecht gemeten).
- Draaiing per frame (uit het origineel): 00 driekwart rug, kijkt links; 01-04 rug (01 arm hoog, 02 armen recht omhoog,
  03 armen boven het hoofd, 04 smal); 05 front, armen gekruist boven het hoofd; 06-09 driekwart voor, kijkt links, vuisten
  op een diagonaal; 10-11 driekwart voor, vuisten voor de borst; 12-14 driekwart voor, voorste arm gestrekt naar links.
- Prompts: basis `mk_cb_basis` (= mk_strike zonder FACING), dan `mk_cb1`..`mk_cb6`, `mk_cb7b`, `mk_cb8b`, `mk_cb11`, `mk_cb13`.
- Posts:
  1 163457cf 0,65 mk_cb1 (driekwart rug, kijkt links)
  2 0404bf49 0,65 mk_cb2 (rug, arm hoog)
  3 57939581 0,43 mk_cb3 (rug, armen recht omhoog; stand smaller dan origineel)
  4 1465cd26 0,51 mk_cb4 (rug, armen boven het hoofd; geplaatst met PAAR_SCHAAL=0.8,1.1,7 PAAR_BEREIK=120; Grok tekende een stompje stok tussen de vuisten, valt onder de speer)
  5 5645bb5b 0,79 mk_cb5 (rug, smal, armen omhoog; vuist niet geplakt)
  6 f5924b7b 0,76 mk_cb6 (front, armen gekruist boven het hoofd)
  7 ad154b82 0,78 mk_cb7b (driekwart voor, vuisten op een diagonaal); afgekeurd d30061ed (beide vuisten rechtsboven, 0,46)
  8 fe05f5c8 0,76 mk_cb8b (driekwart voor, voorste vuist ver links); afgekeurd 11e8e31a (onderste vuist bij de borst i.p.v. naar voren)
  9 828e1d27 0,75 mk_cb8b
  10 aa56ec17 0,72 mk_cb8b
  11 374bd6be 0,77 mk_cb11
  12 4eab34b6 0,78 mk_cb11
  13 cc5ec0d1 0,61 mk_cb13
  14 888a5557 0,69 mk_cb13
  15 845cfbd2 0,73 mk_cb13
- Export combo_sp, 12 fps.

## Stofsweep (af, 14 van 14)
- Origineel: `aanval/stofsweep/stof_00..13`, speer in elk frame. Overrides tip/kont voor 01, 02, 08, 10-13 (breed 16 voor
  01, 02; 30 voor 11-13, waar de speer achter het hoofd staat); handen [] voor alle frames (valse handen op het lint).
  In s14 (stof_13) het lint linksboven met de hand weggehaald voor Grok.
- Draaiing: 00-02 front, kijkt links; 03-07 driekwart voor, kijkt links; 08 gebogen, driekwart voor; 09 profiel links,
  hurk; 10-13 rug naar ons, armen voor de borst.
- Prompts: `mk_st1`, `mk_st3`, `mk_st4`, `mk_st5`, `mk_st8b`, `mk_st9`, `mk_st10`, `mk_st11`, `mk_st12` (basis mk_cb_basis).
- Posts:
  1 4aa84df0 0,79 mk_st1
  2 d7cde5ff 0,77 mk_st1
  3 71412c45 0,79 mk_st3
  4 26b2dece 0,83 mk_st4
  5 c90e68ba 0,82 mk_st5
  6 630938d8 0,81 mk_st5
  7 12379372 0,75 mk_st5
  8 75d3916f 0,67 mk_st8b; afgekeurd 3820cebd (te rechtop, voeten naast elkaar, 0,59)
  9 bd9f7e65 0,71 mk_st9
  10 f5bb3bda 0,71 mk_st10
  11 9b66ae8d 0,62 mk_st11 (rug, stap)
  12 8eddc9ec 0,69 mk_st12
  13 e447bac4 0,61 mk_st12
  14 7ca7714b 0,64 mk_st12
- Export stof_sp, 12 fps (metadata.json van het origineel noemt 24 fps met ticks; de plaatsing volgt de frames).

## Rol/worp (af, 33 van 33)
- Origineel: `beweging/rol/worp/worp_1..33`, speer in 1-23. Speeroverrides voor 12-15 (de speer kruist het lijf).
- Draaiing en voeten (Tom, 22-11: ook letten op welke voet voor/achter en waar de handen zitten): 1-5 profiel links,
  hurk, voeten verspringend, vuist bij de enkels/knieen; 6-8 opkomen, achterste voet omhoog achter hem; 9-11 knie voor
  omhoog; 12-14 uitstap naar links, borst half naar ons; 15-23 diepe uitval, werphouding vastgehouden (een Grok-beeld);
  24-26 arm recht omhoog; 27 arm ver naar voren-onder; 28 driekwart rug; 29-33 rug, arm omhoog achter (een Grok-beeld).
- Prompts: `mk_rw1b` (FEET-zin), `mk_rw2`, `mk_rw4`, `mk_rw5`/`mk_rw5b`, `mk_rw7a`, `mk_rw8`, `mk_rw9`, `mk_rw12`,
  `mk_rw14`, `mk_rw19`, `mk_rw24`, `mk_rw28`, `mk_rw27b`, `mk_rw30b`.
- Posts:
  1 15dee20c 0,57 mk_rw1b (vuist bij de enkels, voeten verspringend); afgekeurd 746c2623 en 0a3c8ca9 (rechtop, handen naar voren op de grond, voeten naast elkaar; Tom)
  2 16e8b404 0,75 mk_rw2
  3 4d550327 0,76 mk_rw2
  4 fbfc4ecd 0,78 mk_rw4
  5 8198a958 0,59 mk_rw5b (laag, vuisten bij de knieen; voeten minder ver uit elkaar dan origineel); afgekeurd 6a48cdeb (te rechtop)
  6 dd7f48c4 0,70 mk_rw5
  7 881fe5a0 0,73 mk_rw7a
  8 f8436c73 0,69 mk_rw8 (achterste voet omhoog achter hem); afgekeurd 7c8e884c (knie voor omhoog, hoort bij 9)
  9 0e9f6377 0,66 mk_rw9
  10 7c8e884c 0,60 mk_rw9 (Grok-beeld van de eerste poging op 8 hergebruikt)
  11 8243e505 0,61 mk_rw9
  12 ab7ad7a3 0,57 mk_rw12 (romp rechter en borst meer naar ons dan origineel; 7e280a73 met mk_rw12b gaf hetzelfde, 0,50)
  13 6ca081b5 0,67 mk_rw12
  14 67faf846 0,71 mk_rw14
  15-23 41581998 0,64..0,55 mk_rw19 (een Grok-beeld voor de hele vastgehouden werphouding; achterste vuist iets lager dan origineel); eerst 67faf846 geprobeerd, 0,51..0,44
  24 743c84de 0,56 mk_rw24 (voorste arm lager dan origineel)
  25 743c84de 0,68 mk_rw24
  26 743c84de 0,59 mk_rw24 (origineel buigt al naar links over het hoofd; Grok-beeld van 24/25)
  27 54c7aa0e 0,58 mk_rw28 (arm ver naar voren klopt, maar borst iets naar ons; origineel draait al met de rug)
  28 0dd729b1 0,50 mk_rw27b (rug naar ons, klopt)
  29-33 c209f6ea 0,62..0,70 mk_rw30b (rug, arm omhoog achter, vastgehouden)
- Export rolworp_sp, 12 fps.

## 22-11-2026, 02:00 nakijken (rapport/NAKIJKEN.md), nieuwe chat
- Werkmap opnieuw opgebouwd; `ref_hulp.png` uit post `d0bb0d1c` met een zoomtegel van het hele beeld (0,6) en `raster.key`.
- Prompts: basis `mk_nk_basis` (= mk_rw12 tot aan FACING), per frame `mk_nk_<set><n>` met FACING/BODY/FEET/ARMS.
- `export.py`: een frame dat in deze chat niet opnieuw is gemaakt komt nu uit de repo in het rapport (met speer en
  vuistlaag), in plaats van te ontbreken; plaatsing.json blijft voor dat frame ongemoeid.
- Rol/worp 24-33 hebben geen speer (worp is los), maar hadden speerplaatsingen en bij 29 en 33 een vuistlaag van een valse
  meting. `"geen": true` in overrides.json voor 24-33, vuistlagen en plaatsingen daarvan weg.
### Rol/worp
- worp_27: VERVANGEN, post `17ac79af` 0,73 (was 0,58), `mk_nk_rw27`: rug naar ons, voorste arm ver naar links. Klopt.
- worp_26: VERVANGEN, post `8dcea7bc` 0,76 (was 0,59), `mk_nk_rw26`: arm in een boog over het hoofd naar links. Klopt.
- worp_12: NIET vervangen. Drie pogingen (`33a243ed`, `1c0188db` 0,45, `5da87ce3`; mk_nk_rw12, rw12b, rw12c, ook met
  "pure side view", "only one eye", "torso 45 degrees"): Grok zet de romp steeds rechtop met de borst naar ons, de stoot
  naar links. Niet beter dan het huidige frame.
### Lage zwaai
- sweep_8: VERVANGEN, post `ae7d9ae6` 0,55 (was 0,60), `mk_nk_sw8`: driekwart rug, een arm horizontaal naar links, een hand
  op de grond, been ver naar rechts. Lagere IoU door een iets hoger hoofd, maar de houding klopt nu (eerst twee handen op de grond).
### Stofsweep
- stof_07 en stof_08: NIET vervangen. Op dezelfde schaal naast het origineel staat het hoofd van Mkuki al even hoog als in
  het origineel; Grok maakt de hurk niet dieper zonder de figuur te verkleinen. stof_08: `52874da5` (ogen dicht, halve hurk),
  `f6a4dd37` 0,67 (zelfde hoogte als nu), `f3090ed6` (rechter); stof_07: `cb2433f7` 0,55 (lager, maar 10% kleiner geplaatst).
  Prompts `mk_nk_st07`, `mk_nk_st08`, `mk_nk_st08b`, `mk_nk_st08c`.
### Ren met speer (kruisframes)
- Niet eerder gedaan in de rencyclus-chat (REN_WISSEL.md raakte 4 en 10 niet aan).
- ren_sp_4: VERVANGEN, post `10138fbb` 0,61, `mk_nk_ren4` (benen kruisen, beide voeten achter de heup, geen wandelpas).
  Schoon, geen geplakte benen of rafelige vuist meer. Borst iets meer naar ons dan in het origineel.
- ren_sp_10: VERVANGEN, post `0a0007d5` 0,53, `mk_nk_ren4`: compacte afzet, voorste voet iets verder naar voren dan in het
  origineel, maar schoon. `6f568575` met `mk_nk_ren10` (benen dicht bij elkaar) gaf twee rechte benen, afgekeurd.
- Let op: de verre-been-correctie van REN_WISSEL.md (wissel.py) is niet over de nieuwe 4 en 10 gehaald; beide benen zijn
  even licht. In de kruisframes valt dat weinig op.
- export.py haalt nu een oude vuistlaag weg als een nieuw frame geen vuist heeft.
### Rol/worp, prioriteit B
- worp_15 t/m 23: VERVANGEN, een nieuw Grok-beeld voor de vastgehouden werphouding, post `3cecc798`, `mk_nk_rw19` (gemaakt op
  worp_19; achterste vuist hoog boven het hoofd, voorste hand open). Per frame apart uitgelijnd: IoU 0,62 tot 0,71 (was
  0,64 tot 0,55). De achterste vuist zit nu op de schacht, dus de vuistlaag is voor 16-22 nu ook geplakt (was niet); bij 23
  niet (hand op 319,142 niet gevonden, zoals eerder). Bij 15 staat de vuist net boven de schacht.
- worp_24: VERVANGEN, post `cb68dc87` 0,77 (was 0,56), `mk_nk_rw24`: voorste arm op schouderhoogte naar links.
- worp_5: VERVANGEN, post `f8fe1b2c` 0,55 (was 0,59), `mk_nk_rw5`: voeten ver uit elkaar en verspringend (voor plat, achter
  op de bal). Zelfde hoogte als het vorige frame.
### Lage zwaai, prioriteit B
- sweep_9: VERVANGEN, post `af377795` 0,55 (was 0,57), `mk_nk_sw9`: profiel rechts, romp bijna plat voorover, hand op de grond,
  achterarm schuin omhoog. Romp nu duidelijk vlakker.
- sweep_13: VERVANGEN, post `4d54af81`, `mk_nk_sw13b` (lage trap, knie gebogen, standbeen rechts). Met de hand geplaatst
  (`/home/claude/handplaats.py ... 1.0 0 0`, IoU 0,31; het IoU-zoeken gaf 0,13 en zette hem verkeerd). Trap lager dan het
  vorige frame, dichter bij het origineel; standbeen nu het rechter. `f6216d9b` met `mk_nk_sw13` (hoge trap) afgekeurd.
- sweep_6: VERVANGEN, post `2a49d175` 0,52 (was 0,54), `mk_nk_sw6`: linkerarm verder naar links-onder. Iets lagere IoU door
  de bredere knieen, maar de arm reikt nu verder.
- sweep_10: NIET vervangen. `f675b74f` (`mk_nk_sw10`) gaf een arm ver naar rechts, maar maar een arm zichtbaar en hij kwam
  hoger en verschoven te staan (0,35). Het huidige frame (twee armen) blijft beter.
