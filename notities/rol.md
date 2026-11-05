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
