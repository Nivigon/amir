# Tribes, talent tree en abilities

## tribes: de keuze per run en de abilities

`TRIBE_CONFIG` (bovenin het script: alle namen, teksten en getallen) en `RUN` (tribeId, verdiende abilities, uitgespeelde levels); onder "tribes: keuzescherm, ability, HUD" `tribeKies`, `tribeNaLevel` (vanuit `winLevel`, geeft een talentpunt in `RUN.punten`), de talent tree onder "talent tree" (optie A uit de voorstellen: een tak van links (tier I) naar rechts, de kop met je punten erboven en het venster als brede strook eronder, links de tekst (`.tbilinks`) en rechts de knoppen (`.tbirechts`); het thema per tribe in `boom` in `TRIBE_CONFIG`, met `TB_RING`, `tbLijn` (in `.tbstam` een kwartslag gedraaid, zodat de staande tekening liggend tussen twee ringen zit), de ringmaat `--tbr` die zich uit het aantal talents (`--tbn`, gezet in `tribeBoomToon`), de breedte en de hoogte rekent zodat het scherm liggend nooit scrolt, de T-splitsing onder de naam (op een scherm lager dan 450 px alleen in het venster), pijltjes links en rechts (en op en neer) lopen langs de talents, `TB_TEKEN` voor plaatjes die nog ontbreken en `tbVergelijk` voor zonder en met; `tribeBoomToon`, `tbStaat`, `tbKlik`, `tbBijwerken`; in `#trunlock`, ook te bekijken via `pztalents` in de pauze; op het keuzescherm opent een kaart de boom zonder te kiezen (`tribeBekijk`, `tbKijk`, `tbRun`), en `tribeVastleggen` legt de tribe pas vast bij het eerste talent of bij Join; een tribe op slot laat `TB_LEEG` lege plekken zien), `opnieuw` (na game over hetzelfde level, abilities blijven), `hudToon`, `tribeHeeft` en `abilityWaarde`. Een ability werkt alleen via die twee: Quick Hand in `updateThrow`, Thorn Breaker in `hitThicket`, Twin Sweep (id `low_sweep`, `ladingen`) in `sweepMax`; de lage zwaai zelf heeft iedereen, met ladingen die in `SWEEP_HERLAAD` seconden terugkomen (`swLading`, `sweepLaden`, `zwaaiHud` rechtsboven), en wat hij raakt staat voor iedereen in `zwaaiVak`, Fourth Life in `levensStart`. Een tribe met `bijStart` krijgt zoveel talentpunten meteen bij het kiezen; nu staat dat bij alle tribes op 1, zodat je keuze vanaf level 1 telt (`tbWanneer` zegt dan `From the start`). De woedemeter van Bhubesi (`woede` in zijn blok, stand in `RUN.woede`) staat onder "woede": `heeftWoede` (Long Breath of Blood Rush), `woedeVul` (vanuit `vijandDood` en `hitPanther`), `woedeStart` (G, de meter, de knop `woede` in `TOUCH_BTNS`), `woedeAan` houdt `hurtPlayer`, `valLand` en `fosforBijt` tegen, `woedeGloed` en `woedeVonken` bij het tekenen van Amir. Elke episode begint met de tribekeuze (`runStart` in zijn speelknoppen, en bij dubbelklikken op een kaartje in `buildCards`), nu De Poorten en Baboon tests; de Test levels niet, tenzij daar expliciet om gevraagd wordt, en daar gelden alle abilities van de tribes die niet op slot staan, net als in de Test van de Maker (Test 14 laat je kiezen, zie `talentKeuze`). Een tribe op slot (nu Impungushe) mag al abilities hebben: die gelden dan alleen in de sandbox en in Test 14; zijn boom laat ze dicht zien en zijn kaart op het keuzescherm blijft leeg. De sandbox heeft `sbAbilities`, de speelrobot speelt zonder tribe en dus zonder abilities. De plaatjes in `design/tribes/` komen uit `tools/tribe_logos.py`; de drie ability-plaatjes van Bhubesi zijn uitgeknipt (tot 400 bij 400, grijs eromheen doorzichtig) uit de JPG's in `notities/` (`notities/fastereimmortal.jpg`, `notities/longerimmortal.jpg`, `notities/extralife.jpg`), waarvan twee namen omgewisseld zijn: `fastereimmortal.jpg` is Long Breath, `longerimmortal.jpg` Blood Rush, `extralife.jpg` Fourth Life

