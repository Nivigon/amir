# Highscores per team in Co-op Survival (`HS`)

Een team is een combinatie van spelers: de namen uit de lobby (`mpSpelerNoem`), op het alfabet, met ` + ` ertussen
(`hsTeam`). Alleen spelen (Co-op solo) is een team van een. Hoofdletters tellen niet (`hsSleutel`), dus "Gissa + Tom" en
"gissa + tom" zijn hetzelfde team. Typ in de lobby dus altijd dezelfde naam, anders word je een nieuw team.

- De regel `eind` van de tester-log krijgt `team` en `map` mee (in `tlogCoop`). De designer logt nu ook, met als naam
  `designer` (`tlogAan`, `tlogWie`); de vraag na het potje (sterren) krijgt alleen een tester.
- De Apps Script houdt op het tabblad **Highscores** per team de beste score bij (de Co-op episode niet).
- Op het eindscherm van Co-op Survival: de beste van dit team en het record van iedereen (`hsEindToon`). Het potje dat net
  klaar is telt meteen mee, ook als de regel nog in de wachtrij staat (`hsMetEigen`).
- Onder Multiplayer de knop **High scores** (`hsOverzicht`): elk team met zijn score, ronde en map, teams waar jouw
  lobbynaam in zit licht op, en onderaan het beste team per aantal spelers.
- Logt niemand in het team (geen tester en geen designer), dan komt het potje er niet in. Speel je met elkaar, dan sturen
  allebei de apparaten de uitslag; dat geeft niets, er blijft per team alleen de hoogste staan.

Namen om op te grepen: `HS`, `hsTeam`, `hsVraag`, `hsEindToon`, `hsOverzicht`, `mphs`.

## Het stuk Apps Script

Het script hangt aan de Sheet "Amir testers log" (Extensies, Apps Script). Erbij nodig:

1. Bovenaan in de bestaande `doPost(e)`, naast de regel van de notities (deze regel gaat daarna gewoon door, de regel komt
   dus ook nog in de log):

```js
  try { const h = JSON.parse(e.postData.contents); if (h && h.soort === 'eind' && h.team && !h.epLevel && h.sleutel === 'amir-tester-2026') hsRegel(h); } catch (x) {}
```

2. In de bestaande `doGet`, naast de regel `if (p.actie === 'open') ...`:

```js
  if (p.actie === 'scores') return notitieAntwoord({ ok: true, scores: hsLijst() });
```

3. Onderaan het script:

```js
// ---- highscores per team in Co-op Survival (HS in het spel) ----
const HS_TAB = 'Highscores';
function hsTab(){
  const ss = SpreadsheetApp.openById(NOTITIE_SHEET);
  let sh = ss.getSheetByName(HS_TAB);
  if (!sh){
    sh = ss.insertSheet(HS_TAB);
    sh.appendRow(['sleutel', 'team', 'spelers', 'score', 'ronde', 'kills', 'tijd_s', 'map', 'wanneer', 'logger']);
    sh.setFrozenRows(1);
  }
  return sh;
}
function hsRegel(d){
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try {
    const sh = hsTab(), team = String(d.team).slice(0, 120), k = team.toLowerCase().replace(/\s+/g, ' ').trim();
    const score = Number(d.score) || 0, n = sh.getLastRow() - 1;
    const rij = [k, notitieVeilig(team), team.split(' + ').length, score, Number(d.ronde) || 0, Number(d.kills) || 0,
      Number(d.duur_s) || 0, notitieVeilig(d.map), notitieVeilig(d.gespeeld), notitieVeilig(d.tester)];
    const keys = n > 0 ? sh.getRange(2, 1, n, 1).getValues().map(r => String(r[0])) : [];
    const i = keys.indexOf(k);
    if (i < 0) sh.appendRow(rij);
    else if (score > Number(sh.getRange(i + 2, 4).getValue())) sh.getRange(i + 2, 1, 1, rij.length).setValues([rij]);
  } finally { lock.releaseLock(); }
}
function hsLijst(){
  const sh = hsTab(), n = sh.getLastRow() - 1;
  if (n < 1) return [];
  return sh.getRange(2, 1, n, 10).getValues()
    .map(r => ({ team: String(r[1]).replace(/^'/, ''), score: Number(r[3]) || 0, ronde: r[4], kills: r[5], tijd: r[6], map: String(r[7]), wanneer: String(r[8]) }))
    .sort((a, b) => b.score - a.score);
}
```

4. Opslaan, en dan **Implementeren, Implementaties beheren**, potloodje bij de bestaande implementatie, **Versie: Nieuwe
   versie**, Implementeren (zo blijft de URL in `TLOG.url` hetzelfde, zie `notities/designer-notities.md`).

Zolang het script dit nog niet kent, zegt het eindscherm alleen de score van dit potje en het overzicht "No connection".
Potjes van voor deze stap staan niet in de lijst: het tabblad begint leeg.

## Het eindscherm (een regel, niet twee)

Het eindscherm van Co-op Survival heeft een regel high score en een regel record (`hsEindToon`). De high score is die van
dit team uit de Sheet, solo op je naam: de naam uit de lobby, en zonder lobbynaam die van de tester-log (`hsTeam`), niet de
naam van de outfit. Of het een nieuwe is, vergelijkt hij met de lijst van voor het potje (`HS.voor`, gevraagd in
`mpCoopStart`): bij het einde vragen is te laat, want de regel van dit potje kan er dan al in staan. Logt er niemand of is
er geen verbinding, dan de lokale high score van dit apparaat (`mpcEindSleutel`), met "(this device)" erbij.
