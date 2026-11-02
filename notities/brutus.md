# Brutus (in beeld: Nyundo), de baas van het plein

Brutus is de codenaam; in het spel heet hij **Nyundo** (Swahili: de hamer, `BRU.naam`). Een enorme
shirtloze bruut met een stekelknots op zijn schouder. Hij is een baas (regel 12): Tom heeft hem voor
**Stad 6: Het plein** gevraagd. Code: de sectie `// ---- Brutus: de eerste baas` (`BRU`, `makeBrutus`,
`updateBrutus`, `hitBrutus`, `bruTeken`, `bruBalkTeken`, `bruKlem`) en het tekenblok
`// ---- Brutus, de baas van het plein` in de lus.

## Het gevecht
- Amir begint binnen op het plein (`start: -3000`), de ingang achter hem is dicht. Brutus staat aan de
  overkant zwaar te ademen (`wacht`) tot Amir een stap zet.
- **Storm**: hij rent op Amir af (`BRU.stormV`), met op twee stormframes (`BRU.stapFrames`) het stapgeluid,
  een kleine schok en stof. Loopt hij Amir omver, dan kost dat een leven.
- **Zwaai**: vlak voor Amir (`BRU.aanval`) stopt hij. Eerst de tell (zwaaiframes 0 t/m 2, `BRU.tell`,
  ingedraaid en even vast), dan de zijwaartse zwaai; de knots raakt in frames `BRU.raakVan` t/m
  `BRU.raakTot`, alleen voor hem en tot `BRU.raakHoog` boven de grond. Ontwijken: terugstappen, of
  erdoorheen rennen (hij zwaait alleen naar voren). Daarna blijft hij in zijn eindpose staan (`BRU.eind`):
  het raam voor ongeveer twee treffers. Staat Amir dan nog dichtbij (`BRU.opnieuw`), dan zwaait hij meteen
  weer met een kortere tell (`BRU.tellOpnieuw`); anders ademt hij even (`BRU.adem`) en stormt opnieuw.
- **Woede**: met `BRU.woedeHp` (6) levens of minder gaan de tell, de zwaai en het raam sneller
  (`BRU.woede`): dan red je nog maar één treffer.
  Je ziet het aan hem (`BRU.gloed`, `bruGloedStap`): bij de omslag een flits, een schok en een korte hitstop, daarna
  gloeit hij rood op het ritme van zijn adem (`bruPuls`). Zijn eigen kleuren worden met rood vermenigvuldigd zodat de
  lijnen blijven (`bruGloedBeeld`), met een rode gloed om zijn silhouet (`shadowBlur`), een rode plas licht op de vloer
  (`bruVloerGloed`) en vonken die van zijn schouders opstijgen (`bruVonkTeken`). Bij zijn dood dooft het weer.
- Een treffer van Brutus kost Amir één leven en Amir vliegt weg (`BRU.duw`).
- **Zestien treffers** (`BRU.hp`): de steek, de lage zwaai en de worp tellen elk één (de worp valt daarna
  naast hem neer, zoals bij elke vijand). Het mes doet niets. Na een treffer is hij `BRU.inv` s onraakbaar.
- De balk onderaan het scherm: zijn naam en zestien vakjes, rood vanaf de woede.
- **Dood**: het doodsgeluid, hij kantelt in code achterover (`s.val`), ploft neer (`sounds/bavland.mp3`, schok) in
  een grote stofwolk over zijn hele lengte (`bruDoodStof`), en vaagt daaronder weg (`s.weg`). De poort met `uit: true` gaat open en `bossBlocking` laat het level weer
  uitspelen. Een echte dood-animatie komt later.
