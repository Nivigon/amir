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

Hoger op (`tonOp`): met `dak` (`true` of een hoogte, net als bij een vijand, zie `stadDakPlek`) staat hij op het dak of de
galerij van de stad het dichtst bij `x`, met `zwever: true` op de zwevende savannelaag boven `x`. Een dak schaalt mee met het
scherm: met `a` (Amir van het midden van dat dak) staat hij op elk scherm op dezelfde plek, zonder `a` op `x`; altijd een halve
ton binnen de rand. Een stapel op een dak: elke ton krijgt hetzelfde `dak` en dezelfde `a`, de bovenste met `y: 0.62`. Hij houdt
zijn vloer bij (`t.vloer`, `{h, l, r}`), dus de losse stukken en de kalebas blijven op het dak liggen (`tonStukVloer`,
`hppotionHopVloer`); wat over de rand vliegt valt naar beneden. Op een dak staat hij achter de kartels: `stadKanteelVoor` tekent de tanden na
de personages opnieuw in een strook rond elke ton op dat dak (net als rond wie erop staat), zodat alleen zijn bovenkant
erboven uitsteekt en de bovenste van een stapel er helemaal bovenuit komt. Op een galerij achter de leuning, zonder slagschaduw op de straat. Nyundo op de straat komt er niet bij
(`tonBruut` slaat een ton op een dak of zwever over). Een terras van grond (`terraces`, ook `grond: true`) hoeft niets: daar
staat een ton al vanzelf op (`terrainH`).

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
- **Naar de lens** (`TON.lens`, `tonLensMaak`, `tonLensStap`, `tonLensTeken`): in de slag van de opening van het plein
  (`brutus.intro.fase === 'slag'`, in `tonBruut`) vliegen de stukken in plaats daarvan echt op de camera af. Elk stuk heeft
  een plek in het beeldvlak en een diepte `d` van 1 (de ton) naar 0 (de lens); op het scherm staat het op het midden plus
  (plek min midden) / d, 1/d keer zo groot, onscherp (tot `blur`) en donkerder. Per ton schieten er `langs` langs de rand
  weg (hooguit `max`), en een keer per slag een half deksel (`stuk_08`) dat zo gericht is dat het na `raakDuur` op `doel`
  tegen de lens slaat, zo hoog als `vulling` van het scherm: een hitstop (`stop`), een schok, een doffe klap
  (`tonLensKlap`, zonder bestand), het plakt `plak` s, glijdt weg (`glij`) en er blijft stof op de lens (`stof`). De plek
  op het scherm wordt in de wereldlaag gezet (`tonLensPlaats`, met de zoom erin); getekend wordt na de balken van de
  opening (`tonLensTeken`, na `bruIntroTeken`), in schermcoördinaten, zodat het niet met de wereld mee schudt. In het
  gevecht zelf blijft het de oude manier: een stuk op de lens zou het zicht wegnemen.
- **Kapot is kapot**: wat Nyundo breekt (`tonBruut`) onthoudt `tonKapot` (per level, per sessie, de index in `level.tonnen`),
  en `tonReset` zet die na een dood niet terug. Wat Amir breekt komt bij een nieuwe poging gewoon weer heel terug.
  Sandbox: De stad, **Tonnen naar de lens** (`sbtonlens`): drie tonnen die na `lensT` (1,2 s) in een klap gaan, met de lens.
- Een ton op een ton valt als de onderste weg is (`tonStap`), met een tik en wat stof.
- Hooguit `TON.max` losse stukken; daarna vervaagt de oudste.

## De plaatjes

`tools/ton_kleur.py` maakt alles uit de Grok-platen in `design/stad/ton/bron/` (heel, met een gat, gebroken, en een plaat
losse stukken): de drie standen op een maat en een voetlijn (304 hoog), de losse stukken op dezelfde schaal (`stuk_01` tot en
met `stuk_20`), warmer en lichter dan Grok ze gaf (op het zonnige plein stonden ze anders in de schaduw), en `ton.json` met de
maten. De soorten stukken (splinter, duig, hoepel, deksel) staan als nummers in `TON.soort`; maak je de plaat opnieuw, kijk
die lijst dan na. Daarna `gen-offline-manifest.py`. Niet in `gen-klein.py`: ze zijn al klein.

## Sandbox en Maker

In de Maker nieuwstijl onder Decor, Kamp: **Ton**, met een, twee naast elkaar of twee met een erop, en een kalebas erin (zie "Tonnen en
stadsvolk" in `notities/maker.md`); die krijgt altijd een eigen `x`.

Onder De stad, **Tonnen**: twee net over elkaar en een recht op de voorste voor je uit, en een losse met een kalebas.
**Tonnen op het dak**: zo'n stapel op het dak van het huis van 2 hoog en een losse met een kalebas op de galerij (zet de stad
neer als die er nog niet is). Onder Zwevende laag, **Tonnen erop**: twee met een erop bovenop de laag.

In de Maker: teken je een ton op een dak, galerij of balkon, dan krijgt hij `dak` (de hoogte van die vloer, zoals een vijand),
op een zwevende laag `zwever: true`.
