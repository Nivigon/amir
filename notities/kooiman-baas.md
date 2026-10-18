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
in het spelen bij te stellen, zie **Live afstellen**). Het idee: een leesbare bait-en-punish, geen ritme-maatwerk.
Bewust simpel gehouden zodat hij combineert met andere mobs en hindernissen; de rijke zoner-set hierboven is
voor de eindbaas-arena, niet voor deze mob.

- **Intro.** Zodra hij volledig in beeld komt bevriest het beeld, maar alleen Amir en de andere vijanden
  (`kooiVries`, `kooiVriesStap`, de states `stomp`, `hatch`, `stomp_out`); de stamp zelf loopt door, met zijn
  stofwolk en de omhoog schietende steentjes. Hij heft zijn knie en stampt, de kooi klapt open, de vogel schiet
  eruit, unfreeze, een korte uitloop en dan `drag` met `vogelGedaan`. Zo kan Amir er tijdens de telegraaf niet
  naartoe rennen.
- **Eén afstand-ram (de opener).** Na de intro houdt hij een scherm-relatieve standoff (`KOOI_DUEL.afstand`) en
  slaat hij na `eersteNa` eenmalig de kooi op de grond. De klap zet Amir terug (`schok`, binnen `schokVer`, dooft
  gewoon uit zoals een gewone klap, zodat hij zelf in beeld blijft) en kost een heel leven als je in de klap-zone
  staat (`schade`, net als de grond-hit). Een worp die je al opspant breekt af door de schok (`thrCancel`), dus je
  kunt pas na het terugzetten een verse worp inzetten (niet tijdens zijn animatie voor-mikken).
- **Daarna de nadering, en pareren.** Vanaf `s.slagen >= 1` komt hij op je af (`volg`) en slaat hij reactief zodra
  je binnen `slagBereik` komt (ruimer dan je steek, dus naar binnen rennen en steken lukt niet: je vangt eerst zijn
  slag). Buiten zijn herstel pareert hij alles, worp en melee (`kooiPareer`), met precies hetzelfde effect als de
  bandiet-parry: de clang en de vonken op het snijpunt plus de korte hitstop en schok (`banClang`, `banVonk`,
  `BAN_PAREER_STOP`/`SHAKE`), zodat je hoort en ziet dat het een parry is; later een eigen animatie waarin hij de
  kooi omhoog houdt. Hij ligt alleen open in zijn
  **herstel** (`kooiRaakbaar`/`kooiMeleeRaak`: `state === 'recovery'`).
- **De weg om hem te slopen: bait, stapterug, punish.** Lok zijn slag uit, stap terug zodat hij misslaat, en raak
  hem in zijn herstel, een worp of een steek, een rake treffer is dodelijk (`hp` 1). Naar de overkant glippen
  helpt niet: hij draait altijd naar je toe en op gelijke hoogte slaat hij versneld terug als je er vlak langs
  wil (`s.snel` als je binnen een lijf-breedte komt). Op een hogere laag (terras, zwevende laag) telt de slag niet
  (`kooiZelfdeHoogte`) en loop je er gewoon overheen.
- **De geparede worp ketst terug naar Amir.** `kooiSpeerKaats` laat hem `speerKaats` px voor Amir vallen, altijd
  aan Amirs kant van de kooiman (nooit erachter, geen softlock). Snel oppakken wel: loopt de kooiman er eerst bij,
  dan kost het je een hit.
- **De vogel is eenmalig, een half leven.** Hij komt uit de intro, duikt een keer (`KOOI_DUEL.vogelDuik` seconden
  patrouille, zo gezet dat hij op je eerste nadering valt) en is daarna dood. Zo is de eerste poging de spannende.
  (`spawnVogel` alleen nog vanuit de hatch van de intro; de duik doet een half leven, `v.duel`.)

**Live afstellen.** In de pauze onder Instellingen staat **Kooiman-duel: afstelling** (`pzkooibtn`, `KOOI_SCHUIF`):
schuifjes die `KOOI_DUEL` meteen aanpassen, ook bij een herstart, bewaard in de browser (`KOOI_DUEL_KEY`). Zo zoek
je de balans in het spelen (de standoff, de loop/volgsnelheid, de tijd tot de opener, het slagbereik van de
nadering, de knockback en zijn bereik, het slagtempo, de schade van een rake slag, hoe ver de geparede speer
terugketst, en wanneer de vogel duikt). Ben je tevreden, neem de getallen dan over in `KOOI_DUEL`. De knop staat
er alleen in een level (of de sandbox) met een duel-kooiman.

Nog te doen: een echte parry-animatie (nu de clang en vonken van de bandiet-parry, later houdt hij de kooi snel
omhoog), en de telefoon-afstelling (nu laptop-first). Test 38 is het proefstuk.

## De lichte versie (de gewone kooiman, wel nu gebouwd)
- Zoner-smaak, maar simpel: hij houdt stand en slaat als je in bereik bent, draait naar je toe, en
  rukt op als je buiten bereik komt. Geen kooi-boog-muur, geen leash-finesse van de baas.
- Zwaardere grond-impact (meer stof, trillende steentjes, schok), geen speler-duw.
- Gepantserd behalve in het herstel, vier klappen.
- Eén vogel, echt dodgebaar: recht omhoog, naar boven Amir, patrouille op X met lichte Y, stilhangen
  als tell, dan duiken op je vastgelegde plek; dood bij een misser. Opt-in met `vogel: true`, het
  aantal als veld voor later.
