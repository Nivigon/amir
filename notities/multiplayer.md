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
| Shop and gold | uit | vinkje: de winkel van het Duel (`pvp.dw`, zie "De winkel van het Duel" in `notities/pvp.md`); de rijen hieronder staan er alleen met het vinkje aan (`winkel: true` in `MP_DUEL_RIJEN`) |
| Starting gold | 100 | 0 tot 300, per 10 (`goud0`) |
| Shop before round 1 | aan | eerst allebei naar de winkel (`winkelEerst`) |
| Shop between rounds | After every round | Never, of na elke 1, 2 of 3 rondes (`winkelNa`) |
| Gold at each shop | 50 | 0 tot 200, per 10, bij elke winkel tussen de rondes (`goudErbij`) |

Het wapen (speer of stokken) kiest ieder zelf in de lobby, ook voor het Duel (zie "Het wapen"). De kit in het Duel is die van
Co-op: stof in de ogen met de speer, de grondklap met de stokken (5 s afkoeling, `GK.koelCoop`). Zie "De kit" in `notities/pvp.md`.

### Co-op-instellingen

| instelling | standaard | bereik |
| --- | --- | --- |
| Enemies in round 1 | 1 | 1 tot 6 |
| Extra enemies per round | 1 | 1 tot 3 |
| Shop after every | 3 rondes | 2 tot 6 |
| Time between rounds | 10 s | 5 tot 30 |
| Spears in the rack | 4 | 0 tot 4 |
| Gourd chance in a barrel | 30% | 0 tot 100, per 10 |
| Starting gold | 0 | 0 tot 400, per 10: ieder begint met zoveel in zijn beurs (`goud0`, in `mpCoopStart`) |
| Start in the shop | uit | vinkje: voor ronde 1 eerst allemaal naar de winkel; de host zet `fase: 'naarWinkel'` (`winkelEerst`) |
| Enemies | alles aan | per soort Off/On, of Off/Easy/Hard/Both |

De soorten en hun twee versies (`MP_SOORTEN`):

| soort | makkelijk | moeilijk |
| --- | --- | --- |
| slangen | zandslang | zwart, knock en fosfor |
| bandiet | gewone bandiet | elite-garde, en die is in Co-op echt moeilijker: 5 levens, altijd een dolk die hij eerst werpt, iets sneller |
| schildbandiet | `niveau: 'makkelijk'` | normaal |
| kooiman | gewoon (`duel: false`) | het duel |
| kruisboogbandiet | zonder hoorn | met hoorn |
| schorpioen, hyena, goudaapje, zweepman | een vinkje | |

Bazen (panter, baviaan, Nyundo, Murghtaan) staan er niet in (regel 12, en de opdrachtgever wil ze voorlopig uit).

### De broekkleur (gebouwd)

`MP_BROEK`, `mpBroekZet`, `mpBroekVrij`, `mpBroekAnder`, `mpBroekStart`, `pvp.broek`

Links naast de lobby (`#mpamir`, in `#mplinks`, een kind van `#start`, zichtbaar met de klasse `mplobby` op `#start`) staat je eigen Amir
in de idle, met pijltjes ernaast, zoals de broekkeuze van Test 73 (`BROEK`, `broekBeeld`). De lijst is het eigen paars van
Amir (geen lapje) plus `BROEK.kleuren`. Ieder kiest zelf, ook een gast; `{t: 'broek', id}` gaat naar de anderen bij het
openen van de lobby en bij elke wissel (een gast via de host). Een kleur die een ander draagt slaan de pijltjes over. Kiezen
twee tegelijk dezelfde, dan houdt het laagste slot hem (de host eerst) en schuift de ander door naar de eerste vrije
(`mpBroekAnder`). Standaard is de host paars, de eerste gast rood en de tweede turkoois (`MP_BROEK_STANDAARD`); de laatste
keuze staat op het apparaat (`amir.mpbroek`). In het spel geeft `broekNu` de eigen kleur zolang `pvp`
loopt, en `pvpTeken` tekent de ander in de zijne. Geldt in Co-op en in Duel, want de lobby is dezelfde.

### De naam en het team in de lobby (gebouwd, 19-11-2026)

`MP_NAAM`, `mpNaamZet`, `mpNaamAnder`, `mpSpelerNoem`, `mpNamenZien`, `mpNaamTeken`, `mpTeamToon`, `mpTeamTeken`, `pvp.naam`, `#mpnaam`, `#mpteam`

- **De naam.** Bovenaan naast de lobby (`#mpnaam`, hooguit `MP_NAAM.max` 14 tekens, `mpNaamSchoon` haalt stuurtekens en `<>`
  weg) typt ieder zijn naam, bewaard op het apparaat (`amir.mpnaam`). Net als de broek en het wapen: `{t: 'naam', n}` naar de
  anderen (in `MP_DOOR`, een nieuwe gast krijgt de namen in `pvpGastErbij`). Zonder naam heet je naar je broek.
  `mpSpelerNoem(p, klein)` is hoe een speler heet in elke melding (weg, Give 5 gold, de revive, de camera van een dode).
- **De dobbelsteen** (`#mpnaamrol`, `mpNaamRol`, `MP_NAAM_ROL`): naast het naamveld geeft een klik een stoere naam uit een vaste
  lijst van 50, van Afrikaanse koningen, krijgers en koninginnen (Shaka, Sundiata, Nzinga, Menelik, Taharqa) en woorden voor
  kracht en roofdieren (Jabari, dapper; Simba, leeuw; Jomo, brandende speer; Gamba, krijger; Hondo, oorlog). Nooit je eigen
  naam of een die een ander in de lobby al heeft. Elke naam past in `MP_NAAM.max`.
- **Boven het hoofd.** `pvpTekenEen` tekent boven het pijltje en de hartjes een naambordje (`mpNaamTeken`): Archivo 800, licht
  met een zwarte rand, op een donkere pil met een streepje in de broekkleur (`MP_NAAM.kleur`); van een dode half doorzichtig.
  Je eigen naam zie je niet. In Co-op en in het Duel.
- **Namen zien of niet.** Het vinkje **Show names above heads** (`#mpnamen`, `amir.mpnamen`, standaard aan) is per speler en
  gaat niet over de lijn. Solo is het weg.
- **Het team.** In de lobby onder de spelersregel (`#mpteam`, niet solo) per speler een heldenkaart (de opdrachtgever koos
  uit drie varianten, 19-11-2026): zijn Amir in de idle in een gloed van zijn broekkleur (`--kl`, uit `MP_NAAM.kleur`), met de
  stokken het staande stokframe (wie rechts van jou staat kijkt naar links), de naam in hoofdletters, broek en wapen, en
  onderaan een strook Host, Ready of Not ready. Getekend in de lus van het
  voorbeeld (`mpTeamTeken` in `mpBroekStart`), opnieuw opgebouwd alleen als er iets verandert (`mpTeamSleutel`).
- **De indeling: team links, instellingen rechts** (de opdrachtgever koos uit drie mockups, 23-11-2026). Links staat het
  hele team op een rij (`#mplinks`, `#mpteamrij`): je eigen vak (`#mpamir`) groot, met onderaan je eigen strook Host,
  Ready of Not ready (`#mpikstatus`), en ernaast de kaarten van de anderen (`#mpteam`, je eigen kaart staat er niet meer
  in), en zolang er plek is een lege kaart **Open slot** met de code (`.mpkaart.leeg`; in Duel tot twee spelers). De ping
  staat eronder. Rechts alleen de instellingen, zonder grote titel en zonder eigen scrollbalk: Co-op Survival in twee
  kolommen (`.mpkol`: links de regels en het licht, rechts de vijanden). Op 1280x720 past alles zonder scrollen; het
  paneel centreert met `safe center`, zodat te hoge inhoud nooit meer boven uit beeld valt.
- **Live meekijken.** Elke klik van een ander op zijn broekpijltjes of wapenknop komt meteen over (`broek`, `wapen`). Zijn
  kaart licht dan even op in zijn kleur (`.wissel`, `pvp.teamFlits`) en zijn Amir vloeit over van de oude naar de nieuwe
  keuze (`mpTeamWissel`, `pvp.teamOud`, net zo lang als je eigen voorbeeld, `BROEK_VB.over`).
- **Even groot met de stokken.** Het stokframe heeft boven het hoofd meer lucht dan de idle, maar dezelfde pixels per Amir;
  `mpAmirVak` knipt het even hoog als de idle om het lijfmidden, zodat Amir met de stokken net zo groot staat (in het
  eigen voorbeeld en op de kaarten, allebei via `mpAmirTeken`). Ready zag eerst alleen de host; nu stuurt hij `{t: 'klaarStand', k}` na elke Ready, en een
  `lobby`-bericht zet hem bij de gasten weer leeg.

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
- **Lion Claw sticks (19-11-2026):** na Hardwood sticks (`eis: 'hout'`, 80 goud) de klauwstokken: de slag, stapslag en
  slag 2 kosten een heel leven (`STOK.schadeKlauw`), en Amir heeft de witte botstokken met de leeuwenklauw in elke set
  (`STOK.klauwDir`, pas geladen bij de koop: `stokKlauwLaad`, `stokUitBank`, `stokSlipNu`). `stokHoutNu` geeft nu 0, 1
  (Hardwood) of 2 (Lion Claw), en dat getal gaat als `hw` mee met een treffer van een gast. De teamgenoot ziet de klauwstokken
  vanzelf, want het beeld gaat als pad over. Een `eis` in de winkel noemt nu de naam van wat eerst moet ("Buy Hardwood sticks first.").
- **Gold King sticks (19-11-2026):** de keuze naast Lion Claw (`sluit` in `MPC_WINKEL`: heb je de een, dan "You chose ...", ook
  80 goud na Hardwood). Slaat als Hardwood (0,75), en een stokslag op het schild van de schildbandiet haalt met kans
  `STOK.goudSchild` (0,5) een stand extra af (`hitSchildman`, met de crit-ster). `stokHoutNu` geeft 3. De stokken uit
  `STOK.skins.goud` (zwart met het gouden leeuwenkopje), en de kwast van gouden manen hangt als slip aan de knoop.
- **De Pathfinder Spear (22-11-2026):** een speerartikel (`speer: true`, 40 goud, een per speerplek, `koop.pathfinder` telt hoeveel, `mpcWinkelHeb` is uitverkocht bij 1 + `RUG_MAX`), zie "de Pathfinder
  Spear" in `notities/speer.md`. De host markeert: een treffer van een gast draagt `pf` in `mh` (zijn worp met een
  Pathfinder-speer), `mpcTrefferVanGast` zet dan `prooiGast`, en `prooiRaak` stuurt `{t: 'prooi', a, id}` naar de anderen.
  Alleen de host vertraagt (`prooiTraag` doet niets bij een gast: daar komen de plekken van de host).
- **Het zijpaneel van de winkel (22-11-2026):** een klik op een artikel kiest het (`mpcKeus`, een gouden rand) en het paneel
  `#wkinfo` laat de naam, de sfeertekst (`sfeer`, met de bron `bron` schuin eronder), de uitleg en **Buy** zien
  (`mpcInfoToon`); een dubbelklik koopt meteen. Sfeertekst staat nu bij de Pathfinder Spear en het gif; de inventory
  laat die van het gif ook zien (`INV_DING.gif.sfeer`, `#invsfeer`). De winkel buiten Co-op koopt nog met een klik.
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
- **Elkaar niet raken:** geen steek, zwaai of speer van de een raakt de ander. Een speer van de ander in de vlucht zie je niet, maar wel als hij neerkwam (zijn `jav` uit `s`, als `st` niet `vlucht` is) en zijn losse speren op de grond (`ls`, `pvpLosZend`, `pvpLosTeken`, zie "Wat er over de lijn gaat" in `notities/pvp.md`). Alleen beeld: oprapen kan alleen wie hem gooide. `tools/mptest.js --proef` kijkt na dat de host en de tweede gast een losse speer van de gast zien en dat hij weer weg is als de gast hem opraapt.
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
- **Punten (teamtotaal):** slang, schorpioen, goudaapje, hyena 10; bandiet, zweepman 15; kooiman, kruisboog 20;
  schildbandiet 25. De moeilijke versie 5 extra. Een multikill 10 extra per kill in de reeks.
- **Eindscherm:** alleen het team: score, de ronde waarin het eindigde, tijd. Een highscore op het apparaat, per keuze van
  vijanden, en solo apart van een team (`amir.coopBest.solo.`, in de episode `.solo` achter de sleutel). Logt de speler
  (tester of designer), dan komt de high score van Survival uit de Sheet, per team en solo op je naam (zie
  `notities/highscores.md`); de lokale is dan alleen het vangnet zonder verbinding, met "(this device)". De regel eronder
  zegt altijd waar je staat (`mpcHighRegel`): **New high score!** (met de vorige erbij), gelijk, de high score die blijft
  staan, of nog geen. In een episode telt de high score alleen als je hem uitspeelt; game over zegt dat ook. Solo staat er
  Score in plaats van Team score en geen "both press".
- **Eerst de val, dan het eindscherm:** is iedereen dood (en komt er geen revive), dan wacht `mpcDodenStap` tot de val
  (NEER) uitgespeeld is, plus `NEER.scherm` en `MPC.eindRust` (`mpcEindWacht`, `C.eindOm`). Solo telt het vanaf hoe ver
  de eigen val is (in een ravijn ligt hij meteen), met een team de langste val.

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

