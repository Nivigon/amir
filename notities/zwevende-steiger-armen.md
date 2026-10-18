# Transfer: zwevende steiger, gedragen door een stenen arm en hand

Dit is een overdrachtsdocument voor een andere cloud-sessie (met de Grok Imagine
skill). Het vat samen wat we hebben besloten, wat er al in de engine staat, en
welke assets er in Grok gemaakt moeten worden, met de prompts erbij.

Repo: `nivigon/amir`. Branch met de proef: `claude/wizardly-hypatia-0a7jp0`.
Taal: Nederlands, geen em-dashes (projectregel en persoonlijke voorkeur).

## Het idee

Een beloopbare, zwevende steiger (een hoger stuk grond om op te vechten), die niet
op een rechte pilaar rust maar **opgetild wordt door een stenen arm met een hand**.
De pilaar erachter is de arm, een tussenstuk is de pols/onderarm, en een hand grijpt
het platform aan de voorkant en houdt het omhoog. Het mag iets onnatuurlijks hebben,
maar het moet **natuurlijk ogen**, niet als een cartoon-hand.

De truc om het natuurlijk te laten ogen (pareidolia): geen letterlijke hand, maar
**verweerde rots die een hand/arm suggereert**, en dat met licht, schaduw, vaagheid,
waas en deels achter de grond/het platform laten wegzakken. Van dichtbij en scherp is
het een hand, half in schaduw en wazig leest het als een natuurlijke rotsformatie die
toevallig grijpt.

## Besliste ontwerpkeuzes (uitkomst van de verkenning)

- **Het dek is een `zwevers`-laag** (zwevende savannelaag). De botsing is al opgelost:
  je loopt eronderdoor (`onder >= CHAR_H`), landt erbovenop, stoot je hoofd van onderaf.
  Zie CLAUDE.md, "zwevende savannelaag".
- **De steun leest als "ver"**: hij staat achter de voorste grond (voet valt weg achter
  de grondband) en krijgt waas, zodat hij terugwijkt. Niet in Amirs vlak (anders een
  halfdoorzichtige "ghost" over zijn benen).
- **De steun is een arm + hand die tilt**, geen rechte pilaar. Het dek wordt getild,
  niet gedragen.
- **Natuurlijk maken in de engine**: belichte voorkant + donkere, koele, terugwijkende
  flank (volume); waas die naar de uiteindes toeneemt (vingers/arm zakken weg); voet
  achter de voorste grond; hand overlapt het dek net, zodat het "vastgepakt" lijkt;
  zelfde gesteente als de rest.

## Wat er al in de engine staat (proef, op de branch)

Alleen additief, geen enkel echt level aangeraakt. Nog geen sandbox-knop.

- `design/rotswand_pilaar.png`: de pilaar, schoon uitgeknipt uit een Grok-render
  (witte achtergrond weg op helderheid).
- `zweefSteun(z, groundY, scale, cx)`: tekent de steunpilaar achter een zwevende laag,
  met een waas-fade naar onderen en een lichte waas over het geheel. Aangeroepen in
  `scene()` vlak voor de grondband (dus achter de voorste grond), voor elke zwever met
  `z.steun && z.h >= 0`.
- Veld `steun` op een zwever loopt mee door `readLevel` en `syncLevel`.
- Checks gedraaid: `levelcheck.py` 0 fouten, `bouwertest.js` 0 met verlies,
  `offline-assets.json` bijgewerkt.

Dit wordt uitgebreid zodra de arm/hand-assets er zijn: de rechte pilaar wordt vervangen
of aangevuld door de arm-en-hand, met de licht/waas-behandeling hierboven.

## Assets die in Grok gemaakt moeten worden

Een klein setje: een paar armen en een paar handen, zodat ze afgewisseld kunnen worden
en niet overal dezelfde vorm staat.

**Stijl-referentie** (zit in de repo): `design/rotswand_zuilen.jpg` (of
`design/rotswand_spits.jpg`, `design/rotswand_pieken.jpg`), en de al gemaakte
`design/rotswand_pilaar.png`. Zelfde handgetekende, gefacetteerde, warm grijsbruine
rots met donkere kieren en lichte tan-facetten.

