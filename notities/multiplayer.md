# Multiplayer: de lobby, Co-op Survival en Duel

`MP_KAARTEN`, `MP_SOORTEN`, `mpStandaard`, `mpLobbyToon`, `mpWijzig`, `mpStart`, `mpSpelStart`, `pvpDuelStart`, `mpNaarLobby`;
Co-op: `MPC`, `MP_COOP_LEVEL`, `mpCoopStart`, `mpCoopStap`, `mpcUpdate`, `mpcHitDoor`, `mpcStandZend`, `mpcStandLees`, `mpcHostStap`;
de winkel: `MPC_WINKEL`, `MPC_WINKEL_KAMER`, `mpcWinkelIn`, `mpcWinkelUit`, `mpcWinkelToon`, `mpcWinkelKoop`, `mpcKlaarDruk`, `mpcGoudAllebei`, `mpcFcModus`

De knop **Multiplayer** in het hoofdmenu (was PvP, de id is nog `btnpvp`, het scherm nog `menuPvp`). De verbinding is die
van `notities/pvp.md` (PeerJS, met het relais als vangnet). Dit document is het plan voor de hele modus, uit een grill met de
opdrachtgever (november 2026). Wat gebouwd is staat erbij; de rest is de afspraak voor de volgende stukken.

## Bouwvolgorde

1. **Multiplayer en de lobby** (gebouwd). Host of Join, daarna allebei in de lobby. De host kiest de modus, de map en de
   regels; de gast kijkt mee en drukt Ready; de host drukt Start. Duel werkt zoals PvP, met de regels uit de lobby. Escape
   (pauze, Menu) brengt allebei terug naar de lobby met de verbinding nog open; **Leave the lobby** verbreekt hem.
2. **Co-op Survival** (gebouwd, zie "Co-op Survival: hoe het gebouwd is" onderaan). De aangepaste map, rondes met
   vijanden, elkaar niet raken, tonnen met de knikkerzak, de revive, het wapenrek, punten en het eindscherm.
3. **De winkel en de economie** (gebouwd, zie "De winkel: hoe het gebouwd is" onderaan). De binnenkamer, goud, de
   prijslijst, Ready, de upgrades.


## De lobby (gebouwd)

- `pvpVerbonden` start niet meer meteen het duel, maar opent de lobby (`mpLobbyOpen`, de klasse `lobby` op `menuPvp`).
- De host bewaart zijn instellingen op het apparaat (`amir.mp` in localStorage, `mpLaadInst`); elke wijziging gaat als
  `{t: 'lobby', inst}` naar de gast (`mpWijzig`) en zet de Ready van de gast weer uit.
- De gast drukt Ready (`{t: 'klaar', aan}`); pas dan mag de host op Start (`mpKnoppen`). Start stuurt `{t: 'start', regels}`
  en allebei starten met dezelfde regels (`mpSpelStart`).
- In een potje: `toMenu` stuurt `{t: 'lobbyTerug'}` en allebei gaan naar de lobby (`mpNaarLobby`). Is de verbinding weg
  (`pvp.weg`), dan sluit `toMenu` hem (`pvpStop`) en sta je weer bij Host en Join.
- Wat de gast kan kiezen: niets. Alleen de host stelt in.

### Duel-regels

| regel | standaard | wat |
| --- | --- | --- |
| Rounds | Best of 3 | 1, 3 of 5 rondes; `pvp.winst` is de helft naar boven (was `PVP.winst`) |
| Lives per round | 3 | 1 tot 5 (`pvp.levens`, `levensStart` geeft dit in een potje; er zijn nu 6 hartjes in de HUD) |
| Longer roll cooldown | aan | `PVP.rolKoel` (1,2 s) of de gewone `ROL.koel` |

### Co-op-instellingen

