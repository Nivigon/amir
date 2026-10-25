/* Service worker voor Amir: King of Africa.
 *
 * Twee caches, met opzet gescheiden:
 *
 *   SHELL   het spel zelf (HTML, manifest, iconen). Klein, en mag bij elke
 *           update vervangen worden. Network-first, zodat je online altijd de
 *           nieuwste versie speelt en offline de laatst bekende.
 *
 *   ASSETS  de sprites, achtergronden en geluiden. Honderd megabyte, dus die
 *           willen we juist nooit opnieuw ophalen. Cache-first: staat een
 *           bestand er eenmaal in, dan gaat er geen enkel verzoek meer het
 *           netwerk op.
 *
 * De assets komen er op twee manieren in. Tijdens het spelen wordt alles wat
 * het spel opvraagt onderweg bewaard, dus na een keer doorspelen staat het
 * grootste deel er al. En in het startmenu zit een knop die de hele lijst uit
 * offline-assets.json in een keer binnenhaalt, zodat het spel daarna ook
 * zonder verbinding compleet is.
 */

const SHELL_CACHE = 'amir-shell-v1';
// v2: de assetcache is cache-first en revalideert nooit, dus een vervangen sprite (zelfde
// bestandsnaam) bleef als oude versie in de cache hangen tot je hard herlaadde. Het ophogen van
// deze naam gooit de oude cache (v1) in een keer weg bij activate, zodat iedereen schoon opnieuw
// begint. Voor latere wijzigingen doet syncAssetVersion de rest (zie hieronder), zonder dat deze
// naam elke keer mee hoeft.
// v3: de schildbandiet tekent alleen nog uit lagen (lagen.json en executie.json); de oude complete
// sets zijn uit de repo, en zo gaat ook de oude set uit de cache op de telefoon.
// v4: de baviaan en het goudaapje hebben een halve set in klein/; een schone cache, zodat de telefoon
// die meteen binnenhaalt in plaats van de grote frames uit de oude cache te blijven gebruiken.
// v5: het goudaapje staat in klein/ op een kwart in plaats van de helft, onder dezelfde bestandsnamen;
// een schone cache, zodat de telefoon de halve frames niet uit de oude cache blijft gebruiken: het spel
// rekent nu met een kwart (KLEIN_BRON), dus een oud half frame zou twee keer te groot getekend worden.
// v6: de meelman heeft een halve set in klein/; een schone cache, zodat de telefoon die meteen
// binnenhaalt in plaats van de grote frames uit de oude cache te blijven gebruiken.
const ASSET_CACHE = 'amir-assets-v6';

// Sleutel waaronder we in de assetcache bijhouden welke assetversie erin zit.
// Geen echt bestand, alleen een plek om een string te bewaren.
const VERSION_KEY = new URL('./__offline-version__', self.location).href;

const SHELL = [
  './',
  './index.html',
  './amir-king-of-africa.html',
  './manifest.webmanifest',
  './offline-assets.json',
  './ravijn/ravijn-effect.js',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
];

// Hoeveel bestanden we tegelijk ophalen bij het downloaden. Hoog genoeg om de
// lijn te vullen, laag genoeg om Safari niet te laten stikken in verzoeken.
const PARALLEL = 6;

// Is dit de fout van een volle opslag? Dan zegt het spel dat in plaats van "geen verbinding".
const isVol = (err) => !!err && (err.name === 'QuotaExceededError' || err.code === 22);

// Een runtime-cachefout (tijdens het spelen een bestand bewaren dat niet past) houdt het spel niet
// tegen: het bestand komt gewoon van het net. Maar stil wegeten maakte een volle opslag onzichtbaar.
// We onthouden het daarom, melden het een keer in de console en geven het mee met de status.
let runtimeVol = false;
let runtimeGemeld = false;
function runtimeFout(err) {
  if (isVol(err)) runtimeVol = true;
  if (!runtimeGemeld) {
    runtimeGemeld = true;
    console.warn('[sw] een bestand kon niet in de cache:', err && (err.name || err.message || err));
  }
}

