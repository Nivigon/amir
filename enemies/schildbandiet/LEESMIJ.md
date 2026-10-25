# Schildbandiet (block and kill)

Vijand voor Amir, King of Africa. Hij loopt dreigend op Amir af met een houten schild op,
en valt aan door te springen. Alles wordt getekend uit lagen: het schild is een los
plaatje op het lijf, en de dood en de executie komen uit een tweede set lagen.

## Bestanden

- `lagen.json`             loop, strike en flinch: per beweging, per frame, per schildstaat de lagen in
                           tekenvolgorde (zie `LEESMIJ_lagen.md`)
- `lagen/lijf/`            de lijf-plaatjes (116), elk een keer, bijgesneden tot zijn eigen randen
- `lagen/schild/`          de schild-plaatjes (81): heel, een hap eruit, twee happen
- `executie/executie.json` knielen, wankel, val en de special execution (zie `executie/LEESMIJ.md`)
- `executie/lagen/`        de plaatjes daarvan (127)
- `klein/enemies/schildbandiet/` dezelfde lagen op halve grootte (`tools/gen-klein.py`)

Alle lagen staan op hetzelfde canvas (544x860) met dezelfde grondlijn (781) en anchorX
(272): `dx`, `dy` in een json is de linkerbovenhoek van de laag ten opzichte daarvan, in
pixels van de grote set. Kijkrichting is naar links; spiegel in code voor naar rechts.

## Gedrag

1. Hij loopt op Amir af met schild op (`loop`, 10 fps).
2. Amir raakt hem: witte flits, houtklap en houtsnippers, en hij speelt de flinch: hij
   twist even naar de camera en schuift een klein stukje naar achteren (knockback) met een
   stofwolk aan zijn voeten. Elke treffer slaat zichtbaar een hap uit het schild (de
   schildstaat: metschild, fase1, fase2, zonderschild).
3. Na de derde treffer is het schild weg: loop, strike en flinch spelen dan de staat
   `zonderschild`. Vanaf nu is hij in een klap dood.
4. Zodra hij bij Amir staat, valt hij aan met de sprong-aanval (`strike`): hij zakt diep
   door zijn knieen (de tell), springt naar de plek waar Amir stond (dan is hij
   onstuitbaar en onaantastbaar) en landt met zijn speer. De sprongboog zit in de
   frames, de horizontale verplaatsing doet de engine.
5. De dood: hij knielt en valt voorover (`knielen`, `val` uit `executie.json`), of het
   wordt de special execution (steek 1 op 5, worp 1 op 3). Zie `executie/LEESMIJ.md`.

## Timing

De frameduur per beweging staat in de json's (`durations_ms`); het spel gebruikt voor de
strike en de flinch zijn eigen, afgestemde tijden (`SCHB.strikeDur`, `SCHB.flinchDur` in de
HTML) en voor de executie `EXE.exeDur`.

## Geschiedenis

Tot 25-10-2026 stonden hier complete sets per schildstand (`loop_metschild`,
`strike_fase1`, ...), een eigen dood-set (`dood/`) en een losse speer (`speer/`), met
`metadata.json` erbij. Die zijn vervangen door de lagen en weggehaald.
