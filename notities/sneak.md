# Sneak: de sluipaanval, gehoor en de argwaanklok

Kop in de HTML: `// ---- sneak: de sluipaanval, gehoor en de argwaanklok (level.sneak, zie notities/sneak.md) ----`,
direct na `zichtTeken` en voor `TRIGGER`. Grep: `SNEAK`, `sneakAan`, `sneakKan`, `sneakDoe`, `sneakRust`, `lawaaiPuls`,
`sneakHoort`, `sneakOogTeken`, `sneakPatStap`.

## Wat het is

Met `sneak: true` in een level (naast `zicht: true`, zonder zicht doet het niets) kan Amir een vijand die hem
niet opgemerkt heeft van achteren in een klap doden. Het bouwt op het zicht (`notities/zicht.md`): een vijand
begint in rust (`s.zWacht`) en wordt wakker als hij Amir ziet. Het zicht had achter zijn rug nog de oude
afstand (een half scherm op zijn niveau), dus van achteren naderen kon niet. De sluipaanval vervangt dat
achterbereik door gehoor, alleen voor de mens-vijanden: bandiet, schildbandiet, kooiman, meelman,
kruisboogbandiet en zweepman (`oog === 'mens'` in `vijandZiet`, dat zet `s.sMens`). Slangen, schorpioenen,
hyena's en de panter kijken zoals ze deden; een baas doet niet mee.

## Gehoor (`lawaai`, `lawaaiPuls`, `sneakHoort`)

Elk beeld zet de hoofdlus `lawaai`: hoe ver Amirs voetstappen nu dragen (`lawaaiNu`). Kruipen en stilstaan zijn
stil, lopen draagt `SNEAK.gehoor.loop` (1,8 Amir, net buiten steekafstand), sprinten (en de renstoot) tot het oude
zichtbereik (`zichtBereik(1100)`). In de lucht is hij stil (`gehoor.lucht` 0): springen en van een muurtje vallen
maakt geen geluid, zo kom je achter een patrouille. Voetstappen op een andere vloer (een terras, een blok) hoort hij
ook niet (`zichtNiveau`). Een vijand in rust hoort je als je binnen die afstand op
zijn niveau staat (`zichtNiveau`). Daarnaast zijn er pulsen op een plek (`lawaaiPulsen`, `SNEAK.puls`, elk
`duur` 0,35 s): het loslaten van een speer (klein, alleen vlakbij te horen, zodat een worp van achteren kan),
een treffer op een vijand (in elke `hitX` en in `enemyTakeHit`, `hitHyena`), een klap op Amir (`hurtPlayer`),
een speer die neerkomt (`javStick`) en een sluipkill (klein). Een puls gaat door hoogte heen. Alles staat in
Amir (`sneakPx`), want de steek reikt op een telefoon minder pixels dan op een laptop, en de maten schalen mee.
Voor hem geldt gewoon het zicht; lawaai hoort hij ook als je voor hem buiten zijn halve cirkel staat.

## De argwaanklok (`sneakRust`)

Sta je onopgemerkt achter een vijand binnen `SNEAK.argwaan.bereik` (2,4 Amir) op zijn niveau, dan loopt een klok
(`s.sArg`, 0 tot 1): aan de rand `van` (3,6 s), pal achter hem `tot` (1,8 s), lineair ertussen. Vol, dan draait hij
zich om (`s.sKijk`, `kijk` 0,8 s). Ziet hij je dan (de gewone zichtlijn, een kei verbergt niet), dan is hij wakker;
anders draait hij terug en loopt de klok na `rust` (0,6 s) opnieuw. Loop je weg, dan zakt de klok weer. De klok loopt
alleen met een vrije lijn van zijn ogen naar Amir (`sneakVoelt`, dezelfde `zichtLijnVrij` als het zicht): door een
muurtje of een terras heen voelt hij niets, dus daarachter kun je wachten. Dit is het
tijdraam: lopen tot net buiten gehoor, bukken, een stukje kruipen en steken duurt zo'n 1,5 s, de klok op die afstand
geeft ongeveer 3 s. Wie treuzelt wordt gezien. Lion's Patience verdubbelt de klok.

