# De zweepman

`ZWM`, `ZWM_TOUW`, `makeZweepman`, `updateZweepman`, `hitZweepman`, `zwmTeken`, `zwmTouwStap`, `zwmRaakt`. Een testvijand
(regel 12: een gewone vijand, geen baas): een pezige, kale bandiet die laag en loerend op Amir af sluipt en een lage
zweepslag uitdeelt, laag of hoog. Alleen in de sandbox (rij **Zweepman**, met **AI uit** en **Slag: wissel/laag/hoog**)
en in Test 58.

## Het gevecht

- **Rust en sluipen**: in zijn wacht wiegt hij (`idle`, 8 fps); ziet hij je (`zichtWaak`, zoals de schildman), dan sluipt
  hij op je af (`loop`, `ZWM.loopFps`, `ZWM.loopV` wereld-px/s, net als de andere vijanden en dus los van de schermhoogte;
  eerst was het 4,5 idle-pixels per frame, 42 px/s op een laptop en 23 op een telefoon). Binnen `ZWM.houd` blijft hij staan. Keien en
  ravijnen houden hem tegen (`knockBlocked`, regel 7); hij vault niet.
- **Twee slagen** (`ZWM_SLAG`, per slag de set, de terugweg, de frametijden, de knal en de boog van de punt); hij kiest
  willekeurig (`ZWM.hoogKans`), of vast met `s.slagVast` (de sandboxknop **Slag**). De tell zegt welke: **laag** = zijn
  borst naar je toe en grijnzen, **hoog** = hij komt omhoog met zijn rug naar je toe en de zweep boven zijn hoofd.
- **De hoge slag** (`hoog`, terugweg `hoogterug`): de zweep slaat over zijn hoofd naar hoofdhoogte; alleen het stuk hoger dan
  `hoogMin` raakt (gebukt is Amir zo'n 237 idle-pixels hoog), dus bukken of kruipen gaat eronderdoor. De punt trekt harder
  (`wExp`, `kracht`), zodat de zweep op hoogte blijft in plaats van door te zakken.
- **De lage slag** (`slag`, op ms per frame): binnen `ZWM.aanval` (en verder dan `ZWM.min`) en op hetzelfde
  niveau (`kooiZelfdeHoogte`). Hij begint bij `tellVan` (de eerste frames van de clip zijn lang grijnzen). De tell: hij
  draait zijn borst naar je toe en grijnst; tot `pantserVan` onderbreekt een treffer de slag, daarna zet hij door. Vanaf
  `slagVan` is de zweep een touw in code; op `knal` knalt hij (een flitsje, een ruisknal in Web Audio
  `zwmKnalGeluid`, een kleine schok). De zweep raakt van `gevaarVan` tot `ZWM.gevaarNa` s na de knal, en alleen het
  stuk dat lager is dan `laagH` boven de grond (`zwmRaakt`, elk touwpunt tegen Amirs vak): springen helpt, bukken niet.
- **Het herstel** (`herstel`, `ZWM.herstel` s): de spreidstand met zijn rug naar je toe, de zweep gestrekt op de grond. Dit is
  het raam om te straffen. Daarna de terugweg (`terug`, `ZWM.terugFps`, tot `terugTot`) en `ZWM.cool` rust.
- **Geraakt**: drie treffers (`ZWM.hp`, met de health-balk), een witte flits, een korte hitstop en een terugstoot. Dood: een
  witte flits en wegvagen (`ZWM.vervaag`), `banSterf` en `vijandDood`. Een flinch en een echte dood zijn er nog niet.

## Het ritme

Afgesteld op ongeveer 1 s van het begin van de slag tot de knal en zo'n 3,4 s van slag tot slag (eerst 1,3 s en 4,8 s):

- **Laag**: tell 0,42 s, opzwaai 0,29 s, slag 0,25 s (`dur` in `ZWM_SLAG.laag`); **hoog**: 0,46, 0,36 en 0,21 s.
- Daarna `ZWM.herstel` 0,5 s, de terugweg op `ZWM.terugFps` 18 (laag 1,2 s, hoog 0,9 s) en `ZWM.cool` 0,6 s rust.
- Alle tijden lopen op `gameTempo` (het tempo uit de instellingen), net als bij de andere vijanden.

## Zijn stem

`ZWM_STEM`, `zwmZeg`, `zwmStem` (lui gemaakt in `zwmLaad`, weg in `laadVrij`). Drie geluiden in `sounds/`:

- `zweeplach.mp3`: als hij in beeld komt (`s.geroepen`), en na een treffer op Amir soms (`raakLach`).
- `zweepcomehereboy.mp3`: als hij je achterna gaat sluipen en je verder dan `komVer` keer zijn aanvalsafstand staat (`komKans`).
- `zweepfeelmyhurt.mp3`: als zijn zweep je raakt (`raakVoel`), en soms al bij het begin van de slag (`tellVoel`).

Na elke zin zwijgen alle zweepmannen samen `ZWM_STEM.rust` s. "Come here boy" en "feel my hurt" zijn geknipt uit
een opname met beide zinnen (tot 1,46 s en vanaf 1,84 s, met een korte fade), zodat ze los te spelen zijn.

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
Lui geladen (`zwmLaad`, `zwmLaadLevel` in `laadLevel`, vrijgegeven in `laadVrij`, `warmBouw`). Een kleine set via
`gen-klein.py` (`enemies/zweepman/lagen`, drempel 60, `KLEIN_FAM`). Ongeveer 173 MB uitgepakt op de grote set, een kwart
daarvan op de kleine.

Gemaakt uit Grok-clips (idle, sluipen, de lage slag en de terugweg), gekeyd en opgeschoond in de chat; de werkwijze staat in
het project (`claude/zweepman_overdracht.md`). De zweep is fel groen gegenereerd en overal weggekeyd.

## Nog te doen

- `sounds/zweepslag.mp3` (een echte zweepklap, de stilte ervoor eraf geknipt zodat de klap meteen komt) vervangt de
  ruisknal `zwmKnalGeluid` op de knal. Staat klaar, nog niet ingebouwd.
- De zweep laag en hoog duidelijk anders laten zien (mock-up in de chat): laag veegt hij over de grond met een zandspoor
  en stof en knalt hij op enkelhoogte; hoog trekt hij rond de knal recht op hoofdhoogte met een witte zwiep. Nu zakt de
  hoge zweep op de knal al naar de grond (de liggen-kracht begint op de knal), en komt de lage van boven.

De vangst (de zweep om je speer, touwtrekken), arm eraf en berserk, de knie-fase, een flinch en de
echte dood.
