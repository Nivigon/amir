# Amir: King of Africa

Een browserspel in een enkel bestand: open `amir-king-of-africa.html` in de browser (via een lokale webserver, bijvoorbeeld `python3 -m http.server`, zodat de sprites geladen mogen worden).

Alle sprites, achtergronden en geluiden staan los op schijf. Het spel verwacht de mappenindeling hieronder; de paden staan letterlijk in de HTML.

## Episodes

In het menu onder **Levels** staan vier reeksen: Episode 1 (de weg naar het koningschap), Episode Renew, Episode Winter World en de oefenlevels voor Rosa.

Episode Renew is tien levels lang en loopt op van rustig naar zwaar: van het dorp bij de start en het eerste doornbos, via de poelen, het doornenpad, de heuvelrug, de hyenavlakte, het verdronken dorp en de bergpas, naar de nacht waarin alles tegelijk komt, en tot slot twee keer de zwarte panter als eindbaas. Elk level heeft zijn eigen uitzicht en gebruikt alles wat het spel heeft: drinkkalebassen, doornbossen, water, ravijnen, terrassen en richels, dorpen, botten, hyena's, slangen en schorpioenen. De leveldefinities staan in de HTML als `RENEW_1` tot en met `RENEW_10`.

Episode Winter World speelt hoog in de bergen. Een level met `winter: true` krijgt sneeuw op alles wat je beklimt (de `_sneeuw`-versies van de rotsen en klimstukken), een besneeuwde grond met grijze rots eronder, bevroren gras, sneeuwval, een besneeuwd uitzicht (de `_sneeuw`-versies van de bergpanelen en de heuvelrij in `design/bg/`, uit `tools/sneeuw_bg.py`: witte toppen, sneeuw op de ruggen en de vlakte) en witte dieren: de witte hyena's uit `enemies/hyena_wit` en de witte panter uit `enemies/panter_wit`. Die winterplaatjes worden pas geladen als je zo'n level kiest. Van het dorp bestaat ook een winterversie: de zeven dorpsplaten hebben elk een `_sneeuw`-tegenhanger (`hut_round_arch_sneeuw`, `well_sneeuw`, enzovoort) die je in een leveldefinitie onder `village` neerzet, en in de bouwer staan een besneeuwde hut, boom en struik. Het winterlevel begint bij een ingesneeuwd berggehucht. De witte panter jaagt anders dan de zwarte: hij is half onzichtbaar zolang hij sluipt (let op zijn schaduw), en zijn sprong is een hoge sneeuwduik die neerkomt op de plek waar je stond toen hij afzette. Bukken helpt niet, opzij stappen wel, en daarna zit hij even tot zijn buik in de sneeuw: dan steek je. Vanaf zijn tweede fase wisselt hij de duik af met de lage tackle. De leveldefinities staan in de HTML als `WINTER_1` en `WINTER_2`.

Winter 2 (De ijskloof) is de zwaardere tocht: steeds bredere ravijnen (tot 300), een trap van drie terrassen, een steile wand met twee richels waar je aan de andere kant 600 diep vanaf springt, twee ingesneeuwde gehuchten, roedels witte hyena's van twee kanten, en aan het eind opnieuw de witte panter. Het level heeft zijn eigen uitzicht (`winter_kloof`): later op de dag, donkerder blauw en dikkere nevel.

Of het sneeuwt, verschilt per potje. Bij de start wordt een weerplan geloot: de hele tijd sneeuw, helemaal geen, sneeuw die onderweg begint, sneeuw die onderweg ophoudt, of een bui midden in het level. Het plan hangt aan de afstand door het level, en begin en einde gaan langzaam: over ongeveer een tiende van het level dikt de sneeuw aan of dunt hij uit, en vlokken die weg moeten vallen gewoon uit beeld. Ook de dikte van de bui verschilt per potje (`planSnow` in de HTML).

In de winter is al het stof sneeuwstof (de stofplaatjes worden bij het laden wit gemaakt), en bij een landing of een lage zwaai stuift de sneeuw echt op: een brede lage wolk die blijft hangen, een waaier glinsterende kristallen en klonten die in een boog wegvliegen en bij het neerkomen een wolkje geven. Hoe harder je neerkomt, hoe groter de plof.

