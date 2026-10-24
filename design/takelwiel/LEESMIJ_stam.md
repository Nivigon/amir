# Amir, King of Africa - tilbaar platform met tandwiel-mechaniek

Dit pakket bevat de nieuwe onderdelen die we voor dit decorstuk hebben gemaakt,
plus uitleg en een voorbeeld van wat we bouwen. Het grote tandwiel op de grond,
het platform en het touw staan al op de repo, die zitten hier bewust NIET in.

## Wat we bouwen

Een houten draagpaal (de stam) tilt een platform. Op de grond ernaast staat het
grote houten tandwiel (al op de repo) waar de speler op slaat. Een touw (al op de
repo) loopt vanaf de achterkant van dat wiel, achter de paal langs. Op de pen
bovenaan de paal zit een klein roestig tandwiel dat meedraait zodra het platform
beweegt. Zo lijkt het geheel een aandrijving in plaats van losse stukken.

Zie `voorbeeld_opbouw.png` voor de opbouw (de animatie-mockup is weggehaald).
In de voorbeelden staan het grote wiel, platform en touw alleen
ter context; gebruik daarvoor de bestaande repo-assets.

## Wat zit erin (nieuw)

- `assets/stam_vol.png` - de hele draagpaal in een stuk, transparant uitgeknipt.
- `assets/stam_top.png` / `assets/stam_mid.png` / `assets/stam_bottom.png` - de paal
  in drie stukken, zodat je hem op elke lengte kunt zetten (zie hieronder).
- `assets/stam_voorbeeld_lang.png` - voorbeeld van een langere paal (top + 5x mid + bottom).
- `assets/minitandwiel.png` - het roestige mini-tandwiel, transparante openingen,
  naaf exact in het midden van het plaatje (zodat je het schoon kunt ronddraaien).
- `tools/build_stam.py` - scriptje dat de drie paalstukken tot een paal van de
  gewenste hoogte stapelt.
- `spec.json` - de maten en ankerpunten op een rij.

## De stam lengte geven (bewerkbaar en schaalbaar)

De paal is opgebouwd zodat je hem langer of korter maakt zonder zichtbare naad:

1. Teken `stam_top.png` bovenaan (hierin zit de pen).
2. Herhaal `stam_mid.png` eronder net zo vaak als nodig om de gewenste hoogte te
   vullen. Dit middenstuk is naadloos gemaakt, dus je mag de kopieen gewoon tegen
   elkaar aan zetten.
3. Sluit onderaan af met `stam_bottom.png`.

De pen zit altijd bovenaan (in `stam_top.png`), dus die blijft op zijn plek hoe lang
je de paal ook maakt. Wil je het vooraf als een enkel plaatje: run
`python3 tools/build_stam.py <hoogte_in_px> uit.png`.

In de game kun je hetzelfde doen: top tekenen, mid herhalen om de hoogte te vullen,
bottom eronder. Zo is de hoogte een gewone parameter.

## Het mini-tandwiel laten draaien (in code, niet via Grok)

Het mini-tandwiel is een enkel sprite met de naaf precies in het midden van het
plaatje. Ronddraaien doe je door het sprite elke frame een paar graden om zijn eigen
midden te roteren. Op 60fps is dat volledig vloeiend; Grok is hier niet nodig en zou
juist onrustiger lopen.

- Draaipunt: het midden van `minitandwiel.png`.
- Plek: op de pen van de paal (zie `spec.json`, `peg_anchor`).
- Koppeling: draai mee met de platformbeweging (hoek evenredig aan de verplaatsing
  van het platform), zodat het lijkt alsof het de lift aandrijft. Richting en snelheid
  staan als suggestie in `spec.json`, pas gerust aan.
- Het grote wiel op de grond staat in dit voorbeeld stil.

## Opbouw en laagvolgorde (achter naar voor)

1. platform (achter de paal)
2. touw (vanaf de achterkant van het grote wiel, achter de paal langs)
3. groot tandwiel op de grond
4. de stam (paal) ervoor
5. mini-tandwiel op de pen, bovenop

De paal draagt de nabije kant van het platform. Het platform schuift in de animatie
verticaal langs de paal (de engine bepaalt de hoogte).
