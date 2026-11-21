# Dierenkooien en het kistje

Houten kooien in de stad, met of zonder doek, en het kistje (een kleine kooi helemaal onder het doek). Code: de sectie
"dierenkooien" (`DKOOI`, `dkReset`, `dkTeken`, `dkBouw`, `dkPlats`, `dkVloerBij`, `dkLijkVal`, `dkPlaat`, `dkVgTeken`).
Proefstuk: **Stad 16: The cage market**; sandbox: De stad, **Dierenkooien**. De keuzes en de Grok-posts staan ook in het
projectdocument `claude/kooi_doeken.md`.

Let op de naam: `kooien` bestond al (de kooi in de kelderzaal, `kelderZaal.kooien`, en de kooiman met `KOOI`). Daarom
heten de velden `dierkooien` en `kistjes`, en de code `DKOOI`/`dk...`.

## Velden

- `dierkooien: [{x, maat, doek, dier, f, achter, vg, s, dekking, kleur}]`
  - `maat`: `hoog` (1,56 x 0,95 Amir, de bovenkant op 0,88 Amir: te hoog voor een sprong, zet er een kistje voor),
    `laag` (0,76 hoog, in een sprong te halen, het beest zit gebukt) of `slang` (1,44 x 0,74).
  - `doek`: `half` (over de linkerkant) of `over` (slordig overgegooid), zonder doek een kale kooi.
  - `dier`: `hyena` of `slang`, een stilstaand plaatje dat licht ademt. Het is decor: er komt (nog) niets uit.
  - `f` spiegelt (het halve doek komt rechts).
  - `achter: true`: decor op de stoep tegen de muur, 0,55 van de maat, minder contrast en 30% waas naar `kleur`
    (standaard leemkleur 176,146,112). Nooit grijzer of waziger dan de muur erachter, anders leest hij als achter de
    muur. Geef bij een oranje huis een warmere `kleur` mee.
  - `vg: true`: groot (1,8), donker (0,3, warme tint) en onscherp voor de camera, na de voorgrond, met parallax 1,3.
  - `dekking`: het donker over het beest (standaard 0,3 zonder doek, 0,62 met doek).
- `kistjes: [{x, f, achter, vg, s}]`: 0,7 Amir breed, de bovenkant op 0,39 Amir; je staat op de middelste helft
  (het doek is bol), de voeten 0,04 Amir in de stof. Het is de opstap naar een hoge kooi, maar ook gewoon sfeer en een
  manier om ergens makkelijker op of af te komen (een galerij, een kraam).

Spawn op een kooi: `{x, k: 'bandiet', dak: 'kooi'}` (`stadDakPlek` kiest dan alleen een kooi).

## Hoe het werkt

- **Loopvlak:** `dkPlats` geeft de bovenkant als dunne vloer aan `platsNear` (`stad: 'kooi'`): eronder langs lopen,
  van boven erop landen, met `doorval` erdoorheen zakken (`DOORVAL.soorten.kooi`). Een vijand krijgt dezelfde bovenkant
  via `dkVloerBij` in `vloerBij`, voor de daken en galerijen.
- **Een lijk valt eraf:** `dkLijkVal` zit vooraan in `opstapVolg` (dat bijna elke vijand elk beeld doet). Is hij dood
  op een kooi, dan schuift hij naar de dichtste rand (`DKOOI.lijk.schuif`, Amir/s) en valt hij met de zwaartekracht
  (`DKOOI.lijk.g`) naar de vloer eronder (`vloerBij` met `dkZonder`).
- **Tekenen** (`dkBouw`): donkere vloer, achtertralies (een halve tralie verschoven, donkerder), het beest, de dekking,
  de voorkant met het blad uit de galerij, en het doek. De doeken liggen op een vaste plek als deel van de kooi
  (`DKOOI.doeken`, gemeten op de Grok-platen). Een kooi op de looplijn krijgt de schuine slagschaduw van de stad
  (`STAD_SLAG.ton`) en een contactstreep. Stoep en voorgrond worden een keer per maat en schaal in een eigen canvas
  gebakken (`dkPlaat`, `dkCache`).
- **Lui laden:** `dkLaadLevel` in `laadLevel`, `dkReset` naast `tonReset`.

## Assets

`design/stad/kooi/`, gebakken door `tools/kooi_bak.py` uit de Grok-segmenten in `bron/` (kale kooi, halve doek,
overgegooid doek, de kooi onder het overgegooide doek) en het blad uit `design/stad/galerij.png`. Daarna
`tools/gen-offline-manifest.py`.

## Nog open

- De deur die opengaat en het beest dat eruit komt (en zich dan opricht tot zijn volle maat).
- 2 a 3 extra doekvormen in dezelfde vuile stijl, vanuit het halve doek als startbeeld.
- Een doek dat eraf valt (Grok-video, alleen de doeklaag).
- De muurkleur van een decorkooi uit de gevel erachter halen in plaats van met de hand (`kleur`).
