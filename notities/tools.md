# De tools (volledige uitleg)

## Levels nakijken: tools/levelcheck.py

Na elk nieuw level, en na elke wijziging aan een level, draai je:

```
python3 tools/levelcheck.py            alle levels
python3 tools/levelcheck.py "Test 4"   alleen de levels waarvan de naam dit bevat
python3 tools/levelcheck.py -v         ook de info-regels
python3 tools/levelcheck.py level.json een level uit de bouwer, voor het in de HTML staat
```

Het script leest de leveldefinities uit de HTML, samen met de getallen waar het spel
zelf mee rekent (`CHAR_H`, `JUMP_V`, `GRAVITY`, de loopsnelheid en de sprint, `PLAFOND_WEG`,
de maten van keien, klif en fakkels). Het verandert niets aan de levels, het meldt alleen.
FOUT betekent: stuk, of tegen een regel uit dit document in. LET OP betekent: het werkt,
maar krap, of het spel lost het stilletjes voor je op. Een nieuw level gaat pas de deur uit
zonder FOUT. Wat het nakijkt: velden die `readLevel` niet kent, vaste dingen waar later een ravijn
openscheurt, ravijnen tegen de echte
sprong (met het plafond en het water erbij), decor boven een ravijn met dezelfde maten als
`schoonLevel`, het plafond boven keien en treden, rechtop kunnen lopen, of elke trede met
een sprong, een richel, een kei, de rijzende grond of een sprong van een buurterras over een dodelijk gat te halen is, of de klif achter de fakkels staat, alles
rond een gang onder de grond (zie "hoogteverschil onder de grond"), of er na een rune een doornbos voor het
volgende skelet staat (`speer na een rune`), en met `valschade` of Amir
de vallen langs de route overleeft.

**De sprong.** `JUMP_V` en `GRAVITY` geven op papier 208, maar het spel rekent per beeld (eerst
de zwaartekracht, dan de hoogte), en dan komt hij lager uit: op 60 beelden per seconde 200, op het
traagste toestel (het spel neemt hoogstens 0,05 seconde per beeld) 184. Gemeten: een trede van
199 haalt hij, een van 203 niet. Het script rekent daarom met 200, en de sprong over een ravijn
ook per beeld.

**De route.** Voor de vallen loopt het script het level af zoals een speler dat doet: naar links,
over een gewoon ravijn springend, tegen een wand of kei op, en van een rand af op looptempo. Van
een kei of een richel springt hij liever dan dat hij valt, als hij dan hoger uitkomt. Waar hij
neerkomt rekent het per beeld uit, dus een val van een terras op een lagere trede die net verderop
begint, telt als de kleine stap die het in het spel ook is.

Maten die aan het scherm hangen rekent het uit voor 1280 bij 720 op Formaat 25; met `--hoog`
en `--formaat` kijk je een ander scherm na.

**Meldt iemand iets in een level dat niet samen kan** (een laag plafond boven een kei om op
te springen, een poel vlak voor een ravijn), dan komt dat er als regel bij: een functie met
`@regel('naam')` in `tools/levelcheck.py`, met de getallen uit de code en niet uit het hoofd.
Draai daarna alle levels opnieuw en meld wat de nieuwe regel in de bestaande levels vindt,
zonder die levels aan te passen (regel 1).

## De speelrobot: tools/speelrobot.js

`levelcheck.py` rekent, de speelrobot speelt. Hij laadt het echte spel in Chromium, zet een level
klaar en loopt het naar links uit op een vaste 60 beelden per seconde, los van hoe snel de
computer is. Hij springt als hij vastloopt, springt over een ravijn zonder gang eronder, laat zich
in een ingang vallen, pakt zijn speer, steekt naar doornbossen en vijanden voor hem, en blijft op
een kei staan om er vanaf te springen. Hij meldt waar hij landt, wat een val kost, waar hij
vastloopt en wat er in de console staat.

```
node tools/speelrobot.js "Test 4"               een level uit de HTML, op naam
node tools/speelrobot.js level.json --taai      een level uit de bouwer; --taai: levens komen terug
node tools/speelrobot.js "Test 4" --shots map   elke anderhalve seconde een schermafdruk
node tools/speelrobot.js level.json --vredig --wacht -1490:12
                                                op -1490 twaalf seconden blijven staan, zonder te steken
```

Regel 7 kijkt hij altijd na: per vijand onthoudt hij aan welke kant van elke kei en elk ravijn
die stond, en komt hij aan de andere kant terecht, dan staat er `REGEL 7` in de uitvoer. Met
`--wacht` laat je Amir op een kei of voor een ravijn staan tot de vijanden er zijn, met
`--vredig` steekt hij niet terug. Bij elk verloren leven staat erbij welke vijand het dichtst
bij was en wat die deed. Met `--hoe` staat bij elke overtreding waar de vijand de seconde
ervoor liep en wat hij deed.

Zo zijn twee gaten in regel 7 gevonden, allebei op telefoonformaat (852 bij 393), waar het spel
trager loopt en vijanden verder achter Amir raken:

- de keien telden voor de vijanden alleen binnen 2600 px van Amir (`platsNear`). Een vijand die
  verder achter hem zat, liep er dwars doorheen. De vijanden krijgen nu alle keien van het level;
- een hyena die buiten beeld op zijn beurt wacht, schoof mee met Amir en kon zo aan de overkant
  van een ravijn opduiken. Hij schuift nu niet meer over een ravijn of kei (`panBaan`).

Daarna: in tien levels op telefoonformaat geen enkele overtreding meer, en in proefstukken met
een kei en een ravijn kwam geen slang, zwarte slang, fosforslang, schorpioen, zwaardvechter,
hyena of panter erover.

