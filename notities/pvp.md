# PvP: een tegen een over internet

`PVP`, `PVP_LEVEL`, `pvpHost`, `pvpJoin`, `pvpVerbonden`, `pvpStap`, `pvpVang`, `pvpTeken`, `pvpRondeUit`, `pvpStop`

De knop **Multiplayer** in het hoofdmenu (`btnpvp`, het scherm `menuPvp`). De een drukt op **Host a game** en krijgt een code van
vier letters, de ander tikt die in en drukt op **Join**. Daarna staan ze in de lobby (zie `notities/multiplayer.md`), en
kiest de host Duel, dan spelen ze allebei het stadje `PVP_LEVEL` (`pvpDuelStart`).

## De verbinding

- WebRTC met PeerJS (`PVP.lib`, van jsdelivr, pas geladen bij Host of Join met `pvpLib`, zodat het menu er niet op wacht).
  De openbare PeerJS-server koppelt de twee een keer: de host heet daar `PVP.pre` plus de code. Daarna gaan de berichten
  rechtstreeks. Geen eigen server, geen account. Thuis werkt dat bijna altijd; achter een strenge router kan het mislukken
  (dan zie je een foutmelding), en dan is een TURN-server of een eigen doorgeefluik de volgende stap.
- Onderweg zegt het scherm waar het is: Loading, Reaching the server, Calling, Found each other (`pvpWaakStart` kijkt elke
  halve seconde naar `iceConnectionState`). Mislukt de rechtstreekse lijn (`failed`) of duurt het langer dan `PVP_GEDULD`
  (25 s), dan staat er waarom, in plaats van eeuwig "Connecting...". Komt de joiner na 12 s niet bij de server, ook.
- `PVP_ICE`: STUN van Google, en als vangnet de gratis openbare TURN-server van Open Relay (openrelay.metered.ca, met de
  openbare gebruikersnaam en het wachtwoord). Nodig voor een telefoon op mobiele data: die zit vaak achter een NAT waar
  rechtstreeks niet doorheen komt (de eerste proef, iPhone tegen laptop, bleef op Connecting staan). Een gratis dienst kan
  verdwijnen of traag zijn; werkt hij niet meer, dan is een eigen TURN (Metered of Cloudflare, met een account) de stap.
  Die staat in de wacht: online spelen is voorlopig voor laptops (zie "Voor wie" in `notities/multiplayer.md`).
- **Het relais** (`PVP_RELAY`, `pvpRelayLuister`, `pvpJoinRelay`, `pvpRelayConn`): de TURN-servers zonder account bleken niet
  te helpen (de iPhone op mobiele data gaf "negotiation-failed": ICE mislukt). Daarom probeert de gast eerst rechtstreeks,
  en na een fout of `PVP_RELAY.na` (8) seconden gaat hij via een openbare MQTT-broker (HiveMQ, EMQX of Mosquitto, de eerste
  die antwoordt; mqtt.js lui van jsdelivr of unpkg). Dat is een websocket over https, dus het komt door elk netwerk. De host
  luistert vanaf Host meteen op allebei. Onderwerp: `PVP_RELAY.pre` plus de code, `/h/<sid>` naar de host (hij luistert op
  `/h/+`) en `/g/<sid>` naar die gast, zodat met twee gasten ieder zijn eigen onderwerp heeft; de gast roept `relayHallo`
  met zijn `sid` tot de host `relayOk` antwoordt (of na `bel` seconden opgeeft). Elk bericht draagt de `sid`. Via het relais 15 berichten per seconde (`PVP_RELAY.hz`). Openbaar en zonder garantie: wie de code en het
  voorvoegsel kent kan meelezen (alleen posities), en valt een broker weg dan pakt het de volgende uit de lijst.
- **Hartslag**: hoort een kant `PVP.stilte` (15) seconden niets, dan is de verbinding weg en gaat hij terug naar het menu.
  De ping (zie "De netcode") loopt los van het spel door, dus ook een pauze houdt de verbinding nu levend.
- De service worker laat andere hosts met rust (`sw.js`, `url.origin`), dus de bibliotheek komt altijd van internet. Offline
  is er geen PvP.
- Deze sandbox (de cloud waar Claude in werkt) mag PeerJS niet bereiken; daar is het getest met een nagebootste `Peer` die
  de berichten tussen twee browservensters doorgeeft.

