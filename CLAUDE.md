# Werkafspraken voor dit project

Amir: King of Africa is een browserspel in één bestand. `amir-king-of-africa.html`
bevat de opmaak, de stijl en alle code; de sprites, achtergronden en geluiden staan
los op schijf. Geen buildstap, geen testsuite, geen afhankelijkheden.

Lees dit document voordat je iets aanraakt. `README.md` is de uitleg voor de speler
en beschrijft wat het spel kan; dit document beschrijft hoe je eraan werkt.

## Regels

**1. Levels van een echte episode blijven met rust.** Nu is er geen bevroren episode meer: De Valse Koning,
Oaktown, De Belegerde Stad, De Gouden Poort, De Rivierstad en The Roofs of Kumbasa zijn op verzoek weggehaald, en
The Clay City (`KLEI_1` tot en met `KLEI_7`) staat tussenin (geen proefstuk, wel aanpassen als de opdracht erom vraagt). Wijst de opdrachtgever
weer een episode als bevroren aan, dan geldt het volgende daarvoor. De Episode Test levels (`TEST_1` en verder) de episode Baboon tests (`BAB_1` en verder), de episode Murghtaan (`MUR_1` en verder), de Elite tests (`REI_1` en verder) en de episode Test levels stad (`STAD_1` en verder) vallen niet onder deze regel: ze zijn er
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

**5. Nederlands achter de schermen, Engels in het spel, en geen em-dashes.** Code, commentaar,
notities, commits en pull requests zijn Nederlands. Wat de speler leest is Engels: een nieuwe tekst
in het spel (een melding, een scherm, een knop, het levelrapport, "Double Kill") schrijf je in het
Engels, zoals de talents al heten. De menu's en teksten die nu nog Nederlands zijn blijven staan tot
de opdrachtgever vraagt ze te vertalen. Gebruik komma's of haakjes, nooit een lang gedachtestreepje.

**6. Werk op een `claude/*`-branch.** Push daarheen en maak alleen een pull request
als daarom gevraagd wordt.

**7. Vijanden komen niet over keien en ravijnen.** Slangen, fosforslangen en ook
de panters worden tegengehouden door een kei om op te springen en
door de rand van een ravijn: niet lopend, niet met een sprong of een duik, en ze duiken
ook niet aan de overkant op. Zo is een kei of een ravijn voor de speler een schuilplek.
Een schuilplek, geen veilige plek: een slang of schorpioen naast de kei mag Amir bovenop die
kei nog bijten of steken, want hun beet reikt tot de hoogte van een kei. Dat is zo bedoeld.
Uitzondering op verzoek van de opdrachtgever: een bandiet die gestund is door de counter van de stokken en dan een slag
krijgt aan de rand van een ravijn, slaat erin en is dood (`STOK_RAND`, `banRandVal`, zie `notities/stokken.md`); aan de rand
van een galerij of dak slaat hij eraf naar de straat met de val van Full Circle (`FC_VAL`), alleen als hij veilig neerkomt.
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
Uitzondering op verzoek van de opdrachtgever: de chaser (`chaser: true`, de Asloper uit `enemies/bandiet_as/`) springt
van een galerij, dak of terras naar beneden als Amir lager staat (`BAN_GJ`, `banGjStap`, zie "de chaser" in
`notities/bandiet.md`); omhoog komt ook hij niet. Uitzondering op verzoek van de opdrachtgever: de terugslag van Full Circle slaat een bandiet of schildbandiet van een galerij of dak naar de straat, alleen als hij daar veilig neerkomt (`FC_VAL`, `fcValLanding`, zie `notities/combo.md`). Uitzondering op verzoek van de opdrachtgever: staat Amir op een springdoek, een rieten kraamdak of de doek van
een kraam (die tellen niet als vloer), dan slaan de bandiet, de schildbandiet en de zweepman toch als hun slag er
in de animatie bij kan, genoeg van Amir binnen het bereik van hun wapen (`amirOpDoek`, `slagBij`, `banKanBij`,
`schbKanBij`, `zwmKanBij`, `BAN_BIJ_MIN`). Alleen de slag zelf; dolkworp, vault en hinderlaag niet.
De uitzondering is een opstapje: een terras met `opstap: true` (tot `OPSTAP.max`, 32) lopen Amir en de lopende vijanden op en af,
op verzoek van de opdrachtgever; slangen en schorpioenen niet (zie "opstapjes" in `notities/stad.md`).

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
  kooiman, kruisboogbandiet, zweepman en goudaapje. Die mag je in de sandbox en in een testlevel (regel 1 en 3) gewoon neerzetten.
- **Bazen**: de panter (zwart, en wit in een winterlevel: dezelfde spawn `k: 'panter'`, altijd met `boss: true`
  en de arena-camera, drie treffers), de baviaan (`BAVIAAN`, de eindbaas in wording) en Brutus (in beeld Nyundo,
  `BRU`, de baas van Stad 6: Het plein, zestien treffers, zie `notities/brutus.md`) en Murghtaan (`MUR`, de bezeten
  hyena, door de opdrachtgever ook **de hyenabaas** genoemd, de baas van de episode Murghtaan, zie `notities/episodes.md`). Een baas zet jij
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

**15. Online spelen is voorlopig voor laptops.** Multiplayer (Co-op en Duel) hoeft alleen op laptops te werken, ook op
verschillende netwerken; een telefoon op mobiele data hoeft niet. Stap 3 van de netcode (een eigen TURN-server) staat
daarom in de wacht: bouw hem niet en stel hem niet voor, tot de opdrachtgever er zelf om vraagt. Wat er al is (STUN,
de gratis openbare TURN-servers en het relais) blijft staan: het relais is ook het vangnet voor een laptop op een
streng netwerk. Zie "Voor wie" in `notities/multiplayer.md`.

**16. Kansen gaan met een knikkerzak.** Een kans in het spel (een crit, een leven terug, wat er uit een ton komt) trek
je niet met `Math.random() < kans`, maar uit een knikkerzak (de marble bag): zoveel knikkers waarvan zoveel raak, zonder
terugleggen, en een lege zak gaat geschud weer vol. Zo is 1 op 10 echt 1 op 10, zonder lange reeksen pech of geluk.
Voorbeelden: `critZak` (True Flight), `mpcKnikker` (de tonnen van Co-op), `ardhiKnikker` (de Ardhi-wapens). Een verse zak
per level. Oudere kansen die nog met `Math.random()` gaan (Gris-gris, Gold King) laat je staan tot de opdrachtgever
erom vraagt; een nieuwe kans gaat altijd met een zak.

