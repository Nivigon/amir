# Notities van de designer (`NOTE`)

Alleen voor de designer (rol Designer, `body.designer`). Rechtsboven in beeld staat een klein potloodknopje (`#notknop`),
in het menu en midden in een level. Het opent een vak: kies **Bug** of **Improvement**, typ wat je zag, **Send**
(of Ctrl+Enter; Esc sluit). Het level, de modus, de plek (`world`) en de schermmaat gaan vanzelf mee. Typen gaat niet
naar het spel, en het spel loopt gewoon door.

De notitie gaat als regel `{soort: 'notitie'}` naar dezelfde Apps Script als de tester-log (`TLOG.url`), die hem op het
tabblad **Notities** van de Sheet "Amir testers log" zet met status `open`. Zonder verbinding wacht hij in localStorage
(`NOTE.rijKey`) en gaat hij mee bij de volgende keer.

In het hoofdmenu staat onder Updates en Settings **Open notes: N** (`#btnnotopen`): wat de Sheet open heeft plus wat hier
nog niet verstuurd is. Klik erop en de Sheet opent. Een notitie is dicht zodra je in de kolom `status` een van deze woorden
zet: `done`, `klaar`, `fixed`, `opgelost`, `af`, `x`, `wontfix`. Al het andere (ook `bezig`) telt als open.

Namen om op te grepen: `NOTE`, `noteOpen`, `noteZend`, `noteLeeg`, `noteTelVraag`, `noteTelToon`.

## Het stuk Apps Script

Het script hangt aan de Sheet (Extensies, Apps Script) en staat niet in deze repo. Erbij nodig:

1. Bovenaan in de bestaande `doPost(e)`, als eerste regel binnen de functie:

```js
  try { const n = JSON.parse(e.postData.contents); if (n && n.soort === 'notitie' && n.sleutel === 'amir-tester-2026') return notitieRegel(n); } catch (x) {}
```

2. Onderaan het script dit hele stuk (staat er al een `doGet`, voeg dan de twee `if`-regels daarin toe in plaats van een tweede `doGet`):

```js
// ---- notities van de designer (NOTE in het spel) ----
const NOTITIE_SHEET = '1wruH7GhJrK4Z_Bt88h-S9lwOwes0GjlsdAzN-JTgVMI';
const NOTITIE_TAB = 'Notities';
const NOTITIE_DICHT = ['done', 'klaar', 'fixed', 'opgelost', 'af', 'x', 'wontfix'];
function notitieTab(){
  const ss = SpreadsheetApp.openById(NOTITIE_SHEET);
  let sh = ss.getSheetByName(NOTITIE_TAB);
  if (!sh){
    sh = ss.insertSheet(NOTITIE_TAB);
    sh.appendRow(['aangekomen', 'gemaakt', 'soort', 'tekst', 'level', 'modus', 'plek_x', 'scherm', 'status']);
    sh.setFrozenRows(1);
  }
  return sh;
}
function notitieVeilig(v){ v = String(v == null ? '' : v); return /^[=+\-@]/.test(v) ? "'" + v : v; }
function notitieRegel(d){
  const sh = notitieTab();
  sh.appendRow([new Date(), notitieVeilig(d.gespeeld), notitieVeilig(d.type), notitieVeilig(String(d.tekst || '').slice(0, 1000)),
    notitieVeilig(d.level), notitieVeilig(d.modus), d.plek_x === '' || d.plek_x == null ? '' : Number(d.plek_x), notitieVeilig(d.scherm), 'open']);
  return notitieAntwoord({ ok: true, open: notitieOpen() });
}
function notitieOpen(){
  const sh = notitieTab(), n = sh.getLastRow() - 1;
  if (n < 1) return 0;
  return sh.getRange(2, 9, n, 1).getValues().filter(r => NOTITIE_DICHT.indexOf(String(r[0]).trim().toLowerCase()) < 0).length;
}
function notitieAntwoord(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function doGet(e){
  const p = (e && e.parameter) || {};
  if (p.sleutel !== 'amir-tester-2026') return notitieAntwoord({ ok: false });
  if (p.actie === 'open') return notitieAntwoord({ ok: true, open: notitieOpen() });
  return notitieAntwoord({ ok: false });
}
```

3. Opslaan, en dan **Implementeren, Implementaties beheren**, potloodje bij de bestaande implementatie, **Versie: Nieuwe
   versie**, Implementeren. Zo blijft de URL in `TLOG.url` hetzelfde. Een nieuwe implementatie maken geeft een nieuwe URL,
   en die werkt dan niet in het spel.

Werkt het script nog niet bij, dan blijven de notities in de wachtrij van de browser staan (de teller zegt "unsent")
en gaan ze vanzelf weg zodra het script ze aanneemt.
