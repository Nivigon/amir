# De laag doortrekken tot de plantjes, en die band weghalen

Nog steeds een mockup. Aan `amir-king-of-africa.html` is niets veranderd.

Je hebt gelijk, twee keer.

## 1. De donkere band is onnodig

Die band is `bodemDonker()`: een vlakke vulling van `groundY` naar beneden over de volle
breedte van het scherm. De grondtegel erna wordt wel uit de gaten geknipt, die vulling niet.
Knip je hem met dezelfde `evenodd`-clip ook uit de gaten, dan is hij weg en is er verder
niets voor in de plaats nodig.

## 2. Er moet wel iets doorlopen, anders kijk je door het canvas heen

Onder de grondlijn is niets getekend: de achtergrond stopt daar. Haal je alleen de band
weg, dan kijk je in dat lege stuk. In de mockup was dat meteen te zien als een paarsgrijze
plak achter de randtegel, want dat is de kleur van de pagina.

Dus: de laag die er ligt moet doorlopen, precies zoals je zegt, tot aan de plantjes van de
overkant. Daarna hoeft er geen aparte rand met dikte en geen slagschaduw meer overheen.

## Welke laag je doortrekt, maakt uit

Dat is stand 1 tegen stand 2 in `voorbeeld3-renew6.png`.

**Stand 1, de landkleur doortrekken.** Dat was mijn eerste poging. Het werkt, maar er blijft
een donkerblauwe streep boven de rand staan. `sc.land` is in Renew 6 een diep paars, terwijl
wat er op de grondlijn werkelijk ligt de onderkant van het dichtstbijzijnde heuvelpaneel is,
en dat is roodbruin. Je trekt dus de verkeerde laag door, en de streep is precies het
verschil tussen die twee.

**Stand 2, doortrekken wat er werkelijk ligt.** Een regel pixels net boven de grondlijn
kopiëren en naar beneden uitrekken, en daarna laten wegzakken. Per kolom dezelfde kleur, dus
er is geen overgang, wat er ook in de achtergrond staat. Heuvels, water, nevel, een ander
uitzicht, een nieuw level: het klopt vanzelf, en er hoeft nergens een kleur geraden te worden.

    ctx.drawImage(cv, 0, (groundY - 2) * DPR, W * DPR, 1, 0, groundY - 1, W, D + 2);

Dat is de hele truc: het canvas tekent zijn eigen regel opnieuw. Het moet wel vóór de
bodemvulling gebeuren, want op dat moment staat de achtergrond er al en de grond nog niet.
De `* DPR` is nodig omdat `drawImage` de bronpixels van het canvas pakt en het canvas op een
telefoon groter is dan `W` bij `H`. Sla je dat over, dan pakt hij de verkeerde regel.

Verder geen slagschaduw en geen eigen rand. Alleen daarna wegzakken, zodat het gat niet
als een gelijkmatig verlichte plaat blijft liggen.

## Wat er in stand 2 nog meer in zit

Twee dingen uit de analyse, allebei alleen kleur, geen opbouw:

- **Het steen omgeverfd.** Een `color`-blend in plaats van de platte vulling van 28 procent:
  tint en verzadiging van de grond, helderheid van het steen. Daarmee is de wand aarde in
  plaats van lila, en is de bleke streep bovenop de rand getemperd.
- **De diepte op het zichtbare stuk.** De nevel en het donker lopen nu tot anderhalve Amir
  onder de grondlijn, en daar kijk je nooit. Ze omzetten naar de zichtbare band (`groundY`
  tot de onderrand van het beeld) is het verschil tussen een vlakke plaat en een gat.

Wil je alleen jouw punt en verder niets, dan is dat stand 1 zonder die twee: band eruit
knippen, doortrekken, klaar. De twee kleurdingen staan er los van en kunnen later.

| bestand | wat |
| --- | --- |
| `voorbeeld3-renew6.png` | voor, stand 1, stand 2, en de zware versie van daarnet die dus niet nodig is |
| `voorbeeld3-dark1.png` | voor en na, Dark Africa 1 |
| `voorbeeld3-winter2.png` | voor en na, Winter 2 |
| `voorbeeld3-heelbeeld.png` | voor en na, het hele scherm |
