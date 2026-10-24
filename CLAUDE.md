# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Levels van een echte episode blijven met rust.** Nu is dat De Valse Koning (`VK_1` tot en met
`VK_8`). De Episode Test levels (`TEST_1` en verder) en de episode Baboon tests (`BAB_1` en verder) vallen niet onder deze regel: ze zijn er
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

**7. Vijanden komen niet over keien en ravijnen.** Slangen, fosforslangen en ook
de panters worden tegengehouden door een kei om op te springen en
door de rand van een ravijn: niet lopend, niet met een sprong of een duik, en ze duiken
ook niet aan de overkant op. Zo is een kei of een ravijn voor de speler een schuilplek.
Een schuilplek, geen veilige plek: een slang of schorpioen naast de kei mag Amir bovenop die
kei nog bijten of steken, want hun beet reikt tot de hoogte van een kei. Dat is zo bedoeld.
Een uitzondering mag alleen als de opdracht er expliciet om vraagt, of in een gevecht met
een eindbaas als je daar zelf voor kiest omdat het dat gevecht beter maakt; zeg dan
achteraf dat en waarom. Voor de panter is dat het veld `over: true` in zijn spawn
(`panBaan`); zonder dat veld blijft hij aan zijn kant. De bandiet is de staande
uitzondering: hij vault standaard over een kei naar Amir toe (zie "de bandiet"), zodat
een kei voor hem geen schuilplek is. Dat zet je alleen uit met `vault: false` in zijn
spawn, en alleen als de opdracht daar expliciet om vraagt.

