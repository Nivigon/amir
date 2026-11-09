# Ideeën voor de kit van Amir

Nog niets hiervan is gebouwd. Dit is de stand van het gesprek over wat Amir mist, vooral in gevechten
met meerdere bandieten: nu is de truc door ze heen rennen, een treffer van achteren en omdraaien, en dat
voelt lame. De rol-worp als finisher voelt juist goed.

## Hoe we indelen

- **Basis kit**: alles waar een level of vijand op moet kunnen rekenen. Test levels en de speelrobot spelen
  zonder tribe, dus wat daar moet werken hoort in de basis.
- **Tribe-ability**: wat je meteen krijgt als je de tribe kiest en wat je speelstijl bepaalt (zoals de woede
  bij Bhubesi, G).
- **Talents**: maken de ability of de basis sterker of geven een andere draai. Een talent mag bij twee tribes
  passen.
- De tribes blijven fysiek en geloofwaardig: geen magie bij Mkuki (terugroepen van de speer viel daarom af).

## Nu aan de beurt: stof in de ogen

**Gebouwd, met de eigen animatie.** `STOF`, `STOFA`, `stofStart`, `stofStap`, `stofWerp`, `stofEind`, `stofRaak`,
`stofDwaal`, `stofTeken`. Onder Speer en spullen de knop **Stof (X)**; staat hij aan, of heeft het level `stof: true`
(Test 63; `restart` zet `STOF.aan` uit het level), dan doet X de stofveeg.

De animatie staat in `karakters/amir/aanval/stofsweep/` (14 frames, `metadata.json`, ook in `klein/`): Amir staat
zijwaarts met de speerpunt achter zich op de grond (frame 0, 6 ticks: de tell), schraapt de punt over de grond naar voren,
zet een pas en draait door tot zijn rug naar de camera staat, de speer schuin omhoog (de veeg 0,46 s, daarna 12 ticks
uithouden). Eigen frame-teller (`stofA`, ticks van 1/24 s uit `STOFA.ticks`), eigen canvas en voetpunt (`STOFA.W`, `H`,
`GROUND`, `ANKER`), schaal `STOFA.schaal` (49/53: zijn hoofd in de clip tegen idle_ns). De frames kijken naar links en
spiegelen zoals de gewone sets. De standvoet blijft staan en de pas zit in de frames; aan het eind zet `stofEind` Amir
op het lijfmidden van het laatste frame (`STOFA.EIND`, niet over een ravijn), net als de rol. Tijdens de veeg staat hij
(`dir = 0`), en steken, werpen, springen, rollen, bukken, de lage zwaai en de renstoot wachten tot hij klaar is. Een
treffer, een val of een sprong breekt hem af. Lui geladen (`stofLaad`, `stofLaadLevel` in `laadLevel`, en bij het
aanzetten van de sandbox-knop); zonder frames gaat X niet af.

Het geluid `sounds/stofveeg.mp3` (ElevenLabs, 1 s: het schrapen piekt van 0,15 tot 0,45 s) gaat af als de punt de grond
raakt (frame 1, `STOFA.geluid`), via `banStemmen`/`banStemSpeel`, zodat het ook op een telefoon klinkt. De opname was te
zacht (gemiddeld -25 dB); hij is 18 dB opgehaald met een limiter (ffmpeg `volume=18dB,alimiter=limit=0.97`), nu
gemiddeld -13,5 dB, zo hard als de zwaardslag van de bandiet, en speelt op vol 1. De zachte versie zit in de git-geschiedenis.

De stofwolken (`STOF_FX`): tijdens het schrapen (frame 1 tot 8, `stofSchraap`) komt aan de speerpunt een sliert stof en
korrels op, steeds meer naarmate hij naar voren komt; waar de punt per frame staat zegt `STOFA.punt` (canvas-x op de
grondlijn). Op `STOF.werpFrame` (9, de punt laat de grond los) gooit `stofWerp` drie dingen: een waaier zand
(`stofStraal`, korrels als streepjes in een boog naar gezichtshoogte, eigen stap en tekenlaag `stofStraalStap`,
`stofStraalTeken`; geland verdwijnen ze), een pluim wolken over de hele baan tot `STOF.bereik` die oploopt van de grond
naar gezichtshoogte en blijft hangen (`stofWolk`, de zweef van de baviaan, met een zandkleurige kern onder het plaatje:
`kleur` in `wdust`), en een dikke wolk aan de punt, met een tikje schok. Wie geraakt wordt krijgt een wolk om zijn hoofd en
zand dat van hem af valt (`stofRaak`). In de sneeuw (`stofSneeuw`) is het allemaal wit. De veeg
zelf raakt niets, alleen `stofWerp` verblindt. Een bandiet voor Amir, binnen `STOF.bereik`, op zijn niveau
(`banZelfdeHoogte`) en met zijn gezicht naar Amir krijgt `s.verblind = STOF.duur`: hij wankelt eerst weg van Amir en dwaalt
dan heen en weer in de patrouillegang (`walk`) rond die plek, valt niet aan en werpt niet (`updateBandiet` keert vroeg
terug), met drie draaiende zandsterretjes boven zijn hoofd. De volgende treffer in `hitBandiet` telt dubbel (met `critFx`)
en maakt hem wakker; met twee levens is hij dan dood. Alleen de bandiet nog. Let op: van de knop tot het stof duurt het
0,58 s, en een bandiet die op Amir af stormt is dan al bij hem; zijn slag wordt afgebroken als het stof hem raakt.
Testlevel: **Test 63: Stof in de ogen**, drie gewone bandieten na elkaar met hun gezicht naar Amir.

