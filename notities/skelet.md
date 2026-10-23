# Het skelet met de speer

### Het skelet met de speer

De plaatjes staan in `design/botten/skelet/` en zijn allemaal op één schaal gemaakt: 0,19 bij een Amir van 237 px
(`SKELET.schaal`), dus het zittende skelet is 0,61 Amir. Rekenen gaat in skeletcoordinaten, met (0, 0) op de
linkerbovenhoek van het skelet zelf en de grond op 754.

- **Zitten** zijn de negen losse botten uit `delen/` op hun plek, met daarover de speer,
  `skelet_voorste_botten` en het doekframe. De voorste botten zijn niet optioneel: zonder die laag ligt de speer op
  het skelet in plaats van erdoorheen. Tot de botten binnen zijn staat `skelet_met_speer.png` er.
- **Instorten** speelt het spel zelf met die botten (`SKELET.delen`, `skBotten`), op de valcurve van het pakket. De
  ingebakken sheet uit het pakket wordt niet gebruikt: daarin bleven de onderbenen met de knie in de lucht staan. Nu
  kantelt het bovenbeen om de heup en ploft het onderbeen plat (`a` en `laat` bij de benen). Een kind draait mee met
  zijn ouder, zoals in `onderdelen.json`.
- **De schedel** is na het instorten, of als hij eraf getikt is, een los ding (`s.kop`): hij valt, landt met stof,
  rolt met de hoek aan de afgelegde weg (weg gedeeld door de straal van 58) en ligt dan stil. Daarna is hij decor:
  tegenaan lopen of erop slaan doet niets.
- Wat Amir kan: E **vasthouden** bij de schacht trekt de speer eruit (`skeletTrek`, `skeletTrekLos` bij het
  loslaten van de toets of de E-knop). Het skelet schudt steeds harder, de speer schuift eruit en rond de E loopt een
  ring vol; na `SKELET.trek.duur` (2 seconden) laat hij los en ploft het in elkaar. Eerder loslaten of weglopen en hij
  blijft erin. Alleen met lege handen: een speer die je met E hebt weggestoken telt als in je hand (dan wiebelt hij en
  speelt `sounds/dontneedthis.mp3`); een weggegooide speer niet, die blijft liggen waar hij ligt. Een steek of een worp tegen de schedel
  tikt die eraf (`skeletRaak`, aangeroepen vanuit de tekenlus waar ook de slangen geraakt worden). Een lage zwaai laat het
  meteen vallen, en de speer valt eruit en blijft liggen.
- De speer uit het skelet heeft een **blauw vaantje**. Het rode lint zit in Amirs sprites gebakken en wordt bij het
  tekenen omgekleurd (`vaanBlauw`, `vaanMaak`). Op tint alleen gaat dat mis: in de idle is het lint oranje, en in de
  werpframes is zijn huid net zo verzadigd als het lint. Wat scheidt is helderheid, samenhang en nabijheid; de stappen
  en getallen staan bij `VAAN`. Verander je iets, kijk dan alle speerframes na, ook de twintig van de worp. De grote
  werpframes kosten tot een tiende seconde, dus die worden vooraf gedaan zodra je de blauwe speer hebt (`vaanVoorwerk`).
- **Losse speren** (`losseSperen`): er kan nu meer dan een speer zijn. Wat niet in je hand is en niet je eigen speer in
  de wereld, ligt daar. Pak je een andere speer terwijl de jouwe ergens ligt, dan wordt de jouwe een losse speer
  (`eigenSpeerNeer`), zodat hij niet verdwijnt.
- Het geluid `sounds/skeletvalt.mp3` start als het valt, niet bij het trekken, en gaat via een versterker op 3,6
  (vier keer 0,9), want een audio-element komt niet boven 1. Een tweede instorting start het opnieuw.
- Stof: eigen wolkjes per skelet (`SKELET.stof`), want `stofwolk.png` is ijl en `puffWorld` is voor een voetstap.
- De schaduw vermenigvuldigt de grond met (0,74, 0,80, 0,91) en ligt naar links, want de zon staat rechtsboven.

De plaatjes laden pas als er een skelet in het level staat (`skeletLaad`).

## skelet met speer

`SKELET`, `skeletTrek`, `skeletUpdate`, `skeletTeken`, `skeletRaak`: E vasthouden trekt de speer eruit, het skelet stort in met de losse botten (`sounds/skeletvalt.mp3`); de schedel is daarna los decor; losse speren op de grond (`losseSperen`) en het blauwe vaantje (`vaanBlauw`)