## T-splitsing in de talent tree

een talent met `varianten` in `TRIBE_CONFIG` krijgt naast zijn naam een gestippelde splitsing met de namen (`tbSplit`, `.tbsplit`) en in het venster de varianten met hun tekst (`.tbivar`). Nog niets te kiezen; nu alleen bij Jackal Fang. Een tribe op slot laat zijn talents dicht zien; `TB_LEEG` alleen als hij er nog geen heeft Tijdelijk getekend: het plaatje komt uit `tools/mes.py` (`design/mes/mes.png`), zijn lijf schiet naar voren omdat er geen frames met een mes zijn. De kalebas is de speertekenvariant `kalebas`

## De talents van de rol-worp: True Flight (Mkuki) en The Pounce (Bhubesi)

Het vierde talent van beide trees. Het houten plaatje is `4_true_flight.png` en `4_the_pounce.png` in `design/tribes/<tribe>/abilities/` (Grok, image-to-image op Thorn Breaker en Fourth Life, uitgeknipt op 400 bij 400 met de donkere rand doorzichtig); het teken in `TB_TEKEN` blijft de reserve als het plaatje niet laadt.

- **True Flight** (`true_flight`, `critKans`, `zak`): een rol-worp met `jav.crit` (gezet in `rolWorpLos` door
  `rolWorpCrit`). Perfect is altijd een crit; een gewone trekt een knikker uit `critZak` (de marble bag: `zak` knikkers,
  `critKans` deel crit, geschud, zonder terugleggen, `critZakVul`/`critZakTrek`), per level een verse zak (`restart`).
  Raakt de speer, dan zet `javHitEnemy` `critNu`, en de `hitX` van de vijand haalt met `critPak()` een treffer extra af
  in dezelfde aanroep (een tweede aanroep stuit op zijn `inv`): `enemyTakeHit` (slangen, schorpioen), `hitHyena`,
  `hitBandiet`, `hitMeelman`, `hitKruisboog`, `hitKooiman`, `hitZweepman` (die slaat de arm eraf niet over) en
  `hitSchildman` (het schild een stand extra, nooit door het schild heen in een klap). Bazen roepen `critPak` niet aan;
  elk beeld zet `critNu` uit bij `javBox`. Het effect: `critFx` (hitstop, schok) en `critFxTeken` (een witgouden ster),
  ook op het oefendoel van Test 60. Een fosforslang of een kooiman die de speer afslaat krijgt geen schade, dus ook geen crit.
- **The Pounce** (`the_pounce`, `vul`, `vulPerfect`): `javHitEnemy` vult met een rol-worp (`jav.rol`) de woede, 0,05 en
  perfect 0,10, door `woedeVul` (dus maal Blood Rush, en niet terwijl de woede loopt). Geeft zelf de meter (`heeftWoede`).
  Een oefendoel telt niet: dat loopt niet via `javHitEnemy`.
- Afstellen in de pauze onder Rol-worp: test, het groepje Talents. Test 60 heeft `talentKeuze`, in de sandbox staan ze
  bij Tribe Mkuki en Tribe Bhubesi.

## De plaatjes van Soft Step (Mkuki) en Lion's Patience (Bhubesi)

Het vijfde talent van beide trees: `5_soft_step.png` en `5_lions_patience.png` in `design/tribes/<tribe>/abilities/`
(Grok, image-to-image op True Flight, op 400 bij 400 met de donkere rand doorzichtig). De voet is naar het midden geschoven
(het oude symbool met hout van links ingevuld; de nerf loopt horizontaal, dus geen naad), en het hout van de leeuw is naar
het roodbruin van Bhubesi gekleurd. De leeuw loert uit het gras: het talent gaat over sluipen en toeslaan, een rustige of
liggende leeuw las te vriendelijk.

## De tweede speer: Second Spear en Tumbling Spear (Mkuki)

