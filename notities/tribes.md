# Tribes, talent tree en abilities

## tribes: de keuze per run en de abilities

`TRIBE_CONFIG` (bovenin het script: alle namen, teksten en getallen) en `RUN` (tribeId, verdiende abilities, uitgespeelde levels); onder "tribes: keuzescherm, ability, HUD" `tribeKies`, `tribeNaLevel` (vanuit `winLevel`, geeft een talentpunt in `RUN.punten`), de talent tree onder "talent tree" (ontwerp 7 uit de schetsen: groeit omhoog, het thema per tribe in `boom` in `TRIBE_CONFIG`, met `TB_RING`, `tbLijn`, `TB_TEKEN` voor plaatjes die nog ontbreken en `tbVergelijk` voor zonder en met; `tribeBoomToon`, `tbStaat`, `tbKlik`, `tbBijwerken`; in `#trunlock`, ook te bekijken via `pztalents` in de pauze; op het keuzescherm opent een kaart de boom zonder te kiezen (`tribeBekijk`, `tbKijk`, `tbRun`), en `tribeVastleggen` legt de tribe pas vast bij het eerste talent of bij Join; een tribe op slot laat `TB_LEEG` lege plekken zien), `opnieuw` (na game over hetzelfde level, abilities blijven), `hudToon`, `tribeHeeft` en `abilityWaarde`. Een ability werkt alleen via die twee: Quick Hand in `updateThrow`, Thorn Breaker in `hitThicket`, Twin Sweep (id `low_sweep`, `ladingen`) in `sweepMax`; de lage zwaai zelf heeft iedereen, met ladingen die in `SWEEP_HERLAAD` seconden terugkomen (`swLading`, `sweepLaden`, `zwaaiHud` rechtsboven), en wat hij raakt staat voor iedereen in `zwaaiVak`, Fourth Life in `levensStart`. Een tribe met `bijStart` krijgt zoveel talentpunten meteen bij het kiezen; nu staat dat bij alle tribes op 1, zodat je keuze vanaf level 1 telt (`tbWanneer` zegt dan `From the start`). De woedemeter van Bhubesi (`woede` in zijn blok, stand in `RUN.woede`) staat onder "woede": `heeftWoede` (Long Breath of Blood Rush), `woedeVul` (vanuit `vijandDood` en `hitPanther`), `woedeStart` (G, de meter, de knop `woede` in `TOUCH_BTNS`), `woedeAan` houdt `hurtPlayer`, `valLand` en `fosforBijt` tegen, `woedeGloed` en `woedeVonken` bij het tekenen van Amir. Elke episode begint met de tribekeuze (`runStart` in zijn speelknoppen, en bij dubbelklikken op een kaartje in `buildCards`), nu De Poorten en Baboon tests; de Test levels niet, tenzij daar expliciet om gevraagd wordt, en daar gelden alle abilities van de tribes die niet op slot staan, net als in de Test van de Maker (Test 14 laat je kiezen, zie `talentKeuze`). Een tribe op slot (nu Impungushe) mag al abilities hebben: die gelden dan alleen in de sandbox en in Test 14; zijn boom laat ze dicht zien en zijn kaart op het keuzescherm blijft leeg. De sandbox heeft `sbAbilities`, de speelrobot speelt zonder tribe en dus zonder abilities. De plaatjes in `design/tribes/` komen uit `tools/tribe_logos.py`; de drie ability-plaatjes van Bhubesi zijn uitgeknipt (tot 400 bij 400, grijs eromheen doorzichtig) uit de JPG's in `notities/` (`notities/fastereimmortal.jpg`, `notities/longerimmortal.jpg`, `notities/extralife.jpg`), waarvan twee namen omgewisseld zijn: `fastereimmortal.jpg` is Long Breath, `longerimmortal.jpg` Blood Rush, `extralife.jpg` Fourth Life

## T-splitsing in de talent tree

een talent met `varianten` in `TRIBE_CONFIG` krijgt naast zijn naam een gestippelde splitsing met de namen (`tbSplit`, `.tbsplit`) en in het venster de varianten met hun tekst (`.tbivar`). Nog niets te kiezen; nu alleen bij Jackal Fang. Een tribe op slot laat zijn talents dicht zien; `TB_LEEG` alleen als hij er nog geen heeft Tijdelijk getekend: het plaatje komt uit `tools/mes.py` (`design/mes/mes.png`), zijn lijf schiet naar voren omdat er geen frames met een mes zijn. De kalebas is de speertekenvariant `kalebas`

## De talents van de rol-worp: True Flight (Mkuki) en The Pounce (Bhubesi)

Het vierde talent van beide trees, met een getekend teken in `TB_TEKEN` tot er een houten plaatje is.

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
