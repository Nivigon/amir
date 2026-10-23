# Prompt: CLAUDE.md inkorten tot reglement plus wegwijzer

Kopieer alles onder de streep in een verse chat.

---

Kort `CLAUDE.md` in van 219 KB naar 25 tot 30 KB, door de feature-uitleg te verhuizen naar `notities/`. Niets mag verloren gaan: dit is knippen en plakken, geen herschrijven. Werk op een `claude/`-branch, commit in het Nederlands, geen em-dashes, en maak aan het eind een pull request met als titel "CLAUDE.md: regels en wegwijzer, de uitleg naar notities".

## Uitgangssituatie (gemeten)

- `CLAUDE.md` is 219 KB en 1591 regels. De sectie Regels is 7 KB, de tabel "Waar wat staat" 101 KB, de `###`-secties onder "Een level lezen of schrijven" samen 80 KB, de tool-secties 10 KB.
- Vijf tabelcellen zijn samen 50 KB: rijzende grond (regel 154, 3,5 KB), takelwiel (155, 9 KB), de bandiet (179, 13 KB), de bandiet-arena (180, 6 KB), de baviaan (181, 18 KB).
- `notities/` bestaat al, met `combinaties.md` en `zegeltekens.md`. Sluit daarop aan, maak geen tweede map.

## De toets

Een stuk tekst blijft in `CLAUDE.md` als het een van deze drie is:
1. een regel die voor het hele project geldt;
2. een wegwijzer: welke naam, welk bestand;
3. een commando dat je draait, met wat FOUT en LET OP betekenen.

Alles wat uitlegt hoe iets van binnen werkt, waarom een getal zo gekozen is, wat er gemeten is, of welke sandbox-knop erbij hoort, is een notitie. Meetgeschiedenis ("gemeten: 141 px", "eerst viel hij pas bij frame 32") gaat mee naar de notitie en wordt niet geschrapt.

## Stap 1: knippen met een script, niet met de hand

Schrijf een klein Python-script in `tools/` (of eenmalig in de scratchpad) dat:
- elke `###`-sectie onder "Een level lezen of schrijven" naar een eigen bestand `notities/<onderwerp>.md` schrijft, met de kop als titel;
- elke tabelcel uit "Waar wat staat" die groter is dan 1,5 KB naar `notities/<onderwerp>.md` schrijft; cellen die bij elkaar horen mogen in één bestand (bandiet en bandiet-arena samen in `bandiet.md`, speerbeet en speer-in-de-baviaan bij `baviaan.md`, de drie geluidsstukken bij `geluid.md`);
- de tekst letterlijk overneemt.

Bestandsnamen in kleine letters, Nederlands, zonder spaties: `baviaan.md`, `bandiet.md`, `takelwiel.md`, `rijzende-grond.md`, `muur.md`, `runes.md`, `lichtkaart.md`, `ravijn.md`, `rotsraster.md`, `plafond.md`, `schacht.md`, `skelet.md`, `gang.md`, `savannelaag.md`, `weer.md`, `geluid.md`, enzovoort.

## Stap 2: de nieuwe CLAUDE.md

Houd, vrijwel ongewijzigd:
- de kop en de tien regels;
- "Een level toevoegen", "Een episode toevoegen", "Een vijand of prop toevoegen", "Testen en afronden";
- per tool (`levelcheck.py`, `speelrobot.js`, `runecheck.js`, `beeldgelijk.js`, `bouwertest.js`) alleen de aanroepregels en de betekenis van FOUT en LET OP;
- de sectie Assets alleen als lijst van welk script je na welke wijziging draait.

Maak van "Waar wat staat" een index: per onderwerp één regel met de kop, drie tot vijf namen waarop je grept, en het notitiebestand. Voorbeeld:

```
| baviaan | `BAVIAAN`, `bavStand`, `bavVecht`, `BAV_HAP`, `bavKlok` | notities/baviaan.md |
```

Maak van de veldentabel van een level per veld één regel: naam, wat het is in een halve zin, en het notitiebestand als er uitleg is.

Voeg onder Regels één regel toe, als nummer 11: "Raak je een onderwerp uit de index aan, lees dan eerst zijn notitie. Is het breed, laat een subagent die lezen en alleen de conclusie teruggeven (regel 10)."

## Stap 3: nameten

- Tel de bytes: oude `CLAUDE.md` moet ongeveer gelijk zijn aan nieuwe `CLAUDE.md` plus alles wat er in `notities/` bij kwam, min de tabelregels die tot een indexregel zijn ingekort. Meld het verschil en verklaar het.
- Grep een stuk of tien kenmerkende zinnen uit de oude tekst (bijvoorbeeld "1,35 keer de schaal van de grondrand", "BAN_VAULT_ZELF", "interrupted is niet suspended") en laat zien dat ze in een notitie terug te vinden zijn.
- Draai `python3 tools/levelcheck.py` als rookproef; die hoort onveranderd 0 FOUT te geven.
- `README.md` blijft ongemoeid: dat is de spelershandleiding.

## Wat niet

- Geen tweede ronde waarin je de notities zelf inkort of herschrijft; dat is een aparte opdracht.
- Geen wijzigingen aan de HTML.
- Geen samenvattingen in plaats van de originele tekst.

Leg aan het eind in een paar regels uit welke onderwerpen naar welk bestand zijn gegaan, en wat de nieuwe CLAUDE.md weegt in KB.
