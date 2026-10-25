# Rotsdecor (Amir, King of Africa)

Losse decorstukken in cliffstijl, transparante PNG's, achtergrond weggeknipt
(magenta of wit) en per stuk bijgesneden. Stilstaand decor, geen animatie.

Doel: veel van dit soort stukken tegen de cliffs zetten, zodat een plaat die
een doorgang afdekt niet opvalt.

## Wat zit erin

```
zuil_01..03.png      hoge smalle zuilen (sheet 1)
plaat_01..03.png     brede platen: gelaagd, verticaal gespleten, diagonale breuk
                     (de afdekkers voor doorgangen)
laag_01..03.png      lage brokken: richel, scheef blok, bult
brok_01..07.png      gemengde brokken, laatste (brok_07) is een puinhoopje
kei_01..08.png       ronde keien, van groot naar klein
hangrots_01..03.png  hangende rotsen voor plafonds/overhang; bovenkant loopt
                     door tot de rand (laten aansluiten op het plafond),
                     hangrots_03 heeft een wortel onderaan
```

## Plaatsen

- De onderkant van zuil, plaat, laag, brok en kei staat onderaan het canvas:
  zet die op de grondlijn.
- Hangrots: bovenkant tegen het plafond.
- Schaal binnen een groep is onderling gelijk (zelfde sheet). Tussen groepen
  verschilt de schaal; afstemmen in de level maker.
- Spiegelen en iets schalen geeft extra variatie.

## Opnieuw maken

De aangeleverde platen staan in `bron/` (kei, brok en hangrots op magenta, laag, plaat
en zuil op wit). Na een nieuwe of vervangen plaat:

```
python3 tools/rotsdecor_knip.py
python3 tools/gen-offline-manifest.py
```

Nog niet in het spel: geen `PROPS`-regel, niet in de Maker of de sandbox.
