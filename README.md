# Amir: King of Africa

Een browserspel in een enkel bestand: open `amir-king-of-africa.html` in de browser (via een lokale webserver, bijvoorbeeld `python3 -m http.server`, zodat de sprites geladen mogen worden).

Alle sprites, achtergronden en geluiden staan los op schijf. Het spel verwacht de mappenindeling hieronder; de paden staan letterlijk in de HTML.

## Episodes

In het menu onder **Levels** staan vijf reeksen: Episode 1 (de weg naar het koningschap), Episode Renew, Episode Winter World, de oefenlevels voor Rosa, en Test levels.

Episode Renew is tien levels lang en loopt op van rustig naar zwaar: van het dorp bij de start en het eerste doornbos, via de poelen, het doornenpad, de heuvelrug, de hyenavlakte, het verdronken dorp en de bergpas, naar de nacht waarin alles tegelijk komt, en tot slot twee keer de zwarte panter als eindbaas. Elk level heeft zijn eigen uitzicht en gebruikt alles wat het spel heeft: drinkkalebassen, doornbossen, water, ravijnen, terrassen en richels, dorpen, botten, hyena's, slangen en schorpioenen. De leveldefinities staan in de HTML als `RENEW_1` tot en met `RENEW_10`.

Episode Winter World speelt hoog in de bergen. Een level met `winter: true` krijgt sneeuw op alles wat je beklimt (de `_sneeuw`-versies van de rotsen en klimstukken), een besneeuwde grond met grijze rots eronder, bevroren gras, sneeuwval, een besneeuwd uitzicht (de `_sneeuw`-versies van de bergpanelen en de heuvelrij in `design/bg/`, uit `tools/sneeuw_bg.py`: witte toppen, sneeuw op de ruggen en de vlakte) en witte dieren: de witte hyena's uit `enemies/hyena_wit` en de witte panter uit `enemies/panter_wit`. Die winterplaatjes worden pas geladen als je zo'n level kiest. Van het dorp bestaat ook een winterversie: de zeven dorpsplaten hebben elk een `_sneeuw`-tegenhanger (`hut_round_arch_sneeuw`, `well_sneeuw`, enzovoort) die je in een leveldefinitie onder `village` neerzet, en in de bouwer staan een besneeuwde hut, boom en struik. Het winterlevel begint bij een ingesneeuwd berggehucht. De witte panter jaagt anders dan de zwarte: hij vervaagt in de sneeuw zolang hij sluipt (let op zijn schaduw), en zijn sprong is een hoge sneeuwduik die neerkomt op de plek waar je stond toen hij afzette. Bukken helpt niet, opzij stappen wel, en daarna zit hij even tot zijn buik in de sneeuw: dan steek je. Vanaf zijn tweede fase wisselt hij de duik af met de lage tackle. De leveldefinities staan in de HTML als `WINTER_1` en `WINTER_2`.

Winter 2 (De ijskloof) is de zwaardere tocht: steeds bredere ravijnen (tot 300), een trap van drie terrassen, een steile wand met twee richels waar je aan de andere kant 600 diep vanaf springt, twee ingesneeuwde gehuchten, roedels witte hyena's van twee kanten, en aan het eind opnieuw de witte panter. Het level heeft zijn eigen uitzicht (`winter_kloof`): later op de dag, donkerder blauw en dikkere nevel.

Sneeuw hoeft niet de hele winteruitrusting te zijn. Naast `winter: true` kan een level het veld `sneeuw` zetten, en dat is een andere vraag: niet "speelt dit hoog in de bergen", maar "ligt hier sneeuw op de grond, en op wat voor grond". Daar staan twee dingen los van elkaar. De bodem is `savanne` (de gewone rode grond) of `rots` (dezelfde grond als grijze steen, `design/grondrand_rots.png`). Het dek is de sneeuw die daar bovenop ligt, als losse laag in vier standen (`design/sneeuwlaag_25` tot `100`, uit `tools/sneeuwdek.py`). Rode grond blijft dus rood onder de sneeuw, want een ondergesneeuwde zandvlakte is nog altijd zand, en grijs is een keuze voor een rotsbodem in plaats van iets wat er vanzelf bij komt zodra het sneeuwt. Met `van` en `tot` loopt het dek onderweg op: `sneeuw: { soort: 'savanne', van: -1200, tot: -7000 }` begint kaal en eindigt dicht, met de eerste plekken in de kuiltjes en de sneeuwrand die over de breukrand gaat hangen. Zonder `van` en `tot` ligt overal evenveel (`dek`, standaard 1). In de sandbox staat het onder **Sneeuwdek**: geen, savanne of rotsbodem, minder of meer, en een overgang die vanaf waar je staat naar links oploopt. `winter: true` verandert er niet door en houdt zijn eigen ingebakken sneeuwgrond.

