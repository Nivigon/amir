# Multiplayer: de lobby, Co-op Survival en Duel

`MP_KAARTEN`, `MP_SOORTEN`, `mpStandaard`, `mpLobbyToon`, `mpWijzig`, `mpStart`, `mpSpelStart`, `pvpDuelStart`, `mpNaarLobby`;
Co-op: `MPC`, `MP_COOP_LEVEL`, `mpCoopStart`, `mpCoopStap`, `mpcUpdate`, `mpcHitDoor`, `mpcStandZend`, `mpcStandLees`, `mpcHostStap`;
de winkel: `MPC_WINKEL`, `MPC_WINKEL_KAMER`, `mpcWinkelIn`, `mpcWinkelUit`, `mpcWinkelToon`, `mpcWinkelKoop`, `mpcKlaarDruk`, `mpcGoudIedereen`, `mpcFcModus`, `GRISGRIS`;
de versies van de map: `MPC_VERSIE`, `mpcVersieZet`, `mpcVersieWissel`, `mpcFakkelsStap`, `stad_diepnacht`, `donkerGatenNa`;
drie spelers: `PVP.max`, `pvp.peers`, `pvp.spelers`, `pvp.anders`, `pvpGastErbij`, `pvpGastWeg`, `pvpZendAan`, `MP_DOOR`, `mpcDodenStap`

De knop **Multiplayer** in het hoofdmenu (was PvP, de id is nog `btnpvp`, het scherm nog `menuPvp`). De verbinding is die
van `notities/pvp.md` (PeerJS, met het relais als vangnet). Dit document is het plan voor de hele modus, uit een grill met de
opdrachtgever (november 2026). Wat gebouwd is staat erbij; de rest is de afspraak voor de volgende stukken.

## Voor wie (november 2026)

Online spelen is voorlopig voor laptops: twee of drie, elk op zijn eigen netwerk mag. Een telefoon op mobiele data hoeft
niet (afspraak met de opdrachtgever). Tussen gewone thuisnetwerken verbinden de laptops rechtstreeks (STUN); lukt dat niet,
zoals op kantoor, een universiteit of hotel-wifi, dan gaat het na `PVP_RELAY.na` seconden vanzelf via het relais. Stap 3
van de netcode (een eigen TURN-server, Metered of Cloudflare) staat daarom in de wacht tot de opdrachtgever erom vraagt
(regel 15 in `CLAUDE.md`). Het relais en de gratis TURN-servers in `PVP_ICE` blijven staan.

**Welke weg de lijn neemt (Safari, november 2026).** Een gast in Safari op dezelfde wifi had een hoge ping en een
schokkerige Co-op. Safari verstopt zijn eigen adres achter een `.local`-naam, en lukt de rechtstreekse lijn op het netwerk
dan niet, dan gaat PeerJS stil via een gratis openbare TURN-server: traag, en in Co-op merk je dat het meest. Daarom meet
`pvpRouteMeet` (elke `PVP_NET.route` seconden, uit `getStats`) welke weg de lijn echt neemt: `lan`, `net` of `turn`
(`pe.route`, `pvpTurn`). De lobby zegt `direct, local network`, `direct` of `via TURN server, slow`, en de HUD zet
`(TURN)` of `(relay)` achter de ping. Verder gaat het sleutelbericht van de vijanden ('v' met alles, elke `MPC.sleutel`
seconde) over het betrouwbare kanaal: over het snelle kanaal viel zo'n groot bericht in zijn geheel weg zodra een stukje
zoekraakte. Blijkt het TURN te zijn, dan helpt alleen stap 3 echt, en die wacht op de opdrachtgever.

## Bouwvolgorde

1. **Multiplayer en de lobby** (gebouwd). Host of Join, daarna allebei in de lobby. De host kiest de modus, de map en de
   regels; de gast kijkt mee en drukt Ready; de host drukt Start. Duel werkt zoals PvP, met de regels uit de lobby. Escape
   (pauze, Menu) brengt allebei terug naar de lobby met de verbinding nog open; **Leave the lobby** verbreekt hem.
2. **Co-op Survival** (gebouwd, zie "Co-op Survival: hoe het gebouwd is" onderaan). De aangepaste map, rondes met
   vijanden, elkaar niet raken, tonnen met de knikkerzak, de revive, het wapenrek, punten en het eindscherm.
