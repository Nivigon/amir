# De schildbandiet

## de schildbandiet: loopt met zijn schild op en valt springend aan

`SCHB`, `makeSchildman`, `updateSchildman`, `hitSchildman`, `schbMik`, `schbSprongP`, `schbLand`. Het ritme van het gevecht, afgestemd met `tools/schildduel.js`: hij loopt op Amir af tot `houd` (1 Amir) en zet op `aanval` (2,1 Amir) de sprong in. De tell (frame 0..5, ~0,8 s) is tot `pantserVan` (3) te onderbreken; daarna zet hij door (een treffer kost schild maar onderbreekt niet). Tot `mikTot` (7, net na de afzet) stuurt hij bij naar Amir, zo dat zijn speerpunt (`speerVoor`, 0,62 Amir voor zijn midden) op Amir de grond in gaat; de sprong (6..16, ~0,57 s) is onaantastbaar en vloeit op de klok (`schbSprongP`). Hij raakt op 17..20 rond de punt (`speerR`) of onder zijn lijf (`lijfR`) en slaat Amir dan terug (`raakDuw`); de landing geeft een hitstop (`landStop`), schok en een zet die dichtbij harder is (`landDuw`). Het herstel (21..29, ~0,8 s) is het raam om te straffen. Een treffer geeft een korte hitstop (`raakStop`, `breekStop`) en een flinch die meteen begint (`flinchVan`) met een terugstoot (`flinchDuw`); vanaf `dekVan` in de flinch ketst je speer af (geen stunlock), en binnen `wraakT` slaat hij terug met een tell die al gepantserd is. Gemeten op 1280 bij 720: met 0,2 s reactie ontwijk je alles, met 0,35 s word je bij twee van de drie sprongen geraakt, blind steken of stilstaan kost meerdere levens; het gevecht duurt zo'n 8 tot 10 seconden. Dat is het niveau `moeilijk` (zonder veld). Met `niveau: 'makkelijk'` in zijn spawn (`SCHB_NIVEAU`, `schbN`, `schbDur`) heeft hij een langere tell, een tragere sprong en een langer herstel, mikt hij alleen tot de afzet, zet hij later door en slaat hij na een flinch niet gepantserd terug. Het tempo per niveau staat in `SCHB_TEMPO` (tell, aanval = sprong en inslag, herstel; hoger is sneller, `schbDur` deelt de frameduur erdoor en de sprong beweegt vanzelf mee) en is live af te stellen in de pauze onder **Schildbandiet: tempo** (`pzschb`, `SCHB_SCHUIF`, bewaard onder `SCHB_TEMPO_KEY`, de knop alleen in een level of sandbox met een schildbandiet, `schbTempoKnopToon`); aanval en herstel staan bij beide niveaus standaard op 150% (de tell op 100%). Bij het landen klinkt hetzelfde geluid als Amirs speerstoot (`schbLandGeluid`, `music/spearthrust.mp3`, eigen stemmen, verder weg zachter), niet meer het grondgeluid van de kooiman. Met `achter` (px) start een spawn op hetzelfde moment als de spawn op zijn x, maar zoveel verder weg, zodat hij een tel later het gevecht in loopt: zo komen er twee na elkaar (werkt ook voor de bandiet en de kooiman). Test 45 is het proefstuk, Test 46 loopt op van een makkelijke via twee makkelijke en een moeilijke naar twee moeilijke, dan een bandiet met een moeilijke en een moeilijke met de kooiman (gespeeld met `tools/schildduel.js --level "Test 46"`: met 0,35 s reactie 0, 2, 2 en 4 keer geraakt); in de sandbox onder Vijanden. In de Maker nieuwstijl staat hij onder Vijanden als Schildbandiet met twee varianten: Moeilijk (`schildman`) en Makkelijk (`schildman:makkelijk`, wordt in `mkSpawn` `niveau: 'makkelijk'`)


## de schildstaat: het schild gaat zichtbaar kapot

`SCHB_STAAT`, `SCHB_SETS`, `schbStaat`, `schbBankVoor`, `schbFrameImg`. Het schild zit in de frames gebakken, in vier standen: 0 treffers `metschild`, 1 `fase1` (een hap eruit), 2 `fase2` (twee happen), 3 `zonderschild` (weg, daarna in een klap dood). `schbStaat` leidt de stand af uit `s.schild` en `s.metSchild`; omdat `hitSchildman` het schild al verlaagt voor de flinch begint, speelt de flinch meteen in de nieuwe stand en verschijnt de hap op het moment van de klap. Bij een gepantserde treffer (late tell) wisselt de strike midden in de animatie van set; dat verspringt niet, want het lijf is in alle sets pixel voor pixel hetzelfde (zelfde canvas 544x860, grondlijn 781, anker 272, zelfde timing). De loop blijft `loop_metschild` tot het schild weg is.

