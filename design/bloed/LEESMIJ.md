# Bloed-effecten voor Amir - testlevel "bloed"

Dit pakket bevat de bloed-assets en de spec voor het bloed-systeem. Alles is al
op kleur (rood, met alpha), dus gewoon gebruiken zoals het is.

Alles staat in `design/bloed/`, het geluid in `sounds/bloedspuit.mp3` (dat speelt
tijdens het opspuiten van bloed).

## Inhoud

- `snedes/` : 3 statische snee-decals (PNG met alpha).
  - `snee_recht.png` (480x375), lange rechte diagonale haal
  - `snee_haal.png` (164x620), kortere kronkelige haal met drip
  - `snee_dwars.png` (480x136), lange horizontale haal
  - `snedes.json` : maten en vorm per snee
- `spuit_donker/` : bloedspuit-animatie, donkere variant. 27 frames, canvas 360x454.
- `spuit_fel/` : bloedspuit-animatie, iets fellere variant. 27 frames, canvas 360x420.
  - elke map heeft een `<naam>.json` met frames, canvas, anker en per frame de `ticks`.
- `sounds/bloedspuit.mp3` : het geluid bij de bloedspuit (één keer afspelen bij het
  opspuiten, frames 0 tot 6).

Kies zelf een van de twee spuiten (donker of fel) voor de death-spuit.

## Het bloed-systeem (testlevel "bloed", getest op de normale bandiet)

Maak een nieuw testlevel genaamd "bloed" met een normale bandiet erin. Elke rake
klap op de bandiet laat een snee achter op zijn lichaam, en de derde klap is dodelijk:

1. **Eerste treffer:** plaats een hele kleine snee op zijn lichaam, op het raakpunt.
   Gebruik bijvoorbeeld `snee_haal` of `snee_recht`, klein geschaald (ongeveer 15
   procent van de bandiet-hoogte).
2. **Tweede treffer:** een grotere snede erbij (zelfde of andere snee, ongeveer 30
   procent van de bandiet-hoogte), op een nieuw raakpunt.
3. **Derde treffer (dodelijk):** speel de death-animatie van de bandiet, maar houd
   hem even vast op een vroeg frame waar hij geraakt nog overeind of half staat (voor
   hij echt neervalt). Op dat vastgehouden frame begint uit een snee op zijn borst
   bloed te spuiten (de spuit-animatie). Laat de spuit een moment lopen, speel dan de
   rest van de death-animatie af zodat hij neervalt.

## De snee-decals plaatsen

- Center-anchored, vrij schaalbaar en vrij roteerbaar.
- **Clip de decal op het silhouet (alpha-masker) van het bandiet-frame**, zodat het
  bloed netjes op de huid blijft en niet buiten zijn lichaam uitsteekt.
- De decal beweegt mee met de sprite: gebruik per frame dezelfde transform als de
  bandiet, zodat de snee op zijn plek op het lichaam blijft kleven terwijl hij beweegt.
- Spiegelen en roteren mag, zodat dezelfde snee op meerdere plekken en hoeken anders
  oogt.

## De spuit-animatie

- Losse frames op een gedeeld canvas. Het **anker is onder-midden** van de frame: daar
  zit het wondpunt, het bloed komt vanaf de onderrand omhoog.
- Zet het anker op het wondpunt op de borst, en roteer de spuit naar de richting van de
  wond. Voor een wond in de zij of borst (zijaanzicht) draai je de spuit een kwartslag,
  zodat hij zijwaarts spuit in plaats van recht omhoog.
- **One-shot**. De frames zijn ongelijkmatig uitgedund (dicht tijdens het opspuiten, grof
  tijdens het plateau en het uitdruppelen), dus speel ze af met de `ticks` per frame op een
  24 fps klok: elk frame blijft `ticks` lang staan. Zo klopt de timing met een compacte set.
  Frames 0 tot 6 zijn het opspuiten. Op bronsnelheid is dat samen ongeveer 6 seconden, speel
  de ticks gerust 2 tot 3 keer sneller af voor een korte, krachtige kill-spuit.
- Teken de spuit voor (over) de bandiet-sprite, zodat hij uit het lichaam lijkt te komen.

## Later

- Een klein lichteffect rond een verse snee (korte witte flits of lichte gloed op het
  moment van de treffer) kan de engine toevoegen, zit niet in de assets.
- De bloedplas onder een lijk en de klodder op de lens komen in een volgend pakket.