| instelling | standaard | bereik |
| --- | --- | --- |
| Enemies in round 1 | 1 | 1 tot 6 |
| Extra enemies per round | 1 | 1 tot 3 |
| Shop after every | 3 rondes | 2 tot 6 |
| Time between rounds | 10 s | 5 tot 30 |
| Spears in the rack | 4 | 0 tot 4 |
| Gourd chance in a barrel | 30% | 0 tot 100, per 10 |
| Enemies | alles aan | per soort Off/On, of Off/Easy/Hard/Both |

De soorten en hun twee versies (`MP_SOORTEN`):

| soort | makkelijk | moeilijk |
| --- | --- | --- |
| slangen | zandslang | zwart, knock en fosfor |
| bandiet | gewone bandiet | elite-garde, en die is in Co-op echt moeilijker: 5 levens, altijd een dolk die hij eerst werpt, iets sneller |
| schildbandiet | `niveau: 'makkelijk'` | normaal |
| kooiman | gewoon (`duel: false`) | het duel |
| kruisboogbandiet | zonder hoorn | met hoorn |
| schorpioen, hyena, goudaapje, meelman, zweepman | een vinkje | |

Bazen (panter, baviaan, Nyundo, Murghtaan) staan er niet in (regel 12, en de opdrachtgever wil ze voorlopig uit).

### De broekkleur (gebouwd)

`MP_BROEK`, `mpBroekZet`, `mpBroekVrij`, `mpBroekAnder`, `mpBroekStart`, `pvp.broek`

Links naast de lobby (`#mpamir`, een kind van `#start`, zichtbaar met de klasse `mplobby` op `#start`) staat je eigen Amir
in de idle, met pijltjes ernaast, zoals de broekkeuze van Test 73 (`BROEK`, `broekBeeld`). De lijst is het eigen paars van
Amir (geen lapje) plus `BROEK.kleuren`. Ieder kiest zelf, ook de gast; `{t: 'broek', id}` gaat naar de ander bij het openen
van de lobby en bij elke wissel. Een kleur die de ander draagt slaan de pijltjes over. Kiezen ze tegelijk dezelfde, dan
houdt de host hem en schuift de gast door naar de eerste vrije (`mpBroekAnder`). Standaard is de host paars en de gast
rood; de laatste keuze staat op het apparaat (`amir.mpbroek`). In het spel geeft `broekNu` de eigen kleur zolang `pvp`
loopt, en `pvpTeken` tekent de ander in de zijne. Geldt in Co-op en in Duel, want de lobby is dezelfde.

## Co-op Survival (stuk 2, de afspraak; gebouwd)

- **Wie stuurt de vijanden:** de laptop van de host denkt voor alle vijanden en stuurt hun plek en plaatje naar de gast (net
  zoals `pvpVang` dat voor Amir doet). Op dezelfde wifi merk je de vertraging niet. Een treffer van de gast gaat als bericht
  naar de host, die de hit-functie aanroept. Een vijand kiest de dichtstbijzijnde levende Amir als doel.
- **Elkaar niet raken:** geen steek, zwaai of speer van de een raakt de ander. Je ziet alleen je eigen speren.
- **Rondes:** ronde 1 heeft `start` vijanden, elke ronde `erbij` meer, willekeurig uit de gekozen soorten (bij Both de helft
  van de keren de moeilijke). Ze druppelen binnen over een paar seconden, niet allemaal tegelijk. Tussen twee rondes `pauze`
  seconden met "Round N" in beeld; dan raap je je speren op.
- **Waar ze vandaan komen:** dieren (slangen, schorpioen, hyena, goudaapje) alleen van de zijkant, over de grond. Mensen uit
  de deuren: beneden uit de deurgaten (`STAD_DEUR`), boven uit nieuwe deuren op de galerij (twee per huis, 401), en uit een
  deur hoog in het middenhuis met een klein balkon (optie B, alleen kruisboogschutters, hooguit 2 tegelijk; niet te bereiken,
  wel met een worp te raken). Boven staan er hooguit 5 tegelijk; daarna komen ze beneden. Een deur slaat open, de vijand stapt
  eruit, de deur valt dicht met een klap (met geluid). Een vijand blijft op zijn niveau (regel: geen treden). Zie de mockup
  `mockups/pve-map.png`.
