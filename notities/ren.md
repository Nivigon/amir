# De ren van Amir

## Stand

De nieuwe ren is de standaard in elk level en in de sandbox (`REN_NIEUW`, `renNieuwZet`, `renSprintZet`).
De oude ren zit er nog in: een level met `nieuweRen: false` rent de oude, en in de sandbox zet de knop
**Nieuwe ren** hem uit. Test 75 (New run) is het proefveld.

- **Zonder speer** (`karakters/amir/beweging/run/nieuw/ren_ns_1..12.png`): de Grok-ren "test4", gemaakt vanaf het
  basismodel (amir.png, image-to-image en daarna image-to-video "running in place, like on a treadmill"), met het
  gewone gezicht en minder voorover. Contour 0,6 eromheen zodat de rand bij de rest past.
- **Met speer** (`ren_sp_1..12.png`): een composiet. Lijf en benen van de nieuwe ren, de speerarm en de rechtopstaande
  speer uit de oude speer-ren (`run_sp`), geplakt op de tailleband, het doek achter het hoofd en de schacht onder de
  hand achter de benen (hij houdt hem rechts vast).
- **Tempo**: de lus volgt de snelheid (`tempo * fpsEl/12 * v/(pas*nowScale())`, `tempo` 1,5, `pas` 50), en elk frame
  heeft een eigen duur (`REN_NIEUW.duur`) omdat de pas van Grok ongelijk was (dat gaf een hapering in de benen).
- **Stokken** (Test 74): de guard-ren is een eigen set (`karakters/amir/stokken/rennen/`), zie `notities/stokken.md`.
  `stokBeeld` legt de 12 frames op de looplus; met de oude ren (8 frames) wordt hij uitgesmeerd.

## Om op terug te komen

- **De oude ren opruimen.** Is de nieuwe ren een tijd goed bevallen, haal dan de oude weg: `REN_NIEUW.oud`, de
  sandboxknop `sbrennieuw`, het veld `nieuweRen` en de oude frames in `beweging/run/` (en `klein/`, en het manifest).
  Kijk eerst of iets anders de oude frames nog gebruikt (multiplayer tekent de andere Amir met dezelfde sets).
- **De lijnen.** De Grok-frames zijn iets zachter dan het basismodel, ook met de contour. Valt het spelers op,
  dan kan een scherper startbeeld of een sterkere contour.
- **De speerarm is geplakt.** Bij een nieuwe ren met speer (of een andere wapenset) liever een echte pose dan weer een
  composiet; Grok houdt geen voorwerp vast in een rennende hand, dus dat blijft knip- en plakwerk.
- **Tempo en duur** zijn op het oog afgesteld (`tempo`, `pas`, `duur`); bij een andere loopsnelheid opnieuw kijken.

## Scripts (buiten de repo, in de sessie)

`bouw2.py` en `speer2.py` (de test4-ren), `arm2.py` (de speerarm-composiet: SH 2, dx -12, dy +5). De Animeer tool
"Amir ren speer" staat in het project (`claude/animeer_tool_amir_ren.md`).
