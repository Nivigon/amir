# Amir: King of Africa

Een browserspel in een enkel bestand: open `amir-king-of-africa.html` in de browser (via een lokale webserver, bijvoorbeeld `python3 -m http.server`, zodat de sprites geladen mogen worden).

Alle sprites, achtergronden en geluiden staan los op schijf. Het spel verwacht de mappenindeling hieronder; de paden staan letterlijk in de HTML.

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

design/
  *.png / *.jpg            losse props en texturen: boulder, tree, struik, villeaghut, drygrass,
                           cliff, flatrock, grondrand, rotstextuur, savannesand, speer, stofwolk, stofsliert, einde
  bg/laag1/                verre bergen (parallax laag 1)
  bg/laag2/                savanneheuvels (parallax laag 2)
  botten/                  botten en schedels om op de grond te leggen
  klimmen/                 klif_bovenrand, klif_richel, klif_binnenhoek
  vegetatie/               boom_sheet, drygrass_sheet, struik_sheet (bewegende vegetatie) en de losse frames
  water/                   pool_links/midden/rechts, rimpel_01..08, spetter_01..08

music/                     muziek en stemmen (nog niet in deze repo, zie music/README.md)
```

De `*_magenta.png`, `*_preview.gif`, `*_sheet.png` en `*_spritesheet*.png` bestanden zijn bronmateriaal en voorbeelden; het spel gebruikt de losse frames.
