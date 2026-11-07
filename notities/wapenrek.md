# Wapenrek: een houten rek in de stad met speren om te pakken

Code: de sectie `// ---- wapenrek: een houten rek in de stad met speren om te pakken ----` (`WAPENREK`, `wapenrekken`,
`rekMaak`, `rekReset`, `rekBij`, `rekTrek`, `rekUpdate`, `rekTeken`, `rekETeken`).

## In een level

`wapenrekken: [{x, f, n}]`: `n` speren (standaard 3, hooguit `WAPENREK.max`, 5), `f` spiegelt. In plaats van `x` kan het,
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

Nu nog getekend in code (hout en touw in `rekTeken`, de speren zijn `javImg`): een tijdelijke versie. De bedoeling is een
plaat uit Grok van het **lege** rek (zonder speren), op wit, in de stijl van `design/stad/kraam_riet.png`. Het spel tekent
de speren er dan achter, zodat het aantal kan veranderen. Die plaat moet open zijn tussen de palen en de balken, zodat de
speren erachter te zien zijn.

## Maker en sandbox

- Maker nieuwstijl: Decor, Straat, **Wapenrek (speren)** (alleen in de stand stad); paneel met Gespiegeld (`MK_DECOR`).
  Wordt `wapenrekken: [{x, f}]` met drie speren.
- Sandbox: De stad, **Wapenrek**: een rek met drie speren voor je uit en verderop een met vijf.
