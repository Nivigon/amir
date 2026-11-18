# Speelgevoel: wat spelers zoeken, en hoe Amir binnen een minuut lekker voelt

18 november 2026. Een analyse los van de levels: niet wat een level nodig heeft, maar wat een speler zoekt als hij
het spel opent, en wat ervoor zorgt dat hij in de eerste minuut denkt "hé, dit speelt lekker". Hoort bij
`notities/kit-analyse.md` (de talents en de twee wapens). Nog niets gebouwd. Het geldt voor de speer, de stokken en elke
tribe die er later bij komt.

## 1. Wat een speler zoekt

Een speler van een 2D-actiespel in de browser beslist binnen een minuut of hij blijft. In die minuut leest hij geen
tekst en kiest hij geen talent. Hij zoekt, in deze volgorde:

1. **Controle.** Doet het poppetje wat ik bedoel, op het moment dat ik het bedoel? Dit merkt hij in de eerste drie
   seconden, aan lopen, keren en springen, nog voor er een vijand is. Klopt dit niet, dan helpt niets anders meer.
2. **Kracht.** Als ik raak, voel ik dat dan? Een treffer moet in de handen klappen: het beeld stokt, de vijand schokt,
   het klinkt hard. Dit is wat spelers "lekker" noemen, en het is bijna altijd feedback, geen mechaniek.
3. **Eerlijkheid.** Als ik geraakt word, snap ik waarom? Zag ik het aankomen? Een speler vergeeft een moeilijk spel,
   maar geen oneerlijk spel.
4. **Beheersing.** Word ik beter? Merk ik dat ik iets kan wat ik vijf minuten geleden niet kon? Hier zit de perfecte
   rol-worp: makkelijk om te doen, moeilijk om altijd perfect te doen.
5. **Expressie.** Kan ik het op mijn manier doen? Een gevecht dat je op drie manieren kunt winnen voelt als jouw gevecht.
   Hier komen de tribes en talents pas in beeld: ze zijn voor uur twee, niet voor minuut een.

De les: **talents lossen niets op in de eerste minuut.** Het gevoel zit in de basis: lopen, springen, slaan, geraakt
worden. De rest van deze notitie gaat daarover.

## 2. Vijf lagen van gevoel

Uit "Game Feel" van Steve Swink, toegepast op Amir. Elke laag bouwt op de vorige; een fout onderin maakt alles erboven
zwakker.

| laag | vraag | bij Amir |
| --- | --- | --- |
| invoer | reageert hij meteen? | de aanloop van de sprong, de opbouw van de steek |
| beweging | heeft hij gewicht en snelheid? | de sprongboog, keren, landen |
| treffer | voelt contact als contact? | hitstop, schok, geluid, de reactie van de vijand |
| lezen | zie ik wat er gebeurt en gaat gebeuren? | het aankondigen van een klap, open vijanden |
| fantasie | voel ik me een jager, een stokvechter? | de animaties, Tau, de speer in de borst |

## 3. Wat er nu staat (gemeten in de code)

Een paar getallen die het eerste gevoel bepalen.

- **De sprong vertrekt pas na 0,12 s.** Hurken (`CROUCH_T` 0,07) en afzetten (`PUSH_T` 0,05) gebeuren voor hij loskomt.
  Dat ziet er echt uit, maar in de handen voelt het als een sprong die even nadenkt. De meeste goede platformers
  vertrekken op het beeld van de druk, en tonen het hurken hooguit als een frame terwijl hij al stijgt.
- **De sprong is altijd even hoog.** Er is een opsprong (`JUMP_V` 1000) en een zwaartekracht (`GRAVITY` 2400), en die
  zijn op en neer gelijk. Loslaten maakt de sprong niet korter. Een symmetrische boog voelt zweverig, als een bal op de
  maan. Spelers zijn gewend aan een snelle val: zwaarder vallen dan stijgen, en een korte sprong als je vroeg loslaat.
