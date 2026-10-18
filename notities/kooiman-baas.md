# De kooiman als baas: "super bird man" (concept voor later)

De gewone kooiman is bewust **licht** gehouden (zie hieronder). De rijke mechanieken die we
bedachten horen bij een apart, geensceneerd gevecht, een eigen ontwerp en een eigen PR,
waarschijnlijk in een arena (zoals de bandiet-arena en de goudaap-arena). Dit is de notitie zodat
het idee niet wegzakt.

## Identiteit
Een zoner-baas die de grond controleert en de lucht met vogels. De tegenstelling met de bandiet:
de bandiet wil close komen, de kooiman houdt je juist op afstand. Als baas wordt dat uitvergroot.

## Vechtopzet (concreter, uit het brainstormen)
Een arena, geen open vlakte. De aanname is **arena-als-kooi**: een begrensd vak met tralies als rand,
Amir beweegt erbinnen (niet letterlijk vast, anders valt het dansen om de vogels weg). Nog te
beslissen: arena-kooi of Amir echt vast.

- **De boss staat hoog aan de zijkant** en stuurt constant vogels. Je beschadigt hem met
  **speerworpen**, maar je moet eerst **plateaus op springen** om zijn hoogte/strook te halen.
- **Speer-economie met verticaliteit.** Beneden haal je een speer (de aanvoer). Je klimt onder
  vogeldruk omhoog, en de worp is de kwetsbare commit (stilstaan tussen de vogels door). Of je nu
  **raakt of mist, je speer is op** en je moet weer naar beneden voor een nieuwe. Zo ontstaat een
  grond-plateau-top ritme.
- **Twee kooimannen** aan weerszijden slaan regelmatig; een **kooislag kan je van een plateau af
  knikkeren**, zodat je je hoogte (en je klim) verliest. Zo zijn ze de verticale verstoring.
- **Plateaus als echte, tijdelijke dekking**: een plateau kan een duik blokkeren (je schuilt eronder),
  maar de kooimannen slaan je er weer af en de boss verlegt zijn vogels, dus cover is adem, geen haven.
- **Af en toe een ander creature** als kruiding, niet als vierde gelijktijdige dreiging.

### Tuning die het maakt of breekt
- De aanvoer-trip kort houden (speerrek of skelet onderaan, of aangroeiende speren); de klim ~10 tot
  20 s per cyclus; niet te veel treffers nodig (4 a 6), anders rekt het.
- **Raak moet belonen**: bij een treffer deinst de boss en pauzeren de vogels heel even, zodat je adem
  hebt om af te dalen. Anders voelt raken net zo straffend als missen.
- **Van een plateau geknikkerd kost vooral positie**, niet elke keer een leven (lichte valschade mag,
  maar stapel het niet met vogel + boss tot iets onontwijkbaars).
- **De worp moet de boss echt kunnen raken** vanaf een plateau: met een tool (zoals runecheck.js)
  nameten dat er een echte strook is waar je hem raakt en in beeld hebt.
- **Pacing tegen overload**: kooimannen slaan om en om, een maximum vogels tegelijk, en altijd een
  haalbaar gaatje om te gooien (een onmogelijke combo is het enige echte risico).

### Fases (natuurlijk verloop)
1. Rustig: 1 a 2 vogels, kooimannen slaan af en toe. Je leert het ritme en gooit in de gaten.
2. Midden (boss ~2/3): meer/snellere vogels, de creature duikt op, plateaus misschien deels kapot.
3. Eind: beide kooimannen actiever, vogels constant, maar de boss stelt zich vaker bloot: daar zit je
   echte opening.

### Open vragen
- Arena-kooi of Amir echt vast (advies: arena-kooi).
- Win via speerworp (advies) of via klimmen tot bij de boss.
- De tuning hierboven: aanvoer-tempo, raak-beloning, knock-off-straf.

## Mechanieken (de zware set, niet in de lichte versie)
- **Standhouden met leash.** Hij blijft op zijn plek en slaat de kooi neer om je op afstand te
  houden, draait zich naar je toe (de kooi blijft tussen jullie), en rukt pas op als je een eind
  buiten bereik komt. Zo is hij niet te negeren of straffeloos voorbij te lopen.
- **De kooi-boog is een muur.** Tijdens de neerwaartse helft van de slag is de kooi, ook hoog in de
  lucht, een hazard: eronderdoor of erdoorheen lopen tijdens de swing is een treffer. Tussen de
  slagen door mag een sprong eroverheen wel. Zo kom je hem niet voorbij zoals je door de bandiet
  heen loopt; je moet door zijn ritme heen.
- **Naderen in etappes.** Elke slag en zijn ruimte dwingen je in golven dichterbij te komen, of je
  blijft op afstand en mikt in zijn herstelraam.
- **De speer als keuze onder druk.** Gooien kost stilstand (mikken), en stilstaan maakt je kwetsbaar
  voor een duikende vogel. Je raam om te gooien is dus "kooiman ligt open (herstel) EN er duikt net
  geen vogel". Twee assen die samen je timing dicteren.
- **Meerdere vogels, om en om.** Twee of meer vogels op verschillende timers, zodat er altijd een is
  om in de gaten te houden maar ze apart te ontwijken blijven. Nooit tegelijk duiken (anders
  onontwijkbaar). Let bij het tunen op: er moet altijd een haalbaar gaatje zijn om te gooien.
- **Speer-afweer met tell.** De kooi houdt je speer tegen tijdens slepen en slag (hij is dan
  gepantserd); geef dat een metalige clang en een flits, zodat het leest als een actief blok.
  Eventueel later een echte reactieve parry (hij gooit de kooi omhoog op jouw worp), maar dat is
  duurder en kan frustreren als het je enige speer wegblokt.
