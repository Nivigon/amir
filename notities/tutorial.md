# Tutorial: The First Hunt, de mentor en zijn tekstwolk

Kop in de HTML: `// ---- tutorial: de mentor en zijn tekstwolk (level.mentor, zie notities/tutorial.md) ----`, direct na
`checkTips`. Grep: `MENTOR`, `mentorReset`, `mentorUpdate`, `mentorTeken`, `mentorWolkTeken`, `mentorVal`, `mentorKleur`,
`mentorOpname`. Het level is `TUT_1` (The First Hunt, vroeger Test 89), in de reeks `TUT_LEVELS` en te spelen met de knop The First Hunt onder Single Player (`btnTutorial`; zolang hij nooit uitgespeeld is staat er "Start here" op, daarna een vinkje, `TUT_SLEUTEL`), de opname `tools/mentor_opname.js`, het spoor
`design/tutorial/mentor_spoor.json`.

## Wat het is

De eerste tutorial voor nieuwe spelers (ontwerp met de opdrachtgever, 22-11-2026): bewegen leren zonder speer en zonder
vijanden. Een andere jager loopt voor Amir uit. Voorlopig is dat een omgekleurde Amir: de broek in `MENTOR.broek` (turkoois,
via `broekBeeld`) en een donkerder huid (`MENTOR.huid`: de tinten van rood tot oranje, niet te licht, zodat het felle lint
blijft). Identiteit en verhaal komen later; dan kan hij eigen art krijgen.

Bij elk station doet hij het stuk eerst voor ("Watch."), draait zich om, en wacht in zijn idle tot de speler bij hem is
(`MENTOR.bij`, op de grond, en minstens een seconde na zijn aankomst) en gedaan heeft wat het station vraagt (`eis`: `rol`,
gemeld door `rolStart` via `mentorEvent`, of `sprint`, een halve seconde met Shift over de grond rennen). Staat de speler stil
bij hem zonder het gedaan te hebben, dan zegt hij `nog`. Dan "goed zo" (`ok`, met `okDuur` per station), en hij doet het
volgende voor. Voorbij hem lopen kan niet: zolang hij uitlegt, voordoet of aftelt houdt hij de speler `MENTOR.voor` achter
zich (niet in de race en niet bij het slot).

De camera houdt hem in beeld zolang hij voordoet, uitlegt of wacht (niet in de race en niet bij het slot): horizontaal
schuift het midden alleen zover als nodig is tot hij binnen `MENTOR.cam.marge` van de rand staat (`mentorCamKlem`, in de
meekijkende camera), en in de hoogte kijkt de camera naar de laagste vloer van de twee, zolang de hoogste nog in beeld past
(`mentorCamH`, in `updateCamera`). Zo zie je hem ook van het hoge terras springen en onder de stam door kruipen als je
boven blijft staan.

Hij wordt getekend vlak voor Amir (na de lichtkaart), in dezelfde stand van de camera; eerder in het beeld stond hij op
een hogere laag te zweven.

## Het spoor: opgenomen, niet nagebouwd

De mentor heeft geen eigen natuurkunde. `tools/mentor_opname.js` speelt het level in Chromium met Amir (op vaste 60 fps,
met echte toetsaanslagen) en de haak `mentorOpname` (naast `pvpVang`) legt per beeld vast welk plaatje waar stond. Het spel
speelt dat terug op 30 fps. Elk stuk (`segs[i]`) eindigt met omdraaien en een idle; vanaf `lus` speelt hij die idle in een
lus. Per beeld: `[x, h, beeld, dx, dy, dw, dh, spiegel, opDeGrond]`, in sprite-eenheden zoals bij PvP.

Verander je het level (een kei, een gat, een terras), neem dan opnieuw op: `node tools/mentor_opname.js` (met `--spoor` zie
je per tiende seconde x, hoogte en op de grond, om de opdrachten bovenin het script af te stellen). Loopt hij ergens vast,
dan meldt het script FOUT en schrijft het niets weg. Verandert er iets aan Amirs sprites, dan ook.

