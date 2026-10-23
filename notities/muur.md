# De muur die je met je speer openkrijgt

### De muur die je met je speer openkrijgt

Een rotswand die de weg verspert, met op het steen een houten schijf met een rune. Raakt de
punt van een geworpen speer die schijf, dan blijft die speer er voorgoed in zitten en schuift
het rotsblok in een halve seconde omhoog de berg in. Mis je, dan blijft de speer in de rots
steken en valt hij er na `JAV.muurT` vanzelf uit: dat is de gewone wandspeer, daar is niets
voor aangepast.

Een level zet hem neer met `muur: {x, speer}`. `x` is de rechterrand van de rots, de kant waar
Amir aankomt; `speer` is waar zijn speer steeds terugkomt, en dat telt vanaf de lijn waar de
wand hem tegenhoudt, niet vanaf een vaste plek in de wereld. Dat moet ook wel: de rots hangt aan
Amirs maat, dus op een ander scherm verschuift die lijn mee en kwam een vaste plek achter de
muur te liggen, waar je er niet meer bij kon. Verder staat er geen enkele positie in het level: waar de opening en
de schijf komen rekent `muurSet` uit de plaat zelf uit. Alles wat je kunt afstellen zijn maten
en verhoudingen, en die staan bij elkaar in `MUUR`.

**De rots wordt in zijn geheel getekend.** Niet gesneden, niet gespiegeld, niet uitgerekt: de
hele plaat met zijn volledige silhouet, geschaald tot hij past. Zijn maat hangt aan Amir
(`hoogAmir`, 1,6 keer zijn lengte) en niet aan het scherm, en dat is niet vrijblijvend: de
opening en de schijf worden uit Amir gerekend, dus hangt de rots aan het scherm, dan verspringt
die verhouding met elk venster. Op een breed en laag scherm werd de rots groot terwijl Amir
klein bleef, schoof de opening diep de rots in, en was de rune vanaf geen enkele plek meer te
raken. Aan Amir gekoppeld ligt alles op elk scherm hetzelfde. `hoog` en `breed` zijn alleen nog
een vangnet voor het geval hij niet past.

Rotsformaties krijgen voortaan deze maat: 3,5 keer Amir hoog, even groot als deze rots in
Test 3. Zo staat ook de scheve spits met de rune bij het openscheurende ravijn in Test 6
(`RAVIJN_ROTS`).

Omklappen kan met `spiegel`, maar staat uit, en dat is gemeten. Gespiegeld wijst de hoge flank
met de overhang naar Amir en komt de opening onder dat hoge steen te liggen. De schijf hangt
altijd net onder de bovenrand van de rots, dus daar hangt hij hoog, en een hoge schijf betekent
een lange worp: op 1280 bij 720 moet je dan van 480 pixels gooien en staat er nog maar een
strook rots in beeld, en op 1440 bij 620 is er helemaal geen plek meer waar je hem kunt raken.

**De plek van de opening komt uit de alfawaarden.** Per kolom wordt geteld hoe hoog het steen
vanaf de grond draagt (`massief`). Kleine gaten onderweg tellen daarbij niet als het einde: aan
de voet staan de keien los van elkaar met lucht ertussen, en een telling die daar stopt geeft
nul op kolommen waar in het beeld gewoon een muur van steen staat. Dat was precies waarom de
opening met de kale plaat ineens driehonderd pixels dieper ging liggen. Vanaf dat profiel en daarna wordt van de kant waar Amir
vandaan komt de eerste plek gezocht waar de opening past, met daar de hoogste deur die er nog
in kan. Zo dicht mogelijk bij zijn kant dus, en dat is niet alleen netjes: hoe dieper de
opening ligt, hoe verder je moet gaan staan om de rune te raken, en hoe minder er dan van de
rots in beeld past. Twee eisen tegelijk:

- over de volle breedte van de opening moet er genoeg steen staan (de deur plus de schijf
  erboven plus een randje);