Welke sets er op schijf staan, staat in `SCHB_SETS` (per animatie de lijst `standen`). Een stand zonder eigen set valt terug op de stand ervoor (`schbBankVoor`). Nu ontbreekt alleen `flinch_fase1`: de strike toont na de eerste treffer de ene hap (`strike_fase1`), maar de flinch van die eerste treffer speelt nog met een heel schild. Komt hij erbij: frames in `enemies/schildbandiet/flinch_fase1/`, `'fase1'` in de lijst `standen` van `flinch`, dan `gen-klein.py` en `gen-offline-manifest.py`. Upload frames altijd in hun eigen map (of als zip): de sets hebben dezelfde bestandsnamen en overschrijven elkaar in de hoofdmap. Laden, `warmBouw` en de laadpoort volgen vanzelf (alles in `schbBank`). De bron staat in `enemies/schildbandiet/LEESMIJ_schildfases.md` en `metadata.json` (`schild_staat`).
## de nieuwe stijl: het schild als losse laag (lagen.json)

`SCHB_LAGEN`, `schbLagen`, `schbLagenLaad`, `schbLagenLijst`, `schbLaadBasis`, `schbBank.lagen`. Op proef naast de complete
sets, uit de Animeer tool (export 24-10-2026, versie lagen-2; de bron staat in `enemies/schildbandiet/LEESMIJ_lagen.md`).
Het schild is een eigen plaatje en de rest van de figuur is tot zo weinig mogelijk lagen samengevoegd, elk bijgesneden tot
zijn eigen randen. `enemies/schildbandiet/lagen.json` geeft per beweging (`loop`, `strike`, `flinch`), per frame en per
schildstaat (`metschild`, `fase1`, `fase2`, `zonderschild`) de lagen in tekenvolgorde, elk `{src, dx, dy, w, h, schild}`:
`dx`, `dy` de linkerbovenhoek ten opzichte van het anker (272) en de grondlijn (781), `w`, `h` de tekenmaat, allemaal in
pixels van de grote set. De tekencode doet daarom na de `translate` naar de voeten en de spiegeling gewoon
`drawImage(img, dx * gs, dy * gs, w * gs, h * gs)` per laag; de kleine set (`klein/`) tekent met dezelfde getallen een half
zo groot plaatje. De plaatjes staan in `lagen/lijf/` (116) en `lagen/schild/` (81); elk staat er een keer, ook als het in
meerdere frames of staten terugkomt (de loop gebruikt per staat steeds hetzelfde schildplaatje), en `schbLagenLaad` maakt per
`src` een Image die in `schbBank.lagen` gedeeld wordt (zo warmt `warmBouw` ze mee). De flits (`whiteCopy`) gaat per laag.

Alleen de tekenlaag is anders. De bewegingen, de frametelling (22, 30, 21) en de timing zijn die van de complete sets
(`schbAnim`, `SCHB.strikeDur`, `SCHB.flinchDur`), `schbStaat` kiest de staat, de vault hergebruikt de strike-lagen, en de dood
blijft de eigen set in `dood/` (`schbLaadBasis` laadt die en de losse speer voor beide stijlen). Een schildbandiet tekent zo
met `lagen: true` in zijn spawn (`schbLaadLevel` laadt dan de lagen in plaats van de complete sets; `laadJsonOpen` houdt de
laadpoort dicht tot `lagen.json` binnen is en de plaatjes aangevraagd zijn), en in de sandbox met **Neerzetten nieuwe
stijl** onder Schildbandiet (`sbSpawn('schildman_lagen')`). Nagemeten in de sandbox op 1280 bij 720: oude en nieuwe stijl op
dezelfde plek in dezelfde houding en staat (loop, tell, inslag, herstel, flinch, met heel, aangeslagen en zonder schild)
geven hetzelfde beeld op hooguit randpixels na.

Geheugen: de drie bewegingen in alle vier de staten zijn als lagen ongeveer 67 MB uitgepakt (grote set), tegen zo'n 550 MB
als complete frames per staat zouden zijn. `tools/gen-klein.py` halveert de lagen met een eigen doel
(`enemies/schildbandiet/lagen`, drempel 60, voor de map `enemies/schildbandiet` zodat die drempel wint), want de bijgesneden
stukken zijn lager dan de gewone drempel van 400.

