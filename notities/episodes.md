# De episodes en het verhaal

## het verhaal bij een episode

`VERHAAL` en `SLOT`, `verhaalToon()`: tekst op een zwart scherm voor elk level en na het laatste, alleen als je bij het eerste level begint. Op de naam van het level, dus een nieuwe episode hoeft alleen tekst toe te voegen en `verhaalAan` te zetten in zijn speelknop

## Episode De Valse Koning

`VK_1` tot en met `VK_8` en `VK_LEVELS`: acht zware levels met een verhaal (`VERHAAL`, `SLOT`) en Nightmare; menu `menuVK`, `cardsVK`, knop `btnVK` in `menuEpisodes`. Het is nu de enige echte episode (regel 1). De Poorten, De Honingjacht, De Hoge Schijven, De Klim en De Diepte zijn eruit, samen met de zwaardvechter; in Valse Koning 1 en 5 stappen nu twee bandieten op het zegel met het teken van de val (`zegelVijand` en `ravijnLaatVallen` tellen de bandiet mee).

## Episode Test levels

`TEST_1` tot en met `TEST_36`: korte proefstukken, los van de echte episodes. Het menu toont de laatste zes (`KAART_BLAD`); de rest staat achter de knop **Oude tests** (`btnoudetests`, `testOud`, `testToon`). Dat venster komt uit de volgorde van `TEST_LEVELS`, dus een nieuw testlevel duwt vanzelf het oudste het archief in; `markCards` opent het archief als het gekozen level erin staat. Test 14 heeft `talentKeuze`: een scherm voor het begin (`talentKeuzeToon`, `testTalents`, in de pauze `pzkeuze`) waarop je de talents kiest, ook die van een tribe op slot

## Episode Baboon tests

`BAB_1` tot en met `BAB_4` en `BAB_LEVELS`: proefstukken voor de baviaan, met de tribekeuze (`runStart`) zoals De Valse Koning; menu `menuBab`, `cardsBab`. Baboon 1 is de wand en de kooi, Baboon 2 dezelfde vlakte met de speerbeet in plaats daarvan, Baboon 3 de speerval, Baboon 4 de goudaap-arena (`apenArena`, zie hieronder). De eerste en de derde stonden eerst tussen de Test levels