Staat de laadpoort dicht (een winterlevel haalt zijn plaatjes op), dan telt hij dat niet als
vastlopen. Deed hij dat wel, dan sprong hij zodra hij weer mocht, en vloog hij in elk winterlevel
over zijn eigen speer heen; zonder speer kapt hij geen doornbos en staat hij bij het eerste vast.

Hij heeft Node en Playwright nodig (`npm i -g playwright`), en start zelf een webserver. Hij is
geen speler: een eindbaas verslaat hij niet, en een sprong die precies getimed moet worden mist
hij. Loopt hij vast waar `levelcheck.py` niets meldt, kijk dan wat daar staat. Is het de robot,
laat het dan; is het het level, dan hoort er een regel bij. Zo zijn de regels onder de grond
ontstaan.

## Schijven nameten: tools/runecheck.js

`levelcheck.py` rekent met getallen uit de code, maar waar de schijf op een rots zit hangt aan de
alfa van een plaat, en die moet geladen zijn. Daarom doet dit script het in het echte spel: het laadt
de HTML in Chromium, zet elk level met een `runes`-schijf of een `muur` klaar op vier schermformaten
en vraagt het spel zelf van welke afstanden de speer de schijf raakt (`runeStroken`, en voor de
rotswand dezelfde boog tegen `muurSymRaak`). Daarna kijkt het of die strook ook in beeld ligt: de
camera staat op Amir, dus verder dan een half scherm voor hem uit ziet hij de schijf niet.

```
node tools/runecheck.js                 alle levels, op 1280x720, 852x393, 1440x620 en 1920x1080
node tools/runecheck.js "Poort"         alleen de levels waarvan de naam dit bevat
node tools/runecheck.js --formaat 25    het schuifje Formaat
node tools/runecheck.js --schermen 1280x720,852x393
```

FOUT betekent: nergens te raken, of nergens te raken met de schijf in beeld. LET OP: er blijft minder
dan 60 px over. Het meldt per schijf ook waar de rots staat en waar de schijf uitkomt, en dat is niet
overbodig: de rots hangt aan Amirs maat, dus op 1920 bij 1080 staat hij ruim 500 px verder naar
rechts dan op een telefoon. Zet dus niets in de strook waarvan je niet wil dat Amir er staat (een
ravijn, een terras: vanaf een terras gooit hij van een andere hoogte en dan klopt de strook niet).

Nu meldt hij een FOUT in **Test 3**, en dat is er een van voor deze tools: de schijf op de grotboog
is daar alleen van 692 px te raken en dan staat hij op 1280 bij 720 net buiten beeld. Datzelfde geldt
als LET OP voor de rotswand in Test 7. Die twee zijn zo gelaten; De Poorten gebruikt daarom alleen
schijven op een rots.

## Hetzelfde beeld nameten: tools/beeldgelijk.js

Raak je de tekencode aan om hem sneller te maken, dan hoort het beeld niet te veranderen. Dat is
niet met het oog na te kijken: twee potjes lopen nooit gelijk, want het spel ademt op de echte klok
en trekt toeval. Daarom zet je de oude en de nieuwe weg samen in de code achter een vlag, en tekent
dit script hetzelfde bevroren beeld twee keer in hetzelfde potje: een keer met de vlag uit, een keer
met de vlag aan. Daartussen verandert niets (de beeldlus is overgenomen, de klok staat stil, het spel
staat op pauze en de toevalsreeks begint weer vooraan), dus elk pixelverschil komt van de wijziging.

```
node tools/beeldgelijk.js --vlag LAGFIX                een vaste reeks van twaalf levels
node tools/beeldgelijk.js --vlag LAGFIX "Klim 9"       alleen dit level
node tools/beeldgelijk.js --vlag LAGFIX --plekken -300,-2000
node tools/beeldgelijk.js --vlag LAGFIX --breed 852 --hoog 393
```

`gelijk` op elke plek betekent: geen enkele pixel anders. Staat er `max 12 op 1723 bytes`, dan weet je
ook meteen hoeveel het scheelt en waar. Zet de vlag na het nameten weer uit de code; hij is er om een
wijziging te verantwoorden, niet om te blijven staan.

Reken niet met het aantal pixels dat een vulling vraagt: een `fillRect` die buiten het canvas valt
kost bijna niets, want het canvas knipt dat zelf weg. Wat wel kost is een lus die honderden keren
tekent en een doek dat elk beeld opnieuw wordt klaargezet. Meet dus beeldtijden, niet oppervlakte, en
meet de versies om en om, want een enkele ronde is vooral ruis.

## Het schildduel: tools/schildduel.js

Speelt het gevecht tegen de schildbandiet in het echte spel met een paar speelstijlen (stilstaan, blind
steken, geduldig ontwijken en straffen, onder de sprong door, en een "mens" met reactietijd), en meldt per
potje hoe lang het duurde, hoe vaak Amir geraakt werd en in welk stuk van zijn aanval Amir hem raakte. Draai
het na een wijziging aan de getallen in `SCHB`. `--reactie 0.3` zet de reactietijd van de mens, `--breed 1280
--hoog 720` het scherm (standaard kleiner, en daar is ontwijken makkelijker), `--fotos map` maakt
schermafdrukken op vaste frames van de sprong.

## De bouwertest: tools/bouwertest.js

Opent elk level uit de HTML in de bouwer, slaat het op en leest het weer in, en meldt per level de
velden die daarbij veranderd of kwijtgeraakt zijn. Draai hem na elke wijziging aan de bouwer, aan
`readLevel` of aan `syncLevel`; hij verandert niets aan de levels.

```
node tools/bouwertest.js              alle levels
node tools/bouwertest.js "Test 4"     alleen de levels waarvan de naam dit bevat
node tools/bouwertest.js --shots map  daarna een schermafdruk van de bouwer
```
