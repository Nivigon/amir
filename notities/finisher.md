# De finisher-voorspelling

`FINISHER`, `finZie`, `finDodelijk`, `finWorpReken`, `finWorpBijToets`, `finSteekStart`, `finZwaaiStart`,
`finVoorspelling`, `finUitslag`, `finTeken`, `sbFinToon`. Kop in de HTML: `// ---- finisher-voorspelling`.

## Waarom het er is (en wat nog komt)

Het idee: zodra een aanval begint al weten of die een vijand gaat doden, zodat het spel daar een eigen
afloop van kan maken, een speciale finisher-animatie (een andere follow-through van Amir, slow motion, een
camera die met de speer meegaat, een eigen sterfanimatie). **Die animaties zijn er nog niet.** Wat er nu
staat is alleen de voorspelling: het spel rekent het uit, bewaart het en meet achteraf na of het klopte. In
het gewone spel zie en merk je er niets van. In de sandbox kun je het laten zien.

Dit is de voorbereiding. De bedoeling is dat we hier later op verder bouwen door die finisher-animaties
toe te laten; dan is dit de plek om ze aan te haken (zie "Voor later" hieronder).

## Wanneer het rekent

- **Worp, bij het loslaten van de toets** (`thrRelease` roept `finWorpBijToets`): de speer verlaat de hand
  pas op `THR_LOOSE`, dus het rekent vanaf dat moment vooruit (`wacht`). `worpBaan` geeft de baan; dat is
  dezelfde rekensom die `looseSpear` nu gebruikt om de speer te maken, dus die twee lopen niet uit elkaar.
- **Worp, als de speer echt weggaat** (`looseSpear` roept `finWorpBijWorp`): nog een keer, vanaf de echte
  speer, met de vijanden waar ze dan zijn. Dit staat ook op de speer zelf (`jav.fin`).
- **Steek, bij het begin** (`startAttack` roept `finSteekStart`): de punt per raakframe (`ATK_ACTIVE`,
  `TIP_DX`, `TIP_Y`, het vak van `steekR`) tegen de vijanden. Alleen met de speer: het mes doodt niets.
- **Lage zwaai, bij het begin** (`startSweep` roept `finZwaaiStart`): het vak rond Amir over de raakframes
  (`SWEEP_FROM` tot `SWEEP_TO`). De zwaai raakt alles in zijn vak, dus hier is het een lijst.

## Hoe het rekent

De raakvakken komen uit de teken-lus, waar elke vijand ook echt geraakt wordt: elke vijandlus geeft zijn vak
door aan `finZie` (via `finZ`, ook in `goudapenTeken` en `drawFosforSlangen`). Dat rekent het om naar de
wereld (x in wereld-px, hoogte in hoogte-eenheden boven de grondlijn) en zet het in `s.fin`, met een
geschatte loopsnelheid uit het vorige beeld (`vx`, glad gemaakt met `FINISHER.vxGlad`). `finGezien` is de lijst
van het laatste beeld, in de volgorde van de teken-lus, zodat bij twee vijanden achter elkaar dezelfde de
speer opvangt als in het spel.

De vlucht van de worp is gewone natuurkunde zonder toeval (`javUpdate`: Euler, `GRAVITY * JAV.gDeel`), dus
`finWorpReken` doet dezelfde stappen op 60 fps tot de grond, de rotswand, een ravijn of een doornbos. Elke
vijand schuift daarbij mee met zijn `vx`.

Of de treffer dodelijk is beslist `finDodelijk(s, wijze, t)`, per soort dezelfde voorwaarden als in zijn
hit-functie, zonder iets te veranderen:

| soort | dodelijk als |
| --- | --- |
| slang, schorpioen | zonder health-balk altijd, anders de laatste hp (`enemyTakeHit`) |
| fosforslang | de laatste hp, niet met een worp (die ketst af) |
| hyena, meelman | de laatste hp |
| panter | de laatste hp, en alleen in `land` of `rest` (`hitPanther`) |
| bandiet | de laatste hp, niet in een vault of van boven; met `inv` pareert hij |
| schildbandiet | schild weg (`schild === 0`) en niet onaantastbaar in zijn sprong |
| kooiman | de laatste hp, en alleen als hij openligt (`kooiOpen`) |
| kruisboogbandiet | de laatste hp |
| goudaapje | altijd, met een worp alleen in de lucht |
| baviaan | nooit (hij is niet raakbaar, alleen de speerval doodt hem) |

`inv` telt alleen als hij op het moment van de treffer nog loopt.

## Wat het niet ziet aankomen

Alles wat tussen het begin van de aanval en de treffer verandert:

- een vijand die springt, draait, stilvalt of versnelt (hij schuift alleen recht mee met zijn snelheid);
- een staat die omslaat (de panter die uit zijn herstel komt, de kooiman die dichtklapt, de schildbandiet
  die aan zijn sprong begint en dan onaantastbaar is);
- **een klap op Amir**: die breekt de steek en de zwaai af, en kan een worp laten mislukken. In de sandbox
  zag je dat met een schorpioen die op Amir afstormde: de zwaai was voorspeld als dodelijk voor twee, maar
  ging nooit af.

Daarom meet het na. `finStap` kijkt na elke aanval (`FINISHER.oordeel` na het einde) of het voorspelde doel
dood is, en telt met `finDoden` (in `vijandDood`) of er een kill was die niet voorspeld was. De telling staat
in `finUitslag`: `klopt`, `mis` (voorspeld maar niet dood), `gemist` (dood maar niet voorspeld) en `geen`.

## In de sandbox

Onder Speer en spullen, bij Speerworp: **Finisher: uit / toon** (`sbFinToon`). Aan krijgt een voorspeld doel
een rode ring met "dodelijk", een doel dat geraakt maar niet gedood wordt een grijze. Na elke aanval meldt
een hint of het klopte, met de telling tot nu. De knop zet de telling op nul.

## Voor later: de finisher zelf

`finVoorspelling()` geeft wat er nu voorspeld is: `worpBijToets`, `worp` (bij het wegvliegen), `steek` en
`zwaai` (een lijst). Elk doel is `{soort, s, t, wijze, dodelijk}`, met `t` de seconden tot de treffer.
Hier haakt de finisher straks aan. Twee dingen om dan te kiezen:

1. **De voorspelling waar maken.** Een finisher-animatie die begint en dan niet doodt is erger dan geen.
   Begint de finisher, leg de uitkomst dan vast: de speer stuurt een klein beetje bij naar het doel, het doel
   bevriest of vertraagt, en Amir is onkwetsbaar tot de treffer (zoals `exeVries` in de executie van de
   schildbandiet, sluit daarop aan in plaats van een tweede bevriezing te bouwen).
2. **Wanneer beslissen.** Bij de toets is het vroegst, maar de vijand heeft dan nog een hele vlucht om te
   bewegen. Bij het wegvliegen (`jav.fin`) of vlak voor de inslag is het zekerder, maar is Amirs eigen
   worpbeweging al voorbij. Voor de steek is het begin al zeker genoeg: het raakvenster is kort.

De executie van de schildbandiet (`exeKans`, `exeStart`) beslist nu nog bij de inslag. Die kan later dezelfde
voorspelling gebruiken.
