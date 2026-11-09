# De kit van Amir verbeteren: takenlijst

Een beoordeling van de basiskit van Amir (wat hij kan zonder tribe), met per onderdeel een cijfer
en de taken om het naar ongeveer een 9 te krijgen. Gemaakt op 9 november 2026, met stof in de ogen
(X, `STOF`) gerekend als vast onderdeel van de basis. Ideeën die nog los rondzweven staan in
`notities/kit-ideeen.md`.

## Zo werken we (lees dit eerst)

Vraagt de opdrachtgever om de **kit-lijst** ("verbeter Amir kit", "kit-lijst", "laat de kit-taken zien"),
dan gaat het zo:

1. **Laat de lijst zien.** Geef de open taken kort, per onderdeel, met hun code (bijvoorbeeld `G1`) en
   de punten die ze opleveren. Bouw nog niets.
2. **De opdrachtgever kiest er een.** Zeg in een zin wat je oppakt, lees de notitie die erbij hoort
   (regel 11) en bouw het eerst in de sandbox (regel 2).
3. **Bijsturen tot het goed is.** Pas als de opdrachtgever zegt dat het goed is, is de taak klaar.
4. **Afstrepen.** Zet het vinkje (`[x]`), schrijf erachter wat er gebouwd is en welke pull request, en
   werk het cijfer van het onderdeel bij in "Stand". Commit dat mee.

Altijd geldig: de regels uit `CLAUDE.md` (echte episodes niet aanraken, sandbox eerst, geen testlevel
of baas zonder toestemming, aansluiten op wat er is). Een taak per keer, liefst in een eigen, korte chat
(regel 10).

## Wat stof in de ogen doet aan de basis

- Een antwoord op een vijand die Amir aankijkt: verblinden, dan een dubbele treffer (een bandiet met
  twee levens in een klap dood). Het vult het gat tussen sneak en het open gevecht.
- Werkt tegen alles uit De Gouden Poort; de afkoeling van 8 s maakt het een keuze per gevecht.
- Risico's: de aanloop van 0,58 s (een stormer is er al), een gegarandeerde kill elke 8 s kan een
  1-op-1 te makkelijk maken, en het is weer een knop erbij.

## Stand

| onderdeel | cijfer | doel |
| --- | --- | --- |
| Melee (steek, lage zwaai) | 6,5 | 9 |
| Werpen en ophalen | 7,5 | 9 |
| Beweging (rol, renstoot, sprong) | 7 | 9 |
| Groepsgevecht en controle | 6,5 (zonder stof 5) | 9 |
| Sneak | 6,5 | 9 |
| Gevoel en feedback | 7 | 9 |
| Leerbaarheid | 5,5 | 9 |
| **gemiddeld** | **6,6** | **9** |

## Taken

### Melee (M)

- [ ] **M1** Derde slag na twee steken: een duw die de vijand terugzet, met een timingvenster. **+1**
- [ ] **M2** Neerhalende sweep: de lage zwaai legt een vijand op de grond, daarna een steek naar beneden. **+1**
- [ ] **M3** Spin strike op een verblinde vijand, raakt ook achter Amir. **+0,5**

### Werpen en ophalen (W)

- [ ] **W1** Een speer uit de grond plukken vanuit een sprint, zonder te stoppen. **+0,5**
- [ ] **W2** Een hoeklijntje bij de schaalworp, alleen zolang je vasthoudt. **+0,5**
- [ ] **W3** Even slow motion bij de worp die de laatste vijand doodt. **+0,5**
- [ ] **W4** Doorvliegen: een worp die een vijand doodt vliegt door hem heen, met bloed en een eigen geluid,
  en raakt wie erachter staat of landt verderop in de grond. Basis: elke dodelijke worp. Het idee in
  `notities/kit-ideeen.md` (doorboren) bouwt op `krbSpeerVolg`; let op `javRaakt`/`jav.hit` (een worp raakt nu
  maar een vijand). Als talent erbovenop: een crit raakt de tweede ook met een crit. **+1**
- [ ] **W5** De dubbele worp: vlak na het loslaten (rond 0,3 s) F nog eens, en Amir grijpt over zijn schouder
  en gooit meteen een tweede, vlak en snel. Vraagt een speer op de rug (`RUG`, `rugTrekKlaar`). Voorstel: de
  tribe-ability van Mkuki (zie `notities/kit-ideeen.md`), niet de basis, zodat Mkuki zijn eigen gezicht houdt.
  Eerste versie met de gewone worp versneld, echte frames later. **+1** (voor wie Mkuki speelt)

### Beweging (B)

- [ ] **B1** Plunge: van een kei of rand springen met een steek naar beneden. **+1**
- [ ] **B2** Een steek afbreken met een rol (rol-cancel). **+0,5**
- [ ] **B3** Stof meteen uit de hurk na een rol. **+0,5**

### Groepsgevecht en controle (G)

- [ ] **G1** De aanloop van stof inkorten naar ongeveer 0,4 s, of stof vanuit de rol, zodat het ook tegen een stormer werkt. **+1**
- [ ] **G2** Een verblinde bandiet slaat in paniek om zich heen en kan een maat raken (`vriendVuur`). **+1**
- [ ] **G3** De bandiet draait mee als je erdoorheen rent (zie `notities/kit-ideeen.md`). **+0,5**

### Sneak (S)

- [ ] **S1** Een steentje of de speer gooien als afleiding (`lawaaiPuls`). **+1**
- [ ] **S2** Na een sluipkill een kort venster voor een tweede. **+1**
- [ ] **S3** Hoog gras of schaduw om in weg te zakken. **+0,5**

### Gevoel en feedback (F)

- [ ] **F1** Hitstop en een tikje schok op elke treffer, niet alleen op een crit. **+0,5**
- [ ] **F2** Een korte kreet van Amir bij stof of een dubbele treffer. **+0,5**
- [ ] **F3** Killcam bij de laatste vijand van een golf. **+1**

### Leerbaarheid (L)

- [ ] **L1** Stof op de knop van de lage zwaai: tikken is zwaaien, vasthouden is stof. Scheelt een knop. **+1,5**
- [ ] **L2** Een oefenkamer per vaardigheid met een kleine uitdaging (nieuw testlevel: eerst toestemming, regel 3). **+1**
- [ ] **L3** Een icoontje boven een vijand zolang een treffer dubbel telt. **+1**

## Grootste winst eerst

G1, L1 en M2. Voor de worp: W4.
