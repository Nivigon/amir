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
gewone sandbox met twee verschillen: klappen kosten levens (`hurtPlayer` slaat de sandbox-uitzondering
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