- **Geen executies:** een executie bevriest het beeld, en dat kan niet als de ander doorspeelt. In Co-op is de executie uit,
  ook de sluipaanval met de regie.
- **De kit:** de gewone kit plus stof in de ogen (gebukt F vasthouden, 8 s afkoeling, `STOF.koel`), net als in de levels.
  Geen talents en geen tribe; wat je erbij krijgt koop je in de winkel.
- **Levens:** 3 per speler, met een health-balk. Een kalebas geeft er een terug.
- **Tonnen:** elke ronde een ton op een willekeurige bereikbare plek (straat, galerij, de daken van de lage huizen, de
  kramen). Wat erin zit komt uit een knikkerzak: 10 knikkers, `kalebas`% kalebassen en de rest goud (3 voor wie hem breekt).
  Is de zak leeg, dan wordt hij opnieuw gevuld. Zo komt het percentage echt uit, zonder lange droge reeksen.
- **Dood en revive:** wie doodgaat blijft als lijk liggen, de camera volgt de teamgenoot, bovenin "Waiting for revive".
  20 s na de dood komt er een revive-ton (met de letters REVIVE erop, drie treffers). Wie hem breekt en het symbool pakt,
  revivet de ander: die staat op naast hem met 1 leven. Zijn allebei dood, dan is het game over.
- **Het wapenrek:** een rek midden in het level met `rek` speren. Je draagt er hooguit 2 (1 in de hand, 1 op de rug),
  3 met het extra slot uit de winkel. Een speer uit het rek komt niet terug. Na elke winkel is het rek weer vol en heeft
  ieder zijn speren terug.
- **Punten (teamtotaal):** slang, schorpioen, goudaapje, hyena 10; bandiet, meelman, zweepman 15; kooiman, kruisboog 20;
  schildbandiet 25. De moeilijke versie 5 extra. Een multikill 10 extra per kill in de reeks.
- **Eindscherm:** alleen het team: score, de ronde waarin het eindigde, tijd. Een highscore op het apparaat, per keuze van
  vijanden.

## De winkel en de economie (stuk 3, de afspraak; gebouwd)

- Na elke `winkelNa` rondes (zodra de laatste vijand dood is) gaan allebei met een fade naar de binnenkamer van de winkel
  (`binnen` met `winkel`). Wie dood was staat daar gratis weer op. Ieder doet E bij de toonbank en krijgt zijn eigen
  winkelscherm. Verder gaat het als allebei **Ready** drukken.
- **Goud:** het goud van een kill wordt gedeeld, ieder de helft: per persoon 1 voor een dier, 2 voor een mens, 3 voor een
  schildbandiet of kruisboog. Plus 5 per persoon per overleefde ronde. Ieder heeft zijn eigen beurs, en **Give 5 gold**
  geeft je teamgenoot 5 van jouw goud.
- **De prijslijst** (per speler):

| artikel | prijs | hoe vaak |
| --- | --- | --- |
| Kalebas | 5 | tot je levens vol zijn |
| Nieuwe speer | 10 | tot je slots vol zijn |
| Gif | 25 | per speer |
| Full Circle (de draaislag op een open vijand, ook verblind door het stof) | 30 | 1 keer |
| Full Circle: meer schade (1,5 en ver terug, zoals Crushing Circle) | 50 | 1 keer, na Full Circle |
| Full Circle: rondom (raakt iedereen om je heen, ook achter je) | 50 | 1 keer, na Full Circle |
| Extra speerslot (een 2e reserve) | 45 | 1 keer |
| Extra leven, permanent | 60, dan 90, dan 120 | 3 keer |
| Give 5 gold | 5 | onbeperkt |

  De twee upgrades van Full Circle mogen samen (anders dan in de talent tree, waar het een keuze is). Rondom is nieuw:
  Wide Circle raakt alleen voor je, dus rondom vraagt een eigen raakzone.
