# Het gif, de speer in de winkel en de inventory

Kop in de HTML: `// ---- het gif: ...` en `// ---- inventory: ...` (direct na het winkelscherm).

## De winkel

Het winkelscherm (`winkelUIToon`) heeft drie knoppen: kalebas (`#wkkalebas`), speer (`#wkspeer`) en gif (`#wkgif`).
De prijzen staan in `GOUD`: `kalebas` 5, `speer` 15, `gif` 40. Zonder goud (`goudAan`) is alles gratis, maar er moet
wel plek zijn. `winkelBetaal` doet het betalen en het schudden.

- **Speer.** `winkelSpeerNiet` zegt waarom het niet kan: geen rug (`rugAan`), of hand en rug vol. Kan het, dan gaat er een
  speer op de rug (`rugErbij`), en is je hand leeg, dan meteen in je hand (`rugTrekKlaar`). De speer geldt alleen voor
  dit level: `restart` begint toch met een volle rug. Een speer die ergens op de grond ligt, telt niet als vol.
- **Gif.** Een plek in de inventory (`gifCarry`).

## De inventory

`INV_MAX` (= `HPPOTION_MAX`, nu 5) plekken. Een plek per ding: eerst de kalebassen (`hppotionCarry`), dan het gif
(`gifCarry`). `invVol()` is de enige check op ruimte: het oprapen van een kalebas, de winkel en de sandbox gebruiken
hem allemaal. I of het tasje in de HUD (`#invknop`) opent hem (`invUIOpen`), het spel staat dan stil (`paused`), en
Escape, I of Verder sluit hem. Klik op een vak voor de uitleg (`INV_DING`) en de knop: Drinken (`drinkHppotion(true)`,
mag ook als het spel stilstaat) of Op speren smeren (`gifSmeer`). Het tasje krijgt een groene rand zolang de speren
gif hebben.

Wat er in de inventory zit en hoeveel gif de speren nog hebben, gaat mee naar het volgende level, net als het goud
(`goudWin`, `goudVerder`, `goudReset`, met `gifBank` en `gifHitsBank`). Buiten een goudlevel begint elk level leeg
(`resetHppotions`).

## Het gif

`GIF`: `hits` 10, `tik` 3 s, `baas` 0,5 leven.

- **Smeren** zet `gifHits` op 10, voor al je speren samen (hand, rug, de geworpen speer).
- **Een treffer** van Amir roept in de hit-functie van de soort, net na `hits++`, `gifRaak(s, soort)` aan. Alleen
  soorten in `GIF_SOORTEN` (bandiet, kooiman, meelman, kruisboog, zweepman, schildman, hyena, Brutus) vatten het; slang,
  schorpioen, fosforslang en panter zijn immuun en kosten niets. Niet met het mes (`atkMes`), en bij de schildbandiet
  niet als de speer in het schild komt (`s.schild > 0`). Elke treffer met een gifspeer spat wat bloed en gif (`gifSpat`).
- **Pas het volgende beeld** (`gifWacht`, in `gifUpdate`) kost het een treffer: alleen als de vijand de treffer overleefde
  en nog niet vergiftigd was. Een vergiftigde vijand opnieuw raken kost dus geen gif; zijn klok loopt door, de gewone
  schade wel.
- **De tik** (`gifTik`): elke 3 s roept het de hit-functie van zijn soort aan met `gifTikNu` aan. Daardoor speelt elke
  soort zijn eigen geraakt-reactie en zijn eigen dood (en `vijandDood`, dus goud en de kill-tellers), terwijl
  `sneakKan` en `critPak` niets doen en de kooiman, zweepman, kruisboogbandiet en schildbandiet niet afketsen of
  ontwijken. `hits` wordt teruggezet: een tik is geen treffer van Amir. Lukt het niet (de schildbandiet in zijn sprong),
  dan probeert hij het 0,2 s later opnieuw.
- **Een baas of aanvoerder** (`gifBaas`: Brutus, `aanvoerder`, `boss`) verliest eenmalig `GIF.baas` leven (alleen de
  flits en de spetters), en dan is het gif op. Heeft hij niet meer dan dat over, dan is de tik zijn laatste klap.
- **Zweepman met fasen**: neemt het gif zijn laatste leven van fase 1, dan is hij gewoon dood, geen arm eraf en geen fase 2
  (net als bij een sluipaanval, `!gifTikNu` in `hitZweepman`). Komt hij toch in fase 2 (`f2`), door een speer, dan is het gif uitgewerkt.

### Te zien

- `gifSpat` en `gifFxTeken`: druppels rood en groen, bij elke treffer en elke tik (getekend na Amir, naast de crit-ster).
- `gifVijandTeken` (vanuit `vijandHpBalk`, dus bij elke vijand na zijn sprite): een groene waas en vier belletjes.
- `gifBalkAf` in `vijandHpBalk`: de balk loopt langzaam leeg naar de volgende tik, het stuk dat het gif al opat ademt
  groen, en de rand is groen.
- `gifPuntTeken`: een groene punt op elke speer die apart getekend wordt (op de rug in `rugSpeerTeken`, geworpen in
  `javSchacht`), minder groen naarmate de treffers opraken; `gifDrupTeken` laat er een druppel van groeien en vallen.
- `gifHandTeken`: de speer in de hand zit in de sprite van Amir, dus daar weet het spel alleen bij de steek en het
  spannen waar de punt is; dan een groene gloed en een druppel. Rechtop in de hand (stilstaan, lopen) is de punt niet groen.

## Sandbox

Onder Speer en spullen, de rij **Gif**: **Gif in inventory**, **Gif op speren**, **Speren schoon** (ook niemand meer
vergiftigd) en **Winkel** (opent het winkelscherm, gratis). Zet de health-balk aan (Vijanden) om de balk te zien aflopen.
