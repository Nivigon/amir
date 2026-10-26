# De schildbandiet

## de schildbandiet: loopt met zijn schild op en valt springend aan

`SCHB`, `makeSchildman`, `updateSchildman`, `hitSchildman`, `schbMik`, `schbSprongP`, `schbLand`. Het ritme van het gevecht, afgestemd met `tools/schildduel.js`: hij loopt op Amir af tot `houd` (1 Amir) en zet op `aanval` (2,1 Amir) de sprong in. De tell (frame 0..5, ~0,8 s) is tot `pantserVan` (3) te onderbreken; daarna zet hij door (een treffer kost schild maar onderbreekt niet). Tot `mikTot` (7, net na de afzet) stuurt hij bij naar Amir, zo dat zijn speerpunt (`speerVoor`, 0,62 Amir voor zijn midden) op Amir de grond in gaat; de sprong (6..16, ~0,57 s) is onaantastbaar en vloeit op de klok (`schbSprongP`). Hij raakt op 17..20 rond de punt (`speerR`) of onder zijn lijf (`lijfR`) en slaat Amir dan terug (`raakDuw`); de landing geeft een hitstop (`landStop`), schok en een zet die dichtbij harder is (`landDuw`). Het herstel (21..29, ~0,8 s) is het raam om te straffen. Een treffer geeft een korte hitstop (`raakStop`, `breekStop`) en een flinch die meteen begint (`flinchVan`) met een terugstoot (`flinchDuw`); vanaf `dekVan` in de flinch ketst je speer af (geen stunlock), en binnen `wraakT` slaat hij terug met een tell die al gepantserd is. Gemeten op 1280 bij 720: met 0,2 s reactie ontwijk je alles, met 0,35 s word je bij twee van de drie sprongen geraakt, blind steken of stilstaan kost meerdere levens; het gevecht duurt zo'n 8 tot 10 seconden. Dat is het niveau `moeilijk` (zonder veld). Met `niveau: 'makkelijk'` in zijn spawn (`SCHB_NIVEAU`, `schbN`, `schbDur`) heeft hij een langere tell, een tragere sprong en een langer herstel, mikt hij alleen tot de afzet, zet hij later door en slaat hij na een flinch niet gepantserd terug. Het tempo per niveau staat in `SCHB_TEMPO` (tell, aanval = sprong en inslag, herstel; hoger is sneller, `schbDur` deelt de frameduur erdoor en de sprong beweegt vanzelf mee) en is live af te stellen in de pauze onder **Schildbandiet: tempo** (`pzschb`, `SCHB_SCHUIF`, bewaard onder `SCHB_TEMPO_KEY`, de knop alleen in een level of sandbox met een schildbandiet, `schbTempoKnopToon`); aanval en herstel staan bij beide niveaus standaard op 150% (de tell op 100%). Bij het landen klinkt hetzelfde geluid als Amirs speerstoot (`schbLandGeluid`, `music/spearthrust.mp3`, eigen stemmen, verder weg zachter), niet meer het grondgeluid van de kooiman. De houtklap op het schild (`HOUT`, `houtRaak(toon, vol)`, `houtDuik`, `sounds/houtraak.mp3`) is de beloning van het gevecht en staat daarom boven de stoot: het bestand is genormaliseerd naar -1 dB (het zat 6 dB onder `spearthrust.mp3` en verdronk erin, zodat je bij een treffer geen hout hoorde), Amirs stoot (`#thrust`) duikt op de treffer naar `duik` (0,3; elke nieuwe stoot zet zijn volume zelf terug), elke volgende klap klinkt een slag lager (`toon` per schild dat er na de klap over is: 1, 0,93, 0,86, met `preservesPitch` uit zodat lager ook zwaarder is), de breuk (`houtBreek`) moet flink harder zijn en een element kan niet boven volume 1, dus hij speelt `breek.lagen` tegelijk (drie stemmen, 0,9, 0,65 en 0,5 in toon, samen zo'n 9 dB boven een losse klap) en `breek.na` (0,07 s) later `breek.nalagen` (twee lagere stemmen) als naklap, waarvoor de pool zeven stemmen heeft, en het afketsen als hij zich dekt (`dekVan` in de flinch) speelt `kets` (hoger, 1,25, en zachter, 0,6), zodat te horen is dat die treffer niet telde. `wiebel` (5%) strooit wat in de toon tegen het mitrailleurgevoel. Nagemeten in Chromium met een patch op `HTMLMediaElement.play`: elke schildtreffer speelt het bestand, met de stoot op 0,3 op dat moment. Het verstopte zegel gebruikt dezelfde tik via `houtRaak(1, .3)`. Met `achter` (px) start een spawn op hetzelfde moment als de spawn op zijn x, maar zoveel verder weg, zodat hij een tel later het gevecht in loopt: zo komen er twee na elkaar (werkt ook voor de bandiet en de kooiman). Test 45 is het proefstuk, Test 46 loopt op van een makkelijke via twee makkelijke en een moeilijke naar twee moeilijke, dan een bandiet met een moeilijke en een moeilijke met de kooiman (gespeeld met `tools/schildduel.js --level "Test 46"`: met 0,35 s reactie 0, 2, 2 en 4 keer geraakt); in de sandbox onder Vijanden. In de Maker nieuwstijl staat hij onder Vijanden als Schildbandiet met twee varianten: Moeilijk (`schildman`) en Makkelijk (`schildman:makkelijk`, wordt in `mkSpawn` `niveau: 'makkelijk'`)


