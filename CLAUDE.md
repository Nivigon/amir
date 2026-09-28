# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Levels van een echte episode blijven met rust.** Nu is dat De Jagers (`JAGER_1` tot en met
`JAGER_5`). De Episode Test levels (`TEST_1` en verder), de episode Testrun (`RUN_1` en verder) en de episode Baboon tests (`BAB_1` en verder) vallen niet onder deze regel: ze zijn er
juist om aan te rommelen. De leveldefinities van een echte episode zijn bevroren: er komt geen nieuwe vijand, prop, tip, potion of aangepast
getal in, ook niet even om iets te laten zien. Alleen als de opdracht een level bij naam noemt
("zet dit in level 6") mag dat ene level veranderen. Twijfel je of iets eronder valt, dan valt
het eronder: vraag het.

**2. Nieuw werk test je in de sandbox.** Een nieuwe vijand, prop of mechaniek krijgt
knoppen in de sandbox, zodat het zonder level uit te proberen is. Dat is ook hoe de
speerworp erin kwam: knoppen onder "Speerworp", geen enkel bestaand level aangepast.

**3. Een nieuw testlevel alleen na toestemming.** Vraag het eerst, per geval. Mag
het, dan ontwerp je het level zelf: lengte, uitzicht, tegenstanders en opbouw zijn
aan jou, en je legt achteraf uit wat je gekozen hebt.

**4. Sluit aan op wat er is.** Er is al een laadsysteem, een decorregister, een
tekenlaag en een sandbox. Gebruik die in plaats van er een tweede naast te zetten.

**5. Nederlands, en geen em-dashes.** Code, commentaar, teksten in het spel, commits
en pull requests zijn Nederlands. Gebruik komma's of haakjes, nooit een lang
gedachtestreepje.

**6. Werk op een `claude/*`-branch.** Push daarheen en maak alleen een pull request
als daarom gevraagd wordt.

**7. Vijanden komen niet over keien en ravijnen.** Slangen, fosforslangen, de
zwaardvechter en ook de panters worden tegengehouden door een kei om op te springen en
door de rand van een ravijn: niet lopend, niet met een sprong of een duik, en ze duiken
ook niet aan de overkant op. Zo is een kei of een ravijn voor de speler een schuilplek.
Een schuilplek, geen veilige plek: een slang of schorpioen naast de kei mag Amir bovenop die
kei nog bijten of steken, want hun beet reikt tot de hoogte van een kei. Dat is zo bedoeld.
Een uitzondering mag alleen als de opdracht er expliciet om vraagt, of in een gevecht met
een eindbaas als je daar zelf voor kiest omdat het dat gevecht beter maakt; zeg dan
achteraf dat en waarom. Voor de panter is dat het veld `over: true` in zijn spawn
(`panBaan`); zonder dat veld blijft hij aan zijn kant.

**8. Geen versienummer in de code.** Linksboven staat vanzelf van wanneer de versie is die je
speelt, en onder **Updates** in het menu staan de laatste vijf samengevoegde pull requests, van
GitHub zelf, met per stuk of hij al in die versie zit. Zet dus nergens een nummer bij: vroeger
paste elke pull request dezelfde regel aan (`VERSIE`), en twee die tegelijk openstonden botsten
daar altijd op. Geef een pull request wel een titel die zegt wat er nieuw is, in een paar woorden:
die titel is wat de speler onder Updates leest.

**9. Een speer in een houten runeschijf blijft vastzitten.** Op een rots, in de rotswand of bij de
grot: wie de schijf raakt is zijn speer kwijt, en E haalt hem er niet uit. Het spel geeft er niet
vanzelf een nieuwe voor terug; of en waar de speler een nieuwe krijgt (een skelet, een speer in de
grond) is een keuze van het level, en een level zonder mag juist de uitdaging zijn.

## Waar wat staat

De HTML is opgedeeld met commentaarkoppen (`// ---- ... ----`). Zoek daarop, niet op
regelnummer, want die schuiven bij elke wijziging.