- Afgewezen: de Ankh, planken voor een deur en de gouden speerpunt.

## Co-op Survival: hoe het gebouwd is

Het blok `// ---- multiplayer: Co-op Survival ... ----` in de HTML, na de lobby.

- **De host denkt, de gast tekent.** De update-functies van de vijanden (`updateSnakes`, `updateBandieten` en de rest, met
  `updateGoudapen` en `updateFosforSlangen`) zijn omwikkeld met `mpcUpdate`. Bij de gast doen ze niets. Bij de host splitst
  de wikkel de lijst in wie achter de host aan zit en wie achter de gast (`mpcDoel`: de dichtstbijzijnde levende Amir, met
  een marge `MPC.wissel` zodat hij niet heen en weer wisselt), draait de functie voor de eerste groep gewoon en voor de tweede
  met de stand van de gast in `world`, `ph`, `dead`, `invuln`, `lives`, `facing`, `duckT`, `duckShare` (`mpcWisselIn`/`Uit`).
  Zo gaat dezelfde AI achter de gast aan zonder dat er een regel AI veranderd is. Roept een vijand in die tweede ronde
  `hurtPlayer` aan (een slag in de update, zoals de zweepman en de schildbandiet), dan gaat dat als `au2` naar de gast; schrijft
  hij levens rechtstreeks (de fosfor), dan gaat het verschil.
- **De stand over de lijn** (`mpcStandZend`, `MPC.hz` keer per seconde, over het snelle kanaal van `notities/pvp.md`): per
  lijst (`MPC_LIJSTEN`) de id's in volgorde, en per vijand alleen de velden die veranderd zijn sinds het laatste bericht dat de
  gast bevestigde. De gast stuurt in zijn `s` het hoogste volgnummer `ak` dat hij kreeg (`pvp.vAk` bij de host); elk veld
  onthoudt in welk bericht het het laatst veranderde (`mpSeq`). Zo maakt een weggevallen bericht niets uit: het volgende
  draagt het mee. Een kogel gaat mee tot hij bevestigd is, een lege lijst ook (`leegQ`). Over het betrouwbare kanaal (het
  relais) is "bevestigd" gewoon het vorige bericht. Elke `MPC.sleutel` seconde alles. Een veld is een getal op twee decimalen,
  een tekst, of een object dat JSON wil (een kring zoals `groep` van de fosfor, een plaatje of een groot brok gaat niet mee,
  `mpcWaarde`). De gast zet elk bericht in de speelbuffer (`pvpNetIn`) en bouwt zijn lijsten op als het aan de beurt
  is (`mpcStandLees`, vanuit `mpcVolgStap`); daarna staat elke vijand tussen dat bericht en het volgende in (`mpX0`). Kogels, dolken, meelzakken en gif (`los` in `MPC_LIJSTEN`) komen een keer over en vliegen daarna bij de gast
  zelf, zodat ze hem ook raken; komt er een bij hem neer, dan komt hij niet terug (`losWeg`). De goudaapjes rekenen in
  `bavKlok`: hun tijden schuiven bij de gast mee met het verschil tussen de klokken (`MPC_GAAP_TIJD`), want zijn eigen
  `bavKlok` meet ook de tik van zijn speer.
