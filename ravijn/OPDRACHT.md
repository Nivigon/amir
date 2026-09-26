# Opdracht: openscheurend ravijn inbouwen in Amir - King of Africa

## Hoe Tom wil werken

In blokjes van ongeveer vijf minuten, met na elk blokje iets zichtbaars dat hij kan
uitproberen. Houd je daaraan:

- Doe één blokje per keer. Stop daarna en zeg wat hij moet checken.
- Stel alleen de vragen die voor dat blokje nodig zijn. Niet alles vooraf.
- Elk blokje bouwt op het vorige en breekt niets van wat al werkte.
- Zie je een praktisch bezwaar of een snellere route, zeg het meteen.

## Wat je krijgt

Het effect is al gebouwd en getest. Je hoeft het niet te ontwerpen, alleen aan te sluiten.

```
ravijn-effect.js               de module, geen dependencies, plain JS
ravijn-test.html               losse testpagina, werkt zonder de game
assets/ravijn_wand.png         de ravijnwand met alpha, 277x189, rij 0 = grondlijn
assets/steen_1..5.png          losse steentjes die meetrillen
assets/grond_strip.png         alleen voor de testpagina
assets/referentie_frames.png   zes gelabelde momenten uit de animatie
```

Bekijk `assets/referentie_frames.png` voor je begint. Dat is waar je naartoe werkt.

---

# Blok 0: zonder code (2 minuten, doet Tom zelf)

Pak de map uit en open `ravijn-test.html` in de browser. Druk op Start. Dit is precies wat
er straks in de game moet gebeuren. Met de schuiven kun je de breedte en de kwaliteit
veranderen, en met het vinkje de animatie op halve snelheid bekijken.

---

# Blok 1: het effect draait in de game (5 minuten)

Doel: Tom drukt op een toets in de game en ziet het ravijn opengaan. Nog nergens aan
gekoppeld, alleen zichtbaar.

**Vraag eerst alleen dit:** welke toets mag je gebruiken om het te testen, en in welke map
zet hij de assets. Voorstel: toets `O` en map `design/ravijn/`.

Dan:

1. Zet de assets neer en laad `ravijn-effect.js` in het HTML-bestand.
2. Laad de drie plaatjes even simpel, niet via de asset-loader van de game. Dat komt later.

```js
const ravijnWand = new Image(); ravijnWand.src = 'design/ravijn/ravijn_wand.png';
const ravijnStenen = [];
for (let i = 1; i <= 5; i++) {
  const s = new Image(); s.src = 'design/ravijn/steen_' + i + '.png'; ravijnStenen.push(s);
}
```

3. Maak één instantie op schermcoordinaten, midden in beeld, en teken alles bovenop:

```js
let ravijnFx = new RavijnEffect({
  wallImage: ravijnWand,
  stoneImages: ravijnStenen,
  x: canvas.width / 2,
  groundY: Math.round(canvas.height * 0.55),   // voorlopig gewoon iets dat klopt
  width: 277,
  onEvent: n => console.log('ravijn:', n)
});
```

4. In de renderlus, helemaal aan het eind:

```js
ravijnFx.update(dt);           // dt in seconden
ravijnFx.drawGap(ctx);
ravijnFx.drawOverlay(ctx);
```

5. Toets `O` roept `ravijnFx.start()` aan.

**Te checken:** toets indrukken, het ravijn scheurt open midden in beeld. Het zweeft nog
over alles heen en dat hoort zo. De shake doet nog niets.

---

# Blok 2: het zit in de wereld in plaats van erover (5 minuten)

Doel: het gat zit in de grond en schudt mee.

1. Verplaats `drawGap` naar direct na het tekenen van de grond, en `drawOverlay` naar na de
   personages.
2. Hang de shake erin. Als de game al camera shake heeft, tel `ravijnFx.shakeX` en
   `.shakeY` daarbij op. Zo niet, doe het met een translate om het hele wereldtekenen heen:

```js
ctx.save();
ctx.translate(Math.round(ravijnFx.shakeX), Math.round(ravijnFx.shakeY));
  // achtergrond, grond, drawGap, personages, drawOverlay
ctx.restore();
```

3. Zet `groundY` op de echte grondlijn van het level.

**Te checken:** het gat zit nu in de grond, Amir loopt er voorlangs, en het beeld schudt
tijdens het trillen en het openbreken.

---

# Blok 3: op een vaste plek in het level (5 minuten)

**Vraag eerst:** op welk level en op welke x wil Tom dit testen.

1. Zet `x` op een wereldcoordinaat in plaats van het midden van het scherm, en reken de
   camera-offset mee bij het tekenen.
2. Vul `stoneSpots` met een stuk of tien posities op de grond rond dat punt. Die steentjes
   liggen erbij, hoppen tijdens het trillen en vallen mee het gat in.

```js
stoneSpots: [{ x: 1180, y: 548 }, { x: 1226, y: 561 }, ...]
```

