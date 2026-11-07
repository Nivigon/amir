# Tonnen: houten tonnen die breken

Code: de sectie `// ---- tonnen: houten tonnen die breken ----` (`TON`, `tonnen`, `tonStukken`, `tonLaad`, `tonReset`,
`tonRaak`, `tonBreek`, `tonBruut`, `tonStap`, `tonTeken`, `tonVoorTeken`, `tonVak`). Plaatjes in `design/stad/ton/`.

## In een level

`tonnen: [{x, y, f, kalebas}]`, of in plaats van `x` een plek ten opzichte van de stad:

- `put: i, a`: bij `stad.putten[i]`, `a` Amir van het midden van de put. De luifel zit in Amir aan de put vast
  (`STAD.plein.luifel.af`, 2,3), dus zo blijft een ton op elk scherm onder de luifel. Tussen de rand van de put
  (1,05 Amir) en de paal (2,3) is plek voor twee tonnen naast elkaar (a 1,45 en 1,85, net over elkaar) en een erop.
- `luifel: i, a`: net zo bij een losse luifel (`stad.luifels[i]`, zonder put); daar is plek van ongeveer -0,5 tot -2 Amir
  (de paal staat op -2,3 bij `kant: 'l'`). Stad 6: a -1,82 en -1,42 (net over elkaar) en recht op de voorste -1,42, y 0,62.
- `kraam: i, a`: naast `stad.kramen[i]` (het midden van de kraam, 1,68 Amir breed): a 1,1 staat er net naast. Een stapel
  (Stad 4, Beleg 4): a 1,1 en 1,5 net over elkaar, en de bovenste recht op de voorste (a 1,5, y 0,62).

`y` is de hoogte van de onderkant in Amir (0,62 is een ton op een ton, `TON.h`). Een ton op een ton staat in werkelijkheid
op `TON.stapel` (0,55): hij zakt in het deksel van de onderste, anders zweeft hij op de rand (`tonMaak` zet een y van
een of meer tonnen hoog om, `tonStap` laat hem daarop landen). Mooiste stapel: recht op een ton, niet in de kier tussen twee. `f` spiegelt, `kalebas: true` laat er
een drinkkalebas uit springen (`dropHppotion`). `tonPlekX` rekent de plek elk beeld opnieuw uit, zodat hij meeschuift
als het scherm van maat verandert.

Waar ze staan (06-11-2026): Stad 1 tot en met 4, Stad 6 (onder beide luifels: drie onder de losse links, twee bij de put rechts), Oaktown, Beleg 1 tot en met 7, en een
paar lege in de roverskampen van Valse Koning 2 en 5 (met toestemming, regel 1). Alleen in Stad 1 zit een kalebas.

## Gedrag

- Decor: Amir en vijanden lopen erdoorheen. Getekend achter Amir (na de keien), met een schaduwtje.
- **Amir**: steek, lage zwaai of geworpen speer, drie treffers (`TON.treffers`). 1: een gat in een duig (`ton_1`), splinters,
  `houtRaak`. 2: de bovenkant breekt eruit (`ton_2`, de losse hoepel uit de Grok-plaat is weggelaten), een duig vliegt weg.
  3: `tonBreek`: het breekgeluid (`tonBreekGeluid`: `sounds/ton_breek.mp3` na een paar treffers, `sounds/ton_zwaar.mp3` als hij in een klap gaat, zoals bij Nyundo; breken er meer tegelijk, dan klinkt het een keer), stof (`banStofWolk`, `puffWorld`) en negen losse stukken die van Amir af spatten, stuiteren
  (met een tikje), gaan liggen (plat, of op hun kant als ze lang en smal zijn) en na `TON.liggen` vervagen.
- **Nyundo** (`tonBruut(l, r, top, from)`, wereld-x): alles in dat vak gaat in een keer. Aangeroepen vanuit het Brutus-blok
  in de tekenlus (zijn lijf in de storm, het raakvak van de zwaai of de kap), `bruInslag` (de kap, 110 grote-set-px om de bal)
  en `bruSprongInslag` (260 om de bal). Dan valt hij in een hoopje (zeven stukken op de plek, `TON.hoopLiggen` 45 s), vliegen
  er twee of drie stukken naar de camera (`z > 0`: groter, van het midden af, onscherp, getekend voor alles in
  `tonVoorTeken`) en een de verte in (`z < 0`, kleiner, achter).
- Een ton op een ton valt als de onderste weg is (`tonStap`), met een tik en wat stof.
- Hooguit `TON.max` losse stukken; daarna vervaagt de oudste.

## De plaatjes

`tools/ton_kleur.py` maakt alles uit de Grok-platen in `design/stad/ton/bron/` (heel, met een gat, gebroken, en een plaat
losse stukken): de drie standen op een maat en een voetlijn (304 hoog), de losse stukken op dezelfde schaal (`stuk_01` tot en
met `stuk_20`), warmer en lichter dan Grok ze gaf (op het zonnige plein stonden ze anders in de schaduw), en `ton.json` met de
maten. De soorten stukken (splinter, duig, hoepel, deksel) staan als nummers in `TON.soort`; maak je de plaat opnieuw, kijk
die lijst dan na. Daarna `gen-offline-manifest.py`. Niet in `gen-klein.py`: ze zijn al klein.

## Sandbox

Onder De stad, **Tonnen**: twee net over elkaar en een recht op de voorste voor je uit, en een losse met een kalebas.
