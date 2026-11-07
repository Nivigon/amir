# Wapenrek: een houten rek in de stad met speren om te pakken

Code: de sectie `// ---- wapenrek: een houten rek in de stad met speren om te pakken ----` (`WAPENREK`, `wapenrekken`,
`rekLaad`, `rekMaak`, `rekReset`, `rekBij`, `rekTrek`, `rekUpdate`, `rekTeken`, `rekETeken`). Plaat in
`design/stad/wapenrek/`.

## In een level

`wapenrekken: [{x, f, n}]`: `n` speren (standaard en hooguit 4, `WAPENREK.n` en `max`: een per touwlus; per level te
kiezen, 0 is een leeg rek), `f` spiegelt. In plaats van `x` kan het,
net als een ton, bij een put, luifel of kraam staan (`put`, `luifel` of `kraam` met `a`, zie `tonPlekX` en `notities/tonnen.md`).
Geen bestaand level heeft er een.

## Gedrag

- Decor: Amir en vijanden lopen erdoorheen. Getekend achter Amir, na de tonnen, met een schaduwtje en in de stad de slagschaduw.
- **E** ervoor (`rekTrek`, in `toggleSpear` na het skelet en de losse speer): met lege handen gaat er een speer in je hand
  (je eigen speer ergens in de wereld wordt een losse speer, `eigenSpeerNeer`, zoals bij `losTrek`); met je hand vol gaat hij
  op de rug als daar plek is (`rugErbij`); zijn die allebei vol, dan wiebelt het rek en klinkt `dontneedthis`.
- De gepakte speer glijdt nog even omhoog uit het rek en vervaagt (`WAPENREK.uit`). Een leeg rek blijft staan, zonder E.
- Na een dood staat het rek weer vol (`rekReset` in `restart`).
- De speren hebben het rode lint, niet het blauwe vaantje van het skelet.

## Het plaatje

`design/stad/wapenrek/wapenrek.png` is het **lege** rek (twee palen, twee balken, vier touwlussen op de bovenste), uit de
Grok-plaat `bron/wapenrek_grok.webp` (vier varianten op wit; het rek linksboven), door `tools/wapenrek_knip.py`. Grok gaf
de achtergrond al doorzichtig, maar met witte randpixels; het script geeft die de kleur van het hout ernaast. Het schrijft
ook `wapenrek.json` met de maten (de lussen, de balken, de palen), die met de hand in `WAPENREK` staan. Daarna
`gen-offline-manifest.py`; niet in `gen-klein.py`, hij is al klein. Lui geladen (`rekLaad`, `rekLaadLevel` in `laadLevel`).

De speren tekent het spel (`javImg`, met het rode lint), achter de plaat: de punt omhoog, de schacht door een lus, de
voet op de grond, een paar graden schuin (`WAPENREK.leun`, per lus anders). Zo staan echte speerrekken: de schacht in een
lus of gleuf bovenaan en de voet op de grond. Omdat de speren los van de plaat zijn, kan het aantal per level verschillen
en verdwijnt er zichtbaar een als Amir hem pakt. De voorbeeldplaat met de speren erin lag het eerst ter keuze voor
(07-11-2026). Een lus blijft van links naar rechts gevuld: Amir pakt de laatste.

## Maker en sandbox

- Maker nieuwstijl: Decor, Straat, **Wapenrek (speren)** (alleen in de stand stad); paneel met Gespiegeld (`MK_DECOR`).
  Soort is het aantal speren (vier tot leeg); wordt `wapenrekken: [{x, f, n}]`.
- Sandbox: De stad, **Wapenrek**: een vol rek (vier speren) voor je uit en verderop een gespiegeld met twee.
