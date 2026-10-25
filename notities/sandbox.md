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
gewone sandbox met vier verschillen: het veld, de levens, de spawner en het paneel (de wizard, zie hieronder).

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
Valse Koning 8); `restart` vult de rug, en de knop Rug (in de wizard, pagina 2) zet het anders. Daarnaast twee wandfakkels
(`level.fakkels`, gezet in `sbArenaMaat`, gemerkt `arena: true` zodat een fakkel uit de knop Decor, Fakkel
blijft staan): een aan elke rotswand onder de richel, `fakkelX` Amir buiten de wandlijn (daar staat de rots)
op hoogte `fakkelY`; ze laden lui via de tekenlus (`fakkelLaad`).

Omdat de camera vast staat rekent "net buiten beeld" en "in beeld" om het arena-midden, niet om Amir:
`kijkMidden()` (het arena-midden in een vaste arena, anders `world`) in `sbArenaSpawn`, `hyBuitenBeeld` en
`slangInBeeld`. Buiten een vaste arena verandert daar niets.

Klappen kosten levens (`hurtPlayer` slaat de sandbox-uitzondering
over als `sbArena` aan staat, en het levens-element staat aan; ook de beet van de fosforslang, `fosforBijt`), tenzij
Onsterfelijk aan staat (zie hieronder), en er loopt een spawner. Die zit in de
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

De rijen per soort bouwt de code zelf in `#sbarenalijst` (een knop plus drie `<input type=number>`), in het
tabblad Arena (`data-cat="arena"`); dat tabblad en zijn knop `#sbarenatab` blijven altijd verborgen, want in de
arena-modus staat alles in de wizard. De invoervelden geven na een wijziging de focus terug aan het canvas (`typing`
in de toetsafhandeling laat de toetsen in een invoerveld toch al met rust). In de vrije sandbox opent het paneel niet
op een onthouden tabblad Arena (`sbCat('vijanden')`).

De sandbox begint op `sbView = 0.8` (de knop Licht onder Beeld en geluid staat dan aan), zoals een nieuw
level. De testbalk met schuifjes (`#bar`) begint in de sandbox ingeklapt; het pijltje `#barpijl` onderin
het midden van `#stage` (alleen aan in de sandbox, `barPijlToon` zet de richting) klapt hem uit en in,
net als de B-toets. De schildbandiet heeft onder Vijanden twee knoppen, Moeilijk (`schildman`) en
Makkelijk (`schildman_makkelijk`, in `sbSpawn` `niveau: 'makkelijk'`); de arena telt ze apart op `niveau`. Daarnaast
AI uit, Dood (de gewone dood, Dood laag: `schbSterf(s, 'steek')`), en voor de executie (zie `notities/schildbandiet.md`): **Executie: kans/altijd**
(`sbExeAltijd`, elke steek- en worp-kill wordt een executie), **Wankel: E aan/geen E** (`sbExeGeenE`, de worp-kill eindigt
dan in de val), en **Steek-kill** en **Worp-kill** (`sbExeNu`, de eerste levende schildbandiet meteen zo doden).

De grote Start-knop midden in beeld (`#arenastart`, `sbArenaSchermBtn`) staat aan zolang de arena-modus
aan is, de golven niet lopen, Amir niet dood is en de wizard dicht is (`sbArenaToon`); hij roept `sbArenaStart(true)`. Per soort is er `bij` (`+1` in de rij, `data-arenabij`): bij Start,
en na R via `sbArenaReset` als de golven nog aan staan, komt er meteen een van die soort (`sbArenaSpawn`)
en begint zijn klok op `van`, ook als de soort zelf uit staat.

### De wizard: de opzet van de arena

In de arena-modus is het oude paneel met de tabbladen weg. `#sandbox` krijgt de klasse `arena` (de CSS verbergt
dan al zijn kinderen behalve `#arenawiz` en maakt het een laag over het hele beeld), en `on` staat alleen aan
zolang de wizard open is (`sbWiz.open`). Het paneel is halfdoorzichtig (de arena schemert erdoor) met een rand van
rots (lagen gradient op `border-box`) en een warme goudgloed (`box-shadow`); `body.touch` en `max-height: 430px`
maken het krapper voor een liggende telefoon (852x393).

Drie stappen (`sbWiz.pagina`, `.awpagina[data-pagina]`, de stappenrij `.awstappen`): **1 Monsters**, **2 Arena en
regels**, en **3 Klaar**, dat is de wizard dicht met de grote Start. Verder en Terug lopen erdoor (`sbWizToon`).