Of het sneeuwt, verschilt per potje. Bij de start wordt een weerplan geloot: de hele tijd sneeuw, helemaal geen, sneeuw die onderweg begint, sneeuw die onderweg ophoudt, of een bui midden in het level. Het plan hangt aan de afstand door het level, en begin en einde gaan langzaam: over ongeveer een tiende van het level dikt de sneeuw aan of dunt hij uit, en vlokken die weg moeten vallen gewoon uit beeld. Ook de dikte van de bui verschilt per potje (`planSnow` in de HTML).

In de winter is al het stof sneeuwstof (de stofplaatjes worden bij het laden wit gemaakt), en bij een landing of een lage zwaai stuift de sneeuw echt op: een brede lage wolk die blijft hangen, een waaier glinsterende kristallen en klonten die in een boog wegvliegen en bij het neerkomen een wolkje geven. Hoe harder je neerkomt, hoe groter de plof.

Test levels zijn korte proefstukken: een enkel level waarin je een mechaniek los kunt bekijken, zonder gevecht en zonder lange tocht eromheen. Ze staan met opzet apart van de echte episodes, zodat daar niets aan hoeft te veranderen om iets nieuws te kunnen proberen. **Test 1: Gang, dak en klimmen** loopt in drie stukken. Eerst een dak van rots over de weg heen: op twee cellen hoogte loop je er rechtop onderdoor, maar springen gaat niet. Dan een trap van drie terrassen omhoog en aan de andere kant weer omlaag. En tot slot een gang door de rots: het plafond zakt van vier cellen bij de ingang naar drie en dan naar twee, er staan twee blokken om op te klimmen (met een drinkkalebas erboven), en helemaal achterin loopt de rots dicht. Daar staan de fakkels die het level uitspelen. De definitie staat in de HTML als `TEST_1`.

In het pauzemenu (II of Escape) staat **Level overslaan**: die brengt je meteen naar het volgende level van dezelfde reeks. Onder **Instellingen** staan daar ook het tempo van het spel, het looptempo van Amir, het formaat van het beeld en de muziek. Tijdens een level is het speelveld verder leeg: de testbalk met schuifjes staat alleen in de bouwer en de sandbox (met B haal je hem er tijdens het spelen alsnog bij).

## Op je telefoon zetten

Het spel is een installeerbare webapp. Open de Pages-link in Safari, deel, "Zet op beginscherm". Daarna staat Amir als icoon tussen je apps en start hij zonder browserbalken, liggend.

Open hem vanaf het beginscherm en druk in het startmenu op **Download voor offline**. Dat haalt alle sprites en geluiden in een keer binnen (bijna 1200 bestanden, ongeveer 200 MB; het precieze aantal staat in `offline-assets.json`). Vanaf dat moment laadt het spel meteen en speelt het ook zonder internet.

Doe die download vanuit het beginscherm-icoon, niet vanuit Safari: iOS geeft een geinstalleerde webapp een eigen opslag, dus wat je in Safari downloadt telt daar niet mee.

Ook zonder op die knop te drukken wordt alles wat je tijdens het spelen tegenkomt bewaard, dus een tweede potje laadt sowieso sneller.

### Beeld: scherp of licht

Van een deel van de sprites staan twee versies op schijf: het origineel, en een halve versie met dezelfde mappen en namen in `klein/`. Het spel kiest bij het starten: een telefoon krijgt de kleine set, een laptop en een tablet de grote. In het startmenu staat onder **Beeld** een schakelaar (Automatisch, Scherp, Licht) om dat te overrulen; wisselen herlaadt de pagina, want de sprites zijn dan al geladen.

Waarom: de grote frames zijn op een telefoon vele malen groter dan ze getekend worden. Safari houdt ze niet allemaal uitgepakt in het geheugen en decodeert ze midden in het spel opnieuw, en dat zijn de hikjes. De tekencode rekt elk plaatje naar vaste maten, dus beide sets werken met dezelfde code. Ontbreekt een klein frame, dan valt het spel terug op het grote.