**Bij Mkuki, en voor elke vijand uit De Gouden Poort.** De stofveeg hoort bij de tribe Mkuki zelf (geen talent):
`stofveeg: true` in zijn blok in `TRIBE_CONFIG`, en `stofVanTribe` zet `STOF.aan` in elk level (in `restart`, en meteen
bij `tribeVastleggen`). In de Test levels zonder tribe heb je alles, dus ook dit. Op de telefoon is er een stofknop
(`stof` in `TOUCH_BTNS`, `drawBtnStof`) en de uitleg van de toetsen bij het begin noemt X (`HINT_START`).

Afkoeling: `STOF.koel` (8 s), vanaf het stof (`stofKoel`, `stofGereed`). Blind is 4 s met een dubbele treffer erna, dus
ongeveer een keer per gevecht. In de HUD een tegel naast de lage zwaai (`#stofhud`, `stofHud`) met de taartpunt die
wegdraait, op de telefoon een ring om de knop; te vroeg drukken schudt de tegel.

Wie verblind wordt staat in `STOF_SOORTEN`: de bandiet, de schildbandiet, de kruisboogbandiet, de zweepman, de kooiman en
de slangen (alles wat in De Gouden Poort meedoet). Per soort: of hij nu te verblinden is (niet dood, niet midden in een
sprong, slag of hoorn), zijn kijkrichting, zijn hoogte, hoe zijn blindheid begint, waar zijn hoofd zit en zijn kreet. Elke
update heeft een blinde tak (`stofTel`, `stofKeer`: traag heen en weer rond de plek, niet aanvallen), elke hit-functie een
dubbele treffer met `critFx`, en een blinde schildbandiet dekt zich niet, een blinde zweepman en kooiman zijn altijd te
raken (`zwmF1Kwetsbaar`, `kooiRaakbaar`). Bazen (de panter, de baviaan, Nyundo) staan er niet in. De kreet (`stofKreet`):
de mannen krijgen `sounds/banditpijn.mp3` (het begin van de doodskreet van de bandiet, 10% hoger, 0,5 s, met ffmpeg uit
`banditdeath.mp3`), elk op een eigen toonhoogte (`toon`); de zweepman zijn eigen `zweepgeraakt`; een slang sist.

Het idee:

- Werkt alleen als de vijand naar Amir kijkt (sluit aan op `zicht`, de halve cirkel voor hem).
- Verblind: hij loopt een stukje heen en weer, met een symbooltje boven zijn hoofd, en ziet Amir even niet.
- Kwetsbaar: een speertreffer telt dubbel (het mechanisme van True Flight, `critPak`, ligt er al).
- Later: wie zo'n verblinde vijand aanvalt doet een vette move, bijvoorbeeld een spin strike die rondom raakt
  (ook achter je, dus een antwoord op een groep). Daar zijn nieuwe frames voor nodig.
- Aandachtspunten: slangen, schorpioen en fosforslang niet verblinden (hooguit de hyena), een schildbandiet
  met het schild omhoog vangt het stof, een baas kort of niet. Het stof volgt de grond (zand, gruis in de
  stad, sneeuw in de winter). De beweging lijkt op de lage zwaai, die al zand wegveegt bij een verstopt zegel.
- Bij welke tribe hij hoort is nog open.

## Basis: de bandiet draait mee

Rent Amir langs of door een bandiet, dan draait die mee met een backhand-houw of stapt opzij. Door een groep
heen rennen kan dan nog, maar alleen met timing. Bij twee of meer kan er taakverdeling bij: een stormt, de
ander houdt afstand en werpt zijn dolk.

## Mkuki (de speer): snel, vluchtig, op afstand

- **Een speer extra op de rug**: 2 in plaats van 1 (`RUG_MAX`), dus 3 worpen voor je melee-loos bent.
- **De dubbele worp** (de tribe-ability): F nog eens vlak na het loslaten (rond 0,3 s) en Amir grijpt in een
  beweging over zijn schouder en gooit meteen een tweede, vlak en snel, zonder opspannen. Past op de beat
  `RUG.trek` / `rugTrekKlaar`. Een bandiet (twee levens) gaat er van afstand mee neer, maar dan liggen er
  twee speren in het veld. Eerste versie: de gewone worp versneld, echte frames later.
- Talents eromheen: Quick Hand en True Flight passen al; vastpinnen of doorboren (de speer pint een vijand
  tegen een muur of gevel en blijft hangen, of gaat door twee op een rij heen; bouwt op de speer in de borst
  van de kruisboogbandiet, `krbSpeerVolg`); de dubbele worp ook vanuit de rol.

## Bhubesi (de leeuw): Stilte voor de storm

Laag en stil blijven (bukken, stilstaan) laadt een burst op, met een cap: harder slaan, of sneller en hoger.
Liever voor de volgende paar aanvallen dan een paar seconden. Per talent een effect, via de T-splitsing.
Zichtbaar en hoorbaar laden (stof dat om hem heen trekt, een hartslag). Kan de woede voeden. Past bij de
loerende leeuw van Lion's Patience, en bukken is al het antwoord op de dolk van de bandiet.

## Later

- **Spirit guide**: speer in de grond, ogen dicht, naar de camera, en een geest van Amir doet een paar seconden
  zijn aanvallen na (gespiegeld achter hem, of met een kleine vertraging als echo). Kan niet dood. Voelt als de
  kern van een eigen, nieuwe tribe.
- **Neerhalende sweep**: de lage zwaai legt sommige vijanden op de grond. Heeft een opstaan-animatie nodig;
  om te proeven kan het begin van de doodset van de bandiet omgekeerd.
- **Verdoven** met de rol-worp, als talent (een splitsing naast doorboren).
- Afgevallen: een parry met de speer (te dicht op het schild), terugroepen van de speer (magie).