3. **De winkel en de economie** (gebouwd, zie "De winkel: hoe het gebouwd is" onderaan). De binnenkamer, goud, de
   prijslijst, Ready, de upgrades.
4. **Drie spelers** (gebouwd, stap 2 van de netcode, zie "Drie spelers: de ster" onderaan). Co-op voor twee of drie; het
   Duel blijft een tegen een.


## De lobby (gebouwd)

- `pvpVerbonden` start niet meer meteen het duel, maar opent de lobby (`mpLobbyOpen`, de klasse `lobby` op `menuPvp`).
- De host bewaart zijn instellingen op het apparaat (`amir.mp` in localStorage, `mpLaadInst`); elke wijziging gaat als
  `{t: 'lobby', inst}` naar de gast (`mpWijzig`) en zet de Ready van de gast weer uit.
- Elke gast drukt Ready (`{t: 'klaar', aan}`, bij de host in `pvp.klaarVan` per slot); pas als iedereen klaar is mag de host
  op Start (`mpKnoppen`; met drie spelers mag het Duel niet). Start stuurt `{t: 'start', regels, spelers}` en iedereen start
  met dezelfde regels (`mpSpelStart`). Onder de eerste regel staat wie er in de lobby staat (`#mpspelers`), bij de host met
  de code erbij, zodat een derde nog kan inbellen.
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
Amir (geen lapje) plus `BROEK.kleuren`. Ieder kiest zelf, ook een gast; `{t: 'broek', id}` gaat naar de anderen bij het
openen van de lobby en bij elke wissel (een gast via de host). Een kleur die een ander draagt slaan de pijltjes over. Kiezen
twee tegelijk dezelfde, dan houdt het laagste slot hem (de host eerst) en schuift de ander door naar de eerste vrije
(`mpBroekAnder`). Standaard is de host paars, de eerste gast rood en de tweede turkoois (`MP_BROEK_STANDAARD`); de laatste
keuze staat op het apparaat (`amir.mpbroek`). In het spel geeft `broekNu` de eigen kleur zolang `pvp`
loopt, en `pvpTeken` tekent de ander in de zijne. Geldt in Co-op en in Duel, want de lobby is dezelfde.

### Het wapen: speer of stokken (gebouwd, 16-11-2026)

`mpWapenEigen`, `mpWapenZet`, `mpWapenAnder`, `mpWapenToon`, `mpStokken`, `mpWapenLevel`, `pvp.wapen`, `#mpwapen`

Onder de broek naast de lobby kiest ieder zijn wapen, **Spear** of **Sticks** (de stokken van `notities/stokken.md`), net als
de broek: per speler, bewaard op het apparaat (`amir.mpwapen`), `{t: 'wapen', w}` naar de anderen (in `MP_DOOR`, en een nieuwe
gast krijgt de keuzes in `pvpGastErbij`). Met de stokken start het potje (Co-op en Duel) als een level met stokken: `mpWapenLevel`
zet `stokken`, `geenSpeer` en `rugMax: 0` in de kopie van het level, dus geen speer, geen rug en geen worp. Het voorbeeld naast
de lobby staat dan in het staande stokframe.
- **De lage slag (16-11-2026):** gebukt slaan is met de stokken de lage slag (`stokLaag`, zie "De lage slag" in
  `notities/stokken.md`), in plaats van de lage zwaai van de speer die hier eerst tijdelijk zat. Hij loopt op `atkStok`
  en `atkFrame`, dus de andere Amir, de treffers van de gast (`mh`) en Duel (`ss`, `STOK.punt`) werken zoals bij de slag.
- **De counter** is in Multiplayer altijd de stun (`stokTreffer`), zodat het op elke laptop hetzelfde is.
- **Co-op, een treffer van de gast:** de gast stuurt in `mh` zijn slag mee (`st` de set, `sf` het frame, `co` Full Circle,
  `hw` Hardwood); `mpcTrefferVanGast` zet die tijdens de treffer in `atkStok`, `atkFrame` en `atkCombo` (en `stokHoutGast`),
  zodat de schade, de counter door de dekking en de stun van de gast zijn en niet van de host. Daarna `stokTreffer` met
  `'gevolg'` (de reeks, het wankelen, de stun); de gast speelt zelf `'gevoel'` (de klap, hitstop, de lens). Dat lost ook op
  dat een treffer van een gast vroeger met de steek van de host rekende.
