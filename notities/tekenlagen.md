# Niet verder tekenen dan in beeld

## niet verder tekenen dan er in beeld komt

`zichtVak(marge)` geeft het zichtbare vak in de coordinaten die nu gelden (`view` van een level en de schok van het schudden zitten erin verrekend), of `null` als de ruimte scheef staat; `vulVak(x, y, w, h)` is een `fillRect` die daar niet buiten reikt; `werkDoek(naam, w, h)` geeft een doek dat hergebruikt wordt in plaats van elk beeld een nieuw canvas. Elke laag die op wereldmaat tekent en door een clip op zijn plek wordt gehouden, hoort hier tegenaan te lopen: de tegellussen van een gang (`tegel` in `drawHolte`), de grondtegel in `scene`, de achtergrondpanelen (`drawLayer`) en de wand en de kap van een schacht (`grotMassa`, `schachtKap`). Dat was het haperen: niet de pixels (het canvas knipt het overschot zelf weg) maar de lussen en de doeken eromheen, in Klim 9 en Test 27 145 en 137 ms per beeld, nu 9. Verander je hier iets, draai dan `tools/beeldgelijk.js`

## de verte als platen

De verte (lucht, zon, drie bergrijen, het land en de nevel ertussen, de tint en het waas) was per beeld ruim tien schermbrede vullingen over elkaar, samen ongeveer een derde van de beeldtijd. Nu staat hij klaar als plaatjes (`vertePlaten`, `verteBak`, `verteTeken`):

- **de lucht**: de lucht en de zon op schermmaat, staat stil op het scherm. De ring om de zon ademt nog: alleen het vakje om de zon ligt er in `VERTE.fasen` (16) standen overheen, elk een keer gemaakt.
- **een strook per bergrij** (verre bergen, tweede bergrij, heuvels): de rij zelf met het land en de nevel die erachter horen er al in. Een strook is aan elke kant `VERTE.marge` (0,3) scherm breder dan het beeld, schuift met de eigen parallax van de rij, en wordt opnieuw gemaakt als de camera eruit loopt (`vertePlaatBak`). Een strook reikt niet verder omlaag dan waar het land van de volgende hem dekkend afdekt.

De tint en het waas (`sc.dim`, `sc.waas`) lagen over alles heen; die zitten nu met `source-atop` in elk plaatje zelf (`verteTint`). Dat komt op hetzelfde uit zolang het geheel dekkend is.

De platen hangen aan alles wat de hoogte bepaalt (`groundY`, de horizon, de heuvellijn, de maat van het venster, het uitzicht, `MIST`, `LAND`, `ZON`): verandert daar iets aan, dan tekent `sceneAchter` de oude weg tot het `VERTE.rust` (2) beelden stilstaat. Tijdens klimmen of zakken van de camera is er dus geen winst. De stad heeft haar eigen stroken (`stadAchter`) en doet niet mee. Gaat het bakken mis, dan zet het spel `VERTE_PLAAT` uit en meldt het een keer.

Het beeld is niet pixel voor pixel gelijk: elk paneel staat op de strook op een hele pixel, dus bergranden kunnen een halve pixel verschuiven (gemeten: 87 tot 92 procent van de pixels gelijk, de rest op de randen, hoogstens enkele tientallen stappen). Nameten: `node tools/beeldgelijk.js --vlag VERTE_PLAAT`.

Gemeten zonder grafische kaart (software, 1280x720): Valse Koning 1 van 37 naar 31 ms per beeld, op 2x van 117 naar 92, Test 13 van 33 naar 26, Baboon 1 van 35 naar 28, Test 24 (veel klimmen) van 33 naar 29. Dat is 18 tot 22 procent; de bovengrens (de verte als een stilstaande foto) was 35.
