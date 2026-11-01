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

## Laag en hoog zien

Beide slagen begonnen met dezelfde boog over zijn hoofd: de lage viel van boven op Amir, en de hoge zakte precies op de
knal al naar de grond (de `liggen`-kracht begint op de knal). Nu:

- **Laag**: de boog loopt via omlaag (`boogVan` 40, `boog` -125) en trekt hard naar de grond (`kracht` 3,5, `wExp` 0,8): de
  zweep veegt over de grond en komt nooit boven zijn hand. Een zandspoor achter de punt (alleen onder `ZWM_FX.laagOnder`),
  stofwolkjes waar het touw snel over de grond gaat, en op de knal een plof stof.
- **Hoog**: `strak` in `ZWM_SLAG.hoog`: vanaf `van` frames voor de knal tot `na` s erna trekt de punt veel harder
  (`kracht` 7, `wExp` 0,6, `boog` 105) en blijft `prog` onder 1, dus geen `liggen` en geen doorzakken: de zweep staat
  gestrekt op hoofdhoogte zolang hij kan raken.
- **De gloed** (`ZWM_FX.gloed*`, in `zwmTouwTeken`): warm licht onder het touw (`lighter`), feller waar het snel gaat, zodat
  je de zweep ook tegen een drukke achtergrond ziet.
- **De knal**: een lichtflits op de punt (een radiaal verloop) met `vonken` korte vonken in de slagrichting (`s.knalRicht`,
  vastgezet op de knal). Eerst was het een ster met acht stralen plus een ring, en dat leek op een wieltje.
- **De waarschuwing** (`zwmWijsTeken`, `ZWM_FX.wijs*`): tijdens de tell gloeit de plek waar hij gaat slaan, achter hem
  getekend, zacht pulserend. Laag een warme koepel van licht op de grond, hoog een lichte band op hoofdhoogte. Hij komt op
  van `tellVan` tot `slagVan` en dooft in `wijsNa` s na de knal.
- De knal is `sounds/zweepslag.mp3` (een echte zweepklap, de stilte ervoor eraf), zachter op afstand (`takelPan`).

Het spoor en het stof lopen op speltijd (`zwmSpoorStap` in de update, `zwmFxAchter` bij het tekenen).

## Testopties (pauze, Instellingen, Zweepman: test)

`ZWM_TEST`, bewaard in `localStorage` onder `amir.zweep`; de knop staat er alleen in een level of sandbox met een
zweepman (`zwmTestKnopToon`).

- **Rode laag** (`zwmRoodTeken`): een brede rode band achter de hele zweep, fel rood waar hij op dat moment kan raken
  (`zwmGevaar` en `zwmRaaktHoogte`, dezelfde regels als `zwmRaakt`), en een rode stippellijn op de raakhoogte (`laagH` of
  `hoogMin`).
- **Tempo tijdens de slag** (5 tot 100%): de hele wereld vertraagt zolang een zweepman slaat of in zijn herstel ligt
  (`zwmTraagNu`, na `gameTempo` in de lus).
- **Slag**: wissel, laag of hoog (gaat boven `ZWM.hoogKans`; de sandboxknop `slagVast` gaat er weer boven).
- **Gloed op de zweep** en **Waarschuwing vooraf**: aan of uit (`ZWM_TEST.gloed`, `ZWM_TEST.wijs`, standaard aan), om te
  vergelijken.

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

## Fase 2: de arm eraf (`fasen: true`, Test 59)

Alleen met `fasen: true` in de spawn (Test 59), of in de sandbox met **Fasen aan** (nieuwe zweepmannen) en **Arm eraf**
(de zweepmannen die er staan gaan meteen door). Alles staat in `ZWM2` en de sectie "de zweepman, fase 2".

- **Fase 1** duurt `ZWM2.hp1` (2) treffers. De laatste start `zwmArmEraf`: witte flits, hitstop en de set `armeraf`.
- **De arm** (`s.arm`, `zwmArmStap`, `zwmArmTeken`): vanaf frame `los` van `armeraf` hangt de losse arm
  (`lagen/f2_arm.png`, met draaipunt `px, py`, hoek `th0` en lengte `L`) aan de stomp en slingert hij achter het lijf.
  Na `ZWM2.armHang` s scheurt hij los, valt hij, kiept hij plat (0 of 180 graden) en blijft hij `armLig` s op de wereld
  liggen. Daarna vervaagt hij. Uit de stomp druppelt bloed op de grond.
