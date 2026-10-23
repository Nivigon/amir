# De episodes en het verhaal

## het verhaal bij een episode

`VERHAAL` en `SLOT`, `verhaalToon()`: tekst op een zwart scherm voor elk level en na het laatste, alleen als je bij het eerste level begint. Op de naam van het level, dus een nieuwe episode hoeft alleen tekst toe te voegen en `verhaalAan` te zetten in zijn speelknop

## Episode De Poorten

`POORT_1` tot en met `POORT_6` en `POORT_LEVELS`: zes zware levels met een verhaal (`VERHAAL`, `SLOT`) en Nightmare; menu `menuPoort`, `cardsPoort`. Elk level heeft een poort die opengaat met een zegel, een runeschijf, rijzende grond of een zakkend plafond, elk level een ander uitzicht en ander weer, en samen alle vijanden, de panter en de baviaan. Wat de speler met zijn speer moet raken staat er altijd rechtop (een `runes`-schijf op een rots), nooit plat: een zegel stap je op. `tools/runecheck.js` rekent per schermformaat na of elke schijf te raken is met de schijf in beeld. Wat werkt en wat niet staat in `notities/combinaties.md`: lees dat voor je een nieuw level of een nieuwe combinatie bedenkt, en stel ideeën daaruit voor in plaats van ze zomaar in te bouwen

## Episode De Hoge Schijven

`HOOG_1` tot en met `HOOG_5` en `HOOG_LEVELS`: vijf zware levels met een verhaal (`VERHAAL`, `SLOT`) en Nightmare; menu `menuHoog`, `cardsHoog`, knop `btnHoog`. Elke schijf is een rune op een rots met een `opstelling` uit `RUNE_OPSTELLINGEN` (`kei`, `terras`, `boog`, `gang`) en doet iets met rijzende grond: een blok in een ravijn, een brug op terrashoogte, een trage lift naar een terras, en in Hoog 4 een lift uit de gang (een rijzer met `van` op de bodem van de gang, die `levelcheck.py` als weg naar boven telt). Daartussen zakkende stenen (`zak: true`), een sprintsprong (ongeveer 425) uit elkaar en 350 breed, met kieren van 200 tot 250. Nagelopen met `tools/runecheck.js` op 1280 bij 720, 1920 bij 1080 en 852 bij 393: elke schijf te raken met de schijf in beeld, en de plek vanwaar je raakt ligt nooit boven een ravijn. De lifts zijn zo traag gezet dat je ze op elk scherm haalt

## Episode Test levels

`TEST_1` tot en met `TEST_36`: korte proefstukken, los van de echte episodes. Het menu toont de laatste zes (`KAART_BLAD`); de rest staat achter de knop **Oude tests** (`btnoudetests`, `testOud`, `testToon`). Dat venster komt uit de volgorde van `TEST_LEVELS`, dus een nieuw testlevel duwt vanzelf het oudste het archief in; `markCards` opent het archief als het gekozen level erin staat. Test 14 heeft `talentKeuze`: een scherm voor het begin (`talentKeuzeToon`, `testTalents`, in de pauze `pzkeuze`) waarop je de talents kiest, ook die van een tribe op slot

## Episode Baboon tests

`BAB_1` tot en met `BAB_4` en `BAB_LEVELS`: proefstukken voor de baviaan, met de tribekeuze (`runStart`) zoals De Poorten; menu `menuBab`, `cardsBab`. Baboon 1 is de wand en de kooi, Baboon 2 dezelfde vlakte met de speerbeet in plaats daarvan, Baboon 3 de speerval, Baboon 4 de goudaap-arena (`apenArena`, zie hieronder). De eerste en de derde stonden eerst tussen de Test levels