**Harde eisen voor elke plaat** (anders past hij niet in het spel):
- Zij-aanzicht, vlak (geen perspectief/kanteling).
- **Egale witte achtergrond (#FFFFFF, geen gradient)**: het spel knipt wit weg
  (`witKnip`). Een grijs verloop geeft een halo.
- Warm grijsbruin gefacetteerd gesteente, donkere kieren, tan highlights, los puin aan
  de voet mag.
- **Verweerd/natuurlijk dat een hand/arm suggereert, geen gladde cartoon-hand.**
- Vraag per prompt 3 tot 4 varianten.
- Verhouding: armen staand, handen breder/vierkant.

### Prompts

```
1) HAND, grijpend van onderaf:
A weathered rock formation shaped like a giant stone hand, side profile view, flat
side-on, pure flat white background. Hand-painted low-poly faceted stone, warm
grey-brown with tan highlights and dark crevices, same style as the reference.
Thick eroded stone fingers curling UPWARD as if cupping and lifting something above
it, like a palm holding up a slab. Not a cartoon hand: craggy, cracked, natural rock
that only suggests a hand. Loose rubble at the wrist base. Clean game-asset sprite.

2) HAND, over een rand grijpend:
Same style and background. A giant stone hand/claw seen from the side, thick eroded
rock fingers curling DOWN and OVER a ledge edge as if gripping the front lip of a
platform from above. Weathered, cracked natural rock that only suggests fingers.

3) ARM, oprijzend en buigend:
Same style and background. A rising rock column that bends forward like a flexed
stone arm (an elbow), side profile, tapering, warm grey-brown faceted stone, dark
crevices, rubble at the base. Natural weathered rock that suggests an arm reaching up.

4) ARM, rechter variant:
Same style and background. A tall slightly leaning rock pillar like a straight stone
forearm, side profile, faceted weathered stone, for a second support so they are not
identical.
```

## Hoe de assets in de engine komen (integratieplan)

1. Witte achtergrond wegknippen (zoals bij `rotswand_pilaar.png`): flood-fill vanaf de
   rand op helderheid > ~200, dan bijsnijden. Opslaan in `design/`.
2. Wereld-vast tekenen achter de voorste grond (in `scene()`, zoals `zweefSteun` nu),
   zodat de voet achter de grond wegvalt.
3. Volume: belichte voorkant + een tweede, donkere, koele, iets verschoven kopie als
   terugwijkende flank; zachte schaduw-overgang ertussen.
4. Waas naar de uiteindes (vingers/arm) zodat ze wegzakken in de verte.
5. De hand net laten overlappen met de voorrand van het dek, zodat het "vastgepakt"
   lijkt. Het dek zelf blijft de engine-laag (beloopbaar), getekend over de steun heen.
6. Assetregels na nieuwe plaatjes: `python3 tools/gen-klein.py` en
   `python3 tools/gen-offline-manifest.py`. Na wijziging aan `readLevel`/`syncLevel`:
   `tools/bouwertest.js`. Levels nakijken: `python3 tools/levelcheck.py`.

## Nog open (beslissen in de andere sessie of hier)

1. **Opstelling**:
   - (a) zijwaartse reik: arm links/achter, onderarm reikt opzij naar een hand die het
     platform verderop grijpt (dramatischer), of
   - (b) grijp bovenop: arm recht omhoog, hand krult bovenaan over de voorrand van het
     platform (compacter, leest sneller als "draagt").
2. Hoeveel varianten van arm en hand.
3. Arm uit het bestaande `rotswand_pilaar.png`-steen, of een eigen arm-plaat.
4. Diepte/donkerte van de terugwijkende flank: subtiel of sterk.

## Verwijzingen in CLAUDE.md

- "zwevende savannelaag" (`ZWEEF`, `zweefList`, `savanneLaag` met `floating`).
- "de voorgrond hoort bij elk level", "een level donker maken" (licht/waas: `licht`,
  `dim`, `drawWaas`).
- Regel 1 (echte episodes met rust), regel 2 (nieuw werk in de sandbox), regel 4
  (aansluiten op wat er is), regel 5 (Nederlands, geen em-dashes), regel 6
  (`claude/*`-branch).
