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

## Arena-modus

De knop Sandbox in het menu opent eerst een keuzescherm (`menuSandbox`): de vrije sandbox
(`startSandbox(false)`) of de arena-modus (`startSandbox(true)`, vlag `sbArena`). De arena is de
gewone sandbox met drie verschillen: het veld, de levens en de spawner.

Het veld (`sbArenaVeld`, uit `restart` zodra `sbArena` aan staat, voor `sbArenaReset`) is de arena van de
koning (Valse Koning 8, `bandArenaStart`) na de aankomst, maar zonder takel: Amir begint meteen midden op
de vloer met de speer in de hand. Het hergebruikt het arena-object: `arenaAap = {ban: true, sb: true,
staging: false, fase: 'vrij', c, links, rechts, ...}` met dezelfde `span` als `arenaMidden()`, zodat
`arenaAchtergrond` de twee grijze zijwanden tekent, `arenaCam` en `updateCamera` de camera vast in het
midden zetten (hij schuift niet met Amir mee, dus de wanden staan stil) en de hoofdlus Amir tot aan de
schermranden klemt (`arenaVast()`: `A.ban && !A.staging`, dezelfde test als de bandiet-arena, nu ook zonder
`level.bandArena`). De vlag `sb` laat `arenaTick` en `arenaHudTeken` eruit stappen: de golven en de teller
komen uit deze sectie. `sbArenaMaat` zet de twee rotsrichels hoog tegen de wanden, verankerd aan de
schermranden zoals in `bandArenaTick` (links lager en groter, rechts hoger en kleiner), en de echte
rechtergrens `level.rechtsWall` ver voorbij de schermrand, zodat een vijand van rechts buiten beeld kan
beginnen (links is er geen klif, `endWall` is -oneindig); de knoppen Uitzoomen roepen `sbArenaMaat` opnieuw
aan. Het uitzicht is `sbLagen = 'hoogland'`. `stopSandbox` haalt het veld weg (`arenaReset`), en de knoppen
Arena aan/uit onder Goudaap en Bandiet doen in de arena-modus niets (de arena staat al).

Omdat de camera vast staat rekent "net buiten beeld" en "in beeld" om het arena-midden, niet om Amir:
`kijkMidden()` (het arena-midden in een vaste arena, anders `world`) in `sbArenaSpawn`, `hyBuitenBeeld` en
`slangInBeeld`. Buiten een vaste arena verandert daar niets.

Klappen kosten levens (`hurtPlayer` slaat de sandbox-uitzondering
over als `sbArena` aan staat, en het levens-element staat aan) en er loopt een spawner. Die zit in de
sectie "arena-modus: golven vijanden in de sandbox", naar het voorbeeld van de bandietgolf
(`updateBandietGolf`): `SB_ARENA_SOORTEN` is de lijst soorten met hun standaardwaarden, `sbArenaCfg`
de instellingen (`aan`, `ramp`, `kant`, en per soort `aan`, `van`, `tot`, `max` en de aflopende klok `t`).
`sbArenaUpdate(dt)` laat per aangezette soort de klok lopen zolang `sbArenaLevend(k)` onder `max` zit, en
zet bij nul via `sbArenaSpawn` een vijand net buiten beeld (`W / 2 / viewZoom() + 320`) neer met
`sbSpawn(k, kant, x)`, zodat de knoppen onder Vijanden (dolk, elite, AI, klimmen) ook hier gelden.
Het interval krimpt lineair van `van` naar `tot` over `ramp` seconden. `sbArenaReset` zet de klok
en de teller op nul (en spreidt de eerste klok per soort, zodat niet alles tegelijk komt); `restart`
roept hem aan als `sbArena` aan staat, dus R na de dood begint de golven meteen opnieuw.
`vijandDood` telt de kills (`sbArenaKill`), `sbArenaHudTeken` tekent de teller in beeld: de klok groot
(48 px) in het midden bovenin, daaronder klein de kills, de opbouw en de beste tijd (`sbArenaBest`, in
`localStorage` onder `amir.arenaBest`, bijgewerkt in `sbArenaDood` zodra `sbArenaUpdate` de dood ziet,
een keer per potje via `doodGemeld`).

Het tabblad Arena (`data-cat="arena"`, knop `#sbarenatab`) staat alleen in de arena-modus aan; de
rijen per soort bouwt de code zelf in `#sbarenalijst` (een knop plus drie `<input type=number>`). De
invoervelden geven na een wijziging de focus terug aan het canvas (`typing` in de toetsafhandeling
laat de toetsen in een invoerveld toch al met rust). In de vrije sandbox opent het paneel niet op het
onthouden tabblad Arena (`sbCat('vijanden')`).

De sandbox begint op `sbView = 0.8` (de knop Licht onder Beeld en geluid staat dan aan), zoals een nieuw
level. De testbalk met schuifjes (`#bar`) begint in de sandbox ingeklapt; het pijltje `#barpijl` onderin
het midden van `#stage` (alleen aan in de sandbox, `barPijlToon` zet de richting) klapt hem uit en in,
net als de B-toets. De schildbandiet heeft onder Vijanden twee knoppen, Moeilijk (`schildman`) en
Makkelijk (`schildman_makkelijk`, in `sbSpawn` `niveau: 'makkelijk'`); de arena telt ze apart op `niveau`.

De grote Start-knop midden in beeld (`#arenastart`, `sbArenaSchermBtn`) staat aan zolang de arena-modus
aan is, de golven niet lopen en Amir niet dood is (`sbArenaToon`); hij roept `sbArenaStart(true)`, die ook
het paneel dichtklapt (`sbKlap(true)`). Per soort is er `bij` (`+1` in de rij, `data-arenabij`): bij Start,
en na R via `sbArenaReset` als de golven nog aan staan, komt er meteen een van die soort (`sbArenaSpawn`)
en begint zijn klok op `van`, ook als de soort zelf uit staat.