## De netcode: het snelle kanaal, de speelbuffer en de ping

Het blok `// ---- multiplayer: de netcode ... ----` (`PVP_NET`). Stap 1 van het plan voor vloeiend online spelen (november
2026); stap 2, drie spelers, is gebouwd (de ster: een verbinding per gast, zie "Drie spelers: de ster" in
`notities/multiplayer.md`); stap 3, een eigen TURN-server, staat in de wacht: online spelen is voorlopig voor laptops,
een telefoon op mobiele data hoeft niet (zie "Voor wie" in `notities/multiplayer.md`). Alles hieronder geldt per lijn: het snelle kanaal per peer
(`pvp.peers[p].snel`), de speelbuffer en de klok per afzender (`pvp.nets[p]`), de ping per lijn (de host naar elke gast).

- **Het snelle kanaal** (`pvpSnelOpen`, `pvpZendSnel`, `pvpSnelAan`). PeerJS opent een betrouwbaar kanaal: op volgorde, en
  een verloren pakket wordt opnieuw verstuurd terwijl alles erachter wacht. Daarnaast openen allebei de kanten op dezelfde
  lijn een tweede datakanaal, zonder volgorde en zonder opnieuw versturen (`negotiated` met id `PVP_NET.kanaal`, zodat er
  niets onderhandeld hoeft en de `ondatachannel` van PeerJS er niet van weet). Daarover gaan alleen de standberichten (`s`,
  `v`) en de ping. Elk draagt een volgnummer `q`; een bericht dat na een nieuwer binnenkomt valt weg. Zit de buffer van het
  kanaal vol (`PVP_NET.vol`), dan slaat hij een bericht over. Gebeurtenissen blijven op het betrouwbare kanaal. Via het relais
  is er geen snel kanaal: daar gaat alles zoals eerst.
- **De speelbuffer** (`pvpNetIn`, `pvpNetSpeel`, `pvpNetKlok`). Elk standbericht draagt de klok van de afzender (`tm`,
  `performance.now`). De ontvanger schat het verschil tussen de klokken uit de kortste reistijd van de laatste
  `PVP_NET.venster` seconden, en speelt een bericht pas af als het oud genoeg is. Hoe oud hangt af van de lijn: de spreiding
  van de reistijd (`PVP_NET.spreid`, een enkele uitschieter telt niet) plus `PVP_NET.marge` keer de tijd tussen twee
  berichten, tussen de grenzen van `PVP_NET.buffer`, en hij schuift er langzaam naartoe (`bufStap`) zodat niemand verspringt.
  De andere Amir staat dan tussen twee bekende standen in (`pvpAnderStap`, zijn speer in de vlucht ook), in plaats van naar de
  laatste plek te schuiven zoals eerst (`PVP.volg`, weg). Verder dan `PVP_NET.sprong` tussen twee standen (een nieuwe ronde)
  springt hij meteen. Is er nog geen volgende stand, dan blijft hij op de laatste staan. Doorrekenen in de richting waarin hij
  ging is geprobeerd en weer weggehaald: bij vijanden die plots stoppen of uitvallen schoot het voorbij, en de afwijking werd
  op een slechte lijn drie keer zo groot.
- **Wie beslist met welke stand.** Het beeld en de treffers gebruiken de gebufferde stand (`pvp.anders[p].g`), zodat wat je
  ziet ook is wat telt. De host laat de vijanden achter de nieuwste stand van een gast aan gaan (`pvp.anders[p].nu`,
  `pvpAnderNu(p)`), want de gebufferde loopt 0,1 s achter.
- **De ping** (`pvpPingIn`, `pvpPingTekst`): elke `PVP_NET.ping` seconde `pi` en terug `po`, over het snelle kanaal. In de lobby
  onder de eerste regel (`#mpping`, met de soort lijn: direct, direct met het snelle kanaal, of relay) en in de HUD.
