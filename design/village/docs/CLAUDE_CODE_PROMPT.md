# Prompt voor Claude Code

Plak alles hieronder in Claude Code.

---

In de hoofdmap van dit project staat een uitgepakte map `village-assets/`. Die bevat
dorpsdecor voor het spel. Doe het volgende.

**1. Bestanden verplaatsen**

Verplaats `village-assets/village/` naar `design/village/`, inclusief de submap
`foreground/`. Verplaats `village-assets/metadata.json` naar
`design/village/metadata.json`. Laat README.md en preview_testplaatsing.png weg, of
zet ze in `design/village/docs/`. Verwijder daarna de lege map `village-assets/`.

**2. Decorregister toevoegen**

Zoek in het HTML-bestand op waar bestaande decor- en vegetatie-afbeeldingen uit
`design/` geladen worden en sluit daarop aan. Voeg geen nieuw laadsysteem toe als er
al een is. Maak een register met per asset: id, pad, `heightInPlayerHeights`,
`mirrorSafe` en `layer`. Neem de waarden over uit metadata.json, hardcoded in het
HTML-bestand is prima, dit is één bestand zonder buildstap.

**3. Tekenfunctie**

Maak één functie die een decorobject plaatst, met deze regels.

- Ankerpunt midden onder. Hoogte = gerenderde hoogte van Amir maal
  `heightInPlayerHeights`. Breedte volgt uit de beeldverhouding van de PNG.
- Teken het object 3 procent van zijn hoogte onder de grondlijn, zodat de rand van de
  zandplek in de grond wegvalt.
- Optionele parameter `flip`. Weiger die stil, of log een waarschuwing, als
  `mirrorSafe` false is.
- Optionele parameter `depth` tussen 0 en 1 voor objecten verder weg. Bij een hogere
  depth: schaal omlaag, en leg een overlay over het object in de kleur van de
  achtergrondnevel van het spel (het paarsblauw van de verre bergen) met een alpha die
  meeloopt met depth, maximaal ongeveer 0.45. Gebruik daarvoor een offscreen canvas met
  `globalCompositeOperation = 'source-atop'`, zodat alleen de ondoorzichtige pixels
  getint worden en niet de hele rechthoek.
- Objecten met een hogere depth worden eerder getekend, zodat ze achter de rest komen.
  Sorteer de decorlijst op depth aflopend voor het tekenen.

**4. Voorgrondlaag met doorkijk**

`hut_round_back_closeup` heeft `layer: "foreground"`. Die wordt getekend na Amir en na
de vijanden. Als de horizontale positie van Amir binnen de breedte van dit object valt,
laat de alpha van het object dan soepel zakken naar 0.35 in ongeveer 180 ms, en weer
terug naar 1.0 als hij eruit loopt. Gebruik een vloeiende interpolatie per frame, geen
harde omslag. De hitbox en de botsingslogica van Amir veranderen hier niet door, dit is
puur visueel.

**5. Levelbeschrijving**

Zorg dat decor in de leveldata beschreven kan worden als een lijst objecten met id, x,
`flip` en `depth`. Zet als voorbeeld een klein dorpje in het huidige testlevel: een
waterput, twee ronde hutten waarvan één gespiegeld, een kookafdak, en twee hutten met
een hoge depth ver op de achtergrond.

**6. Controle**

Start het spel en controleer dat de nieuwe ronde hut even hoog is als de hut die er nu
al staat, dat er geen roze randen zichtbaar zijn, en dat de voorgrondhut vervaagt als
Amir er achterlangs loopt. Rapporteer wat je hebt aangepast en waar.
