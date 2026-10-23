# Sandbox

## Sandbox

De sandbox start met vlakke grond en een leeg level, geen automatische vijanden en
geen levens. Een knop erbij is twee dingen: een `<button>` in `<div id="sandbox">`
(een eigen `.row` met een `<label>` als het een nieuw onderwerp is) en de afhandeling
in de sandbox-sectie van de code. De rijen staan in tabbladen per categorie (`.sbcat`:
Vijanden, Speer en spullen, Decor, Terrein, Beeld en geluid), want alles onder elkaar past
niet meer op het scherm. Zet een nieuwe rij in de categorie waar hij hoort; een nieuwe
categorie is een `.sbcat` met een `data-cat` en een knop met dezelfde `data-sbcat` in `#sbtabs`.
Van rechts, Alles weg en Terug naar menu staan eronder, buiten de tabbladen. Spawnen gebeurt net binnen beeld aan de gekozen
kant (`sbFromRight`), altijd geklemd tussen `endWall()` en `cliffAt().wall`.
