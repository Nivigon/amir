# Savannelagen (hoger en zwevend)

### Een hogere savannelaag

Een terras is grijze rots, en dat is goed voor een klif of een mesa. Wil je dat een level niet één
savanne heeft maar twee of drie boven elkaar, dan is rots het verkeerde materiaal: je rijdt met een
blok savanne omhoog en stapt boven op steen. Daarom heeft een terras het veld `grond`:

```
terraces: [ {r: -2020, l: -3800, h: 300, grond: true} ]
```

Dat verandert alleen het tekenen. De looplijn, de wand, `terrainH`, `terracePlats`, de sprong erop en
de rand waar vijanden stoppen (regel 7) zijn precies wat ze bij een terras waren, en `levelcheck.py`
rekent hem na met dezelfde regel `terrassen`. Wat je ziet is de grondtegel van het level (`bodemPic`)
op die hoogte, met daaronder de aarde die wegzakt in het donker, en het silhouet van een terras
(`terClipPath`): de zijkanten breken net zo open, en sluit er een hoger terras op aan, dan heeft deze
laag aan die kant geen rand.

Drie dingen die ertoe doen:

- **De tegel hangt aan de wereld, niet aan het scherm.** `savanneLaag` legt hem neer met dezelfde
  ankerberekening als de grond zelf, als `zuilTeken` en als `rijsTeken`. Daardoor loopt een blok
  rijzende grond dat tot de hoogte van de laag komt er naadloos in over: dezelfde tegel, dezelfde
  looplijn. Reken je vanaf de rand van de laag, dan verspringt het patroon zodra de camera beweegt.
- **Het donker hangt aan de tegel, niet aan Amir.** `SAV_LAAG.donker` telt in tegelhoogtes, zodat het
  donker precies vol is waar `grondrand.png` ophoudt. In Amir gerekend viel dat bij een laag van 600
  net naast de onderrand van het plaatje, en dan ligt er een streep in de wand.
- **De weg omhoog is de rijzende grond.** Amir springt 200, dus een laag van 300 haal je niet zelf.
  Zet er een ravijn tegen de rand van de laag met een rijzer die tot die hoogte komt en een zegel
  ervoor (zie "rijzende grond"), precies zoals Test 21 dat met rotsterrassen doet.

Test 22 is het proefstuk: de lage savanne, een laag op 300 en een op 600, met op elke laag gras, een
struik en een vijand, zodat je ziet dat decor en dieren daar gewoon op de grond staan. In de sandbox
staat het onder Terrein, **Savannelaag**: Op 300, Op 600, en Met een lift erheen, die er het ravijn,
het blok en het zegel bij zet.

## hogere savannelaag: een terras van grond

`SAV_LAAG`, `savanneLaag` (in `drawClimb`, voor de rotslus): een terras met `grond: true` is geen rotsplateau maar savanne die hoger ligt. Botsen, dragen en `terrainH` blijven wat ze bij een terras waren; alleen het tekenen is anders: de grondtegel van het level (`bodemPic`, vast aan de wereld, net als `zuilTeken` en `rijsTeken`, zodat een blok rijzende grond er naadloos in overloopt) met daaronder de aarde die wegzakt in het donker, en het silhouet van een terras (`terClipPath`), zodat de zijkanten net zo openbreken en een hoger terras dat ertegenaan staat de rand afdekt. De winter en een rotsbodem (`sneeuw`) lopen vanzelf mee, want die zitten al in `bodemPic` en `bodemDonker`. Ligt er onder de laag een gang (een `holte`) en zit de laag op of boven het dak van die gang (`top < dakY`, dus geen vloer-trede diep in de gang, die heeft wel aarde onder zich), dan is daaronder geen aarde maar de holte zelf: de donkere onderkant (`bodemDonker` en het donkerverloop) stopt bij het dak van de gang (`groundY + HOLTE_DAK * scale`, met een evenodd-clip op de kolommen uit `holteLijst` die onder de laag vallen), zodat het steen van de gang dat `drawHolte` er vlak ervoor al tekende zichtbaar blijft in plaats van zwart overschilderd te worden. De onderrand krijgt daarbij dezelfde afsluiting als het gangplafond naast een gat: de aarde loopt over in het steen (`holteOvergang`) en daaronder hangt de tandenband (`plafondBand` op `-HOLTE_DAK`, dezelfde helderheid als het dak in `drawHolte`), allebei vast aan de wereld zodat ze naadloos aansluiten op het gangplafond ernaast in plaats van een rechte snede te geven. Zonder gang eronder verandert er niets. Zo blijft een gang onder een hoger of lager gezette savannelaag leesbaar (de Maker zet die combinatie zo neer). Test 22 is het proefstuk; in de sandbox onder Terrein, Savannelaag (`SB_SAV`, `sbSavLaag`)

## zwevende savannelaag: een dik savanneblok in de lucht

`ZWEEF`, `zweefList`, `savanneLaag` (met `floating`), `zweefKop`: het veld `zwevers: [{r, l, h, onder, look}]`, los van `terraces` want `terrainH` is enkelvoudig. Een dik stuk savanne dat zweeft met lucht eronder: je loopt eronderdoor als er genoeg ruimte onder zit, je landt bovenop via de rand of een lift (`terracePlats`, `supportHeight`), en van onderaf stoot je je hoofd (`zweefKop` in `updateJump`). Hoeveel ruimte nodig is rekent `amirOnderRuimte()`: staand `CHAR_H`, en helemaal gebukt net binnen een celhoogte (`KRUIP_RUIMTE` 0,56, zo'n 140, onder een cel van 150), zodat je onder een laag met een cel lucht (`onder` ~150, onder `CHAR_H` maar boven `KRUIP_RUIMTE`) **gebukt doorkruipt**, en onder twee cellen gewoon loopt; past hij er niet onder, dan is de zijkant een wand (`blockByPlatforms`). **Dichttimmeren**: hangt er een lage laag boven hem (`zweefDakBoven`), dan houdt de lus hem zo ver gebukt dat zijn kop er net onder blijft, zodat hij niet rechtop door de rots steekt; hij komt vanzelf overeind als er weer ruimte is. Zit hij daar en druk je links of rechts, dan kruipt hij ook zonder pijl omlaag (`laagDak` in de buk-code); vroeger stond hij dan gebukt stil tot je pijl omlaag erbij drukte. `onder` dicht bij `h` geeft een dunne plateau, laag geeft een dik blok met een diepe aardrand. Met `look: 'rots'` tekent de laag als steen (`rotsLaag`: het terrasgesteente met de plafond-tandenband eronder) in plaats van savanne, voor een rotsoverhang om onder te kruipen; de botsing blijft gelijk. Getekend als savanne met de aardrand doorgetegeld en een schaduw-onderkant, of als rots. Test 24 is het proefstuk; in de sandbox onder Terrein, Zwevende laag (`SB_ZWEEF`, `sbZweef`): **Kruipen (cel lucht)** en **Rotsoverhang (kruipen)**. In de Maker zet je er een met het **Overhang**-voorwerp (Objecten), met schuifjes voor breedte, dikte en de onderkant-hoogte (vrij van het grid) en een knop voor de look; `mkNaarLevel` vertaalt het naar een zwever