**Afspraak (22-11-2026): een status of animatie op een vijand is op elk scherm te zien.** Wat een speler een vijand aandoet
(stof in de ogen, een stun, gif, prooi, wankelen, opwippen, de draaislag) moet bij iedereen hetzelfde staan. De regel: zet
een status altijd bij de host, als veld op de vijand, en laat de stand (`mpcStandZend`) hem naar de rest brengen. Een gast
zet niets op zijn eigen kopie: hij stuurt een bericht naar de host (zoals `mh` voor een treffer en `stofR` voor het stof,
`mpcStofVanGast`) en speelt lokaal alleen beeld en geluid af. En een klok die zo'n status laat aflopen hoort niet achter een
vlag van de host zelf (zijn wapen, zijn level): de stun van de stokken telde eerst alleen af als de host ook stokken had,
en dan bleef een bandiet van een gast voor altijd staan. Een nieuw veld begint niet met `mp` of `_`, want die gaan niet mee.

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
  is (`mpcStandLees`, vanuit `mpcVolgStap`); daarna staat elke vijand tussen dat bericht en het volgende in (`mpX0`). Kogels, dolken en gif (`los` in `MPC_LIJSTEN`) komen een keer over en vliegen daarna bij de gast
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
- **Samen beginnen** (`mpLaadVast`, `mpLaadLos`, `mpLaadReset`): een potje (Co-op, de Co-op episode, elk level daarvan,
  en het Duel) begint pas als elke laptop geladen is. Tot dan blijft bij iedereen het laadscherm staan met "Waiting for your
  teammate..." (laadStap vraagt het na het laden en bakken); een gast die klaar is stuurt `geladen`, de host telt
  (`pvp.geladen`) en stuurt `los` als hij zelf en elke gast klaar zijn, dan gaat het laadscherm overal tegelijk weg. Vroeger
  wachtte alleen ronde 1 (`cklaar`), en liep wie eerst geladen was al rond. Tijdens het laden stuurt ieder `hb`, anders
  verbreekt `PVP.stilte` het potje. `tools/mptest.js` houdt bij de start de laatste gast kunstmatig aan het laden en kijkt
  dat de host wacht.
- **De rondes** (`mpcHostStap`, alleen de host): dan `wacht` (de pauze, met "Round N in .. s") en `golf`: de rij uit
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
- **Dood en revive:** wie dood is ligt (`mpcLig`, het plaatje plat om zijn voeten, want het spel heeft geen doodspose; op een
  galerij, dak of trapbalkon ligt hij `MPC_LIG_TIL` hoger, op de vloer in plaats van half door de planken, `mpcLigHoog`), het
  dood-scherm komt niet, en de camera volgt de ander (`mpCoopCam`, in de hoofdlus de eerste keus van de camera, met `camVast`
  uit: anders zette de meekijkende camera hem elk beeld terug op het lijk en schudde het beeld). Pijl links en rechts (ook de
  stick op een telefoon) wisselen tussen je eigen lichaam en elke levende teamgenoot (`mpcKijkStap`, `mpcKijkNu`,
  `pvp.coop.kijk`); zonder keuze de dichtstbijzijnde, en onder de banner staat naar wie je kijkt (`#mpkijk`). Staat de teamgenoot ver weg of in een
  andere kamer (een huis of de winkel in, die liggen ver van de straat), dan schuift de camera niet door de lege wereld maar
  gaat het beeld even op zwart en staat hij daarna bij hem (`MPC_KIJK_FADE`, `mpcKijkCam`, `mpcKijkFadeTeken`); in een huis klemt
  de camera op de kamer van de teamgenoot, niet op die van het lijk. Na `MPC.reviveNa`
  zet de host een revive-ton (drie treffers, "REVIVE" erop, `mpCoopTeken`) bij de levende; breekt hij, dan valt het symbool
  (`sym`), en wie het aanraakt (`mpcSymboolStap`) laat de ander naast zich opstaan met 1 leven (`symPak`, `mpcOpstaan`).
  Allebei dood: `mpcEinde`.
- **Het wapenrek:** een `wapenrekken` in het midden met `rek` speren, en `rugMax: 1`. Wie er een pakt meldt de nieuwe stand
  (`rek`). "Na elke winkel weer vol" komt met stuk 3.
- **Punten en einde:** de host ziet een kill aan een vijand die leefde en nu niet meer (`mpcKillKijk`), telt `MPC.punten`
  plus de reeks (`mpcKill`, met "Double Kill" in beeld) en stuurt de stand mee (`cs`). Het eindscherm (`#mpeind`,
  `mpcEindToon`) met de beste score per keuze van vijanden in localStorage (`mpcEindSleutel`). R bij allebei: opnieuw
  (`mpCoopOpnieuw`, `cnieuw`); Escape: de lobby. Midden in Survival start R van de host (solo of samen) het potje meteen
  opnieuw voor iedereen; een gast krijgt "Only the host can restart". De Co-op episode houdt R alleen na het einde.

### De host klikt weg (gebouwd, 19-11-2026)

De lus van het spel hangt aan `requestAnimationFrame`, en dat zet de browser stil zodra het tabblad verborgen is (ander
tabblad, venster geminimaliseerd of helemaal bedekt). In Co-op denkt de host voor de vijanden en de rondes, dus dan stond
het spel voor iedereen stil. Nu tikt er bij de host een kleine Web Worker (`ACHTER`, `achterZet`, `achterTik`; zijn timers
remt de browser niet af, anders dan `setTimeout` op de pagina) 30 keer per seconde, en zolang de pagina verborgen is draait
elke tik een beeld van de lus. Komt de host terug, dan neemt `requestAnimationFrame` het weer over. `lusVraag` (en
`lusRaf`) zorgt dat er altijd hooguit een beeld aangevraagd is, anders liepen er na terugkomst twee lussen naast elkaar.
Alleen de host van Co-op (Survival en de episode); een gast die wegklikt staat zelf nog stil, en speelt de rest gewoon door.
Ook het geluid van de host loopt door. De verbinding valt in geen van beide gevallen weg: de ping (`pvpNetStart`) houdt
`PVP.stilte` op afstand. Gemeten in Chromium met een nagebootst verborgen tabblad (geen `requestAnimationFrame`): 30
beelden per seconde, en na terugkomst één lus.

**De ping liep op als de host wegklikte (gerepareerd, 20-11-2026).** De worker tikte 30 keer per seconde, ook als het vorige
beeld nog niet klaar was. Op de achtergrond duurt een beeld langer, dus de tikken stapelden zich op in de wachtrij van de
pagina, en een ping van de gast stond achter al die tikken: de ping bij de gast liep op tot 5000 ms en verder (nagemeten:
15.000 ms na 25 s weg). Nu stuurt de worker pas een nieuwe tik als `achterTik` de vorige beantwoord heeft (een bericht
terug na het beeld). Nagemeten in Chromium onder xvfb (het venster van de host bedekt en `document.hidden`): de ping
blijft rond 40 tot 100 ms, de host draait 26 beelden per seconde. Een gast die wegklikt had dit niet: zijn lus staat
stil en de ping wordt meteen beantwoord.

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

### De lag gemeten (23-11-2026)

`node tools/mptest.js --profiel` meet per venster de beeldtijd, ons eigen JS per beeld, haperingen, de bytes per seconde
over de lijn (per soort bericht) en een CPU-profiel; met `--epkaart 0` of `--epkaart b3` een level van een Co-op episode.
Gemeten in headless Chromium zonder grafische kaart (alles software, drie of twee vensters op vier kernen), dus de
absolute getallen zijn lager dan op een laptop; de verhoudingen zeggen wel iets.

- **Het netwerk is het probleem niet.** De host stuurt met twee gasten zo'n 23 KB/s (per gast `s` 29/s van 290 B en `v`
  14/s van 170 B, en een sleutelbericht van 1 KB per seconde), een gast 4 KB/s.
- **De vijanden zijn het probleem niet.** De AI (ook drie keer per beeld met drie spelers) komt in het profiel niet boven
  de 0,4%. Bijna alle tijd gaat naar het tekenen.
- **De stad is zwaar, de savanne licht.** Met twee vensters: Co-op 1 (savanne) 54 beelden/s, Ambush 1 45, Co-op 3 en Ambush
  4 tot 7 rond de 35, Ishmul 16, The Dye Yard met drie vensters 20. De savanne bakt de verte in een paar platen
  (`vertePlaten`); de stad tekent per beeld de lucht (`verteLucht`, in de A/B zo'n 3 ms) en de verre stad (`stadAchter`,
  zo'n 7 ms, vooral het vullen van drie brede stroken en het paleis over het hele scherm). De stroken worden niet steeds
  opnieuw gebakken (0 keer in 670 beelden, ook met de meekijkende camera).
- **Waar het profiel de tijd neerlegt:** de browser spoelt zijn tekenwerk door op een `restore` of `fillRect` (in
  `drawVoorgrond`, `drawVeg` of de dim van `sceneAchter`), dus die functies staan bovenaan zonder dat ze zelf duur zijn.
  Vergelijk daarom de beeldtijd met een laag uit en aan (een A/B), niet de JS-tijd.
- **Gerepareerd:** `broekBeeld` en `mkLosBeeld` bouwden elke Amir (de outfit, de speer, de lapjes) elk beeld opnieuw op,
  ook als hij nog op hetzelfde animatieframe stond; nu onthoudt het doek waarmee het gevuld is (`BB_MEMO`, `_bbMemo`).
  Niet met gif of de Pathfinder, die veranderen per beeld. Nagemeten: 321 van 321 beelden gelijk aan een vers opgebouwd
  doek. En het naambordje (`mpNaamTeken`) wordt een keer gebakken (`mpNaamBak`) in plaats van elk beeld tekst met een
  omlijning. Samen ruim een beeld per seconde erbij in de meting van The Dye Yard.
- **Lag die met de rondes oploopt (gerepareerd, 23-11-2026):** met drie spelers werd Survival rond ronde 18 traag. Oorzaak:
  `updateScorps` werkt ook het stof en de steentjes van de hele wereld bij (`updateWereldStof`: `wdust`, `grains`, de
  stofstraal), en bij een gast doet de wikkel `mpcUpdate` niets. Bij een gast verdween dus geen wolkje meer: in de meting
  liep `wdust` op van 240 naar 860 in vijf minuten, en elk wolkje werd elk beeld getekend. Bij de host liep het stof met
  schorpioenen in twee of drie groepen juist twee of drie keer zo snel. Nu werkt `mpcStofUpdate` het stof in Co-op een keer
  per beeld bij, bij iedereen, en slaat `updateScorps` het dan over (`wereldStofKlaar`). Nagemeten tot ronde 17: bij de
  gasten blijft `wdust` onder de 15, en de beelden per seconde zakken niet meer weg met de rondes.
  Meten met `node tools/mptest.js --taai --geenwinkel --pauze 2 --killer 6 --groei --duur 420`: `--killer s` laat de host
  een vijand die langer dan s seconden leeft raken (zodat de rondes doorlopen), `--groei` meldt elke 15 s per venster de
  beelden per seconde en de lijsten die groeien, `--ronde N` springt naar ronde N, `--geenwinkel` en `--pauze` versnellen.
- **Nog te doen, als het op een laptop nodig blijkt:** de lucht en de verre stad samen in een plaat bakken zoals de
  savanne, en alleen opnieuw als de camera ver genoeg verschuift. Eerst met F9 op een echte laptop meten of de stad daar
  ook onder de 60 zakt.

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

### Het geheim van de winkel in Ishmul (easter egg, 21-11-2026)

Gevraagd: "een winkel waar je met een geheim trucje achter de toonbank komt en in de achterkamer een kist met goud vindt,
af en toe in Ishmul". Het geheim staat in Ishmul bij elk winkelbezoek aan (`WINKEL.geheim.kans` 1, de host stuurt het mee in het bericht `winkel` als `g`); het zeldzame zit in de marktman, die maar 1 op 10 keer naar achteren loopt (`achterKans`). `mpcWinkelIn(g)` zet `winkelGeheimZet` en maakt de kist dicht en vol (`kistReset`). De marktman is gedeeld (27-11-2026, `dukaDeel`, `dukaHostZend`, `dukaGastStap`): de host beslist wat Duka doet en stuurt bij elke keuze (en elke 3 s als vangnet) het bericht `duka` met zijn plek, doel, fase, animatie en klok; een gast doet zelf geen keuzes en speelt dat af. Zo staat hij voor het hele team tegelijk met zijn rug naar de winkel (eerder liep hij op elke laptop een eigen rondje, en stond hij bij de een met zijn rug naar je toe en bij de ander niet). Gesnapt worden blijft per speler: wie betrapt wordt ziet zijn eigen regie, daarna pakt hij de Duka van de host weer op (`naRegie`). `tools/mptest.js --proef --winkeleerst` kijkt het na. Het trucje (zie "het geheim" in `notities/stad.md`) loopt per speler op zijn eigen laptop. De
achterkamer is `MPC_ACHTERKAMER` (een `binnen` zonder deur naar buiten, met een boog terug), met een kist van 30 goud: de
kist van Co-op (`mpcKistE`), dus maar een speler krijgt het goud. `mpcWinkelUit` zet het geheim weer uit.

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
  "1 of 2 teammates ready"), R na game over pas als iedereen R drukte (`mpCoopRematchKijk`), het potje begint pas als iedere
  laptop geladen is (zie "Samen beginnen"). Het goud van een kill en van een ronde krijgt iedereen (`mpcGoudIedereen`). Give 5 gold heeft
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

