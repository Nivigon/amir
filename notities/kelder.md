# De kelderzaal

Een level met `kelderZaal` speelt onder de grond. Alles staat in de HTML onder de kop
`// ---- de kelderzaal` (grep `KZAAL`, `kzaalReset`, `kzaalAchter`, `kzaalMidden`, `kzaalVoor`, `kzaalLichtNa`).
Test 86 is het proefstuk, de sandbox heeft de knop **Kelderzaal** onder De stad (zonder trap en bundel).
Het kelderluik op de straat (`kelder`, Stad 14) is iets anders: dat is de ingang. Die leidt nog niet naar dit level.

## Het veld

```
kelderZaal: { trap: {x}, plafond: {r}, palen: [x], deuren: [{x, bandiet}], bundel: true }
```

- `trap.x`: de voet van de houten trap. De trap loopt naar rechts omhoog (Amir loopt naar links, dus hij komt
  van boven). Zet `start` op de trap, het level begint erop (restart zet `ph` op de vloer onder de start).
- `plafond.r`: het rechtereind van het plafond; links ervan tot het eind van het level. Rechts ervan is het trapgat.
- `palen`: stutpalen (`binnen/paal_*`) van de vloer tot in het plafond.
- `deuren`: traliedeuren in de achterwand. `bandiet: true` is alleen een vlag voor de lezer: een deur heeft een vijand
  als er een spawn met `kgat: i` naar wijst.
- De kooi met een beest is geen deel van de kelderzaal meer: het is een gewone dierenkooi (`dierkooien` met `dier` en
  `open: 'bij'`, zie `notities/kooien.md`), zodat het overal dezelfde kooi is (bruin hout, galerijblad, doeken).
- `bundel`: de lichtbundel rechtsboven langs de trap, met stofjes.
- Het uitzicht: `lagen: 'kelder'` (de diepe nacht met gaten, warm in plaats van blauw). Daarnaast `stad` (leeg), voor de
  straattegel als vloer, en `fakkels` aan de muur.

## Hoe het werkt

- **Trap**: `trap_hout.png` gespiegeld. Onder de wang legt `kzaalReset` onzichtbare opstapjes (`look: 'geen'`,
  `opstap: true`, `kz: true`, elk `KZAAL.trap.stap` hoog) langs een looplijn `zak` bronpx onder de bovenrand.
  Een wereld-x is een schermpixel, dus de breedte schaalt met `nowScale()`: verandert het formaat, dan legt
  `kzaalUpdate` de treden opnieuw. Het plafond schuift daarbij mee (`kzaalPlafRechts`, `kzaalPlafR`): het begint nooit
  boven een stuk trap waar Amir er niet onder past. Zonder die klem was de trap op een laptop smaller en steiler dan het
  vaste `plafond.r` en liep Amir halverwege de trap met zijn hoofd tegen de rand van het plafond vast. De wang komt na Amir (`kzaalVoor`), zijn slagschaduw op de muur in `kzaalAchter`.
- **Plafond**: `plafond.png` als strook (`KZAAL.plafond`), met een zachte onderrand (het leem vloeit weg in de muur)
  en aarde erboven die naar het trapgat toe wegzakt. De botsing is een onzichtbare zwever (`look: 'geen'`) met de
  onderkant op de balkkoppen.
- **Traliedeur**: dicht, rammel (`deur.rammel` s, stof), breek (klap, gat, groot gat in `deur.fases`, dan open). Op de
  breuk: deurslag, schok, freeze, splinters (`wielSplinters`) en het kruis (`scherf_kruis.png`) dat groot naar de camera
  vliegt, draait en vervaagt (`kzaalLichtNa`). De spawn wacht tot de deur open is (`kzaalKlaar`) en komt in het gat.
  De ogen: wit met een pupil, niet gloeiend, volgen Amir en knipperen, alleen zolang er een vijand achter zit.
- **Kooi**: zie de dierenkooien (`notities/kooien.md`). Vroeger had de kelder een eigen kooi (`kooi.png`, `kooideur.png`,
  een lange regie met de wereld stil); die is weg.
- **Licht**: `kzaalMidden` meet de bundel, `donkerGatenNa` snijdt hem uit het donker (`kzaalGaten`), en `kzaalLichtNa`
  tekent de bundel, de lichtvlek en de stofjes erover.

## Plaatjes

`design/stad/kelder/binnen/`: `trap_hout.png`, `plafond.png`, `deur/deur_0_heel..deur_4_open.png`, `deur/scherf_kruis.png`,
Uit Grok (zie de projectdoc `kelder_overdracht.md`), verkleind voor het spel;
ze staan niet in de kleine set, het spel laadt de grote.

## Open

- Het kelderluik van Stad 14 leidt nog niet naar dit level.
- Een kooi met een schorpioen, en een hendel of bandiet die de kooi opent (zie `notities/kooien.md`).
- De bandiet stapt nu uit het gat; een sprong door de deur heen zou mooier zijn.
