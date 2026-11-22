# Mkuki: frames om na te lopen en zo mogelijk opnieuw te maken via Grok

Stand 22-11-2026. Dit zijn de frames waar de houding (draaiing, armen, voeten, hoogte) niet goed genoeg op het
origineel lijkt. De plaatsing van de speer staat hier NIET in: die doet Tom in de Animeer tool.

Paden: het Mkuki-frame staat onder `karakters/amir/mkuki/<pad>`, het origineel onder `karakters/amir/<pad>`.
Uitzondering: de speerworp-originelen staan in `amir runc/amir_sprites/design/amir/speerworp/`.
Per frame staat in `../LOG.md` welke Grok-post en prompt het nu is.

Prioriteit: **A** = zichtbaar fout, eerst doen. **B** = wijkt af, verbeteren als het lukt. **C** = alleen kijken.

| prio | pad (onder karakters/amir/) | wat er mis is | wat het moet worden (uit het origineel) |
| --- | --- | --- | --- |
| A (af 22-11, Grok 10138fbb) | beweging/run/nieuw/ren_sp_4.png | noodgreep: benen uit het origineel geplakt, vuist rafelig, voeten rood-paars | gekruiste benen (kruismoment van de ren); Grok tekende steeds een wandelpas. Mogelijk al gedaan in de chat over de rencyclus: eerst nakijken |
| A (af 22-11, Grok 0a0007d5) | beweging/run/nieuw/ren_sp_10.png | idem | idem |
| A (niet gelukt, 3x rechtop met borst naar ons; zie LOG 22-11) | beweging/rol/worp/worp_12.png | romp te rechtop, borst naar ons | profiel links, leunt voorover in een lange uitstap |
| A (af 22-11, Grok 17ac79af) | beweging/rol/worp/worp_27.png | borst naar ons | draait al met de rug naar ons, arm ver naar voren-onder |
| A (af 22-11, Grok 8dcea7bc) | beweging/rol/worp/worp_26.png | beeld van 24/25 hergebruikt | buigt naar links, arm in een boog over het hoofd |
| A (af 22-11, Grok ae7d9ae6) | aanval/lowsweep/sweep_8.png | beide handen op de grond | voorste arm horizontaal naar links, driekwart rug |
| A (niet vervangen: hoofd al even hoog als origineel, Grok niet dieper; LOG 22-11) | aanval/stofsweep/stof_07.png | te hoog | diep op de hurken |
| A (niet vervangen, idem) | aanval/stofsweep/stof_08.png | te hoog | diep op de hurken |
| B | beweging/rol/worp/worp_5.png | voeten te dicht bij elkaar | voeten verder uit elkaar, verspringend |
| B | beweging/rol/worp/worp_24.png | voorste arm te laag | voorste arm hoger, naar links |
| B | beweging/rol/worp/worp_15.png t/m worp_23.png | een Grok-beeld voor alle 9; achterste vuist te laag | vuist vlak boven het hoofd; eventueel per frame een eigen beeld voor beweging |
| B | aanval/lowsweep/sweep_10.png | armen te kort | armen ver naar rechts gestrekt |
| B | aanval/lowsweep/sweep_13.png | trap hoger, standbeen rechter; met de hand geplaatst | zijtrap zoals origineel; overgang 12 naar 13 controleren |
| B | aanval/lowsweep/sweep_9.png | romp te rechtop | bijna plat voorover |
| B | aanval/lowsweep/sweep_6.png | linkerarm korter | arm verder |
| B | aanval/combo/combo_06.png | bovenste vuist te laag | vuist hoog boven het hoofd |
| B | aanval/combo/combo_07.png | bovenste vuist te laag | idem |
| B | aanval/combo/combo_02.png | voeten smaller | bredere stand |
| B | speerworp/speerworp_15.png | achterarm te gestrekt | zoals origineel |
| B | speerworp/speerworp_16.png en speerworp_17.png | voorste arm reikt minder ver | verder naar voren |
| B | speerworp/speerworp_12.png | voorste hand een vuist | open hand |
| B | aanval/speerstrike/ frame 4 en 9 (bestandsnaam in LOG.md, sectie Speerstoot) | 4 leunt minder voorover, 9 staat rechter | zoals origineel |
| B | beweging/rol/zonder/rol_25.png | hand reikt minder ver | hand verder naar voren naar de grond |
| B | beweging/rol/met/rol_17.png en rol_18.png | vuisten niet op de handpunten | vuisten op de plek van de originele handen |
| C | beweging/rol/met/rol_22.png | benen iets anders | |
| C | beweging/run/nieuw/ren_ns_10.png | IoU laag, volgt de omtrek | |
| C | beweging/jump/jump/amirjump2afzet.png | hoofd van Grok | naast de rest leggen |
| C | idle/idle_sp/idle_sp_10.png en idle_sp_12.png | hoofd kijkt in Grok iets omhoog | |
| C | aanval/combo/combo_12.png t/m combo_14.png | achterste vuist bij de heup | met speer erop bekijken |
| C | aanval/stofsweep/stof_10.png t/m stof_13.png | vuisten zichtbaar voor het gezicht | met speer erop bekijken |

Algemeen (alle sets van voor 21-11 17:51): het verre been en de verre arm zijn niet donkerder, zoals in het origineel
wel. Dat is geen Grok-werk maar een nabewerking (zie TWIJFEL.md, "Voor- en achterkant van de ledematen").