- waar de schijf komt te hangen moet de bovenrand van de rots juist laag genoeg blijven, onder
  de top van de werpboog. Het spel rekent die top uit de worpconstanten uit. Ligt de rand
  hoger, dan kan de speer er per definitie nooit overheen en is de rune onraakbaar.

Past de opening nergens, dan krimpt hij tot hij wel past, tot Amirs eigen lengte. Dat is met
opzet: een deur die vasthoudt aan zijn maat belandt aan de rand van de rots, half in de lucht,
en dat is precies wat er niet mag.

**De schijf hangt aan de bovenrand, niet op een vaste hoogte.** In zijaanzicht is de rots een
massief silhouet: een punt onder de bovenrand zit in het steen, en daar komt geen speer ooit,
hoe je ook gooit. De schijf hangt dus net onder die rand (`onder`, 1 betekent dat haar
bovenkant hem raakt), zodat het hout helemaal op de rots ligt en de punt er toch bij kan door
er overheen te scheren. Daarom is het raakvlak (`raak`) ruimer dan het hout: de ruimte waar de
speer kan komen ligt boven de schijf. Dat raakvlak staat los van de straal, en met opzet: `r`
is hoe groot het hout eruitziet, `raak` is hoe nauw het luistert, allebei als deel van Amirs
lengte. Zo maakt een kleinere schijf het spel niet meteen ook moeilijker. De punt blijft steken waar hij binnenkwam, geklemd op de
rand van het hout, dus hij springt niet naar het midden.

**Gat en blok komen uit dezelfde pixels.** Uit de plaat op maat komen drie canvassen: de muur
met de vorm van de opening eruit gegumd (`destination-out`), het schuifblok dat precies dat
uitgegumde stuk is met een marge eromheen, en een masker dat die vorm doorsnijdt met de rots
zelf. Het masker is een pixel ruimer dan het gat, anders blijft er door de anti-aliasing een
haarlijntje op de rand staan.

Die snede met de rots gaat met de hand en niet met `destination-in`. Die rekent alfa maal alfa,
en waar de omtrek van de rots zelf door het gat loopt (langs de voet, bij de steentjes) werd het
blok daardoor doorzichtiger dan het steen eromheen. En zolang het blok stilstaat wordt de
ongeschonden plaat getekend en verder niets: de drie canvassen weer samenstellen levert op de
zachte randen 8-bits afrondingen op, en dat is precies het haarlijntje dat er niet mag zijn.

**De speer botst op de alfawaarde**, met de punt, en dat gaat vanzelf goed omdat `jav.x` en
`jav.h` in dit spel de punt zelf zijn. Lukt het uitlezen niet, dan telt de hele plaat als rots.

**Amir loopt door de rots heen.** De hele rots is decor, ook de deur: uitspelen gaat met E als
de deur open staat en hij ervoor staat (`muurUitgang`). Er is dus niets dat hem tegenhoudt, en
een level dat bij de rots eindigt zonder klif erachter laat hem voorbij de rots eindeloos de lege
savanne in lopen. Zet er een klif een stuk achter.

**Controleer na elke wijziging of de rune nog te raken is.** Dat is geen gevoelskwestie: simuleer
de boog vanaf elke plek waar Amir kan staan en kijk of er een aaneengesloten strook overblijft.
Op een scherm van 1280 bij 720 en Formaat 25 is die strook 141 pixels breed, van 94 tot 235
pixels voor de muurlijn, en vanaf de hele strook staat de rots in zijn geheel in beeld.

Het gras aan de voet staat niet in de plaat maar wordt er los voor gezet (`MUUR.gras`), met
dezelfde tekencode als al het andere gras, dus het buigt mee met de windvlagen. Ingebakken gras
schaalt mee met de rots, en dan staan er sprieten van een meter hoog zodra hij groter wordt. Dichterbij gaat de speer onder de rune door tegen het steen, verder weg zakt hij er al
voor. Er is nog een tweede strook op ruim tweeduizend pixels, maar daar staat de rots buiten
beeld, dus die telt niet mee.