// De json hoort erbij: de schildbandiet tekent uit lagen.json en executie.json, de hyena, de kooiman
// en de vogel lezen hun metadata.json. Die gingen eerst als "het spel zelf" network-first naar de
// shellcache, terwijl de downloadknop ze in de assetcache zette: offline vond de fetch-handler ze
// dan niet, en de schildbandiet (de enige die zijn json pas bij het eerste gebruik ophaalt) kwam
// niet binnen. De bestandslijst zelf blijft network-first, die moet juist vers zijn.
const isAsset = (url) =>
  /\.(png|jpe?g|mp3|json)$/i.test(url.pathname) && !/\/offline-assets\.json$/.test(url.pathname);
const isFontHost = (url) =>
  url.host === 'fonts.googleapis.com' || url.host === 'fonts.gstatic.com';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(SHELL_CACHE)
      // addAll faalt in zijn geheel als er een bestand ontbreekt, en dan zou
      // de service worker niet installeren. Per bestand dus, en missers negeren.
      .then((cache) => Promise.all(SHELL.map((p) => cache.add(p).catch(() => {}))))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((names) =>
        Promise.all(
          names
            .filter((n) => n !== SHELL_CACHE && n !== ASSET_CACHE)
            .map((n) => caches.delete(n)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // Lettertypen van Google: cache-first, en desnoods opaak. Lukt het niet, dan
  // valt de CSS terug op Helvetica en Arial, die al in de font-stack staan.
  if (isFontHost(url)) {
    event.respondWith(cacheFirst(req, SHELL_CACHE, { crossOrigin: true }));
    return;
  }

  if (url.origin !== self.location.origin) return;

  // Sprites en geluiden: nooit opnieuw van het net als ze er al staan.
  if (isAsset(url)) {
    // Safari vraagt audio in stukken op. Een heel bestand terugsturen op zo'n
    // deelvraag laat het afspelen stukgaan, dus dan snijden we zelf een 206.
    event.respondWith(
      req.headers.has('range') ? rangeFromCache(req) : cacheFirst(req, ASSET_CACHE),
    );
    return;
  }

  // Het spel zelf en de lijst: online de nieuwste, offline de bewaarde.
  event.respondWith(networkFirst(req, SHELL_CACHE));
});

async function cacheFirst(req, cacheName, opts = {}) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req, { ignoreVary: true });
  if (hit) return hit;

  try {
    const res = await fetch(opts.crossOrigin ? new Request(req.url, { mode: 'no-cors' }) : req);
    // Een opaak antwoord (status 0) bewaren we ook; de browser kan het
    // uitserveren, alleen wij kunnen er niet in kijken.
    if (res && (res.ok || res.type === 'opaque')) {
      cache.put(req, res.clone()).catch(runtimeFout);
    }
    return res;
  } catch (err) {
    // Offline en niet in deze cache. Misschien wel in een andere: de json van een vijand stond tot
    // de vorige versie in de shellcache (zie isAsset), en wie hem daar nog heeft speelt gewoon door.
    const elders = await caches.match(req, { ignoreVary: true });
    if (elders) return elders;
    return new Response('', { status: 504, statusText: 'offline' });
  }
}

// Safari vraagt een geluidsbestand in vele kleine stukken op. Het hele bestand
// telkens opnieuw uit de cache naar een ArrayBuffer kopiëren (5 MB voor de
// muziek) is zonde van de CPU op een telefoon, dus de laatste paar bestanden
// houden we uitgepakt bij de hand.
const RANGE_KEEP = 4;
const rangeBufs = new Map();   // url -> { buf, headers }
async function rangeBuffer(req) {
  const had = rangeBufs.get(req.url);
  if (had) {
    // opnieuw achteraan zetten: de oudste valt er als eerste uit
    rangeBufs.delete(req.url);
    rangeBufs.set(req.url, had);
    return had;
  }
  const cache = await caches.open(ASSET_CACHE);
  // De cache is gevuld met hele bestanden, dus matchen zonder het Range-verzoek.
  const plain = new Request(req.url);
  let hit = await cache.match(plain, { ignoreVary: true });

  if (!hit) {
    // Nog niet in de cache: het hele bestand halen en bewaren, dan snijden.
    const res = await fetch(plain);
    if (!res.ok) return null;
    // past het niet in de cache (opslag vol), dan toch afspelen: alleen niet bewaren
    try { await cache.put(plain, res.clone()); } catch (err) { runtimeFout(err); }
    hit = res;
  }
  const entry = { buf: await hit.arrayBuffer(), headers: hit.headers };
  rangeBufs.set(req.url, entry);
  while (rangeBufs.size > RANGE_KEEP) rangeBufs.delete(rangeBufs.keys().next().value);
  return entry;
}

