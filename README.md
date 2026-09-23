# Amir: King of Africa

Een browserspel in een enkel bestand: open `amir-king-of-africa.html` in de browser (via een lokale webserver, bijvoorbeeld `python3 -m http.server`, zodat de sprites geladen mogen worden).

Alle sprites, achtergronden en geluiden staan los op schijf. Het spel verwacht de mappenindeling hieronder; de paden staan letterlijk in de HTML.

## Op je telefoon zetten

Het spel is een installeerbare webapp. Open de Pages-link in Safari, deel, "Zet op beginscherm". Daarna staat Amir als icoon tussen je apps en start hij zonder browserbalken, liggend.

Open hem vanaf het beginscherm en druk in het startmenu op **Download voor offline**. Dat haalt alle 511 sprites en geluiden (ongeveer 104 MB) in een keer binnen. Vanaf dat moment laadt het spel meteen en speelt het ook zonder internet.

Doe die download vanuit het beginscherm-icoon, niet vanuit Safari: iOS geeft een geinstalleerde webapp een eigen opslag, dus wat je in Safari downloadt telt daar niet mee.

Ook zonder op die knop te drukken wordt alles wat je tijdens het spelen tegenkomt bewaard, dus een tweede potje laadt sowieso sneller.

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

music/                     bg.mp3 (achtergrond), stemmen van Amir (iamtheking, iamamir, iamamirfatherson,
                           hellomyfriend, ikill, protectinnocent, godsforsaken), snakehiss, spearthrust, scatter,
                           watersplash (de volle plons: instappen en landen) en waterstep (de korte knip
                           uit diezelfde plons, voor de voetstappen in het water)
```

De `*_magenta.png`, `*_preview.gif`, `*_sheet.png` en `*_spritesheet*.png` bestanden zijn bronmateriaal en voorbeelden; het spel gebruikt de losse frames.
