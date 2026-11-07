# Licht op personages

`PLICHT`, `persLicht`, `plichtBronnen`, `plichtRand`

Eén systeem voor het licht dat op een personage valt. Na het tekenen van een personage roept zijn tekencode
`persLicht(img, x, y, w, h, flip, wx, vloer, fig, groundY, scale, cx, alfa)` aan met zijn frame zoals het op het
scherm staat. Dat doet twee dingen:

- **Een rand van licht.** `plichtBronnen` zoekt de bronnen bij hem en neemt de sterkste twee (`maxBron`). Van elk komt
  een warm randje aan de kant van de bron over zijn silhouet, met 'lighter'. Het randmasker is per frame, per kant en
  per breedte een keer gebakken (`plichtRand`, op `bak` px hoog) en daarna alleen ingekleurd, dus het kost per beeld weinig.
- **Het raam binnen.** De lichtbundel van een raam valt over het hele lijf (`binnenLichtOp`, zie "binnen" in
  `notities/stad.md`), geknipt op de vorm van de bundel. Zijn schaduw in de lichtvlek is alleen er voor Amir
  (`binnenBundelSchaduw`).

De bronnen nu:

- **zon**: alleen als hij laag staat (de hoogte `sun[1]` van het uitzicht onder `zon.laag`, vol na `zon.band`), maal het
  daglicht, maal hoeveel zon er op die plek valt (`amirZon`, dus niet onder de grond of onder rots), minder met `dim`
  (avond, nacht), en niet binnen. De kleur is die van de zon van het uitzicht, een eind naar wit (`zon.wit`). Bij de hoge
  middagzon van de stad (`stad_dag`) is hij er niet.
- **fakkel**: elke fakkel in `level.fakkels` binnen `fakkel.bereik` Amir, met de flikker van de vlam (`fakkelFlik`).
  In vol daglicht blijft er `fakkel.dag` van over, in het donker alles.
- **raam**: zie hierboven.

Een nieuwe bron (een vuurkorf, de flits van onweer, een rune die oplicht, de maan in een nachtlevel) is een blok in
`plichtBronnen` dat `{ soort, dir, sterk, kleur, rand, boven }` teruggeeft: `dir` -1 of 1, de kant op het scherm waar het
licht vandaan komt; `sterk` 0 tot 1; `rand` de breedte in Amir; `boven` hoeveel het ook van boven (positief) of van onder
(negatief) komt.

Bewust niet: een donkerlaag op personages (in een slagschaduw of in het donker). Dat maakt Amir en de vijanden slechter te
lezen, en in het donker zorgt de lichtkaart al voor het donker.

Aangesloten: Amir, de bandiet en de schildbandiet (elke laag apart). De andere vijanden nog niet: dat is per soort een
aanroep na zijn `drawImage`, met zijn frame op het scherm.

In de sandbox onder Beeld en geluid, **Licht op personages**: alles aan of uit, en per bron (Zon, Fakkel, Raam). Om te
bekijken: Tijd van de dag Ochtend of Avond (de zon), Decor, Fakkel, In het donker, en De stad, Huis met binnenkant.