**De grot met de kei** is een tweede soort muur: `muur: {x, speer, soort: 'grot'}` (nu alleen Test
3). Instellingen in `MUUR_GROT`, de canvassen in `muurGrotSet`, tekenen in `drawMuurGrot`. De rots is
de geschilderde boog `design/rotswand_boog.jpg`, met het wit eruit via `witKnip` (dezelfde functie
als de rots bij het ravijn); het donker in de grot is een vulling vanuit de voet van de boog, dus het
volgt de geschilderde rand. Voor de ingang staat `PROPS.boulder`, zo groot dat hij de grot dekt. Bij
een treffer trilt hij, zakt hij de grond in en blijft zijn bovenkant als drempel liggen (`kei.blijf`),
met stof (`puffPic()`) en gruis dat van de boog valt, allemaal op `muurKlok`. Zet hier geen gegumde
opening in: een getekend gat in een geschilderde rots blijft computertekenwerk, en daar is dit de
vervanger van. `muurSet` geeft voor de grot dezelfde velden terug (`l`, `r`, `t`, `b`, `symX`, `symY`,
`alfa`), dus de E voor de deur, de speer in de schijf en `muur.speer` werken gewoon door.

De schijf staat op `sym.hoog` 2,0 Amir, op de linkerpoot (`sym.u`). Dat is gemeten, niet gekozen: met
de huidige boogworp raak je hem op een scherm van 1280 bij 720 van 465 tot 770 pixels, waarvan 465 tot
620 met de schijf in beeld (de camera staat op Amir, dus je ziet 640 naar links). Op 2,28, de hoogte van
de kale rots, begint de strook pas op 590 en valt er bijna niets meer in beeld. Op 1440 bij 620 is het
400 tot 660, op 1920 bij 1080 690 tot 1155, op een telefoon van 844 bij 390 250 tot 420. Hoe lager de
schijf, hoe dichterbij: de boog stijgt nog als hij bij de schijf is.

Een speer blijft bij de grot pas in het steen steken als hij er van buitenaf in vliegt (`jav.buiten` in
`muurSteen`). Amir staat hier vaak voor de rots, onder de boog of voor de kei, en dan vertrekt de speer
al in het steen: met de gewone regel bleef hij er na een paar pixels in steken en was de schijf van
dichtbij niet te halen. Zolang de kei staat vangt die ook een speer (`keiAlfa`).

Let op: de getallen hierboven voor de kale rots (94 tot 235 pixels) kloppen niet meer met de huidige
worp. Met dezelfde meting raak je de schijf in de oude Diepte 3 (dezelfde kale rots als in Rune 10) van 590 tot 1005 pixels.

Het geluid zit in `SFX_DEUR` (`sounds/deuropen.mp3`) en speelt af op het moment van de treffer.
De opname duurt 42 seconden en staat van begin tot eind even hard, terwijl het blok maar een
halve seconde schuift, dus er wordt alleen de kop van gebruikt: vol tot `duur`, dan wegzakken in
`uit`, samen zo'n drie seconden. Dezelfde aanpak als bij het windgeluid. `duur: 0` speelt hem
wel helemaal uit.

Een ravijn dat openscheurt gebruikt dezelfde opname als aardbeving (`playBeving`, `SFX_BEVING`), maar
vanaf het eerste trillen (`onTremorStart`) in plaats van op de klap: hij zwelt aan van `begin` tot vol
op de klap, houdt aan tot het gat open is en de stenen liggen, en zakt dan weg in `uit`. De tijden
komen van het effect (`fx.tCrack`, `fx.tOpen`), dus een breder ravijn rommelt langer. Voor een gewoon
ravijn is dat van 0 tot 5,3 seconden; eerst was het van 1,6 tot 4,1.