- **Duel:** het `s`-bericht heeft `ss` (de stokset); `pvpTekenEen` rekent de punt en de reik van die slag uit `STOK.punt` en
  `STOK.reik`. Elke nieuwe slag telt als nieuwe steek (`pvp.sn`, ook een gebufferde die op frame 0 begint). De stapslag stapt
  niet door de andere Amir heen (`stokVijandVoor`). Het blok vangt een klap van de ander via `hurtPlayer`, zoals in een level.
- **De winkel:** een artikel met `speer: true` (speer, gif, Full Circle en zijn upgrades, extra speerslot) ziet een stokspeler
  niet, een met `stok: true` (**Hardwood sticks**, 40 goud: de slag, stapslag en slag 2 kosten 0,75 in plaats van 0,5,
  `STOK.schadeHout`, `stokHoutNu`) alleen hij (`mpcWinkelVoorMij`). Het rek en `mpcSperenTerug` geven hem geen speer.
- **De grondklap (16-11-2026):** een stokspeler heeft in Co-op de grondklap van `notities/stokken.md` (`mpWapenLevel` zet
  `grondklap`, niet in het Duel), met 5 s afkoeling (`GK.koelCoop`). Een treffer van de golf van een gast gaat in `mh` met
  `gk` (begin, eind van "recht eronder", richting, schade, knock) naar de host, die er tijdens de treffer `gkRaak` van maakt,
  zodat de schade en de terugduw van de gast zijn (`gkVan`, `gkKnock` op de vijand). De klap zelf (golf, stof, geluid) gaat
  met `{t: 'gk'}` naar de anderen (in `MP_DOOR`), alleen voor het beeld (`gkKlapBeeld`). In de winkel **Ground slam: heavier**
  (50 goud, `slam`, `stok: true`): een hele treffer in plaats van een halve en 1,6 keer verder terug (`GK.zwaar`, `gkZwaarNu`).
  `tools/mptest.js --stokken host,gast --soorten bandiet` kijkt het na.
- **Open:** de stokken doen alleen bij een bandiet een halve treffer (`stokSchade` zit alleen in `hitBandiet`); bij de andere
  vijanden is een stokslag een hele. In het Duel kost elke stokslag een leven, net als een steek. De slippen aan de grip
  tekent alleen je eigen Amir. Testen: `tools/mptest.js --stokken gast` (of `host`, met `--duel`).

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
- **Lijken (16-11-2026):** een dode vijand is na `MPC.lijkWeg` (5) seconden weg, met een wolkje stof (`mpcLijkStap` bij de
  host, `mpcLijkWolk`); de gast volgt de lijst van de host en zet dan ook een wolkje. `tools/mptest.js --stokken host,gast
  --soorten bandiet` kijkt na dat het lijk bij allebei binnen 6 s weg is.
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
  dood-scherm komt niet, en de camera volgt de ander (`mpCoopCam`, in de hoofdlus de eerste keus van de camera, met `camVast`
  uit: anders zette de meekijkende camera hem elk beeld terug op het lijk en schudde het beeld). Pijl links en rechts (ook de
  stick op een telefoon) wisselen tussen je eigen lichaam en elke levende teamgenoot (`mpcKijkStap`, `mpcKijkNu`,
  `pvp.coop.kijk`); zonder keuze de dichtstbijzijnde, en onder de banner staat naar wie je kijkt (`#mpkijk`). Na `MPC.reviveNa`
  zet de host een revive-ton (drie treffers, "REVIVE" erop, `mpCoopTeken`) bij de levende; breekt hij, dan valt het symbool
  (`sym`), en wie het aanraakt (`mpcSymboolStap`) laat de ander naast zich opstaan met 1 leven (`symPak`, `mpcOpstaan`).
  Allebei dood: `mpcEinde`.
- **Het wapenrek:** een `wapenrekken` in het midden met `rek` speren, en `rugMax: 1`. Wie er een pakt meldt de nieuwe stand
  (`rek`). "Na elke winkel weer vol" komt met stuk 3.