**Vijanden gaan niet over treden; de weg omhoog is een lift.** Een vijand loopt op gelijkvloerse grond
en blijft op zijn niveau: terrassen en treden houden hem tegen (naast keien en ravijnen, regel 7). Hij
stapt geen trede op of af. Omhoog of omlaag komt hij alleen mee met een lift of rijzend stuk grond dat
op zijn x omhoog of omlaag komt: dan rijdt hij mee, net zoals Amir (`rijsDraagtMob`, zie "rijzende
grond"). De bandiet en de kooiman blijven daarnaast op hun eigen niveau en halen niet uit over een
hoogteverschil (`banZelfdeHoogte`, `kooiZelfdeHoogte`: de vloer onder Amir vergeleken met hun eigen vloer).

**Over plateaus klimmen is uit (opt-in, nergens in een level).** Met `klim: true` in een spawn stapt een
slang of fosforslang wel terrassen op en af, stap voor stap (`KLIM_STAP`, `KLIM_V`, `klimBase`, in
`blocksMonster`/`dropAhead`/`slangSchuif`). Dat gaf zweven op een trap (de hoogte liep achter het blok
aan), en is daarom in geen enkel level meer aan. Het zit nog wel in de sandbox onder Vijanden, bij
Slangen, **Klimt terrassen** (`sbKlim`), om het te bekijken.

**8. Geen versienummer in de code.** Linksboven staat vanzelf van wanneer de versie is die je
speelt, en onder **Updates** in het menu staan de laatste vijf samengevoegde pull requests, van
GitHub zelf, met per stuk of hij al in die versie zit. Zet dus nergens een nummer bij: vroeger
paste elke pull request dezelfde regel aan (`VERSIE`), en twee die tegelijk openstonden botsten
daar altijd op. Geef een pull request wel een titel die zegt wat er nieuw is, in een paar woorden:
die titel is wat de speler onder Updates leest.

**9. Een speer in een houten runeschijf blijft vastzitten.** Op een rots, in de rotswand of bij de
grot: wie de schijf raakt is zijn speer kwijt, en E haalt hem er niet uit. Het spel geeft er niet
vanzelf een nieuwe voor terug; of en waar de speler een nieuwe krijgt (een skelet, een speer in de
grond) is een keuze van het level, en een level zonder mag juist de uitdaging zijn. Wel moet die nieuwe
speer te halen zijn: een doornbos na de rune en voor het skelet houdt je voorgoed tegen, want zonder
speer kap je het niet (behalve met het mes van Jackal Fang). `levelcheck.py` meldt dat onder `speer na een rune`.

En de speer bij dat skelet moet ook echt te trekken zijn: E vasthouden kost zo'n 2 seconden stilstaan
met lege handen (`SKELET.trek.duur`), dus het eerste skelet na een rune hoort een vrije pull-zone te
hebben. Een slang, schorpioen, fosforslang of hyena mag er dichtbij staan (traag of wachtend, en de
lage zwaai werkt zonder speer), maar een charger niet zomaar.

Een krappe pull mag wel een bewuste uitdaging zijn, en dat geldt breder, ook voor toekomstige
mechanieken: een situatie mag zwaar en krap zijn als bewuste keuze, de vijand mag dus wel wat doen,
zolang hij te doen blijft en niet onmogelijk is. Bij de speer na een rune is het verschil: een
bandiet (net onder sprint, blijft je op de hielen) geeft ook met weglopen geen raam. `levelcheck.py`
(onder `speer na een rune`, met `SPEER_HAAL_VRIJ`) meldt daarom een bandiet binnen 1200 px voorbij het
skelet als FOUT. Dit kwam uit Valse Koning 1, waar twee bandieten op het skelet stonden.

**10. Werk zuinig, maar hou de kwaliteit.** Deze HTML is groot en de hele geschiedenis gaat elke beurt opnieuw
mee, dus token-verbruik telt. Houd je aan deze volgorde:

- **Breed of diep uitzoekwerk door de codebase** (iets vinden dat over veel secties verspreid zit, een bug
  diagnosticeren waarvan je alleen de conclusie nodig hebt) delegeer je naar een Sonnet-subagent, zodat dat zware
  lezen buiten de dure hoofdcontext blijft en alleen de conclusie terugkomt.
- **Kleine gerichte lookups** (een bestandsnaam, één functie, een paar regels) doe je zelf met grep en een
  gerichte read: een subagent kost daar meer dan hij bespaart.
- **Implementatie en edits** doe je zelf, niet in een subagent, zeker niet in een bestand dat je tegelijk bewerkt.
- Weeg het per taak af: delegeer alleen als het echt tokens scheelt, en zeg kort waarom.
- Een losstaande taak hoort in een eigen, korte chat: een lange chat met veel features betaalt de opgebouwde
  context telkens opnieuw. Stel een verse chat voor als een nieuw verzoek los staat van wat er nu loopt.

**11. Raak je een onderwerp uit de index aan, lees dan eerst zijn notitie.** De tabel onder
"Waar wat staat" wijst per onderwerp naar een bestand in `notities/`; de volledige uitleg,
de meetgeschiedenis en de sandbox-knoppen staan daar, niet meer hier. Is het breed, laat een
subagent die notitie lezen en alleen de conclusie teruggeven (regel 10).

## Waar wat staat

De HTML is opgedeeld met commentaarkoppen (`// ---- ... ----`). Zoek daarop, niet op
regelnummer, want die schuiven bij elke wijziging.

Per onderwerp de kop, een paar namen om op te grepen, en het notitiebestand met de
uitleg (leeg betekent: de wegwijzer hiernaast is alles wat er is).

| kop | grep | notitie |
| --- | --- | --- |
| laadpoort: een level loopt pas als alles binnen is | `LAAD`, `laadOpen`, `laadPoort` | notities/laadpoort.md |
| foutmelding: een fout een keer melden, ook als hij elk beeld terugkomt | `meldFout`, `tekenHerstel`, `ctxDiepte`, `laadMist` |  |
| versie: welke update er live staat | `versieTijd`, `document.lastModified`, `toonUpdates` | notities/wegwijzers.md |
| niet verder tekenen dan er in beeld komt | `zichtVak(marge)`, `view`, `null` | notities/tekenlagen.md |
| de zon: schijf, krans en ademende ring | `ZON`, `drawZon`, `ringAdem` | notities/zon.md |
| globale lichtlaag | `licht`, `SCENES` | notities/wegwijzers.md |
| de schaduw van Amir | `AMIR_SCHADUW`, `amirSilhouet`, `amirSilLeg` | notities/schaduw-amir.md |
| tribes: de keuze per run en de abilities | `TRIBE_CONFIG`, `RUN`, `tribeKies` | notities/tribes.md |
| muziek per level | `MUZIEK`, `MUZIEK_BASIS`, `muziek` | notities/wegwijzers.md |
| beeld: de grote of de kleine spriteset | `KLEIN_FAM`, `zetBron` | notities/wegwijzers.md |
| hppotion | de drinkkalebas |  |
| renstoot: sprinten en dan stoten | `RENSTOOT`, `glijStart`, `glijUpdate` | notities/speer.md |
| reserve-speren op de rug (prototype) | `RUG`, `RUG_MAX`, `rugSperen` | notities/rug-speren.md |
| zicht: een vijand ziet je alleen als er niets tussen zit | `ZICHT`, `vijandZiet`, `zichtWaak` | notities/zicht.md |
| health-balk: 3 levens met een balkje boven het hoofd | `HP_BALK`, `HP_BALK_LEVENS`, `vijandHpBalk` | notities/health-balk.md |
| bukken, jump frames, tempo | Amir zijn bewegingen |  |
| rotsen om op te springen | `rocks` | notities/wegwijzers.md |
| winter: episode Winter World | `WINTER_SRC`, `winterOn()`, `winterPic()` | notities/wegwijzers.md |
| bodem en sneeuwdek | `sneeuw` | notities/wegwijzers.md |
| het verhaal bij een episode | `VERHAAL`, `SLOT`, `verhaalToon()` | notities/episodes.md |
| Episode De Valse Koning | `VK_1`, `VK_8`, `VK_LEVELS` | notities/episodes.md |
| Episode Test levels | `TEST_1`, `TEST_47`, `KAART_BLAD` | notities/episodes.md |
| Episode Baboon tests | `BAB_1`, `BAB_4`, `BAB_LEVELS` | notities/episodes.md |
| goudaapje: het kleine gouden aapje en de arena | `GAAP`, `gaapSpawn`, `updateGoudapen` | notities/goudaapje.md |
| het mes: Jackal Fang van Impungushe | `MES`, `mesInHand`, `mesTeken` | notities/mes.md |
| T-splitsing in de talent tree | `varianten`, `TRIBE_CONFIG`, `tbSplit` | notities/tribes.md |
| Feign Death | `SCHIJN`, `schijnDoodVang`, `hurtPlayer` | notities/wegwijzers.md |
| lichtkaart: het licht onder de grond | `LK`, `drawLichtkaart` | notities/lichtkaart.md |
| terrassen en richels | `terraces`, `ledges`, `drawLedge` | notities/rotsraster.md |
| schacht: een kloof om uit te klimmen | `schacht`, `schacht: true`, `grotMassa` | notities/schacht.md |
| hogere savannelaag: een terras van grond | `SAV_LAAG`, `savanneLaag`, `drawClimb` | notities/savannelaag.md |
| zwevende savannelaag: een dik savanneblok in de lucht | `ZWEEF`, `zweefList`, `savanneLaag` | notities/savannelaag.md |
| de rotswand rechts | `cliffs` | notities/wegwijzers.md |
| grotten: rots als een raster van cellen | `grotten` | notities/rotsraster.md |
| plafond: de rots boven je, als hoogtelijn | `plafond` | notities/plafond.md |
| muur unlock: de rotswand met het rune-symbool | `MUUR`, `MUUR_GROT`, `muurGrotSet` | notities/muur.md |
| ravijn in de winter | `RAVIJN_WINTER`, `ravijnWandNu()`, `ravijnSneeuwRand()` | notities/ravijn.md |
| zegel in de grond: de runeschijf plat, als schakelaar | `ZEGEL`, `zegelGrond`, `zegelUpdate` | notities/zegel.md |
| verstopt zegel: onder het zand, tot de lage zwaai het blootveegt | `ZEGEL_VERSTOP`, `ZEGEL_VEEG`, `zegelVeegUpdate` | notities/zegel.md |
| verstopt zegel per vloer, en in de Level Maker | `ZEGEL_VLOER`, `zegelVloerSoort`, `mkVulZegel` | notities/zegel.md |
| speerval: een speer in de rotswand die een zegel losschiet | `SPEERVAL`, `speervalZegel`, `zegelUpdate` | notities/speerval.md |
| zakplafond: een plafond dat zakt als je op een zegel stapt | `ZAK`, `zakStand`, `rust` | notities/zakplafond.md |
| rijzende grond: steen dat op een zegel uit een ravijn komt | `RIJS`, `rijsUpdate`, `duur` | notities/rijzende-grond.md |
| takelwiel met plateau: een rad dat je met je speer slaat | `TAKEL`, `takelLaad`, `takelReset` | notities/takelwiel.md |
| masker: geverfde stukken die een deel van het level verbergen | `MASKER`, `maskerLijst`, `maskerVan` | notities/masker.md |
| de draaiende speer: rollen om de lengteas in de vlucht | `DRAAI`, `draaiImgs`, `draaiBeeld(soort, t)` | notities/speer.md |
| skelet met speer | `SKELET`, `skeletTrek`, `skeletUpdate` | notities/skelet.md |
| speerteken: een speer in de grond met een zwart doek en schedels | `TEKEN`, `tekenUpdate`, `tekenTeken` | notities/decor.md |
| licht op de runerotsen | `RUNE_LICHT`, `runeLichtMaak`, `runeGrondSchaduw` | notities/wegwijzers.md |
| runeschijf: het losse symbool | `runeSchijf(ctx, x, y, r, {aan, spiegel})` | notities/wegwijzers.md |
| vallen: schade bij een diepe val | hoe diep een val telt en wat hij kost |  |
| schorpioen, het projectiel, spannen en werpen, de geworpen speer | `javTegenDak`, `javFloor`, `vloerBij` | notities/speer.md |
| fakkel: een geanimeerde wandfakkel | `FAKKEL`, `fakkelLaad`, `fakkelFrame` | notities/fakkel.md |
| personages, dorpsdecor | `VILLAGE` | notities/wegwijzers.md |
| Amir zegt er iets van als hij geraakt wordt | `SFX_RAAK`, `playRaak()` | notities/geluid.md |
| Amir zegt iets als een vijand sterft | `SFX_RUST`, `vijandDood(baas)`, `DOOD_KANS` | notities/geluid.md |
| stap voor stap leren spelen | `tutorial` | notities/wegwijzers.md |
| gaten in de grond | `gaps`, `grondDoorlopen` | notities/wegwijzers.md |
| zuil: een smalle strook grond tussen twee ravijnen | `ZUIL`, `zuilBij`, `zuilWand` | notities/zuil.md |
| zuil met een hoogte: hoger of lager dan de grond | `ZUIL_HOOG`, `zuilLijst`, `zuilBasis` | notities/zuil.md |
| put: een ravijn in de bodem van een gang | `PUT`, `putLijst`, `putBij` | notities/put.md |
| stof, sneeuwval, het weer | deeltjes en het weerplan per potje |  |
| het weer: regen, onweer, zandstorm, sneeuw en sneeuwstorm | `WEER`, `weerDoel`, `updateWeer` | notities/wegwijzers.md |
| vegetatie, water, doornbos | `props`, `water`, `thickets` | notities/wegwijzers.md |
| schilden in de wind | `SCHILD`, `schildStofUpdate`, `schildTil` | notities/decor.md |
| slangen: kleur, zicht en patrouille | `SNAKE_DIRS`, `slangZiet`, `startPatrouille` | notities/slangen.md |
| zwarte panter, de witte panter, de hyena | de grote vijanden |  |
| de bandiet: een rover met een kromzwaard | `BAN`, `banLaad`, `makeBandiet` | notities/bandiet.md |
| de schildbandiet: loopt met zijn schild op en valt springend aan | `SCHB`, `makeSchildman`, `updateSchildman` | notities/schildbandiet.md |
| schildstaat: het schild in vier standen, van heel tot weg | `SCHB_STAAT`, `SCHB_SETS`, `schbStaat` | notities/schildbandiet.md |
| de bandiet-arena: het geënsceneerde eindgevecht | `BANDARENA`, `bandArenaStart`, `bandArenaWachters` | notities/bandiet.md |
| baviaan: de eindbaas in wording | `BAVIAAN`, `baviaanLaad`, `baviaanTeken` | notities/baviaan.md |
| speerbeet: de baviaan pakt je speer | `BAV_BEET`, `BAV_MOND`, `BAV_SPEER` | notities/baviaan.md |
| speer in de baviaan: de speerval blijft in zijn borst zitten | `BAV_VALSPEER`, `bavSpeerTeken`, `baviaanTeken` | notities/baviaan.md |
| voorgrond: de laag tussen de camera en Amir | `VOORGROND`, `VG_SOORT`, `VG_LAGEN` | notities/voorgrond.md |
| achtergrondlagen, uitzicht per level | `SCENE0`, `SCENES` | notities/wegwijzers.md |
| startscherm, level maken, menu: kaartjes per level | menu en bouwer |  |
| kaarslicht: de startfoto van onderen belicht | `KAARS`, `kaarsStart`, `kaarsLus` | notities/kaarslicht.md |
| level maken | `GEREEDSCHAP`, `bouwOpen`, `bouwVelden` | notities/bouwer.md |
| elk level nakijken op decor boven een ravijn | `schoonLevel`, `schoonKomend`, `komendeRavijnen` | notities/ravijn.md |
| wat er staat waar een ravijn openscheurt | `RAVIJN_DECOR`, `ravijnDecor`, `ravijnDecorStap` | notities/ravijn.md |
| sandbox | de vrije testmodus |  |

Op schijf: `karakters/` (Amir, dorpeling, dorpelinge), `enemies/`, `design/` (decor,
achtergronden, water, dorp, botten), `klein/` (dezelfde mappen op halve grootte),
`music/` en `sounds/`, `tools/` (de Python-scripts), `icons/`, `sw.js` en
`offline-assets.json` (de webapp).

## Een level lezen of schrijven

Amir loopt naar links, dus alle `x` zijn negatief en lopen op naarmate je verder
komt. Een leveldefinitie is een gewoon object; de bouwer in het spel exporteert
precies hetzelfde formaat naar JSON.

De velden met een langere uitleg staan in `notities/velden.md`; hieronder kort.

| veld | wat |
| --- | --- |
| `name` | naam op het kaartje in het menu |
| `lagen` | sleutel uit `SCENES`: welk uitzicht dit level krijgt |
| `muziek` | sleutel uit `MUZIEK`: welk deuntje eronder loopt (`bg` voor het oude thema); zonder dit veld `MUZIEK_BASIS`, Dark Africa |
| `winter` | `true` zet het hele level in de sneeuw (witte dieren, sneeuwversies van het decor) |
| `sneeuw` | sneeuw op de grond, los van `winter`: `{soort, dek, van, tot}` (zie hieronder) |
| `weer` | het weer onderweg: `[{x, soort, sterkte}]`, `soort` uit `WEER.soorten` (`droog`, `regen`, `onweer`, `zandstorm`, `sneeuw`, `sneeuwstorm`); voorbij `x` slaat het om (zie "het weer") |
| `valschade` | `true` laat een diepe val levens kosten (standaard uit): vanaf een Amir diep een leven, vanaf twee Amir twee (`VAL_VRIJ`, `VAL_ZWAAR`, `VAL_MAX`), en vanaf zes Amir diep is hij dodelijk (`VAL_DOOD`, `fallDeath` in `valLand`), ongeacht je levens. `levelcheck.py` (regel `vallen`) meldt een val van zes Amir of dieper als FOUT |
| `rugMax` | reserve-speren op de rug: 1 in de hand plus zoveel op de rug (0 tot 5, standaard 0 = uit) (zie `notities/velden.md`) |
| `zicht` | `true`: een vijand merkt Amir pas op als hij hem echt kan zien. Voor hem een halve cirkel met een zichtlijn die grond en rots tegenhouden, achter hem de oude afstand maar alleen op zijn eigen niveau, en na 3 s zonder zicht vergeet hij je. Zonder veld de oude manier (alle bestaande levels); een nieuw level krijgt `zicht: true`, een spawn met `zicht: false` houdt toch de oude manier (zie `notities/zicht.md`) |
| `hpBalk` | `true` of een lijst soorten: 3 levens met een health-balkje boven het hoofd, ook voor Amir; de schildbandiet krijgt een schildbalk erboven. Zonder veld uit, een nieuw level krijgt `hpBalk: true` (zie `notities/velden.md`) |
| `hoogUitzicht` | `true`: gestapelde dikke grondlagen zien er op hoogte hetzelfde uit als de basis (zie `notities/velden.md`) |
| `view` | een getal van 0,5 tot 1: uitgezoomd spelen; een nieuw level krijgt standaard `view: 0.8` (zie `notities/velden.md`) |
| `zichtBreed` | een doel-wereldbreedte in beeld in plaats van een vaste `view`; geen level gebruikt het nog (zie `notities/velden.md`) |
| `worp` | `'schaal'` zet de schaalworp aan: de hoek loopt op zolang je vasthoudt, van vlak tot 30 graden (`THR_HOEK_MAX`); zonder dit veld de twee trappen. In de sandbox de knop Worp onder Speerworp |
| `speerInHand` | `true`: Amir begint met de speer in de hand in plaats van hem voor zich uit de grond te pakken; de Level Maker nieuwstijl zet dit in elk level, de echte episodes hebben het niet |
| `rocks` | keien om op te springen: `{x, s}` |
| `spawns` | vijanden: `{x, k}`, `k` is groen/zwart/knock/scorp/hyenas/panter/fosfor/bandiet/kooiman/meelman/schildman, met vlaggen per soort (zie `notities/velden.md`) |
| `bandArena` | `true`: het level is een bandiet-arena (Valse Koning 8), zoals de goudaap-arena maar met de elite-garde (zie "de bandiet-arena") |
| `bandietGolf` | een oplopende golf bandieten: `{van, tot, ramp, max, dolk}` (zie `notities/velden.md`) |
| `duel` | per kooiman-spawn `{x, k: 'kooiman', duel}`; standaard aan is het 1-op-1 duel, `duel: false` de gewone kooiman (zie `notities/velden.md`) |
| `props` | decor: `{x, k, s, f, v}`, `k` uit `PROPS`, `f` spiegelen, `v` verre laag |
| `village` | dorpsplaten uit `VILLAGE`: `{id, x, depth, flip}` |
| `gaps` | ravijnen: `{x, w}` |
| `water` | poelen: `{x, n}` met `n` = aantal middenstukken |
| `thickets` | doornbossen: `{x, n, seed}` |
| `terraces` | terrassen om op te klimmen: `{r, l, h}`; negatieve `h` is een trede in een gang, `grond: true` een hogere savannelaag (zie `notities/velden.md`) |
| `holtes` | gangen onder de grond: `{r, l, diep}`, een ravijn erboven is de ingang, een gat met treden de uitgang (zie hieronder) |
| `putten` | ravijnen in de vloer van een gang: `{x, w}`, helemaal binnen een holte (zie "put") |
| `zuilen` | zuilen met een hoogte in een ravijn of put: `{x, w, h}`, `h` van -250 tot 180 boven de grond of de vloer (zie "zuil met een hoogte") |
| `ledges` | richels aan een wand: `{x, h, s}`; met `f` gespiegeld (vlakke kant rechts, punt naar links, botsing naar links van `x`), met `achter: true` achter de schacht-wand getekend (zie "De schacht") |
| `zwevers` | zwevende savannelagen: `{r, l, h, onder, look}`, een dik savanneblok in de lucht met lucht eronder; `h` de looplijn bovenop, `onder` de onderkant (de ruimte eronder; onder `CHAR_H` kruip je er gebukt onderdoor), `look: 'rots'` tekent het als een rotsoverhang (zie "zwevende savannelaag") |
| `grotten` | rotsgebieden als raster: `{x, cel, y, grid, ...}` (zie hieronder); met `schacht: true` is de wand de plafondvulling met de tanden erlangs in plaats van de terrasplaat (zie "De schacht") |
| `start` | waar Amir begint (wereld-x); zonder dit veld op 0. Voor een schacht waar hij tussen de wanden start in plaats van ernaartoe te lopen |
| `plafond` | de rots boven je als hoogtelijn: `[{x, y}, ...]` (zie hieronder) |
| `muur` | de rotswand met het rune-symbool: `{x, speer}`, of met `soort: 'grot'` de rotsboog met de kei (zie hieronder) |
| `hppotions` | drinkkalebassen: `{x, y}` |
| `skeletten` | een zittend skelet met een speer erin: `{x, f}`, `x` is het midden van het skelet, `f` spiegelt; E bij de schacht trekt hem eruit (zie hieronder) |
| `tekens` | speertekens: `{x, v, f}`, `v` is `teken`, `gebroken`, `gekruist`, `jagers` of `kalebas`, `f` spiegelt; decor, behalve dat het mes de kalebas lossnijdt |
| `fakkels` | geanimeerde wandfakkels: `{x, y, s, f}`, `x` de schacht, `y` de hoogte van de voet boven de grond in Amir (0 = op de grond, hoger = tegen een wand), `s` schaal, `f` spiegelen; brandend decor met gloed, vonken, schaduw en vuurgeluid (zie "fakkel") |
| `talentKeuze` | `true`: voor het begin kies je zelf welke talents gelden, van alle tribes (alleen voor een Test level; nu Test 14) |
| `zegels` | zegels plat in de grond: `{x, ravijn, sluit, breed, muur, speerval, teken, vijand, plafond, rijs, speer, verstop, veeg, dak}`; met `dak` ligt hij boven een gang op de savanne in plaats van op de gang-bodem, met `verstop` ligt hij onder het zand tot de lage zwaai hem blootveegt, `veeg` kiest de onthulling (standaard de wolk, traag en middel), `veegDuur` en `veegMaat` het tempo en de grootte, `vloer` de kleur van het zand (zie `notities/velden.md`) |
| `rijzers` | steen dat uit een ravijn omhoog komt: `{id, r, l, tot, van, v, wacht, duur}`, `id` de naam waar een zegel of een rune (`doel: true`) met `rijs` naar wijst, `tot` en `van` de bovenkant boven en beneden (standaard -1 en -900), `wacht` seconden voor hij begint, `duur` seconden boven voor hij terugzakt (zie "rijzende grond"); met `zak: true` staat hij boven en zakt hij onder Amir weg |
| `takel` | een takelwiel met een hangend plateau; sla het rad met je speer, het plateau draagt en veert (zie `notities/velden.md`) |
| `maskers` | geverfde stukken die een deel van het level verbergen: `{id, look, vakken}` (zie `notities/velden.md`) |
| `zakplafond` | stukken rots die zakken: `{r, l, rust, dicht, v, schok, duw}` (zie `notities/velden.md`) |
| `speervallen` | speren in de rotswand: `{x, h}`, `x` de klif waar hij in zit (uit `cliffs`), `h` de hoogte in Amir (standaard 0,82); een zegel met `speerval` schiet hem los (zie "speerval") |
| `runes` | ravijnen met een rune op een rots ervoor: `{x, breed, rots, groot, hoog, doel}` (zie `notities/velden.md`) |
| `fg` | strook waarover de voorgrondbegroeiing ligt: `{from, to}` |
| `voorgrond` | de onscherpe laag vlak voor de camera: `{stroken: [{van, tot, dicht, struik, kei}], los: [{x, k, s, f}]}`, `k` uit `VG_SOORT`; los van `fg`. Zonder dit veld krijgt het level de standaard, met `false` heeft het er geen (zie hieronder) |
| `arena` | het veld van de eindbaas: `{c}` |
| `cliffs` | de afsluitende rotswand: `{x}`, staat altijd achter `ends` |
| `ends` | de fakkels die het level uitspelen: `{x}` |
| `npcs` | dorpelingen: `{x, k, f, s}` |
| `tips` | tekst onderweg: `{x, t}` |
| `pijlen` | rode pijlen in de lucht die iets aanwijzen: `{x, t}`, alleen voor testlevels (Test 47) |

### Een level toevoegen (alleen na toestemming)

1. De definitie erbij, na de laatste van die reeks. Zet er `view: 0.8` in: een nieuw level
   staat standaard op die laptop-zoom (zie het veld `view`). De bestaande episodes blijven staan
   zoals ze zijn (rule 1), dus pas hun view niet mee aan. Zet er ook `hpBalk: true` in: elke
   vijand en Amir krijgt in een nieuw level een health-balk (zie "health-balk"). En `zicht: true`:
   een vijand ziet je dan alleen als er niets tussen zit (zie "zicht"). De bouwer en Maker
   nieuwstijl doen dit al zelf.
2. De naam in de array van die reeks (`VK_LEVELS`, `TEST_LEVELS` of `BAB_LEVELS`).
3. Een ondertitel in `SUBS`, op de naam van het level.
4. Een eigen uitzicht in `SCENES` als het level er anders uit moet zien.
   De voorgrond komt er vanzelf bij (zie hierboven); zet alleen een eigen `voorgrond` als het level
   daar iets mee wil.
5. `python3 tools/levelcheck.py` draaien, en elke FOUT oplossen voor je commit (zie
   hieronder).

### Een episode toevoegen

Die vijf stappen, plus: een knop in `menuEpisodes` (het scherm met alle episodes, dat onder de knop
Episodes in `menuChoose` hangt; een nieuwe losse reeks die geen episode is, zoals Baboon tests, krijgt
juist een knop in `menuChoose` zelf), een eigen `menuXxx`-blok in de
HTML naar het voorbeeld van `menuTest`, en die aanmelden in `buildCards`,
`markCards` en `showMenu` (die kiezen nu tussen `cardsVK`/`menuVK`, `cardsBab`/`menuBab` en
`cardsTest`/`menuTest`, en `toMenu` ook), en de reeks in `tools/bouwertest.js`, `tools/speelrobot.js`
`tools/runecheck.js` en `tools/beeldgelijk.js`. De Terug-knop van een episodescherm krijgt de klasse `menuepisodes` (terug naar
Episodes), niet `menuback` (dat gaat naar het Levels-scherm). Een nieuwe episode begint altijd met de tribekeuze: `runStart` in zijn speelknop, en `tribeLijst` geeft
hem alleen wat de speler verdiend heeft (alleen `TEST_LEVELS` krijgt alles). Wil de episode een
verhaal, zet dan de tekst in `VERHAAL` en `SLOT` en `verhaalAan` in zijn speelknop. De Valse Koning is het
voorbeeld van een episode met verhaal en Nightmare.

### Een vijand of prop toevoegen

Tekencode en gedrag erbij, opnemen in `PROPS`, `VILLAGE` of de dierenlijst, en
knoppen in de sandbox. Kies de soort (vast, los, plant of ver, zie "wat mag waar") en zet hem in
de vijf functies die daarbij horen. Pas daarna is de vraag aan de orde of er een level bij moet.

## De bouwer

Level maken in het startmenu: dezelfde wereld als het spel, met een laag bediening
eroverheen. Hoe de indeling werkt en hoe je er een stuk aan toevoegt (`GEREEDSCHAP`,
`bouwVelden`, `bouwExtra`, `holteMaak`, `bouwSchakelTeken`, `syncLevel`): zie
`notities/bouwer.md`. Na een wijziging aan de bouwer, `readLevel` of `syncLevel` draai je
`tools/bouwertest.js`.

## Sandbox

De vrije testmodus: vlakke grond, een leeg level, geen vijanden en geen levens. Een knop
erbij is een `<button>` in `<div id="sandbox">` plus de afhandeling in de sandbox-sectie,
in het juiste tabblad (`.sbcat`). Zie `notities/sandbox.md`.

## Assets

Welk script draai je na welke wijziging (de volledige uitleg staat in `notities/assets.md`):

- **Sprites toegevoegd, vervangen of weggehaald** → `python3 tools/gen-klein.py` en daarna
  `python3 tools/gen-offline-manifest.py` (in die volgorde). Het eerste print de lijst voor
  `KLEIN_FAM`, het tweede werkt de offline-download bij.
- **Bodem of sneeuwdek** (`grondrand_rots.png`, `sneeuwlaag_25..100.png`) → `tools/sneeuwdek.py`
- **Run van de baviaan** → `tools/baviaan_run_fix.py`
- **`design/grot/rots_vulling.png`** → `tools/rots_vulling.py`
- **Speerteken** → `tools/speerteken.py`
- **Slangen** (zand, roet, knock) → `tools/slang_kleur.py`
- **Dood van de schildbandiet** (speer eruit, lijf op de grond) → `tools/schildbandiet_dood.py`, daarna `gen-klein.py` en `gen-offline-manifest.py`
- **Elite-garde** → `tools/bandiet_elite_kleur.js`, daarna `gen-klein.py` en `gen-offline-manifest.py`
- **Kooi-plaat van de kooiman** → `tools/kooi_kleur.py`, daarna `gen-klein.py` en `gen-offline-manifest.py`
- **Goudaapje** → `tools/goudaapje_kleur.js`
- **Tribe-logo's** → `tools/tribe_logos.py`
- **Winterversies** → `tools/sneeuw.py`, `sneeuw_bg.py`, `sneeuw_dorp.py`, `winter_art.py`

Geluid staat in `music/` (achtergrondnummers, aangemeld in `MUZIEK`) en `sounds/` (korte
geluiden); beide zitten in de offline-download, dus draai na een nieuw bestand
`tools/gen-offline-manifest.py` opnieuw.

## De tools

De volledige uitleg (rekenregels, de sprong, de route, voorbeelden) staat in `notities/tools.md`.

### Levels nakijken: `tools/levelcheck.py`

Na elk nieuw level en na elke wijziging aan een level:

```
python3 tools/levelcheck.py            alle levels
python3 tools/levelcheck.py "Test 4"   alleen de levels waarvan de naam dit bevat
python3 tools/levelcheck.py -v         ook de info-regels
python3 tools/levelcheck.py level.json een level uit de bouwer, voor het in de HTML staat
```

FOUT betekent: stuk, of tegen een regel uit dit document in. LET OP betekent: het werkt, maar
krap, of het spel lost het stilletjes op. Een nieuw level gaat pas de deur uit zonder FOUT.

### De speelrobot: `tools/speelrobot.js`

Laadt het echte spel in Chromium en loopt een level naar links uit op vaste 60 fps; meldt waar
hij landt, wat een val kost, waar hij vastloopt, wat er in de console staat, en overtredingen
van regel 7 (`REGEL 7`). Heeft Node en Playwright nodig (`npm i -g playwright`).

```
node tools/speelrobot.js "Test 4"               een level uit de HTML, op naam
node tools/speelrobot.js level.json --taai      een level uit de bouwer; --taai: levens komen terug
node tools/speelrobot.js "Test 4" --shots map   elke anderhalve seconde een schermafdruk
node tools/speelrobot.js level.json --vredig --wacht -1490:12
                                                op -1490 twaalf seconden blijven staan, zonder te steken
```

### Schijven nameten: `tools/runecheck.js`

Laadt de HTML in Chromium en vraagt het spel van welke afstanden de speer elke `runes`-schijf
of `muur` raakt, en of die strook in beeld ligt.

```
node tools/runecheck.js                 alle levels, op 1280x720, 852x393, 1440x620 en 1920x1080
node tools/runecheck.js "Valse"         alleen de levels waarvan de naam dit bevat
node tools/runecheck.js --formaat 25    het schuifje Formaat
node tools/runecheck.js --schermen 1280x720,852x393
```

FOUT betekent: nergens te raken, of nergens te raken met de schijf in beeld. LET OP: er blijft
minder dan 60 px over.

### Hetzelfde beeld nameten: `tools/beeldgelijk.js`

Tekent hetzelfde bevroren beeld twee keer, met een snelheidsvlag uit en aan, zodat elk
pixelverschil van de wijziging komt.

```
node tools/beeldgelijk.js --vlag LAGFIX                een vaste reeks van twaalf levels
node tools/beeldgelijk.js --vlag LAGFIX "Test 27"      alleen dit level
node tools/beeldgelijk.js --vlag LAGFIX --plekken -300,-2000
node tools/beeldgelijk.js --vlag LAGFIX --breed 852 --hoog 393
```

`gelijk` op elke plek betekent: geen enkele pixel anders. Zet de vlag na het nameten weer uit.

### Het schildduel: `tools/schildduel.js`

Speelt het gevecht tegen de schildbandiet met een paar speelstijlen en meldt per potje de duur,
de treffers en in welk stuk van zijn aanval Amir hem raakte. Draai het na een wijziging aan `SCHB`.
`--reactie 0.3` zet de reactietijd, `--breed 1280 --hoog 720` het scherm, `--fotos map` maakt foto's.

### De bouwertest: `tools/bouwertest.js`

Opent elk level in de bouwer, slaat het op en leest het weer in, en meldt per level de velden
die veranderd of kwijt zijn. Draai hem na elke wijziging aan de bouwer, `readLevel` of `syncLevel`.

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
