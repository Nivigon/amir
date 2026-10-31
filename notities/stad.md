# De stad: een Sahelstraat van leem

`STAD`, `stadAan`, `stadLaad`, `stadLees`, `stadPlats`, `stadAchter`, `stadTeken`, `stadVeer`, `stadSprong`

Een level met het veld `stad` speelt in een drukke straat van een Sahelstad, overdag (uitzicht `stad_dag`).
De onderdelen staan in `design/stad/`, met alle maten in `design/stad/metadata.json`. Test 59 is het proefstuk;
in de sandbox onder Terrein de knoppen **De stad** (Neerzetten, Weg).

```
stad: { paleis, seed, gevels: [{x, hoog, f}], galerijen: [{van, tot, h}],
        kramen: [{x, soort, f}], voet: [{x, stuk, f}] }
```

## De straat

`design/stad/straat.png` komt in de plaats van de grondrand (`bodemPic`). Het plaatje heeft precies de maten en
rijen van `EDGE` (1572x335, kruin 46, walk 95, solid 305), dus ravijnen, terrassen en de Maker werken er zonder
iets anders mee. Het is gemaakt door Grok de grondrand te laten overschilderen (image-to-image), zodat de vorm en
de looplijn gelijk bleven, en daarna naar een warme zandbruine tint gekleurd met behoud van licht en donker.

## Gevels

Een huis wordt gestapeld uit drie banden van `gevel.png`: het dak (`STAD.gevel.dak`), dan `hoog - 1` keer de
verdieping (`ver`), dan de begane grond (`bod`). De naden lopen net onder een balkenrij, dus de banden sluiten
naadloos. `x` is de linkerkant van het plaatje, `f` spiegelt. De maat hangt aan Amir: het deurgat is 1,3 Amir
hoog (`amir: 318` bronpixels per Amir), dus net als een kei schaalt de breedte mee met het scherm en liggen de
hoogtes vast in sprite-eenheden.

- Het dak is beloopbaar: een dun platform op `dakLoop` (de onderkant van de kartels), over de muur (`muur`).
  Hoogtes: 1 hoog 487, 2 hoog 816, 3 hoog 1145, 4 hoog 1474 (`stadGevelH`). Een verdieping is 329.
- Een gevel is decor op het vlak van de straat: Amir en de vijanden lopen ervoor langs, er botst niets.
- Contactschaduw aan de voet (`STAD.schaduw`), zodat de muur niet als een liniaal op de straat staat.
- Het deurgat is donker. De rechthoek staat in metadata.json (`deurgat`): daar komen later losse deuren.

## Galerijen

Een houten looprichel langs een gevel, 9-slice uit `galerij.png` (links, het midden zo vaak als nodig, rechts).
`van` en `tot` zijn de index van een gevel, zodat hij altijd precies over die huizen loopt, ook als de breedte
meeschaalt. `h` is de hoogte van het dek (standaard de eerste verdieping, 401). Het dek is een dun platform: van
onderen spring je erdoorheen. De reling staat achteraan, Amir loopt ervoor.

Amir springt 208 hoog. Een verdieping (329) is dus te hoog om zomaar te halen: een route naar boven gaat via de
kraam, de doek, of galerijen die tussen twee verdiepingen hangen (Test 59 heeft er drie boven elkaar langs de toren).

## Kramen

- `riet`: de tafel (72) en het rieten dak (263) dragen allebei. Samen een trap: grond, tafel, dak, galerij.
- `doek`: de tafel draagt; de doek (267) veert. Na een val wip je terug (`terug` x de valsnelheid, vanaf `min`),
  sta je erop en spring je, of druk je springen net voor of vlak na het landen (`raam`), dan schiet je hoog
  (`hoog` x jumpV, ongeveer 900): tot op het dak van een huis van 2 hoog. De doek buigt mee (`stadDoekDip`).
- De kramen zijn wat rustiger gebakken (`kraamZacht`), zodat een vijand ervoor goed te lezen blijft.
- Ze zijn 1,06 Amir hoog: hoger kon niet, dan haal je het dak niet meer vanaf de tafel.

## Voetdecor

Losse stukjes uit `voetdecor.png` (`STAD.voet.stukken`): zandhoop, stenen, bakstenen, scherven, kruik, stro, puin.
Zandhoop, stenen en puin worden naar de kleur van de straat getint. Zet ze tegen de voet van een muur, daar breken
ze de rechte lijn tussen muur en straat.

## De verte

`stadAchter` tekent na de zon (in `sceneAchter`) het paleis en drie rijen huizen, in plaats van bergen en heuvels:

- Het paleis (`paleis.png`) is een heldlaag met bijna geen parallax (0,03), dus hij blijft de hele straat in
  beeld. `paleis` in het level is zijn wereld-x. Er is nevel overheen gebakken.
- De rijen worden gebouwd uit dezelfde `gevel.png`, kleiner en met nevel (`STAD.rijen`), voorgebakken op
  `STAD.bak` van de bronmaat. De hoogtes komen uit `stadReeks` met de `seed` van het level.
- Onder de verste rij loopt de nevelkleur door tot de grond, zodat er nergens lucht onder een huis zichtbaar is.

## Nog niet

- Deuren in de deurgaten, en vijanden die uit een deur komen.
- De Maker: gevels, galerijen, kramen en voetdecor als gereedschap.
- Een subtiele gloed om de personages (in de mockups hielp dat tegen de bruine muren), en een kleine set (`klein/`).
