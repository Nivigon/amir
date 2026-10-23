# Runes op elke rots

### Runes op elke rots, op elke hoogte

Een rune hoeft niet op de scheve spits op 190 te zitten: `rots`, `groot` en `hoog` zetten hem op een
andere plaat (`RUNE_ROTSEN`, alle met een witte achtergrond door `witKnip`, per plaat geladen in
`runeBeeld`), op een andere maat en op een andere hoogte. De schijf komt op de flank aan Amirs kant
(`ravijnRune` zoekt op die hoogte de rand van het steen in de alfa), en nooit hoger dan zijn eigen
rots min twee stralen (`runeHoog`). Een rune zonder die velden is precies wat hij was.

Hoe hoog is goed? Amir haalt springend 1,83; alles daarboven moet je raken met een worp. Hoe hoger,
hoe verder je moet staan, en de camera staat op Amir: op 1280 bij 720 zie je 640 px voor je uit, en
vanaf ongeveer 2,1 Amir begint de strook waar je hem raakt pas buiten beeld. Dat rekent `runeStroken`
uit, met dezelfde stappen als de speer in het spel en met de worpen van het level (de twee trappen,
of met `worp: 'schaal'` elke hoek tot 30 graden). Het venster in de bouwer laat de strook zien en
waarschuwt als hij leeg is of buiten beeld begint.

Een speer die in een rots vertrekt (Amir loopt door de rotsen heen) blijft pas in het steen steken
als hij er eerst uit is geweest (`jav.rotsUit`), net als bij de grot met de kei. Een speer die na `JAV.muurT` uit
het steen schiet, valt door de rots heen tot op de grond (alleen een vliegende speer blijft in een
runerots steken): anders raakt hij de flank eronder, die naar beneden breder wordt, en zit hij een
stukje lager weer vast. Een vallende speer zet ook geen rune aan.

Met `doel: true` is een rune een doel: raken zet hem aan (`runeGeraakt`), met een felle gloed die in
`RAVIJN_RUNE.flits` wegzakt (`runeFlits`), en hij blijft aan tot je opnieuw begint.

**Een doel dat iets doet.** Een doel met `ravijn`, `sluit`, `muur` of `speerval` doet bij een treffer wat
een zegel met die velden doet (`runeDoet`, met dezelfde functies als het zegel: `zegelDoe`, `zegelSluit`,
`speervalZegel`; de hint zegt dan "De rune", `zegelWie`). Een `ravijn` van een doel telt mee in
`komendeRavijnen` en in `levelcheck.py`, net als dat van een zegel.

**De rots staat op zijn vloer.** `ravijnRotsMaat` geeft `b`, de vloer onder het midden van de plaat
(`terrainH`): op een terras erop, in een gang op de bodem. De hoogte van de schijf (`hoog`), de alfa van
de speer (`ravijnRotsVol`) en het tekenen tellen vanaf daar. Alle runes in de bestaande levels staan op 0,
dus daar verandert niets. In een gang moet de rots onder het dak passen (`groot` kleiner dan `diep` min
`HOLTE_DAK`); `levelcheck.py` meldt het als hij erdoorheen steekt.

**Opstellingen.** Wat gemeten is staat als bouwsteen in `RUNE_OPSTELLINGEN`: `vlak`, `zuilen`, `boog`, `kei`,
`terras`, `gang` en `ver`, elk met `rots`, `groot`, `hoog` (en `kei`), een naam en de strook waar je hem raakt.
Een rune met `opstelling: 'kei'` krijgt die maten (`runeIn`); wat er zelf bij staat gaat voor, en `runeUit` laat
weg wat gelijk is aan de opstelling. In de bouwer kies je hem in het venster van een rune (`doel`), samen met wat
hij doet (`runeVeldZet`: ravijn, sluit, muur, speerval of rijs, de x, de breedte, de naam van de rijzende grond en
de kei). In de sandbox wisselt **Opstelling** (`sbRuneOpst`) wat een nieuwe rune krijgt. `levelcheck.py` geeft een
FOUT bij een opstelling die niet bestaat.

**Een kei bij de rune.** Een rots en de worp schalen mee met Amir en dus met het scherm, een kei op een
vaste x niet. Een kei die je nodig hebt om een hoge rune te raken, lag daardoor op 1920 bij 1080 in de rots
en op een telefoon te ver. Met `kei` (in Amir) legt `runeKeiZet` hem elk beeld op die afstand voor de
schijf, in `level.rocks` met `runeKei`; `syncLevel` schrijft hem niet weg. Let op wat er op zijn plek ligt:
op elk scherm ergens anders (in Test 28 lag hij op 1920 eerst op het zegel). Test 28 is het proefstuk:
vier hoge runes, op de grond met en zonder kei, op een terras en in een gang, nagelopen op 1280 bij 720,
1920 bij 1080 en 852 bij 393.

**Van waar je raakt.** `runeStroken` rekent vanaf de vloer op elke afstand, en die vloer kan een kei of
terras zijn (`javFloor`, met alle keien van het level), en de speer botst daarbij zoals in het spel. De
tabel per rots en per hoogte, vanaf de vloer en vanaf een kei, staat in `notities/combinaties.md`. In de
sandbox kiest de knop Doet (`SB_RUNE_DOET`) wat een nieuwe rune doet, en zegt de hint vanaf hoe ver je hem
raakt.

**Een speer in een runeschijf blijft vastzitten, punt.** Dat geldt voor elke houten schijf: de rune op
een rots, de rotswand en de grot. Bij een treffer wordt de speer meteen decor van de rune
(`runeSperen`, in `ravijnRuneTreffer`), net als `muurSpeer` bij de rotswand: E doet er niets, en Amir
heeft geen speer meer. Het spel geeft er niet vanzelf een nieuwe voor; dat regelt het level, met een
skelet of met de speerplek bij de rotswand (`muurVul`). Een level zonder nieuwe speer na een rune is
dus een keuze, en kan juist de uitdaging zijn: zet er een neer als de speler er daarna nog een nodig
heeft. Test 9 en Test 12 hebben er een skelet voor. Test 12 is het proefstuk: vijf rotsen, en na elke rots een
skelet voor een nieuwe speer.

**Het licht op een runerots** komt van dezelfde zon als de rest (`RUNE_LICHT`). Net als bij de
lichtkaart gaat er uit elk punt van de rots een straal naar de zon (`LK.zonHoek`, aan de kant van
`zonRechts`), en telt hoe ver die door het steen moet (`runeLichtMaak`). Kort: een warme rand, met
`soft-light` zodat licht steen niet wit wordt. Diep (tot `diep`, ongeveer de breedte van een zuil):
schaduw. In een kier zakt die weg maar langzaam weg (`lucht`), anders licht een losse kei aan de
schaduwkant op. Op de grond valt een slagschaduw naar de andere kant (`runeGrondSchaduw`), in de
sneeuw blauwig. De sterkte volgt de gloed van het uitzicht, met `nacht` als ondergrens. De maskers
worden een keer per plaat, kant en maat uitgerekend (zo'n 20 ms), een rots per beeld vanaf het begin
van het level, dus voor je er bent. De grijze schaduwvloer onder de keien in de platen gaat er bij het
laden uit (`RAVIJN_ROTS.voet` in `witKnip`); zonder dat lag er een grijze strook op de grond.

De maten van een rots hangen aan Amir en dus aan het scherm, en een level niet: op 1920 bij 1080
is een rots van 5 Amir ruim 2000 px breed. Laat tussen de rotsen genoeg ruimte voor het grootste
scherm, anders sta je om te gooien in de vorige rots.