- **De landing duurt 0,13 s** (`LAND_T`). Als hij in die tijd niet meteen kan wegrennen of opnieuw springen, voelt dat als
  plakken.
- **Coyote time is er** (`COYOTE_T` 0,12): springen vlak na de rand mag nog. Goed. Een sprong die net te vroeg is
  ingedrukt (voor de landing) wordt nog niet onthouden.
- **De steek raakt na 0,22 s** (`ATK_FPS` 18, raak vanaf frame 4). Voor de gewone aanval is dat aan de trage kant; een
  lichte aanval raakt in de meeste actiespellen binnen 0,10 tot 0,15 s. De afkoeling erna (`ATK_COOLDOWN` 0,18) is kort.
- **De eerste stokslag (de stapslag) raakt pas na 0,36 s.** Dat is de eerste knop die een speler met de stokken indrukt,
  en dan duurt het lang. De stap is mooi, maar het eerste wat je voelt is wachten.
- **Hitstop zit op bijzondere momenten** (de crit, de parade van de bandiet, de kooi, de dubbele worp), niet op een
  gewone treffer. Juist de gewone treffer maakt de eerste minuut.

## 4. De eerste minuut, seconde voor seconde

Wat een nieuwe speler doet, en wat hij dan moet voelen. Dit is de toets voor elke wijziging aan de basis.

**0 tot 5 s: lopen en keren.** Hij drukt links en rechts. Amir moet binnen een tiende op snelheid zijn, bij het keren
meteen omdraaien met een stofje bij de voet, en bij het loslaten bijna meteen stilstaan. Een korte glijpas bij het keren
op volle snelheid geeft gewicht zonder traagheid.

**5 tot 10 s: springen.** Hij springt een paar keer, ook zomaar. De sprong moet vertrekken op de druk, kort zijn bij een
tikje en hoog bij vasthouden, even hangen bovenin, en snel vallen. De landing: een stofwolkje, een frame door de knieën,
en meteen verder kunnen.

**10 tot 20 s: de eerste aanval, in de lucht.** Hij drukt de aanvalsknop zonder vijand. Ook een steek in het niets moet
lekker zijn: een korte zwiep in het geluid, een spoortje van de punt, een klein stapje naar voren. Spelers rammen de
knop om te voelen hoe het wapen is.

**20 tot 40 s: de eerste vijand.** Een makkelijke vijand die op een gewone treffer reageert. Hier valt het oordeel. De
eerste treffer moet het hele pakket hebben (zie hoofdstuk 5), en de eerste kill nog meer.

**40 tot 60 s: de eerste keer geraakt.** De klap moest te zien zijn aankomen. Amir knippert, schuift terug, er is een
kort moment waarin hij niet nog eens geraakt kan worden, en de speler weet precies wat hij fout deed.

Een speler die na deze minuut doorspeelt, gaat zelf ontdekken: de rol, de worp, de rol-worp. Dat is waar beheersing
begint.

## 5. De treffer: het pakket

Een treffer is niet een ding maar acht dingen tegelijk. Ze kosten elk weinig, en samen maken ze het verschil tussen
"het werkt" en "lekker".

1. **Hitstop:** het beeld staat 0,03 tot 0,05 s stil op het moment van contact, bij Amir en de vijand allebei. Bij een
   kill 0,08 tot 0,12 s. Dit is de belangrijkste van de acht.
2. **Witte flits:** de vijand is een of twee frames wit (of licht), zodat het oog het contact ziet.
3. **Duw:** de vijand schuift een stukje in de richting van de klap, ook als hij niet doodgaat.
4. **Schok:** het beeld trilt een paar pixels, in de richting van de klap, niet willekeurig. Klein bij een treffer,
   groter bij een kill.
5. **Deeltjes in de richting van de klap:** stof, bloed of houtsplinters die wegspuiten waar de klap heen gaat.
6. **Geluid in lagen:** de klap zelf (hout, punt, vlees), het materiaal, en soms een stem. Elke keer een tikje andere
   toonhoogte, zodat tien treffers op rij niet als een machine klinken.