- **Wie raakt wie.** Het tekenblok van de gast tekent de vijanden met de gewone code, en die kijkt ook of een vijand de gast
  raakt (zoals in PvP beslist het slachtoffer). De hit-functies (`enemyTakeHit`, `hitBandiet`, `hitSchildman`, ...,
  `gaapDood`, `MPC_HIT`) zijn bij de gast een doorgeefluik (`mpcHitDoor`): ze sturen `mh` met de lijst en de id, hooguit een
  keer per `MPC.dubbel`. Zelf doen ze alleen wat de gast meteen moet voelen (`pvpRaakLokaal`): een witte flits, het geluid
  van een speer in vlees en een korte hitstop; de schade komt van de host. De host roept de echte functie aan met de stand van de gast in de globalen
  (`mpcTrefferVanGast`), voor een slang of schorpioen de uitgeschreven dood uit het tekenblok (`mpcInlineDood`).
- **Elkaar niet raken:** `pvpTeken` tekent in Co-op alleen de ander (met een groen pijltje) en stopt voor zijn speer en de
  treffers.
- **De rondes** (`mpcHostStap`, alleen de host): eerst wacht ronde 1 tot de gast geladen is (`cklaar`; tijdens het laden stuurt
  ieder `hb`, anders verbreekt `PVP.stilte` het potje). Dan `wacht` (de pauze, met "Round N in .. s") en `golf`: de rij uit
  `mpcRonde` druppelt binnen, `MPC.tussen` seconden uit elkaar en hooguit `MPC.tegelijk` tegelijk. Op is de ronde als de rij
  leeg is en er niemand met `mpSoort` meer leeft (`mpcLevend`, `mpcLeeft`).
- **Waar ze vandaan komen** (`mpcSpawn`): dieren op de rand (rechts `cliffAt().wall - 220`, links `endWall() + 220`), mensen uit
  een deur van `MPC_DEUREN`. De deuren zijn het systeem van `STAD_DEUR`: `stadDeurenAlle` en `stadDeurenBoven` zijn omwikkeld
  zodat er in Co-op een houten deur hangt en op de galerij een deur staat in plaats van het raam, en `mpcDeurOpen` zet de
  staat die `stadDeurUpdate` openzwaait; na `MPC.deurOpen` valt hij dicht met `deurSlamSpeel` (`mpcDeurStap`). Boven (galerij
  en balkon) hooguit `MPC.boven`, alleen voor de soorten van `STAD_DEUR.bovenSoorten`. De kruisboog kiest zes op de tien keer
  het balkon (hooguit `MPC.balkon` daar): de nis van `balkon: 'nis'` op de tweede verdieping van het middenhuis (`mpcBalkonMaat`).
- **De soorten** (`mpcMaak`): slangen makkelijk de zandslang, moeilijk zwart of knock, of een op de drie keer een groep fosfor;
  de bandiet moeilijk is de elite-garde met `MPC.elite.hp` levens en een dolk; de kooiman moeilijk is het duel, zonder de
  bevroren opening (`vogelGedaan`), want een freeze kan niet als de ander doorspeelt; de kruisboog moeilijk met de hoorn.
- **Geen executies:** `exeKans` geeft in Co-op altijd false. De sluipaanval staat uit omdat het level geen `sneak` heeft.
- **Tonnen** (`mpcTonNieuw`, `MPC_TONPLEK`): bij het begin van elke ronde een op een vrije plek, bij allebei met dezelfde id
  (`ton`). Een treffer van de gast gaat naar de host (`tonH`, de omwikkelde `tonRaak`), de host telt en stuurt elke treffer
  terug voor het beeld (`tonR`). Breekt hij, dan krijgt wie brak een knikker uit de zak (`mpcKnikker`, `buit`). De kalebas
  gaat in je zak (Q), het goud in `pvp.coop.goud` (ieder zijn eigen, in de HUD).
- **Dood en revive:** wie dood is ligt (`mpcLig`, het plaatje plat om zijn voeten, want het spel heeft geen doodspose), het
  dood-scherm komt niet, en de camera volgt de ander (`mpCoopCam`, in de hoofdlus vlak voor `camSwap`). Na `MPC.reviveNa`
  zet de host een revive-ton (drie treffers, "REVIVE" erop, `mpCoopTeken`) bij de levende; breekt hij, dan valt het symbool
  (`sym`), en wie het aanraakt (`mpcSymboolStap`) laat de ander naast zich opstaan met 1 leven (`symPak`, `mpcOpstaan`).
  Allebei dood: `mpcEinde`.