Welke plaatjes meedoen staat in `DOELEN` in `tools/gen-klein.py`, en dat is met opzet een korte lijst. Een plaatje halveren mag alleen als het op een telefoon nog steeds groter is dan het stukje scherm waar het op terechtkomt. Dat is per familie gemeten en de factor staat erbij. Meedoen: Amir, de hyena's, de panters, de schorpioen, de dorpeling, het droge gras, de kei, de verre hut, de botten en de grotset (7,3x: het plafond, de hoekstukken en de wandtegels zijn de grootste bronnen van het spel en worden tot een tiende getekend). Er juist buiten vallen de boom (1,0x), de struik (1,2x), het doornbos (0,9x), de dorpshutten (1,8x), de klif (1,9x) en de dorpelinge (1,9x): die staan al vrijwel op maat, dus halveren zou je meteen zien.

De download volgt de gekozen set: een telefoon haalt de kleine versies binnen en slaat de grote over, een laptop andersom. Dat scheelt ongeveer 58 MB.

Sprites toegevoegd of vervangen? Draai dan eerst de kleine set opnieuw en daarna de offline-lijst:

```
python3 tools/gen-klein.py
python3 tools/gen-offline-manifest.py
```

Het eerste script print aan het eind de lijst die in de HTML onder `KLEIN_FAM` hoort te staan. Loopt die niet gelijk, dan laadt een familie stilletjes de grote versie.

Op een aanraakscherm tekent het spel op anderhalve canvaspixel per schermpixel in plaats van twee: op zo'n klein scherm zie je dat niet, en het scheelt bijna de helft van het werk per frame. Haalt het toestel de frames dan nog niet, dan zakt het spel vanzelf nog een stap (naar 1) en blijft daar; in de console staat dan een regel met "resolutie omlaag".

### Hoe het werkt

| bestand | rol |
| --- | --- |
| `manifest.webmanifest` | naam, icoon, liggend scherm, start zonder browserbalken |
| `icons/` | app-iconen, gemaakt uit `amir.png` |
| `sw.js` | de service worker: bewaart het spel en de assets, en serveert ze offline |
| `offline-assets.json` | de lijst die de downloadknop afwerkt |
| `tools/gen-offline-manifest.py` | genereert die lijst uit de bestanden op schijf |

De service worker houdt twee caches uit elkaar. Het spel zelf (HTML, manifest, iconen) gaat network-first: online speel je altijd de nieuwste versie, offline de laatst bekende. De sprites en geluiden gaan cache-first en blijven staan, ook als je het spel update. Een nieuwe versie van de HTML kost dus geen nieuwe download van 200 MB.

**Assets toegevoegd of vervangen?** Draai daarna:

```
python3 tools/gen-offline-manifest.py
```

De versie in `offline-assets.json` verandert mee, en de service worker ziet daaraan dat de oude assetcache weg mag.

## Besturing

| | laptop | telefoon |
|---|---|---|
| lopen, rennen | pijltjes, Shift sprint | joystick (duim links) |
| springen | pijl omhoog | ▲ |
| bukken | pijl omlaag | joystick omlaag |
| stoten | spatie (korte tik) | ✦ (korte tik) |
| **speer recht vooruit** | **spatie vasthouden, loslaten** | **✦ vasthouden, loslaten** |
| **speer in een boog** | **langer vasthouden, dan loslaten** | **langer vasthouden, dan loslaten** |
| worp afbreken | tik in plaats van vasthouden | duim van ✦ af slepen en daar loslaten |
| speer oppakken | E, waar je ook langs de schacht staat | E (verschijnt als je er vlakbij staat) |
| drinken | Q | het kalebasje |

### De speerworp

Er wordt niet gemikt. Hoe lang je de knop vasthoudt bepaalt de worp, en de
animatie vertelt zelf welke je krijgt, want hij trekt in twee trappen uit:

| vasthouden | wat er gebeurt |
|---|---|
| tot 0,16 s | de oude stoot, ongewijzigd |
| tot ongeveer 0,77 s | eerste trap: hij trekt uit tot frame 4 en wacht daar. Loslaten geeft de vlakke worp |
| langer | tweede trap: frames 5 en 6 lopen alsnog door en daar wacht hij. Loslaten geeft de boog |