## de schildstaat: het schild gaat zichtbaar kapot

`SCHB_STAAT`, `schbStaat`. Het schild heeft vier standen: 0 treffers `metschild`, 1 `fase1` (een hap eruit), 2 `fase2` (twee happen), 3 `zonderschild` (weg, daarna in een klap dood). `schbStaat` leidt de stand af uit `s.schild` en `s.metSchild`; omdat `hitSchildman` het schild al verlaagt voor de flinch begint, speelt de flinch meteen in de nieuwe stand en verschijnt de hap op het moment van de klap. Bij een gepantserde treffer (late tell) wisselt de strike midden in de animatie van stand; dat verspringt niet, want het lijf is in alle standen hetzelfde plaatje en alleen het schildplaatje wisselt (zie hieronder). Elke beweging (loop, strike, flinch) heeft in `lagen.json` alle vier de standen.

## de kleuren: het bandietpalet, de oude kleuren in bron/

De schildbandiet loopt in de kleuren van de bandiet: een marineblauw gewaad (de bandietjas), een donkerder marineblauwe
cape en een kaki-olijf broek; de rode sjerp, de huid, de schoenen, het schild en de speer blijven zoals ze getekend zijn.
De aangeleverde frames (blauw gewaad, paarse cape, groene broek) staan ongewijzigd in `enemies/schildbandiet/bron/`, met
dezelfde mappen als de speelversie (`lagen/lijf`, `lagen/schild`, `executie/lagen`), want die felle, losse kleurvlakken zijn
handig om later in een ander palet te kleuren. `tools/schildman_kleur.py` leest die bron en schrijft de speelversie, op de
manier van `tools/kooiman_kleur.py` (alleen tint en verzadiging per vlak, de lijnen en plooien blijven, en de magenta
randjes gaan eruit). De lagen van Amir in de executie (`amir_*.png`) staan niet in bron/ en blijven ongemoeid. Het spel en de manifest
laden bron/ nooit.

Het bandietpalet is vanaf nu de standaard. Een nieuwe export (nieuwe frames, een nieuwe submap, of een nieuwe versie over
een bestaand frame heen) zet je gewoon in de speelmap en dan draai je het script: `oude_kleuren` telt per frame de pixels
in het aangeleverde palet (fel blauw, groen, paars; de speelversie telt 0), en boven `OUD_DREMPEL` gaat het frame eerst
naar bron/ en wordt het daarna omgekleurd. Aan het eind kijkt het script na dat er in de speelmap niets meer in de oude
kleuren staat, anders FOUT. Daarna `gen-klein.py` en `gen-offline-manifest.py`.

## de lagen: het schild als losse laag (lagen.json)