7. **Amir voelt het ook:** een korte terugslag in zijn arm of een frame langer op de raakpose. Zijn klap stuit ergens op.
8. **De kill is anders dan een treffer:** langer stilstaan, groter geluid, het lijf valt met gewicht, en even ruimte
   (een halve seconde waarin niets aanvalt) om ervan te genieten.

Hetzelfde voor Amir zelf als hij geraakt wordt, maar dan duidelijk anders: een rode rand, een doffere klap, een kreet.
De speler moet met zijn ogen dicht horen of hij raakte of geraakt werd.

## 6. Eerlijk en vergevingsgezind

Spelers voelen een spel als lekker als het hun bedoeling volgt, niet hun precieze knopdruk.

- **Een grote raakzone voor Amir, een kleine voor de vijand.** Zijn speer raakt net iets verder dan het plaatje zegt; een
  klap van de vijand moet echt contact maken.
- **Invoer onthouden.** Een sprong, rol of aanval die tot 0,12 s te vroeg is ingedrukt, gaat af zodra het kan.
- **Afbreken mag.** Een aanval afbreken met een rol of sprong, tot vlak voor de treffer. Een speler die durft, heeft een
  uitweg nodig.
- **Elke klap van een vijand heeft een aankondiging:** een pose die even blijft staan, een geluid, en bij een klap die je
  niet kunt blokken een rode glinstering. Hoe harder de klap, hoe langer de aankondiging.
- **Na een treffer even onkwetsbaar**, met knipperen, zodat twee vijanden je niet in een tel leegslaan.
- **Ruime vensters voor wie begint.** Een perfecte worp of parade mag in het begin een ruim venster hebben. Krapper maken
  kan later, met een talent of een moeilijkheidsgraad.
- **Een dood is altijd te snappen.** Kort het moment terugzien (het beeld vertraagt op de laatste klap) helpt.

## 7. Beheersing: makkelijk te leren, moeilijk te meesteren

Wat een speler na de eerste minuut vasthoudt, is het gevoel dat hij beter wordt. Daar heeft Amir al goede dingen voor.

- **Een basis die simpel is en een plafond dat hoog is.** De rol-worp is het voorbeeld: iedereen kan rollen en gooien,
  maar perfect is een kunst. Elke nieuwe move moet die vorm hebben: een gewone versie die werkt, en een perfecte die
  knalt.
- **Dingen die aan elkaar vastklikken.** Rol, worp, tweede speer, sprint, plukken, steek: als die zonder pauze in
  elkaar overlopen, gaat de speler zelf reeksen bedenken. Dat is het moment waarop hij het spel "zijn" spel noemt.
  Elk eind van een beweging moet in het begin van een andere kunnen.
- **Het spel ziet het als je goed bent.** De multikill-kralen, het woord, de ster: de speler moet zijn goede actie
  bevestigd zien. Een perfecte actie zonder reactie van het spel is een verspilde perfecte actie.
- **Laat ontdekken in plaats van uitleggen.** Een speler die zelf vindt dat je uit de rol kunt gooien, onthoudt dat
  beter en is er trotser op dan wie het in een tip las. Tips voor de basis, ontdekken voor de rest.

## 8. De fantasie: wie ben ik?

Het laatste dat telt, en het langst blijft: voelt de speler zich iemand?

- **De speer: de jager.** Geduldig, precies, dodelijk van afstand. Het mooiste moment is de worp die van ver raakt en
  de vijand neerhaalt. Geef die worp het gewicht van een gebeurtenis: het geluid van de vlucht, de inslag, het lijf
  dat valt met de speer erin.
- **De stokken: de vechter.** Dichtbij, snel, het ritme van hout op hout. Het mooiste moment is de counter. Geef het
  geluid van de stokken een eigen ritme, als een trom, zodat een goed gevecht klinkt als muziek.
