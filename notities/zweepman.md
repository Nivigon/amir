# De zweepman

`ZWM`, `ZWM_TOUW`, `makeZweepman`, `updateZweepman`, `hitZweepman`, `zwmTeken`, `zwmTouwStap`, `zwmRaakt`. Een testvijand
(regel 12: een gewone vijand, geen baas): een pezige, kale bandiet die laag en loerend op Amir af sluipt en een lage
zweepslag uitdeelt. Alleen in de sandbox (rij **Zweepman**, met **AI uit**) en in Test 58.

## Het gevecht

- **Rust en sluipen**: in zijn wacht wiegt hij (`idle`, 8 fps); ziet hij je (`zichtWaak`, zoals de schildman), dan sluipt
  hij op je af (`loop`, `ZWM.loopFps`, `ZWM.stap` idle-pixels per frame). Binnen `ZWM.houd` blijft hij staan. Keien en
  ravijnen houden hem tegen (`knockBlocked`, regel 7); hij vault niet.
- **De lage slag** (`slag`, op ms per frame, `ZWM.dur`): binnen `ZWM.aanval` (en verder dan `ZWM.min`) en op hetzelfde
  niveau (`kooiZelfdeHoogte`). Hij begint bij `ZWM.tellVan` (de eerste frames van de clip zijn lang grijnzen). De tell: hij
  draait zijn borst naar je toe en grijnst; tot `ZWM.pantserVan` onderbreekt een treffer de slag, daarna zet hij door. Vanaf
  `ZWM.slagVan` is de zweep een touw in code; op `ZWM.knal` knalt hij (een flitsje, een ruisknal in Web Audio
  `zwmKnalGeluid`, een kleine schok). De zweep raakt van `ZWM.gevaarVan` tot `ZWM.gevaarNa` s na de knal, en alleen het
  stuk dat lager is dan `ZWM.laagH` boven de grond (`zwmRaakt`, elk touwpunt tegen Amirs vak): springen helpt, bukken niet.
- **Het herstel** (`herstel`, `ZWM.herstel` s): de spreidstand met zijn rug naar je toe, de zweep gestrekt op de grond. Dit is
  het raam om te straffen. Daarna de terugweg (`terug`, `ZWM.terugFps`, tot `ZWM.terugTot`) en `ZWM.cool` rust.
- **Geraakt**: drie treffers (`ZWM.hp`, met de health-balk), een witte flits, een korte hitstop en een terugstoot. Dood: een
  witte flits en wegvagen (`ZWM.vervaag`), `banSterf` en `vijandDood`. Een flinch en een echte dood zijn er nog niet.

## Het touw

`ZWM_TOUW` (de instellingen uit de proefpagina): een ketting van 30 punten (verlet, 240 stapjes per seconde) in de eigen
ruimte van de zweepman (idle-pixels, anker (0,0) op de grond, naar links kijkend). De wortel is het eind van het handvat in
zijn vuist (`zwmWortel`): de hand komt per frame uit de json (`hand`, vuist en richting) en wordt tussen twee frames
ingeschoven (`zwmHand`). In de slag trekt de punt een boog (`boog` graden, `kracht`) naar laag voor hem; na de knal hangt hij
uit de hand en ligt hij gestrekt (`liggen`). In de laatste frames zit zijn hand achter zijn dij (`achter` in de json): dan
tekent het touw achter het lijf. Getekend als vloeiende, taps toelopende lijn met zwarte rand en een gevlochten streep.

## De lagen

`enemies/zweepman/zweepman.json` en `lagen/`: per beweging (`idle`, `loop`, `slag`, `terug`) per frame `lijf` en `zweep`,
elk `{src, dx, dy, w, h}` t.o.v. het anker (midden tussen de voeten) en de grondlijn, in idle-pixels (de gehurkte figuur is
`ZWM.fig` = 313 hoog; getekend op `ZWM.hShare` van Amirs hoogte, `zwmScale`). `zweep` is Grok's opgerolde zweep als losse
laag in leerkleur (rust, lopen, tell, terugweg); in de slag en het herstel tekent het touw. Alle lagen kijken naar links.
Lui geladen (`zwmLaad`, `zwmLaadLevel` in `laadLevel`, vrijgegeven in `laadVrij`, `warmBouw`). Geen kleine set
(de bron is al klein, ~313 px). Ongeveer 120 MB uitgepakt.

Gemaakt uit Grok-clips (idle, sluipen, de lage slag en de terugweg), gekeyd en opgeschoond in de chat; de werkwijze staat in
het project (`claude/zweepman_overdracht.md`). De zweep is fel groen gegenereerd en overal weggekeyd.

## Nog te doen

De hoge slag (kruipen), de vangst (de zweep om je speer, touwtrekken), arm eraf en berserk, de knie-fase, een flinch en de
echte dood.