`SCHB_LAGEN`, `schbLagen`, `schbLagenLaad`, `schbLagenLijst`, `schbLaadLevel`, `schbBank.lagen`. De enige manier waarop de
schildbandiet getekend wordt, uit de Animeer tool (export 24-10-2026, versie lagen-2; de bron staat in
`enemies/schildbandiet/LEESMIJ_lagen.md`). Het schild is een eigen plaatje en de rest van de figuur is tot zo weinig mogelijk
lagen samengevoegd, elk bijgesneden tot zijn eigen randen. `enemies/schildbandiet/lagen.json` geeft per beweging (`loop`,
`strike`, `flinch`), per frame en per schildstaat (`metschild`, `fase1`, `fase2`, `zonderschild`) de lagen in tekenvolgorde, elk
`{src, dx, dy, w, h, schild}`: `dx`, `dy` de linkerbovenhoek ten opzichte van het anker (272) en de grondlijn (781), `w`, `h`
de tekenmaat, allemaal in pixels van de grote set. De tekencode doet daarom na de `translate` naar de voeten en de
spiegeling gewoon `drawImage(img, dx * gs, dy * gs, w * gs, h * gs)` per laag; de kleine set (`klein/`) tekent met dezelfde
getallen een half zo groot plaatje. De plaatjes staan in `lagen/lijf/` (116) en `lagen/schild/` (81); elk staat er een keer,
ook als het in meerdere frames of staten terugkomt (de loop gebruikt per staat steeds hetzelfde schildplaatje), en
`schbLagenLaad` maakt per `src` een Image die in `schbBank.lagen` gedeeld wordt (zo warmt `warmBouw` ze mee). De flits
(`whiteCopy`) gaat per laag. De bewegingen, de frametelling (22, 30, 21) en de timing staan in `SCHB` (`schbAnim`,
`SCHB.strikeDur`, `SCHB.flinchDur`), `schbStaat` kiest de staat en de vault hergebruikt de strike-lagen. De dood en de
executie komen uit `executie.json` (zie hieronder). `schbLaadLevel` laadt beide achter de laadpoort als het level een
schildman-spawn heeft (`laadJsonOpen` houdt de poort dicht tot de JSON binnen is en de plaatjes aangevraagd zijn), en
`makeSchildman` roept dezelfde (idempotente) laders aan voor de sandbox, de golf, de arena en de takel-passagiers.

Geheugen: de drie bewegingen in alle vier de staten zijn als lagen ongeveer 67 MB uitgepakt (grote set), tegen zo'n 550 MB
als complete frames per staat zouden zijn. `tools/gen-klein.py` halveert de lagen met een eigen doel
(`enemies/schildbandiet/lagen`, drempel 60), want de bijgesneden stukken zijn lager dan de gewone drempel van 400.

