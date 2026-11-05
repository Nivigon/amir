# De rol: een gevechtsrol naar voren

V (of op een telefoon de rolknop, links van de E onderaan) laat Amir induiken, over zijn rug naar voren
rollen en laag gehurkt overeind komen, met een hand op de grond. Een richting ingedrukt bij de start kiest
de kant; anders rolt hij de kant op die hij kijkt.

## Gedrag (`ROL`, `rolStart`, `rolUpdate`)
- Alleen op de grond, niet in de lucht, niet in het water (dieper dan 0,3), niet tijdens een steek, zwaai,
  worp of renstoot, en niet als Amir vast staat (`amirVast`).
- Tijdens de rol is `amirVast()` waar: springen, steken, werpen, bukken, E en het schild doen dan niets, en
  de pijltjes sturen hem niet (`if (rol) dir = 0`).
- Onkwetsbaar vanaf de start: `ROL.onkw` (0,6 s, het duiken en rollen), via `invuln` en `invulnStil`
  (zonder knipperen). Na de rol koelt hij `ROL.koel` (0,5 s) af; de ring om de rolknop loopt dan vol
  (`rolKlaar`).
- De rol duurt 0,87 s: 27 frames van 30 ms en de hurk 60 ms (`ROL.ms`, `ROL.eindMs`; eerst 42 ms, dat was te traag).
- De wereld schuift hem `ROL.afstand` (340 wereld-px) vooruit tussen frame `ROL.van` en `ROL.tot`, zacht in
  en uit (`rolVoortgang`). Aan de rand van een ravijn schuift hij niet verder (`gatOp`), net als de renstoot;
  rotsen, wanden en de rest houden hem tegen zoals altijd (de klemmen na `rolUpdate`).
- Een treffer na het onkwetsbare stuk, een val of loskomen van de grond breekt de rol af (`rolEind`).
- Het geluid: `sounds/amirrol.mp3` (0,84 s, `ROL.geluid`), bij de start: de zwiep van de duik en op 0,25 s de plof
  als hij de grond raakt, wat valt op frame 8 en 9 van de rol.
- In de sandbox onder **Speer en spullen** (bij Renstoot): **Rol: aan/uit** (`sbrol`).

## De frames
- `karakters/amir/beweging/rol/met/rol_1..28.png` (speer erin gebakken) en `.../zonder/` (zonder speer,
  voor als hij hem kwijt is). Canvas 554 x 409, grondrij 387, kijkt naar links zoals de gewone sets.
- `ROL.anker` per frame is het midden van zijn lijf (gespiegeld draait de kolom mee, `ROL.w - anker`), dus het
  beeld rolt niet zelf vooruit: de wereld doet dat. `ROL.schaal` = 275/309: zijn lijf is staand 309 px in de rol
  en 275 in de gewone sets.
- Bron: Grok-clip `roll.mp4` (736 x 400), 28 frames gekozen en gekeyed in de Animeer tool Amir rol
  (https://claude.ai/artifact/MXKfBdQxtwHtckhvPAQDGj), daar de speer per frame geplaatst. De broek is van
  het grijsblauw van Grok naar het paars van de gewone sets gezet. Het bakscript staat in het project
  (`claude/animeer_tool_amir_rol.md`).

## De rol-worp (F tijdens de rol)

`ROL_WORP`, `rolWorpDruk`, `rolWorpStart`, `rolWorpUpdate`, `rolWorpLos`.

- F (of de slagknop) vanaf rolframe `ROL_WORP.van` (13, de tweede helft) tot de landing wordt onthouden (`rol.worp`);
  op het aftakframe `ROL_WORP.tak` (24, frame 25 in de tool: hij landt op zijn voeten) gaat de rol over in de worp.
  `thrPress` stuurt F tijdens de rol naar `rolWorpDruk`; daarbuiten blijft alles zoals het was.
- Perfect: F in de laatste `ROL_WORP.perfect` (3) frames voor de landing. Dan vliegt de speer harder
  (`perfectKracht` 1,3 tegen `kracht` 1) en staat er even "Perfecte worp!".
- Alleen met de speer in de hand (`rol.met`). Tijdens de worp is `amirVast()` waar; onkwetsbaar is hij niet meer
  (de rol is dan al voorbij `ROL.onkw`), dus in de uitval en de nazwaai is hij te raken. Daarna koelt de rol af
  (`ROL.koel`), net als na een gewone rol.
- 33 frames: `karakters/amir/beweging/rol/worp/worp_1..33.png` (524 x 475, grondrij 450), `ROL_WORP.ms` per frame
  (35 ms door de uitval, 30 ms door de worp, de nazwaai 300 ms), `ROL_WORP.tempo` versnelt of vertraagt.
- De speer zit erin gebakken t/m frame 22 (index); op `ROL_WORP.los` (23) vliegt de echte speer (`rolWorpLos`):
  een vlakke worp vanaf de punt zoals Tom hem op dat frame zette (`ROL_WORP.punt`, bronpixels t.o.v. anker en
  grond), met dezelfde bijwerkingen als `looseSpear` (speer weg, de volgende van de rug).
- Het anker per frame is het midden van zijn lijf; de wereld schuift met de verschuiving van dat anker mee, zodat
  de uitval echt naar voren gaat en zijn achterste voet blijft staan. Niet een ravijn in (`gatOp`).
- Ontwerp en clips: zie het project, `claude/animeer_tool_amir_rol.md` (startbeeld uit rolframe 25, tussen- en
  eindframe vanaf het basisontwerp, twee Grok-clips aan elkaar).

## Test 60: Rol-worp, en de oefendoelen

- `rolWorpProef: true` in een level: drie oefendoelen (runeschijf op een paal, `rolDoelen`, `rolDoelTeken`), de rug
  vult zich steeds aan (speren genoeg, met `rugMax: 5`), en in de pauze onder Instellingen de knop
  **Rol-worp: test** (`pzrolw`, `ROL_WORP_SCHUIF`): vanaf welk rolframe F telt, het perfecte venster, het tempo,
  de kracht (gewoon en perfect), en de hoogte en afstand van een nieuw doel. De browser onthoudt de stand
  (`amir.rolworp`). Ook in de sandbox.
- T (in Test 60 en de sandbox) of de knop **Doel voor Amir neerzetten** zet een doel `ROL_DOEL.afstand` Amir voor
  hem uit op `ROL_DOEL.hoog` Amir (standaard 1,22: de hoogte van de punt op het losframe). Een treffer laat de schijf
  flitsen, telt mee ("Raak! 3 raak, waarvan 1 perfect") en de speer verdwijnt.
- In de sandbox onder Speer en spullen: **Rol-worp: aan/uit** (`sbrolworp`).

## Maat per frame (`ROL.maat`, `ROL_WORP.maat`)

Grok liet Amir in de rolclip langzaam groeien, en de worp kwam er zo'n 12 procent groter uit dan de gewone sets.
Per frame staat nu een factor die zijn hoofd even groot maakt als in `idle_ns` (gemeten met template matching op het
hoofd; waar het hoofd ondersteboven of weg is, tussen de metingen in, en over vijf frames zacht gemaakt). De tekencode,
de uitval van de worp en de losplek van de speer rekenen ermee. Nieuwe frames: opnieuw meten.