## Het level: `mentor`

```
mentor: { spoor, finish, prijs: {x, h}, win, verlies, vallen: [grappen], stations: [
  { zeg, seg, ok, eis, nog, kijk, terug, race } ] }
```

- `zeg`: wat hij zegt terwijl hij wacht. Toetsen als `[LEFT]`, `[RIGHT]`, `[UP]`, `[DOWN]`, `[SHIFT]`, `[SPACE]`, `[V]`,
  `[E]` worden knopjes in de wolk (`MENTOR_TOETS`).
- `seg`: welk stuk hij daarna voordoet. Zonder `seg` (maar met `ok`) gaat hij meteen door naar het volgende station.
- `eis` en `nog`: wat de speler eerst moet doen, en wat hij zegt als de speler bij hem is zonder het gedaan te hebben.
- `kijk`: de tekst aan het begin van het voordoen (standaard "Watch.", `false` voor geen).
- `terug`: een veilige plek voor een stuk. Een val (`fallDeath`, via `mentorVal`) zet de speler op de dichtstbijzijnde
  `terug` achter hem (op plek, niet op station: in de race loopt het station al vooruit), met een korte fade
  (`MENTOR.val`) en een grap uit `vallen`; de uitleg van het station blijft achter de grap staan.
- `race`: aftellen (3, 2, 1, Go!), dan speelt hij zijn stuk op `MENTOR.race.tempo` (iets trager dan opgenomen). Wie het
  eerst voorbij `finish` is wint; wint de speler, dan komt er een kalebas op `prijs`.

`readLevel` neemt het veld over. In de sandbox doet de mentor niets.

## De kruipstam (`kruipstammen`)

**Vervangen (26-11-2026):** The First Hunt heeft nu op beide plekken (-3175 en -7730) een korte holle stam van droog
savannehout met een boma erop (`holstamSoort: 'savanne'`, `holstammen: [{x, s: 0.45, n: 0.5, boma: true}]`, zie "de
holle stam" in `notities/wegwijzers.md`). De kruipstam hieronder zit nog in de code, maar geen level gebruikt hem.

Geen zwevende rots meer (de opdrachtgever wil niets dat nergens aan vastzit): een omgevallen dode stam op twee keien, een
Grok-plaat (`design/tutorial/stam_keien.png`, gemaakt met de stijl van `design/tree.png` en `design/boulder.png`, wit
weggeknipt). `kruipstammen: [{x, s}]`, `x` het midden. readLevel zet er een onzichtbare zwevende laag onder
(`look: 'geen'`, `kruipstamDak`) met de onderkant van de stam als `onder` (163): staand loop je ertegenaan, kruipend kom
je eronder door. De keien staan net achter het pad. levelcheck telt zo'n kruipdak niet mee in de sprongen tussen zwevende
lagen.

## De wolk

`mentorWolkTeken` tekent na alles (bij de HUD), op de plek boven zijn hoofd die `mentorTeken` in schermpixels vastlegt: een
donker vlak met een gouden rand, een staartje naar zijn hoofd, het naambordje HUNTER, en de tekst met knopjes. Hij poppt even
op als de tekst wisselt. De grootte schaalt met de hoogte van het scherm. De balk met de toetsen bovenin gaat in dit level weg.

## Open

- De panter aan het eind (de sluiples: hoog gras, omkijken met een tell, de speer van de mentor, steken): het volgende stuk.
- De stem (ElevenLabs) per regel: de opdrachtgever voegt die zelf toe.
- Op een telefoon staan er nog toetsen in de wolk in plaats van de knoppen.
- `offline-assets.json` kent het spoor nog niet: draai `tools/gen-offline-manifest.py` op een volledige checkout. Zonder het
  spoor is het level gewoon speelbaar, alleen zonder mentor.
- Het level staat nu in Test levels; als het af is, krijgt het een eigen plek in Campaign.
- De klim: een laag savanneterras, dan een plateau van rots (een hoge savannelaag wordt onderin zwart) met een richel aan
  de wand.
