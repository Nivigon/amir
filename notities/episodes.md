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
kaart als een dobbelsteen met zes ogen, met poorten ertussen en een minimap; je speelt een level uit met 50 kills (het
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
5 De Kroonwijk, acht straten als een kroon (`GP_5_STRATEN`, `doel: 0`), kapitein Zaki in de Goudsmedenpunt; 6 binnen en de
tweede winkel; 7 Kwame de poortwachter en de eindpoort (een pleinpoort met `einde: true`); 8 het plein met Nyundo, zoals
Stad 6; 9 de garde, de derde winkel en de schatkamer met de kluis; 10 een `bandietGolf`, geen winkel, de goudvorst (16 levens,
`sluip: false`).

## goud: een goudstuk per kill, de winkelprijs en de munt van de koning

`GOUD`, `goudAan`, `goudKill`, `goudReset`, `goudWin`, `goudVerder`, `goudBegin`, `muntE`, `drawMunt`

Alleen in een level met `goud: true`. `vijandDood` roept `goudKill`: `GOUD.perKill` goud. De HUD (`#goud`) staat naast de
kalebassen. In de winkel (`winkelUIToon`, `#wkkalebas`) kost een kalebas `GOUD.kalebas` en draag je er hooguit `HPPOTION_MAX`;
zonder goud blijft de winkel gratis. `winLevel` onthoudt goud en gedragen kalebassen (`goudWin`), pas `wnnext` zet ze op de
bank (`goudVerder`), en `restart` zet alles terug op de bank (`goudReset`, na `resetHppotions`): wie sterft is het goud van dat
level kwijt, en Opnieuw na een gewonnen level geeft geen dubbel goud.

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