- **Punten en einde:** de host ziet een kill aan een vijand die leefde en nu niet meer (`mpcKillKijk`), telt `MPC.punten`
  plus de reeks (`mpcKill`, met "Double Kill" in beeld) en stuurt de stand mee (`cs`). Het eindscherm (`#mpeind`,
  `mpcEindToon`) met de beste score per keuze van vijanden in localStorage (`mpcEindSleutel`). R bij allebei: opnieuw
  (`mpCoopOpnieuw`, `cnieuw`); Escape: de lobby.

### De versies van de map (dag, avond, nacht, diepe nacht)

The Dye Yard heeft in Co-op vier versies (`MPC_VERSIE`): de **dag** (`stad_dag`, blauwe lucht en zon, geen fakkels), de **avond** zoals hij altijd was (`stad_avond`, geen fakkels),
de **nacht** (`stad_nacht`) met acht fakkels, en de **diepe nacht** (`stad_diepnacht`) met dezelfde fakkels, waar het
donker echt donker is en alleen de fakkels en de ramen er licht in snijden (`donkerGatenNa`, zie `notities/fakkel.md`).

- **De lobby:** onder "Time of day" vinkt de host aan welke versies meedoen (`pvp.inst.coop.licht`, bewaard in `amir.mp`).
  Standaard staan de dag, de avond en de nacht aan en de diepe nacht uit (`MPC_VERSIE.standaard`), want die is echt
  zwaarder. De laatste die aan staat kun je niet uitvinken. Staat er maar een aan, dan wisselt de map niet.
- **Kiezen:** de host kiest bij de start (`mpCoopStart`, ook na R) een willekeurige uit de aangevinkte (`mpcVersieKies`, `mpcVersiesAan`), en aan het begin van ronde
  4, 7, 10 enzovoort (`MPC_VERSIE.elke`, in `mpcHostStap`) een andere dan de huidige. Dat staat los van `winkelNa`.
- **Sync:** `mpcVersieWissel` stuurt `{t: 'cv', v}` naar de gasten; ook elke `cs` draagt `v`, zodat een gast die er een
  mist hem binnen een seconde toch heeft. Een gast begint op de avond tot de host het zegt.
- **De fakkels hangen aan de muren:** per gevel een deel van de muur (van links naar rechts) en een hoogte in Amir
  (`MPC_VERSIE.fakkels`): naast de deuren beneden, op de galerij naast de ramen van de lage huizen en naast het balkon
  van het middenhuis, nooit in een steeg. De x van een gevel schuift mee met de schaal (`stadGevelX`), dus
  `mpcFakkelsStap` zet ze opnieuw uit `stadGevelMaat` als `nowScale()` verandert (elk beeld in `mpCoopStap`).
- **Wisselen tijdens het spel:** alleen `level.lagen` en `level.fakkels`; alles wat van het uitzicht afhangt leest
  `sceneCfg()` per beeld of zit in een cache met de scène in de sleutel. De eerste beelden na een wissel bakken de stad
  opnieuw. De fakkelplaatjes laadt `mpCoopLaad` al vooraf, zodat er geen laadscherm komt.
- **Geluid:** het knetteren van `fakkelGeluid` werkt ook hier; bij een wissel naar de dag of de avond dooft het uit (alleen `MPC_VERSIE.fakkel` heeft fakkels).
- **Testen:** de proef van `tools/mptest.js` kijkt na dat iedereen dezelfde versie heeft en dat ronde 4 bij iedereen een
  andere geeft.

### Anders dan de afspraak

- Op de galerij staat een deur per huis, niet twee: het deursysteem van de stad kent een deur per verdieping per huis (op
  de plek van het raam). Twee vraagt een tweede deurplek in `STAD_DEUR`.
- De elite-garde is niet sneller dan de gewone bandiet; alleen de levens en de dolk zijn anders.

### Wat nog kan

- De gast ziet de vijanden een tikje later dan de host (netwerk plus de speelbuffer). Een slag die bij de host nog loopt,
  kan bij de gast al raken of net niet. Op dezelfde wifi valt het niet op; via het relais (15 per seconde) meer. Stap 2
  (drie spelers) is gebouwd; stap 3, een eigen TURN-server, staat in de wacht (zie "Voor wie" hierboven, en "De netcode"
  in `notities/pvp.md`).
