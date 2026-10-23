# Niet verder tekenen dan in beeld

## niet verder tekenen dan er in beeld komt

`zichtVak(marge)` geeft het zichtbare vak in de coordinaten die nu gelden (de zoom van de bouwer, `view` van een level en de schok van het schudden zitten erin verrekend), of `null` als de ruimte scheef staat; `vulVak(x, y, w, h)` is een `fillRect` die daar niet buiten reikt; `werkDoek(naam, w, h)` geeft een doek dat hergebruikt wordt in plaats van elk beeld een nieuw canvas. Elke laag die op wereldmaat tekent en door een clip op zijn plek wordt gehouden, hoort hier tegenaan te lopen: de tegellussen van een gang (`tegel` in `drawHolte`), de grondtegel in `scene`, de achtergrondpanelen (`drawLayer`) en de wand en de kap van een schacht (`grotMassa`, `schachtKap`). Dat was het haperen: niet de pixels (het canvas knipt het overschot zelf weg) maar de lussen en de doeken eromheen, in Klim 9 en Test 27 145 en 137 ms per beeld, nu 9. Verander je hier iets, draai dan `tools/beeldgelijk.js`