- **De wond** (`zwmWondTeken`): een rode ellips met een bot, op `fr.stomp` van elk frame. In `mep`, `sprong`, `sprongterug`,
  `rustin` en `rust` komt die stomp uit de gele zone van de clip. In `armeraf` en `lach` rekent `postfix_f2.py` hem uit vanaf het
  vest (de baardregel pakte soms zijn kin).
- **De cyclus** (`ZWM2.cyclus`): `lach` (een keer), dan steeds `mep` (een gewone slag plus een backhand, de zweep is het touw,
  het raakt op elke hoogte en slaat Amir `mepDuw` weg), twee keer `sprong` plus `sprongterug`, en dan `rustin`, `rust`
  (`rustDuur` s in een lus) en `rustuit` (`rustin` achteruit). Bij `mep`, `sprong` en `rustin` draait hij naar Amir.
- **De sprong** heeft zijn verplaatsing in de frames zelf: het lijf schiet zo'n 340 idle-px vooruit en komt dan terug, netto
  `verschuif` (-72) na `sprongterug`. Staat Amir verder dan `sprongBereik`, dan schuift hij in de sprong nog tot `sprongExtra`
  extra op. Het touw begint pas bij index 27 (daarvoor ligt de rol over zijn achterbeen en zit hij als leer in het plaatje).
  Het gevaar geldt van het begin van het touw tot `gevaarNa` s na de knal (`sprongGevaar`), want bij de knal is hij al
  doorgedraaid.
- **De dood** (`zwmDoodStap`, `s.dood`): de dodelijke treffer geeft de doodskreet (`banSterf`) en een hitstop. Hij
  bevriest `ZWM2.doodVries` s in zijn uitrust-houding en valt dan met de Grok-val (de set `dood`, 26 frames uit
  `export_dood.py`, vanaf rustframe 90): een kwartslag naar de camera, de knieen begeven het en hij zakt in elkaar, steeds
  sneller. Op frame `land` komen een schudding en stof, en `pof.voor` frames eerder de plof (`sounds/bavland.mp3`, zacht).
  Na `doodLig` s liggen vervaagt hij. (Een stijf omkiepen in code is geprobeerd en afgekeurd.)
- **Kwetsbaar** (`zwmF2Kwetsbaar`): alleen in `rustin`, `rust` en `rustuit`, zodat de val altijd in die houding begint.
  Daarbuiten ketst je speer af (de houtklap, een korte flits). `ZWM2.hp2` (2) treffers en hij is dood.
- **Het touw per segment**: `set.touw` is een lijst `{van, knal, tot, boogVan, boog, kracht, hang, blijf}`. In een segment volgt
  het touw de hand (`fr.hand`), met de boog uit dat segment (`s.f2C` in `zwmTouwStap`). Aan het eind vervaagt het, behalve met
  `blijf`. Daarbuiten zit de zweep als leer in het plaatje.
- **Het raakvak** volgt zijn voeten (`zwmLijfDX`, uit `fr.cx`), want in de sprong staat hij ver van zijn ankerpunt.
- **Laden**: de f2-plaatjes (zo'n 114 MB groot) laden pas als er een zweepman met fasen is (`zwmLaadF2`, `zwmF2Wil`).

De frames komen uit `export_f2.py` en `postfix_f2.py` in de chat (de Grok-clips 1armhit, 1armlaugh, manischslag, draaislag,
de sprong, de terugweg en uitrusten2), op dezelfde schaal en hetzelfde anker als fase 1.

## Nog te doen

- In fase 2 laten de touwframes van de mep en het eind van de sprong nog kleine reepjes broek los waar de zweep over zijn
  benen ging (de bron is daar vlekkerig).
- Berserk: de speer uit de lucht slaan. Fase 3: het been eraf, op zijn knie, de laatste klap of een executie.

- De lage slag begint nog op hoofdhoogte, omdat zijn arm in de Grok-clip over zijn hoofd zwaait; de zweep zelf blijft
  laag. Een clip waarin hij van onderen of opzij uithaalt (de hand onder de heup) maakt het helemaal zuiver.

De vangst (de zweep om je speer, touwtrekken) en een flinch.