**17. De telefoon ligt stil.** Op verzoek van de opdrachtgever (28-11-2026) doen we voorlopig niets met de telefoon: bouw
er niets voor, stel er niets voor voor, test er niet op en zet het niet als open punt in een notitie. Wat er al is
(knoppen, de camera voor de telefoon, schermformaten) blijft staan en hoef je niet bij te werken; breekt een nieuwe
wijziging iets op de telefoon, dan is dat geen reden om het te laten. Pas als de opdrachtgever er zelf weer over begint,
komt de telefoon terug.

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
| prestatiemeter: F9 toont fps, beeldtijd, eigen JS-tijd, vijanden, bakbeurten en het dieptepunt per level | `METER`, `meterStap`, `meterVijanden`, `buitenDoek` |  |
| foutmelding: een fout een keer melden, ook als hij elk beeld terugkomt | `meldFout`, `tekenHerstel`, `ctxDiepte`, `laadMist` |  |
| versie: welke update er live staat | `versieTijd`, `document.lastModified`, `toonUpdates` | notities/wegwijzers.md |
| niet verder tekenen dan er in beeld komt | `zichtVak(marge)`, `view`, `null` | notities/tekenlagen.md |
| de verte als platen: de lucht met de zon en per bergrij een strook met land en nevel erin, in plaats van ruim tien vullingen per beeld | `VERTE`, `VERTE_PLAAT`, `vertePlaten`, `verteBak`, `verteTeken` | notities/tekenlagen.md |
| de zon: schijf, krans en ademende ring | `ZON`, `drawZon`, `ringAdem` | notities/zon.md |
| wolken in de lucht: Grok-wolken in drie lagen diepte, per uitzicht ingekleurd, standaard in de savanne (`wolken: false` zet ze uit), in de stad alleen met `stad.lucht` (Ishmul) | `STAD_LUCHT`, `luchtWolken`, `luchtWolkenAan`, `luchtWolkKleur` | notities/wegwijzers.md |
| globale lichtlaag | `licht`, `SCENES` | notities/wegwijzers.md |
| de schaduw van Amir | `AMIR_SCHADUW`, `amirSilhouet`, `amirSilLeg` | notities/schaduw-amir.md |
| licht op personages: zon, fakkel en raam leggen een rand van licht op Amir en de vijanden | `PLICHT`, `persLicht`, `plichtBronnen` | notities/licht-personages.md |
| tribes: de keuze per run en de abilities | `TRIBE_CONFIG`, `RUN`, `tribeKies` | notities/tribes.md |
| muziek per level | `MUZIEK`, `MUZIEK_BASIS`, `muziek` | notities/wegwijzers.md |
| beeld: de grote of de kleine spriteset | `KLEIN_FAM`, `zetBron` | notities/wegwijzers.md |
| hppotion | de drinkkalebas |  |
| renstoot: sprinten en dan stoten | `RENSTOOT`, `glijStart`, `glijUpdate` | notities/speer.md |
| de ren van Amir: de nieuwe ren is de standaard, de oude zit er nog in (`nieuweRen: false`), met de open punten om op terug te komen | `REN_NIEUW`, `renNieuwZet`, `renSprintZet` | notities/ren.md |
| de rol: V of de rolknop, induiken en doorrollen, even onkwetsbaar en een korte afkoeling | `ROL`, `rolStart`, `rolUpdate` | notities/rol.md |
| de rol-worp: F tijdens de rol, hij gooit uit de landing; Test 60 met oefendoelen en afstellen | `ROL_WORP`, `rolWorpDruk`, `rolWorpLos`, `rolDoelen` | notities/rol.md |
| het schild van Amir: C vasthouden, vangen en de parade | `AMIR_SCHILD`, `schildVang`, `schildTeken` | notities/schild.md |
| reserve-speren op de rug (prototype) | `RUG`, `RUG_MAX`, `rugSperen` | notities/rug-speren.md |
| de speervolgorde: welke speersoort eerst in je hand zit (de inventory, Hold first), vanzelf de beste na oprapen en na een worp, Z wisselt | `speerVolgorde`, `speerSorteer`, `speerWissel`, `speerVoorop`, `rugSort`, `invSperenToon`, `pfAantal` | notities/speer-inventory.md |
| de oude speer: gespalkt, drie keer te gebruiken, dan breekt hij; per stand slechter | `OUDE_SPEER`, `oudSoort`, `oudBreek`, `oudSteekStap` | notities/oude-speer.md |
| de Pathfinder Spear: de speer uit de winkel van Co-op met het rode vaantje dat meewaait (op de rug, in de worp, liggend), en de prooi: een geworpen treffer markeert 3 s (rode rand, vaantje boven het hoofd, 20% trager, een half leven extra per treffer) | `PATHFINDER`, `PROOI`, `javTeken`, `pfVaanTeken`, `pfStap`, `prooiRaak`, `prooiGloed` | notities/speer.md |
| de Ardhi-wapens: Ardhi's Grip (stokken), Ardhi's Reach (speer) en Ardhi's Roots uit de winkel van Co-op; een treffer kan een leven teruggeven (knikkerzak: stok 1 op 33, steek 1 op 25, worp 1 op 10, een sapdruppel boven je hoofd), Roots zet wortels om twee vijanden in een groep (alleen op aarde), Bloom verdubbelt de kans van de speer (2 op 25, 2 op 10, met de aderen op de speer); sandboxknoppen Ardhi en Ardhi's Bloom, `tools/ardhi_test.js` | `ARDHI`, `ardhiBloom`, `ardhiAderTeken`, `ardhiStap`, `ardhiTreffer`, `ardhiKnikker`, `ardhiWortelRaak`, `ardhiAarde`, `ardhiVast` | notities/speer.md |
| de Shield Piercer: de speer uit de winkel van Co-op met de zwarte naald en de ijzeren knol, door het schild heen (schildbandiet in een klap dood) uit een knikkerzak: verre worp 2 op 3, korte 1 op 3, steek en lage zwaai 1 op 8; de kansen van de speersoorten (ook de steek en zwaai van de Pathfinder), en het speervak links van de actiebalk (Z, de naam bij een wissel) | `SPEER_KANS`, `speerKansTrek`, `piercerDoor`, `spStap`, `pfMarkeert`, `SPVAK`, `spvakHud` | notities/speer.md, notities/speer-inventory.md |
| neer: de val van Amir (grijpt naar zijn zij, zakt door zijn knieen, glijdt neer op zijn zij), twee eigen sets: Mkuki met de speer en de stokken-Amir; in Co-op neer tot de revive (ook bij teamgenoten), in single player sterven en dan het doodscherm; omkleuren met `tools/neer_zones.py` en `tools/vacht_bak.js`; sandboxknoppen Fall: Mkuki en Fall: sticks; `tools/mptest.js --neer --stokken host --spelers 2` | `NEER`, `amirSterf`, `neerStap`, `neerBeeld`, `neerSetVan`, `neerIs`, `neerMk`, `neerSandbox` | notities/neer.md |
| Silver Pride: het zilveren leeuwenhart uit de winkel van Co-op (alleen de stokken, met een teamgenoot, 35/50/65 goud, een tegelijk): G legt het neer, het pulseert, de dode teamgenoot komt eruit (klein naar groot) terwijl Tau in de lucht brult, dan 3 s onkwetsbaar zonder abilities; Test 91 met een oefenteamgenoot; `tools/mptest.js --zilverhart --stokken host`, `tools/zilverhart_test.js` | `ZH`, `zhGebruik`, `zhStart`, `zhStap`, `zhTeken`, `zhTauNa`, `zhOpstaan`, `zhOntwaakT`, `zhCarry`, `TEST_93` | notities/multiplayer.md |
| Feathers of the Bennu: de veren-revive van de speerspeler (Mkuki): G, op een knie, de veren gloeien, ogen open met een flits, blazen, een luchtbol met veren in de wind, de vlaag van het spel neemt ze mee naar de teamgenoot verderop; in de winkel van Co-op (tab Team, met de speer), over het netwerk (`bn`), de bol houdt vijanden en projectielen buiten; Test 94 met een oefenteamgenoot, K wisselt de kleur; dood met het hart of de veren in de tas brengen ze je zelf terug; `tools/mptest.js --bennu --spelers 2` | `BN`, `bnGebruik`, `bnStap`, `bnSchild`, `bnVan`, `bnZelfStart`, `reviveZelfStap`, `mpcReviveKomt`, `TEST_94` | notities/multiplayer.md |
| vijanden uit elkaar houden: een groep van een soort glijdt uit elkaar, wie in zijn aanval zit blijft staan (bandiet, kooiman, schildbandiet, hyena, zandslang) | `scheidMobs`, `mobScheidAan`, `schbScheidHouding`, `SB_GROEP_N` | notities/scheiden.md |
| zicht: een vijand ziet je alleen als er niets tussen zit | `ZICHT`, `vijandZiet`, `zichtWaak` | notities/zicht.md |
| sneak: de sluipaanval, gehoor in plaats van achterbereik en de argwaanklok (mens-vijanden) | `SNEAK`, `sneakKan`, `sneakRust`, `lawaaiPuls`, `sneakOogTeken` | notities/sneak.md |
| de sluipaanval van Amir: de animatie (steek van schuin onder, de vijand aan de punt, afschudden), een regie zoals de executie | `SNK`, `sneakRegie`, `sneakStart`, `sneakHangZet`, `hangDraai` | notities/sneak.md |
| het aanvalsticket: alleen wie een ticket heeft valt aan (een voor, een achter, een voor afstand), de rest wacht en schuifelt; bandiet en schildbandiet, Test 96 en de sandboxknop Attack tickets | `TICKET`, `ticketMag`, `ticketStap`, `ticketSchuifel`, `banTicketWacht` | notities/ticket.md |
| health-balk: 3 levens met een balkje boven het hoofd | `HP_BALK`, `HP_BALK_LEVENS`, `vijandHpBalk` | notities/health-balk.md |
| bukken, jump frames, tempo | Amir zijn bewegingen |  |
| rotsen om op te springen | `rocks` | notities/wegwijzers.md |
| winter: episode Winter World | `WINTER_SRC`, `winterOn()`, `winterPic()` | notities/wegwijzers.md |
| bodem en sneeuwdek | `sneeuw` | notities/wegwijzers.md |
| grondsoort per plek: stroken straat of rots in de bodem | `GRONDSOORT`, `grondStrokenTeken`, `grondTegelVan` | notities/grondsoort.md |
| het verhaal bij een episode | `VERHAAL`, `SLOT`, `verhaalToon()` | notities/episodes.md |
| Episode The Clay City: zeven stadslevels als solo Co-op episode (reeks `c`): geen tribe en geen talents, de kit, het goud en de winkel van Co-op (in level 2, 4, 6 en 7); bij Play kies je wapen en moeilijkheid (Young Whelp, Lion, Hunter XL), spawns, kalebassen en tonnen met `van`/`tot` | `KLEI`, `KLEI_1`, `KLEI_LEVELS`, `kleiZwaar`, `kleiSpeel`, `kleiCoopStart`, `kleiCoopStop`, `pvp.klei`, `MPC_EPS`, `menuKlei`, `dkzwaar` | notities/episodes.md |
| Episode Test levels | `TEST_1`, `TEST_51`, `KAART_BLAD` | notities/episodes.md |
| Episode Baboon tests | `BAB_1`, `BAB_4`, `BAB_LEVELS` | notities/episodes.md |
| Elite tests: het Test Lab-scherm met een map per elite-vijand of baas (Reinier, Baboon tests, Murghtaan), `menuElite`, Back-knop klasse `menuelite` | `menuElite`, `menuRei`, `REI_LEVELS`, `REI_1` | notities/reinier.md |
| Reinier (codenaam), de bijlveteraan: elite-vijand (geen baas, regel 12), uitvalskap, schijnkap, draaizwaai, strafvenster, wankel, dood; sprites uit de Grok-proef | `REI`, `REI_DATA`, `reinieren`, `makeReinier`, `updateReinier`, `hitReinier`, `reiTeken`, `reiOpen` | notities/reinier.md |
| Episode Murghtaan: de hyena-baas (baas, regel 12), de roedel, de reveal en de kevers | `MUR_1`, `MUR`, `makeMurg`, `updateMurg`, `hitMurg`, `murKevers`, `murKlem` | notities/episodes.md |
| Murghtaan 2: de charge van het nieuwe ontwerp (brul, aanzet, galop, slip met stof, draai; vijf treffers) | `MUR_2`, `MURC`, `murcStap`, `murcRaak`, `murcTeken`, `murcZeg` | notities/episodes.md |
| de pin van Murghtaan 2: schouderblik in de slip (tell), sprong, alleen de rol ontwijkt; happen in het ritme 1, 1, 2, steken op de hap pareert; startkeuze levens/onaantastbaar en extra hyena's; afstellen onder Instellingen | `MURC.pin`, `murcPinStap`, `murcPinHap`, `murcPinAmir`, `MURC_PIN_SCHUIF`, `murcKeuze` | notities/episodes.md |
| Murghtaan 3: de opening (vreten aan een lijk, omkijken met freeze en naam, whoop, roedel van drie achter een muur, dan de charge) | `MUR_3`, `MURC_INTRO`, `murcIntroStap`, `murcVries`, `murcRoedelKomt` | notities/episodes.md |
| Episode Test levels stad | `STAD_1`, `STAD_LEVELS`, `menuStad` | notities/episodes.md |
| de schatkist: E en het goud spat eruit, vaak op een moeilijke plek; kopgeld voor een aanvoerder en Nyundo; de makkelijke schildbandiet in een bruin kleed | `KIST`, `kistE`, `drawKisten`, `goudKopgeld`, `SCHB_TINT` | notities/episodes.md |
| goud: een goudstuk per kill, de winkelprijs (5 goud) en de munt van de koning (een talentpunt extra) | `GOUD`, `goudKill`, `goudReset`, `muntE` | notities/episodes.md |
| multikill: kills binnen 3 s na elkaar zijn een reeks, een kraal per kill, Double, Triple of Multi Kill, een stinger en 1 goud extra; het levelrapport na het level; in elk level aan | `MKILL`, `mkillKill`, `mkillStap`, `mkillRapport`, `mkStat` | notities/multikill.md |
| het gif en de inventory: de speer (15) en het gif (40) in de winkel, I voor vijf plekken, een gifspeer laat een mens elke 3 s een leven verliezen | `GIF`, `gifRaak`, `gifTik`, `invUIOpen`, `INV_MAX` | notities/gif.md |
| de aanvoerder en de eindpoort: een level dat eindigt op een kill of door een poort | `AANV`, `aanvoerderDood`, `eindPoorten`, `aanvKlem` | notities/episodes.md |
| de razernij van de aanvoerder: een meter die oploopt, dan razend (ontwijken, niet aanvallen), dan uitgeput; met `schaduw` onzichtbaar met een stofspoor (De Rivierstad) | `RAZ`, `razStap`, `razSchaduw`, `razMeterTeken` | notities/bandiet.md |
| goudaapje: het kleine gouden aapje en de arena (arena, regel 12) | `GAAP`, `gaapSpawn`, `updateGoudapen` | notities/goudaapje.md |
| het mes: Jackal Fang van Impungushe | `MES`, `mesInHand`, `mesTeken` | notities/mes.md |
| de algemene boom (Perks, eerst The Road): talents voor elke tribe, rechts naast de tribe-boom, een punt na level 1, 3 en 5, de munt als vrij punt | `TRIBE_CONFIG.algemeen`, `RUN.alg`, `tbAlg`, `tbEigen`, `scherpOogTeken` | notities/tribes.md |
| talent tree: twee bomen naast elkaar (tribe links, Perks rechts, het venster ertussen), van boven naar beneden, takken met `eis` en `kant` | `tbEis`, `tbRij`, `tbTakBouw`, `tbLijnen`, `TB_KRAAL` | notities/tribes.md |
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
| de hangende stam: een boomstam aan twee lianen in het regenwoud, slingert, een liaan doorslaan laat hem schuin en dan plat vallen (Test 82); schuin is hij een helling om over te lopen (Test 83) | `HSTAM`, `hstamKnap`, `hstamUpdate`, `hstamPlats`, `hstamHelling`, `hstamTeken` | notities/wegwijzers.md |
| de loopput: een lage put om op te staan en overheen te springen, houdt vijanden tegen als een kei; savanne (verweerde veldsteen, takken, kalebas) of `soort: 'stad'` (leem, houten deksel) (Test 97) | `LOOPPUT`, `loopputDak`, `loopputTeken`, `sbLoopput` | notities/stijlproef.md |
| rotsen met richels: een kopje, tafelrots of gespleten rots als achtergrond met beloopbare richels erop, zo diep als de galerij, elke lengte, schaduw op de rots; de savanne-tegenhanger van de galerij (Test 97, sandbox Rotsen met richels) | `KOPJE`, `kopjeDaken`, `kopjesTeken`, `kopjeRichelBeeld`, `kopjeRotsBeeld`, `sbKopje` | notities/stijlproef.md |
| de holle stam: een omgevallen holle boom in het regenwoud, loop erdoor (de voorkant vervaagt), vecht erin, loop erop, kruip door een kleine; lengte in drie stukken (`n`), grootte `s`; met `vlieg` vuurvliegjes die van een steek, zwaai of kill schrikken en door de openingen wegvliegen (Test 93) | `HOLSTAM`, `holstamBak`, `holstamDak`, `holstamAchter`, `holstamVoor`, `holstamSchrik`, `holstamSlag`, `holstamGatE`, `holstamLens` | notities/wegwijzers.md |
| de schachtboom: een reuzenboom in het regenwoud met tussen zijn wortels een gat naar een gang (geen E, geen valschade, stof bij de landing), een deksel van wortels dat dichtbij vervaagt, links een onzichtbare muur; alleen boven de grond (Test 95) | `SCHACHTBOOM`, `schachtTeken`, `schachtGat`, `schachtMuur`, `schachtLand` | notities/wegwijzers.md |
| een klap in de mist: de stam, een harde landing en de grondklap duwen de grondmist weg, een gat dat dichtloopt en een rand die opbolt en wegrolt | `MIST_STOOT`, `mistStoot`, `mistDekking`, `mistStootStap` | notities/wegwijzers.md |
| stof in het regenwoud: donkere humus in plaats van zand | `RW_STOF`, `regenwoudStof`, `puffPic`, `stofWolk` | notities/wegwijzers.md |
| de stad: een Sahelstraat met gevels, galerijen, kramen en het paleis | `STAD`, `stadPlats`, `stadAchter`, `stadTeken` | notities/stad.md |
| achter de kartels: wie op een dak in de stad staat, staat achter de tanden | `STAD_KANTEEL`, `dakAchter`, `stadKanteelVoor` | notities/stad.md |
| de stadstrap: een buitentrap achter een huis langs, E en een fade | `STAD_TRAP`, `stadTrapE`, `stadInGevecht` | notities/stad.md |
| deurgordijnen: een geweven doek in het deurgat in plaats van de houten deur, waait mee met de vlagen en de storm van het spel, 's nachts een lamp erachter, binnen gespiegeld; per gevel `gordijn`, of `stad.gordijnen: true` voor een vaste keuze per huis | `GORDIJN`, `stadGordijn`, `gordijnWind`, `gordijnLamp`, `gordijnDoek`, `stadGordijnTeken`, `binnenGordijnTeken` | notities/gordijnen.md |
| huizen tegen elkaar: een gevel met `aan` sluit op elk scherm aan op het huis rechts ervan, strak of met een steeg | `aan`, `stadAanVan`, `stadGevelX` | notities/stad.md |
| huistypes: andere gevels (reliefhuis, koopmanshuis, pilarenhuis, vervallen huis, torenhuis, twee ruines zonder dak, het winkelhuis zonder deur) met `soort`, ook in de Maker | `STAD.gevelSoort`, `stadGevelG`, `stadGeenDak`, `stadGeenDeur`, `MK_GEVEL_TYPES` | notities/stad.md |
| balkon: een ingebouwd balkon in een gevel, de nis met een dichte deur of de doorkijk in de hoek (`balkon` in een gevel) | `STAD_BALKON`, `stadBalkonMaat`, `stadBalkonTeken` | notities/stad.md |
| accenten: de takel met een mand in de wind, andere ramen op het oude huis, en `stad.accenten` die per seed zelf kiest | `STAD_TAKEL`, `STAD_RAMEN`, `stadAccenten`, `stadTakelTeken` | notities/stad.md |
| deuren in de stad: een vijand die uit een deurgat van een gevel stapt | `STAD_DEUR`, `stadDeurMaat`, `stadDeurUpdate`, `mkDeurMaat` | notities/stad.md |
| de doorgang: bij de opening van een trap op een galerij loopt het dek de diepte in, langs het huis | `STAD_DOORGANG`, `stadDoorgangen`, `stadDoorgangBeeld` | notities/stad.md |
| lift bij een galerij: het takelplateau voegt zich naar het eind van een galerij | `takelGalerijStap`, `mkLiftGalerij`, `galerij` | notities/stad.md |
| slagschaduwen in de stad: de galerij op de muur, een hoger huis op een lager, huizen en kramen schuin over de straat | `STAD_SLAG`, `stadSlagMuur`, `stadSlagStraat` | notities/stad.md |
| de stoep: een strook straat over de voet van de huizen, zodat niemand op de muurvoet staat | `STAD_STOEP`, `stadStoep`, `stadVoorTeken` | notities/stad.md |
| de verte van de stad: groepjes daken, palmen en de moskee in plaats van de verste rij minigevels, rook uit de daken en gieren die cirkelen | `STAD_VERTE`, `stadVerteRij`, `stadVerteRook`, `stadVerteGieren` | notities/stad.md |
| de stad bij avond en nacht: de verte per uitzicht, brandende ramen, een olielampje bij elke kraam, de gloed na de lichtlaag (`stad_ochtend`, `stad_middag`, `stad_avond`, `stad_nacht`) | `STAD_NACHT`, `stadVerte`, `stadNachtNa`, `stadNacht` | notities/stad.md |
| stadsvolk: dorpelingen op de stoep, omgekleurd, weg als er gevochten wordt | `STAD_VOLK`, `volkTeken`, `volkRustig` | notities/stad.md |
| de leemmuur: een terras met de look van de stad | `LEEM`, `leemMuurTeken`, `look: 'leem'` | notities/stad.md |
| de verhoogde straat: een terras met de look van de straat, treden en een hoge wijk, de onderlaag eronder (`stad.onder`) | `STRAAT_TREDE`, `straatTredeTeken`, `look: 'straat'` | notities/stad.md |
| opstapjes: lage treden (`opstap: true`, tot 32) die Amir en de lopende vijanden oplopen in plaats van opspringen; slangen en schorpioenen niet (Test 78) | `OPSTAP`, `opstapBij`, `opstapVolg` | notities/stad.md |
| savanne-opstapjes: een opstapje met `grond: true` tekent als een lage trede van savanne, met een naadloze wand en een afgebrokkeld eind (Test 80) | `SAV_OPSTAP`, `savOpTeken`, `savOpLaad` | notities/stad.md |
| de tint van een level: de stad een keer omgekleurd, bijvoorbeeld wit zand (`tint: 'wit'`, Ishmul) | `TINT`, `tintStap`, `tintBak` | notities/stad.md |
| de houten vloer: de vloer van een huis met verdiepingen, een zwever met look hout | `look: 'hout'`, `savanneLaag`, `vloer_hout` | notities/stad.md |
| binnen: de binnenkant van een huis, E bij het deurgat, een ladder, licht en stof (in de Maker: kamers van Binnen-cellen); met `verdieping` de deur boven, vanaf een galerij, en met `deuren` meer deuren naar buiten (beneden erin, boven eruit) | `BINNEN`, `binnenE`, `binnenAchter`, `binnenNa`, `mkBinnenKamers` | notities/stad.md |
| de winkel en de inrichting: een toonbank waar Amir tegenaan loopt, een schap, speren, planken met spullen; elke seed anders | `WINKEL`, `winkelOpbouw`, `winkelVoor`, `binnenLinks`; het winkelscherm (E, per klik een kalebas): `winkelUIOpen` | notities/stad.md |
| Duka, de marktman: lopen, idle, gapen, kalebas, schap, met zijn rug naar achteren; gesnapt achter de toonbank (wereld bevriest, lach, klap, magisch wolkje, Amir valt aan de voorkant) | `DUKA`, `winkelManStap`, `dukaBetrap`, `dukaRegie`, `dukaWolk`, `tools/duka_knip.py`, `tools/duka_test.js` | notities/stad.md |
| Kivuli, de reizende handelaar: bij een op de drie winkelbezoeken van Co-op Survival (knikkerzak) in plaats van Duka, drie versies (staat bij de toonbank, komt binnen en leunt, muntje), E opent zijn jas en de binnenkant van zijn mantel met zijn voorraad, 45 s vanaf het eerste praten (of eerder weg als het hele team Done drukt), dan weg en komt Duka soms wel en soms niet; lobby Kivuli comes, Kivuli in the shop en Duka after Kivuli; `tools/kivuli_knip.py`, `tools/kivuli_test.js` | `KIV`, `kiv`, `KIV_ZEG`, `kivBesluit`, `kivStart`, `kivStap`, `kivPraat`, `kivVertrek`, `kivWegUit`, `kivDukaStap`, `kivKlokToon`, `kivTeken`, `kivSfeer`, `kivDonkerNa`, `kivLampTeken`, `kivMuzStap`, de mantel: `kivMantel`, `kivSlots`, `kivMantelToon`, `kivKlaarDruk` | notities/multiplayer.md |
| de spullen van Kivuli en de itemslots: vijf dingen alleen bij Kivuli (Sack o' Bones, Sack o' Fangs, Jar o' Fire Ants, Oil of Mirrors, Ketemba Clay), een per speler per bezoek, in de tas, met I in slot R of T, R en T gebruiken ze (herstarten is Shift+O, overal, ook dood en in het Duel; het oefendoel Y); sandboxrij Kivuli items, `tools/islot_test.js` | `ISLOT`, `islotTas`, `islotZet`, `islotToets`, `islotStart`, `islotStap`, `islotRaak`, `islotMirOm`, `islotDubbelNu` | notities/multiplayer.md |
| straten: losse straten met poorten ertussen, de minimap, aanvullen en een killdoel | `STRATEN`, `straatE`, `straatAanvul`, `straatHudTeken` | notities/oaktown.md |
| knooppunten: een raster van straten met een poort de diepte in en een pad naar voren (Sandville) | `straatRaster`, `straatUitgangen`, `straatKnoopGa`, `straatGevelX` | notities/stad.md |
| de springdoek: de luifel aan de muur van een huis, indigo, doorgezakt, met een eigen hoogte en worp (Stad 9) | `STAD_SPRINGDOEK`, `stadLuifelBeeld`, `sbSpringdoek` | notities/stad.md |
| de einddeur: E voor een open deur hoog in een huis speelt het level uit (Stad 9) | `eindDeur`, `eindDeurUit`, `eindDeurTeken` | notities/stad.md |
| het kelderluik: een schuine kelderingang tegen een muur, het luik vliegt open met de deurslag en E speelt het level uit (Stad 14) | `KELDER`, `kelderUpdate`, `kelderUit`, `kelderTeken` | notities/stad.md |
| de kelderzaal: een kelder als level, met een houten trap (je loopt achter de wang), een plafond met balkkoppen, traliedeuren waar een bandiet doorbreekt en een dierenkooi die opengaat (Test 86) | `KZAAL`, `kzaalReset`, `kzaalLichtNa`, `kgat` | notities/kelder.md |
| de luifel bij de put: een schuine doek die je meteen terugwerpt, vanaf de balk te halen | `STAD.plein.luifel`, `stadLuifelWorp`, `stadLuifelTeken` | notities/stad.md |
| de strakke luifel: een indigo doek in een houten raam aan de muur, je staat in de stof en de doek zakt in onder je voeten; met `ritme` een trampoline waar je hoogte opbouwt door op tijd te springen (Stad 10) | `luifelStrak`, `stadKuil`, `stadLuifelVoor`, `stadRitme`, `stijl: 'strak'` | notities/stad.md |
| poort: een stenen boog, decor of de plek waar een vijand uitkomt | `POORT`, `poortOpen`, `poortKlaar` | notities/poort.md |
| het hek van de poort: een ijzeren valhek dat omhoog getakeld wordt | `HEK`, `hekTeken`, `hekUpdate`, `poortRegie` | notities/poort.md |
| rotsen als decor: een runerots zonder rune, achter de plateaus | `rotsen`, `rotsenTeken`, `rotsenLaadLevel` | notities/decor.md |
| arena gates: de sandbox-modus met drie poorten en rondes | `SB_GATES`, `sbGates`, `sbGatesUpdate`, `gatesRand`, `gatesWeg` | notities/arena-gates.md |
| Co-op solo: Co-op Survival (of de Co-op episode) voor een speler onder Single Player, Survival (knop City Survival), de lobby en de Co-op zonder verbinding | `MP_SOLO`, `mpSoloOpen`, `pvp.solo`, `btnsbcoop` | notities/multiplayer.md |
| masker: geverfde stukken die een deel van het level verbergen | `MASKER`, `maskerLijst`, `maskerVan` | notities/masker.md |
| de draaiende speer: rollen om de lengteas in de vlucht | `DRAAI`, `draaiImgs`, `draaiBeeld(soort, t)` | notities/speer.md |
| skelet met speer | `SKELET`, `skeletTrek`, `skeletUpdate` | notities/skelet.md |
| speerteken: een speer in de grond met een zwart doek en schedels | `TEKEN`, `tekenUpdate`, `tekenTeken` | notities/decor.md |
| licht op de runerotsen | `RUNE_LICHT`, `runeLichtMaak`, `runeGrondSchaduw` | notities/wegwijzers.md |
| runeschijf: het losse symbool | `runeSchijf(ctx, x, y, r, {aan, spiegel})` | notities/wegwijzers.md |
| vallen: schade bij een diepe val | hoe diep een val telt en wat hij kost |  |
| schorpioen, het projectiel, spannen en werpen, de geworpen speer | `javTegenDak`, `javFloor`, `vloerBij` | notities/speer.md |
| omlaag mikken: van een hogere laag naar beneden gooien, pijl omlaag tijdens het spannen (Test 71) | `THR_OMLAAG`, `worpOmlaag`, `thrOmlaag` | notities/speer.md |
| de mik-rig: vrij mikken met losse delen (arm, hoofd en speer draaien mee), pijl op en neer tijdens het spannen; proefveld Test 72 | `RIG`, `rigMik`, `rigBeeld`, `rigMikStap`, `speerOneindig`, `geenEinde` | notities/speer.md |
| fakkel: een geanimeerde wandfakkel | `FAKKEL`, `fakkelLaad`, `fakkelFrame` | notities/fakkel.md |
| donker met gaten: de diepe nacht (`stad_diepnacht`) waar alleen de fakkels en de ramen licht geven | `donkerGatenNa`, `fakkelLichten`, `gaten` | notities/fakkel.md |
| personages, dorpsdecor | `VILLAGE` | notities/wegwijzers.md |
| Amir zegt er iets van als hij geraakt wordt | `SFX_RAAK`, `playRaak()` | notities/geluid.md |
| Amir zegt iets als een vijand sterft | `SFX_RUST`, `vijandDood(baas)`, `DOOD_KANS` | notities/geluid.md |
| stap voor stap leren spelen | `tutorial` | notities/wegwijzers.md |
| de tutorial The First Hunt: een mentor (de gids, de Mkuki-ranger met eigen animaties over het opgenomen spoor; zonder gids.json de omgekleurde Amir) die voordoet en wacht, een tekstwolk met toetsen, een fade terug na een val en een race; een eigen knop onder Single Player met "Start here" tot hij uitgespeeld is | `TUT_1`, `TUT_LEVELS`, `btnTutorial`, `tutKnopToon`, `MENTOR`, `mentorUpdate`, `mentorTeken`, `mentorWolkTeken`, `mentorVal`, `mentorOpname`, `GIDS`, `gidsTeken`, `gidsFx` | notities/tutorial.md |
| gaten in de grond | `gaps`, `grondDoorlopen` | notities/wegwijzers.md |
| zuil: een smalle strook grond tussen twee ravijnen | `ZUIL`, `zuilBij`, `zuilWand` | notities/zuil.md |
| zuil met een hoogte: hoger of lager dan de grond | `ZUIL_HOOG`, `zuilLijst`, `zuilBasis` | notities/zuil.md |
| put: een ravijn in de bodem van een gang | `PUT`, `putLijst`, `putBij` | notities/put.md |
| stof, sneeuwval, het weer | deeltjes en het weerplan per potje |  |
| het weer: regen, onweer, zandstorm, sneeuw en sneeuwstorm | `WEER`, `weerDoel`, `updateWeer` | notities/wegwijzers.md |
| vegetatie, water, doornbos | `props`, `water`, `thickets` | notities/wegwijzers.md |
| water: één materiaal voor plas, poel, rivier, waterval en bron (palet, rimpels, glinsters, schuim, regenringen, geruis); proefstuk Test 67 | `WATER`, `waterTeken`, `waterVoorTeken`, `waterStap` | notities/water.md |
| de brug: een houten brug over een rivier, de galerij van de stad op straathoogte, je loopt er droog over (`brug: true` op een rivier) | `BRUG`, `brugTeken`, `brugIn` | notities/water.md |
| de fontein: een plaat van leem met het water erin, decor met de rand als trede; een steek in het water geeft een plons (sandbox, Fontein) | `WATER.soort.fontein`, `waterFonteinTeken`, `waterFonteinSlag` | notities/water.md |
| schilden in de wind | `SCHILD`, `schildStofUpdate`, `schildTil` | notities/decor.md |
| tonnen: houten tonnen die breken (drie treffers, Nyundo in een keer, een kalebas erin), ook op een dak of zwevende laag | `TON`, `tonRaak`, `tonBruut`, `tonPlekX`, `tonOp` | notities/tonnen.md |
| dierenkooien: houten kooien met een hyena, slang of bandiet, half of slordig onder een zanddoek, op te springen en eroverheen te lopen; een lijk valt eraf; het kistje als opstap en sfeer; decor op de stoep in muurkleur en een stuk kooi voor de camera; met `open` zwaait het deurtje open (dichtbij of op een zegel), een korte freeze, en het beest stapt gebukt naar buiten en richt zich op tot een echte vijand (Stad 16, Test 86) | `DKOOI`, `dkBouw`, `dkPlats`, `dkLijkVal`, `dkPlaat`, `dkStap`, `dkOpen`, `dkBeest`, `dkLos` | notities/kooien.md |
| wapenrek: een houten rek in de stad met speren; E pakt er een, in de hand of op de rug | `WAPENREK`, `wapenrekken`, `rekTrek` | notities/wapenrek.md |
| hangers aan savannegebouwen: kalebasrammelaars en windvangers aan de zijkant van elke savannehut (los decor, dorpsplaten, de starthut, de verre hutjes), per gebouw een knikkerzak (niets, een of twee, welke), zacht zwaaiend; ophangpunten per plaat in `HANGER.haken`; sandboxknop Hangers (bag, always, off) onder Savannedorp | `HANGER`, `hangersTeken`, `hangerVoor`, `hangerLaad`, `hangerModus` | claude/hut_hangers.md (in het project) |
| rotsdecor: losse rotsstukken als props, lui geladen, in de Maker onder Decor | `ROTS_FAM`, `rotsSoorten`, `propLaad`, `mkVulRots` | notities/decor.md |
| slangen: kleur, zicht en patrouille | `SNAKE_DIRS`, `slangZiet`, `startPatrouille` | notities/slangen.md |
| bloed op hout: bloed op een galerij, trapbalkon of brug loopt naar de plankrand en druppelt naar beneden (sluipdood bandiet, executie schildbandiet, zweepman; hooguit twee plekken per vijand) | `BLOED_RAND`, `bloedRandMeld`, `bloedRandStap`, `bloedRandTeken`, `bloedHoutBij` | notities/bloed-rand.md |
| de dood van de slang: een doodsanimatie (gewoon of snel), snee en druppels per soort kill, het lijk vervaagt na 3 s | `SLANG_DOOD`, `slangDoodStap`, `slangDoodTeken` | notities/slangen.md |
| de slangenkop eraf: slag 2 van de stokken doodt een slang, de kop vliegt naar de camera met een bats (rustig: altijd, door de camera met bloed op de lens en een zoef; druk: 1 op 6, klein, valt voor op de grond); Test 98 en de sandboxknop Snake head | `KOP`, `kopMag`, `kopStart`, `kopRustig`, `kopLensTeken`, `kopWereldTeken`, `kopStompTeken`, `kopLaadGeluid` | notities/slangen.md |
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
| de stokexecutie: met de stokken knielt de schildbandiet zonder speer, Amir rent in en doet de draaislag, een grote bloedspat op de lens, hij draait om en valt | `EXE.stok`, `exeStokStart`, `exeStokStap`, `exeStokKlap`, `exeStokTeken` | notities/schildbandiet.md |
| de bandiet-arena: het geënsceneerde eindgevecht (arena, regel 12) | `BANDARENA`, `bandArenaStart`, `bandArenaWachters` | notities/bandiet.md |
| baviaan: de eindbaas in wording (baas, regel 12) | `BAVIAAN`, `baviaanLaad`, `baviaanTeken` | notities/baviaan.md |
| Brutus (Nyundo): de bruut met de knots, baas van het plein; stormt, kapt, springt (golven door de vloer), zestien treffers (baas, regel 12) | `BRU`, `makeBrutus`, `updateBrutus`, `hitBrutus`, `bruKlem`, `bruSprongStap`, `bruGolfStap`; de gebarsten vloer: `BRU_SCHADE`, `bruSchadeTeken` | notities/brutus.md |
| de opening van het plein: het hek valt dicht, Nyundo slaat de tonnen kapot en stormt | `BRU_INTRO`, `bruIntroStap`, `bruIntroVast` | notities/brutus.md |
| tonnen naar de lens: bij die slag vliegen de stukken in perspectief op de camera af, een half deksel knalt tegen de lens | `TON.lens`, `tonLensMaak`, `tonLensTeken` | notities/tonnen.md |
| speerbeet: de baviaan pakt je speer | `BAV_BEET`, `BAV_MOND`, `BAV_SPEER` | notities/baviaan.md |
| speer in de baviaan: de speerval blijft in zijn borst zitten | `BAV_VALSPEER`, `bavSpeerTeken`, `baviaanTeken` | notities/baviaan.md |
| voorgrond: de laag tussen de camera en Amir | `VOORGROND`, `VG_SOORT`, `VG_LAGEN` | notities/voorgrond.md |
| het regenwoud: bijna zwarte silhouetten voor de camera, onderin struik en gras, bovenin bladerdak, een tak en lianen; per level een eigen indeling uit zijn naam, elke ronde dezelfde (`silhouet: false` zet het uit) | `VG_RW`, `vgRegenwoud`, `BLADERDAK`, `drawBladerdak`, `rwSilhouetAan` | notities/voorgrond.md |
| de stadsvoorgrond: kruiken, manden en een leemmuurtje voor de camera, per stuk straat naar wat er staat (De Gouden Poort) | `VG_STAD`, `vgStad`, `vgStadThema`, `voorgrond: 'stad'` | notities/voorgrond.md |
| achtergrondlagen, uitzicht per level | `SCENE0`, `SCENES` | notities/wegwijzers.md |
| startscherm, menu: hoofdmenu (Single Player, Multiplayer, Level Editor, Test Lab, klein Updates en Settings), Single Player met Campaign en Survival, het Test Lab met de Sandbox en de testreeksen; kaartjes per level | `menuMain`, `menuChoose`, `menuSurvival`, `menuLab`, `showMenu` |  |
| kaarslicht: de startfoto van onderen belicht | `KAARS`, `kaarsStart`, `kaarsLus` | notities/kaarslicht.md |
| Level Maker nieuwstijl: het grid, de Test, de controle | `MK`, `mkNaarLevel`, `mkControle`, `MK_VIJ_KNOP` | notities/maker.md |
| elk level nakijken op decor boven een ravijn | `schoonLevel`, `schoonKomend`, `komendeRavijnen` | notities/ravijn.md |
| wat er staat waar een ravijn openscheurt | `RAVIJN_DECOR`, `ravijnDecor`, `ravijnDecorStap` | notities/ravijn.md |
| golvende rand: terreinmassa's met een organische omtrek | `GOLF`, `golfAan`, `golfGrondTeken`, `golfTerrasTeken` | notities/golf.md |
| de kit van Amir verbeteren: takenlijst met cijfers per onderdeel; bij "verbeter Amir kit" de lijst tonen, de opdrachtgever kiest, afstrepen | `kit-lijst`, `G1`, `L1`, `M2` | notities/kit-verbeteren.md |
| de stad verbeteren: werklijst met cijfers en stappen; bij "stadsverbetering" eerst 3 suggesties, de opdrachtgever kiest | `stadsverbetering`, `S1`, `L1`, `V1` | notities/stad-verbeteren.md |
| de shove: aanvallen met de speer terwijl een mens te dichtbij staat en de steek niemand raakt duwt hem terug tot op steekafstand, zonder schade, een wankel en een aanvalsklok, 2 s afkoeling; in Co-op ook bij een gast (`shvR`) | `SHOVE`, `shoveDoel`, `shoveStart`, `shoveRaak`, `shoveDuw`, `shoveKlok`, `shoveGlij`, `mpcShoveVanGast` | notities/speer.md |
| de draaislag: het talent Full Circle (Mkuki) maakt een steek naar een open vijand (verblind, of net mis geslagen) een draaislag met 1 schade en een kleine terugslag; daaronder de keuze Crushing Circle (1,5 en ver terug) of Wide Circle (alles voor je). De oude reeks van drie steken en de duw op X zijn er alleen nog in Test 68 en de sandboxknop Combo | `COMBO`, `FC`, `fcModus`, `fcOpenDoel`, `fcOpenZet`, `slagEen`, `fcHalf`, `comboT`, `comboStart`, `comboSoort`, `atkCombo`, `DUW`, `duwStart`, `comboX`; de keuze in de boom: `sluit`, `tbGekozen` | notities/combo.md |
| ideeën voor de kit van Amir: basis, tribe-ability of talent; stof in de ogen (gebukt F vasthouden, de veeg met eigen animatie en geluid) | `STOF`, `STOFA`, `stofStap`, `stofWerp`, `stofDwaal` | notities/kit-ideeen.md |
| de stokken: twee stokken in plaats van de speer, slaan, blokken op C en de counter (stun of gewoon); Test 74 en de sandboxknop Stokken | `STOK`, `stokAanval`, `stokBlokStap`, `stokBlokVang`, `stokTreffer`, `atkStok` | notities/stokken.md |
| de grondklap: met de stokken in de lucht omlaag plus aanval, de stokken in de grond en een golf naar voren; Test 76 en de sandboxknop Grondklap | `GK`, `gkStart`, `gkInslag`, `gkUpdate`, `gkVak`, `gkSchadeOp` | notities/stokken.md |
| de zonnestraal: met de stokken 3 s mediteren in het licht, dan 6 s Sun Lion (geen blok, dubbele schade, sneller, de hoge sprong, twee grondklappen), dan moe; Test 77 in de reeks Test levels sticks (`STOK_LEVELS`) | `STRAAL`, `straalUpdate`, `straalBurst`, `straalMoe`, `zonnestralen`, `STOK_LEVELS` | notities/stokken.md |
| de outfits van de stoktribe: zes outfits met broek en leeuwenvacht (Homefinder, Ice Warder, Dawnbreaker, Firedancer, Moss Cleaver, Show Stopper; Test 92, en in de lobby van Co-op en Survival met de stokken, de maskers gebakken met `tools/vacht_bak.js`) | `VACHT`, `VACHT.outfits`, `vachtMasker`, `vachtKl`, `broekKeuzeKl`, `MP_VACHT`, `VACHT_BAK`, `broekMaskers`, `vachtWarmTaken` | notities/stokken.md, notities/multiplayer.md |
| de stoktribe: Bhubesi met de stokken als eigen kaart, de stokken in elk level van een episode, het blok met afkoeling, mediteren zonder straal op G, zeven talents | `bhubesi_stok`, `tribeStok`, `stokTribeLevel`, `stokBlokKoel`, `stokZonDruk`, `straalVrijZ` | notities/stokken.md |
| PvP: een tegen een over internet (PeerJS), de andere Amir, wie beslist, rondes en het stadje | `PVP`, `PVP_LEVEL`, `pvpStap`, `pvpTeken`, `pvpVang` | notities/pvp.md |
| het Duel met de kit van Co-op en de winkel: startbudget, winkel voor ronde 1 en tussen de rondes, blind sweep (stof verblindt de ander, geen dubbele schade), de grondklap raakt de ander; `tools/mptest.js --duel --duelwinkel --spelers 2` | `pvp.dw`, `duelWinkelIn`, `mpcWs`, `mpKoop`, `pvpStofIn`, `pvpBlindNa`, `pvpGkIn` | notities/pvp.md |
| de naam in Multiplayer: ieder typt zijn naam naast de lobby, een naambordje boven zijn Amir in het spel (per speler aan of uit), en het team als kaartjes in de lobby (broek, wapen, Ready) | `MP_NAAM`, `mpNaamTeken`, `mpSpelerNoem`, `mpNamenZien`, `mpTeamToon` | notities/multiplayer.md |
| de outfits van Mkuki: Amir met de speer is Mkuki (Outfit 1 standaard, ook buiten Multiplayer), in de lobby zes outfits met de speer en de oude broeken met de stokken; omkleuren per zone met `<frame>_zones.png` (tools/mkuki_spel_zones.py), `tools/outfittest.js` tekent ze allemaal; de speer los erop per speersoort (`tools/mkuki_spel_los.py`, `los.json`) | `MK_OUTFIT`, `MK_LOS`, `mkLosBeeld`, `mkSpeerTeken`, `mkSkinVan`, `mkLap`, `broekNu`, `mpBroekLijst`, `mpBroekPas` | notities/multiplayer.md |
| Multiplayer: de knop in het hoofdmenu, de lobby (de host kiest Co-op Survival of Duel, de map en de regels, de gasten drukken Ready), en het plan voor de winkel | `MP_SOORTEN`, `mpLobbyToon`, `mpWijzig`, `mpStart`, `mpNaarLobby`, `pvpDuelStart` | notities/multiplayer.md |
| het wapen in Multiplayer: ieder kiest in de lobby de speer of de stokken; de stokspeler heeft de lage zwaai, eigen winkelwaar (Hardwood sticks) en geen speerspullen | `mpWapenZet`, `mpStokken`, `mpWapenLevel`, `mpcWinkelVoorMij`, `stokHoutNu` | notities/multiplayer.md |
| drie spelers: de ster (de host een verbinding per gast, een speler-id `p` in elk bericht, doorsturen met `MP_DOOR`, `pvpZendAan` voor een speler), per slot de andere Amir, de vijandgroep, de revive-ton en Ready; Duel blijft twee | `PVP.max`, `pvp.peers`, `pvp.anders`, `pvpGastErbij`, `pvpZendAan`, `mpcDodenStap` | notities/multiplayer.md |
| Co-op Survival: de host denkt voor de vijanden (twee doelen voor dezelfde AI), de gast tekent ze en meldt zijn treffers; rondes uit de deuren, tonnen met de knikkerzak, de revive, punten en het eindscherm; testen met `tools/mptest.js --proef` (drie vensters, `--spelers 2` voor twee) | `MPC`, `mpcUpdate`, `mpcHitDoor`, `mpcStandZend`, `mpcHostStap`, `mpcSpawn` | notities/multiplayer.md |
| de Co-op episode: drie savannelevels samen, pas uit als het hele team levend bij de fakkels staat, de revive-ton bij de levende waar hij ook staat, de spawns ook bij een gast; testen met `tools/mptest.js --ep` | `COOPEP_LEVELS`, `MPC_EP`, `mpEpHostStap`, `mpEpReviveX`, `mpcEpSpawnGasten` | notities/multiplayer.md |
| The Smugglers' Cellar: de tweede Co-op episode, zeven levels met hinderlagen, van de savanne de stad in tot de kelder; in de lobby map 'b0' tot 'b6'; testen met `tools/mptest.js --hl` | `COOPEP2_LEVELS`, `MPC_EPS`, `mpEpLijst`, `mpEpKaartLevel` | notities/multiplayer.md |
| de hinderlaag en het leiband: een lijn die het team pas voorbij kan als iedereen levend bij is, dan een regie (balken, de camera langs de plekken waar de vijanden binnenkomen) en het gevecht; in een Co-op episode niet verder dan 1000 van een teamgenoot (Survival is vrij) | `MPC_HL`, `hinderlagen`, `hinderStart`, `hinderHostStap`, `hinderCamX`, `MPC_LEIBAND`, `leibandKlem` | notities/multiplayer.md |
| Ishmul, de voorstad: de tweede map van Co-op Survival (rivier met brug, plein op opstapjes met fontein, luifel, savanne), en de instellingen per map | `MP_ISHMUL_LEVEL`, `MPC_KAARTEN`, `mpcKaart`, `mpStarts` | notities/multiplayer.md |
| de versies van de Co-op map: avond, nacht met fakkels aan de muren of diepe nacht, willekeurig en om de 3 rondes een andere, gesynchroniseerd met `cv` | `MPC_VERSIE`, `mpcVersieZet`, `mpcVersieWissel`, `mpcFakkelsStap` | notities/multiplayer.md |
| de winkel van Co-op: na `winkelNa` rondes allebei naar een binnenkamer, ieder zijn eigen prijslijst en beurs, goud per kill en per ronde, Full Circle met twee upgrades die samen mogen; het scherm rechts met tabs, kaarten met plaatjes, You carry en de marktman links, Undo van de laatste aankoop, en na Ready van iedereen 3 s aftellen (Not ready stopt het) | `MPC_WINKEL`, `MPC_WINKEL_CAT`, `mpcWinkelToon`, `mpcUndo`, `mpcVertrekStap`, `mpcWinkelIn`, `mpcWinkelUit`, `mpcWinkelKoop`, `mpcGoudIedereen`, `mpcFcModus` | notities/multiplayer.md |
| de winkel als kamer: geen paneel maar de winkelkamer zelf, het spel loopt door; houten bordjes per categorie boven een uitstalplek (het wapenrek met de speren of stokken, of een plank van de winkel), leren prijslabels, de keuze licht goud op (na het schemer getekend), rechts een doek met uitleg, upgrades en Buy; koop, Undo en Ready zijn die van de oude winkel; zonder winkelkamer (het Duel) het oude scherm; `tools/winkel_mockup.js` | `WKK`, `wkk`, `wkkKan`, `wkkTeken`, `wkkNaTeken`, `wkkToets`, `wkkToon`, `wkkLijst`, `design/winkel_ui/` | notities/multiplayer.md |
| Kivuli in een level: in een Co-op episode staat hij altijd in de winkel met `kivuli: true`, de versie, Duka erna en de voorraad wisselen; een nieuw level met winkels krijgt hem in gemiddeld 1 van de 4 winkels | `kivEpBinnen`, `mpEpKivStart`, `kivBesluit(true)`, `kivep` | notities/multiplayer.md |
| verkopen in de winkel van Co-op: alles wat je kocht (ook wat blijft) voor 40% van wat je betaalde, upgrades eerst, Sell naast Buy en S, daarna Buy back | `MPC_VERKOOP`, `mpcVerkoop`, `mpcVerkoopNiet`, `mpcAfgeef` | notities/multiplayer.md |
| tester-logging: per poging een regel naar de Sheet (moves, treffers, fps, aankopen), en welke upgrade werkt: treffers en kills per wapen en aanval (`raakMet`, `killsMet`), effecten die afgingen (`effect`: ardhiLeven, prooi, door, warded, item, zilverhart, bennu) en wat de speler bij zich had (`bezit`) | `TLOG`, `tlogStap`, `tlogVast`, `tlogAanval`, `tlogRaak`, `tlogKill`, `tlogEffect`, `tlogBezit` | claude/tester_logging.md (in het project) |
| highscores per team in Co-op Survival: de combinatie van spelers, het tabblad Highscores van de testers-Sheet, het eindscherm en de knop High scores onder Multiplayer; de designer logt ook (als `designer`) | `HS`, `hsTeam`, `hsEindToon`, `hsOverzicht`, `tlogWie` | notities/highscores.md |
| notities van de designer: rechtsboven een potloodje voor bugs en verbeterpunten, naar het tabblad Notities van de testers-Sheet, en in het hoofdmenu de teller Open notes | `NOTE`, `noteOpen`, `noteZend`, `noteTelVraag` | notities/designer-notities.md |
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
| `grondSoort` | stroken grondsoort in de bodem: `[{van, tot, soort}]`, `soort` savanne, rots, straat, plein of regenwoud (die laatste loopt over ruim 500 px in); per strook een andere grondtegel, met een grillige rand die over een halve cel zacht uitloopt in de grond ernaast, ook op een savannelaag, zwever en gangvloer. De Maker schrijft het uit de grondlijn-cellen; geen bestaand level heeft het (zie `notities/grondsoort.md`) |
| `tint` | `'wit'`: de stad in een andere kleur, een keer omgekleurd bij het laden (huizen, straat, vloer, fontein, verte; niet de luifels, Amir of de vijanden). Alleen Ishmul (zie "de tint van een level" in `notities/stad.md`) |
| `weer` | het weer onderweg: `[{x, soort, sterkte}]`, `soort` uit `WEER.soorten` (`droog`, `regen`, `onweer`, `zandstorm`, `sneeuw`, `sneeuwstorm`, `mist`, `mistdik`); voorbij `x` slaat het om (zie "het weer") |
| `valschade` | `true` laat een diepe val levens kosten (standaard uit): vanaf een Amir diep een leven, vanaf twee Amir twee (`VAL_VRIJ`, `VAL_ZWAAR`, `VAL_MAX`), en vanaf zes Amir diep is hij dodelijk (`VAL_DOOD`, `fallDeath` in `valLand`), ongeacht je levens. `levelcheck.py` (regel `vallen`) meldt een val van zes Amir of dieper als FOUT |
| `rugMax` | reserve-speren op de rug: 1 in de hand plus zoveel op de rug (0 tot 5; zonder dit veld 1, `RUG_STANDAARD`, overal behalve een level met `geenSpeer`; `rugMax: 0` zet hem uit) (zie `notities/velden.md`) |
| `tickets` | het aanvalsticket: `true` aan, `false` uit, of een object met eigen getallen (`voor`, `achter`, `afstand`, `pauze`, `wacht`, ...); zonder veld `TICKET.standaard` (nu uit). Met `ticketKeuze: true` kies je het aan het begin en na R (alleen Test 96, zie `notities/ticket.md`) |
| `zicht` | `true`: een vijand merkt Amir pas op als hij hem echt kan zien. Voor hem een halve cirkel met een zichtlijn die grond en rots tegenhouden, achter hem de oude afstand maar alleen op zijn eigen niveau, en na 3 s zonder zicht vergeet hij je. Zonder veld de oude manier (alle bestaande levels); een nieuw level krijgt `zicht: true`, een spawn met `zicht: false` houdt toch de oude manier (zie `notities/zicht.md`) |
| `sneak` | `true` (naast `zicht`): de sluipaanval. Een mens-vijand (bandiet, schildbandiet, kooiman, kruisboogbandiet, zweepman) hoort je achter zijn rug in plaats van je te zien (kruipen en stilstaan stil, lopen tot net buiten steekafstand, sprinten van ver, een worp, treffer, klap of neerkomende speer geeft een puls), krijgt argwaan als je vlak achter hem staat en kijkt dan om, en een treffer van achteren op wie je niet opmerkte is in een klap dood (bij de schildbandiet langs het schild). Spawnvlaggen `rug`, `draai`, `pat`. Een nieuw level krijgt `sneak: true`; alleen Test 61 heeft het (zie `notities/sneak.md`) |
| `hpBalk` | `true` of een lijst soorten: 3 levens met een health-balkje boven het hoofd, ook voor Amir; de schildbandiet krijgt een schildbalk erboven. Zonder veld uit, een nieuw level krijgt `hpBalk: true` (zie `notities/velden.md`) |
| `slangEenKlap` | `true`: elke slang (zand, zwart, knock en fosfor) is in een klap dood, ook met `hpBalk` aan. Een nieuw level krijgt `slangEenKlap: true`; Oaktown (makkelijk) heeft het (`SLANG_EEN_KLAP`, in `hpBalkAan`) |
| `hyOmkeer` | `true`: een hyena rent na zijn uitval niet het level uit maar draait net buiten beeld om (`HY_OMKEER`) en komt opnieuw dreigen, of eerder als hij ergens tegenaan loopt; met het zicht wacht een hyena die je kwijt is net buiten beeld. De norm: een nieuw level krijgt `hyOmkeer: true`, Co-op, Co-op solo, de Maker en de sandbox (knop **Draaien om** onder Vijanden) hebben het. De bestaande episodes niet: daar rennen ze nog weg (`hyOmkeerAan`, `hyBuitenRand`) |
| `golf` | `true` of `{ruw}`: de golvende rand. De kruin van de grond, een rotsterras, het dak en de vloer van een gang en het zwarte terrein krijgen een golvende omtrek met textuur, druipstenen, keien en hangblokken (zie `notities/golf.md`); `ruw` schaalt de golven, 1 is de maat uit `GOLF`. Zonder veld uit; alleen Test 49 heeft het |
| `dakRand` | `true`: het dak van een huis houdt als vloer 0,12 Amir binnen de muur op, zodat Amir niet half naast het huis in de lucht staat (achter de kartels zie je geen dak); een trapbalkon loopt evenver de muur in. Aan in Co-op, City Survival, de Co-op episodes en de Maker; een nieuw level krijgt `dakRand: true` (zie "Achter de kartels" in `notities/stad.md`) |
| `hoogUitzicht` | `true`: gestapelde dikke grondlagen zien er op hoogte hetzelfde uit als de basis (zie `notities/velden.md`) |
| `view` | een getal van 0,5 tot 1: uitgezoomd spelen; een nieuw level krijgt standaard `view: 0.8` (zie `notities/velden.md`) |
| `zichtBreed` | een doel-wereldbreedte in beeld in plaats van een vaste `view`; geen level gebruikt het nog (zie `notities/velden.md`) |
| `camera` | `true` of `{voor, verken, vecht, telefoon}`: de meekijkende camera. Vooruitkijken in de looprichting, en op een laptop 0,75 onderweg en 0,8 in een gevecht; een telefoon houdt 0,8 en kijkt minder ver vooruit. Gaat boven `view`; in een arena neemt de arena-camera het over en geldt `view`. De standaard voor een nieuw level (Test 51 tot en met 55 en de Maker); in de sandbox de knop Meekijken (`CAM`, `camUpdate`) |
| `worp` | `'schaal'` zet de schaalworp aan: de hoek loopt op zolang je vasthoudt, van vlak tot 30 graden (`THR_HOEK_MAX`); zonder dit veld de twee trappen. In de sandbox de knop Worp onder Speerworp |
| `worpOmlaag` | `true`: pijl omlaag tijdens het spannen breekt de worp niet af maar mikt omlaag, tot 60 graden (`THR_OMLAAG`), voor een worp van een hogere laag naar beneden (alleen Test 71, zie `notities/speer.md`). In de sandbox de knop Aim down onder Speerworp; met `mikKeuze: true` kies je aan het begin en na R hoe het mikken werkt (`MIK`: streepje, zonder, vervagend, wiebel, trillen; ook de sandboxknop Aim) |
| `stof` | `true`: stof in de ogen, gebukt F vasthouden veegt stof naar een bandiet die Amir aankijkt; even blind, de volgende treffer telt dubbel (alleen Test 63, zie `notities/kit-ideeen.md`) |
| `nieuweRen` | de nieuwe ren (uit Grok) is de standaard in elk level, en het tempo van de looplus volgt de snelheid (`REN_NIEUW`, `renNieuwZet`, `renSprintZet`, `renFpsBasis`); `nieuweRen: false` geeft de oude ren, in de sandbox de knop Nieuwe ren (zie `notities/ren.md`) |
| `stokken` | `true`: Amir vecht met twee stokken in plaats van de speer (zie `notities/stokken.md`); met `stokKeuze: true` kies je aan het begin en na R of de counter een stun is of een gewone treffer (alleen Test 74); met `grondklap: true` de grondklap (omlaag plus aanval in de lucht), en met `gkKeuze: true` kies je het bereik en de schade (alleen Test 76) |
| `combo` | de draaislag van Full Circle (Mkuki): standaard aan in elk level, `combo: false` zet hem uit (zie `notities/combo.md`); met `comboKeuze: true` kies je aan het begin en na R Full Circle, Crushing, Wide, de oude drie steken of de duw (alleen Test 68) |
| `schild` | `true`: Amir heeft een schild, C (of de schildknop) houdt het op; het vangt alles van voren en net op tijd is het een parade (alleen Test 56, zie `notities/schild.md`) |
| `rand` | `true`: het level begint aan de rand. Geen rotswand en hut aan de start, de rechtergrens ligt `RAND.ruimte` (320) achter de start (een getal in plaats van `true` is die ruimte zelf) en de camera kijkt niet voorbij die grens (`randCam`, in `camUpdate`). De standaard voor elk nieuw level (Stad 1); de bestaande levels hebben het niet |
| `speerInHand` | `true`: Amir begint met de speer in de hand in plaats van hem voor zich uit de grond te pakken; de Level Maker nieuwstijl zet dit in elk level, de echte episodes hebben het niet |
| `executie` | `true`: elke dodelijke steek, worp of lage zwaai op een schildbandiet is de executie, in plaats van 1 op 5 en 1 op 3 (alleen Test 50, zie `notities/schildbandiet.md`) |
| `herhaal` | `true`: is de laatste schildbandiet weg (na de executie of de gewone dood), dan komt er na `EXE.herhaalWacht` een nieuwe aanwandelen, net buiten beeld voor Amir uit, met de vlaggen van de eerste schildman-spawn (alleen Test 50, `exeHerhaalStap`) |
| `wateren` | het water van `WATER`: `[{k, x, w}]`, `k` is `plas`, `poel`, `rivier`, `val` (van de rechterkant van een terras op `x`) of `bron` (met `hoog` in Amir); een poel en rivier laten je waden zoals de oude `water`, een rivier met `brug: true` krijgt een houten brug waar je droog overheen loopt. De rivier met de waterval (vooraan over de rand, standaard rustig, met `val: true` snel) is af: hij mag, met en zonder brug, in elk nieuw level (zie `notities/water.md`). Met `stroom: true` valt hij niet maar stroomt hij naar de camera, recht tussen de wanden met oeverplanten over de naad (alleen Test 87). De andere vormen (plas, poel, val, bron) staan nog alleen in Test 67. |
| `zonnestralen` | bundels zonlicht om met de stokken in te mediteren: `[{x, h}]` (zie "de zonnestraal" in `notities/stokken.md`; alleen Test 77) |
| `onstKeuze` | `true`: aan het begin en na R kies je Lives of Invulnerable (`duoKeuze.onst`); de stoklevels |
| `vacht` | `true` (naast `broekKeuze`): bij elke start en na R kies je een van de zes outfits voor de stokken, broek en leeuwenvacht samen (`VACHT.outfits`, alleen Test 92, zie "de outfits van de stoktribe" in `notities/stokken.md`) |
| `wapenKeuze` | `false`: dit testlevel laat niet kiezen. Standaard kies je in elk level uit een testreeks (niet de tutorial) aan het begin en na R Mkuki met de speer of Bhubesi met de stokken, behalve als het level al `stokken` of `geenSpeer` heeft (`wapenKeuzeAan`, `wapenKeuzeLevel`, in het scherm van `duoKeuze`) |
| `vredig` | `true`: geen vijanden, en ook geen vrije slangen of kalebassen die het spel anders bij lege `spawns` stuurt (Test 67) |
| `rocks` | keien om op te springen: `{x, s}` |
| `tonnen` | houten tonnen die breken: `{x, y, f, kalebas}`, of `put`/`luifel`/`kraam` met `a` (Amir van die put, losse luifel of kraam) in plaats van `x`; hoger op met `dak` (een dak of galerij van de stad, met `a` vanaf het midden van dat dak) of `zwever: true` (zie `notities/tonnen.md`) |
| `dierkooien` | dierenkooien: `{x, maat, doek, dier, f, achter, vg, s, dekking, kleur, open, id, deur}`, `maat` hoog/laag/slang, `doek` half/over, `dier` hyena/slang/bandiet, `open` `'bij'` of `'zegel'` (een zegel met `kooi: id`) laat het beest eruit als echte vijand, zonder `open` decor, `achter` decor op de stoep, `vg` voor de camera; `kistjes: [{x, f, achter, vg, s}]` het kistje onder het doek, opstap en sfeer; een spawn met `dak: 'kooi'` staat op een kooi (Stad 16, zie `notities/kooien.md`) |
| `wapenrekken` | houten rekken met speren: `{x, f, n}`, `n` speren (standaard en hooguit 4, een per touwlus), of `put`/`luifel`/`kraam` met `a` zoals bij `tonnen`; E pakt er een (zie `notities/wapenrek.md`) |
| `spawns` | vijanden: `{x, k}`, `k` is groen/zwart/knock/scorp/hyenas/panter/fosfor/bandiet/kooiman/schildman/kruisboogbandiet, met vlaggen per soort (zie `notities/velden.md`) |
| `goud` | `true`: een goudstuk per kill, een kalebas kost 5 goud in de winkel, goud en kalebassen gaan mee naar het volgende level (De Gouden Poort, zie "goud" in `notities/episodes.md`) |
| `multikill` | kills binnen 3 s na elkaar zijn een reeks, met het snoer kralen, het woord, de stinger en vanaf de tweede kill 1 goud extra (in een level met goud). Standaard aan in elk level, `multikill: false` zet hem uit (zie `notities/multikill.md`) |
| `rapport` | na het level het levelrapport in het winscherm: kills, multikills, langste reeks, tijd en goud (in een level met goud). Standaard aan in elk level, `rapport: false` zet het uit (zie `notities/multikill.md`) |
| `kelder` | het kelderluik: `{x}`, de achterkant van de wig tegen een hoge leemmuur; het luik vliegt open als Amir eraan komt en E speelt het level uit, in plaats van `ends` (alleen Stad 14, zie "het kelderluik" in `notities/stad.md`) |
| `kelderZaal` | de kelderzaal: `{trap: {x}, plafond: {r}, palen, deuren: [{x}], bundel}`, met `lagen: 'kelder'`; een spawn met `kgat: i` breekt door deur i; een kooi met een beest is een gewone `dierkooien` (alleen Test 86, zie `notities/kelder.md`) |
| `eindDeur` | de einddeur: `{gevel, verdieping}`, die deur staat open en E ervoor (op een galerij) speelt het level uit, in plaats van `ends` (alleen Stad 9, zie "de einddeur" in `notities/stad.md`) |
| `munt` | de munt van de koning: `{x, y, vast}`; E pakt hem, en na het level is er een talentpunt extra (een keer per run) |
| `kisten` | schatkisten: `{x, y, vast, goud, f}`, `y` en `vast` zoals bij de munt; E maakt hem open en `goud` (standaard 20) gaat bij je goud. Sterf je, dan is hij weer dicht (zie "de schatkist" in `notities/episodes.md`) |
| `kopgeld` | `true` (naast `goud`): een aanvoerder geeft 10 goud extra, Nyundo 25 (`GOUD.kopgeld`) |
| `schildKleur` | `true`: de makkelijke schildbandiet (`niveau: 'makkelijk'`) krijgt een bruin kleed (`SCHB_TINT`); een schildman-spawn kan ook zelf `tint` hebben |
| `bandArena` | `true`: het level is een bandiet-arena (Valse Koning 8), zoals de goudaap-arena maar met de elite-garde (zie "de bandiet-arena") |
| `duoArena` | `{c, golven, pauze, eerste, niveau}`: een arena op de open savanne rond `c` (vaste camera, geen wanden); per golf tegelijk een kruisboogbandiet en een schildbandiet, elk willekeurig van links of rechts. De schutter schiet pas helemaal in beeld (`inBeeld`, `krbInBeeld`) en zijn bouten raken de schildman (`vriendVuur`, `krbPijlVriend`). Na `golven` golven is het level uit (Test 55 en 56, `duoTick`). Met `keuze: true` kies je voor het begin de lading van de schutter (`KRB_SALVO`, standaard 2 bouten en daarna 1) en het niveau van de schildman, in plaats van `niveau` (`duoKeuze`, alleen Test 56) |
| `bandietGolf` | een oplopende golf bandieten: `{van, tot, ramp, max, dolk, niveau}`; met `niveau: true` komt een nieuwe rover alleen op de hoogte waar Amir staat, en telt een rover die op een ander niveau vastzit niet mee (Rivier 14) (zie `notities/velden.md`) |
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
| `zegels` | zegels plat in de grond: `{x, ravijn, sluit, breed, muur, speerval, teken, vijand, plafond, rijs, poort, kooi, speer, verstop, onzichtbaar, veeg, dak}`; `kooi` opent de dierenkooien met die `id` en `open: 'zegel'`; met `onzichtbaar` is er niets van te zien tot iemand erop stapt (dan gaat hij aan en verschijnt hij), met `dak` ligt hij boven een gang op de savanne in plaats van op de gang-bodem, met `verstop` ligt hij onder het zand tot de lage zwaai hem blootveegt, `veeg` kiest de onthulling (standaard de wolk, traag en middel), `veegDuur` en `veegMaat` het tempo en de grootte, `vloer` de kleur van het zand (zie `notities/velden.md`) |
| `poorten` | stenen bogen uit `design/boog/`: `{id, x, k, f, y, s, look, hek, wand, wandF, wandH, wandX, regie, bij}`, `look` steen, sneeuw of savanne (zonder: sneeuw in een winterlevel), decor; een zegel of rune met `poort: id` opent hem en dan komen de spawns met `poort: id` eruit (zie "poort"); `hek` een valhek dat optakelt, `wand` een rotswand erachter (`true` de kale wand, of een soort uit `HEK_WANDEN`: `kaal`, `spits`, `pieken`, `zuilen`, `boog`, `grot`), `wandH` zijn hoogte en `wandX` een verschuiving, allebei in Amir, `regie` vanzelf open als hij in beeld komt (of bij `bij`) met Amir vast tot de vijand eruit is (zie "het hek van de poort") |
| `rotsen` | losse rotsen als decor: `{x, soort, groot, y}`, een van de platen onder een rune (`spits`, `pieken`, `zuilen`, `boog`) zonder schijf, `x` de linkervoet, `groot` de hoogte in Amir, `y` een vaste vloer; getekend achter de plateaus, zodat een zwever erin kan snijden (zie `notities/decor.md`) |
| `rijzers` | steen dat uit een ravijn omhoog komt: `{id, r, l, tot, van, v, wacht, duur}`, `id` de naam waar een zegel of een rune (`doel: true`) met `rijs` naar wijst, `tot` en `van` de bovenkant boven en beneden (standaard -1 en -900), `wacht` seconden voor hij begint, `duur` seconden boven voor hij terugzakt (zie "rijzende grond"); met `zak: true` staat hij boven en zakt hij onder Amir weg; `look` de bovenrand (`savanne`, `rots`, `sneeuw`, `zwart`) en `kleurVanaf` een hoogte waaronder het blok zwart blijft; in een put (`putten`) is de gangvloer zijn grond (Test 48) |
| `stad` | de Sahelstad: `{paleis, seed, gevels, galerijen, kramen, voet, trappen, volk}`; `volk: [{x, k, kleur, f}]` dorpelingen op de stoep die verdwijnen als er gevochten wordt (zie "stadsvolk" in `notities/stad.md`); `luifels: [{x, kant}]` de luifel van de put zonder put (zie "de luifel bij de put" in `notities/stad.md`), of `luifels: [{gevel, wand, h, voet, maat, kleur, zak, worp}]` de springdoek aan de muur van een huis (zie "de springdoek" in `notities/stad.md`), `trappen: [{gevel, kant, niveau, balkon}]` een houten buitentrap achter een huis langs (E, zie "de stadstrap" in `notities/stad.md`), gevels van 1 tot 4 hoog met een beloopbaar dak (met `aan: true` of `aan: 0.5` staat een gevel op elk scherm tegen het huis rechts ervan, of met een steeg van zoveel Amir, zie "huizen tegen elkaar" in `notities/stad.md`), houten galerijen, kramen (`riet` draagt, `doek` veert) en de straattegel in plaats van de grondrand; met `lagen: 'stad_dag'` (Stad 1, zie `notities/stad.md`). Een galerij en een dak zijn ook de vloer van een vijand (`stadVloerBij` in `vloerBij`): een spawn met `dak: 401` (de hoogte) of `dak: true` staat erop en de rand houdt hem tegen; de camera klimt mee |
| `binnen` | de binnenkant van huizen: `[{gevel, r, l, deur, verdieping, deurH, deuren, ramen, palen, ladders, bogen, winkel, planken}]`, elk een eigen strook ver van de straat; E voor het deurgat van gevel `gevel` en je staat binnen bij de deur `deur` (recht, net als buiten), E daar en je staat weer buiten; met `verdieping: 1` zit die deur op de eerste verdieping, je gaat erin vanaf een galerij of balkon en komt binnen uit op de houten vloer van die hoogte (`deurH`); `deuren: [{deur, verdieping, gevel}]` geeft een kamer meer deuren naar buiten, elk twee kanten op, ook in een ander huis (beneden erin, boven eruit); `bogen: [{x, naar}]` is de binnenpoort, de ronde boogdeur naar een volgende kamer (een kamer met `gevel: null` heeft geen deur naar buiten); een ladder werkt als de stadstrap. Een spawn met `vloer: 450` staat op die verdieping. Stad 7, en de Maker nieuwstijl bouwt het uit Binnen-cellen (zie "binnen" in `notities/stad.md` en `notities/maker.md`) `winkel: {x, seed}` zet links een winkel (toonbank, schap, marktman, E opent het winkelscherm), `winkel.kivuli: true` zet Kivuli vast in die winkel (een Co-op episode, zie "Kivuli in een level" in `notities/multiplayer.md`; een nieuw level met winkels geeft hem aan gemiddeld 1 van de 4 winkels), `planken: [{x, h, soort, seed}]` planken met spullen aan de muur; de seed bepaalt hoe het eruitziet, dus geef een nieuw level een nieuwe (zie "de winkel" in `notities/stad.md`) |
| `straten` | een stadje van losse straten: `{start, doel, aanvul, knopen, lijst: [{id, naam, r, l, knoop}]}`; elke straat een eigen strook (van `r` naar `l`), met `raster: true` en `muur` heeft elke straat knooppunten (twee of meer, met `m` voor een middelste) met een poort de diepte in en een pad naar voren, dood op een leemmuur aan elk eind (zie "knooppunten" in `notities/stad.md`); rechtsonder een minimap op een laptop, een straat vult zich aan na `aanvul` seconden weg, en bij `doel` kills is het level uit (geen `ends` nodig, `doel: 0` is geen einde). Sandville en Oaktown (zie `notities/oaktown.md`). Een nieuw level met straten krijgt altijd `raster: true`, en alleen rechte straten: elke straat is een rij of een kolom op de kaart, nooit schuin. De hoekpoort (zonder raster) gaat eruit; geen level gebruikt hem nog |
| `hangstammen` | de hangende stam: `[{x, h, breed}]`, `x` het midden, `h` de looplijn boven de grond (standaard 190), `breed` als deel van een Amir (standaard 2,2), `tweede` na hoeveel seconden de tweede liaan vanzelf knapt (standaard 3, `false` nooit: dan blijft de schuine stam een helling); een liaan doorslaan laat hem vallen (Test 82 en 83, zie "de hangende stam" in `notities/wegwijzers.md`) |
| `holstammen` | de holle stam: `[{x, s, n, vlieg, hol, anker}]`, `x` het midden (met `anker: 'r'` de rechterkant; de breedte schaalt met het beeld zoals een kei), `hol: {dx, inhoud, h, kruis}` een verstopt hol in de binnenwand dat in vier slagen openbreekt (`inhoud` kalebas of goud: E graaft en vindt het; `ruimte`: een lege ruimte; `uitzicht`: een gat waardoor je naar buiten kijkt; `ingang`: E kruipt in een eigen hol met een kalebas of met `vondst: 'kist'` een schatkist; `kruis` een rood kruis, alleen testlevels), `s` de grootte (1 standaard, 2,25 Amir hoog; rond 0,45 kruip je erdoor), `n` hoe vaak het middenstuk erin zit (0 tot 3, standaard 0,5), `vlieg: true` de variant met vuurvliegjes; readLevel zet er een onzichtbare zwevende laag onder (bovenop lopen, plafond binnen), zoals bij de kruipstam; `boma: true` legt er een wal van doorntakken op en maakt het dak te hoog om over te springen (Test 93 en The First Hunt, zie "de holle stam" in `notities/wegwijzers.md`) |
| `holstamSoort` | het hout van de holle stam: `'savanne'` (droog gebleekt hout, `HOLSTAM_SOORT`, platen in `design/savanne/holstam/`); zonder veld het regenwoud (alleen The First Hunt) |
| `zwammen` | losse paddenstoeltjes op de grond: `[{x, k, v, s, f}]`, `k` paddo of gloei (lichtgevend), `v` de tweede paddo, `s` grootte; uit de kit van de holle stam (alleen Test 93, zie "de holle stam" in `notities/wegwijzers.md`) |
| `schachtbomen` | de schachtboom: `[{x, s}]`, `x` het midden van het gat, `s` de grootte; er hoort een holte onder te liggen, readLevel zet het gat (`gaps`) en de muur (een zwever met look `geen`) er zelf bij (alleen Test 95, zie "de schachtboom" in `notities/wegwijzers.md`) |
| `takel` | een takelwiel met een hangend plateau; sla het rad met je speer, het plateau draagt en veert (zie `notities/velden.md`) |
| `maskers` | geverfde stukken die een deel van het level verbergen: `{id, look, vakken}` (zie `notities/velden.md`) |
| `zakplafond` | stukken rots die zakken: `{r, l, rust, dicht, v, schok, duw}` (zie `notities/velden.md`) |
| `speervallen` | speren in de rotswand: `{x, h}`, `x` de klif waar hij in zit (uit `cliffs`), `h` de hoogte in Amir (standaard 0,82); een zegel met `speerval` schiet hem los (zie "speerval") |
| `runes` | ravijnen met een rune op een rots ervoor: `{x, breed, rots, groot, hoog, doel}` (zie `notities/velden.md`) |
| `fg` | strook waarover de voorgrondbegroeiing ligt: `{from, to}` |
| `voorgrond` | de onscherpe laag vlak voor de camera: `{stroken: [{van, tot, dicht, struik, kei}], los: [{x, k, s, f}]}`, `k` uit `VG_SOORT`; los van `fg`. Zonder dit veld krijgt het level de standaard, met `false` heeft het er geen, met `'stad'` de stadsvoorgrond (De Gouden Poort, zie `notities/voorgrond.md`) |
| `silhouet` | `false`: een regenwoudlevel zonder de silhouetten voor de camera (bladerdak bovenin, struiken onderin); zonder dit veld heeft elk level met een regenwoud-uitzicht ze vanzelf, ook met `voorgrond: false` (zie `notities/voorgrond.md`) |
| `arena` | het veld van de eindbaas: `{c}` |
| `cliffs` | de afsluitende rotswand: `{x}`, staat altijd achter `ends`; met `s` groter getekend (`s: 2.3` in The Dye Yard, zodat de top buiten beeld valt), de voet zakt dan dieper (`CLIFF.sinkGroot`) en wordt op de grond afgeknipt; de grens blijft op `x` |
| `ends` | de fakkels die het level uitspelen: `{x}` |
| `npcs` | dorpelingen: `{x, k, f, s}` |
| `tips` | tekst onderweg: `{x, t}` |
| `loopPutten` | de loopput: `[{x, s, f, soort}]`, `x` het midden, `s` de grootte, `f` spiegelen, `soort: 'stad'` de leemput (zonder: de savanneput); een lage put om op te staan, readLevel zet er een onzichtbaar loopvlak op dat vijanden tegenhoudt als een kei (`LOOPPUT`, alleen Test 97, zie `notities/stijlproef.md`) |
| `kopjes` | rotsen met richels: `[{x, soort, s, f, richels: [{dx, h, breed}]}]`, `soort` kopje, tafel, spleet of geen (alleen richels); de rots is achtergrond, elke richel is een loopvlak (`h` de looplijn, `breed` in wereld, `dx` vanaf het midden van de rots) met een onderkant, zodat je eronder door kunt; de platte top van de tafel draagt ook. Een treetje hoger dan zo'n 180 haalt Amir niet met een sprong (`KOPJE`, alleen Test 97, zie "Rotsen met richels" in `notities/stijlproef.md`) |
| `kruipstammen` | een omgevallen stam op twee keien om onderdoor te kruipen: `{x, s}`, `x` het midden; readLevel zet er een onzichtbaar dak onder (`KRUIPSTAM`, `kruipstamDak`; geen level gebruikt hem nog, The First Hunt heeft nu de holle savannestam met boma) |
| `mentor` | de mentor van de tutorial: `{spoor, finish, prijs, win, verlies, vallen, stations: [{zeg, seg, ok, eis, nog, kijk, terug, race}]}`; zijn spoor komt uit `tools/mentor_opname.js` (alleen The First Hunt, zie `notities/tutorial.md`) |
| `hinderlagen` | de hinderlaag van Co-op: `[{x, vecht, shots: [{x, h, t, poort, deur, kelder}]}]`, een lijn op `x` tot het hele team er levend is, dan de regie langs de shots en het gevecht; een spawn met `hl` en `shot` komt binnen op zijn shot (alleen de Co-op episode The Smugglers' Cellar, zie `notities/multiplayer.md`) |
| `pijlen` | rode pijlen in de lucht die iets aanwijzen: `{x, t}`, alleen voor testlevels (Test 47) |

### Een level toevoegen (alleen na toestemming)

1. De definitie erbij, na de laatste van die reeks. Zet er `view: 0.8` in: een nieuw level
   staat standaard op die laptop-zoom (zie het veld `view`). De bestaande episodes blijven staan
   zoals ze zijn (rule 1), dus pas hun view niet mee aan. Zet er ook `hpBalk: true` in: elke
   vijand en Amir krijgt in een nieuw level een health-balk (zie "health-balk"). Zet er ook
   `slangEenKlap: true` bij: slangen blijven in een nieuw level altijd in een klap dood. En `hyOmkeer: true`: hyena's draaien na hun uitval om in plaats van het level uit te rennen. En `zicht: true`:
   een vijand ziet je dan alleen als er niets tussen zit (zie "zicht"). En `sneak: true`: de
   sluipaanval, een mens-vijand hoort je achter zijn rug in plaats van je te zien (zie "sneak"). En `camera: true`: de
   meekijkende camera (zie het veld `camera`); een arena-level mag het ook hebben, daar neemt de
   arena-camera het over. En `dakRand: true`: wie op een dak staat, staat niet half naast het huis in de
   lucht (zie het veld `dakRand`). De Maker nieuwstijl doet dit al zelf. En `rand: true`: geen rotswand
   en hut aan de start, Amir begint aan de rand van het level en de camera kijkt er niet voorbij
   (zie het veld `rand`). Dat geldt voor elk nieuw level vanaf nu; de bestaande levels houden hun
   rotswand (rule 1, en een speerval zit in die wand). De Maker had al een kale start (`kaleKlif`).
2. De naam in de array van die reeks (`KLEI_LEVELS`, `TEST_LEVELS`, `STOK_LEVELS`, `RW_LEVELS`, `TUT_LEVELS`, `BAB_LEVELS`, `MUR_LEVELS` of `STAD_LEVELS`).
3. Een ondertitel in `SUBS`, op de naam van het level.
4. Een eigen uitzicht in `SCENES` als het level er anders uit moet zien.
   De voorgrond komt er vanzelf bij (zie hierboven); zet alleen een eigen `voorgrond` als het level
   daar iets mee wil.
5. `python3 tools/levelcheck.py` draaien, en elke FOUT oplossen voor je commit (zie
   hieronder).

### Een episode toevoegen

Die vijf stappen, plus: een knop in `menuEpisodes` (het scherm Campaign, onder Single Player in `menuChoose`;
een nieuwe testreeks die geen echte episode is krijgt juist een knop in het Test Lab, `menuLab`,
met een Back-knop met de klasse `menulab`; een reeks voor een elite-vijand of baas, zoals Reinier, Baboon tests en Murghtaan, krijgt
zijn knop in Elite tests, `menuElite`, met een Back-knop met de klasse `menuelite`), een eigen `menuXxx`-blok in de
HTML naar het voorbeeld van `menuTest`, en die aanmelden in `buildCards`,
`markCards` en `showMenu` (die kiezen nu tussen `cardsKlei`/`menuKlei`, `cardsBab`/`menuBab`,
`cardsStad`/`menuStad` en `cardsTest`/`menuTest`, en `toMenu` ook), en de reeks in `tools/speelrobot.js`,
`tools/runecheck.js` en `tools/beeldgelijk.js`. De Terug-knop van een episodescherm krijgt de klasse `menuepisodes` (terug naar
Episodes), niet `menuback` (dat gaat naar het Levels-scherm). Een episode begint met de tribekeuze (`runStart` in zijn speelknop,
`tribeLijst` geeft hem alleen wat de speler verdiend heeft, alleen `TEST_LEVELS` krijgt alles), tenzij de opdrachtgever het anders
vraagt: The Clay City heeft geen tribe en geen talents, maar loopt als solo Co-op episode met de kit en de winkel van Co-op en een keuze van wapen en moeilijkheid (`kleiSpeel`, `kleiCoopStart`).
Wil de episode een verhaal, zet dan de tekst in `VERHAAL` en `SLOT` en `verhaalAan` in zijn speelknop (nu heeft geen episode er een).

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
- **Kelderluik** (`design/stad/kelder/wig.png` en `luik.png`, uit de Grok-platen in `bron/` en de textuur van `gevel.png`) → `tools/kelder_knip.py`, daarna `gen-offline-manifest.py`; een ander canvas vraagt nieuwe maten in `KELDER`
- **Fontein** (`design/stad/fontein.png`, uit de Grok-plaat in `design/stad/bron/fontein.webp`) → `tools/fontein_knip.py`, daarna `gen-offline-manifest.py`; een nieuwe plaat vraagt nieuwe maten in `WATER.soort.fontein`
- **Winkelspullen, het derde vel** (`design/stad/binnen/spul_*.png`, uit `bron/spullen_vel3.png`) → `tools/spul_knip.py`, daarna `gen-offline-manifest.py`
- **Winkelinrichting** (`design/stad/binnen/toonbank_leem.png`, `plank_pin.png`, `wand_*.png`, `kruik_groot.png`, `zak_*.png`, `manden.png`, uit `bron/winkel_b.jpg`) → `tools/winkel_b_knip.py`, daarna `gen-offline-manifest.py`
- **Kivuli** (`karakters/kivuli/`, uit de Grok-clips van Tom) → `tools/kivuli_knip.py <map met de mp4's>` (frames komen half getemperd uit `DIM`; de lantaarn: `tools/kivuli_lantaarn.py`), daarna `gen-offline-manifest.py`
- **De slangenkop** (`enemies/slang_kop/<kleur>/`, uit de Grok-koppen in `bron/`) → `tools/slang_kop.py`, daarna `gen-offline-manifest.py`
- **De slang van Sack o' Fangs** (`enemies/slang_kivuli/`, zwart met gouden banden, uit `enemies/slang2/`) → `tools/slang_kivuli.py`, daarna `gen-offline-manifest.py`
- **Wapenrek** (`design/stad/wapenrek/`, uit de Grok-plaat in `bron/`) → `tools/wapenrek_knip.py`, daarna `gen-offline-manifest.py`
- **Deurgordijnen** (`design/stad/gordijn/`, uit de Grok-platen in `bron/`) → `tools/gordijn_knip.py`, daarna `gen-klein.py` en `gen-offline-manifest.py` (de gordijnmap staat niet in de lijst van `gen-klein.py`, dus het spel laadt de grote versie, net als bij de tonnen)
- **Dierenkooien** (`design/stad/kooi/`, uit de Grok-segmenten in `bron/` en het blad van `galerij.png`) → `tools/kooi_bak.py`, en het deurtje (`deur.png`) `tools/kooi_deur.py`, daarna `gen-offline-manifest.py`
- **Tonnen** (`design/stad/ton/`, uit de Grok-platen in `bron/`) → `tools/ton_kleur.py`, daarna `gen-offline-manifest.py`
- **Savanne-opstapjes** (`design/opstap/savanne_onder.png` uit de grondrand, `savanne_eind.png` uit de Grok-plaat in `bron/`) → `tools/savanne_opstap.py`, daarna `gen-offline-manifest.py`
- **Hangers aan de savannegebouwen** (`design/savanne/hangers/hanger_*.png`, verkleind uit de uitgeknipte Grok-platen in `bron/`, 518 px per Amir-hoogte) → `gen-offline-manifest.py`; een nieuw gebouw krijgt hangers met een regel in `HANGER.haken` (de plaat en twee ophangpunten)
- **Hutten en putten van het savannedorp** (`design/savanne/hutten/`, `design/savanne/putten/`, ook na een nieuwe Grok-plaat op wit) → `tools/rand_ontwit.py` (haalt de witte franje en het ingesloten wit weg), daarna `gen-offline-manifest.py`
- **Rotsdecor** (`design/rotsdecor/`, losse rotsstukken uit de platen in `bron/`) → `tools/rotsdecor_knip.py`, daarna `gen-offline-manifest.py`
- **Stadsvoorgrond** (`design/stad/voorgrond/`, geknipt uit `design/stad/voetdecor.png`) → `tools/stad_voorgrond.py`, daarna `gen-offline-manifest.py`
- **De val van Mkuki** (`karakters/amir/mkuki_spel/beweging/neer/`) → `tools/neer_zones.py` (de zonekaarten, ook in `klein/`), daarna `gen-offline-manifest.py`; nakijken met `tools/outfittest.js --frames mkuki_spel/beweging/neer/neer_45.png`
- **Frames van Amir** die een stokspeler kan tonen (de stokken, de lage zwaai, `beweging/`, `idle/`): daarna `node tools/vacht_bak.js` (de maskers voor de outfits van de stoktribe in `karakters/amir_vacht/`), dan `gen-offline-manifest.py`
- **De stokken van Amir** (`karakters/amir/stokken/`, uit `bron/lijf/` en `bron/stok_grok.jpg`) → `tools/stok_bak.py` (zet de regels die het print in `STOK`: de canvasmaat en `slip`), daarna `gen-klein.py` en `gen-offline-manifest.py`; `gen-klein.py` schrijft ook andere kleine plaatjes opnieuw, zet die terug
- **Tau, de leeuwenkop van de zonnestraal** (`karakters/amir/tau/`, uit de Grok-clip in `bron/`) → `tools/tau_leeuw.py`, daarna `gen-offline-manifest.py`; een ander aantal frames of een andere maat gaat in `TAU`
- **Oude speer** (`design/speer/oud/`, uit de gewone speer) → `tools/oude_speer.py`, daarna `gen-offline-manifest.py`
- **Ardhi-wapens** (`design/ardhi/`, `design/speer/ardhi/`, `bron/ar_<hoek>.png`, de winkelplaatjes) → `tools/ardhi_bak.py`, de stokken `tools/stok_variant.py --plaat design/ardhi/bron/stok_schoon.png --uit stokken_ardhi --rij 0` (kopieer de map naar `klein/karakters/amir/`), daarna `gen-offline-manifest.py`
- **Rotsen met richels** (`design/savanne/rotsen/`, uit de Grok-platen in `bron/`) → `tools/rotsrichel_knip.py`, daarna `gen-offline-manifest.py`
- **Holle stam: kit en bastrand** (`design/regenwoud/holstam/kit/`, `rand.png`, uit de Grok-platen in `bron/`) → `tools/holstam_kit_knip.py`, daarna `gen-offline-manifest.py`
- **Pathfinder Spear** (`design/speer/pathfinder/`, uit de Grok-platen in `bron/`) → `tools/pathfinder_speer.py` (zet de regel die het print in `PATHFINDER`), daarna de Pathfinder in Amirs hand (`karakters/amir/mkuki_spel/bron/pf_<hoek>.png`) met `pathfinder()` uit `tools/mkuki_spel_los.py`, en `gen-offline-manifest.py`
- **Shield Piercer** (`design/speer/piercer/jav.png` en de speer in Amirs hand, `karakters/amir/mkuki_spel/bron/sp_<hoek>.png`, uit `bron/speer.png`) → `tools/piercer_speer.py`, daarna `gen-offline-manifest.py`
- **De gids van The First Hunt** (`design/tutorial/gids/`, uit de Grok-clips in `bron/`, ook na een nieuwe opname van het spoor) → `tools/gids_bouw.py`, dan `tools/gids_glad.py` (anker op het zwaartepunt, de sprong gelijkmatig), daarna `gen-offline-manifest.py`
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
node tools/runecheck.js "Clay"          alleen de levels waarvan de naam dit bevat
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

### Lucht tussen de huizen: `tools/stadlucht.js`

Loopt de camera over de straat van elk level met `stad.achterTot` (Ishmul) en meldt FOUT waar de huizen in de verte
te vroeg ophouden, zodat je tussen de huizen lucht ziet, of waar een huis in de verte in een keer verdwijnt. Draai hem na een wijziging aan `stadAchter`, de achterrijen of
een level met `achterTot`.

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

Beweegt iets op een eigen klok die trager is dan het tekenen (een opgenomen spoor, een animatie op 30 fps die ook
de positie bepaalt), dan interpoleer je de positie tussen twee beelden, anders staat het om het beeld stil en springt
het dan (de gids van The First Hunt schokte zo naast Amir). Meet het na: de verschuiving per getekend beeld hoort
gelijkmatig te zijn, net als bij Amir.

Er zijn geen tests en geen linter, dus kijk zelf na wat je aangeraakt hebt: speelt
het level uit, blijft de speer vindbaar, staat er niets in de lucht, en geeft de
console geen 404. Merkt de speler iets van je wijziging, werk dan `README.md` bij.
Commit in het Nederlands, in dezelfde toon als de bestaande geschiedenis: één regel
die zegt wat er nu anders is, en daaronder de uitleg.