/** Beantwoordt een Range-verzoek uit de assetcache met een echte 206. */
async function rangeFromCache(req) {
  let hit;
  try {
    hit = await rangeBuffer(req);
  } catch (err) {
    return new Response('', { status: 504, statusText: 'offline' });
  }
  if (!hit) return fetch(req);

  const buf = hit.buf;
  const header = req.headers.get('range') || '';
  const m = /^bytes=(\d*)-(\d*)$/.exec(header.trim());
  if (!m) return new Response(buf, { status: 200, headers: hit.headers });

  const size = buf.byteLength;
  let start;
  let end;
  if (m[1] === '') {
    // "bytes=-500": de laatste 500 bytes.
    const len = parseInt(m[2], 10);
    if (!Number.isFinite(len)) return new Response(buf, { status: 200, headers: hit.headers });
    start = Math.max(0, size - len);
    end = size - 1;
  } else {
    start = parseInt(m[1], 10);
    end = m[2] === '' ? size - 1 : Math.min(parseInt(m[2], 10), size - 1);
  }

  if (!(start >= 0 && start < size && end >= start)) {
    return new Response(null, {
      status: 416,
      headers: { 'Content-Range': `bytes */${size}` },
    });
  }

  return new Response(buf.slice(start, end + 1), {
    status: 206,
    statusText: 'Partial Content',
    headers: {
      'Content-Type': hit.headers.get('Content-Type') || 'application/octet-stream',
      'Content-Length': String(end - start + 1),
      'Content-Range': `bytes ${start}-${end}/${size}`,
      'Accept-Ranges': 'bytes',
    },
  });
}

async function networkFirst(req, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const res = await fetch(req);
    if (res && res.ok) cache.put(req, res.clone()).catch(runtimeFout);
    return res;
  } catch (err) {
    const hit = await cache.match(req, { ignoreVary: true });
    if (hit) return hit;
    // Bij een navigatie liever het spel uit de cache dan een foutpagina.
    if (req.mode === 'navigate') {
      const game = await cache.match('./amir-king-of-africa.html', { ignoreVary: true });
      if (game) return game;
    }
    return new Response('', { status: 504, statusText: 'offline' });
  }
}

/* ---- berichten vanuit het spel ------------------------------------- */

// Naast de set (klein of groot) kan het spel een deel noemen: een naam uit manifest.delen (nu
// alleen 'arena', uit gen-offline-manifest.py), dan tellen en downloaden alleen die bestanden.
// Zonder deel (of een onbekend deel) is het de hele lijst. Elk antwoord noemt het deel terug,
// zodat het spel weet bij welke knop het hoort.
self.addEventListener('message', (event) => {
  const data = event.data || {};
  const set = data.set === 'klein' || data.set === 'groot' ? data.set : null;
  const deel = typeof data.deel === 'string' && data.deel ? data.deel : null;
  if (data.type === 'precache') event.waitUntil(precacheAll(set, deel));
  else if (data.type === 'status') event.waitUntil(reportStatus(set, deel));
  else if (data.type === 'clear') event.waitUntil(clearAssets(set, deel));
});

/* Van sommige sprites staat er een halve versie in klein/ (tools/gen-klein.py).
 * Een toestel speelt er maar één van, dus de andere hoeft het ook niet binnen te
 * halen. Dat scheelt op een telefoon ruim de helft van de download.
 *
 * Welke bestanden een kleine versie hebben leidt de lijst zelf af: alles wat met
 * klein/ begint. Het spel hoeft hier dus niets over door te geven behalve welke
 * set het speelt, en een nieuwe familie in gen-klein.py werkt vanzelf mee.
 */
