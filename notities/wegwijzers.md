# Wegwijzers (korte onderwerpen)

De korte cellen uit "Waar wat staat" die geen eigen notitie hebben.

## versie: welke update er live staat

`versieTijd` (uit `document.lastModified`) heel klein linksboven, en `toonUpdates`: de laatste vijf samengevoegde pull requests van GitHub (`VERSIE_REPO`), met of ze erin zitten (regel 8)

## globale lichtlaag

kleurwaas over het beeld, volgt de zon van het level; een level stelt hem bij met `licht` in `SCENES`

## muziek per level

`MUZIEK`, `MUZIEK_BASIS` (Dark Africa: bij de start, in het menu, de sandbox en elk level zonder veld `muziek`), `zetMuziek()`: welk deuntje onder welk level loopt

## beeld: de grote of de kleine spriteset

`KLEIN_FAM`, de keuze groot of klein, `zetBron`

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

## het weer: regen, onweer, zandstorm, sneeuw en sneeuwstorm

`WEER`, `weerDoel`, `updateWeer`, `drawWeer`, `weerWind`, `weerGeluid`: het veld `weer` van een level (zie "het weer" hieronder)

## vegetatie, water, doornbos

`props`, `water`, `thickets`

## achtergrondlagen, uitzicht per level

`SCENE0` en `SCENES`