- Zolang hij leeft blijven Amir en Brutus tussen `brutus.van` en `brutus.tot` (`bruKlem`).
- **Bloed** (eerste versie, `BRU.bloed`, `bruBloedRaak`): elke treffer geeft een spat druppels uit zijn borst, naar de kant
  waar de klap vandaan kwam, die op de grond blijven liggen en vervagen (de druppels van de zweepman: `zwmDruppelStap`,
  `zwmDruppelTeken`). Op treffer 2, 5, 8, 11 en 14 (`sneeOp`) komt er een snee op zijn lijf, een decal uit
  `design/bloed/snedes` op een vaste plek op zijn borst en buik (`snedes`), geknipt op zijn silhouet (`zwmSneeLaag`).
  Bij een draai of de zwaai valt een snee soms (deels) buiten zijn lijf en is dan niet te zien. Bij zijn dood speelt
  ook het bloedgeluid (`bloedSpeel`).
- **Speertreffer**: `sounds/brutus_speerraak.mp3` op elke treffer (een tijdelijk, in ffmpeg gemaakt geluid: een doffe
  dreun met een korte natte klap; vervang het bestand met dezelfde naam door een echt geluid).

- **Stof**: Brutus heeft zijn eigen stofdeeltjes (`s.stof`, `bruStofStap`, `bruStofTeken`, met het wolkje van het spel):
  bij elke stap in de storm schieten er wolken omhoog en achter hem weg (`BRU.stof`).
- **Achtervolgen**: rent Amir in het raam na de zwaai verder weg dan `BRU.opnieuw` x `BRU.wegVlucht`, dan breekt hij het
  raam af, kijkt kort om en stormt erachteraan; na een zwaai zonder Amir dichtbij ademt hij maar `BRU.adem` (0,5 s).
- **Maat en voeten**: de zwaaiframes staan in brutus.json 1,1 keer groter dan de bron (anders oogde hij in de zwaai
  kleiner), en hij zakt `BRU.zak` grote-set-pixels in de vloer zodat zijn voorste voet op de lijn van Amir staat.

## Het level
Het laadscherm van een level met `brutus` is `design/menu/laadscherm_brutus.jpg` (Amir tegenover Nyundo in de poort,
de klasse `brutus` op `#laad`, in `laadPoort`); het gaat boven het stadsbeeld.
`brutus: { x, van, tot }` in de leveldefinitie (ook door `readLevel`), en bij de pleinpoorten
`uit: true` voor elke uitgang. Stad 6 is een dicht plein: aan beide kanten een poort met een hek, geen fakkels.
Amir komt niet verder dan onder de boog (`pleinKlem`). Ligt Brutus, dan takelen na `BRU.hekWacht` beide hekken op
in `BRU.hekDuur` (`pleinHekStap`, het takelgeluid, stof bij de voet), en onder een open poort staat het bordje
"Het plein verlaten?  E": E speelt het level uit (`pleinPoortBij`, `pleinUitgang`). `levelcheck.py` kent dit als einde.
Sandbox: Vijanden, rij **Brutus (baas)**: zonder wachten, meteen stormen.

## Bestanden
- `enemies/brutus/brutus.json` met per beweging (`idle`, `storm`, `zwaai`) per frame `{src, dx, dy, w, h, ms}`
  t.o.v. het anker (midden van het lijf) en de grondlijn, in pixels van de grote set (figuur ~340 hoog van
  haar tot voet), naar links kijkend. `klein/enemies/brutus/` dezelfde frames op halve grootte.
- Bron: Grok-clips (idle_breathign1, RC2, hitnice), gekeyd en per clip op één schaal en één verschuiving
  gezet (animeer tool Bruut), daarna omgekleurd: broek zwart, sjerp bloedrood, windsels ijzer; het rode
  haar bleef. De idle is één inademing heen en terug; in het spel volgt hij het ademgeluid (`BRU.ademPeriode`).
- Geluiden: `sounds/brutus_adem.mp3` (loopt zolang hij staat te ademen), `brutus_stap.mp3`,
  `brutus_zwaai.mp3` (start op zwaaiframe `BRU.zwaaiGeluid`, de zoef valt op de treffer),
  `brutus_geraakt.mp3`, `brutus_dood.mp3`.
