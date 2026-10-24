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
aan. `stopSandbox` haalt het veld weg (`arenaReset`), en de knoppen
Arena aan/uit onder Goudaap en Bandiet doen in de arena-modus niets (de arena staat al).

Ruimer dan de echte arena, op dezelfde maat (`SB_ARENA_VELD`): de zijwanden worden dunner getekend
(`wandSchaal` 1,3 op het arena-object, `arenaAchtergrond` leest `A.wandSchaal || ARENA.wandSchaal`; de
goudaap-arena houdt 1,85 voor de hangers), de richels zitten daarom iets dieper in de rand (`richelDiep`,
0,55 Amir in plaats van 1), en de verre lagen schuiven een klein stuk met Amir mee (`parallax` 0,08): `scene`
verschuift `world` (tijdens het tekenen de camera) richting `camSwap` (Amir) voor de lucht, de bergen en de
bomen, en zet hem terug voor `arenaAchtergrond` en de grond, zodat de wanden, de vloer en alles erop stil
staan. Het uitzicht blijft het gewone avonduitzicht (`sbLagen = ''`): de lage einder voelt opener dan het
hoogland van Valse Koning 8. Dit zijn de suggesties 2, 3 en 4 uit het overleg; de wanden op de schermrand
(1) is bewust niet gedaan, zodat de arena even breed blijft als de echte.

De ruimte (`SB_ARENA_VELD.ruimte`, 0,6 Amir, de knop **Ruimte** op het tabblad Arena, `sbArenaRuim`, standaard aan):
de arena is aan elke kant zoveel breder dan het beeld. `sbArenaMaat` zet het in px op het arena-object (`A.ruimte`)
en legt de richels en `rechtsWall` aan de arenarand (schermrand plus ruimte) in plaats van de schermrand. De klem in
de hoofdlus (`arenaVast`) laat Amir tot die arenarand, en `arenaCam` geeft voor de bandiet-arena het midden plus
`arenaRuimDrift(p)`: de camera schuift evenredig met Amir mee, `(p - c) * r / (halfVis + r)`, geklemd op `±r`, zodat
de wand aan zijn kant precies op de schermrand staat als hij ertegenaan staat en de andere wand net uit beeld is.
`kijkMidden` geeft dan het midden plus die drift (de echte camera), zodat "net buiten beeld" in `sbArenaSpawn`,
`hyBuitenBeeld` en `slangInBeeld` om het beeld rekent en niet om het arena-midden. Zonder het veld (Valse Koning 8,
de goudaap-arena) is `arenaRuimte()` 0 en verandert er niets: de camera staat stil in het midden. De boss-klem
`arena.c ± arenaHalf()` in de hoofdlus slaat een vaste arena over (`!arenaVast()`), want die klemt zelf al tot haar
rand; voor Valse Koning 8 was die tweede klem toch al ruimer dan de eerste.

De arena-modus geeft Amir altijd 1 reservespeer op de rug (`startSandbox`: `RUG_MAX = sbArena ? 1 : 0`, zoals
Valse Koning 8); `restart` vult de rug, en de knop Rug onder Speer en spullen zet het anders. Daarnaast twee wandfakkels
(`level.fakkels`, gezet in `sbArenaMaat`, gemerkt `arena: true` zodat een fakkel uit de knop Decor, Fakkel
blijft staan): een aan elke rotswand onder de richel, `fakkelX` Amir buiten de wandlijn (daar staat de rots)
op hoogte `fakkelY`; ze laden lui via de tekenlus (`fakkelLaad`).

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
**De afteller** (`SB_AFTEL`, `sbAftelStart`, `sbAftelUpdate`, `sbAftelTeken`, `sbArenaGo`): Start bij een vers
begin (stroom: `t0 === 0`, golven: `g.nr === 0`) en `sbArenaReset` met de arena aan (R) zetten eerst
`sbArenaCfg.aftel` op `{t, tel, go}`. `sbAftelUpdate` (bovenaan `sbArenaUpdate`, dus stil in de pauze) telt
van `van` (3) af, `stap` seconden per cijfer, elk met `sbAftelPiep(false)` (een driehoekstoon van `piepHz`),
en gaat na het laatste cijfer op `go`: de lange hoge toon (`sbAftelPiep(true)`, `goHz`) en `sbArenaGo`. Zolang
hij aftelt staan de klok en de spawner stil. `sbArenaGo` laat de eerste vijand meteen komen: in de stroom de
soorten met `bij` (+1), en als geen soort +1 heeft de eerste die aan staat (`sbArenaSpawn(k, true)`); in de
golven `sbGolfVolgende` en meteen fase `golf` (de afteller was de aankondiging). `inBeeld` in `sbArenaSpawn`:
een spuwer (zwart, knock) komt niet aanlopen, dus die eerste begint op `SB_AFTEL.inBeeld` keer de halve
schermbreedte, in beeld, in plaats van 320 px erbuiten. `sbAftelTeken` (na `sbArenaHudTeken` in de tekenlus)
tekent het cijfer groot midden in beeld (`maat` keer H, op hoogte `y` keer H), zonder paneel: het komt op
`popVan` keer zijn maat en veert in `pop` seconden uit naar 1, vervaagt de laatste `uit` seconden van zijn tel,
room met een warme gloed en de donkere rand van de teller; na `go` nog `SB_AFTEL.go` seconden 'Los!' net zo.
Stop zet `aftel` op null; Start na Stop telt niet opnieuw af (geen vers begin). Zonder een aangezette soort
geen afteller, alleen de hint.