| kop | wat er staat |
| --- | --- |
| laadpoort: een level loopt pas als alles binnen is | `LAAD`, `laadOpen`, `laadPoort`, `laadStap`, `#laad`: het zetten van `src` op elk plaatje zet het vanzelf in `laadOpen` tot het binnen is of ontbreekt (een haakje op `HTMLImageElement.prototype`), dus een nieuwe lader hoeft niets aan te melden. `restart` zet de poort dicht; de lus staat stil (`dt` 0, geen toetsen) tot `laadOpen` twee beelden achter elkaar leeg is, met na `LAAD.toon` het scherm Laden en na `LAAD.max` gaat hij toch door. In het menu en de bouwer wacht hij niet. Geluid telt niet mee |
| versie: welke update er live staat | `versieTijd` (uit `document.lastModified`) heel klein linksboven, en `toonUpdates`: de laatste vijf samengevoegde pull requests van GitHub (`VERSIE_REPO`), met of ze erin zitten (regel 8) |
| de zon: schijf, krans en ademende ring | `ZON`, `drawZon`: de zon in de lucht, met een lichte kern, een krans, een gloed op de horizon en een zachte ring die langzaam ademt (`ringAdem`, `ringT`). Plek, straal en kleur blijven uit `sun` in `SCENES`. Daarnaast `drawWaas`: overdag lucht tussen jou en de verte, met het veld `waas` in `SCENES` (het uitzicht `middag`). In de sandbox onder Tijd van de dag (`sbLagen`) en Zon |
| globale lichtlaag | kleurwaas over het beeld, volgt de zon van het level; een level stelt hem bij met `licht` in `SCENES` |
| de schaduw van Amir | `AMIR_SCHADUW`, `amirSilhouet`, `amirSilLeg`, `drawAmirSchaduw`: zijn eigen frame als silhouet op de grond, in twee lagen en nergens een ronde vlek. De omgevingsschaduw (`omgeving`) is het silhouet recht naar beneden platgedrukt, dikker gemaakt en zacht, half achter en half voor de voeten; die is er altijd, ook onder de grond, even sterk als het licht rond hem (`amirLicht`, uit `lkRondAmir`). De zonneschaduw: richting en lengte uit de zon van het uitzicht (`zonSchaduw`, `sun` in `SCENES`): naar voren, want de zon staat achter het landschap, opzij van de zon af, en langer naarmate de zon lager staat, tot 1,2 keer zijn lengte. Onder de grond of onder rots alleen waar de zon komt (`amirZon`, uit `lkZon`). In een sprong blijven beide recht onder hem; de zonneschaduw vervaagt snel (`wegSil`), zodat de omgevingsschaduw de landing aanwijst. Getekend na de terrassen, treden en keien (`amirSchaduw`, vlak voor de lichtkaart), anders vallen die eroverheen. Een keer per frame gebakken. De ravijnen en de lichtkaart gebruiken nog de vaste `LK.zonHoek` |
| tribes: de keuze per run en de abilities | `TRIBE_CONFIG` (bovenin het script: alle namen, teksten en getallen) en `RUN` (tribeId, verdiende abilities, uitgespeelde levels); onder "tribes: keuzescherm, ability, HUD" `tribeKies`, `tribeNaLevel` (vanuit `winLevel`, geeft een talentpunt in `RUN.punten`), de talent tree onder "talent tree" (ontwerp 7 uit de schetsen: groeit omhoog, het thema per tribe in `boom` in `TRIBE_CONFIG`, met `TB_RING`, `tbLijn`, `TB_TEKEN` voor plaatjes die nog ontbreken en `tbVergelijk` voor zonder en met; `tribeBoomToon`, `tbStaat`, `tbKlik`, `tbBijwerken`; in `#trunlock`, ook te bekijken via `pztalents` in de pauze; op het keuzescherm opent een kaart de boom zonder te kiezen (`tribeBekijk`, `tbKijk`, `tbRun`), en `tribeVastleggen` legt de tribe pas vast bij het eerste talent of bij Join; een tribe op slot laat `TB_LEEG` lege plekken zien), `opnieuw` (na game over hetzelfde level, abilities blijven), `hudToon`, `tribeHeeft` en `abilityWaarde`. Een ability werkt alleen via die twee: Quick Hand in `updateThrow`, Thorn Breaker in `hitThicket`, Twin Sweep (id `low_sweep`, `ladingen`) in `sweepMax`; de lage zwaai zelf heeft iedereen, met ladingen die in `SWEEP_HERLAAD` seconden terugkomen (`swLading`, `sweepLaden`, `zwaaiHud` rechtsboven), en wat hij raakt staat voor iedereen in `zwaaiVak`, Fourth Life in `levensStart`. Een tribe met `bijStart` krijgt zoveel talentpunten meteen bij het kiezen; nu staat dat bij alle tribes op 0, zodat je in level 1 nog niets van je keuze merkt. De woedemeter van Bhubesi (`woede` in zijn blok, stand in `RUN.woede`) staat onder "woede": `heeftWoede` (Long Breath of Blood Rush), `woedeVul` (vanuit `vijandDood` en `hitPanther`), `woedeStart` (G, de meter, de knop `woede` in `TOUCH_BTNS`), `woedeAan` houdt `hurtPlayer`, `valLand` en `fosforBijt` tegen, `woedeGloed` en `woedeVonken` bij het tekenen van Amir. Elke episode begint met de tribekeuze (`runStart` in zijn speelknoppen, en bij dubbelklikken op een kaartje in `buildCards`), nu De Jagers, Testrun en Baboon tests; de Test levels niet, tenzij daar expliciet om gevraagd wordt, en daar gelden alle abilities van de tribes die niet op slot staan, net als bij testen vanuit de bouwer (Test 14 laat je kiezen, zie `talentKeuze`). Een tribe op slot (nu Impungushe) mag al abilities hebben: die gelden dan alleen in de sandbox en in Test 14; zijn boom laat ze dicht zien en zijn kaart op het keuzescherm blijft leeg. De sandbox heeft `sbAbilities`, de speelrobot speelt De Jagers zonder abilities. De plaatjes in `design/tribes/` komen uit `tools/tribe_logos.py`; de drie ability-plaatjes van Bhubesi zijn uitgeknipt (tot 400 bij 400, grijs eromheen doorzichtig) uit de JPG's in de hoofdmap, waarvan twee namen omgewisseld zijn: `fastereimmortal.jpg` is Long Breath, `longerimmortal.jpg` Blood Rush, `extralife.jpg` Fourth Life |
| muziek per level | `MUZIEK`, `MUZIEK_BASIS` (Dark Africa: bij de start, in het menu, de bouwer, de sandbox en elk level zonder veld `muziek`), `zetMuziek()`: welk deuntje onder welk level loopt |
| beeld: de grote of de kleine spriteset | `KLEIN_FAM`, de keuze groot of klein, `zetBron` |
| hppotion | de drinkkalebas |
| renstoot: sprinten en dan stoten | `RENSTOOT`, `glijStart`, `glijUpdate`, `glijWolk`: vanuit een sprint neemt hij zijn vaart mee in de stoot en glijdt hij remmend door, met het stof van de lage zwaai bij zijn voeten; stopt voor een ravijn. In de sandbox onder Renstoot |
| bukken, jump frames, tempo | Amir zijn bewegingen |
| rotsen om op te springen | `rocks`, en het automatisch bijgroeien |
| winter: episode Winter World | `WINTER_SRC`, `winterOn()`, `winterPic()` |
| bodem en sneeuwdek | het veld `sneeuw`: savanne of rots, en het dek in vier standen |
| het verhaal bij een episode | `VERHAAL` en `SLOT`, `verhaalToon()`: tekst op een zwart scherm voor elk level en na het laatste, alleen als je bij het eerste level begint. Op de naam van het level, dus een nieuwe episode hoeft alleen tekst toe te voegen en `verhaalAan` te zetten in zijn speelknop |
| Episode De Jagers | `JAGER_1` tot en met `JAGER_5` en `JAGER_LEVELS`: vijf pittige levels met een verhaal (`VERHAAL`, `SLOT`) en Nightmare; menu `menuJager`, `cardsJager` |
| Episode Test levels | `TEST_1` tot en met `TEST_16`: korte proefstukken, los van de echte episodes. Test 14 heeft `talentKeuze`: een scherm voor het begin (`talentKeuzeToon`, `testTalents`, in de pauze `pzkeuze`) waarop je de talents kiest, ook die van een tribe op slot |
| Episode Baboon tests | `BAB_1` en `BAB_LEVELS`: proefstukken voor de baviaan, met de tribekeuze (`runStart`) zoals Testrun; menu `menuBab`, `cardsBab`. Baboon 1 is een kopie van Test 15 met de speerbeet in plaats van de wand en de kooi |
| Episode Testrun | `RUN_1` tot en met `RUN_3` en `RUN_LEVELS`: drie snelle levels die bestaande dingen combineren; een episode, dus met de tribekeuze (`runStart`) en talents per level, net als De Jagers; menu `menuRun`, `cardsRun`. Wat werkt en wat niet staat in `notities/combinaties.md`: lees dat voor je een nieuw level of een nieuwe combinatie bedenkt, en stel ideeën daaruit voor in plaats van ze zomaar in te bouwen |
| het mes: Jackal Fang van Impungushe | `MES`, `mesInHand`, `mesTeken`, `mesPunt`: E wisselt rond in `toggleSpear` (speer, mes, niets). Een steek is de gewone stoot met `atkMes`; alles wat de punt ergens tegen houdt vraagt `steekLive`, `steekDX`, `steekY`, `steekR` en `steekRaakt(soort)`, dus een nieuwe vijand gebruikt die en niet `TIP_DX`. Het mes doodt niets: op elke plek waar de punt een vijand raakt gaat het met `atkMes` naar `mesAfweer(s, soort)`, die hem terugduwt, zijn aanval afbreekt en hem meteen weer laat komen, met een afkoeltijd per vijand (`s.afweerTot`, op `mesKlok`). Het terugdeinzen loopt in de update van de slang, schorpioen en hyena via `afweerStap` (met `knockBlocked` of `hyMove`, dus nooit over een kei of ravijn), bij de zwaardvechter via zijn eigen `knock` en bij de fosforslang via `vx`. Een nieuwe vijand krijgt dus een tak in `mesAfweer`. Het mes snijdt ook de kalebas aan een koordje los (`tekenSnij`, dat was eerst het talent Scavenger). Bared Teeth, de dreighouding: `houding`, `houdingZet` (in de update van Amir: aan of uit, en waar hij heen kijkt), `houdingStap` (bovenin de update van de slang, schorpioen, hyena en zwaardvechter), `houdingLos` (hij valt aan) en per soort `BEDWING` (wanneer hij mag, hoe hij beweegt, hoe hij aanvalt). De getallen van beide talents staan in `TRIBE_CONFIG` en zijn in de pauze bij te stellen (Instellingen, Mes: reacties: `MES_SCHUIF`, `mesAfstelZet`, bewaard onder `MES_KEY`). |
| T-splitsing in de talent tree | een talent met `varianten` in `TRIBE_CONFIG` krijgt naast zijn naam een gestippelde splitsing met de namen (`tbSplit`, `.tbsplit`) en in het venster de varianten met hun tekst (`.tbivar`). Nog niets te kiezen; nu alleen bij Jackal Fang. Een tribe op slot laat zijn talents dicht zien; `TB_LEEG` alleen als hij er nog geen heeft Tijdelijk getekend: het plaatje komt uit `tools/mes.py` (`design/mes/mes.png`), zijn lijf schiet naar voren omdat er geen frames met een mes zijn. De kalebas is de speertekenvariant `kalebas` |
| Feign Death | `SCHIJN`, `schijnDoodVang` (vanuit `hurtPlayer`, `valLand` en `fosforBijt`), `schijnDoodZet` (kantelt zijn frame), `schijnHud` (`#schijn`); per level terug in `restart` |
| lichtkaart: het licht onder de grond | `LK`, `drawLichtkaart`: een lichtbron (de hemel en de zon) voor alles onder de grond en onder rots boven je, per level een keer uitgerekend |
| terrassen en richels | `terraces`, `ledges`, klimmen |
| de rotswand rechts | `cliffs`, het einde van het level |
| grotten: rots als een raster van cellen | `grotten`: het raster, de randen, de verstrooiing, de botsingen |
| plafond: de rots boven je, als hoogtelijn | `plafond`: de lijn, de vulling, de band, de losse blokken |
| muur unlock: de rotswand met het rune-symbool | `MUUR`: de plaat, het gat, het schuifblok, het masker en de schijf; en de grot met de kei (`MUUR_GROT`, `muurGrotSet`, `drawMuurGrot`) |
| ravijn in de winter | `RAVIJN_WINTER`, `ravijnWandNu()`, `ravijnSneeuwRand()`: het openscheurende ravijn in een winterlevel, de wand bij het laden omgekleurd naar blauwgrijze steen (alleen kleur, per pixel op helderheid), een getekende sneeuwrand en het berijpte gras |
| zegel in de grond: de runeschijf plat, als schakelaar | `ZEGEL`, `zegelGrond`, `zegelUpdate`, `zegelDoe`: erop stappen zet hem aan of uit, en wat hij dan doet (een ravijn openen of sluiten, de rotswand openen, een speerval losschieten). Het teken op het hout komt uit `ZEGEL_TEKENS` (`zegelTekenVan`, `zegelRunePad`: alleen lijnen en cirkels, in het platte vak): `rune` en `teken1` tot en met `teken8`, die met opzet niets betekenen. Elk teken krijgt een vaste bestemming, zodat de speler het leert herkennen: `rune` is activatie door de speler, `teken2` activatie ook door een vijand; de andere zijn nog open (zie `notities/zegeltekens.md`, en wijs er daar een aan voor je er een gebruikt). Met `vijand` zet ook een vijand in beeld hem aan (`zegelVijand`, niet een hyena die buiten beeld wacht), en krijgt hij standaard `teken2`; het ravijn dat hij opent is een val (`fx.vangt`, `ravijnVangt` bovenin `ravijnValt`): een vijand in dat stuk staat vast tot het open is en valt er dan in. Een zegel waar een ravijn onder opengaat valt mee (`z.val`, `ZEGEL_VAL`). In de sandbox Val voor vijanden en Zegelteken |
| speerval: een speer in de rotswand die een zegel losschiet | `SPEERVAL`, `speervalZegel` (vanuit `zegelUpdate`, en daar begint het opspannen), het geluid `sounds/speerval.mp3` (`SPEERVAL_SND`, `speervalSpeel`, `speervalStil`, twee audio-elementen `valSpanSnd` en `valVuurSnd`, ook in `geluidOntgrendel`: het kraken van 0,05 tot 0,9 seconde tijdens het trillen, `SPEERVAL.wacht` 0,8, en het vuren vanaf `vuur` 1,7, `voor` 0,1 seconde voor hij los is, zodat de klap op 1,8 valt als hij de wand uit komt), `speervalUpdate`, `speervalTeken` (twee keer: in de wand voor de klif, zodat het steen over zijn staart ligt, en na de baviaan als hij vliegt), `speervalBox`, `speervalReset`. Waar het steen op zijn hoogte begint komt uit de alfa van de klifplaat (`klifVlak`), want de klif hangt aan het scherm en niet aan Amir. Hij zit op `h` (0,82 Amir): boven een gebukte Amir (`DUCK_BOX`), door een staande, dus bukken laat hem passeren en springen niet. In de tekenlus raakt hij Amir (`hurtPlayer`, alleen als die niet onkwetsbaar is) of de baviaan (`valRaakt` in `bavGevecht`, voor de beet gekeken): die gaat dood, ook met `BAV_VECHT.raakbaar` uit, en van voren blijft de speer in zijn borst zitten (zie "speer in de baviaan"). Zolang de baviaan leeft houdt hij de fakkels dicht, maar alleen in een level met een speerval (`bavBlokkeert`, in `bossBlocking`), want anders is hij niet te verslaan. Een misser valt, ligt `lig` seconden, en zit dan weer in de wand; het zegel gaat dan vanzelf uit. In de sandbox onder Speer en spullen, Speerval (`sbSpeerval`, `SB_SPEERVAL`: een klif met `valKlif` en een zegel). Geen soort uit "wat mag waar": hij zit in de wand, niet op de grond. Test 16 is het proefstuk. Hij is de gekartelde valspeer (`val` uit `DRAAI`): zwart staal met een geslepen lichte snede langs de kartels en een middenrib, de ring onder het blad in goud, een smalle gouden ring op de schacht en een gouden kap (`zwart_staal` in `tools/draaispeer.py`, op alle draaiframes); hij rolt in de vlucht; hij is langer dan `javImg`, dus de laag voor de klif rekent met zijn eigen lengte (`lang`) |
| de draaiende speer: rollen om de lengteas in de vlucht | `DRAAI`, `draaiImgs`, `draaiBeeld(soort, t)`, `draaiTeken(img, soort, k)`: 36 frames per omwenteling in `design/speer/draai/`, `gewoon` (Amirs speer, even lang als `javImg`) en `val` (de speerval), op dezelfde schaal `k` als `javImg`, punt rechts op `tipY`. Amirs geworpen speer rolt alleen in de vlucht (`javSchacht`, op `jav.t`; met `vaanBlauw` ook blauw, en in `vaanVoorwerk`), de speerval alleen in de vlucht (op `sp.t`). Stilliggen, in een wand of in de grond is weer `javImg`. De frames komen uit `tools/draaispeer.py`, uit de video van Grok in `design/speer/bron/`: alleen frame 0 tot 17 daarvan was bruikbaar, de rest van de rol is dat stuk gespiegeld |
| skelet met speer | `SKELET`, `skeletTrek`, `skeletUpdate`, `skeletTeken`, `skeletRaak`: E vasthouden trekt de speer eruit, het skelet stort in met de losse botten (`sounds/skeletvalt.mp3`); de schedel is daarna los decor; losse speren op de grond (`losseSperen`) en het blauwe vaantje (`vaanBlauw`) |
| speerteken: een speer in de grond met een zwart doek en schedels | `TEKEN`, `tekenUpdate`, `tekenTeken`: decor in vijf varianten (`teken`, `gebroken`, `gekruist`, `jagers`, en `kalebas`: een kalebas aan een koordje die je met het mes lossnijdt, `tkKalebas`, `tekenSnij`); het doek wappert op `windAt` zoals het gras. Maten in Amir |
| licht op de runerotsen | `RUNE_LICHT`, `runeLichtMaak`, `runeGrondSchaduw`: de zon op een rots met een rune, uit dezelfde richting als de lichtkaart (`LK.zonHoek`, `zonRechts`); zie "runes op elke rots" |
| runeschijf: het losse symbool | `runeSchijf(ctx, x, y, r, {aan, spiegel})`: de houten schijf met de rune, los te hergebruiken |
| vallen: schade bij een diepe val | hoe diep een val telt en wat hij kost |
| schorpioen, het projectiel, spannen en werpen, de geworpen speer | de speerworp; wachten met een gespannen speer (ademen, trillen, glimmen) en afbreken met springen, bukken of de andere kant op staan in `WORP_WACHT`, `thrAfbreken`, `thrWachtBij`, `thrWachtZet`, en er wordt nooit vanzelf gegooid; `speerNaastAmir` zet een speer waar Amir niet meer bij komt (achter of in een doornbos, boven op een terras dat hij van deze kant niet meer op komt) naast hem, nooit over een ravijn; `speerBereikbaar` rekent dat uit over de vloeren om hem heen |
| personages, dorpsdecor | NPC's, `VILLAGE`, de dorpsplaten |
| Amir zegt er iets van als hij geraakt wordt | `SFX_RAAK`, `playRaak()`: de twee kreten |
| Amir zegt iets als een vijand sterft | `SFX_RUST`, `vijandDood(baas)` (het bestand is 9 dB harder gemaakt, met een limiter): "ta soul, rest" na elke verslagen eindbaas en na een op de `DOOD_KANS` (7) andere vijanden; elke plek waar een vijand sterft roept `vijandDood` aan |
| stap voor stap leren spelen | het `tutorial`-systeem (staat klaar, geen level gebruikt het nu) |
| gaten in de grond | `gaps`, de overkant, de nevel en de diepte; de laag die eronder doorloopt is `grondDoorlopen`, in de bodemsectie |
| stof, sneeuwval, het weer | deeltjes en het weerplan per potje |
| het weer: regen, onweer, zandstorm, sneeuw en sneeuwstorm | `WEER`, `weerDoel`, `updateWeer`, `drawWeer`, `weerWind`, `weerGeluid`: het veld `weer` van een level (zie "het weer" hieronder) |
| vegetatie, water, doornbos | `props`, `water`, `thickets` |
| schilden in de wind | `SCHILD`, `schildStofUpdate`, `schildTil`, `drawSchildStof`: een schild (`schild: true` in `PROPS`) is een windscherm; bij een vlaag stuwt er stof tegen de windkant op, dat eroverheen waait. De plaatjes in `design/schilden/` zijn zelf de bron (het donkere motief van het klauwenschild is er met de hand in teruggezet) |
| slangen: kleur, zicht en patrouille | `SNAKE_DIRS`, `slangZiet`, `startPatrouille`, `slangSchuif` |
| zwarte panter, de witte panter, de hyena | de grote vijanden |
| baviaan: de eindbaas in wording | `BAVIAAN`, `baviaanLaad`, `baviaanTeken`: nog alleen een plaatje (`enemies/baviaan/baviaan.png`, uit `tools/baviaan_knip.py`, dat de magenta achtergrond van `baviaan_base_magenta.png` ontmengt), zonder gedrag. In de sandbox onder Vijanden, Baviaan (`sbBaviaan`, `sbBavStap`): neerzetten, schuiven, van maat veranderen en spiegelen; `level.baviaan = {x, y, s, f}`, `y` en `s` in Amir. De afzet (`BAV_AFZET`, `bavStand`, `bavAfzetWissel`): 44 frames in `enemies/baviaan/afzet/` op een gedeeld canvas, een keer; tot frame 8 heeft hij zijn arm nog aan de wand (op 15 per seconde, `delen`); een schaal voor de hele reeks uit het kader van de baviaan in frame 0 (`kader`), zodat hij precies over het losse plaatje valt. Het hangen, de afzet en de val zijn kleiner getekend dan de staande frames (zijn kop zo'n 60 bronpixels tegen 80 tot 90), dus die tekent het spel `BAV_GROEI.hang` (1,12) keer zo groot (1,25 maakte hem even groot, maar hangend te fors; zo lijkt hij aan de wand wat kleiner en richt hij zich na de landing op tot iets groters), vanuit de grondlijn van het canvas, ook het losse plaatje; in de landing loopt dat tot frame `tot` (10) zacht terug naar 1 (`bavGroei`, het veld `groei` uit `bavStand`), zodat het krimpen in het opvangen valt en de overgang naar de brul naadloos blijft. De schaduw, het stof bij de landing (`bavBronX`) en de camera (`bavKijk`) rekenen die groei mee. Zijn schaduw is die van Amir (`bavSchaduw` roept `drawAmirSchaduw` aan, en vervaagt met hem als hij doodgaat): zijn eigen frame als silhouet, een omgevingsschaduw recht onder hem en een zonneschaduw van de zon af, met de voeten op de grondlijn van het canvas (rij 576, bij de sprong `BAV_SPRONG.grond` 770); hoog aan de wand is er nog niets, in de val komt hij op. Bij frame `los` (10) laat hij los: vanaf daar maakt het hele canvas een valboog (vooruit met `vx`, eerst even `op` omhoog, omlaag met `zwaar` keer `GRAVITY`, want met de zwaartekracht van Amir zweefde hij naar beneden; `bavValDuur`) en speelt de rest van de afzet (oprollen en uitstrekken) in de lucht, uitgerekt over de valtijd, op minstens `luchtMin` per seconde. Eerst viel hij pas bij frame 32 en hing hij daarvoor opgerold stil in de lucht. Is de afzet op en valt hij nog, dan de val (`BAV_VAL`): 8 frames in `enemies/baviaan/val/` op hetzelfde canvas en dezelfde schaal, als lus. De val stopt als de grondlijn van het canvas (`grond`, bronrij 575) de grond raakt, 40 bronpixels onder zijn handen. De landing (`BAV_LANDING`): 25 frames in `enemies/baviaan/landing/`, een keer, en dan het laatste, met het tempo per stuk in `delen`: frame 0 tot 4 op 40 per seconde (zijn handen reiken naar de grond en vangen de klap, in frame 4 tot 6 tot 10 bronpixels eronder, zo bedoeld), de rest op 24 (op 12 zag je elke stap; samen nu 0,9 seconde). Hij begint `vroeg` (0,05) seconde voor het canvas de grond raakt, en daarna loopt de vaart vooruit in `uit` (0,12) seconde uit, zodat hij niet in een beeld stilstaat. Van 1,5 Amir hoog duurt de val zo 0,43 seconde. Waar hij de grond raakt stuift het op (`BAV_STOF`, `bavStof`, met de plek uit de frames via `bavBronX`): een lage wolk en korrels bij de klap van de wand (landing frame 3 en 5) en na een sprong (sprong frame 23, de afzet op 6), een wolkje en wat korrels achter elke pas (run frame 4 en 10), en remstof naar voren aan het eind van de uitval van een hap, als hij uit zijn run stilhoudt bij de kooi en als hij omdraait. In de sneeuw (Winter World, of het veld `sneeuw` vanaf `sneeuwVanaf`) is dat poedersneeuw en kristallen (`snowBurst`, `snowFxPush`), in het water of boven een ravijn niets. De zandwolken staan in `wdust` met een eigen dekking (`a`, `BAV_STOF.dicht`), want `stofwolk.png` is ijl, en met `zweef`: ze remmen af en stijgen langzaam op in plaats van te vallen, komen zacht op en blijven langer dicht (en `lang` per soort laat ze langer hangen), zodat het een wolk is en geen sliert. Als hij dood neerploft een brede wolk langs zijn hele lijf (`plof`, op dood_18) en eerst wat remstof bij zijn handen (dood_16). Direct daarna de brul (`BAV_BRUL`): 24 frames in `enemies/baviaan/brul/`, een keer, en dan het laatste, met het geluid `sounds/babrawr.mp3` (`bavBrulSnd`, ook in `geluidOntgrendel`), op gewoon volume (`geluid.vol` 1): de eerste van de twee brullen. Het tempo loopt mee met het geluid (`delen`, met `deelFrame` en `deelTijd`): overeind komen (0 tot 6) op 20 per seconde (daar springt hij 25 tot 33 bronpixels per frame), de bek wijd open (7 tot 19) op 10 zodat dat over het luide stuk van 1,3 seconde valt, dicht (20 tot 23) over het uitsterven; het geluid start 0,05 seconde voor frame 7, een keer per afzet; brul_00 is de pose van het laatste landingsframe. Dat canvas is 542 breed in plaats van 493 en begint 44 bronpixels links van het landingscanvas (`links`, in `bavStand` als `ox`), met dezelfde bovenkant, grondlijn en schaal; gespiegeld schuift het vanzelf naar rechts. Na de brul loopt nu de grommende idle (`BAV_IDLE_GROM`, zijn hoofd-idle op de grond): 39 frames in `enemies/baviaan/idle_grom/` als naadloze lus, op hetzelfde canvas als de brul, met `enemies/baviaan/idle_grom_metadata.json` erbij. Welke idle er na de brul loopt kiest `BAV_NA_BRUL` (`'grom'` of `'opgefokt'`); er wordt niet tussen die twee gewisseld. Met `'opgefokt'` loopt de opgefokte idle (`BAV_IDLE_OP`): 12 frames in `enemies/baviaan/idle_opgefokt/` als lus, op precies hetzelfde canvas als de brul. Daartussen komt later nog een korte opstaan-animatie; tot die er is verspringt de houding daar even. Na de brul volgt een vast verloop (`BAV_VERLOOP`, `bavRustStand`): idle, hoofdschudden (`BAV_SCHUD`, 64 frames in `enemies/baviaan/hoofdschudden/`, op hetzelfde canvas, met de shake een keer extra rond (`herhaal`: frame 46 is precies frame 18, dus 18 tot 45 is een naadloze ronde; `bavSchudReeks`), samen 2,2 seconden, en met het grommen `sounds/bavgrom.mp3` erbij: `bavGromSpeel` bij het begin van elk schudden, via een eigen gain op de versterker van de brul (`bavGromGain`), ook in `geluidOntgrendel`; de aangeleverde monkey growl geknipt tot 2,23 seconden, van 0,03 tot 2,26, zodat de uithalen op de shake vallen en het uitsterven op het weer omhoog komen), idle, en de grote brul (`BAV_ROAR.groot`), en dan stormt hij (`BAV_RUN`). Er zijn dus twee brullen: de eerste bij de landing op gewoon volume, en de grote, drie keer zo hard. De grote zijn de brulframes vanaf frame 6 (`van`: brul_00 is de lage landingshouding, en uit de rechtop staande idle zakte hij dan eerst door zijn knieen) met een eigen tempo per stuk, en `babrawr.mp3` veel harder (`vol` 3, boven 1 via `bavBrulVersterker`, ook in `geluidOntgrendel`) en trager en dieper (`rate` 0,8, zonder vaste toonhoogte), via `bavBrulSpeel(vol, rate)`. Van frame 7 tot 20 (`tril`) trilt het scherm licht (`shake`), rommelt de aarde zacht (`bavBeving`: het geluid van een ravijn dat openscheurt, `deurSnd` via `deurVersterker`, op `beving` van zijn volume) en trillen er steentjes op de grond (`BAV_STENEN`, `bavStenenStart`, `bavStenenTeken`: dezelfde steentjes als rond een openscheurend ravijn, `ravijnStenenNu`, verspreid over het beeld maar niet op een kei, getekend direct na de grond in `scene()` zodat het decor eroverheen valt, en een paar pixels hoog, zoals bij het ravijn). Van de landing tot hij stormt zo'n 7 seconden. De run: 17 frames in `enemies/baviaan/run/` als lus, canvas 790 bij 592, dat 108 bronpixels links van het canvas van de brul begint (`links` is dus 44 plus 108), met de grondlijn ook op rij 575. Hij rent even snel als Amir sprint (`bavV`: `v`, 495 wereld-px per seconde, 330 lopend maal 1,5 met Shift, maal `walkK()` als je Amir in de instellingen trager of sneller zet). Alles van de baviaan loopt op speltijd (`bavKlok`, in de lus opgeteld met `dt`), niet op `performance.now()`: op een telefoon zet het spel het tempo lager (`gameTempo`, zo'n 0,75) en daar moet hij in meelopen, anders is hij daar sneller dan Amir; in de pauze staat hij stil, zodat je hem niet ontloopt, en het tempo van de frames loopt mee zodat zijn voeten niet glijden: de voet op de grond schuift in de frames `pas` (40) bronpixels per frame naar achteren, dus v / (pas maal de schaal) frames per seconde, op 1280 bij 720 zo'n 34, geklemd tussen `fpsMin` en `fpsMax` (20 en 36). Hij volgt de grond onder zich. Na het verloop is hij een tegenstander (`bavVecht`, `bavGevecht`, `BAV_VECHT`): hij rent op Amir af en draait om aan het begin van een pas als Amir achter hem staat; zijn plek staat dan in `r.wx` (wereld-px vanaf `b.x`, los van de kant waar hij op kijkt). Komt de voorkant van zijn lijf binnen het bereik van Amirs speerstoot (`BAV_HAP.speer`: de verste punt uit `TIP_DX` plus de punt zelf, 333 eenheden, en `marge`), dan hapt hij meteen, midden in een pas (`BAV_HAP`): 26 frames in `enemies/baviaan/hap/`, op hetzelfde canvas als de run. Het tempo staat per stuk in `delen` (`bavHapFrame`, `bavHapTijd`): het opendoen en de uitval (frame 0 tot 10) in 0,12 seconde, het bijten (11 tot 13) en terugtrekken op 40 per seconde. In de uitval schiet hij het stuk tot Amir over (`uitval`, tot 1,6 Amir); zijn plek volgt daarbij de tijd, niet de beelden, zodat hij er ook bij een haperend beeld helemaal komt. Zo valt de beet samen met het moment dat je had kunnen steken, en zie je niet wie eerst was. Een kei tussen hem en Amir houdt hem tegen (regel 7), dus daar springt hij overheen (`BAV_SPRONG`): 32 frames in `enemies/baviaan/sprong/` op 24 per seconde, canvas 900 bij 800 met de grondlijn op rij 770, 154 bronpixels links en 195 boven het canvas van de brul (`links` 198, `boven` 195; `oy` in `bavStand`). De frames stijgen niet zelf: 10 tot 22 zweven al boven de grondlijn, en het spel tilt hem daarbovenop in een boog op, per kei zo hoog dat hij er met `marge` overheen komt (`zweeft`, `boog`). Vooruit per stuk in `snel` (in de hurk en de landing afgeremd, afzetten en de lucht 1,7 keer zijn rensnelheid, `bavSprongWeg`); hij zet af als het midden van zijn lijf halverwege de lucht boven het midden van de kei komt, en gaat na `sprong_29` terug naar run_00. Gemeten: in elk frame boven een kei 12 tot 105 px ruimte. Zolang hij aan de wand hangt speelt de hang-idle (`BAV_HANG`): 36 frames in `enemies/baviaan/hang_idle/`, 12 per seconde als lus, canvas 600 bij 960 zonder grondlijn, niet bijgesneden; het hangt aan de greep (bronpixel 545, 28), en die komt precies waar zijn hand in afzet_00 zit (`afzetGreep`, met `maat` voor de schaal), dus bij de afzet verspringt de hand niet. Met `zicht: 'ver'` begint Amir zo ver van hem als kan terwijl hij hem nog ziet (`BAV_VER.rand`, `startWereld`), en met `skelet` staat het eerste skelet van het level op dat deel van de weg naar hem toe, kijkt Amir naar hem, en zet de baviaan pas af als de speer eruit is, als Amir dichterbij komt (`nader`) of als hij `weg` px de andere kant op loopt (`bavWakker`). `geenSpeer: true` in een level zet er geen speer voor je in de grond. In een level staat hij in het veld `baviaan` (`{x, y, s, f, zicht, kooi, beet}`, `readLevel` zet er `lvl` en `f0` bij; met `beet: true` hangt hij niet maar staat hij op de grond voor de speerbeet, zie hieronder): hij hangt aan de wand tot Amir `BAV_START` px gelopen heeft vanaf waar hij begon (`b.start`). Met `zicht` (een deel van de schermbreedte) begint Amir niet op 0 maar zo dat de baviaan daar in beeld hangt (`startWereld`, in `restart`; zijn speer staat dan `SPEAR_AHEAD` voor die plek): Amir staat in het midden, dus op een telefoon begint hij dichter bij de baviaan dan op een laptop, en nooit dichter dan 50 px bij de rotswand. Zolang hij hangt of valt kijkt de camera wat omhoog (`bavKijk`, `BAV_KIJK`, in `updateCamera`; na een herstart meteen, `bavKijkNu`), zodat hij ook op een telefoon met de knoppen erbij helemaal in beeld hangt; bij de landing (`b.geland`) zakt hij terug. In Test 15 en 16 hangt hij zo op x 720 en 1,6 Amir hoog tegen de rotswand achter de hut (`zicht` 0,68), en de eerste tip komt pas als je gaat lopen (x 300), want in het begin viel hij op een telefoon over de baviaan en speelt dan het hele stuk af, en `restart` hangt hem terug. De sprong heeft stukken (`bavSprongDelen(rek, maal)`, met `deelFrame` en `deelTijd`): bij een kei is de lucht zoals hij was, over de kooi duurt de lucht langer en gaat hij sneller. De kooi (`kooi`: de x van twee ravijnen, `bavKooi`, `bavKooiKant`, `BAV_KOOI`): de baviaan komt nooit op het stuk ertussen. Vlucht Amir de kooi in van de kant waar de baviaan staat, dan rent hij naar de rand en springt over allebei de ravijnen naar de overkant; gaat Amir eruit aan de andere kant, dan springt hij meteen en landt hij voor Amir. Na zo'n sprong draait hij om en brult (fase `brul`, met het geluid via `bavBrulSpeel`); staat Amir in de kooi, dan wacht hij grommend (fase `wacht`), en over een ravijn van de kooi hapt hij nooit. Test 15 is het proefstuk. In de sandbox zet Neerzetten met Van rechts (achter Amir) er twee keien voor Amir bij (`BAV_KEIEN`, 520 en 1250 px voor hem uit), waar Amir overheen springt en de baviaan dus ook. Bij elke hap klinkt `sounds/bavbijt.mp3` (`BAV_BIJT`, `bavBijtSpeel`: de aangeleverde bijtmonster met de 0,4 seconde stilte vooraan eraf, zodat de aanzet op de uitval valt), en aan het begin van elke aanval (na de grote brul en na elke rust) gromt hij een keer, trager en dieper (`BAV_REN_GROM`, `bavRenGrom`, op een eigen audio-element `bavRenSnd`; een hap zet hem stil). Onder het rennen hoor je zijn poten (`BAV_POOT`, `bavPoot`): gemaakt met de Web Audio API, een korte dreun die in toonhoogte zakt met een tik zand erbovenop, op de run-frames waar een poot neerkomt (4 en 6 de handen, 10 de achterpoten), elke keer iets anders en zachter naarmate hij verder van Amir is. De klap op de grond (`BAV_LAND`, `bavLandSpeel`, `sounds/bavland.mp3`: de aangeleverde "babboon fall en land" met de 0,22 seconde stilte vooraan eraf) klinkt als hij van de wand neerkomt (op landing frame 3), na een sprong (zachter, `sprong`) en als hij dood voorover klapt (dood_18, `doodF`, met een stofwolk), `voor` seconden vooraf gestart zodat de klap op het frame valt). Alle geluiden van de baviaan gaan via een eigen gain op de versterker van de brul (`bavSpeelVia`) en staan in `geluidOntgrendel`. Raakt hij, dan staat hij `rust` (2) seconden grommend stil en rent weer; mis is meteen weer rennen. Zo is hij niet te verslaan (`BAV_VECHT.raakbaar` staat uit): een steek of de lage zwaai doet hem niets en een geworpen speer ketst af. Met `raakbaar` aan doodt een klap hem (`bavRaak`), net als de speerval, met eerst een drama (`BAV_DRAMA`) zodat de speler denkt dat hij nog leeft: bevroren op het frame van de klap, wit oplichtend (`bavWit`, `flits` in de stand), het scherm schokt en hij deinst terug; dan dreigt hij grommend (de grom-idle met de grom), brult de grote brul met het trillen, het gerommel en de steentjes (`bavBrulEffect`, hetzelfde als in het verloop), twijfelt (de grom-idle vertraagd, stil), en dan bam: een flits en een schok, en hij zakt in elkaar (`BAV_DOOD`: 22 frames in `enemies/baviaan/dood/` op 24 per seconde, een keer, zo'n 0,92 seconde; 00 tot 03 de klap, 04 tot 09 zakken, 10 tot 15 zijn poten begeven het, 16 tot 19 voorover, 20 en 21 dood). Daarna blijft `dood_21` liggen, als lijk, zonder te vervagen, met zijn schaduw. Canvas 830 bij 592, grondlijn op rij 575, 140 bronpixels links van het canvas van de brul (`links` 184, dus 32 links van de run en de hap). De frames zijn aangeleverd zoals ze zijn: niet bijsnijden, schalen of opnieuw opslaan. `vijandDood(true)` ("ta soul, rest") komt na `BAV_DRAMA.stil` seconden stilte na dood_21. Van de klap tot `los` seconden daarna staat Amir vast (`bavDramaNu`, `amirVast`: dezelfde plekken als de speerbeet, lopen, springen, stoten, zwaaien, E en bukken) en schuift de camera naar de baviaan toe (`bavFocusX`, via `camEase` zoals de arena, hoogstens `camMax` schermbreedte). Samen zo'n 6,8 seconden. In de sandbox doodt de knop Dood hem meteen (`bavDoodNu`), ook aan de wand of midden in het verloop. Het raakbare lijf komt uit het kader van zijn frame (`bavKader`, `bavGeo`), de bek is een vast vak in bronpixels (`BAV_VECHT.bek`, de kop met open kaken in hap_11 tot 13, 0,55 tot 1,06 Amir hoog: springen of bukken ontwijkt hem niet); met de hitboxen aan zie je ze. In vier van de aangeleverde frames waren handen en voeten uitgesmeerd tot een halfdoorzichtige vlek (run_00, 01 en 16) of ontbraken ze (de onderarm in run_12): `tools/baviaan_run_fix.py` maakt de speelversie in `enemies/baviaan/run/` uit de ongewijzigde bron in `enemies/baviaan/bron/run/`, door schone stukken uit andere frames erop te plakken (de hand van run_15, de achterpoot en de hand van run_02, de onderarm van run_13); de andere dertien frames kopieert het ongewijzigd. Verandert de bron, draai het dan opnieuw. De stukken idle staan in `BAV_VERLOOP.wacht` (een per stap, 0,5 tot 1,0 seconden, elke keer willekeurig). Bij de opgefokte idle begint het schudden op het einde van de lus, bij de grom meteen, want daar verspringt de houding toch al (het schudden begint en eindigt rechtop, de grom staat laag). Het tempo staat per stuk in `delen` (`bavSchudFrame`): omlaag en omhoog op 40 per seconde, de shake zelf (frame 18 tot 47) op 42, met een ronde extra samen 2,2 seconden. De stand daarvan staat in `bavRust`, niet in `level.baviaan`. K of de knop Hoofdschudden schudt meteen, zolang hij nog niet stormt (`bavSchudNu`). De val eindigt op de grond waar hij neerkomt, niet waar hij afzette (`bavLandPlek`): op een terras komt hij erbovenop, en hoe hoger hij hangt, hoe langer de val-lus doorloopt. In de sandbox hangt hij na Neerzetten op `BAVIAAN.hang` (1,5 Amir) en kan hij niet lager dan `minHang` (0,8), zodat er altijd een echte val is; J of de knop Afzet speelt het hele stuk af (afzet, val, landing, brul, het verloop met twee keer schudden, en dan stormt hij tot je nog een keer drukt), nog een keer is terug naar het plaatje. Staat niet in de kleine set |
| speerbeet: de baviaan pakt je speer | `BAV_BEET`, `BAV_MOND`, `BAV_SPEER`, `bavBeetStap` (in de lus, na de stoot: wanneer het begint, Amir vast met `beetVast`, de uitval, de klem, de ruk), `bavBeetStand` (vanuit `bavStand` als `level.baviaan.beet` staat: de grom-idle, hap_00 tot 25, het hoofdschudden), `bavBeetSpeer` (de speer in zijn bek, achter zijn kop, met het uiteinde aan een veer; hier breekt de schacht en vertrekt de punt), `bavBeetStukken` (de schacht en de splinters), `bavWerpTeken` (de punt naar de camera, na de voorgrond: hij blijft bijna op zijn plek en groeit op constante snelheid als 1 / (1 - afgelegd), draait het blad naar voren en wordt verkort zodat hij in de camera wijst, met de onscherpe en donkere trappen uit `beetSpeerMaak`), `bavZoef` (de zoef erbij: ruis door een bandfilter dat hoger en harder wordt, geen bestand, op `bavAc`), `beetKnipX` (Amirs speer houdt op bij de lip, geknipt bij het tekenen van Amir), `beetReset` (in `restart`). Alleen bestaande frames: de speer is Amirs eigen speer uit stootframe 6, de mond per frame is gemeten op de tanden. Had Amir de blauwe speer uit het skelet, dan houdt de speer in zijn bek dat blauwe vaantje (`r.blauw`, `beetSpeerMaak(blauw)` via `vaanBlauw`), en de punt naar de camera ook, bij de beet en bij de pootslag (`beetWerp.blauw`). De pootslag (`BAV_SLAG`, `bavSlagImgs`, `bavSlagLangFrame`): doet Amir binnen `pootslag` (1,8 Amir) de lage zwaai, dan slaat hij met `slag_kort` op de speer (fases `slag`, `druk`, `terug`): Amir blijft liggen in zwaaiframe `zwaai` (de hold staat in het zwaaiblok van de lus), de baviaan schuift tussen `schuifVan` en `schuifTot` tot de poot `poot` voor Amir neerkomt, en op de klap breekt de speer (`beetKnipZwaai` knipt in het zwaaiframe, rijen 405 tot 505), vliegt de punt vanaf de poot naar de camera en laat Amir aan het eind van het platdrukken de stomp vallen. Canvas 840 bij 680, grondlijn 640, `links` 234 en `boven` 65 (als `ox` en `oy` in de stand, met `grond` voor de schaduw); de frames in `enemies/baviaan/slag_kort/` en `slag_lang/` zijn aangeleverd zoals ze zijn. `slag_lang` (de aangekondigde, met de arm `dreig` seconden hoog) doet nog niets in het spel; in de sandbox laat **Pootslag lang** hem zien. Steekt Amir zelf binnen `slag` (1,7 Amir uitval), dan grijpt hij meteen; loopt hij gewoon door, dan pas bij `vast` (0,6), dus later. Zolang `beetVast` staat, doen springen, stoten, E en bukken niets. In de sandbox **Speerbeet** onder Vijanden, Baviaan (`sbbavbeet`). Baboon 1 is het proefstuk |
| speer in de baviaan: de speerval blijft in zijn borst zitten | `BAV_VALSPEER`, `bavSpeerTeken` (in `baviaanTeken`, na het frame en het witte oplichten), `bavSpeerFrame`, `bavSpeerHoek`: de speerval raakt hem van voren (hij rent op Amir af, Amir staat bij het zegel voor de klif), dan zet `bavGevecht` de speerval op `st: 'baviaan'` (`speervalTeken` slaat hem dan over) en `r.valSpeer` in zijn stand, en tekent de baviaan de speer, door het hele drama tot het lijk. Per frame staat in `anker` waar de plek op zijn borst is, in bronpixels van het canvas van die reeks (run, hap, idle_grom, brul, dood), uit `tools/baviaan_speer_anker.py`, dat een stukje vacht van frame tot frame volgt vanaf een paar punten die met de hand gekozen zijn; verandert een reeks, draai het dan opnieuw en plak de tabel erin. De sprong heeft geen anker (zijn lijf schiet over het canvas en het volgen raakt de weg kwijt): wordt hij daarin geraakt, dan zit de speer waar de punt hem raakte (`r.valSpeer.x`, `y`). De punt wijst zijn lijf in, `diep` zit erin en wordt weggegumd waar het frame is (rechts van de ingang, `destination-out` op een eigen canvas); de schacht draait mee met `hoek` per reeks (graden, + is de voorkant omlaag), en komt het uiteinde onder de grondlijn van het canvas (`grond`), dan gaat de speer dieper zijn lijf in, tot `maxDiep`. Kijkt hij naar rechts, dan raakt de speer hem van achteren en valt hij zoals na een misser. In de sandbox **Dood door speerval** onder Vijanden, Baviaan (`bavDoodNu(true)`) |
| voorgrond: de laag tussen de camera en Amir | `VOORGROND`, `VG_SOORT`, `VG_LAGEN`, `vgStandaard`, `drawVoorgrond`: onscherp gras, struiken, keien en een schedel vlak voor de camera, in twee lagen; schuift sneller dan de wereld, ook verticaal, en valt onder de grond weg. Elk level heeft er een (zie "de voorgrond hoort bij elk level") |
| achtergrondlagen, uitzicht per level | `SCENE0` en `SCENES` |
| startscherm, level maken, menu: kaartjes per level | menu en bouwer |
| level maken | de bouwer: `GEREEDSCHAP` (wat je neer kunt zetten), `bouwOpen` (de rand en de lijst), `bouwVelden` en `bouwExtra` (het venster), `tekenLijn` (de levellijn), `bouwD` en `bouwGeest` (Amir als geest), `bouwTesten` (testen vanaf hier), `holteMaak` en `holteTrap` (gangen), `bouwSchakelTeken` (koppelingen en raakvlakken); zie "De bouwer" hieronder |
| elk level nakijken op decor boven een ravijn | `schoonLevel`, draait bij elk level; `schoonKomend` en `komendeRavijnen` houden hutten, keien, doornbossen, skeletten en speertekens weg waar later een ravijn openscheurt (rune of zegel), en `placeProblem` in de bouwer ook |
| wat er staat waar een ravijn openscheurt | `RAVIJN_DECOR`, `ravijnDecor`, `ravijnDecorStap`: kalebassen, botten en dorpelingen vallen erin, planten, keien, doornbossen en de speer schuiven naar de rand of vervagen; alles in `rv` of `x0`, dus `ravijnReset` zet het terug |
| sandbox | de vrije testmodus |

Op schijf: `karakters/` (Amir, dorpeling, dorpelinge), `enemies/`, `design/` (decor,
achtergronden, water, dorp, botten), `klein/` (dezelfde mappen op halve grootte),
`music/` en `sounds/`, `tools/` (de Python-scripts), `icons/`, `sw.js` en
`offline-assets.json` (de webapp).

## Een level lezen of schrijven

Amir loopt naar links, dus alle `x` zijn negatief en lopen op naarmate je verder
komt. Een leveldefinitie is een gewoon object; de bouwer in het spel exporteert
precies hetzelfde formaat naar JSON.

| veld | wat |
| --- | --- |
| `name` | naam op het kaartje in het menu |
| `lagen` | sleutel uit `SCENES`: welk uitzicht dit level krijgt |
| `muziek` | sleutel uit `MUZIEK`: welk deuntje eronder loopt (`bg` voor het oude thema); zonder dit veld `MUZIEK_BASIS`, Dark Africa |
| `winter` | `true` zet het hele level in de sneeuw (witte dieren, sneeuwversies van het decor) |
| `sneeuw` | sneeuw op de grond, los van `winter`: `{soort, dek, van, tot}` (zie hieronder) |
| `weer` | het weer onderweg: `[{x, soort, sterkte}]`, `soort` uit `WEER.soorten` (`droog`, `regen`, `onweer`, `zandstorm`, `sneeuw`, `sneeuwstorm`); voorbij `x` slaat het om (zie "het weer") |
| `valschade` | `true` laat een diepe val een of twee levens kosten (standaard uit) |
| `worp` | `'schaal'` zet de schaalworp aan: de hoek loopt op zolang je vasthoudt, van vlak tot 30 graden (`THR_HOEK_MAX`); zonder dit veld de twee trappen. In de sandbox de knop Worp onder Speerworp |
| `rocks` | keien om op te springen: `{x, s}` |
| `spawns` | vijanden: `{x, k}` met `k` = `groen`, `zwart`, `scorp`, `hyenas`, `panter`, `zwaard` (met `c`), `fosfor`; een panter met `over: true` mag over keien en ravijnen (zie regel 7) |
| `props` | decor: `{x, k, s, f, v}`, `k` uit `PROPS`, `f` spiegelen, `v` verre laag |
| `village` | dorpsplaten uit `VILLAGE`: `{id, x, depth, flip}` |
| `gaps` | ravijnen: `{x, w}` |
| `water` | poelen: `{x, n}` met `n` = aantal middenstukken |
| `thickets` | doornbossen: `{x, n, seed}` |
| `terraces` | terrassen om op te klimmen: `{r, l, h}` (rechterrand, linkerrand, hoogte); met een negatieve `h` een trede in een gang |
| `holtes` | gangen onder de grond: `{r, l, diep}`, een ravijn erboven is de ingang, een gat met treden de uitgang (zie hieronder) |
| `ledges` | richels aan een wand: `{x, h, s}` |
| `grotten` | rotsgebieden als raster: `{x, cel, y, grid, ...}` (zie hieronder) |
| `plafond` | de rots boven je als hoogtelijn: `[{x, y}, ...]` (zie hieronder) |
| `muur` | de rotswand met het rune-symbool: `{x, speer}`, of met `soort: 'grot'` de rotsboog met de kei (zie hieronder) |
| `hppotions` | drinkkalebassen: `{x, y}` |
| `skeletten` | een zittend skelet met een speer erin: `{x, f}`, `x` is het midden van het skelet, `f` spiegelt; E bij de schacht trekt hem eruit (zie hieronder) |
| `tekens` | speertekens: `{x, v, f}`, `v` is `teken`, `gebroken`, `gekruist`, `jagers` of `kalebas`, `f` spiegelt; decor, behalve dat het mes de kalebas lossnijdt |
| `talentKeuze` | `true`: voor het begin kies je zelf welke talents gelden, van alle tribes (alleen voor een Test level; nu Test 14) |
| `zegels` | zegels plat in de grond: `{x, ravijn, sluit, breed, muur, speerval, teken, vijand}`; `teken` is een sleutel uit `ZEGEL_TEKENS` (standaard `rune`, met `vijand` `teken2`; zie `notities/zegeltekens.md`), en met `vijand: true` zet ook een vijand hem aan: een `ravijn` op de x van het zegel zelf is dan een val (en geen FOUT in `levelcheck.py`); erop stappen zet hem aan of uit, en met `ravijn` scheurt de grond daar open als hij aangaat, `breed` breed (standaard 277). Met `sluit` gaat het open ravijn op die x juist weer dicht (staat er niets open, dan blijft hij donker). Met `muur: true` opent hij de rotswand van het level (`zegelMuur`); de rune op de wand werkt daarnaast gewoon. Met `speerval` (een x) schiet hij de speer in die rotswand los; zit die niet in de wand, dan blijft hij donker |
| `speervallen` | speren in de rotswand: `{x, h}`, `x` de klif waar hij in zit (uit `cliffs`), `h` de hoogte in Amir (standaard 0,82); een zegel met `speerval` schiet hem los (zie "speerval") |
| `runes` | ravijnen met een rune op een rots ervoor: `{x, breed, rots, groot, hoog, doel}`, `x` het midden van het ravijn; de rots komt vanzelf aan de kant waar Amir aankomt. `rots` is de plaat uit `RUNE_ROTSEN` (standaard de spits), `groot` de hoogte van de rots en `hoog` die van de schijf, allebei in Amir (standaard 3,5 en 0,76). Met `doel: true` opent hij niets maar gloeit hij op en blijft hij aan, en is `x` de linkervoet van de rots (zie "runes op elke rots"). Oudere levels hebben ze nog op naam in `RAVIJN_PROEF` (Test 6 en Test 9); staat het veld er, dan telt het veld |
| `fg` | strook waarover de voorgrondbegroeiing ligt: `{from, to}` |
| `voorgrond` | de onscherpe laag vlak voor de camera: `{stroken: [{van, tot, dicht, struik, kei}], los: [{x, k, s, f}]}`, `k` uit `VG_SOORT`; los van `fg`. Zonder dit veld krijgt het level de standaard, met `false` heeft het er geen (zie hieronder) |
| `arena` | het veld van de eindbaas: `{c}` |
| `cliffs` | de afsluitende rotswand: `{x}`, staat altijd achter `ends` |
| `ends` | de fakkels die het level uitspelen: `{x}` |
| `npcs` | dorpelingen: `{x, k, f, s}` |
| `tips` | tekst onderweg: `{x, t}` |
| `tutorial` | stapjes met uitleg (nu door geen level gebruikt) |

### Bodem en sneeuwdek: grijs en rood zijn twee verschillende dingen

`winter: true` is de complete uitrusting van episode Winter World: witte dieren, sneeuw
op alles wat je beklimt, en een grond waarin sneeuw en grijze steen in één tegel zijn
gebakken. Dat is de bergversie en die blijft zoals hij is.

Het veld `sneeuw` beantwoordt een andere vraag: ligt hier sneeuw op de grond, en op wat
voor grond. Twee dingen die los van elkaar staan:

| | |
| --- | --- |
| `soort: 'savanne'` | de rode grond van de savanne, en die blijft rood onder de sneeuw |
| `soort: 'rots'` | dezelfde grond als grijze steen: een rotsbodem, ook zonder sneeuw |
| `dek` | hoeveel sneeuw er ligt, 0 tot 1 (standaard 1) |
| `van` en `tot` | alleen samen: het dek loopt op van niets op `van` tot vol op `tot` |

Kies dus bewust. Grijs is een steensoort, geen gevolg van sneeuw: een ondergesneeuwde
zandvlakte is onder die sneeuw nog altijd rood zand, en dat zie je ook, want het dek
laat overal plekken grond vrij. Vraagt iemand om een besneeuwd savannelevel, dan is dat
`soort: 'savanne'`; gaat het om een kale steenvlakte of een hoogvlakte, dan `'rots'`.

Amir loopt naar links, dus `tot` is negatiever dan `van`:

```
sneeuw: { soort: 'savanne', van: -1200, tot: -7000 }
```

Het dek zelf zijn vier doorzichtige lagen (`design/sneeuwlaag_25` tot `100`) die genest
zijn: wat op 25 wit is, is dat op 50 ook. De overgang van de ene stand naar de volgende
is daardoor alleen sneeuw die erbij komt, en die grens loopt grillig, zodat je nergens
een rechte streep over de grond ziet. Zet je een nieuwe stand bij, houd die nesting dan
intact, anders knippert er sneeuw weg terwijl je loopt.

Wat nu nog niet meeloopt: de rotsen, de klimstukken, het gras en de dieren hebben alleen
een aan-of-uit sneeuwversie. Loop je door een overgang, dan springen die er in één keer
om. Dat is bewust buiten deze wijziging gelaten.

`schoonLevel` kijkt elk level bij het laden na en schuift decor dat boven een ravijn
staat naar de kant, of haalt het weg (behalve binnen een gang: daar staat het op de bodem). Reken daar niet op als ontwerper: zet het
meteen goed.

### Het weer

Een level zet het weer met `weer: [{x, soort, sterkte}]`. Voorbij `x` geldt die soort tot het
volgende punt, de overgang loopt over `WEER.overgang` px en voor het eerste punt is het droog.
Zonder het veld blijft het oude gedrag: in een winterlevel het sneeuwplan per potje (`planSnow`),
verder geen weer. `sterkte` is standaard 1, hoogstens 1,5.

Elke soort is een mengsel van zes lagen (`WEER.lagen`: regen, onweer, storm, zand, sneeuw, jacht),
zodat de ene soort in de andere overloopt. De sneeuw zijn de gewone vlokken: `updateSnowfall`
vraagt `weerDoel()` en sneeuwt dan ook buiten een winterlevel. Wil je de grond ook wit, zet er dan
het veld `sneeuw` bij met dezelfde `van`.

Drie keuzes die vastliggen:

- **Weer maakt het beeld niet donkerder.** Geen waas over de lucht en geen donkere laag: regen maakt
  het hooguit een zweem koeler (`WEER.koel`), een storm legt alleen vlak boven de grond een stuifband.
  Zo is het gevraagd.
- **Een storm is een vlaag die niet ophoudt.** `weerWind` zet `gust` op een vlaag over de hele kaart
  (`gust.weer`), met een amplitude die golft. Alles wat al op `windAt` reageert gaat zo vanzelf mee;
  de planten gaan in een storm verder plat en fladderen sneller (`WEER.storm.buig`, `fladder`, in
  `drawVeg`). Waait het harder dan 1, dan staat een doek strak (`tekenWind` klemt op 1). Een nieuw
  ding dat in de wind beweegt hoeft dus alleen `windAt` te gebruiken.
- **Geluid**: de storm is `music/woestijnwind.mp3` als lus door een versterker (`stormSnd`,
  `weerVersterker`), de regen en de donder zijn gefilterde ruis uit de Web Audio API. Alles hangt aan
  `weerAc`, die `geluidOntgrendel` bij een tik op gang zet. Onder de grond klinkt het gedempt, en er
  valt geen weer (`holteDiepT`, net als de sneeuw).

Nog niet: onder een plafond of in een grot regent het gewoon door, en planten en keien hebben in de
sneeuw alleen hun aan-of-uit sneeuwversie. In de sandbox onder **Weer**; Test 13 laat alles zien.

### Wat mag waar: vast, los, plant en ver

Elk ding in een level valt in een van vier soorten, en de soort bepaalt wat er gebeurt bij een
ravijn, bij een ravijn dat later openscheurt (een rune of een zegel) en in een gang.

| soort | wat | boven een ravijn | waar later een ravijn openscheurt | in een gang |
| --- | --- | --- | --- | --- |
| vast | keien, hutten en andere props met `bouwwerk`, doornbossen, skeletten, speertekens | nooit | nooit: ze gaan naar de rand | op de bodem, en niet hoger dan de gang |
| los | botten (`RAVIJN_DECOR.valt`), kalebassen, dorpelingen | nooit | mag: het valt erin | op de bodem |
| plant | gras, struik, boom, schilden en ander laag decor | nooit | mag: het schuift naar de rand, of vervaagt als daar al iets staat | op de bodem, en niet hoger dan de gang |
| ver | props met `v` die hoger staan dan `FAR_GAP_LIFT` | mag | mag | blijft boven op de savanne |

Wat Amir tegenhoudt staat daar los van: een kei draagt (je springt erop), een doornbos houdt je
tegen tot je hem kapt, en al het andere is decor waar je doorheen loopt.

De soort staat niet op een plek, maar zit in vijf functies. Een nieuw ding krijgt dus eerst een
soort, en komt dan in alle vijf:

1. `schoonLevel`: schuift het uit een ravijn bij het laden (behalve ver decor);
2. `schoonKomend`: schuift vaste dingen weg waar later een ravijn openscheurt;
3. `ravijnDecor` en `ravijnDecorReset`: wat er gebeurt als het ravijn toch onder iets openscheurt
   (in de sandbox), en dat een herstart het terugzet (`x0` of `rv`);
4. `tools/levelcheck.py`: de regels `boven een ravijn`, `waar een ravijn openscheurt` en `onder de
   grond`, met de maten uit de code;
5. `placeProblem`, als het in de bouwer neer te zetten is. Skeletten en speertekens staan er
   sinds de nieuwe bouwer ook in (`skelet` en `teken`).

Voor een speerteken staan de maten per variant in `TEKEN.varianten`: `voet` is van waar tot waar
het op de grond staat (het liggende stuk en de schedels in het zand tellen mee, dus niet
symmetrisch om `x`), `hoog` tot waar de speer reikt. Een teken is 0,86 tot 1,34 Amir hoog, dus
in een gang minder diep dan zo'n 530 steekt de speer door het dak.

### Rots als een raster van cellen

Een rotsgebied is geen kamer maar terrein: een raster waarin elke cel vol of leeg is.
Amir loopt door de lege cellen, en rots kan net zo goed boven of naast hem zitten als
eronder. Je tekent het met de hand uit.

| veld | wat |
| --- | --- |
| `x` | wereld-x van de linkerrand van het raster (dus negatief) |
| `cel` | celbreedte in wereld-px (standaard `GROT_CEL`, 120) |
| `hoog` | celhoogte, als factor op de standaard (standaard 1 = 150 eenheden) |
| `y` | onderrand van het raster boven de grondlijn, in cellen (standaard 0) |
| `grid` | de rijen van boven naar beneden; `#` is vol, al het andere leeg |
| `seed` | dezelfde seed geeft elke keer dezelfde verstrooiing |
| `strooi` | hangblokken, richels en keien vanzelf neerzetten (standaard `true`) |
| `massief` | de volle cellen blokkeren (standaard `true`) |
| `decor` | met de hand erbij: `[{k, x, y, f, s}]` |

Een cel heeft twee maten, en dat is met opzet, want het spel rekent zo overal. De
**breedte** staat in wereld-px en ligt dus vast, net als bij `gaps`, `terraces` en `rocks`,
en net als Amir zijn looptempo. De **hoogte** staat in sprite-eenheden (`GROT_HOOG * CHAR_H`
= 150, precies een terrastrede) en schaalt dus mee met Amir, net als `terraces.h`.

Dat verschil is niet vrijblijvend. Zou de hoogte ook in wereld-px staan, dan komt Amir op
een kort scherm kleiner uit terwijl de cel gelijk blijft, en is een blok van één cel ineens
niet meer te halen. Nu is een cel overal 150 eenheden en Amir zijn sprong overal 200, dus
één cel klim je altijd, twee cellen nooit. Op een telefoon zijn cellen daardoor breder dan
hoog en op een groot scherm hoger dan breed; rond het standaardformaat zijn ze vierkant.
De losse stukken worden allemaal op één schaal getekend (zie hieronder), dus er wordt
nergens iets uitgerekt.

Wat dat voor het ontwerp betekent: één cel is een trede, twee cellen is een gang waar je
rechtop door loopt maar je hoofd stoot als je springt, drie cellen is ruim, en een gat van
één cel hoogte kun je niet in.

Buiten het raster is het lucht, behalve onder de laatste rij: daar loopt de aarde door.
De bovenkant van je rots is dus ook de bovenkant van het level, met de hemel erboven.
Moet de massa doorlopen tot buiten beeld, maak het raster dan hoger.

### Rots is hetzelfde gesteente als een terras

Dit is de kern, en het is de derde poging: een rotsgebied krijgt geen eigen steensoort.
Elke volle cel hangt onder precies een cel waarvan de buur boven leeg is (loop je van een
volle cel omhoog, dan kom je daar altijd uit), en zo'n bovenrand met de massa eronder is
niets anders dan een terras van een paar cellen breed. Daarom tekent `grotMassa` de massa
met `klif_bovenrand.png` zelf, op `terScale(scale)`, precies zoals `drawClimb` een terras
tekent: middenstukken om en om gespiegeld, en aan een open kant de afbrokkelende rand van
het plaatje. Een rotsblok is daarmee van hetzelfde steen als de terrassen ernaast, en de
winterversie loopt automatisch mee, want `terPic()` regelt dat al.

Wat daarvoor stond, klopte niet: een eigen vlakke massa (`GROT_MASSA`) met een lichte band
eronder, in een andere kleur en een andere korrel dan de vloer. Dat leest als een grijze
rechthoek naast het level, hoe je die kleur ook kiest. Een getegelde textuur in plaats van
die vlakke kleur is niet beter: elk ander plaatje is net iets lichter of donkerder dan de
band, en dan ligt elke rand als een rechthoek in de rots.

Wat een terras niet heeft is een onderkant, want daar kom je bij een terras nooit. Dat is
het enige waar de grotset nog voor nodig is:

| buur leeg | wat erop komt |
| --- | --- |
| boven | het bovenvlak van het terrasplaatje: je loopt erop zoals je op een terras loopt |
| links of rechts | de afbrokkelende rand van datzelfde plaatje, over de rijen waar die kant echt open ligt |
| onder | de tanden van `plafond_strook.png`, horizontaal getegeld |

De zijkanten staan niet kaarsrecht: `grotSilPad` breekt ze open met `terJag`, dezelfde golf
die de zijkant van een terras openbreekt, geklemd op `GROT_JAG` (0,16) van een cel. De
botsing blijft wel op de celrand liggen, dus die hap mag niet groter worden. Waar de rots
zijdelings doorloopt blijft de naad recht en valt hij onder het buurstuk.

De ribbels van de wand liggen op een raster dat aan het hele gebied hangt, niet aan een los
stuk massa. Doe je dat niet, dan zet een stuk de wand halverwege opnieuw in en loopt er een
naad door het steen. Hetzelfde geldt voor de fase van de plafondtanden.

Van `plafond_strook.png` komt alleen wat onder de plafondlijn hangt in beeld: rij 433 tot
508 is massief steen (`GROT.band.dicht`) en dat deel wordt weggeknipt, rij 509 tot 592 is
de tandenrand en die hangt in de open ruimte, met een donkere contour eronder
(`grotSilhouet`), zoals de aardlaag van de grond er ook een heeft. Teken je dat massieve
deel wel, dan ligt er een lichte plaat met een kaarsrechte bovenkant op de wand, en precies
dat leest als een rechthoek op de rots.

De band wordt op `grotSteen()` getekend, 1,35 keer de schaal van de grondrand: groot genoeg
om als rots te lezen, en lichter dan de grondband. Op 2,1 zijn de brokken boven en onder
precies even groot, maar dan wordt de band twee keer zo zwaar als de vloer en vult hij het
halve scherm.

De rijen van `GROT.band` staan in de maten van `grot.json`, dus in de grote bron. Op een
telefoon komt hetzelfde plaatje op halve grootte uit `klein/`, en dan ligt rij 433 buiten
het plaatje. `grotTegelSet` schaalt die snee daarom mee met de werkelijke bronbreedte. Sla
je dat over, dan valt op een telefoon de hele band weg en hangt er niets aan het plafond,
zonder dat er iets in de console staat.

Wat de set niet heeft vullen de brokken op:

- waar een vloer op een wand uitkomt komt een handvol keien over de naad;
- waar een plafond tegen een wand aan loopt die verder naar beneden doorloopt, zit een hoek
  van 90 graden: daar hangt een hangblok in, want `hoek_plafond_wand.png` past niet in een
  raster en wordt niet gebruikt;
- waar een rotspunt in de open ruimte steekt komen keien of een hangblok overheen.

`wand_richel` zit met opzet niet in de verstrooiing: dat is een plank om op te springen, en
tegen een losse celrand geplakt hangt hij als een plaat in de lucht. Zet hem met de hand
neer, daar waar je hem als opstap wilt. `wand_rand.png` wordt sinds de terrasmassa niet meer
gebruikt: als tegel over een cel van 120 px leest dat stuk als een lichte rechthoek.

De losse stukken (hangblokken, richels, keien) hangen aan Amir (`grotDecorS`), niet aan de
steenschaal: daarop zou een hangblok zes keer zo hoog worden als hij.

Geen tint, geen overlay, geen `globalCompositeOperation` op deze sprites. Ze zijn allemaal
hetzelfde warm grijsbruine gesteente; elke waas eroverheen maakt van de ene helft grijs en
van de andere bruin.

Tegels worden een keer op maat gezet (`grotBandSet`) en daarna op hele pixels neergelegd.
Verklein je een naadloze tegel rechtstreeks met `drawImage`, dan klemt de resampler op de
rand en zie je de naad alsnog als een lijn door het steen lopen.

Alleen `wand_richel` draagt, met een hitbox die alleen de bovenkant van het brok beslaat.
Hangblokken en losse keien zijn puur decor.

### Het plafond als hoogtelijn

Het raster hierboven is terrein in cellen, en dat geeft rechte hoeken. Voor rots boven je
staat daarnaast de plafondlijn, en die is opgezet als de grond: `terrainH(x)` geeft per
wereld-x hoe hoog de bodem ligt, `plafondH(x)` geeft hoe hoog de onderkant van de rots hangt,
allebei in sprite-eenheden boven de grondlijn. Tussen twee punten loopt de lijn recht door,
dus een schuin stuk is niet meer dan twee punten op verschillende hoogte.

```
plafond: [ {x: -1000, y: 4000},    geen plafond: PLAFOND_WEG of hoger is open lucht
           {x: -2600, y: 360},     zakt schuin in beeld tot een gang
           {x: -5200, y: 280},     en knijpt verder dicht
           {x: -6600, y: 4000} ]   weer omhoog, uit beeld
```

De punten mogen in looprichting staan (x steeds negatiever); het spel zet ze zelf op volgorde.
Reken met Amir: hij is `CHAR_H` (251) hoog en springt 200 (zie "de sprong" hieronder). Boven de 460 merkt hij niets, op
400 loopt hij rechtop maar stoot hij bij elke sprong zijn hoofd, op 280 zit springen er niet
meer in, en onder de 251 kan hij er helemaal niet langs, want gebukt loopt hij niet.

Staat er iets onder de lijn om op te springen, tel dan door: een plafond knipt zijn sprong af,
dus de lijn moet minstens op de hoogte van dat ding plus 251 plus ongeveer 75 liggen. Op de kei
van Test 1 (114 hoog) is dat 440. Op 400 haalt hij het ook nog, maar alleen als hij precies op
tijd afzet, en dan sta je de halve tijd klem voor een kei van een halve meter. Dat is gemeten,
niet geschat: op 400 lukt de sprong vanaf 30 tot 180 px voor de kei, op 440 vanaf 30 tot 270.

Drie lagen, in deze volgorde:

1. **Vulling** (`plafondVulling`): alles boven de lijn, met de lijn als clippad. De tegel is
   `design/grot/rots_vulling.png`, uit het massieve deel van `plafond_strook` geknipt
   (`tools/rots_vulling.py`), en wordt op `grotSteen()` getekend: dezelfde schaal als de band,
   dus per definitie dezelfde korrel. Naadloos in beide richtingen, nooit uitgerekt, en hij
   loopt altijd door tot ruim voorbij de bovenrand van het scherm.
2. **Band** (`plafondBand`): dezelfde tandenrand als bij de grotten (`GROT.band`, de onderste
   160 bronrijen van `plafond_strook`), maar langs de lijn, en per stuk meegedraaid met de
   helling. Het patroon loopt door over de knikken heen (`plafondFase`), anders begint het bij
   elk stuk opnieuw en zie je de knik in het steen zitten. Die fase moet ook doorlopen buiten
   de lijn: het spel tekent anderhalve schermbreedte breder dan het beeld, dus aan het eind
   van een level ligt de rand van dat venster voorbij het eerste punt van de lijn. Daar is de
   lijn vlak (`plafondH` klemt), dus de lengte is gewoon de afstand, en `plafondFase` geeft
   hem negatief terug. Stopt hij daar op nul, dan staat de fase stil terwijl het stuk tussen
   de vensterrand en het eerste punt wel meegeteld wordt, en plakt de tandenrand aan het
   scherm in plaats van aan de wereld: hij schuift dan precies met je mee.
3. **Losse blokken** (`plafondDecorLijst`): om de `PLAFOND_STAP` wereld-px een plek, waar
   ongeveer een op de drie keer een hangblok of een richel hangt, met een seed uit de lijn zelf.
   Ze worden afgesneden op de lijn: wat erboven uitsteekt zit in het steen. Hoe krapper de
   ruimte onder de lijn, hoe kleiner ze uitvallen (`PLAFOND_HANG`), want je moet er niet
   doorheen hoeven lopen.

De band loopt aan zijn bovenkant uit in de vulling (`PLAFOND_VERVAAG`), en de vulling loopt
daarvoor even ver door onder de lijn. Zonder die overgang ligt er een lichte plaat met een
kaarsrechte bovenkant op de rots, en dat is precies wat er bij de grotset ook al misging.

Botsen: de ruimte boven de lijn is massief. `plafondKop` is de laagste lijn over zijn breedte
min zijn eigen lengte, en gaat samen met `grotKop` als plafond in `updateJump`. `plafondBlok`
duwt hem terug waar de lijn onder zijn kruin duikt, zoals `grotBlok` dat bij een celwand doet.
Hangblokken zijn decor; alleen `wand_richel` draagt, met dezelfde hitbox als in een grot
(`plafondPlats`).

`hoek_plafond_wand.png` en `wand_rand.png` worden nergens meer getekend. Ze blijven wel in
`design/grot/` staan, voor later, als er een ravijn komt waar je in afdaalt.

### De muur die je met je speer openkrijgt

Een rotswand die de weg verspert, met op het steen een houten schijf met een rune. Raakt de
punt van een geworpen speer die schijf, dan blijft die speer er voorgoed in zitten en schuift
het rotsblok in een halve seconde omhoog de berg in. Mis je, dan blijft de speer in de rots
steken en valt hij er na `JAV.muurT` vanzelf uit: dat is de gewone wandspeer, daar is niets
voor aangepast.

Een level zet hem neer met `muur: {x, speer}`. `x` is de rechterrand van de rots, de kant waar
Amir aankomt; `speer` is waar zijn speer steeds terugkomt, en dat telt vanaf de lijn waar de
wand hem tegenhoudt, niet vanaf een vaste plek in de wereld. Dat moet ook wel: de rots hangt aan
Amirs maat, dus op een ander scherm verschuift die lijn mee en kwam een vaste plek achter de
muur te liggen, waar je er niet meer bij kon. Verder staat er geen enkele positie in het level: waar de opening en
de schijf komen rekent `muurSet` uit de plaat zelf uit. Alles wat je kunt afstellen zijn maten
en verhoudingen, en die staan bij elkaar in `MUUR`.

**De rots wordt in zijn geheel getekend.** Niet gesneden, niet gespiegeld, niet uitgerekt: de
hele plaat met zijn volledige silhouet, geschaald tot hij past. Zijn maat hangt aan Amir
(`hoogAmir`, 1,6 keer zijn lengte) en niet aan het scherm, en dat is niet vrijblijvend: de
opening en de schijf worden uit Amir gerekend, dus hangt de rots aan het scherm, dan verspringt
die verhouding met elk venster. Op een breed en laag scherm werd de rots groot terwijl Amir
klein bleef, schoof de opening diep de rots in, en was de rune vanaf geen enkele plek meer te
raken. Aan Amir gekoppeld ligt alles op elk scherm hetzelfde. `hoog` en `breed` zijn alleen nog
een vangnet voor het geval hij niet past.

Rotsformaties krijgen voortaan deze maat: 3,5 keer Amir hoog, even groot als deze rots in
Test 3. Zo staat ook de scheve spits met de rune bij het openscheurende ravijn in Test 6
(`RAVIJN_ROTS`).

Omklappen kan met `spiegel`, maar staat uit, en dat is gemeten. Gespiegeld wijst de hoge flank
met de overhang naar Amir en komt de opening onder dat hoge steen te liggen. De schijf hangt
altijd net onder de bovenrand van de rots, dus daar hangt hij hoog, en een hoge schijf betekent
een lange worp: op 1280 bij 720 moet je dan van 480 pixels gooien en staat er nog maar een
strook rots in beeld, en op 1440 bij 620 is er helemaal geen plek meer waar je hem kunt raken.

**De plek van de opening komt uit de alfawaarden.** Per kolom wordt geteld hoe hoog het steen
vanaf de grond draagt (`massief`). Kleine gaten onderweg tellen daarbij niet als het einde: aan
de voet staan de keien los van elkaar met lucht ertussen, en een telling die daar stopt geeft
nul op kolommen waar in het beeld gewoon een muur van steen staat. Dat was precies waarom de
opening met de kale plaat ineens driehonderd pixels dieper ging liggen. Vanaf dat profiel en daarna wordt van de kant waar Amir
vandaan komt de eerste plek gezocht waar de opening past, met daar de hoogste deur die er nog
in kan. Zo dicht mogelijk bij zijn kant dus, en dat is niet alleen netjes: hoe dieper de
opening ligt, hoe verder je moet gaan staan om de rune te raken, en hoe minder er dan van de
rots in beeld past. Twee eisen tegelijk:

- over de volle breedte van de opening moet er genoeg steen staan (de deur plus de schijf
  erboven plus een randje);
- waar de schijf komt te hangen moet de bovenrand van de rots juist laag genoeg blijven, onder
  de top van de werpboog. Het spel rekent die top uit de worpconstanten uit. Ligt de rand
  hoger, dan kan de speer er per definitie nooit overheen en is de rune onraakbaar.

Past de opening nergens, dan krimpt hij tot hij wel past, tot Amirs eigen lengte. Dat is met
opzet: een deur die vasthoudt aan zijn maat belandt aan de rand van de rots, half in de lucht,
en dat is precies wat er niet mag.

**De schijf hangt aan de bovenrand, niet op een vaste hoogte.** In zijaanzicht is de rots een
massief silhouet: een punt onder de bovenrand zit in het steen, en daar komt geen speer ooit,
hoe je ook gooit. De schijf hangt dus net onder die rand (`onder`, 1 betekent dat haar
bovenkant hem raakt), zodat het hout helemaal op de rots ligt en de punt er toch bij kan door
er overheen te scheren. Daarom is het raakvlak (`raak`) ruimer dan het hout: de ruimte waar de
speer kan komen ligt boven de schijf. Dat raakvlak staat los van de straal, en met opzet: `r`
is hoe groot het hout eruitziet, `raak` is hoe nauw het luistert, allebei als deel van Amirs
lengte. Zo maakt een kleinere schijf het spel niet meteen ook moeilijker. De punt blijft steken waar hij binnenkwam, geklemd op de
rand van het hout, dus hij springt niet naar het midden.

**Gat en blok komen uit dezelfde pixels.** Uit de plaat op maat komen drie canvassen: de muur
met de vorm van de opening eruit gegumd (`destination-out`), het schuifblok dat precies dat
uitgegumde stuk is met een marge eromheen, en een masker dat die vorm doorsnijdt met de rots
zelf. Het masker is een pixel ruimer dan het gat, anders blijft er door de anti-aliasing een
haarlijntje op de rand staan.

Die snede met de rots gaat met de hand en niet met `destination-in`. Die rekent alfa maal alfa,
en waar de omtrek van de rots zelf door het gat loopt (langs de voet, bij de steentjes) werd het
blok daardoor doorzichtiger dan het steen eromheen. En zolang het blok stilstaat wordt de
ongeschonden plaat getekend en verder niets: de drie canvassen weer samenstellen levert op de
zachte randen 8-bits afrondingen op, en dat is precies het haarlijntje dat er niet mag zijn.

**De speer botst op de alfawaarde**, met de punt, en dat gaat vanzelf goed omdat `jav.x` en
`jav.h` in dit spel de punt zelf zijn. Lukt het uitlezen niet, dan telt de hele plaat als rots.

**Amir loopt door de rots heen.** De hele rots is decor, ook de deur: uitspelen gaat met E als
de deur open staat en hij ervoor staat (`muurUitgang`). Er is dus niets dat hem tegenhoudt, en
een level dat bij de rots eindigt zonder klif erachter laat hem voorbij de rots eindeloos de lege
savanne in lopen. Zet er een klif een stuk achter.

**Controleer na elke wijziging of de rune nog te raken is.** Dat is geen gevoelskwestie: simuleer
de boog vanaf elke plek waar Amir kan staan en kijk of er een aaneengesloten strook overblijft.
Op een scherm van 1280 bij 720 en Formaat 25 is die strook 141 pixels breed, van 94 tot 235
pixels voor de muurlijn, en vanaf de hele strook staat de rots in zijn geheel in beeld.

Het gras aan de voet staat niet in de plaat maar wordt er los voor gezet (`MUUR.gras`), met
dezelfde tekencode als al het andere gras, dus het buigt mee met de windvlagen. Ingebakken gras
schaalt mee met de rots, en dan staan er sprieten van een meter hoog zodra hij groter wordt. Dichterbij gaat de speer onder de rune door tegen het steen, verder weg zakt hij er al
voor. Er is nog een tweede strook op ruim tweeduizend pixels, maar daar staat de rots buiten
beeld, dus die telt niet mee.

**De grot met de kei** is een tweede soort muur: `muur: {x, speer, soort: 'grot'}` (nu alleen Test
3). Instellingen in `MUUR_GROT`, de canvassen in `muurGrotSet`, tekenen in `drawMuurGrot`. De rots is
de geschilderde boog `design/rotswand_boog.jpg`, met het wit eruit via `witKnip` (dezelfde functie
als de rots bij het ravijn); het donker in de grot is een vulling vanuit de voet van de boog, dus het
volgt de geschilderde rand. Voor de ingang staat `PROPS.boulder`, zo groot dat hij de grot dekt. Bij
een treffer trilt hij, zakt hij de grond in en blijft zijn bovenkant als drempel liggen (`kei.blijf`),
met stof (`puffPic()`) en gruis dat van de boog valt, allemaal op `muurKlok`. Zet hier geen gegumde
opening in: een getekend gat in een geschilderde rots blijft computertekenwerk, en daar is dit de
vervanger van. `muurSet` geeft voor de grot dezelfde velden terug (`l`, `r`, `t`, `b`, `symX`, `symY`,
`alfa`), dus de E voor de deur, de speer in de schijf en `muur.speer` werken gewoon door.

De schijf staat op `sym.hoog` 2,0 Amir, op de linkerpoot (`sym.u`). Dat is gemeten, niet gekozen: met
de huidige boogworp raak je hem op een scherm van 1280 bij 720 van 465 tot 770 pixels, waarvan 465 tot
620 met de schijf in beeld (de camera staat op Amir, dus je ziet 640 naar links). Op 2,28, de hoogte van
de kale rots, begint de strook pas op 590 en valt er bijna niets meer in beeld. Op 1440 bij 620 is het
400 tot 660, op 1920 bij 1080 690 tot 1155, op een telefoon van 844 bij 390 250 tot 420. Hoe lager de
schijf, hoe dichterbij: de boog stijgt nog als hij bij de schijf is.

Een speer blijft bij de grot pas in het steen steken als hij er van buitenaf in vliegt (`jav.buiten` in
`muurSteen`). Amir staat hier vaak voor de rots, onder de boog of voor de kei, en dan vertrekt de speer
al in het steen: met de gewone regel bleef hij er na een paar pixels in steken en was de schijf van
dichtbij niet te halen. Zolang de kei staat vangt die ook een speer (`keiAlfa`).

Let op: de getallen hierboven voor de kale rots (94 tot 235 pixels) kloppen niet meer met de huidige
worp. Met dezelfde meting raak je de schijf in de oude Diepte 3 (dezelfde kale rots als in Rune 10) van 590 tot 1005 pixels.

Het geluid zit in `SFX_DEUR` (`sounds/deuropen.mp3`) en speelt af op het moment van de treffer.
De opname duurt 42 seconden en staat van begin tot eind even hard, terwijl het blok maar een
halve seconde schuift, dus er wordt alleen de kop van gebruikt: vol tot `duur`, dan wegzakken in
`uit`, samen zo'n drie seconden. Dezelfde aanpak als bij het windgeluid. `duur: 0` speelt hem
wel helemaal uit.

Een ravijn dat openscheurt gebruikt dezelfde opname als aardbeving (`playBeving`, `SFX_BEVING`), maar
vanaf het eerste trillen (`onTremorStart`) in plaats van op de klap: hij zwelt aan van `begin` tot vol
op de klap, houdt aan tot het gat open is en de stenen liggen, en zakt dan weg in `uit`. De tijden
komen van het effect (`fx.tCrack`, `fx.tOpen`), dus een breder ravijn rommelt langer. Voor een gewoon
ravijn is dat van 0 tot 5,3 seconden; eerst was het van 1,6 tot 4,1.

**Geluid op een telefoon.** Een telefoon laat geluid alleen starten vlak na een tik. De versterkers
(`deurVersterker`, `skeletVersterker`) werden pas aangemaakt als het spel ze nodig had, midden in het
spel en zonder tik, en bleven dan stil: op een telefoon hoorde je de aardbeving, de rotswand en het
skelet niet. `geluidOntgrendel` maakt ze bij elke tik of toets aan en zet ze op gang, en geeft de
audio-elementen een keer een stil begin. Maak je een nieuw geluid met een eigen versterker of een
eigen audio-element dat het spel zelf start, zet het daar dan bij. Headless Chromium past die regel
niet toe, dus in de speelrobot is dit niet na te spelen: controleer het op een echte telefoon.

### Runes op elke rots, op elke hoogte

Een rune hoeft niet op de scheve spits op 190 te zitten: `rots`, `groot` en `hoog` zetten hem op een
andere plaat (`RUNE_ROTSEN`, alle met een witte achtergrond door `witKnip`, per plaat geladen in
`runeBeeld`), op een andere maat en op een andere hoogte. De schijf komt op de flank aan Amirs kant
(`ravijnRune` zoekt op die hoogte de rand van het steen in de alfa), en nooit hoger dan zijn eigen
rots min twee stralen (`runeHoog`). Een rune zonder die velden is precies wat hij was.

Hoe hoog is goed? Amir haalt springend 1,83; alles daarboven moet je raken met een worp. Hoe hoger,
hoe verder je moet staan, en de camera staat op Amir: op 1280 bij 720 zie je 640 px voor je uit, en
vanaf ongeveer 2,1 Amir begint de strook waar je hem raakt pas buiten beeld. Dat rekent `runeStroken`
uit, met dezelfde stappen als de speer in het spel en met de worpen van het level (de twee trappen,
of met `worp: 'schaal'` elke hoek tot 30 graden). Het venster in de bouwer laat de strook zien en
waarschuwt als hij leeg is of buiten beeld begint.

Een speer die in een rots vertrekt (Amir loopt door de rotsen heen) blijft pas in het steen steken
als hij er eerst uit is geweest (`jav.rotsUit`), net als bij de grot met de kei. Een speer die na `JAV.muurT` uit
het steen schiet, valt door de rots heen tot op de grond (alleen een vliegende speer blijft in een
runerots steken): anders raakt hij de flank eronder, die naar beneden breder wordt, en zit hij een
stukje lager weer vast. Een vallende speer zet ook geen rune aan.

Met `doel: true` is een rune een doel: raken zet hem aan (`runeGeraakt`), met een felle gloed die in
`RAVIJN_RUNE.flits` wegzakt (`runeFlits`), en hij blijft aan tot je opnieuw begint.

**Een speer in een runeschijf blijft vastzitten, punt.** Dat geldt voor elke houten schijf: de rune op
een rots, de rotswand en de grot. Bij een treffer wordt de speer meteen decor van de rune
(`runeSperen`, in `ravijnRuneTreffer`), net als `muurSpeer` bij de rotswand: E doet er niets, en Amir
heeft geen speer meer. Het spel geeft er niet vanzelf een nieuwe voor; dat regelt het level, met een
skelet of met de speerplek bij de rotswand (`muurVul`). Een level zonder nieuwe speer na een rune is
dus een keuze, en kan juist de uitdaging zijn: zet er een neer als de speler er daarna nog een nodig
heeft. Test 9 en Test 12 hebben er een skelet voor. Test 12 is het proefstuk: vijf rotsen, en na elke rots een
skelet voor een nieuwe speer.

**Het licht op een runerots** komt van dezelfde zon als de rest (`RUNE_LICHT`). Net als bij de
lichtkaart gaat er uit elk punt van de rots een straal naar de zon (`LK.zonHoek`, aan de kant van
`zonRechts`), en telt hoe ver die door het steen moet (`runeLichtMaak`). Kort: een warme rand, met
`soft-light` zodat licht steen niet wit wordt. Diep (tot `diep`, ongeveer de breedte van een zuil):
schaduw. In een kier zakt die weg maar langzaam weg (`lucht`), anders licht een losse kei aan de
schaduwkant op. Op de grond valt een slagschaduw naar de andere kant (`runeGrondSchaduw`), in de
sneeuw blauwig. De sterkte volgt de gloed van het uitzicht, met `nacht` als ondergrens. De maskers
worden een keer per plaat, kant en maat uitgerekend (zo'n 20 ms), een rots per beeld vanaf het begin
van het level, dus voor je er bent. De grijze schaduwvloer onder de keien in de platen gaat er bij het
laden uit (`RAVIJN_ROTS.voet` in `witKnip`); zonder dat lag er een grijze strook op de grond.

De maten van een rots hangen aan Amir en dus aan het scherm, en een level niet: op 1920 bij 1080
is een rots van 5 Amir ruim 2000 px breed. Laat tussen de rotsen genoeg ruimte voor het grootste
scherm, anders sta je om te gooien in de vorige rots.

### Het skelet met de speer

De plaatjes staan in `design/botten/skelet/` en zijn allemaal op één schaal gemaakt: 0,19 bij een Amir van 237 px
(`SKELET.schaal`), dus het zittende skelet is 0,61 Amir. Rekenen gaat in skeletcoordinaten, met (0, 0) op de
linkerbovenhoek van het skelet zelf en de grond op 754.

- **Zitten** zijn de negen losse botten uit `delen/` op hun plek, met daarover de speer,
  `skelet_voorste_botten` en het doekframe. De voorste botten zijn niet optioneel: zonder die laag ligt de speer op
  het skelet in plaats van erdoorheen. Tot de botten binnen zijn staat `skelet_met_speer.png` er.
- **Instorten** speelt het spel zelf met die botten (`SKELET.delen`, `skBotten`), op de valcurve van het pakket. De
  ingebakken sheet uit het pakket wordt niet gebruikt: daarin bleven de onderbenen met de knie in de lucht staan. Nu
  kantelt het bovenbeen om de heup en ploft het onderbeen plat (`a` en `laat` bij de benen). Een kind draait mee met
  zijn ouder, zoals in `onderdelen.json`.
- **De schedel** is na het instorten, of als hij eraf getikt is, een los ding (`s.kop`): hij valt, landt met stof,
  rolt met de hoek aan de afgelegde weg (weg gedeeld door de straal van 58) en ligt dan stil. Daarna is hij decor:
  tegenaan lopen of erop slaan doet niets.
- Wat Amir kan: E **vasthouden** bij de schacht trekt de speer eruit (`skeletTrek`, `skeletTrekLos` bij het
  loslaten van de toets of de E-knop). Het skelet schudt steeds harder, de speer schuift eruit en rond de E loopt een
  ring vol; na `SKELET.trek.duur` (2 seconden) laat hij los en ploft het in elkaar. Eerder loslaten of weglopen en hij
  blijft erin. Alleen met lege handen: een speer die je met E hebt weggestoken telt als in je hand (dan wiebelt hij en
  speelt `sounds/dontneedthis.mp3`); een weggegooide speer niet, die blijft liggen waar hij ligt. Een steek of een worp tegen de schedel
  tikt die eraf (`skeletRaak`, aangeroepen vanuit de tekenlus waar ook de slangen geraakt worden). Een lage zwaai laat het
  meteen vallen, en de speer valt eruit en blijft liggen.
- De speer uit het skelet heeft een **blauw vaantje**. Het rode lint zit in Amirs sprites gebakken en wordt bij het
  tekenen omgekleurd (`vaanBlauw`, `vaanMaak`). Op tint alleen gaat dat mis: in de idle is het lint oranje, en in de
  werpframes is zijn huid net zo verzadigd als het lint. Wat scheidt is helderheid, samenhang en nabijheid; de stappen
  en getallen staan bij `VAAN`. Verander je iets, kijk dan alle speerframes na, ook de twintig van de worp. De grote
  werpframes kosten tot een tiende seconde, dus die worden vooraf gedaan zodra je de blauwe speer hebt (`vaanVoorwerk`).
- **Losse speren** (`losseSperen`): er kan nu meer dan een speer zijn. Wat niet in je hand is en niet je eigen speer in
  de wereld, ligt daar. Pak je een andere speer terwijl de jouwe ergens ligt, dan wordt de jouwe een losse speer
  (`eigenSpeerNeer`), zodat hij niet verdwijnt.
- Het geluid `sounds/skeletvalt.mp3` start als het valt, niet bij het trekken, en gaat via een versterker op 3,6
  (vier keer 0,9), want een audio-element komt niet boven 1. Een tweede instorting start het opnieuw.
- Stof: eigen wolkjes per skelet (`SKELET.stof`), want `stofwolk.png` is ijl en `puffWorld` is voor een voetstap.
- De schaduw vermenigvuldigt de grond met (0,74, 0,80, 0,91) en ligt naar links, want de zon staat rechtsboven.

De plaatjes laden pas als er een skelet in het level staat (`skeletLaad`).

### Een gang onder de grond

`holtes: [{r, l, diep}]` legt een gang onder de grondlijn, met de vloer `diep` sprite-eenheden
lager. Een ravijn uit `gaps` dat erboven ligt is de ingang: daarin val je niet dood maar kom je
op de vloer terecht. Met `valschade: true` kost een val van 600 twee levens (vanaf twee Amir,
502). Het dak is de onderkant van het grondpakket, `HOLTE_DAK` (190) onder de grondlijn.
Laat de gang aan de kant van het ravijn wat verder doorlopen dan het gat, anders staat de wand
onder de rand. Alles in de gang staat op de bodem, want `terrainH` geeft daar `-diep`.

Het licht onder de grond komt uit een plek: de lichtkaart (zie hieronder). De tegels van de
gang zijn zelf maar een beetje donker gezet (`HOLTE_LICHT`), de looprand van de vloer lichter
dan de vulling eronder. `Test 10` is het proefstuk voor het licht, `Test 4` voor de gang.

### De lichtkaart: een lichtbron voor alles onder de grond

Er is een lichtbron onder de grond: de hemel, met de zon als vaste richting. Voor elke cel van
`LK.cel` bij `LK.cel` rekent `lkKolom` uit hoeveel hemel hij ziet (stralen omhoog die grond en
rots tegenhouden, `lkZicht`) en of de zon hem raakt (`lkZon`, een smalle kegel, dus een zachte
schaduwrand). De zon staat aan de kant waar hij in de lucht van het level staat (`zonRechts`),
`LK.zonHoek` graden van recht boven. Daaruit volgt vanzelf wat je wilt zien: een gat is licht,
de rand werpt een schuine schaduw van de zon af, en hoe verder de gang van een gat af loopt,
hoe donkerder, zonder rechte streep. Vaste grond is een doorsnede: die krijgt het licht van de
oppervlakte erboven en wordt dieper eronder donkerder (`LK.diepte`, `LK.bodem`). Lucht die zelf
weinig hemel ziet, krijgt kaatslicht van wat eromheen ligt (`LK.kaatsR` cellen in het rond), en
dat is warm waar de zon in de buurt iets raakt.

Dit vervangt alle losse lagen die er eerst waren: de getekende lichtbundel door een gat, de
schaduw tegen de eindwanden, het verloop in het grondpakket, `holteFilter` en `holteHelder`
voor decor en treden, en een vervaagde donkerlaag over de rots. Die gaven elk hun eigen licht
en dus rechte randen. Teken er dus geen nieuwe bij: een nieuw soort terrein hoeft alleen in
`lkVastPunt` te zeggen wat vast is.

Twee regels die ertoe doen:

- **De zonnegloed van de lichtlaag schijnt niet door de rots.** `drawLichtlaag` telt de gloed rond
  de zon op in schermruimte; onder de grond (`holteDiepT`) gaat die uit. Deed hij dat niet, dan lag
  er in de gang zo'n 40 punten helderheid bovenop, en daar was het steen vlak en oranje van.
- **Vaste grond wordt pas donker als de camera zakt.** Het plaatje met de grond (`lk.grond`)
  krijgt `holteDiepT` als dekking: van bovenaf ziet de savanne eruit zoals altijd. Wat lucht is,
  een gat of een gang, is altijd zo licht als het is.
- **Een ravijn zonder gang eronder laat de kaart met rust.** Zo'n gat tekent zijn eigen diepte en
  schaduw (zie hieronder); in `lkRuw` krijgt het geen licht of donker uit de kaart. Zonder die
  regel kreeg een dodelijk ravijn vlak bij een gang ineens zon en kaatslicht.
- **De zon valt pas onder het dak binnen**, en loopt daar over `LK.zonInloop` eenheden in. De wand
  van een gat erboven is de overkant, en die hoort niet lichter te zijn dan de grond vooraan.
- **Een open ravijn telt mee.** `lkSleutel` kijkt ook naar `ravijnGaten()`: scheurt er in een level
  met een gang een ravijn open, dan rekent de kaart opnieuw.

**De zon volgt het uitzicht** (`lkZonKleur`), net als de zon op de wand van een ravijn. De sterkte
schaalt met `gloedSterkte` (0,30 overdag), met `LK.zonNacht` als ondergrens, en in de winter is de
kleur koel wit (`LK.zonWinter`) in plaats van warm (`LK.zonKleur`). Anders viel er in de sneeuw oranje
licht op grijze steen, en was de zon 's nachts beneden even fel als overdag. Kleur en sterkte zitten in
`lkSleutel`.

**Rots boven je, ook buiten.** Een plafondlijn en de volle cellen van een rotsraster zijn voor de
kaart rots (`lkRotsPunt`), ook boven de grond, en een level met alleen een plafond of grotten krijgt
ook een kaart. Die reikt dan tot `LK.buitenTop` omhoog en rekent buiten alleen binnen `LK.buitenBuur`
van die rots (`lk.buur`); verder weg blijft het gewoon dag. Een punt buiten telt hoeveel hemel het
onder de rots nog ziet, en of de zon het raakt (`lkZicht` en `lkZon` met `rots`: alleen de rots houdt
dan de straal tegen, niet de grond en de terrassen). Het lichtste van die twee telt. De zon komt schuin
van zijn kant, dus onder een overhang ligt een schuine schaduwrand, en aan de open kant valt hij naar
binnen. Buiten weegt het donker minder zwaar (`LK.buiten`), want de lucht eromheen is open, en er komt
geen zonnevlek bij: het is al dag. Een terras of een kei onder de rots is voor de kaart lucht, zodat
de schaduw er ook overheen ligt. De rots zelf wordt boven de grond niet donkerder gemaakt.

Wat het kost, gemeten in Test 1: de hele kaart 0,3 seconde, in stukjes van `LK.budget`; het eerste
beeld van een level onder de rots eenmalig zo'n 50 ms.

### Een gewoon ravijn is een ravijn dat al open staat

Een ravijn uit `gaps` zonder gang eronder wordt getekend met dezelfde module als het ravijn dat
openscheurt: `ravijnVastVoor(g)` maakt er een `RavijnEffect` van dat meteen open staat
(`openInstantly`), en `ravijnenTeken()` geeft die samen met de openscheurende ravijnen aan de
ravijnlus in `scene()`. Zo heeft elk ravijn dezelfde wand, dezelfde rand van de overkant die
lager ligt dan de grond vooraan, de achtergrond erboven, het kleine gras en in de winter de
sneeuwrand. Het effect wordt per ravijn bewaard (`ravijnVast`) en pas opnieuw gemaakt als de
schaal, de wandplaat of het level verandert. Botsen gaat zoals altijd over `gaps`, daar is niets
aan veranderd.

Een gat boven een gang is hetzelfde ravijn, met dezelfde lage rand aan de overkant, maar de wand
houdt op bij het dak en daaronder zie je de gang. Dat tekent niet `scene()` maar de gatenlus, met
`ravijnGangTeken`: het effect (`ravijnTekenEen`, hetzelfde als in `scene()`) afgeknipt twee pixels onder
het dak, en daarover binnen de breuk `holteSchacht`, de overgang van aarde naar het steen van de gang.
De zon op de wand staat daar uit, want het licht komt uit de lichtkaart. Eerst had zo'n gat een eigen
tekening met de overkant op de kruin, en lag de rand in Jager 3, Test 4, Test 10 en Test 11 dus even
hoog als de grond vooraan. Dat geldt ook voor een ravijn dat boven een gang openscheurt (een rune of een
zegel): zolang het scheurt tekent het effect zichzelf in `scene()`, maar zodra het open staat is het een
gat in het dak (`ravijnBovenGang`) en telt het mee in `gatenTeken()` (met zijn effect in `g.fx`), de lijst
waar de gatenlus, `drawHolte` en de grond op tekenen. Botsen gaat nog steeds via `gatenMetRavijn` en `inGap`. Zonder dat bleef het
dak onder het gat dicht en zag je van boven een ondiepe kuil.

Een vijand die in een ravijn staat dat al openscheurde voor hij verscheen (zijn spawn ligt in
`ravijnGat`), komt niet meer: hij is erin gevallen. Anders stond hij boven het gat in de lucht. Wie
er al stond valt erin (`ravijnValt`). Zo werkte de valkuil in de oude Vorst 2 en 5: fosforslangen en
zwaardvechters blijven stil staan tot ze je zien, dus een rune die van verder weg de grond onder ze
openscheurt, neemt ze mee. Hyena's vallen hier buiten, want die komen van de rand van het beeld.

In de winter valt er geen sneeuw in een gang (`drawSnowfall` dooft onder de grondlijn met
`holteDiepT`), en treden in een gang (een terras met een negatieve `h`) krijgen de kale steen, niet
de besneeuwde.

In de bouwer is het precies hetzelfde ravijn, dus ook een level dat je daar maakt krijgt alleen de
nieuwe stijl. Twee dingen zijn er anders omdat je daar van verder weg kijkt (`viewZoom`): de ravijnen
worden rond het midden van de grondlijn geschaald, net als de grond (`ravijnZoom`, ook bij het vangen
van de achtergrond), en onder de wand komt de donkere bodem (`ravijnBodemVul`), want uitgezoomd reikt
het beeld dieper dan de wand. Versleep je een ravijn, dan wordt het effect opnieuw gemaakt; dat kost
minder dan een tiende milliseconde.

### De zon op de wand van een ravijn

De wand in een ravijn is de overkant: verder weg dan de grond vooraan, dus nooit lichter. De rand
aan de kant van de zon werpt er een schuine schaduw op, onder dezelfde hoek als waaronder de zon
in een gang binnenvalt (`LK.zonHoek`, `zonRechts`). Boven die lijn vangt de wand gedempt licht,
eronder ligt hij in de schaduw. Zo komt het licht in elk gat uit dezelfde richting als de zon in
de lucht. `ravijnZonLicht(g, x0, x1, top, onder, knik, open, atop)` tekent dat; de waarden staan
in `RAVIJN_ZON`.

| waar | hoe |
| --- | --- |
| gewoon ravijn en openscheurend ravijn | via het haakje `opLicht` van de module (`ravijn/ravijn-effect.js`), op het eigen canvas van de wand met `source-atop`: alleen op de wandpixels, nooit op de achtergrond erboven. `knik` is de verticale rek (`ravijnRek`), zodat de lijn in beeld de goede hoek heeft, en `open` is `fx.p`: de schaduw groeit mee met het openscheuren |
| gat boven een gang | niet: daar doet de lichtkaart het |

's Nachts is het verschil kleiner: de sterkte schaalt met `gloedSterkte` van het uitzicht (0,30
overdag), met `RAVIJN_ZON.nacht` als ondergrens. In de winter is de schaduw blauwig
(`RAVIJN_ZON.winter`): sneeuw en steen in de schaduw worden koel, niet grauw. De sneeuwrand van het
openscheurende ravijn komt na de wand en blijft dus wit.

De kaart hangt alleen af van de vorm van het level, dus elke cel wordt een keer uitgerekend. Wat
vast is gaat in een keer (`lkKaart`), de stralen per kolom zodra hij nodig is, en `lkVooruit`
rekent elk beeld `LK.budget` ms vooruit, vanaf Amir naar buiten: zo is de kaart af voor je
beneden bent. Het kaatslicht gaat met lopende sommen (`lkSom`), en de plaatjes worden eerst in
het geheugen gezet en per beeld een keer overgezet (`lkPlaatjes`). Zonder die twee kostte het
kaatslicht 1,2 seconde op Test 10, nu 70 ms; de hele kaart is een halve seconde, in stukjes.
Verandert de vorm (in de sandbox) of een regelaar, dan begint hij opnieuw (`lkSleutel`).

**De kaart wordt in twee delen getekend**, zodat de personages minder donker zijn dan hun
omgeving zonder dat hun tekencode iets van licht weet. Het eerste deel (`'wereld'`) komt vlak voor
Amir, na alles wat achter hem staat; het tweede (`'allen'`) komt na alles (na `drawWind`) en valt
dus ook over Amir, de vijanden en wat er voor hen langs komt, en daarin zit ook de zon. Per cel
worden de twee zo uitgerekend dat de wereld samen precies het hele donker `a` krijgt:
`a2 = LK.personage * a` voor iedereen, en `a1 = 1 - (1 - a) / (1 - a2)` voor de wereld eronder,
want `(1 - a1)(1 - a2) = 1 - a`. De personages krijgen alleen `a2`. Teken dus niets tussen Amir en
het tweede deel wat bij de wereld hoort, want dat mist het eerste deel. De ooggewenning ligt als
dekking over beide delen; dat is niet precies hetzelfde als het donker zelf verminderen, en in Test
10 scheelt het op de wand ongeveer een punt helderheid.

De regelaars staan in de sandbox onder **Licht onder de grond** (donker, ondergrens, gewenning,
personages, zon, kaatslicht, warm); elke klik laat ze allemaal zien, zodat je ze in `LK` kunt
overnemen.

**Ooggewenning** (`lkGewenning`): hoeveel licht er rond Amir is, staat al in de kaart (`lk.licht`,
het licht per cel zoals het getekend wordt), dus er wordt niets uit het beeld teruggelezen.
`lkRondAmir` neemt het gemiddelde van de luchtcellen om hem heen. Hoe donkerder daar, hoe meer van
het donker van de kaart wegvalt, tot `LK.gewenning`, en zijn ogen doen er `LK.gewenTijd` seconden
over (op de speltijd, dus ook de speelrobot ziet het). Diep in een gang wordt het zo na een paar
tellen lichter, en loop je naar een gat of een uitgang, dan komt het donker terug. Gemeten in Test 10:
zonder gewenning zakt het lange donkere stuk tot helderheid 30, met gewenning blijft het rond 44;
bij de uitgang komen beide weer bij elkaar uit. De zonnegloed in de kaart valt er niet onder.

**De ondergrens** (`LK.minLicht`) houdt het spel speelbaar: donkerder dan dat deel van het licht
wordt de kaart nergens, hoe weinig hemel een plek ook ziet. Zo blijven de vloer, de randen en de
treden te lezen. Het is een grens op het donker van de kaart, niet op het beeld: de tegels van de
gang zijn zelf al een beetje donker, en de lichtlaag komt er nog overheen.

**De schaduw van Amir** ligt op dezelfde vloer als waar zijn voeten op komen (`grondVloer`, net
als in `updateJump`), dus beneden in een gang op de bodem. Het gat eruit knippen gebeurt alleen
bovengronds: beneden is een gat erboven geen rand.

**Boven het dak loopt de aarde over in steen, en dat is materiaal, geen kleur.** Het grondpakket
boven een gang en de wand van het gat erboven zijn aarde, de gang is steen. Onderin het pakket
wordt de wandtegel van de gang zichtbaar (`holteOvergang`, over `HOLTE_OVERGANG` eenheden), op
precies hetzelfde ankerpunt in de wereld als de gangwand. Onder een gat ligt daardoor op de
daklijn aan beide kanten hetzelfde steen en loopt het patroon gewoon door; naast een gat hangen
er de tanden van het dak onder. Niet proberen de naad weg te poetsen met een tint of door kleuren
gelijk te trekken: dat is geprobeerd, en het gaat mis zodra het uitzicht of de lichtlaag anders
is. Meten deed het wel, en dat is de manier om een wijziging hier na te kijken: helderheid per
rij over de naad, en geen sprong van meer dan een paar punten.

De opbouw, van boven naar onder:

| waar | wat |
| --- | --- |
| naast een gat | de vloer van de savanne, dan aarde die overloopt in steen, en dan de tanden |
| in een gat (`holteSchacht`) | de wand van het ravijn zonder de nevel en het zwart van een afgrond, onderaan de overgang naar steen |
| buiten de gang | dichte rots, onder het dak |

Hoe licht of donker elk daarvan is, komt uit de lichtkaart. Het steen zit alleen boven een gang
en loopt voorbij de uiteinden over `HOLTE_UITLOOP` uit. Het ravijn boven een gang houdt twee
pixels onder het dak op, op een hele beeldpixel (`heelPx`): waar twee zachte randen op dezelfde
lijn liggen schijnt er anders een haarlijn doorheen.

Alles wat binnen `r` en `l` van een gang staat, staat op de bodem: vijanden, decor,
kalebassen en de fakkels. Een level kan dus onder de grond eindigen; de wand van
de gang houdt je dan achter de fakkels tegen, een klif is niet nodig. Dat werkt omdat
`grotTerrein` zonder raster `-Infinity` geeft en geen 0: gaf hij 0, dan trok `terrainH` alles in
de gang weer naar de savanne, en dat is precies waarom de vijanden in een gang eerst boven
stonden en de fakkels daar niet te halen waren.

Twee hulpjes houden boven en beneden uit elkaar. `gatOp(x, base)` is `inGap` voor wie op
hoogte `base` staat: beneden in een gang is een gat erboven geen rand, dus een vijand loopt er
onderdoor. `vloerBij(x, h)` is de vloer voor wie op hoogte `h` staat: boven een gang de
savanne, erin de bodem. De vijanden rekenen hun vloer daarmee uit, en de sandbox zet een vijand
daarmee op jouw hoogte neer. Gebruik ze in plaats van `inGap` en `terrainH` als het om iets gaat
dat zowel boven als beneden kan staan.

**Terug naar boven** gaat via een tweede gat in het dak met treden erin. Een trede is een gewoon
terras met een negatieve `h`, dus de klimstukken van de terrassen, en `drawClimb` tekent ze in
een tweede ronde na de ravijnen (anders tekent de overkant van het gat over de bovenste heen).
Hoe licht ze zijn komt uit de lichtkaart. Reken zo:

- het dak ligt op 190, dus onder het dak mogen zijn voeten niet hoger dan -441 (`-HOLTE_DAK -
  CHAR_H`). Een trede hoger dan dat moet helemaal onder het gat staan;
- zijn rechterrand ligt minstens een halve Amir binnen het gat, anders staat hij bij het
  afzetten nog onder het dak en haalt hij hem niet;
- elke stap is minder dan de sprong (200); 150 is ruim;
- de bovenste ligt binnen een sprong van de grondlijn en loopt door tot de linkerrand van het
  gat: daar stapt hij de savanne op.

Zolang zijn voeten tussen het dak en de grondlijn zitten, houdt `holteBlok` hem binnen het gat,
want zijwaarts zit daar het grondpakket. Op de savanne boven een gang dragen de treden eronder
niet (`supportHeight`). Test 4 heeft zo'n trap: van 900 diep in zes stappen van 150 naar boven.

```
gaps:     [ {x: -1000, w: 620}, {x: -3400, w: 900} ],       ingang, en de uitgang van -3850 tot -2950
holtes:   [ {r: -540, l: -3850, diep: 900} ],
terraces: [ {r: -2850, l: -3850, h: -750}, {r: -3050, l: -3850, h: -600}, ... {r: -3650, l: -3850, h: -150} ]
```

`levelcheck.py` kijkt dit na onder `onder de grond`.

### Hoogteverschil onder de grond

Een gang die dieper wordt, of waar je klimt en weer daalt, is **één gang** met de diepste `diep`,
en de hogere stukken zijn treden: terrassen met een negatieve `h`, net als de trap naar buiten.
Je landt dan op een richel, loopt eraf naar de bodem, klimt met een kei of een richel weer op,
en daalt weer. Alles wat voor terrassen geldt, geldt hier ook; daarbovenop kapt het dak elke
sprong af op -441.

Wat niet werkt, en waarom. Elk hiervan is nagelopen met de speelrobot (zie hieronder) in een
proefgang, en `levelcheck.py` meldt ze:

- **Twee gangen tegen elkaar** (de ene dieper dan de andere). `holteBlok` houdt Amir in allebei
  tegelijk vast: op de naad duwt de ene wand hem terug en de andere ook, en daar staat hij voorgoed
  klem, ook als hij er net in is gevallen.
- **Een terras op de savanne boven een gang.** Zijn wand wordt tot onder in beeld getekend en
  houdt hem ook tegen, dus in de gang staat een lichte stenen pilaar waar hij niet langs komt.
- **Een kei in de gang die tot in het dak reikt.** Op een trede van -520 staat de bovenkant van
  een kei op -406, en daar mogen zijn voeten niet komen: hij komt er niet overheen en niet langs.
- **Decor dat hoger is dan de gang.** Alles staat op de bodem, ook een boom, en die steekt dan
  door het dak. Een doornbos of een dorpsplaat net zo.
- **Een ingang die maar half boven de gang ligt.** Wie aan de kant zonder gang erin stapt, valt
  recht naar beneden (in een val loop je niet meer) en is dood.
- **Een gang die de speer overdekt.** Aan het begin staat je speer op `SPEAR_AHEAD` (-260) in de
  grond; ligt daar een gang, dan staat hij beneden op de bodem en begin je zonder.
- **Een gang minder diep dan 441.** `readLevel` maakt er zonder iets te zeggen 441 van, en dan
  kloppen je treden niet meer.
- **Vallen met `valschade`.** De val door de ingang telt ook: een ingang boven een richel op -700
  kost al twee levens. Tel de vallen langs de hele route op tegen de drie levens en de kalebassen
  die onderweg liggen.

Wat het spel zelf regelt, zodat je er als ontwerper niet op hoeft te letten:

- **Water kijkt naar de hoogte.** `waterDepthAt(x, h)` geeft 0 voor wie beneden in een gang
  staat: een poel boven een gang maakt Amir daar niet nat, traag of zwak in de sprong.
- **Decor in een gang is donker.** Props, keien en doornbossen beneden in een gang krijgen
  hetzelfde licht als alles daar, want de lichtkaart ligt eroverheen. De personages krijgen er
  een deel van (`LK.personage`), zodat je ze in het donker altijd ziet.
- **Hyena's komen op de goede hoogte.** Hyena's in een gang worden pas losgelaten als Amir zelf
  beneden is, en komen dan uit de gang aanrennen (`hyBuitenBeeld`), niet van de savanne erboven.
- **Vijanden blijven in hun gang.** Voor wie beneden staat is de eindwand van de gang een rand
  (`dropAhead`): daar lopen ze niet doorheen naar boven.

### Een level donker maken

De lichtlaag ligt over het hele beeld, dus ook over de grond en over Amir. Een level dat
er anders uit moet zien zet in zijn `SCENES`-blok een veld `licht` met de waarden die
afwijken (zie `LICHT`), en dat is hoe de nachtuitzichten (`dark_rots`, `dark_hart` en de andere
`dark_`-blokken) donker worden: een blauwgrijze
schaduw- en lichtkleur, een zwakkere gloed en een iets diepere onderkant. `aan` en
`sterkte` blijven van de regelaars (`L`, en `,` en `.`), ook in zo'n level: die zijn er
om te kunnen kijken wat de laag doet, en dat moet in elk level werken.

Het veld `dim` in `SCENES` is iets anders: dat zet alleen de achtergrond dieper, tot aan
de grondlijn. Wil je dat de hele wereld donkerder wordt, dan is `licht` het juiste veld;
wil je alleen dat de verte wegzakt, dan `dim`. Meestal gebruik je ze samen.

### De voorgrond hoort bij elk level

Elk level heeft een voorgrond: de onscherpe laag vlak voor de camera die het beeld diepte geeft.
Dat is geen keuze per level maar standaard. Zet een level er zelf geen, dan krijgt het er een van
het spel (`vgStandaard`): ijl (`VG_STANDAARD.dicht`), over het hele level, met open plekken rond
alles waar je naar moet kunnen kijken: ravijnen en de plekken waar er later een openscheurt, zegels,
de rots met de rune (die reikt ver naar rechts, want de rots staat aan de kant waar Amir aankomt), de
poort (`muur`), de fakkels en het veld van de eindbaas. Zo verbergt hij nooit een rand, een schijf of
een vijand die je moet zien. De maten van die open plekken staan in `VG_STANDAARD`. De standaard hangt
aan het level zelf, dus ook een level uit de bouwer krijgt hem, en verschuif je daar een ravijn, dan
schuift de open plek mee.

Een eigen `voorgrond` in de definitie gaat voor de standaard (Test 11 heeft er een). Doe dat als een
level een plek heeft waar de voorgrond iets moet vertellen: dicht gras aan het begin, een schedel in
het gras bij een eindbaas. `voorgrond: false` zet hem uit; doe dat alleen met een reden.

De voorgrond heeft twee lagen (`VG_LAGEN`), van ver naar dichtbij, en daardoor zit er ook binnen de
voorgrond diepte:

| laag | schuift | grootte | onscherp | schaduw |
| --- | --- | --- | --- | --- |
| ver | 1,2 keer de wereld (1,4 verticaal) | 0,6 | een beetje (3) | 0,85 van de schaduw |
| dichtbij | 1,45 keer (1,8 verticaal) | 1 | veel (7) | de hele schaduw |

Beide lagen lezen dezelfde stroken; de verre laag heeft een eigen reeks, zodat de pollen niet op
elkaar staan, en staat wat dichter op elkaar omdat hij kleiner is. Losse stukken (`los`) staan alleen
in de dichtbije. In de winter staan er de besneeuwde versies (`winter` bij elke soort in `VG_SOORT`)
met een koelere, lichtere schaduw (`VOORGROND.schaduwWinter`), anders wordt de sneeuw bruin; 's nachts
staat hij dieper in de schaduw, naar de gloed van het uitzicht. De hele voorgrond kost zo'n 0,05 ms per
beeld: de plaatjes worden per soort, laag en tint een keer onscherp gemaakt en bewaard.

### Een level toevoegen (alleen na toestemming)

1. De definitie erbij, na de laatste van die reeks.
2. De naam in de array van die reeks (`JAGER_LEVELS` of `TEST_LEVELS`).
3. Een ondertitel in `SUBS`, op de naam van het level.
4. Een eigen uitzicht in `SCENES` als het level er anders uit moet zien.
   De voorgrond komt er vanzelf bij (zie hierboven); zet alleen een eigen `voorgrond` als het level
   daar iets mee wil.
5. `python3 tools/levelcheck.py` draaien, en elke FOUT oplossen voor je commit (zie
   hieronder).

### Een episode toevoegen

Die vijf stappen, plus: een knop in `menuChoose`, een eigen `menuXxx`-blok in de
HTML naar het voorbeeld van `menuTest`, en die aanmelden in `buildCards`,
`markCards` en `showMenu` (die kiezen nu tussen `cardsJager`/`menuJager` en `cardsTest`/`menuTest`,
en `toMenu` ook), en de reeks in `tools/bouwertest.js` en `tools/speelrobot.js`. Een nieuwe episode begint altijd met de tribekeuze: `runStart` in zijn speelknop, en `tribeLijst` geeft
hem alleen wat de speler verdiend heeft (alleen `TEST_LEVELS` krijgt alles). Wil de episode een
verhaal, zet dan de tekst in `VERHAAL` en `SLOT` en `verhaalAan` in zijn speelknop. De Jagers is het
voorbeeld van een episode met verhaal en Nightmare.

### Een vijand of prop toevoegen

Tekencode en gedrag erbij, opnemen in `PROPS`, `VILLAGE` of de dierenlijst, en
knoppen in de sandbox. Kies de soort (vast, los, plant of ver, zie "wat mag waar") en zet hem in
de vijf functies die daarbij horen. Pas daarna is de vraag aan de orde of er een level bij moet.

## De bouwer

Level maken in het startmenu. Het is dezelfde wereld als het spel, met drie verschillen: je kijkt
van verder weg (`BUILD_ZOOM`), Amir is een geest, en er ligt een laag bediening overheen.

**De indeling.** Een balk boven (`#bbalk`) met de naam, openen, opslaan, de twee testknoppen en
de levellijn (`tekenLijn`, een canvas: het hele level van opzij). Een rand links (`#brand`) met een
knop per soort, die de lijst ernaast uitklapt (`bouwOpen`). Het venster rechtsonder (`#binfo`) is
voor wat je aanklikt. De instellingenbalk van het spel (`#bar`) staat in de bouwer uit; B haalt hem
terug.

**Amir is een geest.** Het spel tekent hem niet (`globalAlpha` 0 in de bouwer, ook zijn schaduw),
en de camera blijft aan hem hangen. `bouwD` is hoe diep je kijkt, in sprite-eenheden, en
`updateCamera` zet de camera daarop. Omdat de camera in de bouwer ook met de zoom schaalt, klopt
`-camY / scale` daar niet: gebruik `camDiepte(scale)` als iets wil weten hoe diep je kijkt. En
reken een klik met `pointerLift`, die telt `camY` mee.

**Een stuk erbij in de bouwer** is vier dingen:

1. een regel in `GEREEDSCHAP` (id, soort, naam; `sneeuw` voor een winterversie, `kop` voor een
   tussenkopje);
2. een tak in de `pointerdown` van de bouwer, op dat id, met een `placeProblem` ervoor;
3. een tak in `builderHit`, zodat je het kunt aanklikken, en een naam in `bouwNaam`;
4. de velden in `bouwVelden` (getal, vink, keuze of tekst), en wat er verder bij hoort in
   `bouwExtra`: regels die zeggen wat er geldt, en knoppen.

Het wegschrijven hoef je niet bij te werken voor een veld dat de bouwer niet zelf beheert:
`syncLevel` begint bij het level zoals het binnenkwam (`level.bron`) en zet daar alleen overheen wat
de bouwer kent. Beheert de bouwer een veld wel, zet het dan in `syncLevel`, en draai
`tools/bouwertest.js`.

**Gangen** maakt de bouwer goed in plaats van ze achteraf na te kijken. `holteMaak` legt een gang
onder een ravijn, laat hem aan de beginkant `HOLTE_BUUR` doorlopen, houdt hem van de speer aan het
begin weg en voegt hem samen met een gang die hij raakt (`holteVerbind`). `holteTrap` legt de
uitgang aan het linkereind: treden van hoogstens `HOLTE_TREDE.stap`, 200 breed, alles boven -441
onder het gat, en raakt het gat de ingang, dan loopt de gang verder door. Verander je daar iets aan,
draai dan `levelcheck.py` en de speelrobot op een level uit de bouwer.

**Schakelaars** (`bouwSchakelTeken`): elke koppeling een kleur uit `KOPPEL_KLEUR` en een nummer, een
stippelkader waar een ravijn later openscheurt, de stippelcirkel om de schijf van een rune
(`RAVIJN_RUNE.raak`) en de streep onder een zegel (`ZEGEL.op`). Het raakvlak van de rotswand
tekent `muurBoxen`.

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

## Assets

Sprites toegevoegd, vervangen of weggehaald? Draai daarna, in deze volgorde:

```
python3 tools/gen-klein.py
python3 tools/gen-offline-manifest.py
```

Het eerste script print de lijst die in `KLEIN_FAM` hoort te staan. Loopt die niet
gelijk, dan laadt een telefoon stilletjes de grote versie. Het tweede werkt de lijst
bij die de downloadknop afwerkt; sla je dat over, dan mist de offline-download
bestanden.

Een plaatje hoort alleen in de kleine set als het op een telefoon nog steeds groter
is dan het stukje scherm waar het terechtkomt. De afweging per familie staat in
`DOELEN` in `tools/gen-klein.py` en in de README.

De bodem en het dek van het veld `sneeuw` komen uit `tools/sneeuwdek.py`
(`grondrand_rots.png` en `sneeuwlaag_25..100.png`). Die staan met opzet niet in de kleine
set: `grondrand.png` staat daar ook niet in, en een dek dat anders geschaald wordt dan de
bodem eronder gaat schuiven.

De run van de baviaan komt uit `tools/baviaan_run_fix.py`: de aangeleverde frames staan ongewijzigd in
`enemies/baviaan/bron/run/`, het script plakt de kapotte handen en voeten dicht met stukken uit andere
frames en schrijft de speelversie naar `enemies/baviaan/run/`. Een map `bron/` gaat niet mee in de
offline-download, want het spel laadt hem nooit.

`design/grot/rots_vulling.png` (het steen boven een plafondlijn) komt uit `tools/rots_vulling.py`:
dat knipt het massieve deel uit `plafond_strook.png`, haalt het licht-donkerverloop eruit en
maakt de boven- en onderrand op elkaar aansluitend. Verandert de strook, draai het dan opnieuw.

De grotset in `design/grot/` hoort wel in de kleine set: die stukken zijn de grootste
bronnen van het spel en worden tot een tiende getekend. Dat mag hier omdat de tekencode
met de maten uit `grot.json` rekent en elk stuk naar die maat rekt; de ankerpunten
schuiven dus niet mee met de bronmaat. `grot.json` zelf blijft buiten de kleine set,
want `gen-klein.py` pakt alleen png's.

Geluid staat in `music/` en `sounds/`. De achtergrondnummers staan in `music/` en worden
aangemeld in `MUZIEK`; korte geluiden van personages en dieren horen in `sounds/`. Zo staan
`ahhit.mp3` en `stopit.mp3`, de twee kreten van Amir, bij de hyenageluiden en niet bij de
muziek. Beide mappen zitten in de offline-download, dus draai na een nieuw bestand
`tools/gen-offline-manifest.py` opnieuw.

Het speerteken heeft maar twee soorten eigen plaatjes, en die komen uit `tools/speerteken.py`:
het doek in drie kleuren (`design/botten/speerteken/doek_zwart`, `doek_vaal`, `doek_rood`), omgekleurd
op helderheid uit het blauwe doek van het skelet, en `riem.png`, de rode omwikkeling onder Amir zijn
speerpunt in `amirspear.png`, bruin gemaakt. Zo blijft het in de stijl van de rest. Teken er niets met
de hand bij; zoek een stuk uit een bestaande sprite en kleur dat om.

De twee slangen komen uit `tools/slang_kleur.py`: dat kleurt `enemies/slang1/` om naar de
zandslang in `enemies/slang1_zand/` en `enemies/slang2/` naar de zwarte in
`enemies/slang2_roet/`. Het spel tekent alleen die twee omgekleurde mappen (`SNAKE_DIRS`); de
originelen blijven staan als bron, en `venom.png` komt nog steeds uit `slang2/`. Verandert er
een frame, draai het script dan opnieuw. Ze staan niet in de kleine set.

Winterversies komen uit `tools/sneeuw.py` (rotsen en klimstukken), `sneeuw_bg.py`
(achtergrondpanelen), `sneeuw_dorp.py` (hutten, boom, struik) en `winter_art.py`
(dieren, grond, gras). Verandert een origineel, draai het bijbehorende script dan
opnieuw.

## Levels nakijken: tools/levelcheck.py

Na elk nieuw level, en na elke wijziging aan een level, draai je:

```
python3 tools/levelcheck.py            alle levels
python3 tools/levelcheck.py "Test 4"   alleen de levels waarvan de naam dit bevat
python3 tools/levelcheck.py -v         ook de info-regels
python3 tools/levelcheck.py level.json een level uit de bouwer, voor het in de HTML staat
```

Het script leest de leveldefinities uit de HTML, samen met de getallen waar het spel
zelf mee rekent (`CHAR_H`, `JUMP_V`, `GRAVITY`, de loopsnelheid en de sprint, `PLAFOND_WEG`,
de maten van keien, klif en fakkels). Het verandert niets aan de levels, het meldt alleen.
FOUT betekent: stuk, of tegen een regel uit dit document in. LET OP betekent: het werkt,
maar krap, of het spel lost het stilletjes voor je op. Een nieuw level gaat pas de deur uit
zonder FOUT. Wat het nakijkt: velden die `readLevel` niet kent, vaste dingen waar later een ravijn
openscheurt, ravijnen tegen de echte
sprong (met het plafond en het water erbij), decor boven een ravijn met dezelfde maten als
`schoonLevel`, het plafond boven keien en treden, rechtop kunnen lopen, of elke trede met
een sprong, een richel of een kei te halen is, of de klif achter de fakkels staat, alles
rond een gang onder de grond (zie "hoogteverschil onder de grond"), en met `valschade` of Amir
de vallen langs de route overleeft.

**De sprong.** `JUMP_V` en `GRAVITY` geven op papier 208, maar het spel rekent per beeld (eerst
de zwaartekracht, dan de hoogte), en dan komt hij lager uit: op 60 beelden per seconde 200, op het
traagste toestel (het spel neemt hoogstens 0,05 seconde per beeld) 184. Gemeten: een trede van
199 haalt hij, een van 203 niet. Het script rekent daarom met 200, en de sprong over een ravijn
ook per beeld.

**De route.** Voor de vallen loopt het script het level af zoals een speler dat doet: naar links,
over een gewoon ravijn springend, tegen een wand of kei op, en van een rand af op looptempo. Van
een kei of een richel springt hij liever dan dat hij valt, als hij dan hoger uitkomt. Waar hij
neerkomt rekent het per beeld uit, dus een val van een terras op een lagere trede die net verderop
begint, telt als de kleine stap die het in het spel ook is.

Maten die aan het scherm hangen rekent het uit voor 1280 bij 720 op Formaat 25; met `--hoog`
en `--formaat` kijk je een ander scherm na.

**Meldt iemand iets in een level dat niet samen kan** (een laag plafond boven een kei om op
te springen, een poel vlak voor een ravijn), dan komt dat er als regel bij: een functie met
`@regel('naam')` in `tools/levelcheck.py`, met de getallen uit de code en niet uit het hoofd.
Draai daarna alle levels opnieuw en meld wat de nieuwe regel in de bestaande levels vindt,
zonder die levels aan te passen (regel 1).

## De speelrobot: tools/speelrobot.js

`levelcheck.py` rekent, de speelrobot speelt. Hij laadt het echte spel in Chromium, zet een level
klaar en loopt het naar links uit op een vaste 60 beelden per seconde, los van hoe snel de
computer is. Hij springt als hij vastloopt, springt over een ravijn zonder gang eronder, laat zich
in een ingang vallen, pakt zijn speer, steekt naar doornbossen en vijanden voor hem, en blijft op
een kei staan om er vanaf te springen. Hij meldt waar hij landt, wat een val kost, waar hij
vastloopt en wat er in de console staat.

```
node tools/speelrobot.js "Test 4"               een level uit de HTML, op naam
node tools/speelrobot.js level.json --taai      een level uit de bouwer; --taai: levens komen terug
node tools/speelrobot.js "Test 4" --shots map   elke anderhalve seconde een schermafdruk
node tools/speelrobot.js level.json --vredig --wacht -1490:12
                                                op -1490 twaalf seconden blijven staan, zonder te steken
```

Regel 7 kijkt hij altijd na: per vijand onthoudt hij aan welke kant van elke kei en elk ravijn
die stond, en komt hij aan de andere kant terecht, dan staat er `REGEL 7` in de uitvoer. Met
`--wacht` laat je Amir op een kei of voor een ravijn staan tot de vijanden er zijn, met
`--vredig` steekt hij niet terug. Bij elk verloren leven staat erbij welke vijand het dichtst
bij was en wat die deed. Met `--hoe` staat bij elke overtreding waar de vijand de seconde
ervoor liep en wat hij deed.

Zo zijn twee gaten in regel 7 gevonden, allebei op telefoonformaat (852 bij 393), waar het spel
trager loopt en vijanden verder achter Amir raken:

- de keien telden voor de vijanden alleen binnen 2600 px van Amir (`platsNear`). Een vijand die
  verder achter hem zat, liep er dwars doorheen. De vijanden krijgen nu alle keien van het level;
- een hyena die buiten beeld op zijn beurt wacht, schoof mee met Amir en kon zo aan de overkant
  van een ravijn opduiken. Hij schuift nu niet meer over een ravijn of kei (`panBaan`).

Daarna: in tien levels op telefoonformaat geen enkele overtreding meer, en in proefstukken met
een kei en een ravijn kwam geen slang, zwarte slang, fosforslang, schorpioen, zwaardvechter,
hyena of panter erover.

Hij heeft Node en Playwright nodig (`npm i -g playwright`), en start zelf een webserver. Hij is
geen speler: een eindbaas verslaat hij niet, en een sprong die precies getimed moet worden mist
hij. Loopt hij vast waar `levelcheck.py` niets meldt, kijk dan wat daar staat. Is het de robot,
laat het dan; is het het level, dan hoort er een regel bij. Zo zijn de regels onder de grond
ontstaan.

## De bouwertest: tools/bouwertest.js

Opent elk level uit de HTML in de bouwer, slaat het op en leest het weer in, en meldt per level de
velden die daarbij veranderd of kwijtgeraakt zijn. Draai hem na elke wijziging aan de bouwer, aan
`readLevel` of aan `syncLevel`; hij verandert niets aan de levels.

```
node tools/bouwertest.js              alle levels
node tools/bouwertest.js "Test 4"     alleen de levels waarvan de naam dit bevat
node tools/bouwertest.js --shots map  daarna een schermafdruk van de bouwer
```

## Testen en afronden

Het spel wil van een webserver komen, anders weigert de browser de sprites:

```
python3 -m http.server
```

Er zijn geen tests en geen linter, dus kijk zelf na wat je aangeraakt hebt: speelt
het level uit, blijft de speer vindbaar, staat er niets in de lucht, en geeft de
console geen 404. Merkt de speler iets van je wijziging, werk dan `README.md` bij.
Commit in het Nederlands, in dezelfde toon als de bestaande geschiedenis: één regel
die zegt wat er nu anders is, en daaronder de uitleg.
