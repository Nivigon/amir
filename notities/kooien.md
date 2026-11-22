# Dierenkooien en het kistje

Houten kooien in de stad, met of zonder doek, en het kistje (een kleine kooi helemaal onder het doek). Code: de sectie
"dierenkooien" (`DKOOI`, `dkReset`, `dkTeken`, `dkBouw`, `dkPlats`, `dkVloerBij`, `dkLijkVal`, `dkPlaat`, `dkVgTeken`;
het openen: `DKOOI.open`, `dkStap`, `dkOpen`, `dkBeest`, `dkDeurTeken`, `dkLos`, `dkOpenZegel`).
Dezelfde kooi staat ook in de kelderzaal (Test 86): daar is het gewoon een dierenkooi met `open: 'bij'`.
Proefstuk: **Stad 16: The cage market**; sandbox: De stad, **Dierenkooien**. De keuzes en de Grok-posts staan ook in het
projectdocument `claude/kooi_doeken.md`.

Let op de naam: `kooien` bestond al (de kooi in de kelderzaal, `kelderZaal.kooien`, en de kooiman met `KOOI`). Daarom
heten de velden `dierkooien` en `kistjes`, en de code `DKOOI`/`dk...`.

## Velden

- `dierkooien: [{x, maat, doek, dier, f, achter, vg, s, dekking, kleur, open, id, deur}]`
  - `maat`: `hoog` (1,56 x 0,95 Amir, de bovenkant op 0,88 Amir: te hoog voor een sprong, zet er een kistje voor),
    `laag` (0,76 hoog, in een sprong te halen, het beest zit gebukt) of `slang` (1,44 x 0,74).
  - `doek`: `half` (over de linkerkant) of `over` (slordig overgegooid), zonder doek een kale kooi.
  - `dier`: `hyena`, `slang` of `bandiet`. De hyena en de slang lopen heen en weer en ademen licht (in een donker level
    zie je alleen een silhouet bewegen), de bandiet zit gehurkt (`hurk_idle`). Zonder `open` blijft het decor.
  - `open`: `'bij'` (de kooi gaat open als Amir `DKOOI.open.bij` Amir van de rand is) of `'zegel'` (een zegel met
    `kooi: id` opent hem, ook als een vijand erop stapt). Niet elke volle kooi hoeft open: dat is juist iets om op te letten.
  - `id`: de naam voor het zegel. `deur`: `'l'` of `'r'` zet de kant van het deurtje vast (anders de kant van Amir).
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

- **De kooi gaat open** (`dkStap` op echte tijd, in de lus naast de andere freezes; `dkOpen`): het deurtje op de
  kopse kant zwaait in perspectief naar de camera (`dkDeurTeken`, in stroken zoals het luikje van de kooiman, `deur.png`
  uit `tools/kooi_deur.py`), met het luikgeluid van de kooiman, een tikje shake en een korte freeze (`deurFreeze`,
  `DKOOI.open.vries` 0,35 s). Die freeze komt hooguit een keer per `DKOOI.open.rust` (10) s, zodat een level met veel
  kooien niet steeds stilstaat. Na `wacht` stapt het beest in `uit` s naar buiten: gebukt (zo klein dat hij in de kooi
  past), en in het laatste stuk (`groei`) richt hij zich op tot zijn volle maat. De hyena en de slang lopen met hun
  echte frames, de bandiet schuifelt gehurkt en staat dan op (`hurk_in` achterstevoren). Binnen de kooi tekent `dkBouw`
  het stuk binnen de tralies, `dkTeken` het stuk voorbij de rand (geknipt). Dan is hij een echte vijand (`dkLos`: 
  `makeHyena`, `makeSnake('groen')`, `makeBandiet`) op `DKOOI.open.buiten` Amir voorbij de rand, met zijn kop naar Amir.
- **Laden**: `dkDierLaad` laadt de frames van wat eruit kan komen (en het hurkpakket van een bandiet in een kooi).

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

## Sandbox

De stad, **Dierenkooien** (decor) en **Kooien open**: een lage met een hyena, een hoge met een bandiet, een slangenkooi
en een volle die dicht blijft.

## Assets

`design/stad/kooi/`, gebakken door `tools/kooi_bak.py` uit de Grok-segmenten in `bron/` (kale kooi, halve doek,
overgegooid doek, de kooi onder het overgegooide doek) en het blad uit `design/stad/galerij.png`. Het deurtje
(`deur.png`) komt uit `tools/kooi_deur.py`, uit de voorkant van de hoge kooi. Daarna `tools/gen-offline-manifest.py`.

## Nog open

- Een bandiet die naar een kooi loopt en het deurtje opentrekt (vraagt een nieuwe animatie).
- Een schorpioen in een kooi.
- 2 a 3 extra doekvormen in dezelfde vuile stijl, vanuit het halve doek als startbeeld.
- Een doek dat eraf valt (Grok-video, alleen de doeklaag).
- De muurkleur van een decorkooi uit de gevel erachter halen in plaats van met de hand (`kleur`).