`vijandDood` telt de kills (`sbArenaKill`), `sbArenaHudTeken` tekent de teller in beeld: de klok groot
(48 px) in het midden bovenin, daaronder klein de kills, de opbouw en de beste tijd (`sbArenaBest`, in
`localStorage` onder `amir.arenaBest`, bijgewerkt in `sbArenaDood` zodra `sbArenaUpdate` de dood ziet,
een keer per potje via `doodGemeld`).

**Golven** (`sbArenaCfg.modus`, de knop `#sbarenamodus` wisselt tussen `stroom` en `golven`): in plaats van
de klok per soort komt een golf tegelijk. `sbGolfInhoud(nr)` bouwt de rij van golf `nr` uit elke soort die aan
staat en al meedoet (`nr >= vanaf`): `floor(n + plus * (nr - vanaf))` stuks, geschud. `sbGolfVolgende` begint
de volgende golf (fase `kondig`, `SB_GOLF_KONDIG` seconden "Golf n" groot in beeld, daarna `golf`), en slaat
een lege golf over (de rust loopt dan opnieuw, het nummer blijft staan). `sbGolfUpdate` laat de rij een voor
een binnenkomen (`golf.tussen` seconden ertussen, zolang `sbArenaLevendTotaal()` onder `golf.tegelijk` zit),
en gaat naar `rust` als de rij leeg is en alles dood; na `golf.rust` seconden de volgende. De hoogste golf
staat in `localStorage` onder `amir.arenaBestGolf` (`sbArenaBestGolf`). Stop laat de lopende golf staan,
Start gaat ermee door; R (`sbArenaReset`) begint bij golf 1. De drie invoervelden per soort zijn dezelfde
elementen in beide modi: `sbArenaToon` zet per modus welk veld erin staat (`SB_ARENA_VELDEN`: naam, grenzen,
stap en de kop erboven) en verbergt de +1 (bij start) in de golven; de rij met Opbouw hoort bij de stroom,
die met Rust, Tussen en Tegelijk bij de golven (`#sbarenastroomrij`, `#sbarenagolfrij`), en de hint
(`#sbarenahint`, `SB_ARENA_HINT`) legt de modus uit.

Het tabblad Arena (`data-cat="arena"`, knop `#sbarenatab`) staat alleen in de arena-modus aan; de
rijen per soort bouwt de code zelf in `#sbarenalijst` (een knop plus drie `<input type=number>`). De
invoervelden geven na een wijziging de focus terug aan het canvas (`typing` in de toetsafhandeling
laat de toetsen in een invoerveld toch al met rust). In de vrije sandbox opent het paneel niet op het
onthouden tabblad Arena (`sbCat('vijanden')`).

De sandbox begint op `sbView = 0.8` (de knop Licht onder Beeld en geluid staat dan aan), zoals een nieuw
level. De testbalk met schuifjes (`#bar`) begint in de sandbox ingeklapt; het pijltje `#barpijl` onderin
het midden van `#stage` (alleen aan in de sandbox, `barPijlToon` zet de richting) klapt hem uit en in,
net als de B-toets. De schildbandiet heeft onder Vijanden twee knoppen, Moeilijk (`schildman`) en
Makkelijk (`schildman_makkelijk`, in `sbSpawn` `niveau: 'makkelijk'`); de arena telt ze apart op `niveau`. Daarnaast
Nieuwe stijl (`schildman_lagen`), AI uit, Dood, en voor de executie (zie `notities/schildbandiet.md`): **Executie: kans/altijd**
(`sbExeAltijd`, elke steek- en worp-kill wordt een executie), **Wankel: E aan/geen E** (`sbExeGeenE`, de worp-kill eindigt
dan in de val), en **Steek-kill** en **Worp-kill** (`sbExeNu`, de eerste levende schildbandiet meteen zo doden).

De grote Start-knop midden in beeld (`#arenastart`, `sbArenaSchermBtn`) staat aan zolang de arena-modus
aan is, de golven niet lopen en Amir niet dood is (`sbArenaToon`); hij roept `sbArenaStart(true)`, die ook
het paneel dichtklapt (`sbKlap(true)`). Per soort is er `bij` (`+1` in de rij, `data-arenabij`): bij Start,
en na R via `sbArenaReset` als de golven nog aan staan, komt er meteen een van die soort (`sbArenaSpawn`)
en begint zijn klok op `van`, ook als de soort zelf uit staat.