- **Testen:** `tools/mptest.js --net 60,25,0.05` bootst 60 ms vertraging, tot 25 ms jitter en 5% verlies na (het betrouwbare
  kanaal wacht dan op volgorde, het snelle verliest gewoon), met een nagebootst snel kanaal; `--geensnel` zonder. Aan het eind
  de ping, en hoe goed het beeld van de andere Amir en van de vijanden bij de gast de echte baan volgt: bij de best passende
  vertraging de gemiddelde afwijking in px. De eerste meting (november 2026, 50 s met bandieten en hyena's):

  | lijn | wat | oud | nieuw |
  | --- | --- | --- | --- |
  | 60 ms, 25 jitter, 5% verlies | de andere Amir | 1,0 tot 2,4 px | 0,5 tot 0,6 px |
  | | de vijanden bij de gast | 1,1 px, 240 ms | 0,11 px, 240 ms |
  | 80 ms, 40 jitter, 20% verlies | de andere Amir | 1,3 tot 2,0 px, 290 ms | 0,8 tot 0,9 px, 220 ms |
  | | de vijanden bij de gast | 0,2 px, 410 ms | 1,1 px, 280 ms |

  Op een slechte lijn ruilt het een tikje afwijking bij de vijanden voor 130 ms minder achterlopen. De ping in de test is
  hoger dan de nagebootste lijn, want het doorgeven door Node kost zelf ook tijd. Een echte proef over internet kan alleen
  buiten de cloud (PeerJS is daar niet te bereiken).

  Met drie spelers (`tools/mptest.js --net 60,25,0.05`, standaard drie vensters) volgt de host de gasten even goed als met
  twee; een gast ziet de andere gast een sprong later (zo'n 320 tegen 210 ms bij de host), want die stand gaat via de host.
  De getallen schommelen in de cloud sterk met de belasting van drie Chromium-vensters tegelijk.

## Wat er over de lijn gaat

- `s`, 20 keer per seconde (`PVP.hz`), over het snelle kanaal met `q` en `tm` (en in Co-op bij de gast `ak`, zie
  `notities/multiplayer.md`): plek (`x`, `h`), kijkrichting, het plaatje waarmee Amir net getekend is
  (`pvpVang`, vlak voor de `drawImage` van zijn lijf: het pad van het plaatje en de rechthoek in sprite-eenheden vanaf zijn
  voeten, en of het gespiegeld is), `hurt` (de rode flits), de steek (`sf` het frame, `sl` of hij raakt, `sn` een teller
  per steek), de lage zwaai (`sw`, `wn`), de geworpen speer (`j`, met een teller `n` per worp) en de levens.
- `au` (ik ben geraakt), `speerRaak` (jouw speer zit in mij: die valt dan neer), `ko` (ik ben dood), `ronde` (de host
  start een ronde of meldt het einde), `rematch`, `bye`; `pi` en `po` de ping; `welkom` (je slot), `vol` (geweigerd),
  `weg` (een gast is weg). Elk bericht draagt `p`, het slot van wie het maakte, en een bericht voor een andere gast `naar`.

## Wie beslist

De laptop van wie geraakt wordt. `pvpTeken` (in het tekenblok, na `hitBy` en `pbox`, voor de slangen) tekent de andere Amir
en kijkt of zijn steek (de punt uit `TIP_DX`/`TIP_Y`, net als bij een vijand), zijn lage zwaai (`SWEEP_REACH`,
`SWEEP_HIGH`) of zijn speer de eigen `pbox` raakt, en roept dan gewoon `hurtPlayer`. Zo telt de rol (onkwetsbaar via
`invuln`) vanzelf mee. Voor de speer telt het hele stuk sinds het vorige bericht, anders vloog een snelle speer tussen
twee berichten door hem heen. Elke steek, zwaai en worp raakt een keer (`raakSteek`, `raakZwaai`, `raakSpeer`). De vorige
plek van de speer (`jVorig`) wordt elk beeld bijgewerkt, ook als je onkwetsbaar bent: eerst niet, en dan raakte een speer
waar je net doorheen rolde je alsnog zodra de rol voorbij was.

De aanvaller merkt zijn treffer (`pvpRaakFx`, op het bericht `au`): het geluid van een speer in vlees, een hitstop van
0,06 s en een kleine schok (`PVP.raak`). Daarvoor zag hij alleen de rode flits, die pas met het volgende standbericht kwam.

Het Duel is een tegen een (`pvpDuelAnder`); met drie spelers in de lobby mag het niet starten. De andere Amir komt uit de
speelbuffer (zie "De netcode"); springt hij meer dan `PVP_NET.sprong` (een nieuwe ronde), dan
staat hij er meteen. Boven zijn hoofd een rood pijltje en zijn drie levens.

## Rondes

Standaard best of 3, elke ronde 3 levens; de host stelt dat in de lobby in (`pvp.winst`, `pvp.levens`, zie `notities/multiplayer.md`). Wie doodgaat stuurt `ko`; de host telt de stand, wacht `PVP.pauze` en
start de volgende ronde (`restart`, dan `pvpPlaats`: de host rechts op `-250`, de gast links op `-2550`). Tussen twee
rondes is iedereen onkwetsbaar (`godMode`). Na het duel vraagt R een rematch; die begint pas als allebei R drukten
(`opnieuw` stuurt in PvP naar `pvpRematchDruk`). Het dood-scherm komt in PvP niet.

## De kit

Basis plus de rol: lopen, sprinten, springen, bukken, steken, lage zwaai, werpen (een speer in de hand, een op de rug) en
de rol. Geen talents (`runReset`, en `levelList` is `PVP_LEVELS`, niet `TEST_LEVELS`, want die geeft alle talents en een
vierde leven), geen draaislag (`combo: false`). De rol heeft in PvP een afkoeling van 1,2 s in plaats van 0,5 (`PVP.rolKoel`,
in `pvpVerbonden` gezet en in `pvpStop` teruggezet), zodat je niet elke worp wegrolt.

## Het stadje (`PVP_LEVEL`)

Drie huizen: twee lage (twee hoog) aan de kanten en een hoog koopmanshuis in het midden, steegjes van 1,4 Amir. Een
galerij op 401 loopt over alle drie. Een rieten kraam aan elke kant: van het dak (264) spring je op de galerij. In de
steegjes een stadstrap (E) van de galerij naar een balkon op 730 aan de buitenkant van de lage huizen, en van daar het
dak op (771). Het hoge middenhuis heeft geen weg omhoog. Een ton met een kalebas in het midden van de straat. Nagemeten:
beide kramen naar de galerij en beide trappen. `geenEinde`: het duel eindigt op de rondes, niet bij fakkels.

**De randen (`huisMarge`, `huisMargeStap`).** Links en rechts ligt 3,5 Amir vrije straat naast de buitenste muren, op elk
scherm: de huizen groeien mee met het scherm (en schuiven door `aan`), de grenzen in de wereld niet, dus `huisMargeStap`
(aangeroepen uit `endWall` en `cliffAt`) zet bij elke nieuwe schaal de rechtergrens (`rechtsWall`) en de linker rotswand
opnieuw. Vroeger lag de rots vast op -2950: op de laptop links twee keer zoveel straat als rechts, en op 1920x1080 stond
het linkerhuis half in de rots. De rots is kleiner (`s: 1.6`, de inktlijn is dan dunner en de top valt nog buiten beeld) en
heeft `voor: 2.2`: de grens ligt 2,2 Amir voor de wand, tegen een rotsval van rotsdecor (`props` met `aanRots`, x in Amir
vanaf de wand, schuift mee) met een zachte schaduw eronder. In Co-op branden 's nachts twee fakkels in de rots
(`MPC_VERSIE.rots`, in `mpcFakkelsStap`). Let op: elke speler rekent met zijn eigen scherm, dus de grenzen liggen per
laptop op een andere wereld-x (net als de huizen zelf al deden).

## Wat nog kan

- Nagerekend (november 2026): de steek raakt pas vanaf zo'n 0,65 Amir afstand (het raakvak zit rond de punt), en spelers
  lopen door elkaar heen, dus van dichtbij gaat de steek over de ander heen. De opdrachtgever ziet dat mogelijk als
  gameplay (van dichtbij is een speer zwak, met het oog op andere wapens), eventueel met een ability ervoor; niet
  zomaar dichtmaken.
- De lage zwaai is sterk: eerder, langer, aan beide kanten en zonder dode zone. Temperen alleen in PvP kan met een getal
  in `PVP`, zoals `rolKoel`.
- Het slachtoffer beslist met een vertraagd beeld van de aanvaller (netwerk plus de speelbuffer): een steek die bij de aanvaller
  raakt, kan bij de ander missen. Terugrekenen (lag compensation) is nog niet gedaan.

- De andere Amir heeft dezelfde kleuren als jij; alleen het pijltje maakt het verschil.
- Zijn speren op de rug, de schaduw en het licht op hem worden niet getekend.
