# De episodes en het verhaal

## het verhaal bij een episode

`VERHAAL` en `SLOT`, `verhaalToon()`: tekst op een zwart scherm voor elk level en na het laatste, alleen als je bij het eerste level begint. Op de naam van het level, dus een nieuwe episode hoeft alleen tekst toe te voegen en `verhaalAan` te zetten in zijn speelknop

## Episode The Roofs of Kumbasa

`KUM_1` tot en met `KUM_8` en `KUM_LEVELS`: acht stadslevels, van makkelijk tot extreem, gevraagd als vervanging van De
Valse Koning (die is weggehaald, met zijn menu, verhaal en ondertitels). Menu `menuKum`, `cardsKum`, knop `btnKum` in
`menuEpisodes`; Spelen is `gpSpeel` (tribekeuze, goud op 0, het verhaal), en de knop Nightmare (`btnnightmareKum`) neemt
de Nightmare over die De Valse Koning had. Teksten in het spel in het Engels (regel 5).

Alleen mensen (geen meelman) en hyena's, en Nyundo als enige baas (Roofs 8, gevraagd, regel 12), in indigo
(`KUM_TINT.nyundo`, dertig treffers). Twee aanvoerders in eigen kleur: Sefu de wever (3, groen, razernij) en Zuri de
verfmeester (6, schaduw met stofspoor en razernij, opent de eindpoort).

De rode draad zijn verstopte kisten die je alleen haalt met de volle sprong en een doek. Die plekken zijn letterlijk
overgenomen uit levels waar de sprongen al nagemeten zijn, met dezelfde maten: de doekkraam naar de galerij op 730
(Rivier 3, in 1 en 5), de trampoline-luifels in de steeg (Stad 10, in 3 naar de galerij op 1059, en in 2 en 7 naar het
hoogste dak), de takel (Rivier 8, in 4) en de stelling op de dam (Rivier 6, in 6). Verschuif je daar een huis, meet de
sprong dan opnieuw.

