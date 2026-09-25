# De achtergrond doortrekken: ja, en dat is de betere volgorde

Nog steeds een mockup. Aan `amir-king-of-africa.html` is niets veranderd.

Je vraag was of we niet eerder de achtergrond eronder moeten doortrekken, en dan de rand
daar overheen laten lopen. Dat klopt, en het is structureel beter dan wat ik eerst deed.

## Waarom het beter is

De achtergrond houdt op de grondlijn op. `landFrom` vult tot `groundY` en geen pixel
verder, en daaronder ligt alleen de vlakke `bodemDonker()`. Kijk je in een ravijn, dan kijk
je dus in een gat in de tekening zelf, en ik loste dat in de vorige mockup op door er een
verzonnen donkere kleur in te zetten (`28,17,14` warm, `18,24,36` koud). Dat werkt, maar
die kleur komt nergens vandaan: hij hoort niet bij het uitzicht en moet met de hand
bijgesteld worden voor elke episode.

Trek je in plaats daarvan de landkleur door, dan klopt het vanzelf. Renew krijgt zijn
paarsrode diepte, Winter zijn koude leisteen, Dark Africa zijn bijna zwarte blauw, en als
iemand later een nieuw uitzicht toevoegt loopt het ravijn mee zonder dat er iets bij moet.
Het `dim`-veld en de lichtlaag werken er ook meteen op.

Belangrijk: alleen het **verloop** doortrekken, niet de bergpanelen. Een verloop heeft geen
horizontale vorm, dus er schuift niets mee met de parallax. Trek je de panelen door, dan
heb je het probleem uit de analyse terug: de "overkant" beweegt ten opzichte van het gat
waar hij in hoort te liggen.

## Wat ik heb moeten bijstellen

Dat is de middelste strook in `voorbeeld2-renew6.png`. De landkleur zomaar doortrekken is
te licht en te blauw: het leest als lucht achter een gleuf, alsof het ravijn dwars door de
wereld is gezaagd. Je hoort in een gat te kijken, niet erdoorheen.

Twee correcties maken het af, allebei op dezelfde kleur:

1. **Meteen wegzakken.** Niet geleidelijk over de hele diepte, maar vanaf de grondlijn al
   op ongeveer 38 procent naar zwart, halverwege 70, onderin 90. De diepte gebeurt op het
   stuk dat je werkelijk ziet.
2. **Half naar de grondkleur toe.** De landkleur gemengd met `bodemDonker()`, fiftyfifty.
   De kleur komt nog steeds uit het uitzicht, maar het is aarde en geen hemel.

Daarna loopt de wand er met een verloop uit omhoog (dat is jouw "dat het overloopt"): over
ongeveer een derde Amir gaat de bovenkant van de overkant over in die diepte, zodat hij uit
de schaduw omhoog komt in plaats van ertegenaan geplakt te liggen. En naar beneden lost hij
op in precies dezelfde kleur waar de doorgetrokken achtergrond ook op uitkomt, dus daar zit
nergens een overgang.

## Volgorde van tekenen

Dit is dan de volgorde, en die is anders dan nu:

1. achtergrond, tot aan de grondlijn zoals nu;
2. **de landkleur doorgetrokken onder de grondlijn, verdiept** (nieuw);
3. de vlakke bodemvulling, nu met de gaten eruit geknipt;
4. de grondtegel, met de gaten eruit geknipt, zoals nu;
5. per gat: de overkant, met zijn bovenkant overlopend in stap 2, en naar beneden oplossend
   in dezelfde diepte;
6. de rand waar je op staat: dikte met een grillige onderkant, plus zijn slagschaduw.

Stap 2 is trouwens ook precies wat `diepGesteente` nu met de hand nabootst voor als de
camera onder de grondlijn zakt. Die zou erop kunnen gaan leunen in plaats van zijn eigen
tegelwerk te doen.

| bestand | wat |
| --- | --- |
| `voorbeeld2-renew6.png` | vier standen onder elkaar: voor, doorgetrokken, doorgetrokken en verdiept, en de vorige poging met een vaste kleur |
| `voorbeeld2-dark1.png` | voor en na, Dark Africa 1 |
| `voorbeeld2-winter2.png` | voor en na, Winter 2 |
| `voorbeeld2-heelbeeld.png` | voor en na, het hele scherm |
