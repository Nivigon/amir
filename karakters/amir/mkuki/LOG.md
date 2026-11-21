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