function voorSet(assets, set) {
  if (!set) return assets;
  const klein = new Set();
  for (const rel of assets) {
    if (rel.indexOf('klein/') === 0) klein.add(rel.slice('klein/'.length));
  }
  return assets.filter((rel) => {
    const isKlein = rel.indexOf('klein/') === 0;
    if (set === 'groot') return !isKlein;
    // de kleine set: de halve versies, en van de rest alles waar er geen van is
    return isKlein || !klein.has(rel);
  });
}

/** De bestanden van een deel uit de lijst, of de hele lijst zonder (of met een onbekend) deel. */
function voorDeel(manifest, deel) {
  const lijst = deel && manifest.delen && Array.isArray(manifest.delen[deel]) ? manifest.delen[deel] : null;
  if (!lijst) return manifest.assets;
  const erin = new Set(lijst);
  return manifest.assets.filter((rel) => erin.has(rel));
}

async function post(msg) {
  const clients = await self.clients.matchAll({ includeUncontrolled: true });
  for (const client of clients) client.postMessage(msg);
}

async function loadManifest() {
  const cache = await caches.open(SHELL_CACHE);
  try {
    // Bewust langs de HTTP-cache heen: we willen weten of de lijst veranderd is.
    const res = await fetch('./offline-assets.json', { cache: 'no-cache' });
    if (res.ok) {
      cache.put('./offline-assets.json', res.clone()).catch(() => {});
      return res.json();
    }
  } catch (err) {
    // Geen verbinding. Hieronder de bewaarde lijst.
  }
  // Verzoeken vanuit de service worker gaan niet door zijn eigen fetch-handler,
  // dus die terugval moeten we hier zelf doen. Zonder dit zou het spel offline
  // melden dat het de lijst niet kan lezen, terwijl alles gewoon opgeslagen staat.
  const hit = await cache.match('./offline-assets.json', { ignoreVary: true });
  if (hit) return hit.json();
  throw new Error('de bestandslijst is niet te bereiken');
}

// De assetcache is cache-first en haalt een bestand nooit opnieuw op zodra het erin staat. Dat is
// goed voor de honderd megabyte sprites en geluiden, maar het betekent ook dat een vervangen sprite
// (zelfde bestandsnaam, andere inhoud) als oude versie blijft hangen. gen-offline-manifest.py geeft
// bij elke assetwijziging een nieuwe versie-hash; zodra die verandert, gooien we de assetcache weg,
// zodat verse sprites binnenkomen in plaats van de oude. De cache vult zich daarna vanzelf weer
// tijdens het spelen (of met de downloadknop). Dit draait op elke start (vanuit reportStatus), niet
// alleen bij het downloaden, want juist de gewone speler liep tegen de oude cache aan. Een eerste
// keer (nog geen stempel) gooit niets weg: dan onthouden we alleen de huidige versie.
async function syncAssetVersion(manifest) {
  let cache = await caches.open(ASSET_CACHE);
  const stamp = await cache.match(VERSION_KEY);
  const seen = stamp ? await stamp.text() : null;
  if (seen !== null && seen !== manifest.version) {
    await caches.delete(ASSET_CACHE);
    cache = await caches.open(ASSET_CACHE);
  }
  if (seen !== manifest.version) {
    await cache.put(VERSION_KEY, new Response(manifest.version));
  }
  return cache;
}

/** Hoeveel bytes de lijst voor deze set telt; zonder opgave het hele totaal. Met een deel de bytes van dat deel. */
function bytesVoor(manifest, set, deel) {
  let per = manifest.bytesSet;
  let alles = manifest.bytes;
  if (deel && manifest.bytesDeel && manifest.bytesDeel[deel]) {
    per = manifest.bytesDeel[deel];
    alles = (typeof per.klein === 'number' && typeof per.groot === 'number') ? Math.max(per.klein, per.groot) : alles;
  }
  if (set && per && typeof per[set] === 'number') return per[set];
  return alles;
}

