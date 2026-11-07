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
- **Kap** (sinds 03-11-2026 zijn echte aanval, `BRU.kap`, beweging `kap` in brutus.json): vlak voor Amir remt hij
  uit de storm af (kapframes 0-6, start op stormframe 6), tilt de knots met twee handen hoog achter zijn hoofd
  (7-23) en houdt hem daar terwijl de bal omhoogkomt (24-41): samen de tell, met haatgezicht. Dan kapt hij hem in
  een keer voor zich in de grond (42-51, raak `BRU.kap.raakVan` t/m `raakTot`) en blijft voorovergebogen over de knots hangen: het raam (`BRU.kap.eind`, langer dan bij de zwaai).
  **De inslag** (`BRU.kap.inslag`, frame 52: het eerste frame waarin de bal echt op de grond ligt; op 51 hangt hij er nog
  boven, daar leek hij de grond te missen): `bruInslag` speelt `sounds/brutus_inslag.mp3` (de upload "raakt grond"),
  geeft een schok en stof waar de bal neerkomt (`kap.bal`: zoveel px van de voorkant van het frame), en staat Amir op de
  grond binnen `kap.schok.ver` van de bal of van zijn lijf en is hij niet zelf geraakt, dan zet de klap hem een klein
  stukje terug, weg van Nyundo (`kap.schok.duw` als `knock`, zo'n 60 wereld-px, geen schade; een opspannende worp vervalt,
  zoals bij de trilling van de kooiman). Wie springt op de inslag, schuift niet.
  Meteen opnieuw kappen gaat met een kortere tell (`BRU.kap.tellOpnieuw`). De zijwaartse zwaai (beweging `zwaai`)
  blijft in brutus.json voor de intimidatie (met de dozen, komt nog); `bruSlag()` kiest de kap als die er is.
  Bron: Grok-clip tophit1 (start RC2 frame 24, eind de kap-pose), keyed, bal hersteld waar hij boven uit beeld
  zwiepte (bron 133-138), bron 136 weggelaten, x1,142 op storm_06 geregistreerd en omgekleurd naar de speelkleuren.
- **Terugslag** (`BRU.terug`, beweging `terug`): staat Amir na de inslag van de kap achter hem (erdoorheen gelopen,
  binnen `BRU.terug.achter`), dan kijkt hij om, rukt de knots met een hand uit de grond en zwiept hem met een pas plat
  achter zich langs (raak `raakVan` t/m `raakTot`, het vak ligt achter hem); de knots komt hoog uit. Daarna staat hij
  naar Amir toe: zijn anker schuift `verplaatsing` (brutus.json) achter hem langs en `face` draait om (`bruTerugStap`);
  zijn lijf (de raakbox voor Amir) loopt tijdens de zwiep mee (`bruLijfDX`). Daarna kapt hij meteen weer als Amir dichtbij
  staat, anders ademt hij. Speelwijze: stap terug uit de kap en je hebt het raam; loop door hem heen en de terugslag
  volgt, tenzij je doorloopt tot buiten bereik; wie steeds terugstapt staat vanzelf tegen de wand en moet erdoorheen.
  Bron: Grok-clip bijna_of_goed_2 (begin het laatste kap-frame, tussen omkijken met een hand, eind de eindpose een pas
  verder), frames 1, 60-78 (omkijken) en 80-110, x1,264 op kap_54 geregistreerd, omgekleurd.