Die twee frames ertussen zijn de aankondiging. Zijn voorste arm komt omhoog en
naar voren, hij zakt dieper door zijn knieën, en er glinstert even iets op de
speerpunt. Daarom is er geen balkje en geen richtpijltje nodig.

De boog gaat 30 graden omhoog maar met 78 procent van de worpkracht: een lob,
geen verdragende worp. Vlak komt ongeveer 0,8 scherm verderop neer, de boog
piekt bijna drie keer Amirs lengte en landt rond 1,6 scherm. Lang vasthouden is
daarmee niet gewoon beter, want de boog zeilt over alles heen wat dichtbij
staat en je staat er een halve seconde langer kwetsbaar voor stil.

Amir staat vast zolang hij spant en werpt: niet lopen, niet springen, en de hele
animatie is kwetsbaar. Tot en met frame 6 kan de worp nog afgebroken worden en
houdt hij zijn speer; vanaf frame 7 gaat hij door. Laat je los in de laatste 0,1
seconde voordat Amir geraakt wordt, dan gaat de speer alsnog weg.

De geworpen speer zakt door onder een derde van de zwaartekracht op Amir en
wijst elk frame de kant van zijn snelheid op. Raakt hij een dier, dan doet hij
schade en valt hij neer. Raakt hij grond of muur, dan blijft hij steken en
natrillen, en een speer die in een muur steekt is een dun platform waar je op
kunt staan (alleen van bovenaf; de schacht buigt 3 px door onder Amir). In een
doornbos richt hij niets aan: hij zakt de takken in tot iets minder dan de helft
van zijn lengte, het uiteinde hangt door en steekt eruit, en je trekt hem er met
E weer uit. Hak je het struweel daarna om, dan valt hij op de grond. Een speer
die ergens in steekt wordt achter Amir langs getekend, dus hij loopt nooit meer
dwars door hem heen als je ernaast gaat staan om hem te pakken.

Oppakken doe je bij de schacht, niet bij de punt: de E verschijnt zodra je bij
het stuk staat waar je hem vastpakt, en dat is meestal het stompe uiteinde.

Een speer in een muur wrikt zichzelf na twaalf seconden los en valt langs de
wand naar beneden. De laatste anderhalve seconde trilt hij, dus je ziet het
aankomen. Sta je erop, dan houdt hij het: de klok loopt alleen als je er niet
op staat, en hij gaat verder waar hij was zodra je eraf stapt. Zo blijft een
speer die te hoog in een steile wand terechtkomt nooit hangen waar je niet bij
kunt.

Je raakt hem nooit kwijt. Komt hij in het water of buiten de wereld terecht, dan
ligt hij na drie seconden weer op de laatste vaste grond waar Amir stond. Valt
hij in een ravijn, dan duikt hij na drie seconden aan de overkant op, net buiten
beeld: je loopt er vanzelf tegenaan zodra je de oversteek gehaald hebt. Gooi je
hem tijdens een bazengevecht het veld uit, dan telt dat net zo: je kunt de arena
niet uit, dus hij komt na drie seconden terug bij jou. Alles los te testen met
de knoppen onder "Speerworp" in de sandbox; onder "Ravijn" zet je er een breuk
naast om de rand te bekijken.

Tegen een panter geldt dezelfde regel als voor de stoot en de lage zwaai: raak
is hij alleen in zijn herstel, na een sprong, een duik of een tackle. Ziet hij
je de speer uittrekken terwijl hij op zijn poten staat, dan springt hij opzij,
en een speer die hem daarbuiten raakt ketst af op zijn vacht. De duik van de
witte panter zet hem tot zijn buik in de sneeuw: dat is het langste venster en
je staat er ver genoeg vanaf om te werpen.

## Rots boven en naast je

Een rotsgebied is geen losse grotkamer maar terrein: een raster waarin elke cel vol of
leeg is. Amir loopt door de lege cellen als door een uitgehakte gang, en rots kan net zo
goed boven of naast hem zitten als eronder. Waar een cel leeg is zie je gewoon de lucht en
de savanne erdoorheen, dus een rotsmassa kan ook de bovenkant van een level zijn.

Het gesteente is hetzelfde gesteente als een terras. Rots is in dit spel al iets dat je
beklimt, met een bovenvlak om op te lopen en een geribbelde wand eronder, en een rotsgebied
gebruikt precies dat: een blok rots is van hetzelfde steen als de terrassen ernaast, en in
een winterlevel ligt er dezelfde sneeuw op. De zijkanten staan niet kaarsrecht maar breken
open, net als de zijkant van een terras.