## Ishmul, de voorstad (gebouwd, 19-11-2026)

`MP_ISHMUL_LEVEL`, `MPC_KAARTEN`, `mpcKaart`, `mpStarts`; in de lobby `MP_KAARTEN.coop` (id `ishmul`, "Ishmul, the outskirts")

De tweede map van Co-op Survival, uitgewerkt in een mockup met de opdrachtgever (eerst "The Flood Gate" genoemd). Van rechts
(de start, bij de rand) naar links:

- **Het plein** waar de stad begint: drie opstapjes van 28 naar 84 (`opstap: true`, zie "opstapjes" in `notities/stad.md`),
  de pleinvloer van Nyundo op de bovenste trede (`vloer: 'plein'` op het terras, en `grondSoort` plein), een pleinwand met
  bogen achteraan en een fontein. Een fontein op een terras wordt na de terrassen getekend (`waterFonteinTeken` met
  `opTerras`), anders viel de rand van het plein over zijn voet.
- **Het huis aan de rivier** met een galerij (401) en een deur boven. De galerij loopt een plank uit boven de rivier
  (`meer: [0.3, 0]`, samen 3,1 Amir in plaats van 2,8): staat de schildman voor je, dan rol je net langs hem en sta je
  achter hem nog op de galerij (de rol stopt op de rand, `ROL.rand`). Erop: de rand van de fontein (197), dan de luifel boven
  een raam aan de rechtermuur (de rechte springdoek met `kozijn`, `h: 350`, bovenkant 378), dan de galerij. De luifel hangt
  hoog genoeg dat je er vanaf de trap onderdoor loopt; eerst hing hij op 150 en dat zag er toevallig uit, en een luifel op
  hoofdhoogte haal je vanaf de straat niet (een sprong is zo'n 190).
- **De rivier** van 1280 breed met een brug op straathoogte: de enige weg naar de overkant.
- **De linkeroever**: twee huizen met een gedeelde galerij (401), een rieten kraam als opstap, en het hoge huis.
- **De savanne** tegen de rots (`grondSoort` savanne tot voorbij de rots, gras, een acacia en een struik). Boven de savanne
  houdt de stad in de verte op (`stad.achterTot`): links daarvan tekent `stadAchter` geen rijen huizen meer en vaagt het
  paleis weg, zodat je daar lucht ziet (hoe ver precies: zie hieronder).
- **De rotsreuzen** (`achterBeeld: {k: 'rotsreuzen', x}` in `stad`, `STAD_ACHTERBEELD`, `stadAchterBeeld`): in die lucht
  staan granieten rotskoepels in de verte (`design/stad/verte/rotsreuzen.png`, een Grok-plaat, magenta uitgeknipt). Eigen
  trage parallax (0.12), de horizon net boven de straat, een beetje nevel erover, rechts afgeknipt op de grens van de
  verste rij huizen en naar links herhaald. Hij doet niet mee met de witte tint (`tintNiet`). Met x schuif je de rotsen:
  -2050 zet de hoge rots tussen de acacia en het hoge huis als je bij de savanne staat.
  Elke rij huizen in de verte houdt op bij een vast huis van zichzelf (`stadAchterRanden`): dat huis schuift met zijn rij
  mee, dus er springt nooit een huis weg en er staat nooit een half huis. Eerder hield elke rij op bij de linkermuur van
  het huis aan de straat, en stond het huis in de verte dat die muur doorsneed er half en doorzichtig achter: een half
  spookhuis boven het dak (daarvoor sprong de rand bij elke muur een heel huis op, en nog eerder zag je op de brug lucht
  tussen de huizen). Welk huis het eerste is, rekent het spel een keer per level en schermmaat uit, met twee eisen:
  1. staat de linkermuur van het meest linkse huis aan de straat links op het scherm, dan begint elke rij daar al, zodat je
     rechts ervan nooit lucht tussen de huizen ziet. Verder naar rechts geldt het vanzelf, want het huis aan de straat
     schuift sneller dan de verte. Gerekend met zoom `STAD_RAND.zoom` (0,85), iets boven de meekijkende camera. Let op:
     de verte staat buiten `viewZoom`, de huizen aan de straat erin. `achterTot` is daarbij alleen een extra grens.
  2. bij de rots (`cliffs`) loopt de middelste rij minstens zo ver door als de verste (de daken), zodat onder de daken
     altijd een huis staat en je de nevel daar niet als een plat blauw vak ziet. De voorste rij is vrij: zijn muren lopen
     door tot de grond.
  Met de camera bij de savanne staat de stad in de verte dus een stuk voorbij het huis aan de straat, en houdt hij op met
  hele huizen, als een trap: de voorste rij het verst. Het paleis vaagt weg voor de rand van de verste rij, het achterbeeld
  houdt daar op (`grensRand`).
  `tools/stadlucht.js` loopt de camera over de straat op vier schermen en meldt FOUT op elke plek waar tussen de huizen
  lucht te zien is (`stadAchterRand`) en waar een huis in de verte verspringt (`stadAchterRijen`).
- **De lucht** (`lucht: {wolken, vogels, gloed}` in `stad`, `STAD_LUCHT`, `stadLucht`, `luchtWolken`, `stadReigers`): wolken
  uit Grok in de stijl van de rotsen (`design/stad/verte/wolk_1..8.png`, gefacetteerd, middaglicht), witte reigers in een
  losse V in plaats van de gieren (met een dun grijs randje, zodat ze ook voor een wolk te zien zijn), en een warme gloed
  boven de horizon.

**De kleur**: Ishmul is van wit zand (`tint: 'wit'`, zie "de tint van een level" in `notities/stad.md`) en speelt altijd
overdag, met de blauwe lucht (`lagen: 'stad_dag'`, `versies: ['dag']` in `MPC_KAARTEN`: wit zand bij nacht werd grauw). De
opdrachtgever koos uit vijf beelden variant 3. **De luifel** naar de galerij van het huis aan de rivier is de strakke luifel
uit Stad 10, boven een raam aan de zijmuur (`h: 255, raam: true, maat: 0.45, ritme`): van de bovenste trede (het plein) erop,
en met een sprong naar links de galerij op. Eerst hing hij op 210 en was hij langer; dan leek het raam bijna op de grond te zitten.

Waar je begint: de host voor het huis aan de rivier, de gasten aan de overkant voor de twee huizen (`starts` in
`MPC_KAARTEN`). Het `start` van het level zelf blijft rechts op het plein: de rand (`rand: true`) rekent vanaf daar, en met
de start bij het huis lag de rechtergrens op -830 en het hele plein buiten de kaart. De treden zijn 80 breed: een vijand kijkt
zo'n 60 vooruit, en op een smallere trede zag hij al de straat eronder en bleef hij boven staan. Geen fakkels in de rots
(`rots: []`, die kwamen in de lucht uit), en op het huis met de kraam niet waar de kraam voor de muur staat.

Alles is te halen zonder speer (ook met de stokken), en er is geen balkon dat je niet haalt: de kruisboog komt hier uit de
deuren op de galerijen.

**De instellingen per map** (`MPC_KAARTEN`): het level, de deuren, de tonplekken, de starts per slot, het midden (voor de
revive-ton), het balkon voor de kruisboog, de fakkels per gevel en in de rots, en de kant van de dieren (`dierKant`) en van
de mensen (`mensKant`, met `mensKans`). De Dye Yard houdt precies wat hij had; `mpcKaart()` geeft de map die speelt (in de
episode altijd de Dye Yard-instellingen, die daar niet gebruikt worden). In Ishmul komen dieren alleen van links, en een
mens komt in 35% van de keren van rechts (het plein) in plaats van uit een deur.

**Random map** (`MP_KAARTEN.coop`, id `random`): de laatste keuze in de lijst, in Co-op Survival en in Survival (Co-op solo).
Bij Start loot `mpStart` een echte map uit de lijst (zonder `random` zelf) en zet die in de regels, zodat de gasten dezelfde
krijgen; elke Start loot opnieuw, een herstart met Shift+O speelt dezelfde map. `mpcKaart()` ziet dus nooit `random`.

**Testen:** `node tools/mptest.js --kaart ishmul --proef` loopt de hele proef op Ishmul. De controle op de fakkels verwachtte
8 bij nacht, maar sinds de fakkels in de rots zijn het er 10 (op main gaf hij al FOUT); nu telt elk aantal boven 0.

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
     fosfor, drie hyena's, een gewone kooiman (`duel: false`, geen geënsceneerd duel) en een dolkwerper, twee ravijnen en
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

## De tweede Co-op episode: The Smugglers' Cellar (gebouwd, 20-11-2026)

`COOPEP2_1` tot `COOPEP2_7`, `COOPEP2_LEVELS`, `MPC_EPS`, `mpEpLijst`, `mpEpReeks`, `mpEpKaartLevel`, `mpEpBestSleutel`

Op verzoek van de opdrachtgever: een nieuwe Co-op episode van zeven levels, van makkelijk naar heel moeilijk, met een
regie die laat zien waar de vijanden binnenkomen, de kelder uit Stad 14, en een team dat bij elkaar blijft. Zelf ontworpen
(regel 3). Geen bazen (regel 12), geen doornbossen en geen sneak (zoals de eerste episode).

- **Twee episodes in modus 'ep'.** De map in de lobby kiest episode en level: id '0' tot '2' is de eerste (The Long Grass),
  'b0' tot 'b6' de tweede, in groepen (`optgroup`) in de lijst. `mpEpLijst` geeft de levels van de episode uit
  `pvp.regels.kaart`, `mpEpKaartLevel` het startlevel; alle logica van de episode (banner, HUD, het slot, het eindscherm) leest
  via `mpEpLijst`. De beste score per episode (`amir.coopEpBest`, `amir.coopEp2Best`). De banner haalt het begin van de
  naam weg met `MPC_EP.naamKop` ("Co-op 2: " en "Ambush 5: ").
- **De levels** (een smokkelbende volgen van de karavaanroute, door de poort, de stad in, tot hun kelder):
  1. **The Caravan Trail** (makkelijk, `vlakte`): twee hinderlagen van twee shots, bandieten voor, een van achteren.
  2. **The Dry Gate** (makkelijk, `tafelbergen`): een poort met hek en rotswand die in de regie opengaat, een ravijn, twee
     bandieten die van boven invallen (`neer`) en een makkelijke schildbandiet.
  3. **The Outer Quarter** (middel, `stad_dag`): een deur gaat open, een kruisboog op de galerij (de camera kijkt omhoog), nog
     een deur.
  4. **Market at Dusk** (middel, `stad_avond`): bandieten van de daken, een deur achter het team, de galerij, en het level
     eindigt in de kelder tegen een hoge leemmuur.
  5. **The Gatehouse** (moeilijk, `schemer`): twee poorten met een hek, een kruisboog van achteren, en een elite-garde met
     vijf levens uit de tweede poort.
  6. **Lantern Street** (moeilijk, `stad_nacht`, fakkels): deuren beneden en op de galerij, de daken, een dolkwerper, een
     zweepman van achteren; vier shots in de tweede hinderlaag.
  7. **The Smugglers' Cellar** (heel moeilijk, `stad_nacht`, fakkels): drie hinderlagen; de laatste begint met het luik dat
     openvliegt (**From the cellar!**) en een elite, en dan naar beneden: het hele team bij de kelder.
- **De kelder in Co-op.** `kelderUit` speelt in de episode niet uit maar zegt "Wait at the cellar for your teammate"
  (`mpEpBijFakkels(true)`); de host kijkt met `mpEpBijEind`, dat in een level met `kelder` de plek van de E neemt in plaats
  van de fakkels.
- **Testen:** `node tools/mptest.js --hl` (met `--spelers 2` voor twee, `--shots map` voor plaatjes van de regie in level 7).
- **De winkel in de episode (gebouwd, 20-11-2026).** Gevraagd: "in het nieuwste Co-op level twee of drie shops in
  gebouwen, en goud te verdienen; alle items van Co-op Survival te koop". Episode b heeft `winkel: true` in `MPC_EPS`
  (`mpEpWinkel`); de eerste episode niet.
  - **Goud:** `mpcKill` geeft ook hier `MPC.killGoud` aan iedereen, en `mpEpLevelKlaar` per gehaald level
    `MPC_EP.levelGoud` (10, niet na het laatste). De HUD toont `Gold`.
  - **Drie winkels** in een huis, elk tussen twee hinderlagen (of ervoor), zodat de lijn de deur niet afsluit: Ambush 3
    (gevel 4), Ambush 4 (gevel 3) en Ambush 6 (gevel 4). Een gewone `binnen` met `winkel` en een houten plafond
    (`zwevers`), de strook van -20000 tot -22200, zoals de winkels in de stadslevels; een tip ervoor zegt het.
  - **Het winkelscherm** is dat van Survival (`mpcWinkelToon`, de hele `MPC_WINKEL`), zonder Ready (Close is genoeg) en
    zonder pauze (`winkelUIOpen`): de host denkt voor de vijanden, en zijn pauze zou ze ook stilzetten bij wie nog op
    straat vecht. `hinderKlem` geldt niet in een huis (de lijn trok je anders de winkel uit).
  - **Mee naar het volgende level** (`mpEpNieuw`, `mpEpNaStart`): ieder houdt zijn goud, `koop`, de kalebassen en het gif
    in zijn tas; een extra leven blijft (`pvp.levens`), een gekocht speerslot komt terug en is aan het begin van een level
    gevuld. Na game over de stand van het begin van dat level (`tas0`), na het slot niets.
  - **Kisten** (gevraagd: "een kistje, maar maar voor een van de spelers te openen, en die krijgt het goud"): een in
    Ambush 2 tot en met 6 (20 tot 30 goud, in 3, 4 en 6 op de galerij). De host beslist (`mpcKistE`, `mpcKistNeem`): de
    host zelf meteen, een gast vraagt het met `kistVraag`. Iedereen hoort met `kistOpen` wie het was; die krijgt al het
    goud (`mpcGoudErbij`, niet gedeeld), bij de rest gaat het deksel leeg open met "Your teammate opened the chest". Wie te
    laat was hoort `kistNee` ("Too late"). Drukken twee tegelijk, dan wint wie het eerst bij de host aankomt.
  - **Testen:** `node tools/mptest.js --winkel` (met `--spelers 2` voor twee). Daarin ook de kist: allebei tegelijk E, en de gast alleen.

## De hinderlaag en het leiband (gebouwd, 20-11-2026)

`MPC_HL`, `hinderlagen`, `hinderReset`, `hinderStart`, `hinderStap`, `hinderShot`, `hinderHostStap`, `hinderAllenBij`,
`hinderVechtKlaar`, `hinderKlem`, `hinderHint`, `hinderCamX`, `hinderCamY`, `hinderBalken`, `hinderVast`, `MPC_LEIBAND`,
`leibandKlem`

Gevraagd: "bij bereiken van een punt freezed het spel en gaat de camera naar een paar plekken waar mobs binnenkomen (een
deur, een poort, van boven, van achter), dan weten spelers: ok, dit is de fight", en "spelers kunnen maar max X van elkaar
zijn, of ze kunnen door die freeze niet verder tot de andere speler levend en bij is". Beide zijn gebouwd.