**Te checken:** naar die plek lopen, toets indrukken, het gat opent op de goede plek en de
steentjes springen op.

---

# Blok 4: de collider (5 minuten)

Doel: Amir kan er ook echt in vallen, en pas op het juiste moment.

- Zolang `ravijnFx.colliderActive` false is verandert er niets aan de grond.
- Zodra hij true wordt is het gat er echt, van `ravijnFx.gapLeft` tot `ravijnFx.gapRight`.
- Nooit eerder omzetten. Anders zakt Amir er doorheen terwijl de grond visueel nog dichtligt.

**Vraag hierbij:** is de val dodelijk zoals bij een gewone pit, of is dit juist de doorgang
naar het ondergrondse deel. En wat gebeurt er als Amir precies op de scheurende grond staat.

**Te checken:** tijdens de barst kun je er nog overheen lopen, daarna val je erin.

---

# Blok 5: de echte trigger (5 minuten)

**Vraag eerst:** hoe het symbool en de speerworp nu werken, en of het ook als scripted
level-event aanroepbaar moet zijn.

Vervang de testtoets door de echte trigger: de speer raakt het symbool, dus `start()`.
Voor een level dat al open begint is er `openInstantly()`. Om alles terug te zetten
`reset()`.

**Te checken:** speer werpen, raak is openscheuren, mis is niets.

---

# Blok 6: geluid en mobiel (5 minuten)

1. Geluidsevents inhangen. De module roept `onEvent(naam)` aan:

| event | wanneer |
|---|---|
| `onTremorStart` | het trillen begint |
| `onCrackStep` | de barst kruipt een stuk vooruit, negen keer, losse kraakjes |
| `onCrackSnap` | de barst schiet door, op 34 procent |
| `onSilence` | begin van de stilte |
| `onBreak` | het breekmoment, de dreun |
| `onSettle` | het gat is open, naruisend zand |

Tom maakt de geluiden zelf, zet er voorlopig lege haakjes neer.

2. `quality: isMobile ? 0.5 : 1` meegeven. Bij 0,5 halveren alle spawn-aantallen. Er zit al
   een harde limiet van 220 wolken tegelijk in `RavijnEffect.CFG.maxParticles`.

**Te checken:** op de iPhone in landscape moet het effect de framerate niet laten inzakken.

---

# Daarna, als Tom het wil

- Het gat koppelen aan een bestaande pit uit de level builder, zodat de pit dicht begint.
- Instelbaar maken in de builder: positie, breedte, wel of geen barst vooraf.
- Steentjes automatisch plaatsen in plaats van met de hand.
- Amir laten wankelen zolang de shake loopt.
- Het stof de windrichting meegeven die al voor de vegetatie gebruikt wordt. Nu waait de
  wolk naar twee kanten tegelijk, wat symmetrisch oogt. Dit is de enige inhoudelijke
  verbetering die nog openstaat.

---

## Instelknoppen

Bovenin `ravijn-effect.js` staan `PHASES`, `CFG` en `DUST`.

| wat | waar | nu |
|---|---|---|
| duur van de fasen in seconden | `PHASES` | tremor 0,50 / barst 0,93 / stilte 0,16 / openen 1,20 / uitdempen 1,07 |
| hoeveel stof | `DUST.*.rate` en `.burst` | pluim 15 per frame, burst 34 |
| dekking van het stof | `DUST.*.alpha` | 0,26 tot 0,33 |
| sterkte van de shake | `CFG.shakeOpen` | 10,5 px op het hoogtepunt |
| diepte in het gat | `CFG.depthNear` / `depthFar` | 0,10 blijvend, 0,58 extra tijdens het openen |
| hoeveel wand zijn vorm houdt | `CFG.edgeBand` | 60 px per kant |

Het gat schaalt mee met `width`. Bij een breder gat worden de barst en het openen
automatisch langer en wordt het midden van de wand aangevuld met gespiegelde herhaling. De
bovenrand komt daarbij uit een stuk zonder graspollen, anders zie je dezelfde pol vijf keer
op een rij.

## Twee dingen niet weghalen

**De stilte.** Na de barst staat 0,16 seconde alles volledig stil, geen shake en geen stof.
Die pauze maakt de klap erna twee keer zo hard.

**Het openen is vloeiend.** Traag op gang, snelst in het midden, dempt uit. Een schokkerige
versie met hitstop is geprobeerd en afgekeurd.

## Wat je niet moet doen

- Geen nieuwe art genereren. De wand, de steentjes en al het stof zitten erin of worden in
  code getekend.
- Het ravijn niet horizontaal samenknijpen of uitrekken. De twee wanden schuiven uit elkaar
  en houden hun vorm.
- Geen canvas-blur per frame. De wolkjes zijn eenmalig bij het laden gerenderd als zachte
  radiale verlopen, juist om dat te vermijden.
