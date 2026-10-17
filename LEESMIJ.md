# Kooibandiet: stamp + vogel loslaten

Aanvulling op `kooibandiet_sprites.zip`. Zelfde canvas (728x648), zelfde groundline (598), zelfde kijkrichting (links, spiegel in code voor rechts). Alle frames zijn met dezelfde clean key gemaakt als de sleep-set, de kooi is ook hier donker en half transparant.

## Wat er gebeurt

1. De bandiet sleept (drag loop).
2. Hij heft zijn knie, stampt hard op de grond.
3. Op de stamp: kooislag-geluid, stofwolk, het spel bevriest.
4. Tijdens de freeze klapt het deurtje van achter de kooi omhoog open, de vogel vliegt eruit, het deurtje blijft 1,5 seconde open en slaat dan dicht.
5. Het spel gaat verder, de bandiet sleept weer verder.

## Sets (24 fps basis, ticks = aantal basisframes dat een frame blijft staan)

| set | frames | duur | wanneer |
|---|---|---|---|
| `stomp` | 13 | 16 ticks (0,67 s) | start alleen vanaf **drag frame 0** (stomp_00 sluit daar exact op aan) |
| `hatch` | 19 | 57 ticks (2,4 s) | direct na de stamp, speelt **tijdens de freeze** |
| `stomp_out` | 2 | 2 ticks | na de freeze, korte uitloop |
| `dust` | 12 | 18 ticks (0,75 s) | los effect, gespawnd op de stamp |

`stomp` frame 8 (knie omhoog) blijft 4 ticks staan. Dat is de tell voor de speler: als hij zijn knie heft, komt er een vogel.

## Events en volgorde

**Op `stomp` frame 12 (impact, laatste frame):**
- speel het kooislag-geluid af (hetzelfde geluid als bij de smash)
- spawn `dust` met `anchor_in_sprite` (280,206) op canvaspunt (343,598), dat is onder de stampende voet op de groundline
- **FREEZE**: zet de wereld stil (Amir, andere vijanden, projectielen, physics, timers, input)
- start `hatch`

**Tijdens de freeze lopen alleen door:** de `hatch` set van deze bandiet, de stofwolk, en de vogel die eruit komt.

**`hatch`:**
- frame 0: deurtje nog verstopt (2 ticks), daarna klapt het open en veert het even na
- frame 9: deurtje staat open, **36 ticks = 1,5 s**. Spawn hier de vogel (zie hieronder)
- frame 10 tot 18: deurtje slaat dicht, met een klein tikje terug, en is weer weg
- **UNFREEZE** aan het einde van frame 18, start `stomp_out`

**Na `stomp_out`:** ga terug naar `drag`, maar start op **drag frame 11** (niet 0) en schuif de bandiet **24 px naar voren** (x -24 als hij naar links kijkt, x +24 als hij naar rechts kijkt). Hij heeft tijdens de stamp een stapje gezet, zo loopt het naadloos door.

## Vogel

- spawn op `hatch` frame 9, op canvaspunt (592,464): net in het luikje
- vlieg weg in richting (0.488, -0.873), dat is schuin omhoog weg van de kooi (bij spiegelen de x omdraaien)
- laat hem uit de kooi groeien: schaal van ongeveer 0,12 naar zijn normale grootte in de eerste 0,35 s, gespiegeld (vogel kijkt standaard links, hij vliegt hier naar rechts weg)
- de vogel beweegt ook tijdens de freeze (hij hoort bij het moment); zijn AI (cirkelen, dive) start pas bij de unfreeze
- gebruik de `fly` set uit `vogel_sprites.zip`

## Bestanden

- `sprites.json`: alle sets, ticks, centroids en de events hierboven (ook als data)
- `stomp/`, `hatch/`, `stomp_out/`, `dust/`: de PNG's
- `stomp_chain_preview.gif`: de hele keten met stof en vogel, zoals het ingame moet ogen

## Bron

Clip `stapvooropen.mp4`, frames 1 tot 24. Frame 22 is het freezeframe (eerste frame met de voet op de grond). Het deurtje komt uit `deur_dicht.mp4` (frames 1 tot 19) en staat met de scharnieren precies op dezelfde rail van de kooi als goedgekeurd. Vanaf frame ~64 draait hij zich om in de clip, dat deel is niet gebruikt.