- **Sprong** (sinds 05-11-2026, `BRU.sprong`, bewegingen `sprong` en `landing` in brutus.json, `bruSprongStart`,
  `bruSprongStap`): een keer in de zoveel tijd (`eerste` s na het begin, daarna `elke` s; in de woede x `woede`), als
  Amir binnen `ver` x 1,15 staat. Vanuit het ademen, of uit de storm als Amir niet dichtbij is. Hij zakt in een lage
  afzet en blijft daar `tell` s zitten (het zand trilt), zwaait de knots als een molenwiek over zijn hoofd (sprongframes
  op `opMs`) en komt los op het eerste frame waarin Grok zijn voeten optilde (`los`); daar de afzet (`bruAfzet`: dreun,
  stofstoot, steentjes). In de lucht schuift hij in een boog (`hoog`, bovenop de frames) naar zijn doel en stuurt hij bij
  naar Amir tot hij bovenin hangt (`bruSprongDoel`: zo dat Amir tussen zijn lijf en de bal landt, `balVoor`, nooit verder dan
  `ver` en nooit achteruit). Sinds 07-11-2026 ligt de landingsplek vast zodra de boog `vastBij` (0,5, de top) voorbij is
  (`sp.vast`, eerder `stuurTot: 99`, tot de landing): het zand trilt dan op de strook van zijn lijf tot de bal
  (`bruSprongVast`), en wie dan wegrent ontwijkt hem. Gemeten: bovenin wegrennen, sprintend of lopend, is veilig;
  blijven staan of pas bij de landing (`neer`) gaan is raak. Daarvoor kon je hem niet ontwijken: springen raakt
  sinds de zwaaicheck ook, en weglopen volgde hij tot het laatst. Bovenin hangt hij `hang` s. Op het landingframe waar zijn voeten weer staan (`neer`) een
  dreun en stof (`bruNeer`), en op het frame waar de bal de grond raakt de inslag (`bruSprongInslag`): de grootste
  stofwolk van het spel (een ring naar twee kanten, een hoge pluim die blijft hangen, een waas over de vloer), plavuizen
  die opspringen (`bruSteen`), een harde schok en hitstop. Staat Amir op de grond tussen zijn rug en net voorbij de bal,
  dan is dat de zwaarste klap van het gevecht: een leven, `duw` (2600) weg en `hurt` (0,6 s) uit zijn doen. Ook de knots op weg
  naar beneden raakt (sinds 06-11-2026, `bruSprongZwaaiRaak`, `balStraal`): van het landingframe na `neer` tot en met de
  inslag volgt de check de baan van de bal (`bal` in brutus.json, van het vorige naar het huidige frame, plus `balStraal`),
  tussen zijn lijf en net voorbij de bal. Wie daar in de lucht hangt, bijvoorbeeld omdat hij over de bal probeert te
  springen, krijgt dezelfde klap; vroeger telde alleen de inslag en kon je er doorheen springen. Gemeten: op 120, 250 en
  400 boven de grond raak (frame 11), op 550 ben je erboven. Daarna hangt
  hij `eind` s over de knots (het raam) en komt overeind: zijn anker schuift `verplaatsing` (landing in brutus.json) naar
  de heup van de eindpose.
  Speelwijze: wie blijft staan wordt geraakt; wie wegrent zodra hij bovenin hangt en het zand trilt, ontwijkt hem. **Golven** (`BRU.sprong.golf`, `bruGolfStap`, `bruGolfTeken`): uit de inslag
  rolt een bult naar links en een naar rechts (`v`), tot de wand van de arena of `ver`. De vloer golft echt: de strook
  onder de grondlijn van het al getekende beeld wordt een keer gekopieerd en in smalle kolommen opgetild (`bult`, `breed`;
  steil voorop, golvend erachter, met een donkere scheur eronder), met plavuizen en een lage stofmuur langs de weg. Gaat de
  voorkant over Amir heen terwijl hij lager staat dan `golf.hoog` (Amir-eenheden, net als `ph`), dan kost dat een half
  leven, verdooft het (`stun`) en duwt het hem mee. Springen op tijd of op de put staan (de rand is 0,47 Amir) is veilig.
  Sandbox: **Sprong nu** (`sbbrusprong`) naast de knop Brutus zet de timer op nul.
  **Schade in de vloer** (`BRU_SCHADE`, `bruSchadeErbij`, `bruSchadeStap`, `bruSchadeTeken`): waar de bal van de sprong
  neerkomt barst het plaveisel (een van de zware platen, `zwaar`), langs een golf om de `golfStap` px met kans `golfKans`
  een lichte plaat, en waar de kap inslaat (`bruInslag`) ook een lichte. Het blijft plat: Amir loopt er gewoon overheen,
  geen botsing en geen kuil (een krater waar je in vast komt te zitten is overwogen en voorlopig niet gedaan). De platen
  staan in de maat van `plein.png` (rij 0 op rij `top` van de vloertegel, `mid` het midden van de schade) en worden vlak
  voor Amir getekend, na de vloer, zodat hij erop staat; alleen op een strook grondSoort `plein` (`bruOpPlein`).
  De opspringende stenen zijn nu brokken uit `plein_brokken.png` (`bruBrokTeken`, `brokBreed`) met een schaduwtje op de
  vloer; een groot brok (straal vanaf `blijf`) blijft na de landing als puin liggen (`s.puin`). Hooguit `max` platen en
  `puinMax` brokken: komt er een bij, dan vervaagt de oudste in `vervaag` s. Bron: Grok-platen in `design/stad/bron/`
  (`plein_schade_grok.jpg`, vier platen gebarsten plaveisel, en `plein_brokken_grok.png`), verwerkt met
  `tools/plein_schade.py` (knipt het beschadigde stuk uit, rekent het om naar de maat en kleur van het plein, geeft het
  een grillige zachte rand en print de rechthoeken van de brokken; `--proef map` legt elke plaat op plein.png).
  Sandbox: **Vloer heel** (`sbbruheel`) haalt de platen en het puin weg.
  **De poorten trillen mee** (`BRU_SCHADE.poort`, `bruPoortStenen`): bij de inslag van de sprong vallen van elke pleinpoort
  binnen `ver` een handvol brokken (`n`) van ergens op de poort (`hoog`, deel van zijn hoogte), elk na een eigen `wacht`,
  met een wolkje waar hij loskomt en een sliert stof erachteraan. Slaat een golf tegen de muur van het plein (`van`/`tot`),
  dan vallen er `golfN` van de dichtstbijzijnde poort. Vallend krijgen ze een donkere rand (`st.val`, een schaduw), anders
  zie je ze niet tegen de leem; de grote blijven onder de poort liggen als puin.
  Bron: Grok-clips jump1 en landing1, gemaakt met begin- en eindframes uit drie sleutelhoudingen (de afzet, in de lucht
  en de inslag, image-to-image vanaf het basisbeeld en op één canvas gezet). `tools/brutus_sprong.py` keyt ze, kiest de
  frames (sprong: 0 en 14 t/m 65 per 3, landing: 0 t/m 16 per 2 en 17 t/m 22), zet beide op één schaal (x1,04, op de kop
  gemeten tegen idle_00) en één anker (de heup in de afzet), haalt de sprong van Grok eruit (veld `los`, de engine tilt
  hem) en kleurt om naar de speelkleuren. Magenta die Grok in snelle frames door de bal, de steel en de handen veegt
  wordt grijs (geen kleur van Nyundo heeft rood en blauw allebei boven groen), de bal blijft grijs ook als Grok hem
  blauw of groen maakte, en rood onder de sjerp is de broekrand (zwart).