Het zesde en zevende talent van Mkuki. `DUBBEL` (venster 0,4 s, `vanFrame` 5, `ritme`), `dubbelKan`, `dubbelStart`:
F binnen het venster na het loslaten (`thr.losT`, of `rolW.losT` na de rol-worp) grijpt zonder de beat van `RUG.trek` een
speer van de rug en speelt de worp vanaf frame 5, altijd vlak. `ritme` zegt per frame hoe lang het staat (0,10, 0,08, 0,08,
0,07, 0,05: 0,38 s tot het loslaten): eerst overeind met de speer op de schouder (de greep), dan de uitval in en steeds
sneller, een zweep. Eerst was het frame 7 op dubbel tempo, 0,125 s: dat las als een worp in plaats van twee, en omdat hij
alleen de lage uitval liet zien leek Amir kleiner dan bij de eerste worp (de frames zelf zijn even groot). Een tik op F breekt de tweede
niet af (`thrRelease`). Een druk tijdens de eerste worp, voor het loslaten of vlak erna, wordt onthouden (`dubbelVraag`,
`thr.wil`) en de tweede begint pas op `DUBBEL.naFrame` (12) van de eerste, zodat je de eerste speer los ziet gaan en de
arm ziet doorzwaaien. Eerst begon een druk net voor het loslaten de eerste worp opnieuw bij frame 0 (en ging de eerste
speer er nooit uit), en knipte een druk op het loslaten de nazwaai weg.

De perfecte tweede: druk F tussen `DUBBEL.perfVan` en `perfTot` (0,06 tot 0,24 s) na het loslaten van de eerste (of van
de rol-worp), dan licht Amir op met de ster van de rol-worp (`dubbelGlansTeken`, `glansSter`). Een druk tijdens de eerste
worp telt niet als perfect (anders was rammen genoeg). De perfecte (`thr.perfect`, `jav.perfect`) krijgt het gouden spoor,
een stop van 0,05 s, een camerastoot (`rolStoot`) en even vertraagd beeld: de wereld begint op `traag` (0,3) en is in
`traagDuur` (0,4 echte seconden) weer op gang (`dubbelTraagT`, `dubbelTraagNu`, in de lus naast `zwmTraagNu`). Het
vertraagde beeld zit bewust alleen op de perfecte: elke keer zou snel gaan vervelen.

De tweede speer raakt door de onkwetsbaarheid heen. Een vijand is na een treffer even onkwetsbaar (`s.inv`, bij de bandiet
1,15 s), en de tweede komt zo'n 0,55 s na de eerste aan: hij viel dan zonder schade op de grond, of werd niet eens getest.
Een speer met `jav.dubbel` zet bij een gewone vijand `s.inv` op 0 (`dubbelDoor`, via `javRaakt(box, s)`), en waar een
vijand tijdens zijn onkwetsbaarheid de speertest oversloeg (bandiet, meelman, kruisboogbandiet, schildbandiet, zweepman,
en bij de hyena de test vooraf) test hij nu toch de tweede (`dubbelVliegt`). De bandiet pareert hem niet. Uitgezonderd: de
bazen (panter, baviaan, Nyundo) en de kooiman (alleen te raken als zijn kooi open is). En de eerste `DUBBEL.dichtT`
(0,08 s) raakt de tweede ook wat tussen Amir en de punt staat (`javVak`): een bandiet stormt na de eerste treffer meteen
terug en stond dan al voor de punt. Second Spear geeft het
na een gewone worp, Tumbling Spear na de rol-worp (een verbetering: in de rij komt hij na Second Spear). Een per worp; de
tweede heeft geen derde.

Het spel kende een geworpen speer (`jav`). De tweede staat in `jav2`: `jav2Update` zet hem even op de plek van `jav`, laat
`javUpdate` lopen en zet alle speer-globals terug; komt hij tot stilstand of is hij kwijt, dan wordt hij een losse speer
(`eigenSpeerLos`). Een rune houdt hem vast, zoals elke speer (regel 9). `javRaakt` test ook `jav2`; raakt die, dan ruilt
`javWissel` hem naar `jav`, zodat `javHitEnemy` en de vijand met de goede speer rekenen (ligt de eerste al ergens, dan wordt
die een losse speer). Is `jav` leeg, dan schuift `jav2` door. Getekend met `jav2Draw`. Nog geen houten plaatjes: het teken
in `TB_TEKEN` (`icoon: null`). In de sandbox onder Speer en spullen, bij Tribe Mkuki, en als level **Test 64: De tweede speer** (`TEST_64`: de
oefendoelen en de volle rug van Test 60 met `rolWorpProef`, `rugMax: 3`, en daarna vijanden die om twee speren vragen).