De knoppen zijn de bestaande elementen, niet dubbel gebouwd: `SB_WIZ_PLAATS` zegt per element (of met `true` zijn
hele `.row`) naar welk vak (`data-wiz`) in de wizard het gaat. `sbWizInrichten` (in `startSandbox(true)`) zet een
commentaar op de oude plek en verhuist het element; `sbWizOpruimen` (in `startSandbox(false)` en `stopSandbox`) zet
alles terug. De handlers blijven dezelfde, en omdat de wizard binnen `#sandbox` staat vinden de `sandboxEl.querySelectorAll`
van de Toon-functies (view, lagen, weer, muziek) ze nog. De vrije sandbox ziet dus precies het oude paneel.
Pagina 1: `#sbarenamodus`, `#sbarenakant`, de hint, `#sbarenastroomrij`, `#sbarenagolfrij`, `#sbarenalijst`, en per
soort het gedrag uit Vijanden (bandiet: AI, dolk, vault, elite, duin, bloed, spuit; slangen: klimmen; schildbandiet:
AI, executie, wankel; meelman en kooiman: AI, vogel, duel; allemaal: health-balk, zicht). Pagina 2: de kaartjes met
de arena's (`SB_ARENA_PLEKKEN`, nu alleen `koning`; `sbArenaCfg.veld`), Onsterfelijk (`#awonst`), Kalebassen
(`#awkal`, `#awkalelke`), Ruimte, en uit Speer en spullen en Beeld en geluid: worp, rug, renstoot, lage zwaai, de
drie tribe-rijen, uitzoomen, tijd van de dag, weer en muziek. Onderin Opnieuw en Terug naar menu.

Openen: `sbWizOpen(1)` bij de start van de arena-modus, met **Esc** (de toetsafhandeling kiest in de arena-modus de
wizard in plaats van het pauzemenu, tenzij dat al open is) of het knopje `#arenaopzet` linksboven (`sbArenaOpzetBtn`,
aan zolang de wizard dicht is). Open zet `paused` (de spawner, de afteller en de klok staan dan stil) en onthoudt de
opzet (`sbWizOpzet`: modus, arena en per soort aan en +1). `sbWizSluit` haalt de pauze weg en roept `restart()` (zoals
R) als er een potje liep en de opzet veranderde; anders gaat het verder waar het was. De focus gaat dan van de wizard
af, zodat de toetsen weer naar het spel gaan.

Onthouden: `sbArenaBewaar` schrijft bij elke klik of wijziging in de wizard (en bij sluiten) `amir.arenaCfg` in
`localStorage`: de eigen waarden van de arena (modus, ramp, kant, golf, per soort, veld, onst, kal, Ruimte) en van
elke verhuisde knop zijn tekst en `on` (`sbWizKnoppen`, zonder de doe-knoppen in `SB_WIZ_DOE`). `sbArenaLaadCfg` (in
`startSandbox(true)`, na de standaardwaarden) zet de waarden terug en klikt de knoppen tot tekst en `on` kloppen; een
knop uit een groep (`data-rug`, `data-view`, ...) alleen als hij aan stond. `flashHint` is dan even stil.

### Onsterfelijk

`sbArenaCfg.onst`, standaard aan, de knop `#awonst`. Het is niet `godMode` (die laat de klap helemaal niet landen):
`onsterfelijk()` geeft in de sandbox `sbArena && sbArenaCfg.onst`, en `hurtPlayer` en `fosforBijt` trekken dan geen
leven af (en Feign Death vangt niets), maar de schrik, de knockback, `invuln`, `shake` en het raakgeluid blijven.
`woedeGloed` geeft zolang hij aan staat dezelfde vlam als de woede van Blood Rush, zodat Amir gloeit. `onstOoit`
(gezet in `sbArenaUpdate` zodra hij aan staat terwijl een potje loopt, op nul in `sbArenaReset`) houdt het potje
buiten de records: `sbArenaDood` en `sbGolfVolgende` werken `amir.arenaBest` en `amir.arenaBestGolf` dan niet bij, en
`sbArenaHudTeken` zet de beste tijd grijs met "(onsterfelijk, telt niet)".

### Kalebassen

`sbArenaCfg.kal = { aan, golven, stroom }`: elke zoveel golven (de golven) of seconden (de stroom), een getal per
modus in hetzelfde invoerveld. `sbKalStap` telt (de stroom in `sbArenaUpdate` met `dt`, de golven met 1 als een golf
verslagen is in `sbGolfUpdate`) en zet `kalKlaar`. `sbKalLijken` ziet elke beeld wie net gestorven is (een vijand die
`sbLeeft` was en nu niet meer, gemerkt met `o.sbLeeft`) en laat bij `kalKlaar` de gewone drinkkalebas vallen op zijn
plek (`dropHppotion`, geklemd in beeld), waarna de teller opnieuw begint. Ook met Onsterfelijk aan. `sbArenaReset`
(R) zet de teller terug; `restart` ruimt de liggende kalebassen op (`resetHppotions`). De teller zegt "Kalebas bij de
volgende" zolang er een klaarligt.
