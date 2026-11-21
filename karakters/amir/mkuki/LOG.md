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
