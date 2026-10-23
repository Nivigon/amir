# Bodem en sneeuwdek

### Bodem en sneeuwdek: grijs en rood zijn twee verschillende dingen

`winter: true` is de complete uitrusting van episode Winter World: witte dieren, sneeuw
op alles wat je beklimt, en een grond waarin sneeuw en grijze steen in één tegel zijn
gebakken. Dat is de bergversie en die blijft zoals hij is.

Het veld `sneeuw` beantwoordt een andere vraag: ligt hier sneeuw op de grond, en op wat
voor grond. Twee dingen die los van elkaar staan:

| | |
| --- | --- |
| `soort: 'savanne'` | de rode grond van de savanne, en die blijft rood onder de sneeuw |
| `soort: 'rots'` | dezelfde grond als grijze steen: een rotsbodem, ook zonder sneeuw |
| `dek` | hoeveel sneeuw er ligt, 0 tot 1 (standaard 1) |
| `van` en `tot` | alleen samen: het dek loopt op van niets op `van` tot vol op `tot` |

Kies dus bewust. Grijs is een steensoort, geen gevolg van sneeuw: een ondergesneeuwde
zandvlakte is onder die sneeuw nog altijd rood zand, en dat zie je ook, want het dek
laat overal plekken grond vrij. Vraagt iemand om een besneeuwd savannelevel, dan is dat
`soort: 'savanne'`; gaat het om een kale steenvlakte of een hoogvlakte, dan `'rots'`.

Amir loopt naar links, dus `tot` is negatiever dan `van`:

```
sneeuw: { soort: 'savanne', van: -1200, tot: -7000 }
```

Het dek zelf zijn vier doorzichtige lagen (`design/sneeuwlaag_25` tot `100`) die genest
zijn: wat op 25 wit is, is dat op 50 ook. De overgang van de ene stand naar de volgende
is daardoor alleen sneeuw die erbij komt, en die grens loopt grillig, zodat je nergens
een rechte streep over de grond ziet. Zet je een nieuwe stand bij, houd die nesting dan
intact, anders knippert er sneeuw weg terwijl je loopt.

Wat nu nog niet meeloopt: de rotsen, de klimstukken, het gras en de dieren hebben alleen
een aan-of-uit sneeuwversie. Loop je door een overgang, dan springen die er in één keer
om. Dat is bewust buiten deze wijziging gelaten.

`schoonLevel` kijkt elk level bij het laden na en schuift decor dat boven een ravijn
staat naar de kant, of haalt het weg (behalve binnen een gang: daar staat het op de bodem). Reken daar niet op als ontwerper: zet het
meteen goed.