**Bevalt het, dan gaat de oude manier eruit.** Dat is: de mappen `loop_*`, `strike_*` en `flinch_*` (en hun kleine versies,
via `gen-klein.py` en `gen-offline-manifest.py`), `SCHB_SETS`, `schbBankVoor` en de set-tak van `schbFrameImg` en `schbLaad`
(de dood en de speer blijven, in `schbLaadBasis`), het veld `lagen` en de tweede sandbox-knop (dan is de lagen-stijl de
enige), de `sets` in `metadata.json` en de notitie hierboven over de schildstaat per set.

## de dood

`SCHB.dood`, `schbSterf`, `schbGeo`, `SCHB_SPEER`, `schbSpeerLos`, `schbSpeerStap`, `schbSpeerTeken`. Na de schildbreuk is hij in een klap dood: `schbSterf` geeft de witte flits en de hitstop (`breekStop`), speelt de doodskreet van de bandiet (`banSterf`, `sounds/banditdeath.mp3`) en zet de dood-set aan. Die staat in `enemies/schildbandiet/dood/` (`dood_00..36`, met `dood.json`, `LEESMIJ.md` en `preview.gif`). De set heeft een eigen canvas (544 bij 560, grondlijn 481, hetzelfde anker 272 en dezelfde schaal), dus de tekencode pakt de maat via `schbGeo`. Hij speelt even snel als de dood van de bandiet: 37 frames in de totale duur van de bandiet (`BAN.n.dood` frames op `BAN.fps.dood`, 2,1 s), zo'n 17,6 fps. Daarna blijft `dood_36` liggen als lijk; hij vervaagt niet.

**De speer valt los.** In de oorspronkelijke frames zat de speer in de tekening (hij glipt uit zijn hand en ligt plat voor zijn voeten), ook als hij op de rand van een ravijn of naast een kei stierf. `tools/schildbandiet_dood.py` haalt hem eruit: vanaf frame 7 is de speer weg (de schoenen erachter komen uit een frame waar ze vrij stonden), en de twee bron-frames waarin hij voor de tuniek langs viel zijn eruit, want wat erachter zat was niet netjes terug te halen (39 werd 37 frames). Het spel laat zijn eigen speer vallen (`enemies/schildbandiet/speer/speer_overlay.png`): `schbSpeerLos` zet hem op frame `SCHB.dood.speer.los` (7) op de plek waar hij hem op frame 6 vasthield (`punt`, `eind` in canvas-px), en `schbSpeerStap` laat hem vallen als een staaf met vijf steunpunten (`SCHB_SPEER.steun`) die elk op de vloer onder zich botsen (`schbSpeerVloer`: de grond, een terras of gang, een kei of richel; boven een ravijn niets). Zo stuit hij even, ligt hij plat of scheef, en kantelt hij over de rand een ravijn in; dieper dan `SCHB_SPEER.weg` is hij weg. Hij ligt `voor` canvas-px voor de voeten, zoals in de tekening, en flitst mee met de doodklap.

**Na de flits meteen los.** `SCHB.dood.start` (7): na de witte flits begint de dood op het eerste frame waarop de speer al niet meer voor zijn lijf hangt, en valt de losse speer meteen. Met `start: 0` speelt hij de klap ervoor weer (frame 0 tot 6, waarin hij de speer nog vasthoudt).

**Het lijf op de grond.** In de bron lag hij na de val zo'n 15 tot 30 canvas-px boven de grondlijn: hij zweefde boven zijn schaduw. Het script zet elk frame vanaf de landing zo ver omlaag dat de onderkant van het brede deel van zijn lijf op de grondlijn ligt (`LIG`), met de landing verdeeld over de twee frames ervoor; hoeveel per frame staat in `dood.json` (`omlaag`). De schaduw wordt breder vanaf `SCHB.dood.ligVan`.

Een nieuwe dood-animatie zonder speer erin past zonder het script: zet de frames in de map, `n` op het aantal, `speer.los` op het frame waarop zijn hand opengaat en `punt`/`eind` op de plek van de speer in het frame ervoor. Teken het liggende lijf dan met zijn onderkant op de grondlijn (481). In de sandbox laat de knop **Dood** onder Schildbandiet elke schildbandiet meteen zo sterven.
