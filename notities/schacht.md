# De schacht

### De schacht

Een smalle kloof tussen twee schermbrede rotswanden waar Amir van onder naar boven uit klimt, om en om naar
links en naar rechts springend. Het is geen nieuw systeem maar een opt-in samenstelling van wat er al is, zodat
de bestaande episodes (regel 1) er niets van merken: een grot-raster voor de wanden en de botsing, richels voor
de treden.

Vier kleine toevoegingen maken het:

- **De wand is ander gesteente.** Een grot met `schacht: true` tekent `grotMassa` niet met de terrasplaat
  (`klif_bovenrand`, die las als golvend kaarsvet) maar met de plafondvulling (`plafondVulTegel`,
  `rots_vulling`), hetzelfde steen als de tanden. Bestaande grotten zonder dat veld blijven de terrasplaat.
- **Tanden als zijafwerking.** `schachtTanden` (in `drawGrotten`, na de massa) zet langs elke verticale
  binnenrand van het raster precies dezelfde tandenband als het plafond (`grotBandSet`, op grotSteen-schaal,
  met de donkere rand `strookRand` eronder), een kwartslag gedraaid zodat de tanden de kloof in steken. Het
  tekent net als `plafondBand`: het massieve bovenstuk van de band (`GROT.band.dicht`) valt in de wand achter
  de vulling, de tanden hangen eruit, dus ze sluiten net zo netjes op de rots aan als aan een plafond. De
  diepte de kloof in is een vast deel van de celbreedte (`0.8 * R.cel`, wereld-px, normaal formaat), niet de
  sprite-schaal, want de kloof is schermbreed-vast; anders zijn de tanden op een hoog scherm veel te lang. De
  band wordt uniform met die diepte mee geschaald (`k`) en verankerd op de grondlijn zodat hij bij het klimmen
  niet schuift. De tanden lopen over de hele rand door, ook waar een plateau zit: het plateau wordt er in
  `drawClimb` overheen getekend (zie hieronder) en dekt de tanden erachter af, dus geen skip nodig. Daarnaast
  legt `schaduw` een zachte donkere gradient (multiply) op de wand vlak langs de kloofrand, over de hele
  hoogte, zodat de spleet diep oogt in plaats van vlak. Het zijn decor: ze doen Amir niets.
- **Savanne-grond bovenop de wand.** `schachtKap` (in `drawGrotten`, na de tanden) legt de grondtegel van het
  level (`bodemPic`, vast aan de wereld zoals de grond zelf) als een band op de bovenrand van elke volle
  kolomrij, met de looplijn precies op de wandtop; de aarde loopt een stuk door en vervaagt onderaan in de
  rots, dus de grijze rots blijft de ondergrond en de bovenkant is savanne. Zo land je er netjes op en loop je
  door. De bovenste steenrij vindt hij met `grotReeksH` (`tr`). De vervaging gebeurt op een los canvas
  (`destination-out` daar, dan overzetten): op het hoofdcanvas zou `destination-out` door de rots heen naar de
  lucht gummen, en dat gaf een lichte band aan de voet van de kap.
- **Gespiegelde treden, over de tanden.** Een richel met `f` wordt gespiegeld getekend (`drawLedge`: de
  spiegeling om `x`, met de botsing in `terracePlats` die meeklapt), zodat hij tegen de rechterwand past. De
  richels van de schacht staan niet op `achter`, dus `drawClimb` tekent ze ná `drawGrotten`, bovenop de tanden:
  het plateau steekt uit de wand en dekt de tanden erachter af. Zo lezen het plateau en de tanden als één
  geheel. De botsing (`terracePlats`) staat daar los van, dus ze dragen gewoon. (`achter: true` bestaat nog om
  een richel juist achter de wand te zetten, maar de schacht gebruikt het niet meer.)

**De wanden lopen schermbreed door.** Het raster is veel breder dan het beeld (veertien cellen per kant), met
het gat van drie cellen in het midden. De eerste rij van het raster is leeg (lucht), de rest steen: zo vindt
`grotTerrein` de lege cel boven de wand en geeft hij de wandtop terug (op zo'n 1500), zodat de fakkels
(`ends`) en de savanne-kap daar op de goede hoogte komen en Amir er bovenop kan staan en lopen. Zonder die
lege rij is een kolom helemaal vol en geeft `grotTerrein` `-Infinity` (geen vloer).

**De treden liggen om en om, met een echte zijwaartse afstand.** De linker tegen de linkerwand (bij -1380), de
rechter tegen de rechter (bij -1020), elke 150 hoger. Dat je ook in de breedte moet hoppen was de bedoeling:
er zit een dode zone tussen de tips van twee treden. Het haalbaar houden doet de luchtsturing: in dit spel
stuurt de richting ook in de lucht (zie de loop, `world += dir * 330 ...`), dus je springt van een trede, drijft
in de lucht naar de volgende en landt op de daalboog. Loopsnelheid, niet sprint: met sprint schiet je de
overkant in de wand. Een klim-botje (`tools/speelrobot.js` kan dit niet, het loopt alleen naar links) haalt
het van onder tot boven.

`start` zet Amir onderin tussen de wanden neer in plaats van ernaartoe te laten lopen (de wand zou de aanloop
blokkeren). Boven klimt Amir op de wandtop (de savanne-kap) en loopt links over de savanne. In Test 27 is de
linkerwand daarvoor breed (g.x -4140, 23 cellen): op de kap trekt hij een speer uit een skelet, springt over
een kei (schuilplek, regel 7: vijanden komen er niet voorbij) en verslaat een paar vijanden (twee slangen, een
schorpioen, een zwaardvechter) voor de fakkels. Alles op de kap staat op de wandtop (`terrainH` geeft daar de
wandtop, zo'n 1500). Test 27 is het proefstuk, met een savanne-bodem (veilig); een dodelijke kloof eronder kan
er later bij. Nog niet in de sandbox: een knop om de schacht-wand los te proberen.

## schacht: een kloof om uit te klimmen

de opt-in `schacht`: een grot-raster met `schacht: true` tekent `grotMassa` als de plafondvulling (`plafondVulTegel`) met een rechte rand, met de plafond-tandenband erlangs (`schachtTanden`, `grotBandSet` een kwartslag gedraaid zoals `plafondBand`, over de hele rand) en savanne-grond bovenop de wand (`schachtKap`, `bodemPic` met een vervagende onderkant). De gespiegelde richels (`ledges` met `f`) klimmen ertussen, vóór de tanden getekend zodat ze de tanden erachter afdekken, met een echte zijwaartse afstand ertussen. De wanden lopen schermbreed door met een lege bovenrij, zodat `grotTerrein` de wandtop teruggeeft. `start` zet Amir onderin tussen de wanden. Test 27 is het proefstuk; zie "De schacht" hieronder
