# Savanne-rand voor de opstapjes: Grok-bronnen

Losse platen op wit, nog niet geknipt. Doel: het rechtereind van een trede met de grondrand
(`design/grondrand.png`), zodat zand en kap natuurlijk aflopen in plaats van recht afgesneden.

## Geleverd

- `savanne_rand_1.png` (2176x912, Grok-post d2415bbb): de beste. Zand en kap buigen samen af naar
  rechts, de kapbrokken worden kleiner, drie ronde keien in warm oranjebruin en een graspol op de hoek.
  Let op: het laagste puntje van het eind zakt ongeveer een kapdikte onder de onderrand van de kap
  (ca. 75 px op deze plaat, ca. 34 px op tegelmaat).
- `savanne_rand_2.png` (2176x912, Grok-post 7ea5bdc3): blijft netjes binnen de hoogte van zand plus
  kap, het zand zakt zacht af. Minder mooi: de kap brokkelt aan het eind nauwelijks af (loopt plat
  uit in een punt), de twee keien zijn hoekig en liggen bovenop het zand, de graspol is heel klein.
- `savanne_rand_start.png`: het startbeeld dat Grok kreeg (zie hieronder).

Schaal: Grok heeft het startbeeld (1000 breed) 2,176 keer vergroot en het linkerdeel overgenomen.
Terugschalen met 1000/2176 geeft de maat van `grondrand.png`. Links bovenin staan twee bleke grijze
graspollen: die komen uit `grondrand.png` zelf (half doorzichtig daar), niet van Grok.

Beide platen zijn via de browser binnengehaald (tegels op schermafdruk, aan elkaar geplakt), dus
jpeg-kwaliteit van Grok plus een jpeg-stap. De achtergrond is bijna egaal wit (251 tot 255).

## Prompts en afkeuringen

### Ronde 1 en 2: de prompt uit de opdracht

Startbeeld `design/grondrand.png` (op wit gezet, want het origineel is doorzichtig) plus
`design/drygrass.png` voor de graspol. Prompt woordelijk zoals in de opdracht.

- Ronde 1 (post 58dbaa7a): een plaat met vier varianten in een raster. Alle vier afgekeurd: de
  rotskolommen kwamen terug onder het zand (punt 3), de kap werd een dun randje erboven, en de keien
  waren veel te groot (punt 1). Twee varianten hadden ook twee graspollen.
- Ronde 2 (post e6336eba): een enkele strook. Afgekeurd: weer kolommen onder de kap (punt 3), en de
  steentjes in het zand werden kleiner dan in de tegel (punt 1).

### Wat ik veranderd heb

Grok tekende de kolommen terug omdat ze in het startbeeld staan. Daarom een eigen startbeeld:
de eerste 600 px van `grondrand.png`, alleen zand plus kap, met een grillige onderrand langs de
kieren onder de kapbrokken (y 168 tot 181), op een wit doek van 1000x420 met rechts leeg wit. Zo
staat de schaal al vast en hoeft Grok alleen het eind erbij te tekenen. In de prompt meer woorden
voor wat er NIET mag (geen kolommen, geen verticale rotsplaten, geen klifwand, geen stenen muur,
geen tweede laag), keien "zo groot als de kleine kapbrokken, oranjebruin, niet grijs", en de
graspol alleen in de stijl van de bladen (de referentie heeft grijze stenen eronder).

### Ronde 3 tot 5: de aangepaste prompt

```
Edit the first reference image. It shows a short piece of savanna ground edge: a flat sandy
walking surface seen slightly from above, with one thin row of cracked reddish-brown crust chunks
directly under it, on a white background. Keep this existing piece exactly as it is: same pixels,
same size, same scale, same colours, same line work, same thin crust band. Do not redraw it, do not
enlarge it, do not move it. Only draw in the empty white space to the right of it. On the right
end, continue the ground edge for a short distance and let it end naturally: the crust chunks get
smaller and crumble down in a short rounded slope, the sand surface curves down with them, and two
or three small half-buried round sandstone boulders (the same size as the small chunks in the
crust, warm orange-brown, not grey) and one small dry grass tuft sit at that corner. The grass tuft
only takes the blade style of the second reference, not its grey stones. The whole end stays within
the height of the sand plus the crust band: nothing hangs lower than the bottom of the crust. The
left end stays cut off straight and vertical. Nothing below the crust: no rock columns, no vertical
rock slabs, no cliff face, no stone wall, no second layer, no dirt underneath, no ground line. Pure
flat white background #FFFFFF everywhere else, no gradient, no shadow on the background. No scenery,
no sky, no tree, no bush, no big rock. Clean game-asset sprite, strict side view, no tilt.
```

Referenties: `savanne_rand_start.png` en `design/drygrass.png` (op wit).

- Ronde 3 (post 37e1435a): afgekeurd. Geen kolommen meer en de kleur klopt, maar het eind is een
  hoek die de diepte in draait (een tafelhoek, punt 6) in plaats van een afbrokkelende helling, en
  twee hoekige keien liggen bovenop het zand, groter dan de kapbrokken (punt 1).
- Ronde 4 (post d2415bbb): goedgekeurd, wordt `savanne_rand_1.png`.
- Ronde 5 (post 7ea5bdc3): goedgekeurd als tweede keus, wordt `savanne_rand_2.png`.

Grok gaf met dit startbeeld per keer een plaat, geen vier varianten.
