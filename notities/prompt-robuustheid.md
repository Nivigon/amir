# Prompt: drie verborgen storingen zichtbaar en hersteld

Kopieer alles onder de streep in een verse chat.

---

Herstel drie bevestigde storingen in `amir-king-of-africa.html` en `sw.js`. Ze staan hieronder op volgorde van belang; doe ze in die volgorde, elk in een eigen commit op één `claude/`-branch, zodat de eerste af is als de tijd op is. Lees eerst `CLAUDE.md` (regel 1: geen level van een echte episode aanraken; regel 10: breed leeswerk naar een Sonnet-subagent; regel 11: eerst de notitie van het onderwerp). Hier zijn dat `notities/speer.md`, `notities/laadpoort.md`, `notities/assets.md` en `notities/geluid.md`. Geen nieuwe features, geen refactor buiten wat de fix nodig heeft. Nederlands, geen em-dashes. Maak aan het eind een pull request met als titel "Offline-download, tekenfout en worp in de pauze hersteld".

## 1. `sw.js`: een mislukte offline-download telt als geslaagd

**Wat er misgaat.** In de precache-lus van `sw.js` telt een mislukte `fetch` of `cache.put` alleen op in `failed`, maar na `Promise.all(... worker)` wordt `VERSION_KEY` altijd weggeschreven. Daarna ziet `syncAssetVersion` de cache als actueel terwijl er bestanden ontbreken, en een nieuwe poging start niet vanzelf. Op een telefoon met weinig opslag (de kleine set is 431 MB) is dat precies wat gebeurt. Daarnaast worden runtime-cachefouten stil weggegeten (`cache.put(...).catch(() => {})`).

**Wat je doet.**
- Schrijf `VERSION_KEY` alleen als `failed === 0`. Is `failed > 0`, meld dat in het `precache-done`-bericht zo dat het spel het aan de speler laat zien (hoeveel bestanden ontbreken, en dat opnieuw proberen kan), en laat de versie zo staan dat een volgende poging weer begint en alleen het ontbrekende ophaalt (de `cache.match`-check doet dat al).
- Zoek in de HTML waar `precache-done` en `precache-progress` ontvangen worden en zorg dat de melding er ook echt komt te staan, in de bestaande downloadknop of zijn balk, niet in een nieuw venster.
- Onderscheid een quota-fout (`QuotaExceededError`) van een netwerkfout in de tekst, als dat met weinig code kan.

**Nameten.** Simuleer in Chromium (Playwright, zoals `tools/speelrobot.js` het spel laadt) een download waarbij een paar verzoeken falen (bijvoorbeeld een route die 404 geeft op twee bestanden) en laat zien: de versie wordt niet gezet, de melding verschijnt, en een tweede poging haalt alleen die twee op. Doe daarna een schone run zonder fouten en laat zien dat de versie wel gezet wordt.

## 2. `safeLoop`: een fout in de tekenlus lekt canvas-staat en zegt niets

**Wat er misgaat.** `safeLoop` vangt een exception uit `loop`, roept alleen `ctx.setTransform` aan en plant de volgende frame. De `save`-stapel, een lopende `clip`, `globalAlpha`, `filter` en `globalCompositeOperation` blijven staan. Gooit een tekenfunctie elk beeld dezelfde fout (bijvoorbeeld een `drawImage` op een plaatje dat niet laadde: 65 `new Image()` tegen 49 `onerror`, en die handlers doen alleen `console.warn`), dan lekt de stapel 60 keer per seconde, vult de console zich en ziet de speler een half beeld zonder melding. Er is geen `window.onerror` en geen `unhandledrejection`-handler.

**Wat je doet.**
- Laat `safeLoop` de canvas-staat volledig herstellen: `ctx.reset()` waar dat bestaat, anders de transform, `globalAlpha`, `filter`, `globalCompositeOperation` en de `save`-stapel. De stapeldiepte is niet uit te lezen; houd hem bij met een kleine wikkel om `ctx.save` en `ctx.restore`, of kies een andere manier die aantoonbaar werkt. Kijk eerst of er al iets bestaat dat dit deels doet (`werkDoek`, `zichtVak`, de laadpoort) en sluit daarop aan.
- Dezelfde fout op dezelfde plek niet elk beeld opnieuw loggen: één keer in de console, en één keer een korte melding in beeld voor de speler ("Er ging iets mis bij het tekenen: ..."), in de stijl van de bestaande tips of het laadscherm. De lus blijft draaien.
- Een `window.onerror` en een `unhandledrejection`-handler die hetzelfde doen: één melding, geen spam.
- Een plaatje dat niet laadt: laat de laadpoort of de melding de bestandsnaam noemen, zodat een 404 niet langer stil is. Verander niet dat een ontbrekend plaatje het spel niet blokkeert; dat is bewust (zie `notities/laadpoort.md`).

**Nameten.** Zet tijdelijk achter een vlag een `throw` in een tekenfunctie die elk beeld loopt, draai het spel in Chromium en laat zien: één console-regel, één melding in beeld, de `save`-diepte blijft nul, het beeld blijft bewegen. Haal de vlag daarna weg. Draai `node tools/beeldgelijk.js` op een paar levels om te laten zien dat een foutloos beeld pixelgelijk blijft.

## 3. De speerworp loopt op de wandklok

**Wat er misgaat.** `thrPressT` en `thr.t0` (in `thrStop`, `thrHoek` en de oplaaddrempel bij `THR_CHARGE`) rekenen met `performance.now()`. Ze negeren `dt`, het lagere tempo op een telefoon (`gameTempo`, zo'n 0,75) en de pauze: wie de worp vasthoudt, pauzeert en hervat, gooit met maximale hoek of volle lading. De baviaan doet dit al goed met `bavKlok`, en `mesAfweer` gebruikt `mesKlok`.

**Wat je doet.**
- Zet de worptijden op speltijd. Kijk eerst welke spelklokken er al zijn (`bavKlok`, `mesKlok`, `weerKlok`, misschien meer) en gebruik er een, of maak één gedeelde `spelKlok` die in de lus met `dt` wordt opgeteld en laat de andere daar later naartoe. Geen vierde losse klok erbij.
- `panTipT` en de hyena-lach (`s.enc.lachT`) lopen ook op de wandklok, maar dat is alleen een tip en geluid: laat die staan en noem ze in de PR-tekst als bekend en bewust.

**Nameten.** In de sandbox onder Speerworp: vasthouden, pauzeren, een paar seconden wachten, hervatten, en laten zien dat de hoek en de lading niet verder zijn opgelopen dan voor de pauze. Doe hetzelfde met `gameTempo` op 0,75 (zoals de telefoon) en laat zien dat de oplaadtijd in speelseconden gelijk blijft.

## Afronden

- `python3 tools/levelcheck.py` moet nog 0 FOUT geven.
- `README.md` bijwerken alleen voor wat de speler merkt: de melding bij de offline-download.
- In de PR-tekst per fix: wat er misging, wat er nu anders is, en hoe het is nagemeten.
- Niet in deze PR, wel de volgende: `mesAfweer` zet voor de kooiman en de meelman een terugstoot klaar (`afweerT`, `afweerV`) maar alleen de slang, hyena en schorpioen roepen `afweerStap` aan, en de schildman omzeilt `mesAfweer` helemaal met een losse flits in de hoofdlus. Noem dat als bekend, bouw het hier niet.
