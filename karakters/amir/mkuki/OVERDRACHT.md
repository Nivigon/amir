# Overdracht Mkuki-productie (stand 21-11-2026, avond)

Klaar en gepusht op `claude/mkuki`: idle (22), ren met speer (12), springen met speer (7), bukken met speer (12),
sluipen met speer (22), rol met speer (28), trap (2), ren zonder speer (12), springen zonder speer (7), bukken zonder speer (12), sluipen zonder speer (28), rol zonder speer (28), speerstoot (10), speerworp (20). Zie `LOG.md` voor alle keuzes per set.

## Nog te doen, in deze volgorde

1. (af)
2. (af)
3. Aanvallen: speerstrike 10 (af), speerworp 20 (af), lowsweep 18 (af), combo 15 (af), stofsweep 14 (af), rol/worp 33 (volgende), stofsweep 14, rol/worp 33. De sluipaanval niet.
4. Eindrapport in `rapport/`: overzichtsplaten en GIFs (export.py maakt die per set), TWIJFEL.md bijwerken
   (draaiende speerframes, rol 17 tot 22, en alles wat handwerk vraagt). GEEN recolours (Tom: "van mij hoef je
   overigens nog niet te recoloren").

Paden staan in `notities/mkuki.md` (het plan). Zoek een pad op met `ls` als het niet klopt.

## Werkwijze per set

Werkmap per set: `/home/claude/werk/<set>/` met `lijst.txt` ("sN pad" per regel).

1. Speer eruit controleren: `python3 tools/mkuki/speercheck.py /tmp/x.png <paden>` en de plaat bekijken
   (groen = weg). Klopt iets niet, een override in `tools/mkuki/overrides.json` (sleutel = pad onder `karakters/amir/`).
2. Per frame een `sN.spec` met `{"speer":true,"draai":false}` (zonder speer: `"speer":false`; ondersteboven
   in de rol: `"draai":true`, dan wordt het frame omgedraaid aangeboden en teruggedraaid).
3. `python3 tools/mkuki/paar.py bouw /home/claude/werk/<set>/sN <pad>` (vanuit `/home/claude/amir`).
4. Grok (zie hieronder), beeld ophalen, plakken: `tools/mkuki/plak4id.sh werk/<set>/sN_grok.png id00 id10 id01 id11`
   (1728x1152). Komt een beeld terug op een andere maat (bv. 1248x832): `tools/mkuki/plakmaat.sh uit.png 1248 832 ids`.
5. `python3 tools/mkuki/paar.py terug werk/<set>/sN` print de IoU. Onder ~0,65, of een vergelijkplaat die de pose
   niet volgt: opnieuw genereren, eventueel met de pose in de prompt benoemd.
6. `python3 tools/mkuki/klaar1.py werk/<set>/sN.npy <pad> --eiland` (voeten van Grok; `--benen` alleen als noodgreep, dan in TWIJFEL.md).
7. `python3 tools/mkuki/export.py <setnaam> 12 <paden in speelvolgorde>`, plaat bekijken, LOG.md bijwerken,
   committen (Nederlands, met de attributieregels) en pushen naar `claude/mkuki`. Geen pull request.

## Werkmap opnieuw opbouwen (na een nieuwe chat)
De werkmap `/home/claude/werk/` verdwijnt met de chat. Nodig: `werk/een/ref_hulp.png` (omgekleurde referentie, Grok post
`d0bb0d1c-5942-47dd-830d-0d74fe2467da`, 1648x1200: ophalen met vier tegels van 824x600 via `tegel.sh`, dan keyen met
`raster.key` en bijsnijden; zie LOG.md 11:00). `werk/klaar/` wordt per set opnieuw gevuld door klaar1.py.

## Ophalen (sneller dan de vier tegels)
Snelst: een tegel van het hele beeld op 0,6 (img-breedte W*0.6/1.25, `height:auto`, zoom [0,0,829,553] scale 1), dan
`tools/mkuki/verwerk1.sh werk/<set> sN <postid> <id>`. De muis eerst buiten beeld (`hover` 1400,640).
Oude manier:
Twee tegels van 967x461 CSS-px (1209x576) vanaf beeld-x 519 (left -415.2px), boven en onder (`R(519,576)`), dan
`tools/mkuki/verwerk.sh werk/<set> sN <postid> <id boven> <id onder>`. Staat de figuur verder links: `tegelxy.sh`.
Werk met twee tabbladen: een voor grok.com, een voor assets.grok.com (een batch mag niet van domein wisselen).
De post-id staat in de tab-url na het versturen; `location.pathname` uitlezen loopt vaak tegen een time-out als Grok traag is.
Versturen: na `insertText` op de verzendknop klikken (1236,462); de submit-knop via script werkt niet altijd.

## Grok via Claude in Chrome

- Tab: roep `tabs_context_mcp` aan, gebruik de Grok-tab (was 391493666) of maak er een.
- `https://grok.com/imagine` openen, ~18 s wachten, `find` "file input" (meestal ref_115), `file_upload` met origin `https://grok.com`.
- Prompt staat in localStorage op grok.com: `mk_buk` (bukken), `mk_sluip` (sluipen), `mk_paar`, `mk_paar_ren`.
  Voor een nieuwe set: kopieer `mk_buk` en vervang de zin "He is crouching low, knees bent wide; keep the crouch
  exactly as drawn." door een zin over de pose van die set. Sla op als `mk_<set>`.
- Zetten: `document.execCommand('insertText',false,localStorage.getItem('mk_<set>'))` in `.tiptap.ProseMirror`, dan Return.
- Na ~20 s: id = laatste deel van `location.pathname`. CONTROLEER dat het beeld laadt
  (`new Image()` op `https://assets.grok.com/users/cd0c0caa-675a-4fe6-b7fe-024cc6e0663f/generated/<id>/image.jpg`).
  Laadt het niet: opnieuw versturen. Ids bewaren in localStorage (`mk_<set>_ids`) en in `werk/<set>/ids.json`.
- Ophalen: navigate naar die assets-url (eigen batch, nooit samen met een grok.com-navigate), dan
  `img` op ware grootte zetten (breedte w/1.25, en ALTIJD `height:auto`, anders is het beeld platgedrukt) en `Q(c,r)` verschuift met -w/2.5*c, -h/2.5*r; vier keer
  `zoom` region [0,0,691,461] scale 1 save_to_disk. De ids voor plak4id zijn de random stukjes in de bestandsnamen
  in `/tmp/claude-tool-results/<sessie>/`.

## Stoppen

Alleen bij een Grok-limiet, moderatie of een browser die na 2 à 3 pogingen niet reageert: LOG.md bijwerken,
committen, pushen, korte samenvatting. Verder niets vragen, zelf beslissen en keuzes in LOG.md zetten.
Een lange chat, een trage Grok of veel stappen zijn GEEN reden om te stoppen (Tom, 21-11: "ik heb liever dat de
nieuwe chat gewoon doorgaat"). Werk door, push na elke set, en houd de context zuinig: bekijk tegels op lage
schaal (0,3) en alleen de vergelijkplaten die twijfel geven.

## Voor- en achterkant (Tom, 21-11)
Een frame met de goede omtrek kan toch de verkeerde kant vooraan hebben: IoU ziet dat niet. Bij elke vergelijking
kijken of het verre been en de verre arm achter en donker staan zoals in het origineel. De prompts hebben een DEPTH-zin.

## Houding in 3D: verplichte controle per frame (Tom, 21-11 20:15)
Bij ELK frame, ook in alle toekomstige sets, voor je het afwerkt vergelijken met het origineel:
1. Draaiing van het lijf: borst naar de camera, half ingedraaid, of rug naar de camera (bij Amir: zie je de vacht op
   de rug of op de borst?). Grok draait hem graag met de borst naar voren; dat is fout als het origineel de rug laat zien.
2. Welke schouder en welke arm vooraan staan, en waar beide vuisten zijn.
3. Welk been voor staat en welk achter, en welke voet vooraan.
4. Verre arm en ver been achter en donker.
Klopt een punt niet: afkeuren, ook bij een goede IoU. In de prompt de houding uitschrijven met een zin zoals in
`mk_strike_rug` (FACING: rug naar de camera, band over de RUG, borst van ons af) of een ARMS-zin. Een rug-frame zonder
FACING-zin aanbieden heeft geen zin. Twijfel in TWIJFEL.md.