- **Het veld.** `hinderlagen: [{x, vecht, shots: [{x, h, t, poort, deur, kelder}]}]` in het level; een spawn met `hl` (de
  index van de hinderlaag) en `shot` (het shot) hoort erbij. `readLevel` neemt het over, `levelcheck.py` kijkt het na (regel
  `hinderlaag`: shots, volgorde, niet in een ravijn, voor het einde, de poort, gevel en kelder bestaan, en een spawn wijst naar
  een shot dat er is; een poort die alleen door een shot opengaat telt bij `poorten` als geopend).
- **De lijn.** Op `x` staat een onzichtbare muur (`hinderKlem`, na `aanvKlem` in de lus): niemand komt er voorbij tot de
  hinderlaag open is. Wie er alleen staat krijgt een hint: wachten op het team, of eerst de dode teamgenoot reviven.
- **Het begin.** De host (`hinderHostStap`, in `mpEpHostStap`) begint pas als iedereen leeft en binnen `MPC_HL.verzamel`
  (650) van de lijn staat (`hinderAllenBij`), en stuurt `hl`. Wie in een huis staat telt niet als bij de lijn, en zolang
  het team in de winkel is begint er niets: de winkelkamer ligt op -20000, ver links van elke lijn, en telde eerst als erbij. Bij iedereen dan de regie (`hinderStart`): zwarte balken
  (`#hlbalken`), Amir staat vast (`hinderVast` in `amirVast`) en niets raakt hem (in `hurtPlayer` en `godMode`).
- **De regie** (`hinderStap`, in `mpCoopStap`, op echte tijd): na `MPC_HL.aanloop` per shot `MPC_HL.shot` seconden. De
  camera glijdt naar het shot (`hinderCamX`, een tak voor die van een dode in de lus; zonder `x` kijkt hij naar de deur,
  poort of kelder van het shot) en kijkt mee omhoog naar een dak of een deur op een verdieping (`hinderCamY`, in
  `updateCamera`). De kop van het shot (`t`, "From the gate!") komt als banner. Op het shot (`hinderShot`) komen de spawns
  van dat shot los (`sp.hlVrij`), een poort gaat open (`poortOpen`, bij iedereen, zodat het hek ook bij de gast optakelt),
  het kelderluik vliegt open, en een deur gaat open via de spawn (`stadDeurUpdate` slaat de in-beeld-eis over). De
  spawns komen op hun eigen plek (niet net buiten beeld) en hoe ver het team ook staat (de spawnlus en `poortUpdate`). Het
  beeld staat niet helemaal stil: de wereld loopt door, zodat je ze ziet binnenkomen; alleen de spelers staan vast.
  Daarna terug naar Amir en **FIGHT!** (of de `vecht` van de hinderlaag).
- **Het gevecht.** De lijn blijft dicht tot alle spawns van de hinderlaag er zijn geweest en er geen levende vijand meer is
  binnen `MPC_HL.rond` van de lijn (`hinderVechtKlaar`), of na het vangnet (`MPC_HL.vangnet`, 150 s). Dan stuurt de host
  `hlvrij` en zegt het spel "The way is open".
- **De lijn schuift mee in het gevecht** (`hinderGrens`, 20-11-2026). Zodra het gevecht begint ligt de lijn niet meer op `x`
  maar `MPC_HL.ruimte` (700, was 450) voorbij de verste vijand van de hinderlaag (zijn spawn, de deur waar hij uitkomt, een shot).
  Aanleiding: in Ambush 2 stond de makkelijke schildbandiet op -7600, voorbij de lijn op -6300; hij kwam niet vanzelf en het
  team kon niet bij hem, dus de lijn bleef dicht tot het vangnet. `hinderKlem`, `hinderHint` en `hinderVechtKlaar` lezen allemaal
  `hinderGrens`.
- **De vijanden wachten in de regie** (`hinderHoud`, in `mpcUpdate`, alleen bij de host). Wie er al was voor de regie staat de
  hele regie stil; een nieuwe vijand beweegt `MPC_HL.toon` (1,2 s: de deur uit, de poort door, van het dak) of tot hij binnen
  `MPC_HL.afstand` (500) van een speler is, en wacht dan tot FIGHT!. Gevraagd: "je moet zien dat er iets aankomt, maar niet
  gefreezed zijn tot ze op je staan". Daarvoor liep elke vijand de hele regie door (ruim 7 s bij drie shots) en stond hij bij
  FIGHT! al op je.
- **Een deur niet naast de lijn.** In Ambush 3 (eerste), 4 (tweede) en 6 (allebei) lag de lijn 230 tot 330 px van de deur
  van het eerste shot; die lijnen liggen nu 300 verder terug (en de vijanden van "Behind you!" 100 tot 200 mee). Houd bij een
  nieuwe hinderlaag een deur, poort of dak minstens zo'n 500 px van de lijn.
- **Testen:** `node tools/mptest.js --hl` speelt nu elke hinderlaag van Ambush 2 tot en met 6 na: bij FIGHT! staat geen
  vijand binnen 200 px van een speler, en na 6 s staat elke vijand binnen bereik van de lijn. `HL_LV=3,6` beperkt tot die
  levels (`HL_LV=x` slaat ze over), `HL_DEUR=1` print waar de deuren echt staan.
- **De lijn houdt ook de vijanden tegen, en je ziet hem (22-11-2026).** Gevraagd: "met stun hit met stokken sloeg ik de
  ambush vijand buiten de onzichtbare barriere, die ik ook zichtbaar wil". `hinderKlem` klemde alleen de spelers; een terugslag
  (de stun-counter, de draaislag) sloeg een vijand voorbij de lijn, waar niemand meer bij kon, en dan bleef de lijn dicht tot het
  vangnet. Nu zet de host in het gevecht elke levende vijand die links van `hinderGrens` komt terug op de lijn (zijn spawns
  liggen er allemaal rechts van). En de lijn is te zien: dezelfde lichtzuil als het leiband, maar rood (`HINDER_ZUIL`,
  `hinderZuilX`, in `leibandTeken`), voor en tijdens het gevecht, niet in de regie, binnen of als je dood ligt.
- **Het leiband** (`leibandKlem`, alleen in de Co-op episodes; in Co-op Survival, ook Ishmul en Co-op solo, loop je vrij, op verzoek van de opdrachtgever): een levende speler komt niet verder dan `MPC_LEIBAND.max`
  (1600, eerder 1200 en 1000) van een levende teamgenoot; wie al verder weg was (na een revive of een val) mag alleen dichterbij. Niet in een
  huis, de winkel, de regie of het gevecht van een hinderlaag (`hinderVecht`). Een hint: "Stay close to your teammate".
- **Ruimer en zichtbaar (21-11-2026).** Gevraagd: "vergroot de range met 20%, en zorg dat er licht duidelijk is tot waar je
  mag gaan". `MPC_LEIBAND.max` is 1200 (was 1000). Op de grens staat een zuil van warm licht met een plas op de grond en
  opstijgende vonkjes (`leibandGrens`, `leibandTeken`), die opkomt vanaf `MPC_LEIBAND.zie` (900) van de grens en zacht ademt.
  De grens is de doorsnede van `x ± max` rond elke levende teamgenoot (zonder de speling van wie al verder weg was). Hij
  wordt getekend na de lichtlaag en het weer (`leibandNa`, `leibandNaTeken`, zoals `stadNachtNa`): daarvoor kleurde de
  nacht hem blauw en dun. Niet als je dood ligt, in een huis of de winkel, of in de regie.
- **Anders dan gevraagd:** het spel bevriest niet echt (een `dt = 0` zou de vijanden ook stilzetten, en `mpcVriesWacht`
  ontdooit een freeze die te lang duurt); de spelers staan vast en zijn onaantastbaar, de vijanden lopen binnen en wachten
  dan (zie hierboven).

## Bijgesteld na het spelen (21-11-2026)