- **Het wapenrek:** een `wapenrekken` in het midden met `rek` speren, en `rugMax: 1`. Wie er een pakt meldt de nieuwe stand
  (`rek`). "Na elke winkel weer vol" komt met stuk 3.
- **Punten en einde:** de host ziet een kill aan een vijand die leefde en nu niet meer (`mpcKillKijk`), telt `MPC.punten`
  plus de reeks (`mpcKill`, met "Double Kill" in beeld) en stuurt de stand mee (`cs`). Het eindscherm (`#mpeind`,
  `mpcEindToon`) met de beste score per keuze van vijanden in localStorage (`mpcEindSleutel`). R bij allebei: opnieuw
  (`mpCoopOpnieuw`, `cnieuw`); Escape: de lobby.

### Anders dan de afspraak

- Op de galerij staat een deur per huis, niet twee: het deursysteem van de stad kent een deur per verdieping per huis (op
  de plek van het raam). Twee vraagt een tweede deurplek in `STAD_DEUR`.
- De elite-garde is niet sneller dan de gewone bandiet; alleen de levens en de dolk zijn anders.

### Wat nog kan

- De gast ziet de vijanden een tikje later dan de host (netwerk plus de speelbuffer). Een slag die bij de host nog loopt,
  kan bij de gast al raken of net niet. Op dezelfde wifi valt het niet op; via het relais (15 per seconde) meer. Stap 2 is
  drie spelers, stap 3 een eigen TURN-server zodat niemand meer op het relais hoeft (zie "De netcode" in `notities/pvp.md`).
- Een vijand op de galerij die achter een speler op de straat aan zit, blijft boven staan kijken (regel: geen treden). Zo is
  het bedoeld, maar met een ronde die daardoor niet opraakt moet je naar boven.

## De winkel: hoe het gebouwd is

Het blok `// ---- multiplayer: de winkel en de economie van Co-op (stuk 3) ----` in de HTML, na Co-op.

- **De kamer.** `MP_COOP_LEVEL` heeft een `binnen` met een `winkel` (de toonbank, de marktman, een plank) ver van de straat
  (`MPC_WINKEL_KAMER`, van -20000 tot -21700), zonder deur naar buiten (`gevel: null`), en een houten plafond (`zwevers`).
  Het gewone systeem van "binnen" doet de rest: de camera, de muren, E bij de toonbank (`binnenE` opent `winkelUIOpen`).
- **Erheen.** Is de ronde op (`mpcHostStap`) en is het rondenummer een veelvoud van `winkelNa`, dan stuurt de host `winkel`
  en roepen allebei `mpcWinkelIn` aan: de fase `winkel` (`C.inWinkel`), wie dood was staat op met 1 leven, de revive-ton en
  het symbool zijn weg, ieder krijgt zijn speren terug (`mpcSperenTerug`) en een fade (`stadTrapFade` met `BINNEN.fade`) zet
  hem bij de deurkant van de kamer (`MPC_WINKEL_KAMER.plek`, per speler). Zolang de fase `winkel` is, doet `mpcHostStap`
  verder niets.
- **Het winkelscherm.** Hetzelfde `#winkelui`, met de klasse `coop`: de drie dingen met verkopen en terugkopen zijn weg, in
  de plaats komt `#wkcoop`, de prijslijst `MPC_WINKEL` als knoppen (`mpcWinkelToon`, `mpcWinkelNiet` zegt waarom iets niet
  kan, `mpcWinkelKoop` koopt), en de knop **Ready** (`#wkklaar`). Het scherm pauzeert zoals altijd, maar `pvpStap` loopt in
  de pauze door, dus de verbinding blijft leven en de ander speelt gewoon. De banner van Co-op is weg zolang het scherm open is.
