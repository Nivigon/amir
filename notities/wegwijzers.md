# Wegwijzers (korte onderwerpen)

De korte cellen uit "Waar wat staat" die geen eigen notitie hebben.

## versie: welke update er live staat

`versieTijd` (uit `document.lastModified`) heel klein linksboven, en `toonUpdates`: de laatste vijf samengevoegde pull requests van GitHub (`VERSIE_REPO`), met of ze erin zitten (regel 8)

## globale lichtlaag

kleurwaas over het beeld, volgt de zon van het level; een level stelt hem bij met `licht` in `SCENES`

## muziek per level

`MUZIEK`, `MUZIEK_BASIS` (Dark Africa: bij de start, in het menu, de sandbox en elk level zonder veld `muziek`), `zetMuziek()`: welk deuntje onder welk level loopt. Een level met `stad` en zonder eigen `muziek` krijgt de stadmuziek Market Shadows (`MUZIEK_STAD`, de sleutel `markt`, `music/marketshadows.mp3`); in de sandbox de knop **Stad** onder Muziek, in de Maker **Market Shadows (stad)**. Het eerdere stadnummer Tense Grounding staat nog onder de sleutel `stad` (`music/tensegrounding.mp3`): in de sandbox en de Maker **Tense Grounding**. De oude stadgeluiden zonder muziek staan onder de sleutel `stadgeluid` (`music/citysounds.mp3`): in de sandbox **Stadgeluid**, in de Maker **Stadgeluiden**

## beeld: de grote of de kleine spriteset

`KLEIN_FAM`, de keuze groot of klein, `zetBron`

`bronW` en `bronH`: de maat van een plaatje in pixels van de grote set. `zetBron` zet `_bron` op hoeveel keer
kleiner de geladen versie uit `klein/` is: 2 voor de helft (de standaard), of de factor uit `KLEIN_BRON` voor
een familie die verder verkleind is (het goudaapje: 4, een kwart; op de helft was hij op een telefoon nog
2,45x te groot, op een kwart zit hij op 1,2x op zijn krapst). `KLEIN_BRON` hoort gelijk te lopen met de
factoren in `DOELEN` in `tools/gen-klein.py`; dat script print de lijst. Tekencode die in bronpixels rekent
(de baviaan en het goudaapje: hun kader, `links`, `grond` en de schaal per bronpixel) leest de maat hiermee
in plaats van met `naturalWidth`, anders komt een half frame op de halve maat. Bij een nieuwe familie in
`KLEIN_FAM`: kijk of de tekencode met `naturalWidth` of `naturalHeight` rekent, en zo ja, laad via `zetBron`
en lees via `bronW`/`bronH`.

## rotsen om op te springen

`rocks`, en het automatisch bijgroeien

## winter: episode Winter World

`WINTER_SRC`, `winterOn()`, `winterPic()`

## bodem en sneeuwdek

het veld `sneeuw`: savanne of rots, en het dek in vier standen

## Feign Death

`SCHIJN`, `schijnDoodVang` (vanuit `hurtPlayer`, `valLand` en `fosforBijt`), `schijnDoodZet` (kantelt zijn frame), `schijnHud` (`#schijn`); per level terug in `restart`

## de rotswand rechts

`cliffs`, het einde van het level

## licht op de runerotsen

`RUNE_LICHT`, `runeLichtMaak`, `runeGrondSchaduw`: de zon op een rots met een rune, uit dezelfde richting als de lichtkaart (`LK.zonHoek`, `zonRechts`); zie "runes op elke rots"

## runeschijf: het losse symbool

`runeSchijf(ctx, x, y, r, {aan, spiegel})`: de houten schijf met de rune, los te hergebruiken

## personages, dorpsdecor

NPC's, `VILLAGE`, de dorpsplaten

## stap voor stap leren spelen

het `tutorial`-systeem (staat klaar, geen level gebruikt het nu)

## gaten in de grond

`gaps`, de overkant, de nevel en de diepte; de laag die eronder doorloopt is `grondDoorlopen`, in de bodemsectie

## het weer: regen, onweer, zandstorm, sneeuw, sneeuwstorm en mist

`WEER`, `weerDoel`, `updateWeer`, `drawWeer`, `weerWind`, `weerGeluid`: het veld `weer` van een level (zie "het weer" hieronder)

De grondmist (`mist` en `mistdik`, `WEER.mist`, `mistTegel`, `mistTeken`): twee lagen zachte vlekken laag over de grond,
voor Amir langs (getekend in `drawWeer`, na de lichtlaag), met een eigen parallax en een trage drift. Hij volgt de echte grond
per strook (`weerOppervlakY`, stroken op dezelfde hoogte samen, anders streepjes), en boven een ravijn ligt er niets. `sterkte`
maakt hem hoger en dichter: `mist` op 1 rond de enkels, `mistdik` (1,7) tot over de knieen. Hij komt trager op en trekt
trager weg dan het andere weer (`WEER.mist.tempo`), dus een punt in `weer` laat de mist echt opkomen. In de sandbox **Mist** en
**Dikke mist** onder Weer. Open: de kleur is vast (warm wit), 's nachts zou hij mee moeten donkeren met het licht.

## vegetatie, water, doornbos

`props`, `water`, `thickets`

## achtergrondlagen, uitzicht per level

`SCENE0` en `SCENES`

Een andere biome (`BIOMES`, `biomeImgs`, `layerImgs`): eigen panelen voor de verre laag, de tweede rij en de middenlaag,
met dezelfde tekenweg (`drawLayer`, `vertePlaten`). Een uitzicht kiest er een met `biome`; de panelen laden pas als zo'n uitzicht
voor het eerst getekend wordt. Nu alleen `regenwoud` (uitzicht `regenwoud`, de warme ochtend, panelen uit `design/regenwoud/`,
een per laag), in de sandbox onder Tijd van de dag, **Regenwoud**. De grond blijft nog de savanne.

## wolken in de lucht

`STAD_LUCHT`, `luchtWolken`, `luchtWolkenAan`, `luchtWolkKleur`: wolken uit Grok (magenta of groen uitgeknipt) in drie lagen
diepte (`lagen`: ver, midden, dichtbij). Ver is klein, laag tegen de horizon en deels achter de bergen (ze worden voor de
bergplaten getekend), doffer (`waas`: ze lopen op in de kleur van de horizon, `sky[2]`) en bijna stil; dichtbij is groot, hoog
en schuift het meest mee. Elke laag drijft ook als je stilstaat (`drijf`, pixels per seconde). Per uitzicht ingekleurd: de
schaduwkant naar de nevel en de lucht, de lichte kant naar de kleur van de zon (`sc.wolkTint` stelt het bij).
- Buiten de stad: de avondset `design/stad/verte/avondwolk_1..9.png` (lange strepen, oranje verlichte buik, donkere toppen,
  want de zon staat laag). Standaard aan in elk level, niet in de winter; `wolken: false` in een level zet ze uit.
- In de stad alleen met `stad.lucht.wolken` (Ishmul): de middagset `wolk_1..8.png`, gefacetteerd zoals de rotsen.