`sneakRust` zit in `zichtWaak` (bandiet, schildbandiet, kooiman, zweepman, alleen in rust en alleen voor `'mens'`)
en los in `updateMeelman` en `updateKruisboog`, die hun "ziet" zelf uitrekenen en hun rust via `zichtWaakMet`
bijhouden. De kruisboogbandiet staat met de sluipaanval in rust stil in zijn mikhouding in plaats van naar Amir toe
te lopen, en draait zich in rust niet naar hem toe.

## Rust-variatie (spawnvlaggen)

- `rug: true`: hij staat met zijn rug naar de kant waar Amir vandaan komt (`zichtZet`: `face` van Amir af).
- `draai: n`: in rust draait hij zich om de `n` seconden om, met `SNEAK.draaiSpreiding` (35%) speling, zodat je
  het niet op de tel kunt lopen. Kijkt hij dan jouw kant op, dan geldt het gewone zicht.
- `pat: true` of `pat: 300` (alleen de bandiet): hij loopt in rust heen en weer om zijn plek (`sneakPatStap`, de
  staande loop-set `walk`), `SNEAK.pat.breed` (1,8 Amir) of zoveel px aan elke kant, op `tempo` (0,45) van zijn
  rensnelheid, en aan elk keerpunt staat hij `pauze` (3,5 s) stil met zijn rug naar waar hij vandaan kwam: dat is het
  raam om hem te besluipen. Een kei, een rand of een ravijn keert hem ook (regel 7, `banMove`, `dropAhead`). Lopend
  haal je hem niet in zonder gehoord te worden (hij loopt 216 px/s, jij 330, en op 324 px hoort hij je), dus de route
  is: verstopt wachten tot hij omkeert, dan stil van boven achter hem komen (Test 61).

Zonder vlaggen staat hij zoals altijd met zijn gezicht naar Amir en is er niets te sluipen: de rug moet uit het
level komen (een vlag, of een route van boven langs hem heen). De hinderlaag-bandiet (`hurk`) houdt zijn eigen
gehoor (`banAmbushRange`) en doet niet mee.

## De sluipaanval zelf (`sneakKan`, `sneakDoe`)

`sneakKan(s)`: een mens-vijand met de sluipaanval aan, in rust (`s.zWacht`), niet net omkijkend, en Amir aan de
kant van zijn rug (`Math.sign(playerX() - s.x) !== s.face`). Elke `hitX` van de zes vraagt het bovenin: is het
een sluipaanval, dan `sneakDoe` (de ster, hitstop en shake van een crit via `critFx`, de kleine puls, de melding
"Sluipaanval!", `sneakKills`) en `s.hp = 1` voor de klap, zodat de treffer dodelijk is. De schildbandiet verliest
het schild en sterft met `schbSterf` (geen executie). De kooiman is alleen in zijn herstel raakbaar; de lus kijkt
daarom ook naar `sneakKan` (`raak = kooiRaakbaar(s) || sneakKan(s)`). De zweepman slaat met een sluipkill zijn
fase 2 (de arm eraf) over. Steek, worp en lage zwaai tellen alle drie; de worp van achteren van buiten zijn gehoor
is de stille optie.

## De animatie van Amir (`SNK`, `sneakRegie`, kop "de sluipaanval van Amir")

De frames uit pull request 624 (`karakters/amir/aanval/sneakaanval/`, `metadata.json`): `steek` (22 frames, aanloop 0 tot 6
met de tell op 6, stoot 7 tot 11, raak op 12 met 7 ticks hold, herstel 13 tot 21) en `afschud` (19 frames, til 0 tot 4,
smak 5 tot 10 met los op 10, terug 11 tot 18), canvas 1019x677, grondlijn 637, lijfmidden 634, dezelfde schaal als de
bukkenspeer (`JMP_S`), ticks per frame op 24 fps. Ze laden lui (`snkLaad`, via `laadLevel` in een level met `sneak`, en als
de sandbox-knop aangaat); `klein/` heeft de halve versies (`gen-klein.py`).

