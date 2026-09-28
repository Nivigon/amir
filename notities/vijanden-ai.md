# De AI van de vijanden: getest, en wat er beter kon

Alle vijanden en de twee eindbazen zijn in losse proefstukken gezet met `tools/vijandtest.js` (zie
CLAUDE.md): een vijand of een paar, soms met een kei of een ravijn ertussen, en Amir die op een vaste
manier speelt (stilstaan, gebukt zitten, weglopen, op een kei staan, springen, of vechten als een
redelijke speler). Per scenario meet de test wie Amir raakt, wie hij verslaat, hoe lang elke vijand in
welke toestand stond, of hij ergens bleef hangen, of hij over een kei of ravijn kwam (regel 7) en of hij
zijn aanval al begon voor hij in beeld was.

Draai hem opnieuw na elke wijziging aan een vijand:

```
node tools/vijandtest.js              alle 44 scenario's (drie tegelijk, zo'n kwartier)
node tools/vijandtest.js zwaard       alleen de zwaardvechter
```

## Wat mis was, en nu gerepareerd

| vijand | wat er gebeurde | nu |
| --- | --- | --- |
| baviaan | buiten de kooi rende hij over een ravijn gewoon door, door de lucht, en hapte hij Amir aan de overkant | aan de rand remt hij af en blijft hij grommend staan (`bavRavijnRand`, `BAV_RAND`); happen over een ravijn doet hij nooit meer |
| fosforslangen | liepen ze in hun aanval tegen een ravijnrand, dan bleven ze daar voorgoed kronkelen, alle drie op dezelfde pixel | ze richten zich aan de rand op (`wacht`), sluiten een halve lengte achter elkaar aan (`fosforMaatVoor`) en blijven Amir aanstaren tot hij van plek verandert (`klemW`) |
| zwaardvechter | tegen een kei of ravijnrand rende hij telkens 1,2 seconde ter plekke, dan dreigde hij een seconde, en weer opnieuw | kan hij geen pas naar je toe zetten, dan blijft hij dreigen (`zwKanStap`) |
| schorpioen | hij zag je op 900 px, dus buiten beeld: zijn dreighouding viel buiten beeld, en op een telefoon ook zijn aanloop | hij ziet je pas als hij met zijn hele lijf in beeld staat (`scpZicht`, net als `zwZicht`) |
| panter | stond Amir op een kei toen de panter kwam, dan verscheen die midden in de kei; en naast een kei klauwde hij eindeloos onder Amir door, zonder afkoeltijd, dus ook zonder ooit in zijn herstel te komen | `panBaan` telt de kei onder Amir niet als kei ertussen; hij klauwt alleen als zijn klauw kan raken (`CLAW_SAFE_H` is nu `CLAW_HIGH`), en aan de voet van een kei blijft hij ingedoken liggen loeren |
| slangen | twee of drie slangen van dezelfde kant lagen precies op elkaar | ze sluiten achter elkaar aan (`slangInRij`, `SLANG_RIJ`); valt de voorste weg, dan kruipt de volgende door |

Wat er gemeten is, voor en na:

| scenario | voor | na |
| --- | --- | --- |
| baviaan achter een ravijn | 2 keer gebeten, over het ravijn heen | 0 keer, wacht 5 s aan de rand |
| fosfor achter een ravijn | 11 s in de aanval tegen de rand, alle drie op -1191 | staren, verspreid over -1314, -1238 en -1191 |
| zwaard op een kei / achter een ravijn | 6,8 s en 5,2 s ter plekke rennen | 0,7 s en 0,3 s rennen (tot de rand), daarna dreigen |
| schorpioen aanlopen | dreighouding begint op 895 px, 0,8 s voor hij in beeld is (telefoon: 1,9 s) | begint op 543 px (telefoon 375 px), nadat hij in beeld is |
| panter, Amir op een kei | 15,6 s klauwen in de lucht, midden in de kei | ligt aan de voet te loeren, 0 klappen |
| drie slangen | alle drie op -66 | op -67, -187 en -307 |

## Wat werkt zoals bedoeld

- **Regel 7** houdt stand: in geen enkel scenario kwam een slang, zwarte slang, schorpioen, zwaardvechter,
  hyena, panter of fosforslang over een kei of ravijn. Hyena's tussen twee keien raken Amir niet.
- **De vechter-speler** verslaat een slang, een zwarte slang, een schorpioen, twee zwaardvechters, twee
  hyena's, drie fosforslangen en de panter; de panter in zo'n 40 s, zonder een klap. De vijanden zijn dus
  te verslaan zonder dat je hoeft te gokken.
- **Het buk-trucje van de fosforslangen** werkt: gebukt stilzitten laat ze verstenen, en zo gaat er een neer.
- **Een slang of schorpioen naast een kei** bijt en steekt Amir bovenop de kei, zoals regel 7 zegt.
- **De baviaan** springt over een kei heen en hapt Amir daarbovenop (een eindbaas mag dat).

## Voorstellen (niet ingebouwd, eerst jouw oordeel)

Zet er een oordeel achter, net als in `combinaties.md`.

| # | wat | waarom | oordeel |
| --- | --- | --- | --- |
| 1 | **De zwarte slang spuwt over een ravijn.** Nu kijkt hij aan de rand even, draait om en loopt drie seconden weg, telkens opnieuw: over een ravijn spuwt hij nooit (gemeten: 14 s lang geen enkel schot). | Juist de spuwer is de vijand die over een gat heen iets kan; het ravijn blijft een schuilplek tegen zijn beet. | ? |
| 2 | **Bukken ontwijkt het gif.** Het gif mikt op 0,55 van Amirs lengte en gebukt is hij 0,68 hoog, dus gebukt word je gewoon geraakt (5 van de 5 keer). | Nu is weglopen of springen de enige verdediging; bukken zou een tweede zijn, en het is wat een speler als eerste probeert. Mikken op 0,8 is genoeg. | ? |
| 3 | **Hyena's komen terug.** Een hyena stormt een keer langs je heen het beeld uit en is dan weg; een roedel is dus twee keer springen. | Een tweede ronde (omdraaien buiten beeld, nog een keer dreigen) maakt een roedel een gevecht in plaats van een hindernis. | ? |
| 4 | **De zwarte slang spuwt niet buiten beeld.** Hij blijft je volgen tot 1700 px en spuwt dan ook, maar gif dat meer dan 200 px buiten beeld begint wordt meteen weggegooid. | Nu staat hij buiten beeld voor niets te spuwen; het scheelt niets in het spel, alleen in wat hij doet. | ? |
| 5 | **De panter klauwt minder vaak als je stilstaat.** Stilstaan naast de panter kost acht klappen in zestien seconden: de klauw heeft geen afkoeltijd (dat is de harde regel). | Met een korte afkoeltijd na een klauw die mist of raakt zie je zijn andere aanvallen vaker. Kan ook zo blijven: het straft stilstaan, en dat is de bedoeling. | ? |
