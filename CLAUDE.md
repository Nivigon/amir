# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Levels van een echte episode blijven met rust.** Nu is dat De Valse Koning (`VK_1` tot en met
`VK_8`). De Episode Test levels (`TEST_1` en verder) de episode Baboon tests (`BAB_1` en verder) en de episode Test levels stad (`STAD_1` en verder) vallen niet onder deze regel: ze zijn er
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
stapt geen trede op of af. Een terras, mesa of muur op het oppervlak boven een gang houdt een vijand in die
gang niet tegen: dat staat op de savanne, niet in de gang (`blocksMonster`, `terrainHGang`). Omhoog of omlaag komt hij alleen mee met een lift of rijzend stuk grond dat
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

**12. Bazen zijn een eigen categorie, en een baas komt er alleen na toestemming.** Het spel kent drie
soorten tegenstanders:

- **Vijanden**: zandslang, zwarte slang, knockslang, fosforslang, schorpioen, hyena, bandiet, schildbandiet,
  kooiman, meelman, kruisboogbandiet, zweepman en goudaapje. Die mag je in de sandbox en in een testlevel (regel 1 en 3) gewoon neerzetten.
- **Bazen**: de panter (zwart, en wit in een winterlevel: dezelfde spawn `k: 'panter'`, altijd met `boss: true`
  en de arena-camera, drie treffers), de baviaan (`BAVIAAN`, de eindbaas in wording) en Brutus (in beeld Nyundo,
  `BRU`, de baas van Stad 6: Het plein, zestien treffers, zie `notities/brutus.md`). Een baas zet jij
  nergens neer zonder dat de opdrachtgever het goed vindt: niet in een level, niet in een arena-golf, en ook
  niet "even om iets te laten zien". Dat vraag je vooraf, per geval, voordat je iets bouwt. Mag het, dan bouw
  je het; zonder antwoord bouw je het niet.
- **Arena's**: de geënsceneerde eindgevechten, zoals de bandiet-arena van Valse Koning 8 (`bandArena`) en de
  goudaap-arena van Baboon 4 (`apenArena`, `grotArena`), en in de sandbox de arena-modus en de arena gates
  (`sbGates`, drie poorten met rondes, zie `notities/arena-gates.md`). Dat is een vorm van level, geen baas: er staat geen
  baas in, maar golven vijanden tussen twee wanden met de camera in het midden. De kooiman-baas uit
  `notities/kooiman-baas.md` is een concept voor zo'n arena en is nog niet gebouwd. Een nieuwe arena is een
  nieuw level en valt dus onder regel 3.