**Geschiedenis.** Tot 25-10-2026 stond het schild in de frames gebakken, met complete sets per stand (`loop_*`, `strike_*`,
`flinch_*`, zo'n 190 MB uitgepakt voor de vier strike- en flinch-sets alleen al) en een eigen dood-set (`dood/`) met een losse
vallende speer (`speer/speer_overlay.png`, `SCHB_SPEER`). De lagen stonden er een tijd als proef naast (`lagen: true` in een
spawn, de knop Nieuwe stijl in de sandbox) en zijn nu de enige manier; de oude mappen, `metadata.json`, de sets-tak van de
code en `tools/schildbandiet_dood.py` zijn weg.

## de dood

`schbSterf`, `exeStart` met `dood`, `SCHB.lijk`. Na de schildbreuk is hij in een klap dood: `schbSterf` geeft de hitstop
(`breekStop`) en de schok, speelt de doodskreet van de bandiet (`banSterf`, `sounds/banditdeath.mp3`) en roept `exeStart(s,
wijze, true)` aan: dezelfde lagen als de executie (`executie.json`), maar na `knielen` komt direct `val`, zonder wankelen,
zonder E en zonder freeze. Twee smaken, op `e.laag`:

- **Dood hoog** (na een worp, `wijze: 'worp'`): de lagen `speer` en `wond` tekenen mee, Amirs speer zit in zijn borst
  (`jav = null`), en vanaf frame `EXE.speerLigtVan` (7) van de val ligt hij echt op de grond op `speer_ligt_op`
  (`exeSpeerNeer`, op te pakken met E), net als na het wankelen zonder E.
- **Dood laag** (na een steek, de lage zwaai, of de sandbox-knop Dood): zonder de lagen `speer` en `wond`; Amir houdt zijn
  speer gewoon in handen.

Hij draait bij de klap naar Amir toe (`s.face`), zoals bij de executie. Na de val loopt `s.ligT`: voorbij `SCHB.lijk.lig`
(7 s) vervaagt hij via `s.alpha` in `SCHB.lijk.vervaag` (0,8 s) en op nul gaat hij naar `weg` (opgeruimd in
`updateSchildmannen`). De executie (`lijk` na het splijten) gebruikt dezelfde `vervaag`. Geldt voor elke schildbandiet,
in elk level; `vijandDood` (de arena-teller van de sandbox, de woede) en de witte flits blijven zoals bij elke kill. Of een
kill de executie wordt in plaats van deze dood beslist `exeKans` (steek 1 op 5, worp 1 op 3, zie hieronder). In de sandbox
laat de knop **Dood** onder Schildbandiet elke schildbandiet meteen Dood laag sterven. De schaduw wordt tijdens de val
breder (`ligt` in de tekenlus, op `s.exe.frame`).

## de executie: knielen, wankelen, vallen en de special execution

`EXE`, `exeLaad`, `exeKans`, `exeStart`, `exeTick`, `exeVries`, `exeTeken`, `exeHelften`, `sbExeNu`. De lagen staan in
`enemies/schildbandiet/executie/` (`executie.json`, `LEESMIJ.md`, `lagen/` met 127 plaatjes): optie C, zoals `lagen.json`,
per beweging per frame een lijst lagen `{src, dx, dy, w, h, item}` in tekenvolgorde, `dx` en `dy` vanaf het anker (272) en
de grondlijn (781) in pixels van de grote set. De bewegingen: `knielen` (20), `wankel` (16, loop), `val` (16, met
`speer_ligt_op`) en `executie` (17, met `amir_start_x`, `amir_eind_x` en de `snijlijn`). `exeLaad` laadt ze zoals
`schbLagenLaad` (via de laadpoort, de plaatjes in `schbBank.executie` zodat `warmBouw` ze meebakt) en wordt door
`makeSchildman` aangeroepen, dus voor elke schildbandiet, ook in een level. `hitSchildman(s, wijze)` weet waar de klap
vandaan komt (`steek`, `worp` of `zwaai`); is het schild weg, dan beslist `exeKans` of de kill een executie wordt
(`EXE.kansSteek` 1 op 5, `EXE.kansWorp` 1 op 3, alleen als de lagen binnen zijn) en anders is het de gewone dood
(`schbSterf`, uit dezelfde lagen, zie "de dood"). Een dode schildbandiet heeft `s.state === 'exe'` en in `s.exe.bew` de
beweging; `s.exe.dood` zegt dat het de gewone dood is en `s.exe.laag` dat de lagen speer en wond niet meetekenen.

**De steek-kill**: `exeStart` zet hem naar Amir toe (`s.face`), begint `knielen` en bevriest meteen de wereld
(`exeBevries`): `exeVries` is de schildbandiet van wie de executie loopt, en `loop` zet dan `dt` op nul en laat alleen
`exeTick` op echte tijd lopen, zoals `kooiVries`. Amir staat op `amir_start_x` (`exeAmirX`, met de spiegeling in
`s.exe.dir`), kijkt naar hem, zonder lopende stoot of worp, en is onkwetsbaar (`hurtPlayer`, `amirVast`, `startSweep`
en `dir = 0` in `loop` kijken naar `exeVries`). Tijdens het knielen is de echte Amir nog te zien maar zonder speer
(`exeSpeerWeg`, die zit in de schildbandiet); zodra `executie` begint is hij weg (`exeAmirWeg`: geen sprite, schaduw, rug
of health-balk) en tekenen de lagen hem, op de plek en de schaal van de schildbandiet, gespiegeld als die naar rechts
kijkt.

**Het einde (bewegingen.einde, `exeEindeStart`).** Staat er in executie.json een beweging `einde`, dan komt na het laatste
frame dat einde in plaats van het splijten hieronder. Er gaat een stuk van zijn borst af, schuin omhoog in de richting van
Amirs ruk (een witte flits langs de snee, `einde.flits`; het stuk valt eraf en vervaagt, `einde.stuk` en `einde.stukVal`),
een schouderbot en een armbot schuiven uit de snee (de lagen met `item: 'bot'`, `uit` is de verschuiving aan het begin),
en het spuit kort uit de stomp: de spuit van het bloedsysteem tot frame `einde.spuit.tot`, `spuit.snel` keer zo snel, op
`spuit.x/y` in de richting `spuit.hoek`, met druppels die wegspatten (`exeEindeSpuitStap`). Zijn lijf schokt een paar keer
om `einde.spil` (`einde.spasme`: ms na het begin van de spuit, graden, px), en het bloed over zijn gezicht komt op
(`item: 'bloed'`). Na `tijd.los` staat Amir meteen rechtop in zijn idle (`exeAmirLos`) en loopt de wereld weer; na
`tijd.val` valt de schildman voorover: de val uit death4 met de snede, het vlees en de botten erin gebakken (`einde.frames`),
waarbij het bovenlijf en de voeten tot op de grond doorzakken; op frame `einde.plof` stof en wat bloed (`exeEindePlof`).
Daarna ligt hij als lijk en vervaagt hij (`SCHB.lijk`). Alle lagen zijn gebakken uit de proefpagina Schildman splijten
(route Deel eraf, snede -20 graden, de botten op de standaardplek); tijden in ms vanaf het einde van het laatste frame.
Zonder `einde` in de json splijt hij zoals hieronder.

Zonder einde splijt hij na het laatste frame (de landing, 600 ms) (`exeSplijtStart`): de `schildman`-laag van het laatste
frame wordt langs de snijlijn, doorgetrokken over de hele laag, in twee helften geclipt (`exeHelften`) die uit elkaar
schuiven, om hun voet kantelen, zakken en vervagen (`EXE.splijt`), met de spuit van het bloedsysteem op de wond langs de
lijn omhoog (`exeSpuitTeken`, `bloedSpuitStap`) en druppels die langs de lijn wegspatten en op de grondlijn blijven
liggen (`exeDruppelsTeken`; de lens en de plas bestaan nog niet in het bloedsysteem); de `amir`- en `speer`-lagen van het
laatste frame blijven er bovenop. Daarna (`exeEinde`) staat Amir meteen in zijn idle op `amir_eind_x` (niet boven een
ravijn, anders op `amir_start_x`), van hem af gekeerd, met zijn speer in de hand, en loopt de wereld weer; het bloed
blijft nog `EXE.lijk` en vervaagt dan.

**De bloedboog** (`EXE.boog`, `exeBoogPad`, `exeBoogStap`, `exeBoogTeken`): vanaf de ruk neemt de speerpunt het bloed
mee. De baan is de wond uit de snijlijn en dan de speerpunt per frame van `executie` (`boog.punt`, frames `boog.van`+1 tot
`boog.tot`, gemeten met `tools/exe_speerpunt.py`: de lengteas van de speer-laag, het uiteinde met de grijze punt), glad
gemaakt met Catmull-Rom. De spuitplaat van het bloedsysteem (`bloedSpuitCache`, dezelfde variant als de spuit op de
wond, vanaf frame 1 want frame 0 is het silhouet) wordt in `boog.stroken` stroken langs die baan gebogen: de voet (het
anker) op de wond, de brede kop met de spatten bij de punt, `boog.breed` smal gehouden en `boog.alpha` dekkend. Tijdens
frame f groeit de boog van sleutelpunt f-1 naar f (in de hitstop op de ruk met de hitstop mee), zodat het bloed net
achter de punt aan hangt; over elke `boog.per` px die erbij komt schiet er een druppel van de punt af met `boog.snel` van
zijn vaart (`e.druppels`, dezelfde lijst als de druppels van het splijten, `exeDruppelStap` laat ze vallen en op de
grondlijn liggen). De plaat loopt op zijn eigen klok af (`bloedSpuitStap` op `boog.klok` van de tijd, tijdens het
splijten op de trage klok) en lost zo vanzelf op in losse spatten; bij het lijk vervaagt hij met de rest. Hij wordt
in `exeTeken` als laatste getekend, over Amir en de speer heen.

**Herhalen** (`herhaal: true`, `exeHerhaalStap`, `EXE.herhaalWacht`): is de laatste schildbandiet weg (na de executie of
de gewone dood), dan komt er na `herhaalWacht` een nieuwe aanwandelen op `spawnPoint` net buiten beeld voor Amir uit,
met het `niveau` van de eerste schildman-spawn van het level. Alleen Test 50 heeft het; een herstart wist de
wachttijd (`exeHerhaalNodig`).

**De worp-kill**: `exeStart` haalt de geworpen speer weg (`jav = null`, de lagen tekenen hem in zijn borst), de wereld
loopt gewoon door: `knielen`, dan `wankel` in een loop, `EXE.wankelDuur` (3 s) lang. Staat Amir binnen `EXE.eReik` (ruim een
Amir) van hem, aan beide kanten, op dezelfde vloer (`exeBij`), dan staat er een E boven hem (staat Amir achter hem, dan
draait hij bij E eerst naar hem toe) (`exeETeken`, via `skE`; `eNodig` zet de E-knop
op de telefoon erbij) en start E de executie (`exeTrek`, vooraan in `toggleSpear`). Zonder E maakt hij de lopende loop af
en speelt hij `val`; vanaf frame `EXE.speerLigtVan` (7) ligt Amirs speer echt op de grond (`exeSpeerNeer`: een `jav` op
de grond op `speer_ligt_op`, de punt naar zijn voorkant, op te pakken met E zoals na een worp; is je hand al weer vol van
de rug, dan een losse speer), en tekent de `speer`-laag niet meer. Daarna blijft hij liggen en vervaagt hij zoals de
gewone dood (`SCHB.lijk.lig`, `vervaag`).

**Het ritme** (`EXE.exeDur`, `EXE.t`, `exeDuur`), zoals een combat game het doet: anticipatie lang, de actie een paar korte
frames, op de impact een hitstop met schok, en een korte slowmotion om de klap te laten nazinderen. De frametijden van
`executie` komen niet uit de json maar uit `EXE.exeDur` (de andere bewegingen houden de json): 0 tot 4 de greep, kort
gehouden omdat die frames weinig verschillen (160, 110, 110, 90, 90), frame 5 de aanzet met een hold van `t.aanzet`
(450 ms) en een trilling (`EXE.tril`), 6 tot 9 de ruk in frames van 45 ms, 10 tot 13 het hangmoment iets trager (70, 100,
110, 100), 14 en 15 versnellen (50, 40), 16 de landing met een hold van `t.land` (360 ms, de tel stilte voor de snee). Het
knielen na de steek loopt in de freeze op `t.kniel` (0,7) van de json-tijden (`exeDuur`): anders staat de wereld bijna
twee seconden stil terwijl hij zakt. De worp-kill en de gewone dood knielen op de tijden van de json. Hitstops binnen de freeze (`e.stop`, `exeTick` staat dan stil en de schok rommelt na op `realDt`): op de
dodelijke steek `t.steekStop` (0,2 s, Amir blijft die tel in zijn stootpose, `exeSpeerWeg` houdt daar rekening mee, en
komt pas daarna op `amir_start_x`: `exeBevries` met `naStop`, `exeAmirZet`; hij glijdt erheen in `t.schuif` (0,16 s,
`s.exe.schuif`), want een steek raakt van 120 tot 280 px en `amir_start_x` ligt op 171 px, en verspringen gaf een schok in
het beeld), op de ruk `t.rukStop` (0,1 s, schok
`schokRuk`, een flits) en op de landing `t.landStop` (0,13 s, schok `schokLand`, stof onder Amirs voeten). De camera komt
op de freeze een stap dichterbij (`EXE.zoom.snap`, `exeZoomNu` vermenigvuldigt `viewZoom`; `viewBasis` is de oude view),
kruipt naar `zoom.tot` en veert na de freeze terug (`exeZoomStap`, elk beeld). Vanaf de ruk schuift de camera op echte tijd
mee naar `amir_eind_x` (`exeCamDoel`, `EXE.cam`, via `camEase` zoals de arena), zodat het beeld niet verspringt als Amir
daar los komt; bij E glijdt de camera ook naar `amir_start_x` (Amir is dan al weg, de lagen tekenen hem). Het wereldstof
loopt in de freeze door (`updateWereldStof` op echte tijd, zoals bij de kooiman), zodat het stof van de landing meteen
opwaait in plaats van pas als de wereld weer loopt. Het splijten loopt op een trage klok
(`e.tS`, `exeTraag`): de eerste `t.traagDuur` (0,35 s) op `t.traag` (0,3), dan in `t.ramp` naar echte tijd; de helften
schuiven eerst traag open en vallen dan om tot `splijt.draai` (1,35 rad), blijven als lijk liggen en vervagen met de rest;
een rode waas aan de rand van het scherm (`exeVignetTeken`, in de schermlaag) dooft in `vignet.duur`. Na de freeze is Amir
`t.veilig` (0,4 s) onkwetsbaar, zonder te knipperen (`invulnStil`): hij is niet geraakt. Bij de worp telt E dat net te vroeg kwam nog `EXE.eBuffer` (0,2 s, `exeEBuffer` in
`exeTrek` en de wankel in `exeTick`). De hitstops, het tempo van het knielen, de holds en de slowmotion zijn live af te stellen in de pauze onder
**Schildbandiet: executie** (`pzexe`, `EXE_SCHUIF`, bewaard onder `EXE_TEMPO_KEY`; de knop staat naast Schildbandiet:
tempo, via `schbTempoKnopToon`).

**Geluid.** Op de snee (het begin van het splijten) klinkt `sounds/beheaded.mp3` (`EXE.snij`, `exeSnijSpeel`). Dat bestand
heeft twee geluiden achter elkaar (het eerste van 0 tot 2,35 s met de haal op 0,15 s, dan stilte, het tweede vanaf 3,4 s);
alleen het eerste speelt: hij start op `snij.van` (0,05 s) en `exeSplijtStap` pauzeert hem op `snij.tot` (2,35 s), en
`restart` ook. De rest van de effecten en het geluid komen later: de haakjes staan klaar, `exeHaakFreeze` (begin van de
freeze, de steek of E), `exeHaakRuk` (frame 5 naar 6), `exeHaakLanding` (frame 16) en `exeHaakSplijt`. De doodskreet en
het geluid van de bloedspuit spelen nog niet.

**Test 50: De executie** is het proefstuk: vlakke grond, een makkelijke schildbandiet, `herhaal: true` (na elke dode komt er een nieuwe aanwandelen), `speerInHand` (R begint meteen
opnieuw) en `executie: true`: elke dodelijke steek, worp en ook de lage zwaai (die telt dan als steek) is de executie
(`exeKans`, `hitSchildman`). De lagen laden in een level achter de laadpoort (`schbLaadLevel` roept `exeLaad` aan, en
`warmBouw` wacht op `schbBank.executie`), niet pas bij de spawn.

**Kleine set en geheugen.** `tools/gen-klein.py` halveert `enemies/schildbandiet/executie/lagen` met drempel 60 (zoals de
lagen van loop, strike en flinch); `dx`, `dy`, `w` en `h` blijven, het spel rekt het halve plaatje naar die maat.
Gemeten in de sandbox: de 127 lagen zijn uitgepakt 27,4 MB op de grote set en 7,3 MB op de kleine (5,3 MB en 1,6 MB op
schijf). Ze laden mee zodra er een schildbandiet is.

**Sandbox**, onder Schildbandiet: **Executie: kans/altijd** (`sbExeAltijd`, elke steek- en worp-kill wordt een
executie), **Wankel: E aan/geen E (val)** (`sbExeGeenE`: de worp-kill krijgt geen E en eindigt in de val), **Steek-kill**
en **Worp-kill** (`sbExeNu`: de eerste levende schildbandiet meteen zo doden; bij de steek krijgt Amir zijn speer in de
hand, bij de worp zit zijn speer in de schildbandiet). Nagekeken op 1280 bij 720, groot en klein, naar links en
gespiegeld: de steek, de worp met E, de worp zonder E (de speer ligt naast hem en is op te pakken), zonder consolefouten.