**Geluid op een telefoon.** Een telefoon laat geluid alleen starten vlak na een tik, en er is maar
een versterker voor het hele spel. Alles staat bij elkaar boven `SFX_DEUR`, en het komt op drie dingen
neer:

- **Een gedeelde `AudioContext`** (`geluidAc`, `acWek`, `acLoopt`). Wat harder moet dan volume 1 (de
  brul van de baviaan, het instortende skelet, de aardbeving, de storm) loopt door een gain van de Web
  Audio API. Dat deed elk geluid eerst met een eigen context: vier stuks. Een telefoon staat er maar
  een paar toe, en een context die stilstaat neemt al zijn geluiden mee, dus nu is er een. Een nieuwe
  versterker maakt dus geen `new AudioContext()` meer maar vraagt `acLoopt()`.
- **`interrupted` is niet `suspended`.** Een context begint stil (`suspended`) en mag alleen tijdens
  een tik op gang komen, maar na een telefoontje, het wegleggen van het toestel of het wisselen van
  app staat hij op `interrupted`. Wie alleen op `suspended` kijkt, laat hem daarna voorgoed stilstaan:
  de brul, het skelet, de aardbeving en de storm bleven de rest van het potje weg terwijl de gewone
  geluiden wel klonken. `acWek` hervat alles wat niet `running` is, bij elke tik en als het scherm
  terugkomt (`visibilitychange`).
- **Elk audio-element krijgt een stil begin** (`geluidOntgrendel`). Dat geldt per element: eentje dat
  nog nooit tijdens een tik gespeeld heeft, blijft stil als het spel het later zelf wil spelen. De
  lijst wordt niet met de hand bijgehouden, want dan mist er altijd een: de `<audio>`'s uit de HTML
  worden opgehaald, en elk element dat het script maakt meldt zich aan met `geluidAan(new Audio())`,
  op de regel waar het gemaakt wordt. Doe dat dus ook bij een nieuw geluid. De muziek (`bg`) blijft
  erbuiten, die start `tryPlay`. Dat stille startje zet `a.muted` aan voor het afspelen, en dat werkt
  alleen voor een element dat rechtstreeks speelt. Een element dat via `createMediaElementSource` aan
  de versterker hangt gaat niet meer door het element maar door de context, dus `a.muted` doet daar
  niets: het stille startje zou dan het geluid zelf zijn. Op een telefoon loopt de context al tijdens
  de tik, dus die elementen zijn op dat moment al aangesloten, en zo klonken aan het begin de deur, het
  skelet, de storm en alle geluiden van de baviaan en het goudaapje door elkaar. Die elementen staan nu
  in `geluidViaAc` (ze melden zich aan met `viaAc(a)` op de regel van de `createMediaElementSource`), en
  `geluidOntgrendel` slaat ze over: ze hebben het stille startje ook niet nodig, want de tik ontgrendelt
  de context waar ze aan hangen al. Een nieuw geluid dat je aan de versterker hangt, wikkel je dus in
  `viaAc(...)`.

Een element dat eenmaal via `createMediaElementSource` aan de context hangt, gaat voorgoed door die
context: staat hij dan stil, dan hoor je niets meer, ook niet door `volume` te zetten. Daarom wordt een
element er pas aan gehangen als de context echt loopt (`acLoopt`); tot die tijd speelt het rechtstreeks,
hoogstens op volume 1, dus zachter dan bedoeld maar te horen.

Headless Chromium past de autoplay-regel niet vanzelf toe. Met `--autoplay-policy=document-user-activation-required`
komt het in de buurt, en daarmee is na te kijken dat na een enkele tik elk geluid speelt en dat de
context na een onderbreking weer aangaat; het echte gedrag van Safari op een iPhone is dat niet, dus
controleer het daarnaast op een echte telefoon.

## muur unlock: de rotswand met het rune-symbool

`MUUR`: de plaat, het gat, het schuifblok, het masker en de schijf; en de grot met de kei (`MUUR_GROT`, `muurGrotSet`, `drawMuurGrot`)
