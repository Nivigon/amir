# De kooiman als baas: "super bird man" (concept voor later)

De gewone kooiman is bewust **licht** gehouden (zie hieronder). De rijke mechanieken die we
bedachten horen bij een apart, geensceneerd gevecht, een eigen ontwerp en een eigen PR,
waarschijnlijk in een arena (zoals de bandiet-arena en de goudaap-arena). Dit is de notitie zodat
het idee niet wegzakt.

## Identiteit
Een zoner-baas die de grond controleert en de lucht met vogels. De tegenstelling met de bandiet:
de bandiet wil close komen, de kooiman houdt je juist op afstand. Als baas wordt dat uitvergroot.

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

## De lichte versie (de gewone kooiman, wel nu gebouwd)
- Zoner-smaak, maar simpel: hij houdt stand en slaat als je in bereik bent, draait naar je toe, en
  rukt op als je buiten bereik komt. Geen kooi-boog-muur, geen leash-finesse van de baas.
- Zwaardere grond-impact (meer stof, trillende steentjes, schok), geen speler-duw.
- Gepantserd behalve in het herstel, vier klappen.
- Eén vogel, echt dodgebaar: recht omhoog, naar boven Amir, patrouille op X met lichte Y, stilhangen
  als tell, dan duiken op je vastgelegde plek; dood bij een misser. Opt-in met `vogel: true`, het
  aantal als veld voor later.
