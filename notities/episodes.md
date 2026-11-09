# De episodes en het verhaal

## het verhaal bij een episode

`VERHAAL` en `SLOT`, `verhaalToon()`: tekst op een zwart scherm voor elk level en na het laatste, alleen als je bij het eerste level begint. Op de naam van het level, dus een nieuwe episode hoeft alleen tekst toe te voegen en `verhaalAan` te zetten in zijn speelknop

## Episode De Valse Koning

`VK_1` tot en met `VK_8` en `VK_LEVELS`: acht zware levels met een verhaal (`VERHAAL`, `SLOT`) en Nightmare; menu `menuVK`, `cardsVK`, knop `btnVK` in `menuEpisodes`. Het is nu de enige echte episode (regel 1). De Poorten, De Honingjacht, De Hoge Schijven, De Klim en De Diepte zijn eruit, samen met de zwaardvechter; in Valse Koning 1 en 5 stappen nu twee bandieten op het zegel met het teken van de val (`zegelVijand` en `ravijnLaatVallen` tellen de bandiet mee).

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
episode in de zin van regel 1 (alleen De Valse Koning is bevroren), maar ook geen proefstuk: pas ze aan als de opdracht erom vraagt.
Geen baas (regel 12). Met de tribekeuze (`runStart`); een knop in `menuEpisodes` (`btnBel`), het scherm `menuBel` met `cardsBel`.
De opbouw leunt op de stadlevels: 1 en 6 op Stad 1 (lift en toren), 2 op Stad 2 (trappen), 3 op Stad 3 (bruggen), 5 op Stad 4
(de koningsweg); 4 en 7 zijn nieuw. Level 7 heeft een `bandietGolf` met dolken bovenop de vaste spawns.

## Episode Baboon tests

`BAB_1` tot en met `BAB_4` en `BAB_LEVELS`: proefstukken voor de baviaan, met de tribekeuze (`runStart`) zoals De Valse Koning; menu `menuBab`, `cardsBab`. Baboon 1 is de wand en de kooi, Baboon 2 dezelfde vlakte met de speerbeet in plaats daarvan, Baboon 3 de speerval, Baboon 4 de goudaap-arena (`apenArena`, zie hieronder). De eerste en de derde stonden eerst tussen de Test levels

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
10 het plein met Nyundo bij nacht, `hp: 24` en rode oker (`tint`); 11 de derde winkel en een kist boven op de toren (1388);
12 schutters op alle galerijen, een kist boven in een huis; 13 drie rivieren (de laatste zonder brug), de vierde winkel en twee
kisten; 14 onweer, een `bandietGolf` en de grote dam met een kist op de stelling; 15 een golf die niet ophoudt en Simba Kivuli (20,
`sluip: false`). De tinten van de bazen staan in `RIV_TINT`.

## de schatkist: E en het goud spat eruit

`KIST`, `kisten`, `kistMaak`, `kistReset`, `kistE`, `kistStap`, `drawKisten`, `kistLaadLevel`

`kisten: [{x, y, vast, goud, f}]` in het level, `y` en `vast` zoals bij de munt (een dak of galerij via `stadKalebasPlek`, met `vast`
precies op `y`, binnen op een verdieping). Het plaatje is de kist uit de winkel (`design/stad/binnen/spul_kist.png`), lui geladen.
E erbij (`kistE`, in `eDruk` na `muntE`) tilt het deksel op, `KIST.munten` munten springen eruit, en in een level met goud komt
`goud` (zonder veld `KIST.goud`, 20) bij je goud. `goudReset` roept `kistReset`: na een dood zijn de kisten weer dicht, net als de
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

Alleen in een level met `goud: true`. `vijandDood` roept `goudKill`: `GOUD.perKill` goud. De HUD (`#goud`) staat naast de
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