Een luifel hangt altijd boven een raam, op de hoogte van de voorramen (`raam`, zoals Stad 10); `levelcheck.py` geeft FOUT op
een luifel aan een muur zonder raam (regel `luifel boven een raam`). In 2 en 7 hingen eerst de rechte springdoeken van Stad 9
(boven het balkon en boven het lage dak); die zijn vervangen door de steeg van Stad 10: het korte balkon (`balkon` 0,6), een
steeg van 1,7 Amir, indigo boven het raam van de eerste verdieping, rood aan de overkant boven dat van de tweede, en een
derde (indigo, raam 3) onder het dak van huis 4. Rood naar die derde vraagt een stuit van 1,3 of meer (de top van 1,42 ligt
zo'n 50 boven de doek), dus twee goede stuiten; indigo naar rood de volle 1,42, net als in Stad 10. In 7 kreeg het lage huis
(2) dezelfde steeg naar huis 1 (indigo op raam 1 van huis 2, rood op raam 2 van huis 1, dan het dak op); alles links van
huis 1 schoof daarvoor 306 naar links. Wie daar mist valt op straat en loopt de route opnieuw.

| level | moeite | wat erin zit |
| --- | --- | --- |
| 1 The Ferry Steps | makkelijk | wapenrek, winkel, waterval met brug, kist boven de doeken |
| 2 The Dyers' Lane | makkelijk | stadstrappen, drie luifels in de steeg, kist en munt op het hoogste dak, waterval, rover uit een deur |
| 3 The Weavers' Court | gemiddeld | trampoline, alle huistypes (reliefhuis met nis, pilarenhuis met takel en gordijn, vervallen huis, ruine, toren, winkelhuis), winkel, verdieping met ladder en boog, leemmuur, wapenrek bij een kraam, Sefu |
| 4 The Fountain Square | gemiddeld/zwaar | regen, takel naar de galerij, fontein op een plein, verhoogde straat met de onderlaag, deuren beneden en boven, kooiman-duel |
| 5 The Lantern Alleys | zwaar | nacht, vier straten in een raster met minimap en `accenten`, dertig kills, hinderlaag, zweepman in fasen, hoorn |
| 6 The Dye Falls | heel zwaar | onweer, de dam, wapenrek op de kam, stelling met kist, waterval, winkel, `bandietGolf` met `niveau`, Zuri, eindpoort |
| 7 The High Door | extreem | de route van Stad 9 naar de einddeur, met twee steegjes luifels (Stad 10) in plaats van de springdoeken, de garde op de daken |
| 8 The Indigo Brute | extreem | het plein met Nyundo (opzet van Rivier 10) |

Wapenrekken stonden nog in geen enkel level, en `readLevel` nam het veld niet over; dat doet hij nu. Een rek staat op de
grond of de terrashoogte (`terrainH`), niet op een dak of zwever.

## Episode Test levels

`TEST_1` tot en met `TEST_36`: korte proefstukken, los van de echte episodes. Het menu toont de laatste zes (`KAART_BLAD`); de rest staat achter de knop **Oude tests** (`btnoudetests`, `testOud`, `testToon`). Dat venster komt uit de volgorde van `TEST_LEVELS`, dus een nieuw testlevel duwt vanzelf het oudste het archief in; `markCards` opent het archief als het gekozen level erin staat. Test 14 heeft `talentKeuze`: een scherm voor het begin (`talentKeuzeToon`, `testTalents`, in de pauze `pzkeuze`) waarop je de talents kiest, ook die van een tribe op slot

## Episode Test levels stad

`STAD_1` en `STAD_LEVELS`: proefstukken in de Sahelstad (zie `notities/stad.md`), met de tribekeuze (`runStart`) zoals
De Valse Koning; een knop in `menuEpisodes` (`btnStad`), het scherm `menuStad` met `cardsStad`. Stad 1 is de straat
met de lange galerij en het gevecht erop; het stond eerst als Test 59 tussen de Test levels. Eronder loopt de stadmuziek, Market Shadows
(`MUZIEK_STAD`, `music/marketshadows.mp3`, in elk stadlevel), en net als overal heeft Amir 1 reserve-speer op de rug (`RUG_STANDAARD`).

## Episode Oaktown

`OAK_1` (makkelijk, alleen zandslangen) en `OAK_2` (moeilijk, alleen mensen) en `OAK_LEVELS`: zeven korte straten op een
kaart als een dobbelsteen met zes ogen, op een raster met knooppunten (een poort de diepte in, een pad naar voren) en een minimap; je speelt een level uit met 50 kills (het
veld `straten`, zie `notities/oaktown.md`). Beide levels delen de kaart (`OAK_STRATEN`, `OAK_STAD`, `OAK_TERRAS`,
`OAK_KALEBAS`). Met de tribekeuze (`runStart`); een knop in `menuEpisodes` (`btnOak`), het scherm `menuOak` met `cardsOak`.

## Episode De Belegerde Stad

`BEL_1` tot en met `BEL_7` en `BEL_LEVELS`: zeven stadslevels, moeilijk tot extreem, zelf ontworpen op verzoek. Geen echte
episode in de zin van regel 1 (er is nu geen bevroren episode), maar ook geen proefstuk: pas ze aan als de opdracht erom vraagt.
Geen baas (regel 12). Met de tribekeuze (`runStart`); een knop in `menuEpisodes` (`btnBel`), het scherm `menuBel` met `cardsBel`.
De opbouw leunt op de stadlevels: 1 en 6 op Stad 1 (lift en toren), 2 op Stad 2 (trappen), 3 op Stad 3 (bruggen), 5 op Stad 4
(de koningsweg); 4 en 7 zijn nieuw. Level 7 heeft een `bandietGolf` met dolken bovenop de vaste spawns.

## Episode Baboon tests

`BAB_1` tot en met `BAB_4` en `BAB_LEVELS`: proefstukken voor de baviaan, met de tribekeuze (`runStart`) zoals De Valse Koning; menu `menuBab`, `cardsBab`. Baboon 1 is de wand en de kooi, Baboon 2 dezelfde vlakte met de speerbeet in plaats daarvan, Baboon 3 de speerval, Baboon 4 de goudaap-arena (`apenArena`, zie hieronder). De eerste en de derde stonden eerst tussen de Test levels

## Episode Murghtaan

`MUR_1` en `MUR_LEVELS`: proefstukken voor Murghtaan, de hyena-baas (regel 12, gevraagd door de opdrachtgever). Net als Baboon
tests een eigen knop onder Levels (`btnMur`), het scherm `menuMur` met `cardsMur`, en de tribekeuze (`runStart`). Geen echte
episode in de zin van regel 1: aanpassen mag.

Murghtaan 1: De roedel. Eerst een losse hyena en dan een paar, dan de arena (`murg: {x, van, tot}`, Amir blijft erin met
`murKlem` zolang hij leeft). De baas zelf staat in de HTML onder `// ---- Murghtaan` (`MUR`, `makeMurg`, `updateMurg`,
`hitMurg`, `murTeken`, `murBalkTeken`). Zijn ronde: `nader` (ren), `grauw` (de tell: de lippen trekken op), `sprong` (een reeks
frames met eigen duur, `MUR.sprong.reeks`: korte afzet, snelle vlucht met de bek open; de engine schuift hem `extra` Amir naar
voren, nooit door Amir heen), `klap` (de bek klapt dicht: het laatste grauwframe, met hitstop, schok en de bijtklap
`SFX_HYENA_BITE`), `herstel` (laag grommend in de grauw-lus, het strafvenster), na `MUR.sprongenPerRonde`
sprongen `weg` en `roep` (brul). In fase 1 haalt de roep een hyena (`MUR.maxHyenas` naast hem); na `MUR.hp1` treffers de
`reveal`: hij zakt in (de set `inzakken`), ligt stil (`MUR.reveal.lig`, de balk is weg), wordt bezeten en komt
verkeerd overeind (`inzakken` achterstevoren); hij wordt bezeten (de set uit `enemies/hyena_baas/bezeten/`, rode gloed op de oogkassen uit `ogen` in de metadata,
zwarte rook in `murRook`). Bezeten spuwt de roep kevers (`murKevers`, `MUR.kever`): ze vallen uit zijn bek, kruipen naar Amir,
maken hem trager (`murKeverTraag`, in de loopformule) en kosten `schade` leven per `tik` seconden zolang hij erin staat. Op een
kei kunnen ze niet: ze krioelen om de voet van de kei waar Amir op staat, en na `duur` seconden gaan ze op in rook. De lage
zwaai veegt ze weg (`murKeverVeeg`). Murghtaan zelf springt over een kei heen en staat er ook op (`murLift`): de uitzondering
van regel 7 voor een eindbaas, anders splitst een kei de arena in tweeen. In de sandbox: Vijanden, **Murghtaan**, **Bezeten**,
**Kevers nu** en **Finale** (bezeten met nog een treffer).

De finale, de echte dood (`murFinaleStart`, `murFinaleStap`, `MUR.finale`, state `finale` met `ffase`): na de laatste treffer
bezeten staat Amir vast (`murFinaleVast` in `amirVast`) en de balk is weg. De oranje poot geeft het op (`poot_op`, staan naar de
driepoot), hij draait weg van Amir en hinkt (`mank`, een manke stap als lus; bij het rondgaan schuift `s.x` een stap op, `reis` in
de metadata, root motion), kijkt over zijn schouder om (`omkijken`), hinkt verder en zakt in (`dood_echt`, met `duur_ms` per frame:
strompelen, neerglijden, omrollen, bek op een kier). Tijdens het vallen dooft de gloed in zijn oogkassen (`s.gloed`), daarna trekt
de rook terug in zijn bek (rook met `naar`) en kruipt er een kevertje uit en weg van Amir (kever met fase `uit`): Ndoki ontsnapt.
Dan is hij `dood` en is de arena open. De hinkende stappen houden zich aan de arena (`murArena`). De sets komen uit
`tools/murg_finale.py` (zelfde canvas als `murg_sets.py`, elke clip met schaal en verschuiving op de vorige gelegd), daarna
`murg_kleur.py`; de oogkassen per frame staan met de hand gekozen en geïnterpoleerd in `ogen` (bij het omkijken draait de kop).

De sets komen uit Grok-clips via `tools/murg_sets.py` (keyen, schalen, een offset per clip, de zoom eruit), `tools/murg_kleur.py`
(fase 1: de oranje zone als kale grauwe huid; bezeten: bijna zwart, verkoolde poot met paarse gloed) en `tools/murg_oog.py`
(de oogkas per frame, template matching vanaf een gekozen punt).

De opdrachtgever noemt Murghtaan ook **de hyenabaas**: met "de hyenabaas" is hij bedoeld, in elk ontwerp (fase 1, bezeten, de charge).

Murghtaan 2: The charge (`MUR_2`, `murg.charge: true`): een proefstuk voor het nieuwe ontwerp van Murghtaan (grotere manen,
melkwitte blinde blik, botkraag met slagtanden), alleen zijn charge-ronde. Eigen sets in `enemies/hyena_baas/charge/` (canvas
800x400, grondlijn 380, anker 400, kijkrichting links): `brul`, `aanzet` (inzakken en uitbreken, met `duur_ms` per frame), `galop`
(lus van 25, `in`/`uit` frame 15 is de pose waar de aanzet in eindigt en de slip mee begint), `slip` en `draai` (via de voorkant om,
eindigt de andere kant op). Elke set heeft `reis`: de root motion in canvas-px, die de engine bij het eind van de set bij `s.x`
optelt (`murcReis`). Het gedrag staat onder `// ---- Murghtaan 2: de charge` (`MURC`, `murcStap`, `murcRaak`, `murcTeken`):
wacht, brul, dan steeds aanzet, galop langs Amir (`MURC.voorbij`, en in het remvenster de slip, of eerder bij de arenarand),
slip met stof, draai, even loeren en weer de aanzet. Hij doet Amir niets; na `MURC.hp` (5) treffers blijft
hij staan en is het level na `MURC.winNa` uit (`winLevel`).
De slip glijdt echt door: de vaart van de galop (`MURC.glijStart` maal `ren`) valt in `MURC.glijDuur` kwadratisch stil
(`murcGlij`, in totaal `murcGlijAfstand`, zo'n 1,6 Amir bovenop de `reis` van de set), en de arenarand houdt daar rekening mee.
Bij het inzetten een klap stof (`MURC.stofBurst`), daarna wolken voor zijn voorpoten uit die meegroeien met de vaart
(`BAV_STOF.slip`, groter en langer dan 'rem'), en bij hoge vaart een spoor achter hem.
Tempo: de brul speelt op 15 fps (4,2 s); de eerste aanzet speelt helemaal (2,5 s), elke volgende `MURC.aanzetTempo` (1,6) keer
zo snel (`s.tempo` in `murcSpeel`, `s.aanzetten`). Pootstappen: op de galopframes in `MURC.poten` (5 en 8 de achterpoten na de
zweeffase, 16 en 21 de voorpoten, uit de alfa op de grondlijn) speelt `murcStap1` `sounds/murc_stap.mp3` (de eerste 0,3 s van
`brutus_stap.mp3`, hoger en lichter gemaakt met ffmpeg), uit een rijtje van vier stemmen met wat variatie; de galoplus staat
daarom zachter (0,4). Nog niet gebouwd, bewust uitgesteld door de opdrachtgever: schade bij contact in de galop, en een
reactie op een treffer (struikelen, kortere slip). Geluid uit de Grok-clips: `sounds/murc_*.mp3` (`murcZeg`, de galop
als lus). In de sandbox: Vijanden, **Murghtaan charge**. De sets komen uit de Grok-clips met een eenmalig script: keyen op de
eigen achtergrondkleur van elke clip, registreren op het startbeeld (schaal en verschuiving op maximale overlap), in de
draai de tweede oranje poot terug naar vacht, daarna `tools/murg_kleur.py` (fase 1: de oranje zone wordt kale grauwe huid).
Let op bij het live zetten: een directe push van Claude op `main` start de Pages-build niet; live gaat via een pull request die wordt samengevoegd.
Proefrit: `node tools/murc_test.js [map]` laadt het level, volgt de toestanden, maakt schermafdrukken en raakt hem vijf keer.

De pin (`MURC.pin`, onder `// ---- Murghtaan 2: de pin`, het ontwerp in het project-document `hyena_pin_aanval.md`): na de
galop kiest hij met kans `kans` (en minstens `afkoel` s na de vorige, nooit twee keer achter elkaar, `murcPinMag`) de pin
in plaats van de draai. Op slipframe `blikFrame` gaat hij over in `pin_blik`: laag, lijf van Amir af, kop over de schouder
naar Amir (de tell, `blikT`). Dan `pin_draai` (via de voorkant om, eindigt de andere kant op), `pin_loer` (plat, `loerT`),
`pin_sprong` en `pin_land`. In de lucht stuurt hij naar Amir (`volg`) en hangt hij in een boog (`boog`, `murcPinBoog` op
`s.lift`). Bij de landing (frame 3 van `pin_land`) ligt Amir eronder als hij niet rolt (`murcAmirOntwijkt`: alleen `rol` en
`rolW`) en binnen `reik` Amir van de bek is (`mondX`, canvas-x 455). Een speerworp (`worpTref`) in de tell breekt hem af
(`pinOnder`, telt als treffer); in de pin, de sprong en de landing is hij niet te raken. Ligt Amir eronder (`murcPinAmir`):
`amirVast` en `exeAmirWeg` houden hem vast en verborgen, en `murcPinAmirTeken` tekent hem tijdelijk plat op zijn rug (het
gewone idlebeeld gedraaid, de speer als lijn bij een steek, een vonk bij een parry), tot er echte animaties van Amir zijn.
Vier happen (`murcPinHap`): `hap_op` (`opT`), `hap_boven` (`hou1` tot `hou4`, de tell van die hap, met een grom), `hap_neer`
(`neerT`, aan het eind valt de hap), `hap_bodem` (`bodemT`) en `hap_terug` (`terugT`); de laatste twee zijn de dubbele hap
(de tweede maar half omhoog, `opHalfT`, zonder terug ertussen). De aanvalstoets (`thrPress` zet `murcPinDruk`) binnen
`voor` s voor tot `na` s na de hap pareert (klink `sounds/brutus_speerraak.mp3`); te vroeg zet steken `straf` s uit. Een
gemiste hap kost `schade` levens via `murcAmirSchade` (hurtPlayer zonder terugslag en zonder de onkwetsbaarheid). Beide
happen van de dubbele gepareerd: `pinTrap` (hij schuift weg) en `pinStraf` (`strafT` s treffers x2); anders `pinEraf` (hij
springt eraf) en een nieuwe aanzet. Bij de start kiest `murcKeuze` (het scherm van `duoKeuze`): levens of onaantastbaar
(`duoKeuze.murcOnst`, in `onsterfelijk`) en 0 tot 2 gewone hyena's (`duoKeuze.murcHy`, `murcRoedelAanvul` vult aan); tijdens
de pin vallen die niet aan en giechelen ze (`murcRoedelStap`). Afstellen: onder Instellingen in de pauze **Murghtaan pin:
tune** (`MURC_PIN_SCHUIF`, gebouwd door `murcPinPaneelBouw`), bewaard in localStorage (`amir_murc_pin`), Default zet
`MURC_PIN_STANDAARD` terug. De sets (`pin_*`, `hap_*` in `enemies/hyena_baas/charge/`) komen uit vijf Grok-clips met een eenmalig
script: keyen, gruis en gaatjes weg, elke clip op zijn startbeeld geregistreerd en het startbeeld van de tell op slipframe 11
(schaal 0,255), vanaf `pin_loer` gespiegeld naar de kijkrichting van de charge, in de draai de tweede oranje poot terug naar
vacht, daarna `tools/murg_kleur.py`. Proefrit: `node tools/murc_pin_test.js [map]` speelt drie potjes (niets doen, elke hap
pareren, rollen bij de landing).

Murghtaan 3: The feast (`MUR_3`, `murg.intro: true`, onder `// ---- Murghtaan 3: de opening`, `MURC_INTRO`): de opening voor de
charge. Hij staat `MURC_INTRO.rand` Amir binnen `murg.van`, kijkt naar links en vreet aan een dode bandiet (`dood_62` van de bandiet,
gespiegeld, met getekend bloed: tijdelijk). Toestanden `iVreet`, `iRust`, `iBlik` (omkijken), `iKijk`, `iTerug`, `iWhoop`. Binnen
`zie` Amir: omkijken, dan de freeze met balken en naam (`murcVries`, `murcBalk`, `murcIntroTeken`; de wereld staat stil op dt 0),
de whoop, en de roedel van drie (`murcRoedelKomt`, `h.murcRoedel`). De roedel stormt nooit met twee tegelijk (`murcRoedelBezig`),
staat aan een kant in een rij (`murcRoedelRij` in `hyThreatGap`) en draait na een storm om (`omkeer`). Een muur `muur` Amir rechts
van hem (`murg.muurX`, in `murKlem`, getekend als lijn) houdt Amir weg; een speer gaat erover. Een treffer laat hem omkijken. Is de
roedel dood: omkijken, een korte freeze, en dan `murcAanzet` (de draai naar Amir is nog een harde wissel). De camera schuift in de
opening naar hem toe (`murcIntroCam`). De sets `vreet`, `omkijk`, `omkijk_lus` en `whoop` komen uit `tools/murc_intro_sets.py`
(clips in `enemies/hyena_baas/bron/`); proefrit: `node tools/murc_intro_test.js [map]`.

## Episode De Gouden Poort

`GP_1` tot en met `GP_10` en `GP_LEVELS`: tien stadslevels van makkelijk tot mega, zelf ontworpen op verzoek (regel 3), met
Nyundo als baas van level 8 (regel 12, gevraagd). Net als De Belegerde Stad geen echte episode in de zin van regel 1: pas ze
aan als de opdracht erom vraagt. Een knop in `menuEpisodes` (`btnGP`), het scherm `menuGP` met `cardsGP`. De speelknop en een
dubbelklik op een kaartje gaan via `gpSpeel`: de tribekeuze, het goud op 0 (`goudBegin`) en `verhaalAan`, zodat elk level
(ook een later gekozen) een tekstje uit `VERHAAL` krijgt; `SLOT` na level 10. De latere levels hebben de namiddag
(`stad_middag`) en de avond (`stad_avond`) als lucht, twee extra scenes naast `stad_dag`.

Per level: 1 losse rovers en sluipen; 2 binnen, met de munt boven in het huis van de baas (een slapende wacht ervoor); 3 de
eerste winkel en Bako (aanvoerder, einde); 4 de stadsmuur van leem (terrassen van 170 tot 1530, een houten stelling tot 1870);
5 De Kroonwijk, acht rechte straten in een raster van drie bij drie (`GP_5_STRATEN`, `raster: true`, `doel: 0`), kapitein Zaki in de Goudsmedenpunt; 6 binnen en de
tweede winkel; 7 Kwame de poortwachter en de eindpoort (een pleinpoort met `einde: true`); 8 het plein met Nyundo, zoals
Stad 6; 9 de garde, de derde winkel en de schatkamer met de kluis; 10 een `bandietGolf`, geen winkel, de goudvorst (16 levens,
`sluip: false`).

## Episode De Rivierstad

`RIV_1` tot en met `RIV_15` en `RIV_LEVELS`: vijftien stadslevels van makkelijk tot mega, zelf ontworpen op verzoek (regel 3), met
Nyundo als baas van level 10 (regel 12, gevraagd). Geen echte episode in de zin van regel 1. Een knop in `menuEpisodes` (`btnRiv`),
het scherm `menuRiv` met `cardsRiv`; spelen gaat via `gpSpeel`, net als De Gouden Poort (tribekeuze, `goudBegin`, `verhaalAan`),
met een tekstje per level in `VERHAAL` en `SLOT` na level 15.

Drie dagen, elk van `stad_ochtend` (het ochtendgloren, een nieuwe scene) via `stad_dag` en `stad_middag` naar `stad_avond` en
`stad_nacht`. Weer: regen in 4, 5 en 11, een zandstorm in 8, onweer in 14 en 15. Elk level heeft `goud`, `kopgeld` en `schildKleur`.

Per level: 1 losse rovers, de eerste brug, een kist in een huis; 2 een rivier met en een zonder brug, hyena's, een kist op de
galerij; 3 de eerste winkel, een kist boven de doeken, Jabari (aanvoerder, 6, einde); 4 regen, de eerste zweepman, een snelle val
(`val: true`), een kist boven in een huis met een verdieping; 5 de eerste nacht, sluipen, een kist achter een boog; 6 de dam van leem
(de opzet van Goud 4) met een meelman op de trap en een kist op de stelling; 7 drie kamers achter elkaar (de kist in de achterste) en
de tweede winkel; 8 zandstorm, hyena's in roedels, twee bruggen, de takel als enige weg naar de kist; 9 Kofi (12) en de eindpoort;
10 het plein met Nyundo bij nacht, `hp: 24` en rode oker (`tint`), met vier fakkels zodat Amir te zien blijft; 11 de derde winkel en een kist boven op de toren (1388);
12 schutters op alle galerijen, een kist boven in een huis; 13 drie rivieren (de laatste zonder brug), de vierde winkel en twee
kisten; 14 onweer, een `bandietGolf` met `niveau: true` (een nieuwe rover alleen op Amirs hoogte, en een rover die op een trede
van de dam vastzit telt niet mee voor `max`, `GOLF_NIVEAU`) en de grote dam met een kist op de stelling; 15 een golf die niet ophoudt en Simba Kivuli (20,
`sluip: false`). De tinten van de bazen staan in `RIV_TINT`.

## de schatkist: E en het goud spat eruit

`KIST`, `kisten`, `kistMaak`, `kistReset`, `kistE`, `kistStap`, `drawKisten`, `kistLaadLevel`

`kisten: [{x, y, vast, goud, f}]` in het level, `y` en `vast` zoals bij de munt (een dak of galerij via `stadKalebasPlek`, met `vast`
precies op `y`, binnen op een verdieping). Het plaatje is de kist uit de winkel (`design/stad/binnen/spul_kist.png`), lui geladen.
E erbij (`kistE`, in `eDruk` na `muntE`) tilt het deksel op, `KIST.munten` munten springen eruit, en in een level met goud komt
`goud` (zonder veld `KIST.goud`, 20) bij je goud; het vliegt in een keer uit de kist naar de teller (`goudVlieg`), net als het
kopgeld uit de verslagen aanvoerder of Nyundo. `goudReset` roept `kistReset`: na een dood zijn de kisten weer dicht, net als de
munt, en het goud staat weer op de bank. Een dichte kist fonkelt om de `KIST.fonkel` seconden. In de sandbox onder De stad: de
knop **Schatkist** (een op de straat, een op de galerij als er een stad staat).

## kopgeld en de kleur van de makkelijke schildbandiet

`kopgeld: true` in een level met goud: `goudKopgeld` geeft bij de dood van een aanvoerder (`aanvoerderDood`) `GOUD.kopgeld.aanvoerder`
(10) en bij Nyundo (`hitBrutus`, niet in de sandbox) `GOUD.kopgeld.nyundo` (25), met een melding. `schildKleur: true` geeft elke
schildman met `niveau: 'makkelijk'` de filter `SCHB_TINT.makkelijk` (een bruin kleed in plaats van blauw); een spawn kan ook zelf
`tint` hebben. In de sandbox onder Vijanden, Schildbandiet: **Makkelijk, kleur**. Nyundo neemt `hp` en `tint` uit `level.brutus`
(`makeBrutus`); de woede blijft bij 6 levens over (`BRU.woedeHp`).

## goud: een goudstuk per kill, de winkelprijs en de munt van de koning

`GOUD`, `goudAan`, `goudKill`, `goudReset`, `goudWin`, `goudVerder`, `goudBegin`, `muntE`, `drawMunt`

Alleen in een level met `goud: true`. `vijandDood(baas, wie)` roept `goudKill(wie)`: `GOUD.perKill` goud.

**Goud dat vliegt** (`GOUD_VLIEG`, `goudVlieg`, `goudVliegStap`, `goudTink`, `#goudlaag`): het goudstuk springt draaiend uit de
gevallen vijand (`wie.x`, `wie.base`, op `borst` Amir hoogte), hangt even en vliegt in een boog naar het icoon rechtsboven.
`goud` telt meteen, de teller (`goudHud`) trekt `goudOnderweg` eraf en telt pas bij aankomst, met de pulse en een tink
(WebAudio, geen bestand). De positie op het scherm komt uit de wereldtekening (`goudVliegProj`, naast het stof). Zonder
`wie` springt hij bij Amir op. `goudReset` en `goudBegin` ruimen wat onderweg is op (`goudVliegWeg`). In de sandbox:
Vijanden, **Goud bij een kill** (`sbGoud`, `goudTelt`), zonder winkelprijzen.
 De HUD (`#goud`) staat naast de
kalebassen. In de winkel (`winkelUIToon`, `#wkkalebas`) kost een kalebas `GOUD.kalebas` en draag je er hooguit `HPPOTION_MAX`;
zonder goud blijft de winkel gratis. `winLevel` onthoudt goud en gedragen kalebassen (`goudWin`), pas `wnnext` zet ze op de
bank (`goudVerder`), en `restart` zet alles terug op de bank (`goudReset`, na `resetHppotions`): wie sterft is het goud van dat
level kwijt, en Opnieuw na een gewonnen level geeft geen dubbel goud.

Verkopen (`winkelVerkoop`, `GOUD.verkoop`: kalebas 2, speer 6, gif 16, zo'n 40% van de koopprijs): ruim onder de koopprijs,
zodat kopen en terugverkopen nooit winst geeft. Een kalebas en een gif uit de inventory, een speer alleen als hij gekocht is
en op de rug zit, niet die in de hand en niet het gif dat al op de speren zit (`gifHits`). Een gekochte speer heeft een geel
vaantje (`SPEER_SOORTEN.geel`, de vlag `blauw: 'geel'` op de speer, `speerSoortId`); de verkoop haalt de laatste gele van
de rug. Je eigen speren (rood) en de skeletspeer (blauw) zijn nooit te koop, ook niet een rode uit een rek: elk level begint met
een volle rug, dus anders was de reservespeer elk level 6 gratis goud. Gevonden kalebassen mogen wel, want tonnen en kalebassen
in een level zijn per level op. Geen bevestigingsvraag: **Terugkopen** (`winkelTerug`,
`winkelTerugkoop`) haalt het laatst verkochte terug voor dezelfde prijs, zolang het scherm open is. Koop je met een volle tas,
dan zegt de uitleg "Je tas is vol. Verkoop eerst iets." en lichten de verkoopknoppen op (`winkelVolTekst`). Bij dood telt
het verkopen in dat level niet, want `goudReset` zet goud, kalebassen en gif terug op de bank. Een gekochte speer geldt
maar voor dat level, net als vroeger.
Onderzoek bij het ontwerp: spelers willen terugkopen boven een bevestiging, een andere kleur voor verkopen op een telefoon, en
geen spul dat alleen te verkopen is; 25 tot 50% van de koopprijs is gangbaar.

De munt: `munt: {x, y, vast}` in het level, `y` een hoogte zoals bij een kalebas (een dak of galerij via `stadKalebasPlek`),
met `vast` precies op `y` (binnen op een verdieping). Hij draait, gloeit en fonkelt (`drawMunt`); E erbij (`muntE`, voor alles
in `eDruk`) pakt hem. `tribeNaLevel` geeft voor dat level een punt extra, tot de boom vol is, en zet `RUN.munt` zodat het een
keer per run is; daarna ligt hij er niet meer.

## de aanvoerder en de eindpoort

`AANV`, `aanvoerderDood`, `aanvStap`, `aanvKlem`, `eindPoorten`

Een bandiet met `aanvoerder: true` in zijn spawn: `hp` levens (de balk krijgt een streepje per leven, een gouden rand, een
kroontje en `naam`), `tint` een canvas-filter over zijn frames, `titel` in de melding bij het verschijnen, `sluip: false` zet de
sluipaanval op hem uit. `hitBandiet` roept bij zijn dood `aanvoerderDood`: zonder eindpoort is het level na `AANV.win` uit, met
een eindpoort (een pleinpoort met `einde: true` in `stad.pleinpoorten`, in een level zonder `brutus`) takelt het hek op en
speel je met E onder de boog uit (`pleinPoortBij`, `pleinUitgang`). Zolang dat hek dicht is, houdt `aanvKlem` Amir ervoor.
`levelcheck.py` (regel `einde`) kent een level met een aanvoerder als uit te spelen.
In de sandbox onder Vijanden, Bandiet: de knop **Aanvoerder** (`bandiet_aanv`, zes levens, goud, een naam); daar speelt zijn dood niets uit.