- **Ready.** `mpcKlaarDruk` zet het aan of uit en stuurt `wkklaar` naar de ander (die toont "Your teammate is ready"); de host
  telt (`mpcWinkelKlaar`), en zijn het er twee, dan stuurt hij `winkelUit` en roepen allebei `mpcWinkelUit` aan: het scherm
  dicht, het rek weer vol (`rek` uit de lobby), een fade terug naar de startplek, en bij de host de pauze naar de volgende
  ronde (`mpcVolgendeRonde`).
- **Goud.** De host ziet de kill (`mpcKill`) en geeft ieder `MPC.killGoud` (dier 1, mens 2, schildbandiet en kruisboog 3), en
  aan het eind van elke ronde ieder `MPC.rondeGoud` (5), via `mpcGoudAllebei`: zichzelf meteen, de gast met `cg`. Give 5 gold
  is `geef`. Ieder houdt zijn eigen beurs in `pvp.coop.goud`; die gaat niet over de lijn.
- **De upgrades** staan in `pvp.coop.koop` (ieder de zijne). Full Circle: `fcModus` geeft in Co-op `mpcFcModus`, met
  `basis`, `kracht`, `rond` of `kracht_rond`; het level heeft `combo: true`. `fcKracht` (de 1,5 en de grote terugslag) en
  `fcRondNu` (rondom) lezen `fcSoort`; rondom is een raakzone om Amir heen (`MPC.rond`, in `steekDX`, `steekY`, `steekR`) en
  raakt iedereen een keer, net als Wide Circle (`fcBreedNu`, `slagEen`). Het extra speerslot is `RUG_MAX` plus een, een extra
  leven `pvp.levens` plus een (dat is wat `levensStart` in een potje geeft).

### Anders dan de afspraak, of zelf ingevuld

- **Kalebas, "tot je levens vol zijn":** een gekochte kalebas is meteen een leven terug, en kan alleen als je levens niet vol
  zijn. Een kalebas uit een ton gaat nog wel in je zak (Q).
- **Gif, "per speer":** het gif gaat in je tas, zoals in de levels (I om het op je speren te smeren), en je hebt er hooguit
  zoveel in je tas als je speerplekken hebt (hand plus rug: 2, of 3 met het extra slot).
- **Speren terug:** bij het binnenkomen van de winkel, niet bij het weggaan, zodat je ziet wat je hebt. Terug krijg je de
  speer in de hand en de gewone plek op de rug; het extra slot vul je zelf (een speer kopen, of van het rek). Wat er nog op
  straat lag (een gegooide speer, ook een van het rek) is weg.
- **Rondom:** de draaislag begint nog steeds met een steek naar een open vijand voor je (`fcOpenDoel`); pas de slag zelf raakt
  rondom.
- Wie dood de winkel in gaat, staat op met 1 leven (de kalebas in de winkel vult de rest).

## Testen

`node tools/mptest.js` speelt Co-op met twee vensters en een nagebootste verbinding (Node geeft de berichten door). `--proef`
loopt de vaste stappen na (een ton breken als gast, een treffer van de gast, de winkel met kopen, Give 5 gold, Ready en
terug, Full Circle rondom voor en achter, allebei dood, het eindscherm, R, Escape) en
meldt per stap OK of FOUT; zonder `--proef` lopen twee simpele spelers op de vijanden af, met `--taai` zonder dood te gaan,
`--sterf gast` om de revive te zien, `--soorten bandiet,slang` voor een paar soorten en `--shots map` voor plaatjes.


Voor de lobby is eerder een los script gebruikt met een nagebootste `Peer` die berichten tussen twee
vensters in een browsercontext doorgeeft via een `BroadcastChannel` (Host, Join, lobby, instellen, Ready, Start, Escape
naar de lobby, Leave). De echte PeerJS-server is vanuit de cloud van Claude niet te bereiken.
