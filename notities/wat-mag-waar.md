# Wat mag waar: vast, los, plant en ver

### Wat mag waar: vast, los, plant en ver

Elk ding in een level valt in een van vier soorten, en de soort bepaalt wat er gebeurt bij een
ravijn, bij een ravijn dat later openscheurt (een rune of een zegel) en in een gang.

| soort | wat | boven een ravijn | waar later een ravijn openscheurt | in een gang |
| --- | --- | --- | --- | --- |
| vast | keien, hutten en andere props met `bouwwerk`, doornbossen, skeletten, speertekens | nooit | nooit: ze gaan naar de rand | op de bodem, en niet hoger dan de gang |
| los | botten (`RAVIJN_DECOR.valt`), kalebassen, dorpelingen | nooit | mag: het valt erin | op de bodem |
| plant | gras, struik, boom, schilden en ander laag decor | nooit | mag: het schuift naar de rand, of vervaagt als daar al iets staat | op de bodem, en niet hoger dan de gang |
| ver | props met `v` die hoger staan dan `FAR_GAP_LIFT` | mag | mag | blijft boven op de savanne |

Wat Amir tegenhoudt staat daar los van: een kei draagt (je springt erop), een doornbos houdt je
tegen tot je hem kapt, en al het andere is decor waar je doorheen loopt.

De soort staat niet op een plek, maar zit in vijf functies. Een nieuw ding krijgt dus eerst een
soort, en komt dan in alle vijf:

1. `schoonLevel`: schuift het uit een ravijn bij het laden (behalve ver decor);
2. `schoonKomend`: schuift vaste dingen weg waar later een ravijn openscheurt;
3. `ravijnDecor` en `ravijnDecorReset`: wat er gebeurt als het ravijn toch onder iets openscheurt
   (in de sandbox), en dat een herstart het terugzet (`x0` of `rv`);
4. `tools/levelcheck.py`: de regels `boven een ravijn`, `waar een ravijn openscheurt` en `onder de
   grond`, met de maten uit de code;
5. `placeProblem`, als het in de bouwer neer te zetten is. Skeletten en speertekens staan er
   sinds de nieuwe bouwer ook in (`skelet` en `teken`).

Voor een speerteken staan de maten per variant in `TEKEN.varianten`: `voet` is van waar tot waar
het op de grond staat (het liggende stuk en de schedels in het zand tellen mee, dus niet
symmetrisch om `x`), `hoog` tot waar de speer reikt. Een teken is 0,86 tot 1,34 Amir hoog, dus
in een gang minder diep dan zo'n 530 steekt de speer door het dak.
