# De speervolgorde: speersoorten in de inventory

Uitgedacht met de opdrachtgever op 22 november 2026 en dezelfde nacht gebouwd. Het bouwt voort op de reserve-speren op de
rug (`RUG`, zie `notities/rug-speren.md`), de inventory (`notities/gif.md`) en de Pathfinder Spear (`notities/speer.md`).

## Besloten

- **Meerdere speren, elk met een soort**, ook meerdere van dezelfde soort.
- **Max 2 mee**: 1 in de hand en 1 op de rug (`RUG_STANDAARD`). Een extra plek is te koop (Extra spear slot in Co-op) of
  komt uit een talent (Third Spear van Mkuki).
- **Volgorde in de inventory.** De hand pakt altijd de hoogste soort uit de volgorde die je bij je hebt; de rest hangt op de rug.
- **Een speer houdt zijn soort.** Gooi je hem, dan ligt hij waar hij landt en schuift de volgende in je hand. Raap je hem op,
  dan komt hij terug op zijn plek in de volgorde.
- **Automatisch wisselen, plus de wisselknop Z.**
- **Zichtbaar op de rug** op een vaste plek per animatie uit de animeer tool, de speren gestapeld met de punten zichtbaar,
  geen echte koker. Alle speersoorten dezelfde maat. (Nog niet gebouwd, zie hieronder.)
- **Co-op: het is jouw speer.** Alleen de eigenaar raapt hem op.

## Hoe het werkt (gebouwd)

Kop in de HTML: `// ---- de speervolgorde: ...`, direct na `rugUpdate`.

- **De soort** zit al op elke speer, in het veld van het vaantje: `speerBlauw` (de hand), `rugSperen[].blauw`, `jav.blauw`,
  `losseSperen[].blauw`. `speerSoortVan` maakt er een soort van voor de volgorde (de drie standen van de oude speer zijn
  samen `oud`); `speerNaam` geeft de Engelse naam (`SPEER_SOORTEN[..].en`).
- **De volgorde** is `speerVolgorde`, standaard `pathfinder`, `standaard`, `geel`, `blauw`, `oud`. Een soort die er niet in
  staat komt achteraan; gelijke soorten houden hun plek (`speerRang`, `rugSort`). Hij geldt voor de hele sessie.
- **Vanzelf de beste in je hand** (`speerSorteer`): na oprapen in de hand (`losTrek`), een speer erbij op de rug (`rugErbij`:
  oprapen, het rek, een skelet, de winkel), een nieuwe Pathfinder (`pfStap`) of een nieuwe volgorde zet `speerOrdeVuil`, en
  `rugUpdate` ruilt dan de hand met de beste van de rug, zodra Amir vrij is (`speerWisselMag`: geen steek, worp, zwaai, trek
  of stofveeg). Met een stofwolkje en de melding "Pathfinder Spear in your hand".
- **Na een worp** trekt `rugTrekKlaar` de beste van de rug, en de tweede speer (`dubbelStart`) ook (`rugSort` voor de `shift`).
- **Z** (`speerWissel`): de speer in je hand gaat achteraan op je rug, de voorste van je rug komt in je hand, zodat je kiest
  welke je gooit. Dat blijft zo tot je weer iets opraapt (dan sorteert hij weer). Niet met de stokken. Op de telefoon is er
  nog geen knop. De winkel en de inventory leggen Z uit (`SPEER_Z_UITLEG`).
- **Het speervak** (23-11-2026, op verzoek; `SPVAK`, `spvakHud`, `spvakNaam`, `speerIkoon`): op een laptop links van de
  actiebalk een vak met de kop van de speer in je hand (toets Z) en klein ernaast de volgende van je rug. Bij een wissel
  gloeit het vak kort op en staat de naam van de nieuwe speer ongeveer een seconde klein net boven het vak, dan vervaagt hij;
  geen melding midden in beeld meer (op de telefoon nog wel de flashHint). Het icoon is de voorste helft van de speer, schuin,
  een keer per soort gebakken.
- **De inventory (I)**: bovenaan een rij met je speren (`invSperenToon`), de hand eerst en dan de rug. Een klik toont in het
  zijpaneel de naam, bij de Pathfinder de sfeertekst, wat hij doet, en **Hold first** (`speerVoorop`: die soort bovenaan de
  volgorde, en meteen in je hand, want het spel staat stil).
- **De Pathfinder als bezit**: `koop.pathfinder` telt hoeveel je er kocht (een per speerplek, `pfAantal`). `pfStap` maakt
  zoveel van de gewone speren die je draagt Pathfinder-speren als je er bezit min wat er al is (`pfTel`: hand, rug, in de
  lucht, los op de grond). Zo ben je hem nooit echt kwijt: weg in een rivier of na een revive komt hij terug op de
  eerstvolgende gewone speer die je draagt.
- **Sandbox**: Speer en spullen, Gif, **Pathfinder Spear** geeft er een (de andere blijft gewoon), I en Z om te proberen.

## Nog te doen

- **De rug per animatie**: de plek uit de animeer tool in plaats van `rugSpeerTeken` in schermruimte.
- **In de hand** zit nog de speer uit de sprites, dus de Pathfinder ziet er in Amirs hand nog gewoon uit, tot de speer los
  over de animaties komt.
- **Teamgenoten** zien je rugsperen nog niet.
- **Een Z-knop op de telefoon.**

## Mogelijke ideeën (in de gaten houden, niet bouwen)

- **Oppaktijd per speersoort.** Een zware of speciale speer kost langer om op te rapen (E vasthouden met een ringetje dat
  volloopt, afgebroken als je geraakt wordt). Zo wordt elke speer een afweging, ook in levels of groepen vijanden waar je
  bijna alleen maar kunt gooien en geen tijd hebt om op te rapen.
- **Lege handen.** Zonder speer kan Amir nu niets; voorlopig is de oplossing: zorg dat je een speer krijgt. Later kan er
  iets bij, zoals een zwakke trap of duw die ruimte maakt om te rapen, of de dolk.
- **Kwijtraken of kapotgaan.** Nu kom je een Pathfinder nooit kwijt (zie boven). Een idee is een kans per speersoort dat hij
  breekt, als tegenwicht voor wat hij oplevert (de oude speer breekt nu al na drie keer, `OUDE_SPEER`).
- **Co-op: elkaars speren gebruiken.** Elkaars speer oprapen en gooien zou ook vet kunnen zijn; eventueel als regel die
  de host in de lobby aan of uit zet.
