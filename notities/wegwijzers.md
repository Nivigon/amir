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
**Dikke mist** onder Weer. Waar de grond een stap maakt (terras, ravijn) loopt de mist over `WEER.mist.veer` px zacht uit. Open: de kleur is vast (warm wit), 's nachts zou hij mee moeten donkeren met het licht.

## vegetatie, water, doornbos

`props`, `water`, `thickets`

## achtergrondlagen, uitzicht per level

`SCENE0` en `SCENES`

Een andere biome (`BIOMES`, `biomeImgs`, `layerImgs`): eigen panelen voor de verre laag, de tweede rij en de middenlaag,
met dezelfde tekenweg (`drawLayer`, `vertePlaten`). Een uitzicht kiest er een met `biome`; de panelen laden pas als zo'n uitzicht
voor het eerst getekend wordt. Nu alleen `regenwoud` (uitzicht `regenwoud`, de warme ochtend, panelen uit `design/regenwoud/`,
een per laag), in de sandbox onder Tijd van de dag, **Regenwoud**. In een biome tekent `drawProps` het automatische savannedecor niet (keien, acacia's, hutjes). Proefstuk: Test 81.

## wolken in de lucht

`STAD_LUCHT`, `luchtWolken`, `luchtWolkenAan`, `luchtWolkKleur`: wolken uit Grok (magenta of groen uitgeknipt) in drie lagen
diepte (`lagen`: ver, midden, dichtbij). Ver is klein, laag tegen de horizon en deels achter de bergen (ze worden voor de
bergplaten getekend), doffer (`waas`: ze lopen op in de kleur van de horizon, `sky[2]`) en bijna stil; dichtbij is groot, hoog
en schuift het meest mee. Elke laag drijft ook als je stilstaat (`drijf`, pixels per seconde). Per uitzicht ingekleurd: de
schaduwkant naar de nevel en de lucht, de lichte kant naar de kleur van de zon (`sc.wolkTint` stelt het bij).
- Buiten de stad: de avondset `design/stad/verte/avondwolk_1..9.png` (lange strepen, oranje verlichte buik, donkere toppen,
  want de zon staat laag). Standaard aan in elk level, niet in de winter; `wolken: false` in een level zet ze uit.
- In de stad alleen met `stad.lucht.wolken` (Ishmul): de middagset `wolk_1..8.png`, gefacetteerd zoals de rotsen.

## De hangende stam (HSTAM) en het stof in het regenwoud

Een bemoste boomstam aan twee lianen (`hangstammen: [{x, h, breed}]`), proefstuk Test 82 in de reeks Test levels
rainforest (`RW_LEVELS`, met Test 81; de knop Rainforest in het Test Lab, zonder tribekeuze). Het plaatje komt uit
Grok (`design/regenwoud/hangstam/bron/hangstam_grok2.png`, de scherpere download van 1600x1200 die al doorzichtig is;
de eerste plaat `hangstam_grok.png` staat er nog naast); `tools/hangstam_knip.py` houdt dan de eigen alpha, haalt het witte randje weg en knipt er `stam.png` (de stam met
de knopen) en `liaan.png` (een rechtgetrokken stuk liaan dat naadloos onder elkaar past) uit. Een nieuwe plaat vraagt nieuwe maten in
`HSTAM.bron`, `haak`, `haakRij` en `liaan`. Het spel stapelt de
liaan van de knoop tot een anker `HSTAM.anker` boven de stam, dus ruim buiten beeld.

- **Hangen** (`st: 'hangt'`): een dun platform (`hstamPlats`, met `takel: true` zodat Amir eraan bindt via
  `amirPlat`). Hij slingert uit zichzelf (`swayA`, `swayF`), een landing zakt hem in (`zak`) en zwaait hem mee
  (`landDuw`), met een gesynthetiseerd kraken (`hstamKraak`). Amir schuift mee met de slinger en veert mee op en neer
  (in `hstamUpdate`; anders zakt hij erdoor als de stam terugveert).
- **Raken**: de steek (de hele schacht van Amir tot de punt, ook met de stokken) of een geworpen speer door het raakvak
  van een liaan (`hstamVakken`: van onder de knoop tot `raakBoven` erboven). Ook de lage zwaai (`swbox`) snijdt hem, een liaan per zwaai
  (`st.sweptId`), zodat een zwaai midden op de stam hem niet meteen plat laat vallen; vanaf de stam haal je de knoop,
  vanaf de grond niet bij een stam op de standaardhoogte (190). De speer vliegt door, net als bij het
  touw van de takel. `hstamKnap` speelt de houten tik en de knap (`takelSnap`) en strooit splinters. De liaan breekt op de hoogte waar hij geraakt werd (`hRaak`: de punt van de steek of het midden van de speer, geklemd tussen de knoop en `raakBoven`): het stuk erboven veert op aan de tak (`rest`), het stuk eronder blijft aan de stam en flapt slap omlaag naar buiten (`stomp`). Vanzelf geknapt breekt hij net boven de knoop. De looplijn ligt in het mos (`bron.top` 56), zodat Amirs voeten in het mos staan en niet op de toppen.
- **Half** (`st: 'half'`): de stam draait om het haakpunt van de liaan die nog vastzit tot de losse punt de grond raakt
  (bonk `ton_zwaar.mp3`, stof, een klein stuitje). Na `HSTAM.tweede` (3) seconden knapt de andere liaan vanzelf.
- **Helling**: schuin (`half`) is de stam een dun platform op de hoogte van het bovenvlak onder Amir (`hstamHelling`,
  `hstamHellingVak`); hstamUpdate zet hem elk beeld op die hoogte, ook terwijl de stam nog kantelt (stond hij erop,
  dan kantelt hij mee). Zijn voeten volgen het midden: bij zo'n 14 graden zweeft een voet een paar px, de andere zakt
  in het mos. Het lage eind ligt een stamdikte (zo'n 90) boven de grond: daar spring je op. Met `tweede: false` in de
  stam knapt de tweede liaan nooit vanzelf en blijft de helling (Test 83); `levelcheck.py` telt een stam vlak voor een
  terras als treetje (90 en `h`).
- **Valt** en **lig**: de punt blijft op de grond, de andere kant valt (`valG2`); plat is hij een laag obstakel (geen dun
  platform), met `kooihitground.mp3` en veel stof over de hele lengte. Het afgeknapte stuk liaan veert op (`rest`).
- Sandbox: Terrein, **Hangende stam** (Neerzetten zet er telkens een bij, Weg haalt ze weg).

Het stof in het regenwoud (`RW_STOF`, `regenwoudStof(wx)`): in een uitzicht met `biome: 'regenwoud'` of op een strook
`regenwoud` (grondSoort) geven `puffPic`, `wispPic`, `dustColor` en `stofWolk` donkere humus met een groene zweem in
plaats van savannezand. Een strook savanne in een regenwoud-uitzicht houdt het zand (Test 81 begint zo).

### Een klap in de mist (MIST_STOOT)

Een zware klap op de grond in de grondmist (`mistStoot(wx, kracht, breed, vx)`) duwt de mist weg: een gat dat snel
opengaat (`uit`, `open`) en in de tweede helft van `leven` weer dichtloopt, met een opgestuwde rand die dikker wordt en
opbolt (`rand`, `randOp`, `randB`) en vervaagt. `mistTeken` tekent de mist dan in smalle vakken (`vak`, `stap`), elk op
de dikte van `mistDekking(wx)`. Zonder mist doet `mistStoot` niets. Wie stoot: de hangende stam (een kant 0,6, plat 1
over de hele lengte), een landing van Amir harder dan een gewone sprong (tot 0,7), en de grondklap (0,85, het gat rolt
met de golf mee naar voren via `vx`). Bij een herstart is de mist weer heel.

## De holle stam (HOLSTAM)

Een omgevallen holle boom in het regenwoud (Test 93, sandbox Terrein, Holle stam). Gemaakt in Grok in Toms Chrome; de
lessen en alle afgekeurde versies staan in de projectnotitie `claude/holle_stam_overdracht.md`.

- **Platen** (`design/regenwoud/holstam/`): `schil.png` (de buitenkant, Grok-post 6af92838, wit weggeknipt, de witte zoom
  eraf) en `binnen.png` (de doorsnede, post 320f8104, al in het silhouet van de schil geschaald en op 55%). De Grok-bron
  staat in `bron/`. Beide 2031x576 en precies op elkaar: dezelfde knippen gelden voor allebei.
- **Lengte**: `holstamBak` knipt de plaat in drie stukken (`bron.L`, `bron.R`): linkerkop, middenstuk (`ceil(n)` hele
  stukken, elk `n / ceil(n)` zo breed: een afgeknipt stuk sloot boven niet aan op de rechterkop), rechterkop, met een overloop van `ov` bronpixels. Per stam een keer gebakken op bronmaat (`q._bak`), plus de
  dichte rand: per kolom alleen het bovenste 16% en onderste 10% van de schil.
- **Grootte**: `HOLSTAM.hoog` (2,25 Amir) maal `s`. Bij s 1 ligt het plafond binnen op 357 en de bovenkant op 373
  (sprite-eenheden), dus bovenop kom je alleen vanaf iets hogers (de sprong haalt ruim 200). Bij s 0,45 is het plafond
  160: alleen gebukt erdoor, net als de kruipstam.
- **Ligging**: de looplijn binnen (`bron.vloer`) valt op de grond, en de plaat wordt vlak eronder (`bron.knip`, 14
  bronpixels) grillig afgeknipt, met een zachte schaduw op de snede: hij ligt op de grondlaag, niet ervoor (Tom: eerst
  lag hij te ver naar voren). Bovenop loop je op `bron.top` 118, in het mos, zodat je voeten nergens zweven.
- **Botsing**: `holstamDak` geeft een onzichtbare zwevende laag (look 'geen', zoals `kruipstamDak`). readLevel zet hem
  erbij, de sandbox zelf (met `holstam: true`, zodat Weg hem weer vindt). Vijanden blijven op de grond (vloerBij kijkt pas
  naar een zwever vanaf 140 onder de bovenkant).
- **Breedte**: in wereld-px, en die schaalt met het beeld (`nowScale`), net als een kei: zo valt de botsing precies op de
  plaat. Het dak (`holstamDak`, met `hq`) werkt `holstamUpdate` elk beeld bij. Met `anker: 'r'` is `x` de rechterkant in
  plaats van het midden, zodat een stam strak tegen iets vast ligt (de lange stam in Test 93 tegen de treden). Een kleine
  stam (plafond onder Amir) heeft het dak en het vervagen pas 0,16 Amir binnen de opening: je loopt tot in de opening en
  bukt daar.
- **Lagen**: `holstamAchter` (na `hstamTeken`) tekent de binnenkant achter de personages, en de schil als Amir bovenop
  staat; `holstamVoor` (na `tonVoorTeken`, dus na alle vijanden) tekent anders de schil: een vijand in de stam zie je niet
  tot Amir erin loopt. Loopt Amir erin (`holstamBinnen`, in de eerste 7% vanaf een opening loopt het op), dan vervaagt de
  voorkant helemaal en blijft de rand boven dicht; de onderrand begint onder de looplijn (`bron.lip` -6), zodat je voeten
  altijd te zien zijn.
- **Vuurvliegjes** (`vlieg: true`): binnen 0,5 donker in plaats van 0,3, en twaalf stipjes (`holstamVliegStap`) die
  zweven en knipperen. Een steek (`holstamUpdate`, op atkFrame), de lage zwaai (`holstamZwaai`, een keer per sweepId) of
  een vijand die sterft (`vijandDood`) roept `holstamSchrik` aan: hooguit vier in de buurt flitsen op, schieten weg met
  een zigzag en sterke demping, blijven binnen de stam en vliegen dan door de dichtstbijzijnde opening naar buiten (omhoog
  of opzij). Na 4 tot 6,5 s komen ze rustig door een opening terug naar hun plek. Geen sporen: losse stipjes.

### Gaten in de schors (`HOLSTAM.gat`)

Een steek of lage zwaai binnen in de stam raakt de binnenwand op de speerpunt (`holstamSlag`). Elke slag spat scherven
(bleke houtsplinters, schorsbrokken, mosplukjes, uit `design/regenwoud/holstam/gat/`, Grok-post 11874e58) en kruimels; af
en toe (`kans` 0,3, hooguit 6) blijft er een klein gat. Met `hol: {dx, inhoud, goud}` op een stam zit er een verstopt hol
in de wand: een haarscheur met af en toe een warme zweem, en vier slagen erop breken hem open (`gat_0` tot `gat_4`,
Grok-post 1cc7330a, elk een stand). Bij de laatste slag schudt het beeld en vliegen er stukken in perspectief langs de
camera (`holstamLens`, zoals de tonnen bij Nyundo, maar ze raken de lens niet). Dan gloeit het hol en E steekt je arm
erin: Amir graaft even (`HOLSTAM.gat.zoek`, geschraap van `stofveeg.mp3`, een tik hout en vijf korte ruisstoten als
droog blad, `holstamZoekGeluid`), en dan valt er een kalebas uit (met `zegelontdek.mp3`), of met `inhoud: 'goud'` goud
(`holstamGatE`, `holstamVondst`). Met `inhoud: 'ruimte'` is het een lege ruimte erachter (dieper donker met ringen van de
nerf, E vindt alleen blad en botten), met `inhoud: 'uitzicht'` breek je dwars door de wand: het gat (een grillige
veelhoek, `holstamUitzichtVorm`) wordt uit de binnenkant geknipt en je ziet de gewone achtergrond op zijn plek, met de
bast eromheen (`holstamUitzichtRand`) en daglicht naar binnen; geen E. Met `inhoud: 'ingang'` zit het gat laag bij de vloer
(`ingangH`) en groter, en E kruipt erin: een fade (`holstamFade`) naar een eigen hol ver links van de klif (`holstamDen`,
`HOLSTAM.gat.hol`), net als binnen een huis een strook met eigen wanden (`holstamDenKlem`), camera (`binnenCamKlem`) en
zonder klif (`endWall`). Daar ligt de vondst (`vondst`: een kalebas, of `'kist'` een schatkist), en E bij de opening rechts
brengt je terug. Een uitzicht zit hoger
(`uitzichtH` 0,82, of eigen `h` in Amir). De laatste slag breekt met `ton_breek.mp3`. `kruis: true` (alleen een testlevel)
zet een rood kruis met de soort en de stand erbij. Sterf je, dan is alles
weer dicht (`holstamReset`). Sandbox Terrein, Holle stam, **Met hol**; Test 93 heeft een hol in de eerste en de lange stam.