De onderkant heeft een terras niet, want daar kom je bij een terras nooit. Rots met open
ruimte eronder krijgt daarom de tandenrand uit de grotset: een rij grillige punten die met
hun aanzet in het steen staan en met hun punten in de open ruimte hangen. Een rotsdak leest
daardoor als de onderkant van dezelfde berg waar de grond de bovenkant van is, of je nu
ergens onderdoor loopt of door een vallei met rots boven je.

Twee randen heeft de set niet, en die worden opgevuld met losse brokken: waar een vloer op
een wand uitkomt ligt een handvol keien over de naad, en waar een plafond tegen een hogere
wand aan loopt hangt er een blok in de hoek. Verder krijgt ongeveer een op de drie randen
iets mee, verstrooid met een vaste seed: hangblokken onder het plafond en keien op de
vloeren. Dezelfde seed geeft elke keer precies hetzelfde, maar niets staat op een
regelmatige afstand. Een richel om op te springen wordt niet verstrooid: die zet een level
neer waar hij als opstap bedoeld is.

Een cel is precies zo hoog als een terrastrede, en die hoogte schaalt mee met Amir. Op elk
scherm klim je dus wel op een blok van één cel en nooit op een blok van twee, en loop je
rechtop door een gang van twee cellen maar stoot je je hoofd als je springt.

De volle cellen zijn massief: je stoot je hoofd tegen het plafond, je loopt niet door een
wand heen en je staat op de vloeren. Een richel is een plankje waar je op kunt staan, met
een hitbox die alleen de bovenkant van het brok beslaat. Losse keien en hangblokken zijn
puur decor.

Alles los te proberen met de knoppen onder **Rots** in de sandbox: een gang met rots boven
en naast je, een dak om je hoofd aan te stoten, een uitstekende pilaar en een trap om op te
klimmen. Elke druk geeft een andere seed. Met **Hitboxen aan** zie je welke cellen vol zijn.

## Mappenstructuur## Mappenstructuur

