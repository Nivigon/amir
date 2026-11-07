# De stad verbeteren: werklijst

Een beoordeling van de stadsomgeving (art en speelstijl), los van de levels, met per categorie
een cijfer en de stappen om het op te krikken. Deze lijst werk je stap voor stap af, elke stap
liefst in een eigen, korte chat (regel 10).

Gemaakt op 7 november 2026, uit de platen in `design/stad/` en drie sandbox-scènes (Stad,
Plein met luifel, Knooppunt met poort). De levels zijn bewust niet meegewogen.

## Zo werken we (lees dit eerst)

Vraagt de opdrachtgever om een **stadsverbetering** ("volgende stadsverbetering", "stadsverbetering
punt L1", "verbeter de stad"), dan gaat het zo:

1. **Kies de stap.** Noemt de vraag een punt (bijvoorbeeld `L1`), dan is het dat. Anders neem je het
   eerste open punt uit "Volgorde" onderaan. Zeg in een zin welk punt je oppakt.
2. **Kijk eerst.** Lees de notitie die bij het onderwerp hoort (meestal `notities/stad.md`) en
   bekijk de stad zoals hij nu is: de platen in `design/stad/` en een schermafdruk uit de sandbox
   (knoppen Stad, Plein, Knooppunt; regel 2). Nooit uit een echt episodelevel (regel 1).
3. **Geef precies 3 suggesties** voor die ene stap. Per suggestie:
   - wat er verandert, in een of twee zinnen;
   - hoe het eruit komt te zien of hoe het speelt;
   - wat het vraagt: alleen code, of ook nieuwe art (Grok-platen, met welke skill);
   - het verwachte cijfer voor de categorie.
   Maak de drie echt verschillend (bijvoorbeeld licht, middel en groot), niet drie keer hetzelfde.
   **Bouw nog niets.**
4. **De opdrachtgever kiest er een.** Dan bouw je die, in de sandbox te bekijken, en laat je een
   schermafdruk zien.
5. **Bijsturen tot het goed is.** Zegt de opdrachtgever dat het nog niet goed is, dan pas je aan
   (of geef je weer 3 kleine varianten als de richting niet duidelijk is). Pas als de opdrachtgever
   zegt dat het goed is, is de stap klaar.
6. **Afvinken.** Zet het vinkje bij die stap (`[x]`), schrijf erachter wat er gekozen is en welke
   pull request, en pas het cijfer van de categorie aan in "Stand". Commit dat mee.

Altijd geldig:

- De regels uit `CLAUDE.md` blijven staan: echte episodes niet aanraken (regel 1), nieuw werk eerst
  in de sandbox (regel 2), geen nieuw testlevel zonder toestemming (regel 3), aansluiten op wat er
  is (`STAD`, `stadTeken`, `stadAchter`, `VILLAGE`, de kramen, de tonnen; regel 4), geen baas
  zonder toestemming (regel 12).
- Een stap die nieuwe art nodig heeft: lever eerst de Grok-prompt (skill `grok-environment-asset`
  voor decor, `grok-imagine-prompts` voor personages) en bouw verder als de plaat er is.
- Een nieuw stadsplaatje komt in `design/stad/`, daarna `tools/gen-klein.py` en
  `tools/gen-offline-manifest.py` (zie Assets in `CLAUDE.md`).
- Een stap per keer. Raakt een stap een andere stap, zeg dat, maar vink alleen af wat af is.

## Stand

| categorie | nu | doel met beide stappen |
| --- | --- | --- |
| Sfeer en stijl | 8 | 9 |
| Detail en variatie | 6 | 8,5 |
| Licht en diepte | 6 | 8,5 |
| Leven in de straat | 4 | 7,5 |
| Speelruimte en verticaliteit | 7 | 9 |
| Stadseigen gevechten | 6 | 8,5 |
| **Totaal** | **7** | **ongeveer 8,5** |

Een 10 haal je pas als de art en het spelen samen één geheel worden. Een voorbeeld: de menigte
vlucht een overdekte soek in, en daar vecht je in de strepen zonlicht.

## De stappen per categorie

Achter elke stap staat welk cijfer de categorie haalt met alleen die stap.

### Sfeer en stijl (S): nu 8

Sterk: de Sahel-leembouw met uitstekende balken, regensporen en kale baksteenplekken klopt overal.
Het paleis is van elke plek in de straat te zien en wijst je zo de weg.

- [ ] **S1. Het paleis verweren.** Het paleis is strak, verzadigd en schoon, terwijl de voorgrond
  verweerd en geschilderd is. Geef het stof, verwering en minder felle kleuren, dan hoort het er
  echt bij. Naar **8,5**.
- [ ] **S2. De galerij warmer.** De galerij is koud grijs hout tussen warme leem. Een warmere,
  roodbruine houttint trekt hem in het palet. Naar **8,5**.

Beide samen: **9**.

### Detail en variatie (D): nu 6

Elke gevel is dezelfde plaat met dezelfde luiken op dezelfde plek. Na drie huizen zie je dat.

- [ ] **D1. Gevelvarianten.** 3 tot 4 varianten per gevel: andere raamplekken, een ronde hoektoren,
  een dichtgemetseld raam, en twee of drie leemkleuren (oker, roze leem, bijna wit). Naar **7,5**.
- [ ] **D2. Losse stukken op de gevel.** Een lap stof uit een raam, een kapotte luifel, een nis met
  een kruik. Dan wordt elk huis anders zonder nieuwe gevelplaten. Naar **7**.

Beide samen: **8,5**.

### Licht en diepte (L): nu 6

Vol middaglicht zonder schaduwen: de galerij en de kramen werpen niets op de straat. De lucht is
één egaal blauw.

- [ ] **L1. Slagschaduwen op de straat.** Schuine schaduwen van de huizen, de galerij en de kramen
  over de straat. Dat geeft meteen hitte en diepte. Naar **7,5**.
- [ ] **L2. Lucht met stofwaas.** Een verloop in de lucht met lichte stofwaas onderin, zodat de
  verre huizen er echt in wegvallen in plaats van alleen bleker te worden. Naar **7**.

Beide samen: **8,5**.

### Leven in de straat (V): nu 4

Het zwakste punt. Prachtige kramen, maar geen koopman, geen dier, geen rook. Het voelt als een
verlaten stad.

- [ ] **V1. Figuren op de achtergrond.** Silhouetten of half doorzichtige figuren die niet meedoen
  met het gevecht: een koopman achter de kraam, een vrouw met een kruik op het hoofd. Naar **6**.
- [ ] **V2. Kleine beweging.** Wapperende doeken aan de kraam, rook uit een dakgat, duiven die
  opvliegen als je langsloopt. Naar **5,5**.

Beide samen: **7,5**.

### Speelruimte en verticaliteit (H): nu 7

Galerijen, daken, de lift, deuren waar vijanden uitkomen en de luifel die terugwerpt zijn goede,
stadseigen ideeën.

- [ ] **H1. De trap zonder fade.** De trap met E en een zwarte fade haalt je uit de flow. Laat Amir
  de trap echt oplopen, of maak hem korter, zonder fade. Naar **8**.
- [ ] **H2. Een route bovenlangs.** Dakranden en galerijen meer met elkaar verbinden (springen van
  dak naar galerij), zodat er naast de straat een route bovenlangs ontstaat. Naar **8**.

Beide samen: **9**.

### Stadseigen gevechten (G): nu 6

De tonnen en de luifel zijn goed, maar verder vecht je zoals op de savanne, alleen tegen een ander
decor.

- [ ] **G1. Vijanden van boven.** Een kruisboogbandiet op een dak, of iemand die een kruik naar
  beneden gooit. Naar **7**.
- [ ] **G2. De omgeving doet mee.** Een kraam die instort als je er een vijand tegenaan slaat, of
  een doek dat je los kunt steken. Naar **7,5**.

Beide samen: **8,5**.

## Nieuwe dingen

### Art (A)

- [ ] **A1. Een overdekte steeg of soek.** Een stuk straat onder rieten matten of doeken, met
  strepen zonlicht op de grond. Een donker en licht ritme, heel anders dan de open straat.
  Licht van 6 naar **7,5**, Variatie van 6 naar **7**.
- [ ] **A2. Moskee en groen in de verte.** Een moskee met houten balken in Djenné-stijl en een paar
  palmen of een acacia op een binnenplaats. Groen breekt het eindeloze oker. Sfeer van 8 naar
  **8,5**, Variatie van 6 naar **6,5**.

### Speelelementen (P)

- [ ] **P1. Waslijnen en doeken tussen de huizen.** Je kunt erop springen (ze veren), of ze met de
  speer doorsteken zodat het doek op een vijand valt en hem even vasthoudt. Verticaliteit van 7
  naar **7,5**, Gevechten van 6 naar **7**.
- [ ] **P2. Een menigte op de markt.** Burgers die wegvluchten als er gevochten wordt. Je speer mag
  hen niet raken, en vijanden kunnen zich tussen hen verstoppen. Zo krijgt de stad een eigen
  spanning die de savanne niet heeft. Leven van 4 naar **6,5**, Gevechten van 6 naar **7**.

## Volgorde

De aanbevolen volgorde: eerst wat het meest oplevert per stuk werk. Het eerste open punt is de
volgende stadsverbetering.

1. [ ] L1, slagschaduwen op de straat (veel effect, weinig art)
2. [ ] V1, figuren op de achtergrond (het zwakste punt)
3. [ ] D1, gevelvarianten (de herhaling weg)
4. [ ] S2, de galerij warmer
5. [ ] L2, lucht met stofwaas
6. [ ] H1, de trap zonder fade
7. [ ] V2, kleine beweging
8. [ ] D2, losse stukken op de gevel
9. [ ] S1, het paleis verweren
10. [ ] G2, de omgeving doet mee
11. [ ] G1, vijanden van boven
12. [ ] H2, een route bovenlangs
13. [ ] A1, de overdekte soek
14. [ ] A2, moskee en groen in de verte
15. [ ] P1, waslijnen en doeken
16. [ ] P2, de menigte op de markt

## Gedaan

Per afgeronde stap een regel: het punt, wat er gekozen is, de pull request en het nieuwe cijfer.

(nog niets)
