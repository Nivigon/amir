# Het plafond als hoogtelijn

### Het plafond als hoogtelijn

Het raster hierboven is terrein in cellen, en dat geeft rechte hoeken. Voor rots boven je
staat daarnaast de plafondlijn, en die is opgezet als de grond: `terrainH(x)` geeft per
wereld-x hoe hoog de bodem ligt, `plafondH(x)` geeft hoe hoog de onderkant van de rots hangt,
allebei in sprite-eenheden boven de grondlijn. Tussen twee punten loopt de lijn recht door,
dus een schuin stuk is niet meer dan twee punten op verschillende hoogte.

```
plafond: [ {x: -1000, y: 4000},    geen plafond: PLAFOND_WEG of hoger is open lucht
           {x: -2600, y: 360},     zakt schuin in beeld tot een gang
           {x: -5200, y: 280},     en knijpt verder dicht
           {x: -6600, y: 4000} ]   weer omhoog, uit beeld
```

De punten mogen in looprichting staan (x steeds negatiever); het spel zet ze zelf op volgorde.
Reken met Amir: hij is `CHAR_H` (251) hoog en springt 200 (zie "de sprong" hieronder). Boven de 460 merkt hij niets, op
400 loopt hij rechtop maar stoot hij bij elke sprong zijn hoofd, op 280 zit springen er niet
meer in, en onder de 251 kan hij er helemaal niet langs, want gebukt loopt hij niet.

Staat er iets onder de lijn om op te springen, tel dan door: een plafond knipt zijn sprong af,
dus de lijn moet minstens op de hoogte van dat ding plus 251 plus ongeveer 75 liggen. Op de kei
van Test 1 (114 hoog) is dat 440. Op 400 haalt hij het ook nog, maar alleen als hij precies op
tijd afzet, en dan sta je de halve tijd klem voor een kei van een halve meter. Dat is gemeten,
niet geschat: op 400 lukt de sprong vanaf 30 tot 180 px voor de kei, op 440 vanaf 30 tot 270.

Drie lagen, in deze volgorde:

1. **Vulling** (`plafondVulling`): alles boven de lijn, met de lijn als clippad. De tegel is
   `design/grot/rots_vulling.png`, uit het massieve deel van `plafond_strook` geknipt
   (`tools/rots_vulling.py`), en wordt op `grotSteen()` getekend: dezelfde schaal als de band,
   dus per definitie dezelfde korrel. Naadloos in beide richtingen, nooit uitgerekt, en hij
   loopt altijd door tot ruim voorbij de bovenrand van het scherm.
2. **Band** (`plafondBand`): dezelfde tandenrand als bij de grotten (`GROT.band`, de onderste
   160 bronrijen van `plafond_strook`), maar langs de lijn, en per stuk meegedraaid met de
   helling. Het patroon loopt door over de knikken heen (`plafondFase`), anders begint het bij
   elk stuk opnieuw en zie je de knik in het steen zitten. Die fase moet ook doorlopen buiten
   de lijn: het spel tekent anderhalve schermbreedte breder dan het beeld, dus aan het eind
   van een level ligt de rand van dat venster voorbij het eerste punt van de lijn. Daar is de
   lijn vlak (`plafondH` klemt), dus de lengte is gewoon de afstand, en `plafondFase` geeft
   hem negatief terug. Stopt hij daar op nul, dan staat de fase stil terwijl het stuk tussen
   de vensterrand en het eerste punt wel meegeteld wordt, en plakt de tandenrand aan het
   scherm in plaats van aan de wereld: hij schuift dan precies met je mee.
3. **Losse blokken** (`plafondDecorLijst`): om de `PLAFOND_STAP` wereld-px een plek, waar
   ongeveer een op de drie keer een hangblok of een richel hangt, met een seed uit de lijn zelf.
   Ze worden afgesneden op de lijn: wat erboven uitsteekt zit in het steen. Hoe krapper de
   ruimte onder de lijn, hoe kleiner ze uitvallen (`PLAFOND_HANG`), want je moet er niet
   doorheen hoeven lopen.

De band loopt aan zijn bovenkant uit in de vulling (`PLAFOND_VERVAAG`), en de vulling loopt
daarvoor even ver door onder de lijn. Zonder die overgang ligt er een lichte plaat met een
kaarsrechte bovenkant op de rots, en dat is precies wat er bij de grotset ook al misging.

Botsen: de ruimte boven de lijn is massief. `plafondKop` is de laagste lijn over zijn breedte
min zijn eigen lengte, en gaat samen met `grotKop` als plafond in `updateJump`. `plafondBlok`
duwt hem terug waar de lijn onder zijn kruin duikt, zoals `grotBlok` dat bij een celwand doet.
Hangblokken zijn decor; alleen `wand_richel` draagt, met dezelfde hitbox als in een grot
(`plafondPlats`).

`hoek_plafond_wand.png` en `wand_rand.png` worden nergens meer getekend. Ze blijven wel in
`design/grot/` staan, voor later, als er een ravijn komt waar je in afdaalt.

## plafond: de rots boven je, als hoogtelijn

`plafond`: de lijn, de vulling, de band, de losse blokken
