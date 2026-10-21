# Kooiman - duw-mechaniek

> In deze repo: de 28 frames staan in `enemies/kooiman/duw/`, de losse kooi in
> `enemies/kooiman/kooi/kooi.png`, en de set is als `duw` toegevoegd aan
> `enemies/kooiman/sprites.json` (eigen canvas en de kooi-uitlijning onder `kooi_laag`).
> In de HTML is het de gevechts-loop van de **duel-kooiman** nadat de kooi open is (hij
> duwt de lege kooi voor zich uit als schild); hij is dan alleen in zijn herstel raakbaar.
> De voorbeeldbestanden zijn referentie: `preview/duw_preview.gif` en
> `bron/duw/voorbeeld_duw_met_kooi.png` (niet meegeleverd in de offline-download).

De kooiman verplaatst zich voortaan door de kooi voor zich uit te duwen. Deze duw-walk
vervangt zijn gewone loop. De kooi en de duw-animatie zitten BEWUST los van elkaar in
deze zip, zodat je de kooigrootte en -positie nog kunt bijstellen. De afbeelding is dus
niet ingebakken; er zit alleen een voorbeeld bij.

## Mapstructuur

```
kooiman/
  duw/           28 frames (loop)   ALLEEN de man, zonder kooi
  kooi/
    kooi.png     de rechtopstaande kooi, aparte laag
  metadata.json
voorbeeld/
  voorbeeld_duw_met_kooi.png   stilstaand voorbeeld van het eindresultaat
  voorbeeld_duwcyclus.gif      de hele cyclus als voorbeeld
```

Let op: de bestanden in `voorbeeld/` zijn ALLEEN ter referentie (zo hoort het eruit te
zien). Niet gebruiken als asset en niet inbakken. Gebruik de losse `duw/`-frames plus
`kooi/kooi.png`.

## Canvas en grondlijn

- canvas: 760 x 455
- grondlijn (voeten): y = 415
- anker-x (voeten): x = 509

## De kooi plaatsen (belangrijk)

De kooi is een APARTE statische laag voor de man, geen onderdeel van de man-frames.

1. Teken de kooi OVER de man. Dan valt zijn verre (achterste) hand achter de kooi en
   blijft zijn dichte (voorste) hand ervoor. Zo hoort het.
2. Horizontaal: zet de RECHTERRAND van de kooi OP HANDHOOGTE tegen zijn dichte-hand-
   contactpunt op canvas (262, 241). Gebruik de echte kooirand op die hoogte, NIET de
   breedste plek van de kooi. De koepel buigt naar binnen, dus op de breedste plek
   uitlijnen geeft een gat en dan lijkt hij lucht te duwen.
3. Verticaal: kooi-onderkant op de grondlijn y = 415.
4. Grootte: de bijgeleverde kooi is ~300 px hoog op deze man-schaal. Vrij aanpasbaar;
   daarom houden we 'm los. Als je de grootte wijzigt, herhaal stap 2 op de nieuwe
   handhoogte-rand.

## Gameplay

- **Bewegen:** de kooiman beweegt voortaan met deze duw-walk (kooi voor zich uit). Dit
  vervangt zijn oude loop.
- **Stofwolkjes:** maak stof bij zijn voeten (hij loopt) en logisch onderaan de kooi
  (zwaar object dat vooruit wordt geduwd). Dit zijn engine-effecten, geen sprites in deze
  zip.
- **Parry eruit, wel bewaren:** haal de bestaande parry van de kooiman uit zijn gedrag
  (niet meer actief), maar GOOI 'm niet weg; bewaar de parry-animatie/code voor later.
- **Niet raakbaar tijdens het duwen:** zolang hij de kooi voor zich uit duwt, kan hij
  NIET geraakt worden.
- **Wanneer wel kwetsbaar:** zodra de speler in slag-range komt, start de slag-animatie
  (zijn bestaande kooi-smash) en is hij kwetsbaar. Hij is eveneens kwetsbaar wanneer hij
  de kooi weer probeert op te tillen.