async function reportStatus(set, deel) {
  try {
    const manifest = await loadManifest();
    const assets = voorSet(voorDeel(manifest, deel), set);
    // zijn de assets sinds de vorige keer vervangen, dan hier de oude cache weggooien, zodat de
    // gewone speler na een update verse sprites krijgt in plaats van de oude uit de cache
    const cache = await syncAssetVersion(manifest);
    const keys = await cache.keys();
    const have = new Set(keys.map((r) => new URL(r.url).pathname));
    // Via de URL-parser vergelijken, niet via plakken: bestandsnamen met een
    // spatie staan in de cache als %20 en zouden anders als missend tellen.
    let done = 0;
    for (const rel of assets) {
      if (have.has(new URL(rel, self.location).pathname)) done++;
    }
    await post({
      type: 'status',
      deel,
      done,
      total: assets.length,
      bytes: bytesVoor(manifest, set, deel),
      version: manifest.version,
      vol: runtimeVol,
    });
  } catch (err) {
    await post({ type: 'status', deel, error: String(err.message || err) });
  }
}

// Wissen is altijd alles: de delen overlappen (de arena zit in het hele spel), dus een deel apart
// weghalen zou ook bestanden van een ander deel raken. Het spel zet de knop ook zo neer.
async function clearAssets(set, deel) {
  await caches.delete(ASSET_CACHE);
  await post({ type: 'cleared' });
  await reportStatus(set, deel);
}

async function precacheAll(set, deel) {
  let manifest;
  try {
    manifest = await loadManifest();
  } catch (err) {
    await post({ type: 'precache-error', deel, message: String(err.message || err) });
    return;
  }
  const assets = voorSet(voorDeel(manifest, deel), set);

  // Zijn de assets sinds de vorige keer vervangen, dan is wat we hebben niet meer te vertrouwen en
  // beginnen we schoon opnieuw (gedeeld met de gewone start, zie syncAssetVersion).
  const cache = await syncAssetVersion(manifest);

  const total = assets.length;
  let done = 0;
  let failed = 0;
  let vol = 0;            // waarvan omdat de opslag vol is (QuotaExceededError)
  const mist = [];        // de eerste paar bestanden die niet lukten, voor de console van het spel

  function noteer(rel, waarom) {
    failed++;
    if (mist.length < 5) mist.push(rel + ' (' + waarom + ')');
  }

  const queue = assets.slice();

  async function worker() {
    for (;;) {
      const rel = queue.shift();
      if (rel === undefined) return;
      const req = new Request(rel, { cache: 'no-cache' });
      try {
        if (!(await cache.match(req, { ignoreVary: true }))) {
          const res = await fetch(req);
          if (res.ok) await cache.put(req, res.clone());
          else noteer(rel, 'HTTP ' + res.status);
        }
      } catch (err) {
        if (isVol(err)) vol++;
        noteer(rel, isVol(err) ? 'opslag vol' : String((err && err.message) || err));
      }
      done++;
      // Niet bij elk bestand een bericht: dat zou honderden keren per seconde
      // de hoofdthread onderbreken terwijl de balk toch maar een pixel opschuift.
      if (done % 5 === 0 || done === total) {
        await post({ type: 'precache-progress', deel, done, total, failed });
      }
    }
  }

  await Promise.all(Array.from({ length: PARALLEL }, worker));

  // De versie alleen bevestigen als alles binnen is. Mislukte er iets, dan blijft het bij de stempel
  // die syncAssetVersion aan het begin zette: die zegt alleen van welke versie de bestanden zijn die er
  // wel staan, en reportStatus telt per bestand, dus de knop blijft op "Download voor offline" en een
  // volgende poging haalt via cache.match alleen het ontbrekende op. Ook bij een volle opslag mag deze
  // laatste put het klaarbericht niet tegenhouden: zonder dat bleef de knop voorgoed op "Bezig" staan.
  if (failed === 0) {
    try {
      await cache.put(VERSION_KEY, new Response(manifest.version));
    } catch (err) {
      noteer('versie', isVol(err) ? 'opslag vol' : String((err && err.message) || err));
      if (isVol(err)) vol++;
    }
  }
  // Geen reportStatus erachteraan: die zou de klaarmelding meteen weer
  // overschrijven met een telling. Het spel weet uit dit bericht genoeg.
  await post({ type: 'precache-done', deel, total, failed, vol, mist, bytes: bytesVoor(manifest, set, deel) });
}
