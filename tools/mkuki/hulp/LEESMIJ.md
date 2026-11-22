# Hulpscripts voor een frame (uit de chat van 21/22-11)
Kopieer ze naar /home/claude/ (de scripts verwijzen naar die plek) en zet de werkmap /home/claude/werk/<set>/ op met
`paar.py bouw` (zie OVERDRACHT.md).
- `doe2.sh SET N postid fileid`: tegel ophalen uit de zoom-screenshot, terugzetten (IoU), vergelijkbeeld /tmp/vgl.png.
- `stap.sh SET N postid fileid origpad`: doe2 + klaar1 (--eiland --geenhoofd) + /tmp/spel.png (origineel naast Mkuki).
- `spel.py <naamstuk> <origpad>`: origineel en afgewerkt lijf naast elkaar.
- `handplaats.py werkmap/sN schaal dx dy`: Grok-figuur met de hand plaatsen als het IoU-zoeken hem verkeerd zet.
