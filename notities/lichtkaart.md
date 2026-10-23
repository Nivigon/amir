# De lichtkaart

### De lichtkaart: een lichtbron voor alles onder de grond

Er is een lichtbron onder de grond: de hemel, met de zon als vaste richting. Voor elke cel van
`LK.cel` bij `LK.cel` rekent `lkKolom` uit hoeveel hemel hij ziet (stralen omhoog die grond en
rots tegenhouden, `lkZicht`) en of de zon hem raakt (`lkZon`, een smalle kegel, dus een zachte
schaduwrand). De zon staat aan de kant waar hij in de lucht van het level staat (`zonRechts`),
`LK.zonHoek` graden van recht boven. Daaruit volgt vanzelf wat je wilt zien: een gat is licht,
de rand werpt een schuine schaduw van de zon af, en hoe verder de gang van een gat af loopt,
hoe donkerder, zonder rechte streep. Vaste grond is een doorsnede: die krijgt het licht van de
oppervlakte erboven en wordt dieper eronder donkerder (`LK.diepte`, `LK.bodem`). Lucht die zelf
weinig hemel ziet, krijgt kaatslicht van wat eromheen ligt (`LK.kaatsR` cellen in het rond), en
dat is warm waar de zon in de buurt iets raakt.

Dit vervangt alle losse lagen die er eerst waren: de getekende lichtbundel door een gat, de
schaduw tegen de eindwanden, het verloop in het grondpakket, `holteFilter` en `holteHelder`
voor decor en treden, en een vervaagde donkerlaag over de rots. Die gaven elk hun eigen licht
en dus rechte randen. Teken er dus geen nieuwe bij: een nieuw soort terrein hoeft alleen in
`lkVastPunt` te zeggen wat vast is.

Twee regels die ertoe doen:

- **De zonnegloed van de lichtlaag schijnt niet door de rots.** `drawLichtlaag` telt de gloed rond
  de zon op in schermruimte; onder de grond (`holteDiepT`) gaat die uit. Deed hij dat niet, dan lag
  er in de gang zo'n 40 punten helderheid bovenop, en daar was het steen vlak en oranje van.
- **Vaste grond wordt pas donker als de camera zakt.** Het plaatje met de grond (`lk.grond`)
  krijgt `holteDiepT` als dekking: van bovenaf ziet de savanne eruit zoals altijd. Wat lucht is,
  een gat of een gang, is altijd zo licht als het is.
- **Een ravijn zonder gang eronder laat de kaart met rust.** Zo'n gat tekent zijn eigen diepte en
  schaduw (zie hieronder); in `lkRuw` krijgt het geen licht of donker uit de kaart. Zonder die
  regel kreeg een dodelijk ravijn vlak bij een gang ineens zon en kaatslicht.
- **De zon valt pas onder het dak binnen**, en loopt daar over `LK.zonInloop` eenheden in. De wand
  van een gat erboven is de overkant, en die hoort niet lichter te zijn dan de grond vooraan.
- **Een open ravijn telt mee.** `lkSleutel` kijkt ook naar `ravijnGaten()`: scheurt er in een level
  met een gang een ravijn open, dan rekent de kaart opnieuw.

**De zon volgt het uitzicht** (`lkZonKleur`), net als de zon op de wand van een ravijn. De sterkte
schaalt met `gloedSterkte` (0,30 overdag), met `LK.zonNacht` als ondergrens, en in de winter is de
kleur koel wit (`LK.zonWinter`) in plaats van warm (`LK.zonKleur`). Anders viel er in de sneeuw oranje
licht op grijze steen, en was de zon 's nachts beneden even fel als overdag. Kleur en sterkte zitten in
`lkSleutel`.

**Rots boven je, ook buiten.** Een plafondlijn en de volle cellen van een rotsraster zijn voor de
kaart rots (`lkRotsPunt`), ook boven de grond, en een level met alleen een plafond of grotten krijgt
ook een kaart. Die reikt dan tot `LK.buitenTop` omhoog en rekent buiten alleen binnen `LK.buitenBuur`
van die rots (`lk.buur`); verder weg blijft het gewoon dag. Een punt buiten telt hoeveel hemel het
onder de rots nog ziet, en of de zon het raakt (`lkZicht` en `lkZon` met `rots`: alleen de rots houdt
dan de straal tegen, niet de grond en de terrassen). Het lichtste van die twee telt. De zon komt schuin
van zijn kant, dus onder een overhang ligt een schuine schaduwrand, en aan de open kant valt hij naar
binnen. Buiten weegt het donker minder zwaar (`LK.buiten`), want de lucht eromheen is open, en er komt
geen zonnevlek bij: het is al dag. Een terras of een kei onder de rots is voor de kaart lucht, zodat
de schaduw er ook overheen ligt. De rots zelf wordt boven de grond niet donkerder gemaakt.

Wat het kost, gemeten in Test 1: de hele kaart 0,3 seconde, in stukjes van `LK.budget`; het eerste
beeld van een level onder de rots eenmalig zo'n 50 ms.

## lichtkaart: het licht onder de grond

`LK`, `drawLichtkaart`: een lichtbron (de hemel en de zon) voor alles onder de grond en onder rots boven je, per level een keer uitgerekend
