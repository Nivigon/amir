# Bloed op hout: van de plankrand druppelen

Bloed dat landt op een houten vloer met lucht eronder blijft niet alleen liggen. Een plas, of een paar druppels bij
elkaar, trekt als een tong over de planken naar de voorrand (de lip van de planken, `BLOED_RAND.lip` in de
galerijplaat), en daar komt een kort vegje over de rand met een druppel eraan. Die groeit (`hang`), laat los en valt
voor de balk langs naar de vloer eronder, waar hij een vlekje achterlaat. De balk zelf blijft schoon: dat was de keuze
van de opdrachtgever (niet een stroompje over de hele balk, maar van de rand af).

## Waar

- **Hout**: een galerij (`stadGalerijMaten`), een trapbalkon (`stadTrapPlats`) en de brug boven het water
  (`wateren` met `k: 'rivier', brug: true`, alleen boven de rivier zelf, niet op de oevers). Dat beslist `bloedHoutBij`.
- **Geen hout**: een dak van leem, de straat, een takeldek. Daar blijft het bloed gewoon liggen.
- **Onder de brug** ligt geen wateroppervlak: de rivier valt vooraan over de rand. Een druppel valt daar in de
  waterval en vervaagt onderweg (`inWater`). Geen ringetje, dat stond in de eerste mockup maar klopt niet met het beeld.

## Wie het meldt (`bloedRandMeld`)

Alleen doden waar al bloed in de animatie zit (besproken met de opdrachtgever):

- **De sluipdood van de bandiet** (`SNKD`): elke druppel die landt, en de plas zodra hij een seconde groeit
  (`plas: true`, druppelt meteen). Leeft zo lang als het lijk (`snkdBloedOp`).
- **De executie van de schildbandiet**, ook de stokexecutie (`exeDruppelStap`): de druppels die liggen. Leeft zo lang
  als het lijk.
- **De zweepman** (`zwmDruppelStap`): de spat en het nadruppelen na een treffer, 9 s (`ZWM_BLOED.lig`). Er moeten een
  paar druppels bij elkaar liggen (`drempel`). Nyundo gebruikt dezelfde druppels, maar staat nooit op hout.

Niet: de gewone dood van bandiet, kruisboogbandiet, kooiman en meelman (geen bloed in de animatie), de slang (te klein,
3,8 s), gif, de lensspat.

## Regels

- Bloed binnen `samen` (34 px) op dezelfde vloer is een plek; de massa is de som van de stralen.
- Een plek druppelt vanaf `drempel` (10), of meteen als het een plas is. Losse druppels liggen eerst `zak` (0,6 s),
  dan wint de grootste.
- **Hooguit `perBron` (2) druipende plekken per vijand.** Zonder die grens gaf een executie tien plekken over 400 px:
  een gordijn van druppels.
- Eerst snel (`eerste`, `tussen`), elke druppel `trager` (1,35 keer), en na `duur` (7 s) geen nieuwe meer.
- Hooguit `max` (20) plekken tegelijk; bij een nieuw level gaat alles weg (`setLevel`).

## Ook gerepareerd

De druppels van de zweepman, de executie en de slang landden op hun eigen voetlijn. Vlogen ze over de rand van een
galerij, dan bleven ze in de lucht hangen. Nu landen ze op `vloerBij` en vallen ze over een rand door naar de vloer
eronder (`d.bodem`, `slangVloerDy`).

## Tekenen en stap

`bloedRandStap(dt)` naast `waterStap`; `bloedRandTeken` na `brugTeken`, dus na de galerijen en de brug en voor de
vijanden (het lijk ligt over de tong). De tong en het vegje met `multiply`, zodat de nerf erdoor blijft.

## Sandbox

Onder de stad: **Zweepman op de galerij**, **Schildman op de galerij** (met Executie: altijd zie je het elke keer) en
**Bloed op de galerij** (een plas met een eigen vlek, op de brug als die in beeld staat). De sluipdood: **Bandiet op de
galerij** met de sluipaanval aan.
