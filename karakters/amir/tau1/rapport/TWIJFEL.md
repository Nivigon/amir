# Tau 1: twijfelgevallen (nachtrun 22-11-2026)

## Krassen (losse laag, per frame te verschuiven)
- De krassen zitten niet in de frames maar in `krassen/<frame>_kras.png`, met de startplek in `tau1/krassen_plaatsing.json`.
  Mijn plek is een automatische schatting op de dij; loop ze per frame na.
- Rennen: ze staan op hetzelfde fysieke been (zijn linkerbeen). In de originele ren is de schaduw van de benen in de
  tweede helft niet consequent, dus in 6 tot en met 11 is het gekraste been soms het donkerdere. Kan als springen
  lezen; per frame bijschuiven of het been in de ren-bron donker/licht rechtzetten.
- Springen: in frame 1 (hurk) en 6 (landing) ligt de dij bijna horizontaal; de krassen staan daar op de schatting.
- Rollen: nog GEEN krassen geplaatst (in de rol draait het been rond; liever met de hand in de tool dan een gok).

## Kap
- Rol 8 tot en met 10 (handstand naar voren): de kap is heel klein in beeld en zit half onder de vacht. Leest goed,
  maar kijk of de tanden niet te druk zijn.
- Staan: de vacht komt hier uit Grok (de kap groeit eruit), dus de oogvlekjes op de vacht zijn weg; in rennen,
  springen en rollen is de vacht het origineel (met vlekjes). Kleine stijlbreuk tussen staan en de rest.
- Ogen: zacht amber in het beeld; feller gloeien is voor de code.

## Overig
- rennen_03: het originele frame had een gat in de broek (Tom zag het). In Tau 1 gerepareerd met Grok
  (`bron/rennen_03_hersteld.png`). Het gewone spel heeft het gat nog: zelfde reparatie kan daar ook in.
- Zonekaart: de kap is vacht-zone (groen), tanden wit, ogen oranje. De broek is overal het origineel, dus de
  broek-zone volgt de paarse kleur; een paar pixels donkere schaduw vallen erbuiten.

## Stoksets (nacht 22 op 23 nov)

- Geen krassen in bukken, sluipen, slag, stapslag, slag2, laag, draaislag, draaiterug, blok en grondklap: `dij.json`
  heeft voor die sets nog geen dijlijn. Wil je ze erin, dan per set een dijlijn zetten en `tau.maak` opnieuw draaien.
- Draaislag 10 tot 14 en draaiterug 0 en 1 zijn rugaanzichten: alleen de achterkant van de kap, geen ogen of tanden.
  Draaiterug 2 houdt het profiel. Kijk of de overgang in de draai goed leest.
- Grondklap 17: IoU 0,80 (de stok voor het hoofd), de kap zelf lijkt goed, wel even nakijken in de gif.
- De kap is per vel van zes frames door Grok getekend, dus binnen een vel is hij gelijk, maar tussen twee vellen kan
  de vorm iets verspringen (bijvoorbeeld stapslag 2 naar 3). In de gifs is dat te zien als een klein sprongetje.