Een regie zoals de executie van de schildbandiet. `startAttack` vraagt eerst `sneakStart()`: staat er voor Amir, op zijn
vloer, een nietsvermoedende mens-vijand met zijn rug naar hem (`sneakKan`) tussen 0,45 en 1,6 keer het bereik (`SNK.bereik`,
583 canvas-px van het lijfmidden tot de punt op het raakframe), dan begint `sneakRegie`. Tot het loslaten staat de wereld
stil (`dt` 0 in `loop`, net als `exeVries`; `amirVast`, `hurtPlayer` en `camUpdate` kennen hem, en de camera kust in met
`exeZoomNu`). In de aanloop glijdt Amir in `SNK.schuif` seconden naar precies die afstand. De vijand staat stil
(`s.sneakVast`: zijn update slaat over, zoals `achterMasker`). Op het raakframe (`sneakRaak`) hangt hij aan de punt
(`s.hang`): elk frame zet `sneakHangZet` zijn `x` en zijn vloer op de speerpunt van dat frame (`SNK.punt`, per frame gemeten
als het verste punt van het lijf), zijn romp op `SNK.torso` boven zijn voeten, en zijn eigen tekenlus kantelt hem voorover
(`hangDraai`, na de translate naar zijn voeten, `SNK.kantel`, bij de smak `kantelSmak`). Op het losframe (`sneakLos`) komt hij
op de grond voor Amir en begint zijn gewone dood via zijn `hitX`, met `s.sneakLos` zodat die de treffer als sluipaanval
neemt (`sneakKan` geeft dan true, `sneakDoe` laat de ster weg). Daarna loopt de wereld weer (`sneakRegie.vrij`) en speelt
Amir zijn herstel uit: hij staat vast en is kwetsbaar. Zonder de frames (nog niet geladen) blijft het de snelle klap zonder
animatie, en de worp van achteren ook.

Nagemeten in de sandbox: de bandiet, de schildbandiet en de kooiman (ook naar rechts, dus gespiegeld om het hele canvas met
het lijfmidden aan de andere kant) hangen op de punt en sterven op het losframe, 4,0 s na de aanvalsknop; console schoon.

## De sluipdood van de bandiet (`SNKD`, `snkdTeken`, kop "de sluipdood van de bandiet")

Een gewone bandiet (niet de garde of de Duinwacht) heeft een eigen dood voor de sluipaanval, uit `enemies/bandiet/sneakdood/`
(`metadata.json`, `LEESMIJ_sneakdood.txt`, `proef_bloed.html`): de hangpose `val_00` en de val `val_00` tot `val_19`. Op het
raakframe zet `sneakRaak` hem op `snkdStart` (`s.snk`, en `s.bloed` uit), en vanaf dan tekent `snkdTeken` hem in de tekenlus
van de bandieten in plaats van zijn gewone frame. Zijn dood zelf blijft de gewone (`hitBandiet` in `sneakLos`, state `dood`);
`updateBandiet` neemt `s.klaar` over van `s.snk.klaar`. De frames laden lui met `snkLaad` (`snkdLaad`).

- **Maat**: `SNKD.maat` 1,28 keer de idle-maat (`banScale`), op het oog even groot als `enemies/bandiet/idle` (de kop en de
  lengte nagemeten; naast een gewone bandiet staand 190 px tegen Amir 155 op 1280x720).
- **Hangen**: Amirs tekenlus zet `snkAmirVak` (waar het canvas van de sluipaanval staat). Het uittredepunt (146, 80) ligt
  `SNKD.uittrede` (105) canvas-px achter de punt op de speer, gedraaid met de speerhoek min die van steek 12 (`SNKD.speer`,
  gemeten per frame). Op de maat van idle zakten zijn voeten zo tot een halve Amir door de grond, want de punt zit in de steek
  op borsthoogte van een kleinere man. Daarom: hij kantelt voorover (`snkdKantelDoel`, in stappen van 5 tot `kantelMax` 35
  graden, de kleinste stand waarin de punt na het optillen nog `uitsteek` 60 px uit hem steekt, zacht meeschuivend met
  `kantelV`) en wordt opgetild tot zijn laagste punt (`SNKD.schil`, de convexe schil van `val_00`) op Amirs grondlijn staat
  (`snkdTil`). Hij staat dan op zijn tenen met de speer door zijn onderlijf.
- **Het blad**: over hem heen tekent `snkdBlad` alleen het blad uit Amirs frame, van de punt tot net voorbij waar de speer
  zijn silhouet in gaat (`snkdBladLang`, op de dekking van `val_00`), met de rode waas (`SNKD.blad`). Daar zit ook de wond.
- **De val**: op het losframe begint de val onder het draaipunt; het verschil in hoogte en hoek met de hangplek loopt zacht
  naar 0 tot het knieframe (10). Bij het loslaten geen tweede flits; de flits bij de treffer is zachter (hooguit 0,55).