```
amir-king-of-africa.html   het spel
amir.png                   omslag / poster

karakters/
  amir/
    idle/                  idle_ns.png (zonder speer), idle_sp.png (met speer)
    aanval/
      speerstrike/         attack_sp_1..10.png
      lowsweep/            sweep_1..18.png (lage zwaai vanuit gebukt)
    beweging/
      run/run/             run_ns_1..8.png
      run/speerrun/        run_sp_1..8.png
      jump/jump/           amirjump0staand .. amirjump6landing.png
      jump/jumpspeer/      amirjumpspear0staand .. amirjumpspear6landing.png
      bukken/bukken/       bukken_in_1..8.png, bukken_hold_1..4.png
      bukken/bukkenspeer/  bukken_in_1..8_speer.png, bukken_hold_1..4_speer.png
  dorpeling1/
    dorpelingidle/         idle_01..12.png
  dorpelinge/              sfeerkarakter met kruik, 204x360, grondlijn rij 353, 12 fps
    idle/                  idle_00..17.png (lus)
    neerzetten/            neerzetten_00..25.png (eenmalig, gaat over in gehurkt)
    gehurkt/               gehurkt_00..17.png (lus)
    oppakken/              oppakken_00..25.png (eenmalig, gaat over in idle)
    metadata.json          framecounts en bounding boxes per frame
    preview/               sheets en preview-gifs, bronmateriaal

enemies/
  slang1/                  groene slang: idle_1..8, move_1..8, attack_1..8.png (+ mp4 referenties)
  slang2/                  zwarte slang: idem, plus venom.png (het gif) en sprite sheets
  schorpioen1/
    schorpioen_walk_12/    walk_01..12.png
    charge/schorpioen_charge_12/  charge_01..12.png
    schorpioen_curl_12frames/  curl_01..12.png
  blackpanther/
    blackpanther/          walk/, turn/, prowl/, pounce/, run/ (frames _00.. en sprite sheets)
    lowstrike/             claw_00..13.png (klauwhaal)
    pantherroar.mp3, panter snarl.mp3, panter_snarl_lang.mp3   pantergeluiden
  panter_wit/              de witte panter (Winter World): dezelfde frames, wit gemaakt met tools/winter_art.py
    panter_wit/            walk/, turn/, prowl/, pounce/, run/
    lowstrike/             claw_00..13.png
  hyena_wit/               de witte hyena (Winter World): loop/, dreigen/, ren_lijf/, ren_kop/, uit tools/winter_art.py
  hyena/
    loop/                  loop_00..19.png (aankomen en achteruit stappen)
    dreigen/               dreigen_00..21.png (op afstand blijven grommen)
    ren_lijf/              ren_lijf_00..11.png (onderlaag van de aanvalsren, 16 fps)
    ren_kop/               ren_kop_00..26.png (bovenlaag: de happende kop, 8 fps)
    metadata.json          canvas, grondlijn, aantallen, fps en de kop-offset per lijfframe
    preview/               sprite sheets en preview-gifs (bronmateriaal)

amir runc/
  amir_sprites/design/amir/
    speerworp/             speerworp_00..19.png (eenmalige worp, 20 frames, 12 fps),
                           metadata.json (canvas 984x814, grondlijn rij 803, anker_x 330,
                           Amir 620 px hoog, spannen 0-6, uithaal 7-10, los op 10, herstel 11-19)
    speer_projectiel.png   de geworpen speer, 624x67, punt naar rechts op pixel (623, 33)

items/
  potions/                 hppotion.png (de drinkkalebas die gezondheid teruggeeft)

design/
  *.png / *.jpg            losse props en texturen: boulder, tree, struik, villeaghut, drygrass,
                           cliff, flatrock, grondrand, rotstextuur, savannesand, speer, stofwolk, stofsliert, einde
  bg/laag1/                verre bergen (parallax laag 1); *_sneeuw.png = de winterversie (tools/sneeuw_bg.py)
  bg/laag2/                savanneheuvels (parallax laag 2); *_sneeuw.png = idem, met sneeuw op de ruggen en de vlakte
  botten/                  botten en schedels om op de grond te leggen
  grot/                    de grot- en ravijnset: plafond_strook, hoek_plafond_wand, wand_rand,
                           wand_richel, hangblok_01..03, kei_01..07, kei_rond_01..08. In grot.json
                           staan de maten en de ankerpunten van elk onderdeel; de tekencode rekent
                           daarmee, dus de kleine versies in klein/ vallen precies op hun plek
  klimmen/                 klif_bovenrand, klif_richel, klif_binnenhoek
  *_sneeuw.png             winterversies van flatrock, boulder, cliff en de drie klimstukken; gemaakt
                           met tools/sneeuw.py (draai dat opnieuw als een origineel verandert).
                           grondrand_sneeuw en drygrass_sneeuw komen uit tools/winter_art.py.
                           villeaghut_sneeuw, tree_sneeuw, struik_sneeuw en de zeven platen in
                           village/*_sneeuw.png (sneeuw op het dak, de randen en de grond, bevroren
                           gras) komen uit tools/sneeuw_dorp.py
  grondrand_rots.png       de grond als grijze steen, zonder sneeuw: de rotsbodem van het veld sneeuw
  sneeuwlaag_25..100.png   het sneeuwdek als doorzichtige laag, in vier standen. Past op allebei de
                           bodems en is genest (wat op 25 wit is, is dat op 50 ook), zodat een level
                           onderweg van stand kan wisselen zonder dat er sneeuw verdwijnt.
                           Allebei uit tools/sneeuwdek.py
  vegetatie/               boom_sheet, drygrass_sheet, struik_sheet (bewegende vegetatie) en de losse frames
  water/                   pool_links/midden/rechts, rimpel_01..08, spetter_01..08

sounds/                    hyena_bite.mp3 (lange opname; alleen 14,0-16,0 s is de hap die het spel
                           afspeelt) en hyena_laugh.mp3 (de lach)

music/                     bg.mp3 (achtergrond), stemmen van Amir (iamtheking, iamamir, iamamirfatherson,
                           hellomyfriend, ikill, protectinnocent, godsforsaken), snakehiss, spearthrust, scatter,
                           watersplash (de volle plons: instappen en landen) en waterstep (de korte knip
                           uit diezelfde plons, voor de voetstappen in het water)
```

De `*_magenta.png`, `*_preview.gif`, `*_sheet.png` en `*_spritesheet*.png` bestanden zijn bronmateriaal en voorbeelden; het spel gebruikt de losse frames.