- Met drie spelers draait elke update-functie bij de host tot drie keer per beeld (een keer per groep). Een klok in zo'n
  functie die niet per vijand is, loopt dan ook vaker; tot nu toe is daar niets van te merken.
- Een vijand op de galerij die achter een speler op de straat aan zit, blijft boven staan kijken (regel: geen treden). Zo is
  het bedoeld, maar met een ronde die daardoor niet opraakt moet je naar boven.

## De winkel: hoe het gebouwd is

Het blok `// ---- multiplayer: de winkel en de economie van Co-op (stuk 3) ----` in de HTML, na Co-op.

- **De kamer.** `MP_COOP_LEVEL` heeft een `binnen` met een `winkel` (de toonbank, de marktman, een plank) ver van de straat
  (`MPC_WINKEL_KAMER`, van -20000 tot -21700), zonder deur naar buiten (`gevel: null`), en een houten plafond (`zwevers`).
  Het gewone systeem van "binnen" doet de rest: de camera, de muren, E bij de toonbank (`binnenE` opent `winkelUIOpen`).
- **Erheen.** Is de ronde op (`mpcHostStap`) en is het rondenummer een veelvoud van `winkelNa`, dan wacht de host eerst
  `MPC_WINKEL_WEG.wacht` (3 s) op straat (fase `naarWinkel`), stuurt dan `winkel` en roepen allebei `mpcWinkelIn` aan: de fase `winkel` (`C.inWinkel`), wie dood was staat op met 1 leven, de revive-ton en
  het symbool zijn weg, ieder krijgt zijn speren terug (`mpcSperenTerug`) en een trage fade (`stadTrapFade` met `MPC_WINKEL_WEG.fade`, ook terug de straat op) zet
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
- **De Gris-gris** (`GRISGRIS`, `grisGrisKans`, `grisGrisVang`): het beschermende amulet uit de Sahel, drie trappen in
  `koop.amulet` (10%, 20%, 30% voor 40, 75 en 110 goud). Een item met een lijst als `prijs` (Extra life en de Gris-gris)
  telt in `koop[k]` hoe vaak je het kocht, en een lijst als `uitleg` geeft per trap de tekst. `hurtPlayer` gooit de kans na
  de rol, het schild en de stokken: gevangen is de klap er wel (terugduw, `invuln` zodat dezelfde aanval niet elk beeld
  opnieuw gooit), maar zonder leven en zonder rode flits, met een klokje en "Warded" in de banner. Ieder gooit zelf: een
  klap op een gast komt als `au2` bij zijn eigen `hurtPlayer`. De proef (`tools/mptest.js --proef`) koopt hem drie keer bij
  de host en kijkt na dat gevangen geen leven kost en gemist wel.

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

## Drie spelers: de ster (stap 2 van de netcode)

Co-op is voor twee of drie spelers (`PVP.max`), het Duel voor twee. De host blijft denken voor de vijanden en is het
middelpunt van een ster: hij heeft een verbinding per gast, een gast alleen een naar de host.

- **Slots.** De host is slot 0, de gasten 1 en 2 (het laagste vrije). Wie inbelt terwijl de lobby open is en er plek is,
  krijgt `{t: 'welkom', mij}` en opent pas dan de lobby (`pvpNieuweGast`, `pvpGastErbij`); anders `{t: 'vol', r}` met de
  reden (vol, of het potje loopt al). `pvp.spelers` is wie er meedoet, `pvp.peers` per slot de lijn met zijn snelle kanaal
  en `vAk`, `pvp.nets` per afzender de speelbuffer en de klok, `pvp.anders` per slot de andere Amir (`g` gebufferd voor
  het beeld, `nu` de nieuwste voor de vijanden; `pvpAnderNu(p)`, `pvpAnderen()`).
