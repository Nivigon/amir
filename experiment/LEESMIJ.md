# Renderproef: 2D-canvas versus GPU

Een los prestatiebewijs, buiten het spel. Het tekent dezelfde zware scene (parallax-bergen,
een herhaalde grondtegel, honderden buigende grasbosjes uit het echte spritesheet, en een
paar full-screen lichtlagen) op twee manieren:

- **2D-canvas**: zoals het spel het nu doet.
- **GPU (PixiJS)**: via de grafische kaart.

Zo zie je, met je eigen plaatjes, wat de overstap naar de GPU oplevert voordat we iets aan
de echte spelcode veranderen.

## Draaien

Start vanuit de hoofdmap van het spel een webserver en open de pagina:

```
python3 -m http.server
```

Ga daarna naar <http://localhost:8000/experiment/renderproef.html>.

## Wat je ziet en doet

- Wissel met de twee knoppen tussen **2D-canvas** en **GPU (PixiJS)**.
- Let op **JS per beeld** in het leesvenster: dat is hoeveel werk de processor per beeld
  kwijt is. Lager is beter, en het is de marge die bepaalt of het soepel blijft.
- Zet **Grasbosjes** en **Lichtlagen** hoger om de scene zwaarder te maken, tot de
  2D-kant begint te zakken. De GPU-kant hoort veel langer vloeiend te blijven.
- **Scherpte (DPR)** bootst een scherp laptopscherm na: op 2 tekent hij vier keer zoveel
  pixels als op 1. Juist daar laat de 2D-kant het eerst afweten.
- Met **Meet beide, 6 seconden elk** krijg je harde cijfers naast elkaar.

## Let op

Draai dit op een echte laptop, niet in een omgeving zonder grafische kaart. Zonder GPU valt
de browser terug op trage software-rendering, en dan lijkt de GPU-kant juist langzamer. Op
een gewone laptop met beeldkaart klopt de meting wel.

De GPU-bundel staat als losse kopie in `lib/pixi.min.mjs`, dus de proef werkt zonder
internet en zonder `npm install`. Wil je PixiJS bijwerken: `npm install` in deze map en
`cp node_modules/pixi.js/dist/pixi.min.mjs lib/`.