- **Bloed** (ingetogen, getallen uit `metadata.json`, in canvas-px van de bandiet): de spat bij de treffer langs de speer,
  de wondvlek binnen zijn silhouet (de wond verschoven met hetzelfde stuk als waar de speer echt uit hem kwam, weg vanaf
  frame 13), druppels uit de wond en van de punt (tot 0,3 s na het loslaten, want na frame 10 is de punt niet gemeten),
  vlekjes waar ze landen en de plas onder zijn borst vanaf frame 16. De waas op het blad blijft niet na het loslaten.

In de sandbox: **Sluipdood bandiet** onder Vijanden, bij Sluipaanval (zet de sluipaanval aan, geeft Amir de speer en zet een
gewone bandiet met zijn rug naar hem op 1,45 keer het bereik). Testlevel: Test 62.

## Het oog (`sneakOogTeken`)

Boven elke mens-vijand die zo speelt (vanuit `vijandHpBalk` en `schildHpBalk`, ook zonder de balk): in rust een
dicht oog, met de argwaan als een gele boog die eromheen volloopt; kijkt hij om, dan een vraagteken; is hij net
wakker, dan `SNEAK.wakker` (0,7 s) een rood uitroepteken. Zo leest de speler het raam.

## Talents (tijdelijk)

- **Soft Step** (Mkuki, `soft_step`, `factor` 0,5): de voetstappen dragen half zo ver; pulsen niet.
- **Lion's Patience** (Bhubesi, `lions_patience`, `factor` 2): de argwaanklok loopt half zo snel.

Beide achteraan in hun tree, dus na het vierde uitgespeelde level. Het zijn plaatshouders tot de echte sluip-tree
er is; een echte zou Impungushe en het mes de kans geven om van achteren dodelijk te zijn (het mes doodt nu niets).

## Sandbox

Onder Vijanden, de rij **Sluipaanval**: **Sluipaanval** (`sbsneak`, zet Zicht mee aan), **Rug naar Amir**,
**Draait om** (nee, 4, 8, 15 s) en **Patrouille** zijn de spawnvlaggen voor elke vijand die je daarna neerzet
(`sbSneakSpawn` in `sbSpawn`), **Toon gehoor** (`sneakToon`, `sneakTeken`) tekent de strook op je vloer tot waar je
voetstappen dragen en de pulsen als ringen. Soft Step en Lion's Patience staan bij hun tribe onder Speer.

## Test 61: De sluipaanval

Het testlevel (`TEST_61`, met toestemming, regel 3): een vlakke savanne met zeven vijanden met hun rug naar je toe,
elk met een tip, ruim 1800 px uit elkaar. Een bandiet met `rug`, een met `draai: 7`, de patrouille (`pat: 300`) achter een
muurtje van twee treden (150 en 300 hoog, 150 breed: springen is stil, van het blok vallen ook, en hij ziet en voelt je
niet door het muurtje), een schildbandiet (makkelijk), een bandiet en een kooiman op 500 px (een sluipkill wekt de
ander niet, een gevecht wel), een kruisboogbandiet die stil staat en een zweepman met `draai: 6`. Twee kalebassen.
De patrouille is in px (300) zodat zijn keerpunt op elk scherm op 200 px van het blok ligt; vallen van het blok met
losgelaten pijltje landt op zo'n 150 px achter hem, binnen de steek.

## Nagemeten

In Chromium op 1280x720 (reikwijdte van de steek op een bandiet 280 wereld-px, lopend gehoord op 315) en op 852x393
(160 en 177): lopen tot net buiten gehoor, bukken, kruipen tot steekafstand en steken is op alle zes een sluipkill
(de argwaan staat dan op zo'n 0,8); de worp van buiten zijn gehoor ook; sprintend hoort hij je van ver, met Soft
Step op de helft; stil achter hem blijven staan en hij kijkt na 1,9 s (oude klok) om en ziet je; een bandiet met
`draai: 4` draait om de 3 tot 5 s; de patrouille loopt heen en weer en ziet je aan het keerpunt als je in beeld
staat. Geen console-fouten. In Test 61 (Playwright, de echte speelroute): de eerste bandiet, de draaier (wachten buiten zicht tot hij
wegdraait) en de patrouille (achter het muurtje wachten, treden op, aan de rand loslaten, steken) zijn alle drie een
sluipkill; de speelrobot (die niet sluipt) komt vechtend tot de schildbandiet, zonder fouten.