- **Berichten.** Elk bericht draagt het slot van wie het maakte (`p`). De host zet het zelf op wat binnenkomt (een gast
  spreekt niet voor een ander) en stuurt door wat de andere gast ook moet weten (`MP_DOOR`: de stand `s` over het snelle
  kanaal, de broek, het rek, het opgepakte symbool, Ready in de winkel, R na het einde). Een bericht voor een speler gaat met
  `pvpZendAan(p, o)`: de host rechtstreeks, een gast via de host met `naar` (zo gaan `au2`, `buit` en Give 5 gold naar
  precies die speler). De doorgestuurde stand van de andere gast draagt zijn eigen klok, dus elke afzender heeft een eigen
  speelbuffer; hij loopt een sprong verder achter dan de host (nagemeten: zo'n 320 tegen 210 ms bij 60 ms per sprong).
- **De vijanden.** `mpcDoel` geeft het slot van de dichtstbijzijnde levende speler (met de marge `MPC.wissel`); `mpcUpdate`
  draait de update-functie een keer per groep, de host eerst en dan per gast met diens stand (`mpcWisselIn(p)`). De
  vijandstand gaat als een bericht naar alle gasten; de delta telt vanaf het laagste wat een van hen bevestigde.
- **De revive** (`mpcDodenStap`): per dode een eigen revive-ton (`C.reviveTon[slot]`), bij de levende speler die het dichtst
  bij zijn lijk staat, en een eigen symbool (`C.symbolen`, met `voor`). Met drie spelers staat boven het symbool de kleur van
  wie ermee opstaat. Wie niet meer dood is (of weg) verliest zijn ton en symbool. Game over pas als iedereen dood is. De camera
  van een dode volgt de dichtstbijzijnde levende teamgenoot (`mpCoopCam`), of wie hij met de pijlen kiest.
- **Ready en goud voor iedereen.** De winkel gaat pas dicht als iedereen Ready is (`C.wkKlaar` per slot, de banner zegt
  "1 of 2 teammates ready"), R na game over pas als iedereen R drukte (`mpCoopRematchKijk`), ronde 1 wacht tot iedere gast
  geladen is (`C.klaarVan`). Het goud van een kill en van een ronde krijgt iedereen (`mpcGoudIedereen`). Give 5 gold heeft
  met twee teamgenoten een knop per teamgenoot (`wkc_geef_<slot>`).
- **De derde.** Een derde broekkleur (turkoois) en startplek (`PVP.starts[2]`, -1150, in het midden), en een derde plek in de
  winkelkamer (`MPC_WINKEL_KAMER.plek`).
- **Het relais per sid.** Een gast stuurt naar `/h/<sid>`, de host luistert op `/h/+` en stuurt naar `/g/<sid>`: elke gast
  zijn eigen onderwerp. De host heeft een client voor alle gasten (`pvpRelayConn` met `gedeeld`).
- **Weg.** Gaat een gast weg (Leave, of `PVP.stilte` niets gehoord), dan meldt de host `{t: 'weg', wie}` en spelen de andere
  twee door (in de lobby blijven ze staan); is er niemand meer, dan zoals eerst. Gaat de host weg, dan is het voor iedereen
  uit.

### Anders dan de afspraak, of zelf ingevuld

- **Het Duel blijft een tegen een.** Met drie spelers in de lobby mag Start niet in Duel ("A duel is for two players").
- **Wie dood de revive-ton krijgt:** bij de levende die het dichtst bij het lijk staat, niet bij een vaste speler.
- **Een gast die weggaat:** de rest speelt door. Een nieuwe kan pas weer bij in de lobby, niet midden in een potje.

### Voorstel: zwaardere rondes met drie man (nog niet gebouwd)

Met drie spelers is elke ronde nu even groot als met twee, terwijl er een derde speer, een derde revive en meer goud bij
komt. Het voorstel, in volgorde van belang:

1. **Meer vijanden per ronde:** het aantal uit `mpcRonde` keer 1,5 met drie spelers (naar boven afgerond), zodat ronde 1
   met de standaard 1 vijand er 2 heeft en ronde 5 er 8 in plaats van 5.
2. **Meer tegelijk en sneller binnen:** `MPC.tegelijk` van 10 naar 14 en `MPC.tussen` van 1,5 naar 1,1 s, zodat de extra
   vijanden niet alleen de ronde langer maken maar ook de druk verhogen. `MPC.boven` van 5 naar 6.
3. **Vaker de moeilijke versie:** bij Both 60 in plaats van 50 procent de moeilijke.
4. **De revive duurder:** met drie spelers komt de revive-ton na 25 in plaats van 20 s, want er staan er nog twee rechtop.
5. **Goud gelijk per persoon** (geen verandering): ieder krijgt al evenveel, dus het team krijgt vanzelf anderhalf keer zoveel.

Alles als getallen in `MPC` met een tweede waarde voor drie man (bijvoorbeeld `MPC.drie = { keer: 1.5, tegelijk: 14, ... }`),
zodat het met twee spelers precies blijft zoals nu.

## De Co-op episode (gebouwd, 18-11-2026)

`COOPEP_1`, `COOPEP_2`, `COOPEP_3`, `COOPEP_LEVELS`, `MPC_EP`, `MPC_EP_SOORT`, `mpEpNieuw`, `mpEpHostStap`, `mpEpAllenBijEind`,
`mpEpLevelKlaar`, `mpEpVolgende`, `mpEpBijFakkels`, `mpEpReviveX`, `mpEpNaast`, `mpEpEindToon`, `mpcEpSpawnGasten`

De derde modus in de lobby, **Co-op Episode** (`modus: 'ep'`, voor twee of drie spelers). Drie savannelevels na elkaar, van
makkelijk naar moeilijk, op verzoek van de opdrachtgever ("alleen uit als je samen het eindpunt bereikt", "revive met een
tonnetje op verschillende plekken"). Bij Map kiest de host het level waar het team begint (`MP_KAARTEN.ep`, id '0' tot '2').

- **De levels.** Gewone leveldefinities met de standaard voor een nieuw level (`view`, `hpBalk`, `slangEenKlap`, `zicht`,
  `camera`, `rand`, `speerInHand`), in de reeks `COOPEP_LEVELS`, zodat `levelcheck.py` ze nakijkt. Zonder `sneak`: de
  sluipaanval is in Co-op uit (de regie bevriest het beeld). Zonder doornbossen: wie de stokken heeft kan die niet kappen.
  `mpCoopStart` zet er net als op de map van Survival `stof`, `rugMax: 1` en de reeks van het team in.
  1. **The Long Grass** (makkelijk, `vlakte`): zandslangen, een schorpioen, twee hyena's, drie bandieten, twee keien.
  2. **Broken Ground** (middel, `hoogland`): een terras met een kruisboogschutter erop, twee ravijnen (220 en 240) om over te
     springen, twee makkelijke schildbandieten, bandieten met een dolk.
  3. **The Last Ridge** (moeilijk, `schemer`): een kruisboog op een terras, knock en zwart, een normale schildbandiet,
     fosfor, drie hyena's, een gewone kooiman (`duel: false`, geen geënsceneerd duel) en een meelman, twee ravijnen en
     aan het eind een elite-garde met vijf levens.
- **Alles van Co-op Survival werkt hier:** de host denkt voor de vijanden, `mpcUpdate`, de revive-ton en het symbool, de
  camera van een dode, de lijken. Geen rondes, geen winkel en geen goud (`mpcKill` geeft in de episode geen goud, de HUD
  zegt "Level 1 of 3   Score").
- **De spawns komen ook bij een gast.** De spawns van een level kijken alleen naar `world` (de lus in `updateSnakes`). Bij
  de host draait `mpcEpSpawnGasten` daarom per levende gast `updateSnakes` nog een keer met de stand van die gast
  (`mpcWisselIn`), dt 0 en een lege slangenlijst; wat dan komt, komt bij hem. `mpEpTag` geeft elke vijand uit een spawn
  zijn `mpSoort`, zodat hij meetelt voor de punten.
- **Het eind.** Bij de fakkels speelt `winLevel` niet uit: daar zegt `mpEpBijFakkels` alleen "Wait at the torches for your
  teammate". De host kijkt elk beeld of iedereen leeft en binnen `MPC_EP.eind` van de fakkels staat (`mpEpAllenBijEind`,
  een gast uit zijn nieuwste stand). Dan "Level complete" (`epklaar`, iedereen `godMode`), en na `MPC_EP.na` seconden het
  volgende level (`epnaar` met het level, `mpCoopStart(i)`). Elk level begint iedereen weer met 3 levens.
- **De revive-ton** komt bij de levende die het dichtst bij het lijk staat, waar dat ook is (`mpEpReviveX`): op zijn
  hoogte, niet in een ravijn, niet op een andere ton, binnen het level; lukt dat niet op zijn hoogte (hij staat op een kei),
  dan op de grond. Wie opstaat, staat naast wie het symbool pakte, ook niet in een ravijn (`mpEpNaast`).
- **De score** is van het team en gaat mee naar het volgende level (`mpEpNieuw` met `door`). Game over: R (iedereen)
  speelt hetzelfde level opnieuw, met de score, kills en tijd van het begin van dat level (`s0`, `k0`, `t0`). Na het
  laatste level het eindscherm **Episode complete!** (`mpEpEindToon`, de beste score in `amir.coopEpBest`), en R begint
  weer bij level 1 met score 0.
- **Testen:** `node tools/mptest.js --ep` (met `--spelers 2` voor twee) loopt het na: een spawn bij een gast, de host
  alleen bij de fakkels, een revive midden in het level, door naar level 2 met de score, game over en R, en het slot.

## Co-op solo (gebouwd, 18-11-2026)

De vierde keuze onder Sandbox (`btnsbcoop`): Co-op Survival, of de Co-op episode, voor een speler, zonder verbinding
(`MP_SOLO`, `mpSoloOpen`, `pvp.solo`). Geen eigen arena naast Co-op (regel 4): `mpSoloOpen` maakt het `pvp`-object zoals
`pvpVerbonden` dat voor een host doet, maar zonder peers en zonder `pvpNetStart`, en opent de gewone lobby. Alles daarna
is de code van Co-op zelf; elk bericht gaat naar niemand.

- **Wat vanzelf klopt met een speler:** ronde 1 wacht op geen gast (`pvpGasten()` is leeg), Ready in de winkel is alleen
  de jouwe (`mpcWinkelKlaar`), R op het eindscherm begint meteen opnieuw, en wie doodgaat is iedereen, dus meteen game over
  (`mpcDodenStap`): geen revive-ton.
- **De lobby solo** (de klasse `solo` op `#mplobby`, `mpsolo` op `#start`): geen Duel, geen Ready, geen spelerslijst of ping,
  geen "Waiting for the other players" onder de broek, de titel `MP_SOLO.titel`, en Start kan altijd (behalve zonder
  vijanden). De broek en het wapen kies je zoals in Multiplayer.
- **Bewaard apart:** de instellingen gaan naar `amir.mpsolo` (`MP_SOLO.sleutel`), niet naar die van de host (`amir.mp`).
- **Terug:** Escape geeft het pauzemenu en Terug brengt je naar deze lobby (`mpNaarLobby`); Leave the lobby gaat terug naar
  het Sandbox-scherm.
- **Highscore:** dezelfde als in Co-op, per keuze van vijanden (`mpcEindSleutel`); solo en samen tellen in hetzelfde lijstje.

## Testen

`node tools/mptest.js` speelt Co-op met drie vensters (de host en twee gasten, `--spelers 2` voor twee) en een nagebootste
ster: de host een verbinding per gast, Node geeft de berichten door. `--proef` loopt de vaste stappen na (de lobby met drie
slots, drie broeken, een vierde die geweigerd wordt, Start pas als iedereen Ready is, geen Duel met drie; in het spel drie
startplekken en iedereen ziet de anderen, een ton breken als gast, een treffer van de gast, een vijand die achter de tweede
gast aan gaat en hem raakt, de winkel met kopen, Give 5 gold aan de host en via de host aan de tweede gast, Ready van
iedereen en terug, Full Circle rondom voor en achter, twee doden met elk een revive-ton, de camera en de banner van een dode,
een revive voor een van de twee, iedereen dood, het eindscherm, R pas bij iedereen, Escape, en een gast die de lobby verlaat)
en meldt per stap OK of FOUT. `--duel --spelers 2` loopt het Duel na. Zonder `--proef` lopen simpele spelers op de vijanden
af, met `--taai` zonder dood te gaan, `--sterf gast,gast2` om de revive te zien, `--soorten bandiet,slang` voor een paar
soorten en `--shots map` voor plaatjes. `--net` meet per venster hoe goed elke andere Amir zijn echte baan volgt (per speler,
want de doorgestuurde gast loopt een sprong verder achter) en per gast de vijanden.


Voor de lobby is eerder een los script gebruikt met een nagebootste `Peer` die berichten tussen twee
vensters in een browsercontext doorgeeft via een `BroadcastChannel` (Host, Join, lobby, instellen, Ready, Start, Escape
naar de lobby, Leave). De echte PeerJS-server is vanuit de cloud van Claude niet te bereiken.