- **Meer ruimte (22-11-2026).** Gevraagd: "de ruimte qua afstand van elkaar is nog te klein, of de ambush-ruimte". Drie
  dingen: het leiband staat uit in het gevecht van een hinderlaag (`hinderVecht`, in `leibandKlem` en `leibandGrens`): de lijn
  houdt het team daar al bij elkaar, en bij "Behind you!" wil je je juist opsplitsen. `MPC_LEIBAND.max` van 1200 naar 1600,
  ongeveer de wereldbreedte in beeld op een laptop (1280 / 0,75 is zo'n 1700): daarvoor liep je al tegen de zuil terwijl je
  teamgenoot nog midden in beeld stond. En `MPC_HL.ruimte` van 450 naar 700, zodat er voorbij de verste vijand plek is om te
  ontwijken. `tools/mptest.js --hl` test nu 1600 en dat het leiband in het gevecht uit staat; de revive-proef zet het team
  eerst buiten `MPC_HL.verzamel` neer (de regie begon soms al voor de gast dood was).

- **Wie dood ligt pakt niets op.** `eDruk` en `sgPak` doen niets zolang `dead`: geen speer, rek of kist terwijl je op de
  revive wacht. Daarvoor kon dat wel.
- **Beginnermodus** (`mpcBeginAmulet`, `pvp.inst.coop.beginner`, de rij `#mpbeginrij` onder Map in de lobby, voor Co-op
  Survival en de episodes, niet het Duel): iedereen begint met `koop.amulet` op 2, de Gris-gris op trap 2 (20%). In de
  episode gaat die mee met `koop`, dus ook naar het volgende level; trap 3 koop je in de winkel.
- **Ambush 6 en 7 een tikje makkelijker:** per hinderlaag een vijand eruit. Ambush 6: de dolkbandiet uit de deur van
  hinderlaag 1 en die van het dak in hinderlaag 2. Ambush 7: de dolkbandiet uit de deur (hinderlaag 1), die van het dak
  (hinderlaag 2) en die naast de elite bij het luik (hinderlaag 3).
- **De kruisboog op de galerij is ook met de stokken te halen.** Een kruisboogschutter op een galerij hoort bij een
  hinderlaag en moet dood voor de lijn opengaat, maar zonder speer kwam je er niet bij. Op verzoek van de opdrachtgever geen
  rietkraam (die zet je zo op de galerij), maar een **doekkraam in de steeg aan de verre kant** van het lagere huis van de
  galerij: de doek werpt je op het dak (2 hoog, 771), en van dat dak spring je op de galerij (401). De speerman kiest de worp
  van afstand, de stokkenman de omweg. Ambush 3: de doek van -4900 naar -4625 (dak van huis 5). Ambush 4: de rietkraam onder
  de galerij (-3750, daarmee sprong je er direct op) is een doek op -3425 (dak van huis 4). Ambush 6: de doek van -3650 naar
  -3325 (huis 3) en een nieuwe op -5730 (huis 6). Ambush 7: de doek onder de galerij van -3600 naar -3325, en nieuw op -2530
  (huis 2) en -4930 (huis 5 en 6, voor twee galerijen). Nagemeten in Chromium: straat, tafel, doek, dak, galerij.

## Co-op solo (gebouwd, 18-11-2026)

De derde keuze onder Single Player, Survival (`btnsbcoop`, City Survival): Co-op Survival, of de Co-op episode, voor een speler, zonder verbinding
(`MP_SOLO`, `mpSoloOpen`, `pvp.solo`). Geen eigen arena naast Co-op (regel 4): `mpSoloOpen` maakt het `pvp`-object zoals
`pvpVerbonden` dat voor een host doet, maar zonder peers en zonder `pvpNetStart`, en opent de gewone lobby. Alles daarna
is de code van Co-op zelf; elk bericht gaat naar niemand.

- **Wat vanzelf klopt met een speler:** ronde 1 wacht op geen gast (`pvpGasten()` is leeg), Ready in de winkel is alleen
  de jouwe (`mpcWinkelKlaar`), R op het eindscherm begint meteen opnieuw, en wie doodgaat is iedereen, dus game over zodra de val
  uitgespeeld is (`mpcDodenStap`, `mpcEindWacht`): geen revive-ton.
- **De lobby solo** (de klasse `solo` op `#mplobby`, `mpsolo` op `#start`): geen Duel, geen Ready, geen spelerslijst of ping,
  geen "Waiting for the other players" onder de broek, de titel `MP_SOLO.titel`, en Start kan altijd (behalve zonder
  vijanden). De broek en het wapen kies je zoals in Multiplayer.
- **Bewaard apart:** de instellingen gaan naar `amir.mpsolo` (`MP_SOLO.sleutel`), niet naar die van de host (`amir.mp`).
- **Terug:** Escape geeft het pauzemenu en Terug brengt je naar deze lobby (`mpNaarLobby`); Leave the lobby gaat terug naar
  het Sandbox-scherm.
- **De pauze staat echt stil:** de rondes, de deuren en het spawnen van Co-op lopen op echte tijd (`pvpStap(realDt)`, dan
  `mpCoopStap`), omdat een potje samen niet op een pauze kan wachten. Solo hoeft dat niet: zolang het pauzemenu open is slaat
  `pvpStap` alles over (`pvp.solo && paused`), dus er komt in de pauze geen vijand meer uit een deur.
- **20% meer goud:** alleen verdien je meer, uit kills en overleefde rondes (`MP_SOLO.goudFactor`, 1.2, in `mpcGoudErbij`).
  De beurs blijft heel: het deel achter de komma spaart zich op in `pvp.coop.goudRest`, dus een ronde van 5 geeft 6 en vijf
  kills van 1 samen ook 6.
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

## De nieuwe winkel van Co-op (22-11-2026): tabs, kaarten, Undo en aftellen

Kop in de HTML: `// ---- Undo in de winkel van Co-op` en `mpcWinkelToon`. Ontwerp: optie A2 op het canvas "Amir winkel: twee
layouts" (rechts een paneel, links blijft de winkelkamer met de marktman zichtbaar).

- **Layout** (`#winkelui.coop`): het paneel staat rechts (64vw), de kamer links blijft zichtbaar onder een zacht verloop.
  Bovenin `Shop` en je goud (`#wkgoud`), dan de tabs (`#wktabs`, `MPC_WINKEL_CAT`: Spears of Sticks voor een stokspeler,
  Supplies, Charms & life, Team alleen met een teamgenoot). Elk artikel in `MPC_WINKEL` heeft een `cat`; een artikel met
  `nieuw: true` (nu de Pathfinder) staat als brede kaart bovenaan met NEW.
- **Kaarten** met een plaatje (`mpcBeeld`): de echte speer, de Pathfinder, de kalebas en Silver Pride uit hun eigen map, de rest uit
  `items/winkel/` (`MPC_IKOON_IMG`): Grok-plaatjes in de stijl van de winkelspullen (mat, aardetinten, met de speer en het gifflesje
  uit het spel), en de drie stokken zijn de echte stokken uit het spel, gekruist. Give 5 gold toont de goudstukken van de teller met
  de outfit van wie het krijgt: zijn naam en zijn kleuren als stipjes (`mpcGeefBeeld`, `MPC_SET_KLEUR`, `mpcSetKleuren`)
  (`MPC_IKOON`, `mpcStokIkoon`), plek voor echte art later.
- **Het zijpaneel** (`mpcInfoToon`): het item groot (`#wkinfobeeld`), sfeertekst, uitleg, **You carry** (`mpcDraagToon`: je
  speren in hand en op de rug zoals in de inventory, en je tas) en Buy (bij de Pathfinder "Buy another" als je er al een hebt).
  Zonder keuze toont hij het eerste artikel van de tab.
- **De marktman** zegt iets in de ballon links (`#wkzeg`, `mpcZeg`, de zinnen in `MPC_ZEG`): bij openen, kopen, de Pathfinder,
  Undo, te weinig goud en Ready.
- **Undo** (`mpcLaatste`, `mpcUndo`, `mpcUndoKan`, `#wkundo`): alleen je laatste aankoop, alleen bij deze marktman
  (`mpcWinkelIn` en `mpcWinkelUit` zetten hem op null, dus in Survival alleen wat je deze ronde kocht), en alleen zolang hij
  onaangeroerd is (`mpcUndoStand` legt het na het kopen vast: levens, gif, speren, `RUG_MAX`, Pathfinders). Give 5 gold is
  niet terug te draaien. Het goud komt helemaal terug.
- **Aftellen na Ready** (`MPC_WINKEL_WEG.aftel`, 3 s): het scherm blijft open na Ready. Is iedereen klaar, dan zet de host
  `C.vertrek` en stuurt `wkvertrek`; iedereen toont "Leaving in 3..." (`mpcVertrekToon`, ook in de banner). Not ready stopt het
  (de host stuurt `wkvertrek` met `aan: false`). Bij nul stuurt de host `winkelUit` (`mpcVertrekStap`, vanuit `pvpStap`, ook
  in de pauze van Co-op solo).


## De outfits van Mkuki (22-11-2026)

Op verzoek: Amir met de speer is voortaan Mkuki, de basisskin van de speer-tribe, en met de stokken het oude tenue
met de leeuwenvacht. Dat geldt overal, niet alleen in Multiplayer: buiten Multiplayer is het Outfit 1 (`broekNu`, alleen
niet met `STOK_AAN` of in een level met `broekKeuze` of een eigen `skin`).

- **Hoe het tekent.** Een outfit is een "broekkleur" met `skin: 'mkuki'` (`MK_OUTFIT.lijst`). `broekBeeld` zoekt bij het
  oude frame het frame uit de skin (`mkSkinVan`: zelfde naam in `karakters/amir/mkuki_spel/`, via `_skinRel` uit SKIN) en
  kleurt de kleding om met de zonekaart ernaast (`mkLap`, `<frame>_zones.png`): per zone de doelkleur maal de helderheid
  van het frame gedeeld door die van de Mkuki-kleur (`MK_OUTFIT.vref`), dus licht en schaduw blijven. Per tekening en
  per speler, dus in Co-op kan de een Mkuki zijn en de ander met de stokken het oude tenue. Wat de skin niet heeft
  (de oude ren, de sluipaanval, de executie, de stokken, de schaduw) blijft het oude tenue.
- **Vooraf kleuren (`MK_WARM`).** Eerst kwam een outfit pas op kleur als een frame voor het eerst getekend werd: de
  zonekaart moest nog binnenkomen en het kleuren (13 ms per frame in de grote set) gebeurde midden in het spel, dus zag je
  een beweging eerst in Outfit 1. Nu:
  - `mkLap` is gesplitst: `mkZonen` doet het dure deel een keer per frame (welke pixel bij welke zone, helderheid, alfa,
    binnen de rechthoek), los van de outfit; een outfit inkleuren kost daarna 0,2 ms.
  - `mkSkinVoorladen` laadt de zonekaarten mee, en eerst het voorbeeld van de lobby (de idle uit de grote set).
  - In het menu (`mkVoorWarm`, 6 s na het openen, en bij de knop Multiplayer en in de lobby; elk beeld hooguit
    `MK_WARM_MENU` ms, `requestIdleCallback` kwam in het menu nooit aan de beurt): het voorbeeld van de lobby in alle zes
    outfits, dan elk frame voor de outfit van de vorige keer (`amir.mpoutfit`). Nagemeten: na 5 s staat het voorbeeld klaar.
  - In de lobby (`vachtLobbyStap`) elk frame voor de outfits die nu gedragen worden (`mkWarmTaken`), en de rest achter het
    laadscherm (`warmBouw`). Met de stokken ook het voorbeeld (`stokBank.staan[0]`) in alle zes outfits van de stoktribe.
  - `mkSkinLaad` zet elk pad om naar het volledige adres: `mkLosBeeld` bouwt zijn pad uit `img.src` (volledig), de
    voorlader uit een kort pad, en zonder dat waren het twee plaatjes en kwam het vooraf kleuren in het spel niet aan.
  - `tools/mptest.js` meldt FOUT op elk outfitframe van Mkuki dat pas in het spel gekleurd wordt; nu 0.
- **De zonekaarten** komen uit `tools/mkuki_spel_zones.py`: precies zoals `tools/mkuki_spel_bak.py` het frame bakt (speer,
  maskers, vuist), maar met het lijf in de zonekleuren. Bak je de skin opnieuw (een export uit de Mkuki animeer tool),
  draai dan ook dit script. `--check` kijkt eerst na of de lijven nog kloppen met de frames in de repo.
- **De zes outfits** (neutrale namen, zodat een naam niet stuurt): 1 Mkuki zelf; 2 donkerbruine broek, zand schort, wit
  boven; 3 creme broek, witte schort, rood boven; 4 zwarte broek, oker schort, donkerrood en goud; 5 witte broek, ivoren
  schort, goud; 6 bordeaux met goud. Elk een eigen broekkleur, zodat je elkaar uit elkaar houdt.
- **De lobby.** `mpBroekLijst`: met de speer de outfits (`MP_OUTFIT`, bewaard in `amir.mpoutfit`, standaard mk1, mk3, mk4
  per slot), met de stokken de outfits van de stoktribe (`MP_VACHT`, `amir.mpvacht`; zie hieronder, vroeger de oude
  broeken `MP_BROEK_OUD` en `amir.mpbroek`). Wisselt je wapen, dan zet `mpBroekPas` je keuze
  om. Het bericht blijft `{t: 'broek', id}`. `MP_NAAM.kleur` heeft per outfit zijn opvallendste kleur (`stip`).
  `mpLobbyOpen` zet een level-skin uit (`skinZet(null)`): het menu houdt het laatst geladen level vast, en had dat een
  eigen skin (Test 90, Tau), dan gaf `mkSkinVan` niets en stond Amir in de lobby in het oude tenue in plaats van in zijn outfit.
- **De losse speer (MK_LOS, 22-11-2026).** De speer zit niet meer in het frame: `tools/mkuki_spel_los.py` bakt per frame
  het lijf zonder speer (`_lijf.png`), wat over de speer komt (voor-masker en vuist, `_boven.png`), de maskers van de speer
  (`_sm.png`, rood weg en groen achter) met hun zonekaarten, en `los.json` met per frame de speer uit de Mkuki animeer tool
  (hoek, midden, breedte, draaiing, spiegelen, achter). `mkLosBeeld` tekent speer achter, lijf, speer voor, boven.
  De speer is per soort: de gewone (`bron/amirspeer_<hoek>.png`) met het lint via `speerKleur`, of de Pathfinder
  (`bron/pf_<hoek>.png`) met zijn vaantje recht omlaag aan de knoop. Mijn eigen Amir draagt de soort uit `speerBlauw`
  (`mkSpeerNu`); een teamgenoot de soort uit zijn stand (`sp`, en `vw` de wind voor het vaantje, `mkSpeerZend`, alleen
  als het niet de gewone is). Het vaantje waait in de hand net als op de rug (`pfRugWind`): stil wiegt het, rennend
  waait het naar achteren. Zolang iets laadt het gebakken frame. Stel je de speer
  bij in de tool, draai dan met de export `mkuki_spel_bak.py`, `mkuki_spel_zones.py` en `mkuki_spel_los.py`.
- **De vuist in het bukken (25-11-2026).** In `bukken_hold_1-4_speer` en `bukken_in_8_speer` was de achterste vuist (die de
  speer bij de kin vasthoudt) weggegumd met het weg-masker van het lijf, en de vuistlaag (`_boven.png`) stond op een vaste
  plek: in de ademlus viel de vuist half of helemaal weg. Hersteld zonder de tool: het lijf is daar nu het speerloze
  Mkuki-frame (`bukken/bukken_hold_N.png`, zelfde lijf, 120 px naar rechts op het speercanvas) met zijn zonekaart, de
  boven-laag is de vuist daaruit, en de speer (`los.json`, `_sm.png`) is die van hold 1, verschoven met de vuist mee
  (hold 2: 1, -5; hold 3: 0, 4; hold 4: -1, 3; in_8: 0, -14). Het gebakken frame en de kleine set opnieuw. Let op: draai je
  `mkuki_spel_los.py` opnieuw uit de tool, dan komt de oude fout terug, tenzij de vuist daar ook goed staat.
  Nog over: in `bukken_in_6_speer` zit onder de kin een restje van de vuist (een overgangsframe van 35 ms).
- **De idle glad (23-11-2026).** De 20 Grok-frames van `idle/idle_sp` verschilden elk een beetje: nek en kralen
  veranderden van vorm en schort en broek wiebelden tot 5 px op en neer, terwijl in de oude idle alles vanaf de heup
  stilstaat. `tools/mkuki_idle_glad.py <mkuki-checkout>` maakt ze uit een lijf: frame 0 (bewaard in
  `karakters/amir/mkuki/idle/idle_sp/bron/` op claude/mkuki) bewogen zoals de oude Amir. Bovenlijf en hoofd met de
  optical flow van de oude frames (vanaf de riem uitlopend tot stil), de verre arm om schouder en elleboog met de
  hoeken van de oude arm (de hand op de heup rond frame 10), en een donkere buitenrand om lijf en arm zoals de oude
  Amir heeft. Het schrijft de spelframes met zonekaarten (groot en klein) en de bronframes in de mkuki-checkout,
  zodat de tool en een volgende bak hetzelfde zien. Draai je later `mkuki_spel_bak.py` en de rest opnieuw, dan
  komen deze frames vanzelf mee, want ze staan ook op claude/mkuki.
- **Testen.** `node tools/outfittest.js map`: elke outfit in idle, ren en stoot naast het oude tenue, de losse speer
  tegen het gebakken frame (alleen randjes van de schacht mogen verschillen) en elke speersoort in zijn hand, en de sandbox.
  `node tools/mptest.js --proef --stokken gast2`: twee spelers Mkuki, een met de stokken.

### Silver Pride, het zilveren leeuwenhart (gebouwd, 22-11-2026)

`ZH`, `zhGebruik`, `zhStart`, `zhStap`, `zhTeken`, `zhTauNa`, `zhOpstaan`, `zhKVoor`, `zhOntwaakT`, `zhCarry`, `TEST_91`

Op verzoek van de opdrachtgever: een revive-item voor de stokspeler (de speerspeler krijgt later zijn eigen, de veren).
- **De winkel:** `zilverhart` in `MPC_WINKEL`, tab Team, `stok: true`, en alleen te zien met een teamgenoot (net als Give 5 gold).
  Prijs 35, 50, 65 (de derde keer is de laatste, daarna Sold out). Je draagt er een tegelijk (`ZH.max`, `zhCarry`); Undo kan zolang
  je hem niet gebruikte. Het beeld is `items/zilverhart/hart.png` met het leeuwenmedaillon linksboven (`leeuw_medaillon.png`, de
  Tau-kop in zilver); het icoon in de balk is `hart_icoon.png` met G. In een episode gaat het hart mee in de tas (`tas.zh`).
- **Gebruik:** ligt er een teamgenoot dood, dan drukt de stokspeler G (`zhGebruik`): Amir bukt even (`zhNeerT`, via `canDuck`), het hart
  ligt een halve Amir voor hem, klopt `ZH.puls` s in een cirkel zilverwit licht (zie Bijgesteld hieronder), die in de uitbarsting uiteenspringt in vonken, en dan komt de dode eruit: van
  `ZH.klein` naar normaal in `ZH.groei` s, met een zachte lichtzuil en een ring over de grond, geen flits. Tau brult tegelijk
  `ZH.tauBoven` Amir boven het hart (`zhTauNa`, dezelfde frames als de zonnestraal, wit met een koelere gloed). De uitbarsting klapt: de brul (`sounds/zilverhart_brul.mp3`) met de klap (`sounds/zilverhart_klap.mp3`) eronder, een witte klap met een schokgolf vanuit het hart, een korte witte flits over het hele beeld en het beeld schudt (`ZH.schok`, `ZH.stop`, `ZH.flits`), bij iedereen die het ziet.
- **Het netwerk:** het bericht `zh` (`{voor, x, h}`, in `MP_DOOR`) gaat naar iedereen; ieder speelt het zelf af. De dode staat op zijn
  eigen scherm op (`zhOpstaan`, precies op het hart, net als bij `symPak`), met `invuln` en `zhOntwaakT` op `ZH.onkw` (3 s). Zolang
  zijn stand nog niet binnen is, tekent `pvpTekenEen` het lijk niet meer, en hij groeit via `zhKVoor`.
- **Geen abilities** zolang `zhOntwaakT > 0`: geen rol, duw, woede, stof, grondklap, lage slag, blok, meditatie of kalebas. Gewoon slaan mag.
- **Test 91: Silver Pride** (in Test levels sticks): een oefenteamgenoot in de kleuren van de mentor ligt voor je, G speelt het af, het hart
  is daar onbeperkt en na `ZH.dummyStaat` s valt hij weer om. Proef: `node tools/zilverhart_test.js [map]` en
  `node tools/mptest.js --zilverhart --stokken host`.

**In Co-op solo (23-11-2026):** op verzoek staat Silver Pride ook in de winkel van Co-op solo, daar voor elk wapen
(`mpcWinkelVoorMij`) en voor jezelf (`mpcZhZien`). Eigen prijs `prijsSolo` 50, 80, 110 (een self-revive is meer waard dan
een teamgenoot terug; de derde keer is de laatste) en eigen tekst `uitlegSolo` (`mpcUitleg`). Ga je dood met een hart in de
tas, dan is het geen game over: `zhSoloStap` (in `mpcDodenStap`, voor `mpcEinde`) laat na `ZH.soloWacht` (2 s) het hart
vanzelf kloppen op je lijk (`zhStart` met `voor` jezelf), en met de uitbarsting sta je op (`zhOpstaan`) met een leven en
`ZH.soloOnkw` (4 s) onkwetsbaar; de abilities mogen dan wel (`zhOntwaakT` blijft 0), zodat je met een rol weg kunt komen.
G blijft in solo van de woede (`zhToetsMag`); het icoon in de balk staat altijd klaar.

**Bijgesteld (23-11-2026):** de bol is weg; nu een cirkel zilverwit licht vanuit het midden van het hart, naar buiten zwakker,
die met de slag opzwelt (`ZH.licht`, `ZH.lichtA`, `ZH.slagA`). Het afstellen gebeurt niet in het spel maar in een
losse tool (een artifact van de opdrachtgever, de Silver Pride tuner) die hetzelfde effect nabootst; de getallen daaruit gaan in `ZH`.

**De hartslag en de brul (23-11-2026, uit de tool):** het oude geluid had maar een slag, gerekt. Nu is het een echte lub-dub
(`sounds/zilverhart_slag.mp3`, geknipt uit de ElevenLabs-opname) die per slag opnieuw klinkt, met een afstand die van `ZH.tempoA`
(1,15 s) naar `ZH.tempoB` (0,45 s) loopt binnen `ZH.puls` (3 s): steeds sneller tot de uitbarsting (`zhSlagTijden`, in `zhStap`).
Het licht en het hart (`ZH.pomp`) zwellen op dezelfde tijden op (`zhSlagNu`, lub op `ZH_LUB`, dub op `ZH_DUB`). De brul is weer aan:
de brul van Tau lager gestemd, met een dreun eronder en galm (`sounds/zilverhart_brul.mp3`), op `ZH.brulVol` 4. De klap is een eigen
dreun met een glinstering (`sounds/zilverhart_klap.mp3`); de klap van de zonnestraal (`zegelontdek.mp3`) zei "miss" (het is de
misser van de kooiman). Alle drie spelen op de gedeelde AudioContext (`zhKlank`): boven 1 gaat het volume een compressor in en dan
een begrenzer, zodat harder ook harder klinkt zonder te kraken. Later op verzoek: de klap uit (`ZH.klapVol` 0, alleen de brul) en
het beeld schudt harder (`ZH.schok` 0,7).

### Feathers of the Bennu, de veren van de speerspeler (Test 94, 23-11-2026)

`BN`, `bnGebruik`, `bnStap`, `bnTekenAchter`, `bnTekenAmir`, `bnBol`, `bnZoemStart`, `bnKleurWissel`, `bnDummy`, `TEST_94`

Op verzoek van de opdrachtgever: de tegenhanger van Silver Pride voor Amir met de speer (Mkuki). Nu alleen in Test 94 (Test levels),
nog niet in de winkel van Co-op en nog niet over het netwerk.
- **Het verloop (G):** Amir zakt op een knie en pakt drie veren van zijn heup, legt ze op zijn hand met de andere hand erop en sluit zijn
  ogen (frame 44: de veren gloeien, een zachte zoemtoon zwelt aan), opent ze (frame 52: een flits met stralen, de ogen gloeien egaal
  zonder pupil zoals bij Aang) en blaast (frame 70). Vanaf het begin staat er een luchtbol om hem heen (altijd om zijn hele lijf, `bnBol`),
  hij is onkwetsbaar en staat vast (`bnVast` in `amirVast`). Bij het blazen zet de bol uit, er draaien zes veren om hem heen (de drie
  Grok-veren uit `verenset.png`, elk 49 standen van een draai om de lengteas) en de windvlaag van het spel steekt op (`startGust`, de kant
  op van de teamgenoot). Als de bol verdwijnt (`bnVlaagT`) komt een flinke vlaag met de roep van de Bennu (`sounds/bennu_vlaag.mp3`),
  de veren waaien weg en de teamgenoot staat verderop, op een veilige plek en niet per se in beeld, weer op. Daarna nog `BN.naOnkw` s
  onkwetsbaar. De muziek gaat zolang naar `BN.muziekDemp`.
- **Beeld:** `karakters/amir/mkuki_spel/bennu/`: `lijf.png`, `veer.png` (de veren in zijn hand, grijs), `oog.png` (het wit van de ogen),
  78 frames in 13 kolommen van 218x334, en `meta.json` (per frame het midden van de veren, de ogen en de omtrek van zijn lijf). De frames
  komen uit twee Grok-clips (posts 050ea3a1 en f216f556); de veren en de ogen worden live gekleurd. Alle effecten (bol, lichtstrepen,
  stipjes, gloed, flits) worden getekend in de maat van het afstelbord en met `bnZet` op Amir gezet.
- **Kleuren:** `BN.kleuren` (Pink, Opal, Light blue, Lilac, Gold, Silver); in Test 94 wisselt K. Pink is de keuze van de opdrachtgever.
- **Geluid:** `sounds/bennu_blazen.mp3` op frame `BN.blaasFrame`, `sounds/bennu_vlaag.mp3` bij de vlaag (allebei ElevenLabs), de windvlaag
  van het spel (`playWind` via `startGust`) en een zoemtoon in WebAudio (`bnZoemStart`, `BN.zoemToon`).
- **Instellingen:** uit het afstelbord "Feathers of the Bennu" (artifact), met de waarden van de opdrachtgever op 23-11-2026 (`BN`).
- **Bijgesteld (23-11-2026):** Amir in de animatie was 11% kleiner dan zijn gewone beeld: `bnZet` en `bnBolWereld` namen een frame van
  321,5 px als `CHAR_H`, maar het gewone beeld van Amir is 279 eenheden hoog bij `CHAR_H` 251. Nu `BN.amirPx` (289), zodat hij even groot
  blijft (de bol en de veren groeien mee). En in de bol staat hij echt vast: een slag van een bandiet of de duw van een schildbandiet zette
  `knock` ook als hij onkwetsbaar was, en dan schoof hij weg; nu is `knock` 0 en `world` de plek van het ritueel zolang `bnActief()`.
- **Test 94** (Test levels): de oefenteamgenoot ligt op `level.bennu.x`, ver voor je; hij staat op als de veren aankomen, blijft
  `BN.dummyStaat` s staan en valt weer om. Geen vijanden (`vredig`), dus het terugduwen van vijanden door de bol zit er nog niet in.
- **Nog te doen:** niets meer uit deze lijst; de winkel, het netwerk en de bol als schild zijn gebouwd (zie hieronder, "Live in Co-op").

### Live in Co-op: de zelf-revive en de veren (23-11-2026)

`reviveZelfStap`, `reviveZelfKan`, `reviveOnderweg`, `mpcReviveKomt`, `bnCarry`, `bnVan`, `bnZelfStart`, `bnRitueelStap`, `bnSchild`, `bnBolWereld`, `bnTik`

Op verzoek van de opdrachtgever:
- **Zelf terug, ook met teamgenoten.** Lig je dood met een hart of de veren in de tas, dan gaat het na `ZH.soloWacht` (2 s)
  vanzelf, bij iedere speler zelf (`reviveZelfStap`, naast `zhStap`, niet meer alleen bij de host in solo). Het hart klopt op
  de x en de hoogte van je lijk (`zhStart` met `zelf`, het bericht `zh` met `zelf: 1`), je staat daar op met een leven,
  `ZH.soloOnkw` onkwetsbaar en met je abilities (`zhOpstaan(x, h, zelf)`). Brengt een teamgenoot je intussen al terug
  (`reviveOnderweg`), dan blijft je eigen item in de tas. Leeft je teamgenoot en lig jij niet, dan werkt G zoals eerst.
- **Geen game over zolang het kan.** De stand zegt `rz: 1` als je nog terugkomt; de host kijkt in `mpcDodenStap` met
  `mpcReviveKomt` voor hij `mpcEinde` aanroept. `zhSoloStap` is weg.
- **De veren in de winkel.** `bennu` in `MPC_WINKEL` (tab Team, `speer: true`, 35/50/65, solo 50/80/110), het plaatje
  `items/bennu/veren.png` en het icoon `veren_icoon.png` (`tools/bennu_item.py`, de drie veren uit `verenset.png` in roze).
  Silver Pride is weer alleen van de stokken, ook in solo (`mpcWinkelVoorMij`): met de speer krijg je de veren. In een
  episode gaan ze mee in de tas (`tas.bn`).
- **Het netwerk.** G (`bnToetsMag`, `bnGebruik`) stuurt `bn` (`{voor, x, h, f, dir, kl}`, in `MP_DOOR`); ieder speelt het
  ritueel af in `bnAnder` (`bnVan`), getekend op de plek van de blazer in zijn kleur (`bnCur`), en `pvpTekenEen` tekent zijn
  gewone beeld zolang niet (`bnTekentAnder`). Wie dood ligt staat op zijn eigen scherm op als de veren aankomen (`bnWekT`), waar
  hij lag, zoals na het hart (3 s onkwetsbaar, zonder abilities).
- **Zelf met de veren** (`bnZelfStart`, `bnZelfStap`, `bnZelfTeken`, `bnZelfAlfa`, `BN.zelf`; bijgesteld op verzoek): geen knielen
  en geen bol. Drie veren gaan gloeien op het lijk (`gloei`), de lucht tilt ze rustig op terwijl het lijk vervaagt (`op`), ze
  zweven wiegend in een boog verderop (`vlucht`, met de vlaag van het spel) en daar fadet hij weer levend in terwijl ze om hem
  heen dwarrelen (`in`). De plek kiest de dode zelf (`bnZelfDoel`): `ver` weg van de dichtstbijzijnde vijand (anders naar een
  levende teamgenoot), binnen de wanden, niet in een ravijn, op `terrainH`; hij gaat mee in het bericht (`tx`, `th`).
- **De bol houdt alles buiten** (`bnSchild`, elke stap in `bnStap`, voor elke bol die loopt). `bnBolWereld` rekent de bol om
  naar de wereld (x 1:1, hoogte gedeeld door de schaal). Een vijand uit `straatVijanden()` en `goudapen` met zijn voeten in de
  bol schuift terug naar de rand en zijn `knock` naar binnen vervalt (alleen bij de host, die de vijanden bestuurt). Een
  kruisboogbout, dolk of gifbal die erin vliegt houdt op aan de rand met een rimpeling (`bnTik`), ook bij een gast,
  want die vliegen daar zelf. De blazer was al onkwetsbaar in de bol.
- **Proef:** `node tools/mptest.js --bennu --spelers 2`.

## De outfits van de stoktribe in Co-op en Survival (23-11-2026)

Op verzoek: een speler met de stokken kiest in de lobby (Co-op met 2 of 3, Co-op solo en City Survival) niet meer uit de
oude broekkleuren maar uit de zes outfits van de stoktribe, broek en leeuwenvacht samen (`VACHT.outfits`, zie "De outfits
van de stoktribe" in `notities/stokken.md`): Homefinder, Ice Warder, Dawnbreaker, Firedancer, Moss Cleaver, Show Stopper.
Met de speer blijven het de outfits van Mkuki.

- **De lijst.** `MP_VACHT` (in plaats van `MP_BROEK_OUD`), bewaard in `amir.mpvacht`. `MP_BROEK` is `MP_VACHT` plus
  `MP_OUTFIT`, dus `mpBroekNaam` geeft de naam in Title Case, ook op het kaartje van het team. Het bericht blijft
  `{t: 'broek', id}`; een nieuwe gast krijgt de outfits van de anderen in `pvpGastErbij`, net als de broek eerst.
- **Standaard per slot** (`MP_VACHT_STANDAARD`): de host Homefinder, de eerste gast Firedancer, de tweede Ice Warder.
  Drie andere broeken (paars, ossenbloed, indigo) en drie andere vachten (tawny, goud, wit), zodat je elkaar in een
  gevecht meteen uit elkaar houdt. Paars en indigo liggen dicht bij elkaar, maar daar staan de tawny en de witte vacht
  tegenover. Moss Cleaver (olijf) was het alternatief voor de derde; de asgrijze vacht lijkt dan op de witte niet.
- **Tekenen.** `broekKleurVan` kent de outfits: Homefinder is het tenue zoals het is (geen lapje), de andere `vachtKl(id)`.
  Zo gaat het overal vanzelf: je eigen Amir (`broekNu`), een teamgenoot (`pvpTekenEen`), de lobby (`mpAmirTeken`). Het
  naambordje en het kaartje krijgen de kleur uit `MP_NAAM.kleur` (de broek; bij Dawnbreaker het blond van de vacht).
- **Geen haperingen: gebakken maskers (`VACHT_BAK`).** Eerst rekende `broekLap` per frame het vachtmasker en het
  broekmasker uit, de eerste keer dat het frame getekend werd: 30 tot 40 ms per frame per outfit (gemeten in Chromium),
  dus een hapering bij elke nieuwe beweging, maal het aantal stokspelers. Nu:
  - `tools/vacht_bak.js` bakt per frame dat een stokspeler kan tonen (de stokken, ook goud en klauw, de lage zwaai, de
    bewegingen, de idle) het masker in `karakters/amir_vacht/<frame>`: rood de broek (0 tot 255), groen de vacht, alleen
    de rechthoek om die twee; `lijst.json` geeft per frame die rechthoek. Het script roept `broekMaskers` uit het spel zelf
    aan, met `skinZet(null)` (het opstartlevel heeft een skin, en dan ging `src` van een Amir-frame naar die skin).
    `tools/vacht_bak_pak.py` pakt ze daarna in met een palet (exact): 917 maskers, 1,2 MB.
  - `broekLap` met een masker kleurt alleen nog die rechthoek (`broekKleur`, zonder losse arrays per pixel): 2 tot 5 ms.
    Zonder masker (een nieuw frame) rekent hij het zoals eerst (`broekMaskers`).
  - De lapjes van een outfit staan op de framenaam (`img._skinRel`), niet op het plaatje: het plaatje van een teamgenoot
    (`pvpBeeld`, een eigen Image) en de kleine set krijgen hetzelfde lapje (`lap.w`, `broekBeeld` schaalt). Niet als een
    skin dat frame vervangt (`skinPad`).
  - Vooraf kleuren: in de lobby elk beeld 4 ms (`vachtLobbyStap`, `VACHT_LOBBY`) voor de outfits die nu gedragen worden,
    en wat er dan nog over is achter het laadscherm (`vachtWarmTaken` in `warmBouw`). Wisselt iemand van outfit, dan gaan
    de lapjes van een outfit die niemand meer draagt weg.
  - Nagemeten (Co-op solo, Chromium op 2 cores): laden met een outfit 22,7 s, met Homefinder (niets te kleuren) 23 s;
    eerst, zonder de lobby, 32 s. In het spel komen er geen nieuwe lapjes meer bij (`tools/mptest.js` meldt het).
- **Testen.** `node tools/mptest.js --spelers 2 --stokken host,gast` (of met drie spelers) kijkt na: de standaard per slot,
  iedereen dezelfde outfits, het kaartje, een keuze die bij iedereen aankomt, de lapjes vooraf gekleurd, geen paars in de
  broek over (alle frames, alle outfits: paars dat precies zo bleef binnen 3 px van de omgekleurde broek of een los stuk van
  150 px, hooguit 3%; nu hooguit 2%), en de nieuwe lapjes in het spel. Op deze testmachine (2 cores) crasht een venster met
  drie spelers, ook zonder deze wijziging; met twee spelers is alles OK.
- **Opnieuw bakken** na nieuwe of andere frames van Amir, of een wijziging aan `vachtMasker`, `broekMaskers`, `BROEK` of
  `VACHT` (zaad, groei, eiland): `node tools/vacht_bak.js` (met `--alleen <pad>` voor een deel), daarna
  `tools/gen-offline-manifest.py`.


## De winkel als kamer (24-11-2026)

De winkel van Co-op is geen paneel meer maar de winkelkamer zelf (ontwerp in het project: `claude/winkel_c_ontwerp.md`).

De inrichting (26-11-2026): de toonbank staat op -21020 (`MPC_WINKEL_KAMER.toonbank`, was -21250), zodat de doorgang met het
doek achter Duka helemaal in beeld staat; het linkerraam (-20850) en de paal (-20725) schoven mee. Kivuli versie 2 rekent vanaf
de toonbank en leunt daarom op 570 (was 800), tegen de muur voor de straatdeur. Schuif je de toonbank weer, kijk dan ook `KIV.plek`
na (`node tools/kivuli_test.js 2 1`).
Opent E bij de toonbank de winkel en staat Amir in een kamer met `winkel` (`wkkKan`), dan gaat `wkk.aan` en krijgt
`#winkelui` de klasse `kamer`: het oude paneel is weg, het spel loopt door (`paused = false`, de toetsen kiezen alleen), zodat
de marktman en de teamgenoten bewegen.

- **Tekenen** (`wkkTeken`, vanuit `winkelAchter` in plaats van de planken van de kamer): de uitstalplek op `winkel.x + WKK.standX`.
  Voor de categorie met `stand: 'rek'` het wapenrek uit de stad met de speren rechtop (of de stokken als plaatje), anders een
  plank van de winkel (`plank_touw.png` via `winkelMetSchaduw`, breder en leeg, `wkkPlank`). De bordjes, de prijslabels en de
  gloed van het gekozen ding gaan in `wkk.na` en worden in `binnenNa` na het schemer getekend (`wkkNaTeken`), anders dimt de
  kamer ze. Voor de muis bewaart `wkkScherm` per ding en bordje de rechthoek op het scherm (de transformatie van het moment).
- **Niets onder het doek** (26-11-2026): de bordjes hangen in een blok van twee bij twee (`WKK.bord.kol`), de bovenste rij aan
  de balk, de onderste aan de bovenste. Elk beeld leest `wkkDoekRand` de linkerrand van het doek (DOM) en rekent die terug
  naar de tekencoördinaten; staat de uitstalplek te ver naar rechts (een gast, wiens camera zijn eigen Amir volgt, zag Team
  onder het doek verdwijnen), dan schuiven de uitstalplek en het blok naar links tot ze `WKK.marge` naast het doek staan.
- **Wat waar ligt**: `WKK.waar` (artikel naar categorie). Een artikel met `eis` dat zelf niet op een uitstalplek ligt is een upgrade
  van zijn ouder en staat als icoontje in het doek (`wkkOuder`, `wkkUpgrades`): Full Circle: more damage en all around, Ardhi's Roots.
  Give 5 gold staat bij Team, een keer per teamgenoot.
- **Besturing** (`wkkToets`): links en rechts kiezen, omhoog en omlaag (of Q, Tab) wisselen de categorie, Enter of spatie koopt,
  Backspace is Undo, R is Ready; Escape en E sluiten zoals altijd.
  E bij de deur naar de straat (de sierdeur rechts) is ook Ready (`WK_DEUR`, `wkDeurE`): de eerste E vraagt "Ready to leave?"
  (een hint en een label boven de E), een tweede E binnen 3 s zet Ready; ben je al Ready, dan is E daar meteen Not ready.
  `tools/mptest.js --proef --winkeleerst` kijkt het na.
  Duka verspringt niet meer bij het in- en uitgaan: `mpcWinkelIn` en `mpcWinkelUit` roepen `winkelGeheimZet` met `houd`, zodat
  hij staat waar hij stond (alleen na een betrapping begint hij opnieuw op zijn plek). De muis: hover en klik kiezen, een dubbelklik koopt (`mpcDubbelKlik`, een enkele klik nooit), een
  klik op een bordje wisselt (`pointermove`/`pointerdown` met capture).
- **Het doek** (`#wkkamer`, `wkkToon`): naam, upgrade-label, uitleg, citaat, de upgrade-icoontjes met een hover-kaartje (`wkkTip`),
  de prijs, en de knoppen Buy, Leave, Ready en Undo. De regel bovenin (`.wkk-bericht`) spiegelt `#wkuitleg` en `#wkvertrek` van de
  oude winkel. Kopen, Undo en Ready zijn ongewijzigd (`mpcWinkelKoop`, `mpcUndo`, `mpcKlaarDruk`); `mpcWinkelToon` vult het oude
  paneel nog (verborgen) en roept daarna `wkkToon`.
- **Zonder winkelkamer** (het Duel, `pvp.dw`) blijft het oude scherm met tabs en kaarten.
- **Onderdelen**: `design/winkel_ui/` (doek, label, knop, munt uit Grok, bronvel in `bron/`), lettertype Bree Serif
  (`design/fonts/bree-serif.woff2`, OFL). `tools/winkel_mockup.js` tekent de oude mockup na.
- **Open**: de stipjes van teamgenoten boven wat zij bekijken (nog geen netwerkbericht), de marktman die naar het rek loopt, eigen
  uitstalplekken voor Charms en Team (nu ook een plank), citaten voor artikelen zonder citaat. De stap in `mptest.js --proef` die
  alle kaarten tegelijk verwacht klopte al niet meer sinds de tabs (22-11) en faalt nog steeds op dezelfde manier.

## Kivuli, de reizende handelaar (25-11-2026)

Bij een op de drie winkelbezoeken van Co-op Survival (niet in de Co-op episode) staat Kivuli in de winkel en is Duka er nog niet.
Welk bezoek dat is gaat met een knikkerzak van drie, een raak (`C.kivZak`, een verse zak per potje), dus twee bezoeken
achter elkaar kan, en drie zonder ook. Vroeger kwam hij alleen bij het eerste bezoek; dat kan nog met **Kivuli comes**.
De host besluit het in `kivBesluit` en stuurt het mee met `{t:'winkel', g, kv}`; `mpcWinkelIn(geheim, kv)` zet het bij
iedereen op (`kivStart`). Lobby: **Kivuli comes** (`kivVaak`: 1 in 3 shops, Every shop, First shop only), **Kivuli in the shop** (Random, At the counter, Walks in, Flips a coin, Off) en
**Duka after Kivuli** (Sometimes, Always, Never); Random en Sometimes gaan met een knikkerzak (`kivZak`).

- Versie 1: hij staat al in de kamer, loopt een stukje naar de toonbank en kijkt over zijn schouder naar het team.
- Versie 2: de kamer is leeg; komt iemand bij de toonbank (`KIV.plek[2].nadert`), dan zegt de host `kivin` en komt hij
  door de deur rechts binnen (een sierdeur met indigo doek: `sierDeuren` in de kamer, `MPC_WINKEL_KAMER.deur`, alleen beeld)
  en leunt bij de muur. Weggaan doet hij in elke versie door die deur.
- Versie 3: zonder kap aan de toonbank; als het team binnen is zet hij zijn kap op en gooit hij een muntje op.
- E bij hem (`binnenEBij` soort `kivuli`, `kivPraat`): zijn jas gaat open (wat je zelf ziet zolang jouw winkel open is) en
  de winkel opent, nog in de indeling van Duka, met alleen zijn voorraad (`wkkZichtbaar`): altijd de kalebas en 2 of 3
  andere dingen zonder eis. Elk ding een keer voor het hele team: wie koopt, haalt het weg (`kivweg`, `kivWegUit`), geen
  Undo. De eerste die hem aanspreekt start de klok van 45 s voor iedereen (`kivpraat`, de klok bovenin: `kivKlokToon`).
- Op nul (`kivVertrek`): winkel dicht, jas dicht, korte draai, weg naar rechts. De draai-clip zet vanaf frame
  `KIV.draaiStap` (7) al stappen, dus vanaf daar schuift hij mee (anders liep hij op zijn plek). Komt Duka (`kv.duka`), dan
  komt hij pas uit de achterkamer als Kivuli `KIV.dukaBij` (200) van de deur is, zodat hij hem nog net ziet vertrekken, en loopt hij
  naar zijn plek ("Who was THAT?", of "You bought WHAT from him?" als er iets gekocht is) en gaat de winkel
  gewoon verder. Komt hij niet: even stil, een windvlaag, "Duka didn't come." en de host stuurt het team de straat op.
- Zolang Kivuli er is doet E bij de toonbank niets en is Duka niet te zien (`kivDukaWeg`, `kivToonbankDicht`).
- De sfeer (`KIV.sfeer`, `kivSfeer`, blok "Kivuli: de sfeer"): zolang hij er is (`kivSfeerWil`) wordt de kamer donker (`kivDonkerNa`
  in `binnenNa`, een multiply met een lichtpoel rond de lantaarn, `donker` 100,92,124, in 1,7 s aan en 1,9 s uit), staat zijn
  lantaarn bij zijn voet (`kivLampPos`, `kivLampTeken` in `kivTeken`; loopt hij, dan draagt hij hem en zwaait hij) en speelt
  `music/kivuli.mp3` (naadloze lus van de Suno-track "Kivuli's Lantern", loudnorm -16 LUFS, peak -1,7 dB) boven de gewone
  muziek (`kivMuzStap`, 50 ms klok: fade in 1,8 s, fade uit 2,6 s, `bg` zakt naar 12%). De lamp gaat aan met de fakkelframes
  24 tot 17 achterstevoren, brandt met frame 1 tot 16 en dooft met 17 tot 24 (`design/fakkel/frame_NN.png`, alleen de
  vlam, crop 8,2,114,220). Rustige flikker (`kivFlikker`, drie sinussen van 1,8%, 1,2% en 0,8%), warme gloed, lichtvlekjes
  van de doorboorde lantaarn op de muur en stofjes die in de lichtcirkel oplichten. De lantaarn is dof en zacht
  (`design/kivuli/lantaarn_uit.png` en `_aan.png`, `tools/kivuli_lantaarn.py`, bron in `design/kivuli/bron/`): hij moet
  nauwelijks opvallen. Kivuli's frames zijn half getemperd met dezelfde dimstap als Duka's versies (`DIM` 0,5 in
  `tools/kivuli_knip.py`; `--temper` deed dat eenmalig op de bestaande frames, stempel `karakters/kivuli/.getemperd`).
  Elke winkel begint de sfeer uit (`kivStart`).
- Zijn lachje met de mond dicht (`sounds/kivuli/lach.mp3`, ElevenLabs Sound Effects, gekozen door Tom) speelt heel soms
  (`kivLach`, knikkerzakken): 1 op 3 bij psst, 1 op 3 bij een aankoop, 1 op 2 bij zijn vertrek.
- Wat hij zegt staat in `KIV_ZEG` (wolkjes boven zijn hoofd met `kivWolk`, en in de tekstballon van de winkel via `mpcZeg`).
- De frames: `tools/kivuli_knip.py <map met de mp4's>`, naar `karakters/kivuli/`. Testen: `node tools/kivuli_test.js
  <versie> <duka 1|2>` maakt schermafbeeldingen van een heel bezoek.
- Hij verkoopt zijn eigen spullen (zie hieronder), een per speler per bezoek.
- De mantel (zijn eigen scherm, `kivMantel`, blok "de mantel van Kivuli"): met E bij hem opent niet het doek van Duka maar de
  binnenkant van zijn mantel (`design/kivuli/mantel.png`, 838x646 met grote prijskaartjes: zijaanzicht, de jas hangt aan zijn schouder en zijn opgeheven arm slaat de voorflap open, petrol voering, uit een Grok-plaat; de eerdere voorkant uit `_kivuli/cloak6b.png` is vervangen omdat de spullen op de binnenflap horen te hangen). Zes haken in twee kolommen van drie
  (`KM.pos`, % van de plaat), 3 of 4 gevuld uit zijn voorraad op vaste plekken per bezoek (`kivSlots`, een schudbeurt op de
  inhoud, dus bij iedereen gelijk), het prijslabel als pil onder het ding, en onder het paneel een donkere plaquette met het gekozen ding groot links (`#kmgroot`), de naam, de uitleg en zo nodig
  waarom het niet kan (`#kmbox`, vaste hoogte, de tekst krimpt tot hij past, `--k`). Hover of klik kiest (goud gloeit), een dubbelklik (`mpcDubbelKlik`), Enter of Buy
  koopt; pijltjes en Tab lopen langs de gevulde haken. Het paneel staat aan de kant tegenover hem (`kivMantelKant`: hij links
  van 40% van het scherm dan rechts, rechts van 60% dan links, in het midden de kant waar Amir niet staat; `kiv.sx` en `kiv.ax`
  zet `kivTeken`), de tekstballon van de marktman springt naar de andere kant (`kmlinks`). Een gekocht ding is weg voor
  iedereen en zijn haak is leeg (`kivWegUit`). Bij hem geen bordjes of uitstalplek (`wkkTeken` doet niets), het oude doek, Ready,
  Undo en de berichtbalk zijn weg (CSS `#winkelui.kivm`). Knoppen: Buy, Close (alleen mijn mantel dicht, E opent hem weer) en
  Done (R): drukt het hele team Done (`kiv.klaar` per speler, bericht `kivklaar`), dan loopt hij na 1,6 s (nog terug te draaien met
  Not done) vroegtijdig weg in plaats van de 45 s af te wachten (`kivAllesKlaar` in `kivStap`). Alleen de eerste die hem aanspreekt
  zet de klok; Done telt pas als de klok loopt.

## De spullen van Kivuli en de itemslots (25-11-2026)

Kivuli verkoopt vijf eigen spullen (`MPC_WINKEL` met `kivuli: true`, alleen te zien bij hem: `wkkZichtbaar`), naast de
kalebas. `kivBesluit` kiest er 2 of 3. Ieder koopt er hooguit een per bezoek (`islotKivKoop`, "Kivuli sells you only one
thing."). Een gekocht ding gaat in je tas (`islotTas`, in de inventory onder I); daar zet je het zelf in **slot R** of
**slot T** (`islotZet`, de knoppen Slot R en Slot T). R en T gebruiken het (`islotToets`), herstarten is nu **Shift+O**
(overal: ook dood, na het eind en in het Duel; R herstart nergens meer), en het oefendoel van de sandbox staat op **Y**. De actiebalk
heeft twee vakken erbij (`islot0`, `islot1`) met het plaatje en het aantal.

| ding | prijs | wat |
| --- | --- | --- |
| Sack o' Bones | 25 | een witte stofwolk van 6 s (1,725 Amir breed, 1,65 hoog), hij verblindt niemand; wie erin staat (ook een teamgenoot) wordt door geen projectiel geraakt: bout, dolk, gif en vogel vliegen erdoor (`islotInWolk`) |
| Sack o' Fangs | 30 | de zak valt op de looplijn, een zwarte slang met gouden banden komt eruit en bijt steeds de dichtstbijzijnde vijand, 5 beten (elk een treffer); de vijanden negeren hem |
| Jar o' Fire Ants | 25 | een muur van mieren, 5 s, een Amir breed, voor je; vijanden komen er niet door en wie erin staat deinst terug, projectielen vliegen eroverheen |
| Oil of Mirrors | 35 | 5 s onzichtbaar voor vijanden (jij en je team zien je op 40% met een glasrand); ze vallen niet aan maar rennen zoekend rond; aanvallen maakt je zichtbaar |
| Ketemba Clay | 30 | 8 s klei onder je voeten: niet springen, 15% trager, dubbele schade (bovenop de bonus van je wapen); plakstappen, een hardere klap en kleiklonten van je voeten |

Hoe het werkt (zoek op `ISLOT`):
- `islotStart(m, zelf)` start een effect, bij iedereen: de gebruiker stuurt `{t:'isl', k, x, h, f}` (in `MP_DOOR`). De
  host denkt voor de wolk, de slang en de mieren (`islotStap`), net als voor de vijanden; treffers gaan via `islotRaak`.
- Mirrors: `mpcDoel` slaat een onzichtbare speler over. Tijdens de update van de vijanden zoekt elke vijand een eigen
  zoekpunt binnen 5 Amir van de plek waar je verdween (`islotMirZoek`, nieuw als hij er is of na 1,5 tot 3,2 s), en
  `islotMirOm` draait de update in twee groepen (wie naar links zoekt, wie naar rechts) met het doel telkens een stuk
  voor de groep uit (`ISLOT.mirrors.voor`, per soort `voorK`: 3,5 Amir, 6 voor schildbandiet, zweepman, schorpioen en
  fosforslang, 8 voor de hyena, 30 voor de kruisboog), zodat niemand binnen zijn aanval komt. Zo rennen ze zoekend
  rond en slaan ze niet; een vijand die door je heen loopt merkt niets. `camSwap` gaat daarbij op null, want
  `playerX` leest die voor `world`. Aanvallen maakt je zichtbaar (`islotMirEind`, `{t:'islm'}`). Op verzoek van de
  opdrachtgever: eerst zochten ze op de plek waar je verdween en sloegen ze daar in het niets.
- Clay: `islotDubbelNu` zet `critNu` voor de speer en vermenigvuldigt `straalSchadeK` voor de stokken; een gast stuurt
  `x2` mee in zijn treffer (`mh`). De stappen: `sounds/kivuli/klei_stap1.mp3` en `klei_stap2.mp3` (ElevenLabs, gekozen
  door Tom, even hard als de gewone stappen), de klap `sounds/brutus_raak.mp3`.
- **Iedereen ziet de effecten** (27-11-2026, op verzoek). De wolk, de slang, de mieren en Mirrors kwamen al bij iedereen
  aan (`isl` in `MP_DOOR`); de mieren waren alleen donkerbruin en lazen als een bloedvlek, zeker in de avond en de nacht.
  Nu: een donkere rand, een vuurrood lijf, een glimpje en een rode gloed op de grond die met de muur meegroeit. Ketemba
  Clay was alleen bij de gebruiker te zien; nu houdt elke ander per speler een klok bij (`islotKleiAnder`) en laat
  `islotKleiAnderStap` om de 0,42 Amir die de teamgenoot loopt een klontje en een zachtere smak bij zijn voeten vallen.
  Proef: `node tools/mptest.js --islotzien` (de gast gebruikt alle vijf, de host en de tweede gast moeten elk effect hebben).
- Bazen zitten niet in de vijandlijsten, dus de mieren en Mirrors werken niet op een baas.
- Beelden: `items/kivuli/*.png` (Grok, gekozen door Tom); de slang `enemies/slang_kivuli/` uit `tools/slang_kivuli.py`.
- Sandbox: de rij **Kivuli items** stopt er een in je tas. Testen: `node tools/islot_test.js [map]`.
