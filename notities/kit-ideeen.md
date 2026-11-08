# Ideeën voor de kit van Amir

Nog niets hiervan is gebouwd. Dit is de stand van het gesprek over wat Amir mist, vooral in gevechten
met meerdere bandieten: nu is de truc door ze heen rennen, een treffer van achteren en omdraaien, en dat
voelt lame. De rol-worp als finisher voelt juist goed.

## Hoe we indelen

- **Basis kit**: alles waar een level of vijand op moet kunnen rekenen. Test levels en de speelrobot spelen
  zonder tribe, dus wat daar moet werken hoort in de basis.
- **Tribe-ability**: wat je meteen krijgt als je de tribe kiest en wat je speelstijl bepaalt (zoals de woede
  bij Bhubesi, G).
- **Talents**: maken de ability of de basis sterker of geven een andere draai. Een talent mag bij twee tribes
  passen.
- De tribes blijven fysiek en geloofwaardig: geen magie bij Mkuki (terugroepen van de speer viel daarom af).

## Nu aan de beurt: stof in de ogen

**Prototype gebouwd (sandbox).** `STOF`, `stofStart`, `stofWerp`, `stofRaak`, `stofDwaal`, `stofTeken`. Onder Speer en
spullen de knop **Stof (X)**; staat hij aan, dan doet X de stofveeg. De beweging is voorlopig de lage zwaai (`swFrame`, met
`stofT >= 0` raakt de zwaaibox dan niets); op `STOF.werpFrame` vliegt het stof (`puffWorld`). Een bandiet voor Amir, binnen
`STOF.bereik`, op zijn niveau (`banZelfdeHoogte`) en met zijn gezicht naar Amir krijgt `s.verblind = STOF.duur`: hij wankelt
eerst weg van Amir en dwaalt dan heen en weer in de patrouillegang (`walk`) rond die plek, valt niet aan en werpt niet
(`updateBandiet` keert vroeg terug), met drie draaiende zandsterretjes boven zijn hoofd. De volgende treffer in
`hitBandiet` telt dubbel (met `critFx`) en maakt hem wakker; met twee levens is hij dan dood. Alleen de bandiet nog.
Komt de animatie, dan vervangt die de zwaai-frames in `stofStart` en kiest `STOF.werpFrame` het moment van het stof.

De opdrachtgever maakt de animatie: Amir sleept de punt van zijn speer van achter hem over de grond naar voren
en gooit stof (of gruis) naar de vijand.

- Werkt alleen als de vijand naar Amir kijkt (sluit aan op `zicht`, de halve cirkel voor hem).
- Verblind: hij loopt een stukje heen en weer, met een symbooltje boven zijn hoofd, en ziet Amir even niet.
- Kwetsbaar: een speertreffer telt dubbel (het mechanisme van True Flight, `critPak`, ligt er al).
- Later: wie zo'n verblinde vijand aanvalt doet een vette move, bijvoorbeeld een spin strike die rondom raakt
  (ook achter je, dus een antwoord op een groep). Daar zijn nieuwe frames voor nodig.
- Aandachtspunten: slangen, schorpioen en fosforslang niet verblinden (hooguit de hyena), een schildbandiet
  met het schild omhoog vangt het stof, een baas kort of niet. Het stof volgt de grond (zand, gruis in de
  stad, sneeuw in de winter). De beweging lijkt op de lage zwaai, die al zand wegveegt bij een verstopt zegel.
- Bij welke tribe hij hoort is nog open.

## Basis: de bandiet draait mee

Rent Amir langs of door een bandiet, dan draait die mee met een backhand-houw of stapt opzij. Door een groep
heen rennen kan dan nog, maar alleen met timing. Bij twee of meer kan er taakverdeling bij: een stormt, de
ander houdt afstand en werpt zijn dolk.

## Mkuki (de speer): snel, vluchtig, op afstand

- **Een speer extra op de rug**: 2 in plaats van 1 (`RUG_MAX`), dus 3 worpen voor je melee-loos bent.
- **De dubbele worp** (de tribe-ability): F nog eens vlak na het loslaten (rond 0,3 s) en Amir grijpt in een
  beweging over zijn schouder en gooit meteen een tweede, vlak en snel, zonder opspannen. Past op de beat
  `RUG.trek` / `rugTrekKlaar`. Een bandiet (twee levens) gaat er van afstand mee neer, maar dan liggen er
  twee speren in het veld. Eerste versie: de gewone worp versneld, echte frames later.
- Talents eromheen: Quick Hand en True Flight passen al; vastpinnen of doorboren (de speer pint een vijand
  tegen een muur of gevel en blijft hangen, of gaat door twee op een rij heen; bouwt op de speer in de borst
  van de kruisboogbandiet, `krbSpeerVolg`); de dubbele worp ook vanuit de rol.

## Bhubesi (de leeuw): Stilte voor de storm

Laag en stil blijven (bukken, stilstaan) laadt een burst op, met een cap: harder slaan, of sneller en hoger.
Liever voor de volgende paar aanvallen dan een paar seconden. Per talent een effect, via de T-splitsing.
Zichtbaar en hoorbaar laden (stof dat om hem heen trekt, een hartslag). Kan de woede voeden. Past bij de
loerende leeuw van Lion's Patience, en bukken is al het antwoord op de dolk van de bandiet.

## Later

- **Spirit guide**: speer in de grond, ogen dicht, naar de camera, en een geest van Amir doet een paar seconden
  zijn aanvallen na (gespiegeld achter hem, of met een kleine vertraging als echo). Kan niet dood. Voelt als de
  kern van een eigen, nieuwe tribe.
- **Neerhalende sweep**: de lage zwaai legt sommige vijanden op de grond. Heeft een opstaan-animatie nodig;
  om te proeven kan het begin van de doodset van de bandiet omgekeerd.
- **Verdoven** met de rol-worp, als talent (een splitsing naast doorboren).
- Afgevallen: een parry met de speer (te dicht op het schild), terugroepen van de speer (magie).
