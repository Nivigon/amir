# Sneak: de sluipaanval, gehoor en de argwaanklok

Kop in de HTML: `// ---- sneak: de sluipaanval, gehoor en de argwaanklok (level.sneak, zie notities/sneak.md) ----`,
direct na `zichtTeken` en voor `TRIGGER`. Grep: `SNEAK`, `sneakAan`, `sneakKan`, `sneakDoe`, `sneakRust`, `lawaaiPuls`,
`sneakHoort`, `sneakOogTeken`, `sneakPatStap`.

## Wat het is

Met `sneak: true` in een level (naast `zicht: true`, zonder zicht doet het niets) kan Amir een vijand die hem
niet opgemerkt heeft van achteren in een klap doden. Het bouwt op het zicht (`notities/zicht.md`): een vijand
begint in rust (`s.zWacht`) en wordt wakker als hij Amir ziet. Het zicht had achter zijn rug nog de oude
afstand (een half scherm op zijn niveau), dus van achteren naderen kon niet. De sluipaanval vervangt dat
achterbereik door gehoor, alleen voor de mens-vijanden: bandiet, schildbandiet, kooiman, meelman,
kruisboogbandiet en zweepman (`oog === 'mens'` in `vijandZiet`, dat zet `s.sMens`). Slangen, schorpioenen,
hyena's en de panter kijken zoals ze deden; een baas doet niet mee.

## Gehoor (`lawaai`, `lawaaiPuls`, `sneakHoort`)

Elk beeld zet de hoofdlus `lawaai`: hoe ver Amirs voetstappen nu dragen (`lawaaiNu`). Kruipen en stilstaan zijn
stil, lopen draagt `SNEAK.gehoor.loop` (1,8 Amir, net buiten steekafstand), in de lucht hetzelfde, sprinten (en de
renstoot) tot het oude zichtbereik (`zichtBereik(1100)`). Een vijand in rust hoort je als je binnen die afstand op
zijn niveau staat (`zichtNiveau`). Daarnaast zijn er pulsen op een plek (`lawaaiPulsen`, `SNEAK.puls`, elk
`duur` 0,35 s): het loslaten van een speer (klein, alleen vlakbij te horen, zodat een worp van achteren kan),
een treffer op een vijand (in elke `hitX` en in `enemyTakeHit`, `hitHyena`), een klap op Amir (`hurtPlayer`),
een speer die neerkomt (`javStick`) en een sluipkill (klein). Een puls gaat door hoogte heen. Alles staat in
Amir (`sneakPx`), want de steek reikt op een telefoon minder pixels dan op een laptop, en de maten schalen mee.
Voor hem geldt gewoon het zicht; lawaai hoort hij ook als je voor hem buiten zijn halve cirkel staat.

## De argwaanklok (`sneakRust`)

Sta je onopgemerkt achter een vijand binnen `SNEAK.argwaan.bereik` (2,4 Amir) op zijn niveau, dan loopt een klok
(`s.sArg`, 0 tot 1): aan de rand `van` (3,6 s), pal achter hem `tot` (1,8 s), lineair ertussen. Vol, dan draait hij
zich om (`s.sKijk`, `kijk` 0,8 s). Ziet hij je dan (de gewone zichtlijn, een kei verbergt niet), dan is hij wakker;
anders draait hij terug en loopt de klok na `rust` (0,6 s) opnieuw. Loop je weg, dan zakt de klok weer. Dit is het
tijdraam: lopen tot net buiten gehoor, bukken, een stukje kruipen en steken duurt zo'n 1,5 s, de klok op die afstand
geeft ongeveer 3 s. Wie treuzelt wordt gezien. Lion's Patience verdubbelt de klok.

`sneakRust` zit in `zichtWaak` (bandiet, schildbandiet, kooiman, zweepman, alleen in rust en alleen voor `'mens'`)
en los in `updateMeelman` en `updateKruisboog`, die hun "ziet" zelf uitrekenen en hun rust via `zichtWaakMet`
bijhouden. De kruisboogbandiet staat met de sluipaanval in rust stil in zijn mikhouding in plaats van naar Amir toe
te lopen, en draait zich in rust niet naar hem toe.

## Rust-variatie (spawnvlaggen)