- **Fases en een arena.** Ruimte om de mechanieken te laten ademen, oplopende druk (meer vogels, een
  sneller ritme), en een duidelijk strafvenster.

## Wat we bewust NIET bij de speler doen
Geen gedwongen verplaatsing van Amir door de schokgolf. Dat pakt controle af op het moment dat je
een vogel moet ontwijken (je staat goed, de kooi slaat, en ineens sta je in de duikbaan). De zwaarte
verkoop je met beeld en geluid (stof, trillende steentjes, schermschok, een korte gedeelde hitstop
die ook de vogel bevriest), niet door de speler te duwen. Word je wel geraakt (je stond in de
kooi-boog), dan is de gewone terugstoot van `hurtPlayer` terecht.

## De duel-variant (gebouwd, nu in de sandbox)

Een geensceneerd een-op-een duel, los van de gewone sleep-kooiman. Opt-in met `duel: true` in een spawn,
of de knop **Duel** onder Vijanden, Kooiman in de sandbox. De getallen staan in `KOOI_DUEL` (laptop-waarden,
bedoeld om in het spelen bij te stellen). Het idee: een leesbaar ritme-duel, geen beuken.

- **Intro.** Zodra hij volledig in beeld komt bevriest meteen het hele spel (`kooiVries`, ook Amir), en loopt de
  hele stamp-plus-vogel-keten tijdens die freeze (`kooiVriesStap`, de states `stomp`, `hatch`, `stomp_out`): hij
  heft zijn knie en stampt, op de klap stof en geluid, het luikje gaat open, de vogel schiet eruit, het luikje
  slaat dicht, unfreeze, een korte uitloop en dan terug naar slepen. Zo kan Amir er tijdens de telegraaf niet
  naartoe rennen (vroeger liep de stamp unfrozen en stond je al bij hem voor de freeze begon). Daarna begint het
  gevecht; na `stomp_out` staat hij in `drag` met `vogelGedaan`, en de slag-cadans begint.
- **Afstand houden.** Hij blijft op een scherm-relatieve standoff (`KOOI_DUEL.afstand` maal de zichtbare halve
  breedte), zodat je hem altijd ziet slepen. Loop je weg, dan sleept hij je achterna tot hij zijn afstand terug
  heeft (`volg`). Nader je, dan laat hij je komen en wijkt hij niet terug. Zo kun je kiezen: op afstand blijven
  en gooien, of naar binnen voor een melee.
- **Vaste slag-cadans.** Hij slaat op een tijd-drumbeat (`eersteNa` voor de eerste, daarna `cadans`), los van
  afstand. Afstand bepaalt alleen of zijn klap-zone je bereikt.
- **De trilling zet je terug.** Elke keer dat de kooi de grond raakt stuurt de trilling je een stuk terug
  (`schok`, een knock op de speler, binnen `schokVer`), los van schade. Dat is de spacing: ren je op hem af,
  dan word je per slag teruggezet. Op het idee van de melee-gauntlet: ren, slag zet je terug, ren (netto
  dichterbij), slag zet je terug, en zo haal je hem in een paar golven. Afstellen op ongeveer drie met `schok`.
- **Kwetsbaar na zijn eerste slag.** Na zijn eerste slag ligt hij blijvend open voor een worp of een klap
  (`kooiRaakbaar`: `slagen >= 1`), behalve tijdens een slag zelf, want dan is de kooi zijn pantser. Een rake
  treffer is dodelijk (`hp` 1). Dat de kwetsbaarheid blijft (en niet alleen het krappe herstelraam is) was nodig:
  een worp vanaf de standoff-afstand kwam anders net na het herstel aan en kaatste af. De echte uitdaging blijft
  de vogel ontwijken terwijl je gooit. Gooi je voor die eerste slag, dan versnelt hij zijn slag (de `snel`-boost)
  en ramt hij je speer de grond in (de speer valt bij hem, op te halen); die geforceerde slag telt als zijn
  eerste, dus daarna ligt hij open.
- **De vogel komt steeds terug.** Na elke vogel komt er na `vogelPauze` een nieuwe. Die overlapt het slag-ritme
  en maakt zowel het worp-raam als het naderen lastig. Het mooiste raam is: hij ligt open EN er duikt net geen
  vogel; time je het en beweeg je weg, dan gooi je de kill en ontwijk je de duik in dezelfde beweging.

Nog open / te tunen (vraagt jouw playtest): de precieze cadans en het worp-raam, de kracht van de trilling (de
drie-golven-gauntlet), en of de vogel-timer netjes een offset houdt op de slagen (nu lopen het twee losse timers).
Nog niet gedaan: een echte blokkade (hij houdt je nu tegen met de trilling en de hazard, niet met een muur), een
eigen testlevel (vraagt toestemming), en de telefoon-afstelling (nu laptop-first).

## De lichte versie (de gewone kooiman, wel nu gebouwd)
- Zoner-smaak, maar simpel: hij houdt stand en slaat als je in bereik bent, draait naar je toe, en
  rukt op als je buiten bereik komt. Geen kooi-boog-muur, geen leash-finesse van de baas.
- Zwaardere grond-impact (meer stof, trillende steentjes, schok), geen speler-duw.
- Gepantserd behalve in het herstel, vier klappen.
- Eén vogel, echt dodgebaar: recht omhoog, naar boven Amir, patrouille op X met lichte Y, stilhangen
  als tell, dan duiken op je vastgelegde plek; dood bij een misser. Opt-in met `vogel: true`, het
  aantal als veld voor later.