In het pauzemenu (II of Escape) staat **Level overslaan**: die brengt je meteen naar het volgende level van dezelfde reeks.

## Op je telefoon zetten

Het spel is een installeerbare webapp. Open de Pages-link in Safari, deel, "Zet op beginscherm". Daarna staat Amir als icoon tussen je apps en start hij zonder browserbalken, liggend.

Open hem vanaf het beginscherm en druk in het startmenu op **Download voor offline**. Dat haalt alle sprites en geluiden in een keer binnen (bijna 1200 bestanden, ongeveer 200 MB; het precieze aantal staat in `offline-assets.json`). Vanaf dat moment laadt het spel meteen en speelt het ook zonder internet.

Doe die download vanuit het beginscherm-icoon, niet vanuit Safari: iOS geeft een geinstalleerde webapp een eigen opslag, dus wat je in Safari downloadt telt daar niet mee.

Ook zonder op die knop te drukken wordt alles wat je tijdens het spelen tegenkomt bewaard, dus een tweede potje laadt sowieso sneller.

### Beeld: scherp of licht

Van een deel van de sprites staan twee versies op schijf: het origineel, en een halve versie met dezelfde mappen en namen in `klein/`. Het spel kiest bij het starten: een telefoon krijgt de kleine set, een laptop en een tablet de grote. In het startmenu staat onder **Beeld** een schakelaar (Automatisch, Scherp, Licht) om dat te overrulen; wisselen herlaadt de pagina, want de sprites zijn dan al geladen.

Waarom: de grote frames zijn op een telefoon vele malen groter dan ze getekend worden. Safari houdt ze niet allemaal uitgepakt in het geheugen en decodeert ze midden in het spel opnieuw, en dat zijn de hikjes. De tekencode rekt elk plaatje naar vaste maten, dus beide sets werken met dezelfde code. Ontbreekt een klein frame, dan valt het spel terug op het grote.

Welke plaatjes meedoen staat in `DOELEN` in `tools/gen-klein.py`, en dat is met opzet een korte lijst. Een plaatje halveren mag alleen als het op een telefoon nog steeds groter is dan het stukje scherm waar het op terechtkomt. Dat is per familie gemeten en de factor staat erbij. Meedoen: Amir, de hyena's, de panters, de schorpioen, de dorpeling, het droge gras, de kei, de verre hut en de botten. Er juist buiten vallen de boom (1,0x), de struik (1,2x), het doornbos (0,9x), de dorpshutten (1,8x), de klif (1,9x) en de dorpelinge (1,9x): die staan al vrijwel op maat, dus halveren zou je meteen zien.

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

## Mappenstructuur

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

items/
  potions/                 hppotion.png (de drinkkalebas die gezondheid teruggeeft)

design/
  *.png / *.jpg            losse props en texturen: boulder, tree, struik, villeaghut, drygrass,
                           cliff, flatrock, grondrand, rotstextuur, savannesand, speer, stofwolk, stofsliert, einde
  bg/laag1/                verre bergen (parallax laag 1); *_sneeuw.png = de winterversie (tools/sneeuw_bg.py)
  bg/laag2/                savanneheuvels (parallax laag 2); *_sneeuw.png = idem, met sneeuw op de ruggen en de vlakte
  botten/                  botten en schedels om op de grond te leggen
  klimmen/                 klif_bovenrand, klif_richel, klif_binnenhoek
  *_sneeuw.png             winterversies van flatrock, boulder, cliff en de drie klimstukken; gemaakt
                           met tools/sneeuw.py (draai dat opnieuw als een origineel verandert).
                           grondrand_sneeuw en drygrass_sneeuw komen uit tools/winter_art.py.
                           villeaghut_sneeuw, tree_sneeuw, struik_sneeuw en de zeven platen in
                           village/*_sneeuw.png (sneeuw op het dak, de randen en de grond, bevroren
                           gras) komen uit tools/sneeuw_dorp.py
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