- `rug: true`: hij staat met zijn rug naar de kant waar Amir vandaan komt (`zichtZet`: `face` van Amir af).
- `draai: n`: in rust draait hij zich om de `n` seconden om, met `SNEAK.draaiSpreiding` (35%) speling, zodat je
  het niet op de tel kunt lopen. Kijkt hij dan jouw kant op, dan geldt het gewone zicht.
- `pat: true` (alleen de bandiet): hij loopt in rust heen en weer om zijn plek (`sneakPatStap`, de staande
  loop-set `walk`), `SNEAK.pat.breed` (1,8 Amir) aan elke kant, op `tempo` (0,45) van zijn rensnelheid, met een
  pauze aan elk keerpunt; een kei, een rand of een ravijn keert hem ook (regel 7, `banMove`, `dropAhead`).

Zonder vlaggen staat hij zoals altijd met zijn gezicht naar Amir en is er niets te sluipen: de rug moet uit het
level komen (een vlag, of een route van boven langs hem heen). De hinderlaag-bandiet (`hurk`) houdt zijn eigen
gehoor (`banAmbushRange`) en doet niet mee.

## De sluipaanval zelf (`sneakKan`, `sneakDoe`)

`sneakKan(s)`: een mens-vijand met de sluipaanval aan, in rust (`s.zWacht`), niet net omkijkend, en Amir aan de
kant van zijn rug (`Math.sign(playerX() - s.x) !== s.face`). Elke `hitX` van de zes vraagt het bovenin: is het
een sluipaanval, dan `sneakDoe` (de ster, hitstop en shake van een crit via `critFx`, de kleine puls, de melding
"Sluipaanval!", `sneakKills`) en `s.hp = 1` voor de klap, zodat de treffer dodelijk is. De schildbandiet verliest
het schild en sterft met `schbSterf` (geen executie). De kooiman is alleen in zijn herstel raakbaar; de lus kijkt
daarom ook naar `sneakKan` (`raak = kooiRaakbaar(s) || sneakKan(s)`). De zweepman slaat met een sluipkill zijn
fase 2 (de arm eraf) over. Steek, worp en lage zwaai tellen alle drie; de worp van achteren van buiten zijn gehoor
is de stille optie.

## Het oog (`sneakOogTeken`)

Boven elke mens-vijand die zo speelt (vanuit `vijandHpBalk` en `schildHpBalk`, ook zonder de balk): in rust een
dicht oog, met de argwaan als een gele boog die eromheen volloopt; kijkt hij om, dan een vraagteken; is hij net
wakker, dan `SNEAK.wakker` (0,7 s) een rood uitroepteken. Zo leest de speler het raam.

## Talents (tijdelijk)

- **Soft Step** (Mkuki, `soft_step`, `factor` 0,5): de voetstappen dragen half zo ver; pulsen niet.
- **Lion's Patience** (Bhubesi, `lions_patience`, `factor` 2): de argwaanklok loopt half zo snel.

Beide achteraan in hun tree, dus na het vierde uitgespeelde level. Het zijn plaatshouders tot de echte sluip-tree
er is; een echte zou Impungushe en het mes de kans geven om van achteren dodelijk te zijn (het mes doodt nu niets).

## Sandbox

Onder Vijanden, de rij **Sluipaanval**: **Sluipaanval** (`sbsneak`, zet Zicht mee aan), **Rug naar Amir**,
**Draait om** (nee, 4, 8, 15 s) en **Patrouille** zijn de spawnvlaggen voor elke vijand die je daarna neerzet
(`sbSneakSpawn` in `sbSpawn`), **Toon gehoor** (`sneakToon`, `sneakTeken`) tekent de strook op je vloer tot waar je
voetstappen dragen en de pulsen als ringen. Soft Step en Lion's Patience staan bij hun tribe onder Speer.

## Nagemeten

In Chromium op 1280x720 (reikwijdte van de steek op een bandiet 280 wereld-px, lopend gehoord op 315) en op 852x393
(160 en 177): lopen tot net buiten gehoor, bukken, kruipen tot steekafstand en steken is op alle zes een sluipkill
(de argwaan staat dan op zo'n 0,8); de worp van buiten zijn gehoor ook; sprintend hoort hij je van ver, met Soft
Step op de helft; stil achter hem blijven staan en hij kijkt na 1,9 s (oude klok) om en ziet je; een bandiet met
`draai: 4` draait om de 3 tot 5 s; de patrouille loopt heen en weer en ziet je aan het keerpunt als je in beeld
staat. Geen console-fouten. Geen bestaand level heeft `sneak`.
