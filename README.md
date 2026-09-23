# Amir: King of Africa

Een browserspel in een enkel bestand: open `amir-king-of-africa.html` in de browser (via een lokale webserver, bijvoorbeeld `python3 -m http.server`, zodat de sprites geladen mogen worden).

Alle sprites, achtergronden en geluiden staan los op schijf. Het spel verwacht de mappenindeling hieronder; de paden staan letterlijk in de HTML.

## Episodes

In het menu onder **Levels** staan drie reeksen: Episode 1 (de weg naar het koningschap), Episode Renew en de oefenlevels voor Rosa.

Episode Renew is tien levels lang en loopt op van rustig naar zwaar: van het dorp bij de start en het eerste doornbos, via de poelen, het doornenpad, de heuvelrug, de hyenavlakte, het verdronken dorp en de bergpas, naar de nacht waarin alles tegelijk komt, en tot slot twee keer de zwarte panter als eindbaas. Elk level heeft zijn eigen uitzicht en gebruikt alles wat het spel heeft: drinkkalebassen, doornbossen, water, ravijnen, terrassen en richels, dorpen, botten, hyena's, slangen en schorpioenen. De leveldefinities staan in de HTML als `RENEW_1` tot en met `RENEW_10`.

In het pauzemenu (II of Escape) staat **Level overslaan**: die brengt je meteen naar het volgende level van dezelfde reeks.

## Op je telefoon zetten

Het spel is een installeerbare webapp. Open de Pages-link in Safari, deel, "Zet op beginscherm". Daarna staat Amir als icoon tussen je apps en start hij zonder browserbalken, liggend.

Open hem vanaf het beginscherm en druk in het startmenu op **Download voor offline**. Dat haalt alle 595 sprites en geluiden (ongeveer 121 MB) in een keer binnen. Vanaf dat moment laadt het spel meteen en speelt het ook zonder internet.

Doe die download vanuit het beginscherm-icoon, niet vanuit Safari: iOS geeft een geinstalleerde webapp een eigen opslag, dus wat je in Safari downloadt telt daar niet mee.

Ook zonder op die knop te drukken wordt alles wat je tijdens het spelen tegenkomt bewaard, dus een tweede potje laadt sowieso sneller.

### Beeld: scherp of licht

Van Amir en de hyena staan twee spritesets op schijf: de grote in `karakters/amir/` en `enemies/hyena/`, en een halve versie met dezelfde mappen en namen in `klein/`. Het spel kiest bij het starten: een telefoon of tablet krijgt de kleine set, een laptop de grote. In het startmenu staat onder **Beeld** een schakelaar (Automatisch, Scherp, Licht) om dat te overrulen; wisselen herlaadt de pagina, want de sprites zijn dan al geladen.

Waarom: de grote frames zijn op een telefoon vele malen groter dan ze getekend worden. Safari houdt ze niet allemaal uitgepakt in het geheugen en decodeert ze midden in het spel opnieuw, en dat zijn de hikjes. De tekencode rekt elk plaatje naar vaste maten, dus beide sets werken met dezelfde code.

Sprites van Amir of de hyena toegevoegd of vervangen? Draai dan eerst de kleine set opnieuw en daarna de offline-lijst:

```
python3 tools/gen-klein.py
python3 tools/gen-offline-manifest.py
```

Op een aanraakscherm tekent het spel op anderhalve canvaspixel per schermpixel in plaats van twee: op zo'n klein scherm zie je dat niet, en het scheelt bijna de helft van het werk per frame. Haalt het toestel de frames dan nog niet, dan zakt het spel vanzelf nog een stap (naar 1) en blijft daar; in de console staat dan een regel met "resolutie omlaag".

### Hoe het werkt

| bestand | rol |
| --- | --- |
| `manifest.webmanifest` | naam, icoon, liggend scherm, start zonder browserbalken |
| `icons/` | app-iconen, gemaakt uit `amir.png` |
| `sw.js` | de service worker: bewaart het spel en de assets, en serveert ze offline |
| `offline-assets.json` | de lijst die de downloadknop afwerkt |
| `tools/gen-offline-manifest.py` | genereert die lijst uit de bestanden op schijf |

De service worker houdt twee caches uit elkaar. Het spel zelf (HTML, manifest, iconen) gaat network-first: online speel je altijd de nieuwste versie, offline de laatst bekende. De sprites en geluiden gaan cache-first en blijven staan, ook als je het spel update. Een nieuwe versie van de HTML kost dus geen nieuwe download van 100 MB.

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
  bg/laag1/                verre bergen (parallax laag 1)
  bg/laag2/                savanneheuvels (parallax laag 2)
  botten/                  botten en schedels om op de grond te leggen
  klimmen/                 klif_bovenrand, klif_richel, klif_binnenhoek
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