- **Woede**: met `BRU.woedeHp` (6) levens of minder gaan de tell, de zwaai en het raam sneller
  (`BRU.woede`): dan red je nog maar één treffer.
  Je ziet het aan hem (`BRU.gloed`, `bruGloedStap`): bij de omslag een flits, een schok en een korte hitstop, daarna
  gloeit hij rood op het ritme van zijn adem (`bruPuls`). Zijn eigen kleuren worden met rood vermenigvuldigd zodat de
  lijnen blijven (`bruGloedBeeld`), met een rode gloed om zijn silhouet (`shadowBlur`), een rode plas licht op de vloer
  (`bruVloerGloed`) en vonken die van zijn schouders opstijgen (`bruVonkTeken`). Bij zijn dood dooft het weer.
- Een treffer van Brutus kost Amir één leven en Amir schiet een stuk weg (`BRU.duw`, 1500: zo'n 180 wereld-px), met
  een zware dreun (`sounds/brutus_raak.mp3`, gemengd in ffmpeg uit `kooihitground` en een lager gestemde `houtraak`;
  vervang het gerust door een echt geluid met dezelfde naam), een schok, een korte hitstop en stof: een wolk op de klap
  en een spoor achter zijn voeten zolang hij schuift (`bruRaakAmir`, `bruRaakSpoor`, `BRU.raakStof`). Alleen de klap die
  echt landt doet dit, niet elk beeld van de onkwetsbaarheid erna.
- **Nyundo: test** (pauze, Instellingen; alleen in een level of de sandbox met Nyundo): schuifjes voor de duur van de
  tell, de slag, het raam en de adem tussen de slagen (procenten van de standaard, met de duur in seconden erbij), en
  een vinkje Amir onsterfelijk (`BRU_TEST`, `bruTestToon`, in `onsterfelijk()`). De browser onthoudt de stand
  (`amir.nyundotest`); ben je tevreden, neem de getallen dan over in `BRU`.
- **Zestien treffers** (`BRU.hp`): de steek, de lage zwaai en de worp tellen elk één (de worp valt daarna
  naast hem neer, zoals bij elke vijand). Het mes doet niets. Na een treffer is hij `BRU.inv` s onraakbaar.
- De balk onderaan het scherm: zijn naam en zestien vakjes, rood vanaf de woede.
- **Dood** (`bruDoodStap`, `bruFinale`): op de laatste treffer staat de wereld stil voor Amir (hij kan niet lopen en niet
  geraakt worden) en draait Brutus zich naar hem toe. Dan drie Grok-sets uit brutus.json achter elkaar: `dreig` (hij heft
  zijn knots langzaam naar Amir, vertraagd afgespeeld), `drop` (zijn pols draait, de knots zakt; op het laatste frame staat
  de knots los op zijn bal en kantelt in code van hem weg om, `knots` in de json, `BRU.knotsLig`, met een kleine plof en stof;
  zo zwaar is hij dat hij bij de klap een stuk in de vloer zakt, `BRU.knotsZak`: wat onder de vloerlijn komt is weg, met een
  donkere deuk en een barst eronder)
  en `val` (het doodsgeluid, hij zakt op zijn knieen en valt voorover; op het frame met bron `BRU.valKlap` de plof, een
  schok en de grote stofwolk). Daarna blijft hij liggen (fase `lig`, over de knots heen), gaat de uitgang open en speelt
  "ta soul, rest". De val-frames zijn per frame op de grond gezet: Grok liet hem ruim 100 px boven de grond liggen. Grok liet hem ook
  groeien bij het knielen en liggen: de val-frames zijn per frame geschaald rond het anker (veld `schaal`: staand 1, geknield
  0,76, liggend 0,57), zodat hij liggend ongeveer zo lang is als hij staand hoog is. Liggend is hij
  nog wat lang (het eindbeeld van Grok was te groot); een betere ligpose en de speer-finisher (speer breken, schreeuw) komen later.
- **Zijn stem** (`BRU.spraak`, `bruZeg`, pauze en herstart via `bruSpraakStap`): na treffer `fase2Na` (6) staat de
  wereld stil (`bruVries`, dt 0 in de lus, Amir vast en onraakbaar) zolang `sounds/brutus_fase2.mp3` klinkt; het geluid
  is de klok, zonder geluid duurt het `vries` s (`bruVriesStap`). Op die treffer geen kreet. Bij de omslag naar zijn woede
  speelt `brutus_fase3.mp3` (over het gevecht heen, geen freeze). Bij zijn dood begint `brutus_dood.mp3` (zijn laatste
  woorden, 6,2 s) op de laatste treffer, en dreig en drop rekken samen tot `doodVal` (4,0 s): dan valt `val` in de stilte
  voor zijn laatste zin, en de klap op de grond (zo'n 1,8 s later) op zijn laatste zucht (5,7 s). Loopt de spraak achter,
  dan wacht hij in het laatste drop-beeld. Gemeten in Chromium: val op 4,04 s spraak, de plof op 5,82 s.
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

## De opening (`brutus: {intro: true}`, `BRU_INTRO`)
Stad 6 begint met een tussenstuk (`bruIntroBegin`, `bruIntroStap`, `bruIntroTeken`, `bruSluitStap`). Amir start net binnen de
rechterpoort (`start: -2500`); het hek daarvan staat open en valt na `sluitWacht` in `sluit` seconden dicht (het takelgeluid,
een klap, stof), pas als het laadscherm weg is. Nyundo staat bij de linkerluifel met zijn rug naar Amir (`face -1`; een echte
rug-sprite is er niet, hij kijkt van Amir weg) en ademt. Komt Amir binnen `zie` Amir, of raakt Amir hem, dan:
- `spreek`: het spel staat al stil (balken, camera, Amir vast), maar Nyundo blijft staan en spreekt: `brutus_start1.mp3`,
  een korte pauze (`spreek.pauze`), dan `brutus_start2.mp3`. Op driekwart van start2 (`spreek.loopBij`) gaat hij lopen en
  loopt start2 door onder het stampen. Het geluid zelf is de klok (`currentTime`), met de speltijd als terugval als het
  niet speelt (`spreek.een`, `spreek.twee`: de lengte van de spraak zonder de stilte erachter). Staat het geluid uit, dan
  slaat hij dit stuk over. Bij pauze stopt de spraak even, bij een herstart of een ander level is hij weg (`bruSpraakStap`).
- `loop`: het spel staat stil voor Amir (`bruIntroVast` in `amirVast`), zwarte balken, de camera schuift naar Nyundo en de
  tonnen (`bruIntroCam`). Hij loopt met de stormframes, trager (`loopMs`, `loopV`), naar de dichtste groep tonnen
  (`bruIntroDoel`: `sta` grote-set-px rechts van de meest rechtse).
- `slag`: de zijwaartse zwaai uit brutus.json (heen in frame 11-14, terug in 18-21, `raak`); wat in het vak staat gaat in
  een keer (`tonBruut`), en de stukken vliegen tegen de lens (`TON.lens`, zie "Naar de lens" in `notities/tonnen.md`).
  De naam (NYUNDO, de hamer) komt in beeld.
- `draai`: hij kijkt naar Amir, en na `draai` s stormt hij; de balken schuiven weg (`weg`) en de balk onderaan komt.
`s.state` blijft `wacht` tot de storm, dus hij raakt Amir niet en de sprong-timer loopt niet. Een keer per level per sessie
(`bruIntroGezien`): na een dood staat hij meteen klaar, en de tonnen die hij kapot sloeg blijven kapot (`tonKapot`, per level per sessie, ook wat hij in het gevecht breekt).
Onder de losse luifel links (`stad.luifels`, -6000) staat de stapel die hij kapotslaat; bij de put rechts staan er twee voor
het gevecht (zie `notities/tonnen.md`).

## Bestanden
- **De voeten in de zwaai, de kap en de terugslag**: in de Grok-clip zweefde hij in de zwaai 30 tot 60 px boven de grond, met de ene voet
  hoger dan de andere; in de kap stond de achterste voet 15 px boven de lijn en de voorste tot 42 px, in de terugslag
  wisselde het van 18 px erboven tot 2 px eronder. `tools/brutus_voeten.py` (zonder argument de zwaai, `kap terug` voor
  de andere twee) zet per frame de laagste voet op de grondlijn en buigt het been
  van de hogere voet omlaag (een zachte verschuiving van heup naar voet, van het kruis naar buiten). De originelen staan
  in `enemies/brutus/bron/` (ook hun regels in `bron/brutus.json`); het script werkt altijd vanaf die originelen. In de
  terugslag meet het rond het meeschuivende lijf (`verplaatsing`, zoals `bruLijfDX`), en een voet hoger dan `BUIG_MAX`
  is een pas (het been is opgetild): dat frame wordt alleen verschoven, niet gebogen. Daarna `gen-klein.py` en `gen-offline-manifest.py`.
- `enemies/brutus/brutus.json` met per beweging (`idle`, `storm`, `zwaai`) per frame `{src, dx, dy, w, h, ms}`
  t.o.v. het anker (midden van het lijf) en de grondlijn, in pixels van de grote set (figuur ~340 hoog van
  haar tot voet), naar links kijkend. `klein/enemies/brutus/` dezelfde frames op halve grootte.
- Bron: Grok-clips (idle_breathign1, RC2, hitnice), gekeyd en per clip op één schaal en één verschuiving
  gezet (animeer tool Bruut), daarna omgekleurd: broek zwart, sjerp bloedrood, windsels ijzer; het rode
  haar bleef. De idle is één inademing heen en terug; in het spel volgt hij het ademgeluid (`BRU.ademPeriode`).
- **Nyundo donker** (`huid: 'donker'` in `brutus: {...}`, of in de sandbox de knop **Huid** in de rij Brutus): dezelfde
  frames in een tweede kleurstelling, `enemies/brutus/frames_donker/` (en `klein/`), uit `tools/brutus_donker.py`.
  Donkerder bruine huid, zwart haar, feller rood in het gezicht met een licht litteken over zijn oog, een bruine broek,
  een gouden sjerp en warm gouden polswindsels (een verloop met glans). Het script leest brutus.json voor het anker en
  zoekt per frame het haar, het gezicht, de sjerp, de broek en de polsen op. Lui geladen (`bruDonkerLaad`); tot die
  frames binnen zijn tekent hij met de gewone. Geen level gebruikt het nog. Na `brutus_voeten.py` opnieuw draaien,
  daarna `gen-klein.py` en `gen-offline-manifest.py`.
- Geluiden: `sounds/brutus_adem.mp3` (loopt zolang hij staat te ademen), `brutus_stap.mp3`,
  `brutus_zwaai.mp3` (start op zwaaiframe `BRU.zwaaiGeluid`, de zoef valt op de treffer),
  `brutus_geraakt.mp3` (niet meer gebruikt: de omslag naar zijn woede is nu `brutus_fase3.mp3`). Een treffer geeft naast
  `brutus_speerraak.mp3` (de speer in zijn vlees) een van zes kreten, `brutus_hit1.mp3` tot `brutus_hit6.mp3`, geknipt uit
  hits.mp3, nooit twee keer dezelfde achter elkaar (`BRU_HITS`, `bruHitSpeel`). De opening: `brutus_start1.mp3` en
  `brutus_start2.mp3`.

**Wind tijdens het gevecht** (`BRU.wind`, in `weerGeluid`): zolang Nyundo niet ligt loopt er een constante woestijnwind
onder het gevecht, als een vierde van de zandstorm (dezelfde lus, `stormSnd`). Na zijn dood zwakt hij langzaam af.