- **Amir zelf.** Een kreet, een ademhaling na een gevecht, een blik over zijn schouder. Kleine dingen die hem een
  persoon maken in plaats van een cursor.

Een nieuwe tribe begint met deze vraag: wie ben ik met deze tribe, en wat is mijn mooiste moment?

## 9. De lijst: van groot naar klein

Gesorteerd op hoeveel een speler het in de eerste minuut merkt, gedeeld door het werk. Codes erbij voor de kit-lijst.

| code | wat | merkbaar | werk |
| --- | --- | --- | --- |
| V1 | de treffer-pakket: hitstop, flits, duw en schok op elke gewone treffer (A1) | heel hoog | klein |
| V2 | sprong: zwaarder vallen dan stijgen, en korter bij vroeg loslaten | heel hoog | klein |
| V3 | sprong vertrekt op de druk; het hurken als beeld, niet als wachten | hoog | klein |
| V4 | invoer onthouden (sprong, rol, aanval) en afbreken met een rol (A3) | hoog | klein |
| V5 | de kill anders dan een treffer: langer stil, groter geluid, even ruimte | hoog | klein |
| V6 | de eerste stokslag sneller raak (een korte slag als eerste, de stapslag als tweede of met vasthouden) | hoog (stokken) | middel |
| V7 | de steek iets eerder raak (0,15 s in plaats van 0,22), met een zwiep ook in het niets | hoog (speer) | middel |
| V8 | geluid met variatie in toonhoogte, op elke klap en stap | middel | klein |
| V9 | keren met een glijpasje en stof, stilstaan zonder na te glijden | middel | klein |
| V10 | landen: stof, een frame door de knieën, meteen verder | middel | klein |
| V11 | Amir geraakt: rode rand, eigen klap, knipperen (deels er al) | middel | klein |
| V12 | aankondiging op elke vijandklap, rood voor wat je niet kunt blokken | middel | middel |
| V13 | een open vijand zichtbaar (A2) | middel | klein |
| V14 | elk eind van een beweging loopt in elk begin over: de reeks rol, worp, pluk, steek zonder pauze | hoog na een paar minuten | middel |
| V15 | killcam op de laatste van een gevecht (A6) | hoog na een paar minuten | klein |

**Begin met V1 tot en met V5.** Dat zijn vijf kleine dingen, voor beide wapens en elke toekomstige tribe, en samen zijn
ze precies wat een speler in de eerste minuut voelt. Na elke stap de toets van hoofdstuk 4: open de sandbox, loop, spring,
sla in het niets, sla een vijand, word geraakt. Voelt elke seconde goed?

## 10. Meten in plaats van gokken

Gevoel is te meten. Een klein script naast de speelrobot (`tools/speelrobot.js`), bijvoorbeeld `tools/gevoelmeter.js`,
dat in Chromium de knoppen indrukt en per beweging telt:

- beelden van de druk tot de eerste verandering op het scherm (sprong, aanval, rol);
- tijd van de druk tot de treffer, en van de treffer tot je weer kunt bewegen;
- de sprongboog: tijd omhoog, tijd omlaag, hoogte bij een tikje en bij vasthouden;
- hoe lang het beeld stilstaat bij een treffer en bij een kill.

Zo leg je een wijziging naast de vorige, en zie je of een nieuwe tribe of wapen in hetzelfde tempo voelt als de rest.

## Bronnen en voorbeelden

Steve Swink, "Game Feel" (de lagen van invoer tot fantasie). Jan Willem Nijman (Vlambeer), "The art of screenshake"
(hitstop, schok, geluid, een kill die groter is dan een treffer). Celeste (vergevingsgezind: coyote time, invoer onthouden,
ruime vensters). Hollow Knight en Dead Cells (een treffer met stilstand en duw, afbreken met een rol, aankondigingen).
Hades (een gewone actie die al goed voelt, en een perfecte die knalt).