Deze regel gaat over wat jij bouwt. De speler zelf mag in de Maker nieuwstijl een panter of baviaan in zijn
level zetten, en de knoppen daarvoor blijven staan: haal ze niet weg en zet er geen rem op. De bestaande
levels (de panter in Valse Koning, de baviaan in Baboon 1, de arena's) en de bestaande testlevels blijven
zoals ze zijn, net als de knoppen **Als eindbaas** en **Baviaan** in de sandbox.

**13. Een stadsverbetering gaat volgens de werklijst.** Vraagt de opdrachtgever om een stadsverbetering,
lees dan eerst `notities/stad-verbeteren.md` en volg "Zo werken we": een stap per keer, eerst precies 3
suggesties zonder iets te bouwen, de opdrachtgever kiest er een, bijsturen tot het goed is, en pas dan
afvinken en het cijfer bijwerken.

**13b. De kit van Amir verbeteren gaat volgens de takenlijst.** Vraagt de opdrachtgever om de kit-lijst
("verbeter Amir kit"), lees dan `notities/kit-verbeteren.md` en volg "Zo werken we": laat de open taken zien,
de opdrachtgever kiest er een, bouwen en bijsturen tot het goed is, en pas dan afstrepen en het cijfer bijwerken.

**14. Impungushe ligt stil.** Breng de tribe Impungushe (de jakhals, het mes, Feign Death) niet zelf
ter sprake: stel er geen ideeën, talents of abilities voor in, en deel er niets bij in, tot de opdrachtgever
er zelf weer mee begint. Bestaande code en knoppen blijven gewoon staan. Een talent mag wel bij twee tribes
passen; ideeën voor de kit staan in `notities/kit-ideeen.md`.

## Waar wat staat

De HTML is opgedeeld met commentaarkoppen (`// ---- ... ----`). Zoek daarop, niet op
regelnummer, want die schuiven bij elke wijziging.

Per onderwerp de kop, een paar namen om op te grepen, en het notitiebestand met de
uitleg (leeg betekent: de wegwijzer hiernaast is alles wat er is).

| kop | grep | notitie |
| --- | --- | --- |
| laadpoort: een level loopt pas als alles binnen is | `LAAD`, `laadOpen`, `laadPoort` | notities/laadpoort.md |
| lui laden per level: wat niet elk level gebruikt komt pas binnen als het nodig is | `laadLevel`, `slangLaadLevel`, `hyLaadLevel`, `dorpLaadLevel` | notities/laadpoort.md |
| geheugen vrijgeven bij een levelwissel: wat het nieuwe level niet gebruikt gaat weer weg | `laadNodig`, `laadNieuw`, `laadVrij` | notities/laadpoort.md |
| foutmelding: een fout een keer melden, ook als hij elk beeld terugkomt | `meldFout`, `tekenHerstel`, `ctxDiepte`, `laadMist` |  |
| versie: welke update er live staat | `versieTijd`, `document.lastModified`, `toonUpdates` | notities/wegwijzers.md |
| niet verder tekenen dan er in beeld komt | `zichtVak(marge)`, `view`, `null` | notities/tekenlagen.md |
| de zon: schijf, krans en ademende ring | `ZON`, `drawZon`, `ringAdem` | notities/zon.md |
| globale lichtlaag | `licht`, `SCENES` | notities/wegwijzers.md |
| de schaduw van Amir | `AMIR_SCHADUW`, `amirSilhouet`, `amirSilLeg` | notities/schaduw-amir.md |
| licht op personages: zon, fakkel en raam leggen een rand van licht op Amir en de vijanden | `PLICHT`, `persLicht`, `plichtBronnen` | notities/licht-personages.md |
| tribes: de keuze per run en de abilities | `TRIBE_CONFIG`, `RUN`, `tribeKies` | notities/tribes.md |
| muziek per level | `MUZIEK`, `MUZIEK_BASIS`, `muziek` | notities/wegwijzers.md |
| beeld: de grote of de kleine spriteset | `KLEIN_FAM`, `zetBron` | notities/wegwijzers.md |
| hppotion | de drinkkalebas |  |
| renstoot: sprinten en dan stoten | `RENSTOOT`, `glijStart`, `glijUpdate` | notities/speer.md |
| de rol: V of de rolknop, induiken en doorrollen, even onkwetsbaar en een korte afkoeling | `ROL`, `rolStart`, `rolUpdate` | notities/rol.md |
| de rol-worp: F tijdens de rol, hij gooit uit de landing; Test 60 met oefendoelen en afstellen | `ROL_WORP`, `rolWorpDruk`, `rolWorpLos`, `rolDoelen` | notities/rol.md |
| het schild van Amir: C vasthouden, vangen en de parade | `AMIR_SCHILD`, `schildVang`, `schildTeken` | notities/schild.md |
| reserve-speren op de rug (prototype) | `RUG`, `RUG_MAX`, `rugSperen` | notities/rug-speren.md |
| de oude speer: gespalkt, drie keer te gebruiken, dan breekt hij; per stand slechter | `OUDE_SPEER`, `oudSoort`, `oudBreek`, `oudSteekStap` | notities/oude-speer.md |
| zicht: een vijand ziet je alleen als er niets tussen zit | `ZICHT`, `vijandZiet`, `zichtWaak` | notities/zicht.md |
| sneak: de sluipaanval, gehoor in plaats van achterbereik en de argwaanklok (mens-vijanden) | `SNEAK`, `sneakKan`, `sneakRust`, `lawaaiPuls`, `sneakOogTeken` | notities/sneak.md |
| de sluipaanval van Amir: de animatie (steek van schuin onder, de vijand aan de punt, afschudden), een regie zoals de executie | `SNK`, `sneakRegie`, `sneakStart`, `sneakHangZet`, `hangDraai` | notities/sneak.md |
| health-balk: 3 levens met een balkje boven het hoofd | `HP_BALK`, `HP_BALK_LEVENS`, `vijandHpBalk` | notities/health-balk.md |
| bukken, jump frames, tempo | Amir zijn bewegingen |  |
| rotsen om op te springen | `rocks` | notities/wegwijzers.md |
| winter: episode Winter World | `WINTER_SRC`, `winterOn()`, `winterPic()` | notities/wegwijzers.md |
| bodem en sneeuwdek | `sneeuw` | notities/wegwijzers.md |
| grondsoort per plek: stroken straat of rots in de bodem | `GRONDSOORT`, `grondStrokenTeken`, `grondTegelVan` | notities/grondsoort.md |
| het verhaal bij een episode | `VERHAAL`, `SLOT`, `verhaalToon()` | notities/episodes.md |
| Episode De Valse Koning | `VK_1`, `VK_8`, `VK_LEVELS` | notities/episodes.md |
| Episode Test levels | `TEST_1`, `TEST_51`, `KAART_BLAD` | notities/episodes.md |
| Episode Baboon tests | `BAB_1`, `BAB_4`, `BAB_LEVELS` | notities/episodes.md |
| Episode Test levels stad | `STAD_1`, `STAD_LEVELS`, `menuStad` | notities/episodes.md |
| Episode Oaktown: zeven straten met poorten, 50 kills | `OAK_1`, `OAK_STRATEN`, `menuOak` | notities/oaktown.md |
| Episode De Belegerde Stad: zeven stadslevels, moeilijk tot extreem | `BEL_1`, `BEL_LEVELS`, `menuBel` | notities/episodes.md |
| Episode De Gouden Poort: tien stadslevels, makkelijk tot mega, met goud, winkels en Nyundo | `GP_1`, `GP_LEVELS`, `menuGP`, `gpSpeel` | notities/episodes.md |
| goud: een goudstuk per kill, de winkelprijs (5 goud) en de munt van de koning (een talentpunt extra) | `GOUD`, `goudKill`, `goudReset`, `muntE` | notities/episodes.md |
| het gif en de inventory: de speer (15) en het gif (40) in de winkel, I voor vijf plekken, een gifspeer laat een mens elke 3 s een leven verliezen | `GIF`, `gifRaak`, `gifTik`, `invUIOpen`, `INV_MAX` | notities/gif.md |
| de aanvoerder en de eindpoort: een level dat eindigt op een kill of door een poort | `AANV`, `aanvoerderDood`, `eindPoorten`, `aanvKlem` | notities/episodes.md |
| goudaapje: het kleine gouden aapje en de arena (arena, regel 12) | `GAAP`, `gaapSpawn`, `updateGoudapen` | notities/goudaapje.md |
| het mes: Jackal Fang van Impungushe | `MES`, `mesInHand`, `mesTeken` | notities/mes.md |
| de algemene boom (The Road): talents voor elke tribe, een punt na level 1, 3 en 5, de munt als vrij punt | `TRIBE_CONFIG.algemeen`, `RUN.alg`, `tbAlg`, `tbWissel`, `scherpOogTeken` | notities/tribes.md |
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
| onzichtbaar zegel: niets te zien tot je erop stapt | `ZEGEL_ONZICHTBAAR`, `zegelZie`, `onzichtbaar` | notities/zegel.md |
| speerval: een speer in de rotswand die een zegel losschiet | `SPEERVAL`, `speervalZegel`, `zegelUpdate` | notities/speerval.md |
| zakplafond: een plafond dat zakt als je op een zegel stapt | `ZAK`, `zakStand`, `rust` | notities/zakplafond.md |
| rijzende grond: steen dat op een zegel uit een ravijn komt | `RIJS`, `rijsUpdate`, `duur` | notities/rijzende-grond.md |
| takelwiel met plateau: een rad dat je met je speer slaat | `TAKEL`, `takelLaad`, `takelReset` | notities/takelwiel.md |
| de stad: een Sahelstraat met gevels, galerijen, kramen en het paleis | `STAD`, `stadPlats`, `stadAchter`, `stadTeken` | notities/stad.md |
| achter de kartels: wie op een dak in de stad staat, staat achter de tanden | `STAD_KANTEEL`, `dakAchter`, `stadKanteelVoor` | notities/stad.md |
| de stadstrap: een buitentrap achter een huis langs, E en een fade | `STAD_TRAP`, `stadTrapE`, `stadInGevecht` | notities/stad.md |
| deurgordijnen: een geweven doek in het deurgat in plaats van de houten deur, golft in de wind, binnen gespiegeld; per gevel `gordijn`, of `stad.gordijnen: true` voor een vaste keuze per huis | `GORDIJN`, `stadGordijn`, `gordijnDoek`, `stadGordijnTeken`, `binnenGordijnTeken` | notities/gordijnen.md |
| huistypes: andere gevels (reliefhuis, koopmanshuis, pilarenhuis, vervallen huis, torenhuis, twee ruines zonder dak, het winkelhuis zonder deur) met `soort`, ook in de Maker | `STAD.gevelSoort`, `stadGevelG`, `stadGeenDak`, `stadGeenDeur`, `MK_GEVEL_TYPES` | notities/stad.md |
| balkon: een ingebouwd balkon in een gevel, de nis met een dichte deur of de doorkijk in de hoek (`balkon` in een gevel) | `STAD_BALKON`, `stadBalkonMaat`, `stadBalkonTeken` | notities/stad.md |
| deuren in de stad: een vijand die uit een deurgat van een gevel stapt | `STAD_DEUR`, `stadDeurMaat`, `stadDeurUpdate`, `mkDeurMaat` | notities/stad.md |
| de doorgang: bij de opening van een trap op een galerij loopt het dek de diepte in, langs het huis | `STAD_DOORGANG`, `stadDoorgangen`, `stadDoorgangBeeld` | notities/stad.md |
| lift bij een galerij: het takelplateau voegt zich naar het eind van een galerij | `takelGalerijStap`, `mkLiftGalerij`, `galerij` | notities/stad.md |
| slagschaduwen in de stad: de galerij op de muur, een hoger huis op een lager, huizen en kramen schuin over de straat | `STAD_SLAG`, `stadSlagMuur`, `stadSlagStraat` | notities/stad.md |
| de stoep: een strook straat over de voet van de huizen, zodat niemand op de muurvoet staat | `STAD_STOEP`, `stadStoep`, `stadVoorTeken` | notities/stad.md |
| de stad bij avond en nacht: de verte per uitzicht, brandende ramen, een olielampje bij elke kraam, de gloed na de lichtlaag (`stad_middag`, `stad_avond`, `stad_nacht`) | `STAD_NACHT`, `stadVerte`, `stadNachtNa`, `stadNacht` | notities/stad.md |
| stadsvolk: dorpelingen op de stoep, omgekleurd, weg als er gevochten wordt | `STAD_VOLK`, `volkTeken`, `volkRustig` | notities/stad.md |
| de leemmuur: een terras met de look van de stad | `LEEM`, `leemMuurTeken`, `look: 'leem'` | notities/stad.md |
| de verhoogde straat: een terras met de look van de straat, treden en een hoge wijk, de onderlaag eronder (`stad.onder`) | `STRAAT_TREDE`, `straatTredeTeken`, `look: 'straat'` | notities/stad.md |
| de houten vloer: de vloer van een huis met verdiepingen, een zwever met look hout | `look: 'hout'`, `savanneLaag`, `vloer_hout` | notities/stad.md |
| binnen: de binnenkant van een huis, E bij het deurgat, een ladder, licht en stof (in de Maker: kamers van Binnen-cellen) | `BINNEN`, `binnenE`, `binnenAchter`, `binnenNa`, `mkBinnenKamers` | notities/stad.md |
| de winkel en de inrichting: een toonbank waar Amir tegenaan loopt, een schap, speren, planken met spullen; elke seed anders | `WINKEL`, `winkelOpbouw`, `winkelVoor`, `binnenLinks`; het winkelscherm (E, per klik een kalebas): `winkelUIOpen` | notities/stad.md |
| straten: losse straten met poorten ertussen, de minimap, aanvullen en een killdoel | `STRATEN`, `straatE`, `straatAanvul`, `straatHudTeken` | notities/oaktown.md |
| knooppunten: een raster van straten met een poort de diepte in en een pad naar voren (Sandville) | `straatRaster`, `straatUitgangen`, `straatKnoopGa`, `straatGevelX` | notities/stad.md |
| de luifel bij de put: een schuine doek die je meteen terugwerpt, vanaf de balk te halen | `STAD.plein.luifel`, `stadLuifelWorp`, `stadLuifelTeken` | notities/stad.md |
| poort: een stenen boog, decor of de plek waar een vijand uitkomt | `POORT`, `poortOpen`, `poortKlaar` | notities/poort.md |
| het hek van de poort: een ijzeren valhek dat omhoog getakeld wordt | `HEK`, `hekTeken`, `hekUpdate`, `poortRegie` | notities/poort.md |
| rotsen als decor: een runerots zonder rune, achter de plateaus | `rotsen`, `rotsenTeken`, `rotsenLaadLevel` | notities/decor.md |
| arena gates: de sandbox-modus met drie poorten en rondes | `SB_GATES`, `sbGates`, `sbGatesUpdate`, `gatesRand`, `gatesWeg` | notities/arena-gates.md |
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
| water: één materiaal voor plas, poel, rivier, waterval en bron (palet, rimpels, glinsters, schuim, regenringen, geruis); proefstuk Test 67 | `WATER`, `waterTeken`, `waterVoorTeken`, `waterStap` | notities/water.md |
| schilden in de wind | `SCHILD`, `schildStofUpdate`, `schildTil` | notities/decor.md |
| tonnen: houten tonnen die breken (drie treffers, Nyundo in een keer, een kalebas erin), ook op een dak of zwevende laag | `TON`, `tonRaak`, `tonBruut`, `tonPlekX`, `tonOp` | notities/tonnen.md |
| wapenrek: een houten rek in de stad met speren; E pakt er een, in de hand of op de rug | `WAPENREK`, `wapenrekken`, `rekTrek` | notities/wapenrek.md |
| rotsdecor: losse rotsstukken als props, lui geladen, in de Maker onder Decor | `ROTS_FAM`, `rotsSoorten`, `propLaad`, `mkVulRots` | notities/decor.md |
| slangen: kleur, zicht en patrouille | `SNAKE_DIRS`, `slangZiet`, `startPatrouille` | notities/slangen.md |
| zwarte panter, de witte panter (baas, regel 12), de hyena | de grote vijanden: `boss`, `arena`, `hitPanther` |  |
| de bandiet: een rover met een kromzwaard | `BAN`, `banLaad`, `makeBandiet` | notities/bandiet.md |
| de kruisboogbandiet: herlaadt (de tell), volgt Amir over twintig hoeken, blinkt en schiet; drie doden, de speer in zijn borst | `KRB`, `krbDoelHoek`, `krbSpeerVolg`, `hitKruisboog(s, soort)`; de hoorn (ontwijkt de worp, rolt, blaast twee hyena's erbij): `KRB_HOORN`, `krbWerpGezien`, `krbHoornStap` |  |
| de zweepman: sluipt laag op je af en slaat laag met een zweep (touw in code); testvijand, Test 58 | `ZWM`, `ZWM_TOUW`, `makeZweepman`, `zwmTouwStap` | notities/zweepman.md |
| de zweepman, fase 2: de arm eraf, meppen, sprong-slag en uitrusten (`fasen: true`, Test 59) | `ZWM2`, `zwmArmEraf`, `zwmF2Stap`, `zwmF2Kwetsbaar` | notities/zweepman.md |
| de schildbandiet: loopt met zijn schild op en valt springend aan | `SCHB`, `makeSchildman`, `updateSchildman` | notities/schildbandiet.md |
| schildstaat: het schild in vier standen, van heel tot weg | `SCHB_STAAT`, `schbStaat` | notities/schildbandiet.md |
| de lagen van de schildbandiet: het schild als losse laag uit lagen.json | `SCHB_LAGEN`, `schbLagenLaad`, `schbLagenLijst` | notities/schildbandiet.md |
| de dood van de schildbandiet: knielen en vallen uit executie.json (Dood hoog, Dood laag) | `schbSterf`, `SCHB.lijk`, `exeStart` | notities/schildbandiet.md |
| de executie van de schildbandiet: knielen, wankelen, vallen en de special execution | `EXE`, `exeStart`, `exeTick`, `exeVries` | notities/schildbandiet.md |
| de bandiet-arena: het geënsceneerde eindgevecht (arena, regel 12) | `BANDARENA`, `bandArenaStart`, `bandArenaWachters` | notities/bandiet.md |
| baviaan: de eindbaas in wording (baas, regel 12) | `BAVIAAN`, `baviaanLaad`, `baviaanTeken` | notities/baviaan.md |
| Brutus (Nyundo): de bruut met de knots, baas van het plein; stormt, kapt, springt (golven door de vloer), zestien treffers (baas, regel 12) | `BRU`, `makeBrutus`, `updateBrutus`, `hitBrutus`, `bruKlem`, `bruSprongStap`, `bruGolfStap`; de gebarsten vloer: `BRU_SCHADE`, `bruSchadeTeken` | notities/brutus.md |
| de opening van het plein: het hek valt dicht, Nyundo slaat de tonnen kapot en stormt | `BRU_INTRO`, `bruIntroStap`, `bruIntroVast` | notities/brutus.md |
| tonnen naar de lens: bij die slag vliegen de stukken in perspectief op de camera af, een half deksel knalt tegen de lens | `TON.lens`, `tonLensMaak`, `tonLensTeken` | notities/tonnen.md |
| speerbeet: de baviaan pakt je speer | `BAV_BEET`, `BAV_MOND`, `BAV_SPEER` | notities/baviaan.md |
| speer in de baviaan: de speerval blijft in zijn borst zitten | `BAV_VALSPEER`, `bavSpeerTeken`, `baviaanTeken` | notities/baviaan.md |
| voorgrond: de laag tussen de camera en Amir | `VOORGROND`, `VG_SOORT`, `VG_LAGEN` | notities/voorgrond.md |
| de stadsvoorgrond: kruiken, manden en een leemmuurtje voor de camera, per stuk straat naar wat er staat (De Gouden Poort) | `VG_STAD`, `vgStad`, `vgStadThema`, `voorgrond: 'stad'` | notities/voorgrond.md |
| achtergrondlagen, uitzicht per level | `SCENE0`, `SCENES` | notities/wegwijzers.md |
| startscherm, menu: kaartjes per level | menu |  |
| kaarslicht: de startfoto van onderen belicht | `KAARS`, `kaarsStart`, `kaarsLus` | notities/kaarslicht.md |
| Level Maker nieuwstijl: het grid, de Test, de controle | `MK`, `mkNaarLevel`, `mkControle`, `MK_VIJ_KNOP` | notities/maker.md |
| elk level nakijken op decor boven een ravijn | `schoonLevel`, `schoonKomend`, `komendeRavijnen` | notities/ravijn.md |
| wat er staat waar een ravijn openscheurt | `RAVIJN_DECOR`, `ravijnDecor`, `ravijnDecorStap` | notities/ravijn.md |
| golvende rand: terreinmassa's met een organische omtrek | `GOLF`, `golfAan`, `golfGrondTeken`, `golfTerrasTeken` | notities/golf.md |
| de kit van Amir verbeteren: takenlijst met cijfers per onderdeel; bij "verbeter Amir kit" de lijst tonen, de opdrachtgever kiest, afstrepen | `kit-lijst`, `G1`, `L1`, `M2` | notities/kit-verbeteren.md |
| de stad verbeteren: werklijst met cijfers en stappen; bij "stadsverbetering" eerst 3 suggesties, de opdrachtgever kiest | `stadsverbetering`, `S1`, `L1`, `V1` | notities/stad-verbeteren.md |
| ideeën voor de kit van Amir: basis, tribe-ability of talent; stof in de ogen (gebukt F vasthouden, de veeg met eigen animatie en geluid) | `STOF`, `STOFA`, `stofStap`, `stofWerp`, `stofDwaal` | notities/kit-ideeen.md |
| sandbox | de vrije testmodus |  |

Op schijf: `karakters/` (Amir, dorpeling, dorpelinge), `enemies/`, `design/` (decor,
achtergronden, water, dorp, botten), `klein/` (dezelfde mappen op halve grootte),
`music/` en `sounds/`, `tools/` (de Python-scripts), `icons/`, `sw.js` en
`offline-assets.json` (de webapp).

## Een level lezen of schrijven

Amir loopt naar links, dus alle `x` zijn negatief en lopen op naarmate je verder
komt. Een leveldefinitie is een gewoon object; de Maker nieuwstijl exporteert (Spel-JSON)
precies hetzelfde formaat naar JSON.

De velden met een langere uitleg staan in `notities/velden.md`; hieronder kort.

| veld | wat |
| --- | --- |
| `name` | naam op het kaartje in het menu |
| `lagen` | sleutel uit `SCENES`: welk uitzicht dit level krijgt |
| `muziek` | sleutel uit `MUZIEK`: welk deuntje eronder loopt (`bg` voor het oude thema); zonder dit veld `MUZIEK_BASIS`, Dark Africa, en in een level met `stad` de stadmuziek Market Shadows (`MUZIEK_STAD`, `music/marketshadows.mp3`); `stad` geeft het eerdere Tense Grounding, `stadgeluid` geeft de oude stadgeluiden zonder muziek, `stil` geeft geen muziek (Stad 6) |
| `winter` | `true` zet het hele level in de sneeuw (witte dieren, sneeuwversies van het decor) |
| `sneeuw` | sneeuw op de grond, los van `winter`: `{soort, dek, van, tot}` (zie hieronder) |
| `grondSoort` | stroken grondsoort in de bodem: `[{van, tot, soort}]`, `soort` savanne, rots of straat; per strook een andere grondtegel, met een grillige rand die over een halve cel zacht uitloopt in de grond ernaast, ook op een savannelaag, zwever en gangvloer. De Maker schrijft het uit de grondlijn-cellen; geen bestaand level heeft het (zie `notities/grondsoort.md`) |
| `weer` | het weer onderweg: `[{x, soort, sterkte}]`, `soort` uit `WEER.soorten` (`droog`, `regen`, `onweer`, `zandstorm`, `sneeuw`, `sneeuwstorm`); voorbij `x` slaat het om (zie "het weer") |
| `valschade` | `true` laat een diepe val levens kosten (standaard uit): vanaf een Amir diep een leven, vanaf twee Amir twee (`VAL_VRIJ`, `VAL_ZWAAR`, `VAL_MAX`), en vanaf zes Amir diep is hij dodelijk (`VAL_DOOD`, `fallDeath` in `valLand`), ongeacht je levens. `levelcheck.py` (regel `vallen`) meldt een val van zes Amir of dieper als FOUT |
| `rugMax` | reserve-speren op de rug: 1 in de hand plus zoveel op de rug (0 tot 5; zonder dit veld 1, `RUG_STANDAARD`, overal behalve een level met `geenSpeer`; `rugMax: 0` zet hem uit) (zie `notities/velden.md`) |
| `zicht` | `true`: een vijand merkt Amir pas op als hij hem echt kan zien. Voor hem een halve cirkel met een zichtlijn die grond en rots tegenhouden, achter hem de oude afstand maar alleen op zijn eigen niveau, en na 3 s zonder zicht vergeet hij je. Zonder veld de oude manier (alle bestaande levels); een nieuw level krijgt `zicht: true`, een spawn met `zicht: false` houdt toch de oude manier (zie `notities/zicht.md`) |
| `sneak` | `true` (naast `zicht`): de sluipaanval. Een mens-vijand (bandiet, schildbandiet, kooiman, meelman, kruisboogbandiet, zweepman) hoort je achter zijn rug in plaats van je te zien (kruipen en stilstaan stil, lopen tot net buiten steekafstand, sprinten van ver, een worp, treffer, klap of neerkomende speer geeft een puls), krijgt argwaan als je vlak achter hem staat en kijkt dan om, en een treffer van achteren op wie je niet opmerkte is in een klap dood (bij de schildbandiet langs het schild). Spawnvlaggen `rug`, `draai`, `pat`. Een nieuw level krijgt `sneak: true`; alleen Test 61 heeft het (zie `notities/sneak.md`) |
| `hpBalk` | `true` of een lijst soorten: 3 levens met een health-balkje boven het hoofd, ook voor Amir; de schildbandiet krijgt een schildbalk erboven. Zonder veld uit, een nieuw level krijgt `hpBalk: true` (zie `notities/velden.md`) |
| `slangEenKlap` | `true`: elke slang (zand, zwart, knock en fosfor) is in een klap dood, ook met `hpBalk` aan. Een nieuw level krijgt `slangEenKlap: true`; Oaktown (makkelijk) heeft het (`SLANG_EEN_KLAP`, in `hpBalkAan`) |
| `golf` | `true` of `{ruw}`: de golvende rand. De kruin van de grond, een rotsterras, het dak en de vloer van een gang en het zwarte terrein krijgen een golvende omtrek met textuur, druipstenen, keien en hangblokken (zie `notities/golf.md`); `ruw` schaalt de golven, 1 is de maat uit `GOLF`. Zonder veld uit; alleen Test 49 heeft het |
| `hoogUitzicht` | `true`: gestapelde dikke grondlagen zien er op hoogte hetzelfde uit als de basis (zie `notities/velden.md`) |
| `view` | een getal van 0,5 tot 1: uitgezoomd spelen; een nieuw level krijgt standaard `view: 0.8` (zie `notities/velden.md`) |
| `zichtBreed` | een doel-wereldbreedte in beeld in plaats van een vaste `view`; geen level gebruikt het nog (zie `notities/velden.md`) |
| `camera` | `true` of `{voor, verken, vecht, telefoon}`: de meekijkende camera. Vooruitkijken in de looprichting, en op een laptop 0,75 onderweg en 0,8 in een gevecht; een telefoon houdt 0,8 en kijkt minder ver vooruit. Gaat boven `view`; in een arena neemt de arena-camera het over en geldt `view`. De standaard voor een nieuw level (Test 51 tot en met 55 en de Maker); in de sandbox de knop Meekijken (`CAM`, `camUpdate`) |
| `worp` | `'schaal'` zet de schaalworp aan: de hoek loopt op zolang je vasthoudt, van vlak tot 30 graden (`THR_HOEK_MAX`); zonder dit veld de twee trappen. In de sandbox de knop Worp onder Speerworp |
| `stof` | `true`: stof in de ogen, gebukt F vasthouden veegt stof naar een bandiet die Amir aankijkt; even blind, de volgende treffer telt dubbel (alleen Test 63, zie `notities/kit-ideeen.md`) |
| `schild` | `true`: Amir heeft een schild, C (of de schildknop) houdt het op; het vangt alles van voren en net op tijd is het een parade (alleen Test 56, zie `notities/schild.md`) |
| `rand` | `true`: het level begint aan de rand. Geen rotswand en hut aan de start, de rechtergrens ligt `RAND.ruimte` (320) achter de start (een getal in plaats van `true` is die ruimte zelf) en de camera kijkt niet voorbij die grens (`randCam`, in `camUpdate`). De standaard voor elk nieuw level (Stad 1); de bestaande levels hebben het niet |
| `speerInHand` | `true`: Amir begint met de speer in de hand in plaats van hem voor zich uit de grond te pakken; de Level Maker nieuwstijl zet dit in elk level, de echte episodes hebben het niet |
| `executie` | `true`: elke dodelijke steek, worp of lage zwaai op een schildbandiet is de executie, in plaats van 1 op 5 en 1 op 3 (alleen Test 50, zie `notities/schildbandiet.md`) |
| `herhaal` | `true`: is de laatste schildbandiet weg (na de executie of de gewone dood), dan komt er na `EXE.herhaalWacht` een nieuwe aanwandelen, net buiten beeld voor Amir uit, met de vlaggen van de eerste schildman-spawn (alleen Test 50, `exeHerhaalStap`) |
| `wateren` | het water van `WATER`: `[{k, x, w}]`, `k` is `plas`, `poel`, `rivier`, `val` (van de rechterkant van een terras op `x`) of `bron` (met `hoog` in Amir); een poel en rivier laten je waden zoals de oude `water` (zie `notities/water.md`). Alleen Test 67 |
| `vredig` | `true`: geen vijanden, en ook geen vrije slangen of kalebassen die het spel anders bij lege `spawns` stuurt (Test 67) |
| `rocks` | keien om op te springen: `{x, s}` |
| `tonnen` | houten tonnen die breken: `{x, y, f, kalebas}`, of `put`/`luifel`/`kraam` met `a` (Amir van die put, losse luifel of kraam) in plaats van `x`; hoger op met `dak` (een dak of galerij van de stad, met `a` vanaf het midden van dat dak) of `zwever: true` (zie `notities/tonnen.md`) |
| `wapenrekken` | houten rekken met speren: `{x, f, n}`, `n` speren (standaard en hooguit 4, een per touwlus), of `put`/`luifel`/`kraam` met `a` zoals bij `tonnen`; E pakt er een (zie `notities/wapenrek.md`) |
| `spawns` | vijanden: `{x, k}`, `k` is groen/zwart/knock/scorp/hyenas/panter/fosfor/bandiet/kooiman/meelman/schildman/kruisboogbandiet, met vlaggen per soort (zie `notities/velden.md`) |
| `goud` | `true`: een goudstuk per kill, een kalebas kost 5 goud in de winkel, goud en kalebassen gaan mee naar het volgende level (De Gouden Poort, zie "goud" in `notities/episodes.md`) |
| `munt` | de munt van de koning: `{x, y, vast}`; E pakt hem, en na het level is er een talentpunt extra (een keer per run) |
| `bandArena` | `true`: het level is een bandiet-arena (Valse Koning 8), zoals de goudaap-arena maar met de elite-garde (zie "de bandiet-arena") |
| `duoArena` | `{c, golven, pauze, eerste, niveau}`: een arena op de open savanne rond `c` (vaste camera, geen wanden); per golf tegelijk een kruisboogbandiet en een schildbandiet, elk willekeurig van links of rechts. De schutter schiet pas helemaal in beeld (`inBeeld`, `krbInBeeld`) en zijn bouten raken de schildman (`vriendVuur`, `krbPijlVriend`). Na `golven` golven is het level uit (Test 55 en 56, `duoTick`). Met `keuze: true` kies je voor het begin de lading van de schutter (`KRB_SALVO`, standaard 2 bouten en daarna 1) en het niveau van de schildman, in plaats van `niveau` (`duoKeuze`, alleen Test 56) |
| `bandietGolf` | een oplopende golf bandieten: `{van, tot, ramp, max, dolk}` (zie `notities/velden.md`) |
| `duel` | per kooiman-spawn `{x, k: 'kooiman', duel}`; standaard aan is het 1-op-1 duel, `duel: false` de gewone kooiman (zie `notities/velden.md`) |
| `props` | decor: `{x, k, s, f, v}`, `k` uit `PROPS`, `f` spiegelen, `v` verre laag |
| `village` | dorpsplaten uit `VILLAGE`: `{id, x, depth, flip}` |
| `gaps` | ravijnen: `{x, w}` |
| `water` | poelen: `{x, n}` met `n` = aantal middenstukken |
| `thickets` | doornbossen: `{x, n, seed}` |
| `terraces` | terrassen om op te klimmen: `{r, l, h}`; negatieve `h` is een trede in een gang, `grond: true` een hogere savannelaag, `look: 'leem'` een muur van leem in de stad (zie "de leemmuur" in `notities/stad.md`), `look: 'straat'` een verhoogd stuk straat, trede of hoge wijk (zie "de verhoogde straat" in `notities/stad.md`) (zie `notities/velden.md`) |
| `holtes` | gangen onder de grond: `{r, l, diep}`, een ravijn erboven is de ingang, een gat met treden de uitgang (zie hieronder) |
| `putten` | ravijnen in de vloer van een gang: `{x, w}`, helemaal binnen een holte (zie "put") |
| `zuilen` | zuilen met een hoogte in een ravijn of put: `{x, w, h}`, `h` van -250 tot 180 boven de grond of de vloer (zie "zuil met een hoogte") |
| `ledges` | richels aan een wand: `{x, h, s}`; met `f` gespiegeld (vlakke kant rechts, punt naar links, botsing naar links van `x`), met `achter: true` achter de schacht-wand getekend (zie "De schacht"), met `look` de kleur (`rots` standaard, `sneeuw`, `savanne`; in de Maker de keuze Kleur bij een richel) |
| `zwevers` | zwevende savannelagen: `{r, l, h, onder, look}`, een dik savanneblok in de lucht met lucht eronder; `h` de looplijn bovenop, `onder` de onderkant (de ruimte eronder; onder `CHAR_H` kruip je er gebukt onderdoor), `look: 'rots'` tekent het als een rotsoverhang (zie "zwevende savannelaag"), `look: 'hout'` als de houten vloer van een huis (zie "de houten vloer" in `notities/stad.md`) |
| `grotten` | rotsgebieden als raster: `{x, cel, y, grid, ...}` (zie hieronder); met `schacht: true` is de wand de plafondvulling met de tanden erlangs in plaats van de terrasplaat (zie "De schacht") |
| `start` | waar Amir begint (wereld-x); zonder dit veld op 0. Voor een schacht waar hij tussen de wanden start in plaats van ernaartoe te lopen |
| `plafond` | de rots boven je als hoogtelijn: `[{x, y}, ...]` (zie hieronder) |
| `muur` | de rotswand met het rune-symbool: `{x, speer}`, of met `soort: 'grot'` de rotsboog met de kei (zie hieronder) |
| `hppotions` | drinkkalebassen: `{x, y}` |
| `oudeSperen` | losse oude speren op de grond: `{x, n, f}`, `n` hoe vaak nog (standaard 3); het level begint met een lege rug (alleen Test 65, zie `notities/oude-speer.md`) |
| `skeletten` | een zittend skelet met een speer erin: `{x, f}`, `x` is het midden van het skelet, `f` spiegelt; E bij de schacht trekt hem eruit (zie hieronder) |
| `tekens` | speertekens: `{x, v, f}`, `v` is `teken`, `gebroken`, `gekruist`, `jagers` of `kalebas`, `f` spiegelt; decor, behalve dat het mes de kalebas lossnijdt |
| `fakkels` | geanimeerde wandfakkels: `{x, y, s, f}`, `x` de schacht, `y` de hoogte van de voet boven de grond in Amir (0 = op de grond, hoger = tegen een wand), `s` schaal, `f` spiegelen; brandend decor met gloed, vonken, schaduw en vuurgeluid (zie "fakkel") |
| `talentKeuze` | `true`: voor het begin kies je zelf welke talents gelden, van alle tribes (alleen voor een Test level; nu Test 14) |
| `zweepKeuze` | `true`: voor het begin kies je de oude, de nieuwe, de nieuwere zweepman of nieuwer schreeuw (`ZWM_NIEUW`, `ZWM_NIEUWER`, in het scherm van `duoKeuze`); alleen Test 58 en 59 (zie `notities/zweepman.md`) |
| `zegels` | zegels plat in de grond: `{x, ravijn, sluit, breed, muur, speerval, teken, vijand, plafond, rijs, poort, speer, verstop, onzichtbaar, veeg, dak}`; met `onzichtbaar` is er niets van te zien tot iemand erop stapt (dan gaat hij aan en verschijnt hij), met `dak` ligt hij boven een gang op de savanne in plaats van op de gang-bodem, met `verstop` ligt hij onder het zand tot de lage zwaai hem blootveegt, `veeg` kiest de onthulling (standaard de wolk, traag en middel), `veegDuur` en `veegMaat` het tempo en de grootte, `vloer` de kleur van het zand (zie `notities/velden.md`) |
| `poorten` | stenen bogen uit `design/boog/`: `{id, x, k, f, y, s, look, hek, wand, wandF, wandH, wandX, regie, bij}`, `look` steen, sneeuw of savanne (zonder: sneeuw in een winterlevel), decor; een zegel of rune met `poort: id` opent hem en dan komen de spawns met `poort: id` eruit (zie "poort"); `hek` een valhek dat optakelt, `wand` een rotswand erachter (`true` de kale wand, of een soort uit `HEK_WANDEN`: `kaal`, `spits`, `pieken`, `zuilen`, `boog`, `grot`), `wandH` zijn hoogte en `wandX` een verschuiving, allebei in Amir, `regie` vanzelf open als hij in beeld komt (of bij `bij`) met Amir vast tot de vijand eruit is (zie "het hek van de poort") |
| `rotsen` | losse rotsen als decor: `{x, soort, groot, y}`, een van de platen onder een rune (`spits`, `pieken`, `zuilen`, `boog`) zonder schijf, `x` de linkervoet, `groot` de hoogte in Amir, `y` een vaste vloer; getekend achter de plateaus, zodat een zwever erin kan snijden (zie `notities/decor.md`) |
| `rijzers` | steen dat uit een ravijn omhoog komt: `{id, r, l, tot, van, v, wacht, duur}`, `id` de naam waar een zegel of een rune (`doel: true`) met `rijs` naar wijst, `tot` en `van` de bovenkant boven en beneden (standaard -1 en -900), `wacht` seconden voor hij begint, `duur` seconden boven voor hij terugzakt (zie "rijzende grond"); met `zak: true` staat hij boven en zakt hij onder Amir weg; `look` de bovenrand (`savanne`, `rots`, `sneeuw`, `zwart`) en `kleurVanaf` een hoogte waaronder het blok zwart blijft; in een put (`putten`) is de gangvloer zijn grond (Test 48) |
| `stad` | de Sahelstad: `{paleis, seed, gevels, galerijen, kramen, voet, trappen, volk}`; `volk: [{x, k, kleur, f}]` dorpelingen op de stoep die verdwijnen als er gevochten wordt (zie "stadsvolk" in `notities/stad.md`); `luifels: [{x, kant}]` de luifel van de put zonder put (zie "de luifel bij de put" in `notities/stad.md`), `trappen: [{gevel, kant, niveau, balkon}]` een houten buitentrap achter een huis langs (E, zie "de stadstrap" in `notities/stad.md`), gevels van 1 tot 4 hoog met een beloopbaar dak, houten galerijen, kramen (`riet` draagt, `doek` veert) en de straattegel in plaats van de grondrand; met `lagen: 'stad_dag'` (Stad 1, zie `notities/stad.md`). Een galerij en een dak zijn ook de vloer van een vijand (`stadVloerBij` in `vloerBij`): een spawn met `dak: 401` (de hoogte) of `dak: true` staat erop en de rand houdt hem tegen; de camera klimt mee |
| `binnen` | de binnenkant van huizen: `[{gevel, r, l, deur, ramen, palen, ladders, bogen, winkel, planken}]`, elk een eigen strook ver van de straat; E voor het deurgat van gevel `gevel` en je staat binnen bij de deur `deur` (recht, net als buiten), E daar en je staat weer buiten; `bogen: [{x, naar}]` is de binnenpoort, de ronde boogdeur naar een volgende kamer (een kamer met `gevel: null` heeft geen deur naar buiten); een ladder werkt als de stadstrap. Een spawn met `vloer: 450` staat op die verdieping. Stad 7, en de Maker nieuwstijl bouwt het uit Binnen-cellen (zie "binnen" in `notities/stad.md` en `notities/maker.md`) `winkel: {x, seed}` zet links een winkel (toonbank, schap, marktman, E opent het winkelscherm), `planken: [{x, h, soort, seed}]` planken met spullen aan de muur; de seed bepaalt hoe het eruitziet, dus geef een nieuw level een nieuwe (zie "de winkel" in `notities/stad.md`) |
| `straten` | een stadje van losse straten: `{start, doel, aanvul, knopen, lijst: [{id, naam, r, l, knoop}]}`; elke straat een eigen strook (van `r` naar `l`), met `raster: true` en `muur` heeft elke straat knooppunten (twee of meer, met `m` voor een middelste) met een poort de diepte in en een pad naar voren, dood op een leemmuur aan elk eind (zie "knooppunten" in `notities/stad.md`); rechtsonder een minimap op een laptop, een straat vult zich aan na `aanvul` seconden weg, en bij `doel` kills is het level uit (geen `ends` nodig, `doel: 0` is geen einde). Sandville en Oaktown (zie `notities/oaktown.md`). Een nieuw level met straten krijgt altijd `raster: true`, en alleen rechte straten: elke straat is een rij of een kolom op de kaart, nooit schuin. De hoekpoort (zonder raster) gaat eruit; geen level gebruikt hem nog |
| `takel` | een takelwiel met een hangend plateau; sla het rad met je speer, het plateau draagt en veert (zie `notities/velden.md`) |
| `maskers` | geverfde stukken die een deel van het level verbergen: `{id, look, vakken}` (zie `notities/velden.md`) |
| `zakplafond` | stukken rots die zakken: `{r, l, rust, dicht, v, schok, duw}` (zie `notities/velden.md`) |
| `speervallen` | speren in de rotswand: `{x, h}`, `x` de klif waar hij in zit (uit `cliffs`), `h` de hoogte in Amir (standaard 0,82); een zegel met `speerval` schiet hem los (zie "speerval") |
| `runes` | ravijnen met een rune op een rots ervoor: `{x, breed, rots, groot, hoog, doel}` (zie `notities/velden.md`) |
| `fg` | strook waarover de voorgrondbegroeiing ligt: `{from, to}` |
| `voorgrond` | de onscherpe laag vlak voor de camera: `{stroken: [{van, tot, dicht, struik, kei}], los: [{x, k, s, f}]}`, `k` uit `VG_SOORT`; los van `fg`. Zonder dit veld krijgt het level de standaard, met `false` heeft het er geen, met `'stad'` de stadsvoorgrond (De Gouden Poort, zie `notities/voorgrond.md`) |
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
   vijand en Amir krijgt in een nieuw level een health-balk (zie "health-balk"). Zet er ook
   `slangEenKlap: true` bij: slangen blijven in een nieuw level altijd in een klap dood. En `zicht: true`:
   een vijand ziet je dan alleen als er niets tussen zit (zie "zicht"). En `sneak: true`: de
   sluipaanval, een mens-vijand hoort je achter zijn rug in plaats van je te zien (zie "sneak"). En `camera: true`: de
   meekijkende camera (zie het veld `camera`); een arena-level mag het ook hebben, daar neemt de
   arena-camera het over. De Maker nieuwstijl doet dit al zelf. En `rand: true`: geen rotswand
   en hut aan de start, Amir begint aan de rand van het level en de camera kijkt er niet voorbij
   (zie het veld `rand`). Dat geldt voor elk nieuw level vanaf nu; de bestaande levels houden hun
   rotswand (rule 1, en een speerval zit in die wand). De Maker had al een kale start (`kaleKlif`).
2. De naam in de array van die reeks (`VK_LEVELS`, `TEST_LEVELS`, `BAB_LEVELS`, `STAD_LEVELS`, `OAK_LEVELS`, `BEL_LEVELS` of `GP_LEVELS`).
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
`markCards` en `showMenu` (die kiezen nu tussen `cardsVK`/`menuVK`, `cardsBab`/`menuBab`,
`cardsStad`/`menuStad`, `cardsOak`/`menuOak` en `cardsTest`/`menuTest`, en `toMenu` ook), en de reeks in `tools/speelrobot.js`,
`tools/runecheck.js` en `tools/beeldgelijk.js`. De Terug-knop van een episodescherm krijgt de klasse `menuepisodes` (terug naar
Episodes), niet `menuback` (dat gaat naar het Levels-scherm). Een nieuwe episode begint altijd met de tribekeuze: `runStart` in zijn speelknop, en `tribeLijst` geeft
hem alleen wat de speler verdiend heeft (alleen `TEST_LEVELS` krijgt alles). Wil de episode een
verhaal, zet dan de tekst in `VERHAAL` en `SLOT` en `verhaalAan` in zijn speelknop. De Valse Koning is het
voorbeeld van een episode met verhaal en Nightmare.

### Een vijand of prop toevoegen

Tekencode en gedrag erbij, opnemen in `PROPS`, `VILLAGE` of de dierenlijst, en
knoppen in de sandbox. Kies de soort (vast, los, plant of ver, zie "wat mag waar") en zet hem in
de vijf functies die daarbij horen. Pas daarna is de vraag aan de orde of er een level bij moet.
Laadt de soort niet in elk level, laad hem dan lui: een idempotente `xxxLaad`, een `xxxLaadLevel(lv)`
die in het level kijkt, een regel in `laadLevel` (die `setLevel` en de Test van de Maker allebei
aanroepen) en een aanroep in `startSandbox` als hij daar een knop krijgt. Nooit bovenaan het bestand
laden, zodat het menu er niet op wacht (zie `notities/laadpoort.md`, "lui laden per level").

## De Maker nieuwstijl

De enige bouwer in het spel (de oude bouwer, Level maken, is weg): een grid waarin je per cel schildert wat er is,
dat de Test meteen als level speelt (`mkNaarLevel`). Hij staat helemaal los van de levels. Hoe hij in elkaar zit, wat de controle meldt en welke knoppen een vijand heeft:
zie `notities/maker.md`. Na een wijziging aan de Maker draai je `tools/makertest.js`.

**Het palet en het paneel blijven kort.** Elk gereedschap in `MK_TYPES` en elke vijand in `MK_VIJANDEN` zegt met `groep`
waar hij in het palet staat (een pad zoals `objecten/takel`; de namen staan in `MK_CATS` en `MK_GROEPEN`), en de boom
bouwt zichzelf daaruit (`mkPaletBoom`). Geen enkele categorie, groep of flyout heeft meer dan `MK_PALET_MAX` (6) items,
en het paneel rechts niet meer dan zoveel rijen buiten een inklapbaar kopje (`details.mkklap`, zoals bij de poort en de
rijzer). Een nieuw item zonder `groep` landt vanzelf in Overig, en `tools/makertest.js` (de controle `maat`) geeft FOUT op
Overig, op een groep zonder naam, op een te volle groep en op een te lang paneel. Voeg je iets toe, dan deel je het dus in,
en loopt een groep of paneel daarmee over de maat, dan splits je die in dezelfde pull request (een nieuwe groep in
`MK_GROEPEN`, of een kopje in het paneel) en zeg je achteraf hoe je het ingedeeld hebt.

## Sandbox

De vrije testmodus: vlakke grond, een leeg level, geen vijanden en geen levens. Een knop
erbij is een `<button>` in `<div id="sandbox">` plus de afhandeling in de sandbox-sectie,
in het juiste tabblad (`.sbcat`). Zie `notities/sandbox.md`.

## Assets

Welk script draai je na welke wijziging (de volledige uitleg staat in `notities/assets.md`):

- **Sprites toegevoegd, vervangen of weggehaald** → `python3 tools/gen-klein.py` en daarna
  `python3 tools/gen-offline-manifest.py` (in die volgorde). Het eerste print de lijst voor
  `KLEIN_FAM`, het tweede werkt de offline-download bij, inclusief de arena-set (`ARENA_MAPPEN` en
  `ARENA_SOORTEN`, de knop **Alleen de Arena modus**: de basis plus de vijanden die in de arena aan staan).
  Een nieuwe soort in `SB_ARENA_SOORTEN` krijgt een regel in `ARENA_SOORTEN` (en, laadt hij niet in zijn
  make-functie, een in `SB_ARENA_LAAD`); raakt de wijziging de arena, draai dan ook `node tools/arena-assets.js`.
- **Bodem of sneeuwdek** (`grondrand_rots.png`, `sneeuwlaag_25..100.png`) → `tools/sneeuwdek.py`
- **Run van de baviaan** → `tools/baviaan_run_fix.py`
- **`design/grot/rots_vulling.png`** → `tools/rots_vulling.py`
- **Speerteken** → `tools/speerteken.py`
- **Slangen** (zand, roet, knock) → `tools/slang_kleur.py`
- **Elite-garde** → `tools/bandiet_elite_kleur.js`, daarna `gen-klein.py` en `gen-offline-manifest.py`
- **Kooi-plaat van de kooiman** → `tools/kooi_kleur.py`, daarna `gen-klein.py` en `gen-offline-manifest.py`
- **Schildbandiet** → `tools/schildman_kleur.py`, daarna `gen-klein.py` en `gen-offline-manifest.py`. Het bandietpalet is zijn standaard: elke nieuwe export (lijf, schild, executie) zet je in de speelmap en haal je meteen door dit script, ook als er niemand om de kleuren vraagt. Het zet frames in de oude kleuren eerst in `enemies/schildbandiet/bron/` (de oude kleuren blijven bewaard), kleurt ze om en meldt FOUT als er nog een in de oude kleuren staat
- **Goudaapje** → `tools/goudaapje_kleur.js`
- **Zweepman** → `tools/zweepman_kleur.py`, daarna `gen-klein.py` en `gen-offline-manifest.py`. Net als bij de schildbandiet is het bandietpalet zijn standaard: een nieuwe export zet je in `enemies/zweepman/lagen/` en haal je door dit script; de oude kleuren gaan naar `bron/`
- **Kruisboogbandiet** → `tools/kruisboog_kleur.py`, daarna `gen-offline-manifest.py`. De export uit de Animeer tool (felle kleuren, schouderstuk erop) staat in `enemies/kruisboog/bron/`; het script schrijft de speelversie in het bandietpalet naar `enemies/kruisboog/<set>/`
- **Stenen bogen** (`design/boog/`, uit de platen in `bron/`, met hun sneeuw- en savanneversie en het masker van de opening, `_gat.png`) → `tools/boog_vulling.py` (alleen de maskers: `--gat`), daarna `gen-offline-manifest.py`
- **Schade in de pleinvloer van Nyundo** (`design/stad/plein_schade_*.png`, `plein_brokken.png`, uit de Grok-platen in `design/stad/bron/`) → `tools/plein_schade.py`, daarna `gen-offline-manifest.py`; nieuwe brokken geven nieuwe rechthoeken voor `BRU_SCHADE.brokken`
- **Nyundo** (`enemies/brutus/frames/`, ook na `tools/brutus_donker.py`) → `tools/brutus_spleet.py` (de spleet tussen steel en bal van de knots) en `tools/brutus_rand.py` (de stippelrand om de donkere set), daarna `gen-klein.py` en `gen-offline-manifest.py`
- **Het bloed onder Nyundo als hij in zijn knots valt** (`design/bloed/nyundo_stroom.png`, uit het lijk van de schildman) → `tools/nyundo_bloed.py`, daarna `gen-offline-manifest.py`
- **Wapenrek** (`design/stad/wapenrek/`, uit de Grok-plaat in `bron/`) → `tools/wapenrek_knip.py`, daarna `gen-offline-manifest.py`
- **Deurgordijnen** (`design/stad/gordijn/`, uit de Grok-platen in `bron/`) → `tools/gordijn_knip.py`, daarna `gen-klein.py` en `gen-offline-manifest.py` (de gordijnmap staat niet in de lijst van `gen-klein.py`, dus het spel laadt de grote versie, net als bij de tonnen)
- **Tonnen** (`design/stad/ton/`, uit de Grok-platen in `bron/`) → `tools/ton_kleur.py`, daarna `gen-offline-manifest.py`
- **Rotsdecor** (`design/rotsdecor/`, losse rotsstukken uit de platen in `bron/`) → `tools/rotsdecor_knip.py`, daarna `gen-offline-manifest.py`
- **Stadsvoorgrond** (`design/stad/voorgrond/`, geknipt uit `design/stad/voetdecor.png`) → `tools/stad_voorgrond.py`, daarna `gen-offline-manifest.py`
- **Oude speer** (`design/speer/oud/`, uit de gewone speer) → `tools/oude_speer.py`, daarna `gen-offline-manifest.py`
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
python3 tools/levelcheck.py level.json een level uit de Maker (Spel-JSON), voor het in de HTML staat
```

FOUT betekent: stuk, of tegen een regel uit dit document in. LET OP betekent: het werkt, maar
krap, of het spel lost het stilletjes op. Een nieuw level gaat pas de deur uit zonder FOUT.

### De speelrobot: `tools/speelrobot.js`

Laadt het echte spel in Chromium en loopt een level naar links uit op vaste 60 fps; meldt waar
hij landt, wat een val kost, waar hij vastloopt, wat er in de console staat, en overtredingen
van regel 7 (`REGEL 7`). Heeft Node en Playwright nodig (`npm i -g playwright`).

```
node tools/speelrobot.js "Test 4"               een level uit de HTML, op naam
node tools/speelrobot.js level.json --taai      een level uit de Maker; --taai: levens komen terug
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

### De poorttest: `tools/poorttest.js`

Speelt Maker-grids met poorten in Chromium door (elke vijandsoort, elke hoogte, hek, regie, twee poorten, dood en
herstart) en meldt per scenario OK of FOUT. Draai hem na een wijziging aan de poort, het hek, de regie, de spawner
of `mkNaarLevel`. `--alleen gang` beperkt tot de scenario's met dat woord in de naam.

### De arena-download nameten: `tools/arena-assets.js`

Speelt de Arena modus in Chromium met alle soorten aan en meldt FOUT op elk bestand dat het spel
opvraagt en niet in de arena-set van `offline-assets.json` staat (de basis `delen.arena` plus de `soorten`
die aan staan), voor de grote en de kleine spriteset. Draai hem na een wijziging aan `ARENA_MAPPEN` of
`ARENA_SOORTEN` in `gen-offline-manifest.py`, aan de arena-modus of aan wat de sandbox bij het openen laadt.
`--soorten schildman` meet met alleen die soorten aan, `--beeld klein` beperkt tot een set, `--duur 90`
speelt langer, `--toon` toont alles wat er opgevraagd is.

### De makertest: `tools/makertest.js`

Laadt de Maker nieuwstijl in Chromium met een proefgrid waar alles op staat en kijkt de round-trip,
de vertaling naar een spel-level, rijen invoegen, schilderen, ongedaan maken, de controle, de Test
en de autosave na, en haalt het proefgrid als spel-level door `levelcheck.py`. Draai hem na elke
wijziging aan de Maker.

```
node tools/makertest.js                alle controles
node tools/makertest.js --alleen rij   alleen de controles waarvan de naam dit bevat
node tools/makertest.js --shots map    daarna een schermafdruk van de Maker en van de Test
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
