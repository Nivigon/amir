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
const ASSET_CACHE = 'amir-assets-v1';

// Sleutel waaronder we in de assetcache bijhouden welke assetversie erin zit.
// Geen echt bestand, alleen een plek om een string te bewaren.
const VERSION_KEY = new URL('./__offline-version__', self.location).href;

const SHELL = [
  './',
  './index.html',
  './amir-king-of-africa.html',
  './manifest.webmanifest',
  './offline-assets.json',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
];

// Hoeveel bestanden we tegelijk ophalen bij het downloaden. Hoog genoeg om de
// lijn te vullen, laag genoeg om Safari niet te laten stikken in verzoeken.
const PARALLEL = 6;

const isAsset = (url) => /\.(png|jpe?g|mp3)$/i.test(url.pathname);
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
      cache.put(req, res.clone()).catch(() => {});
    }
    return res;
  } catch (err) {
    // Offline en niet in de cache. Geen bruikbaar antwoord te geven.
    return new Response('', { status: 504, statusText: 'offline' });
  }
}

/** Beantwoordt een Range-verzoek uit de assetcache met een echte 206. */
async function rangeFromCache(req) {
  const cache = await caches.open(ASSET_CACHE);
  // De cache is gevuld met hele bestanden, dus matchen zonder het Range-verzoek.
  const plain = new Request(req.url);
  let hit = await cache.match(plain, { ignoreVary: true });

  if (!hit) {
    // Nog niet in de cache: het hele bestand halen en bewaren, dan snijden.
    try {
      const res = await fetch(plain);
      if (!res.ok) return fetch(req);
      await cache.put(plain, res.clone());
      hit = res;
    } catch (err) {
      return new Response('', { status: 504, statusText: 'offline' });
    }
  }

  const buf = await hit.arrayBuffer();
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
    if (res && res.ok) cache.put(req, res.clone()).catch(() => {});
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

self.addEventListener('message', (event) => {
  const data = event.data || {};
  if (data.type === 'precache') event.waitUntil(precacheAll());
  else if (data.type === 'status') event.waitUntil(reportStatus());
  else if (data.type === 'clear') event.waitUntil(clearAssets());
});

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

async function reportStatus() {
  try {
    const manifest = await loadManifest();
    const cache = await caches.open(ASSET_CACHE);
    const keys = await cache.keys();
    const have = new Set(keys.map((r) => new URL(r.url).pathname));
    // Via de URL-parser vergelijken, niet via plakken: bestandsnamen met een
    // spatie staan in de cache als %20 en zouden anders als missend tellen.
    let done = 0;
    for (const rel of manifest.assets) {
      if (have.has(new URL(rel, self.location).pathname)) done++;
    }
    await post({
      type: 'status',
      done,
      total: manifest.assets.length,
      bytes: manifest.bytes,
      version: manifest.version,
    });
  } catch (err) {
    await post({ type: 'status', error: String(err.message || err) });
  }
}

async function clearAssets() {
  await caches.delete(ASSET_CACHE);
  await post({ type: 'cleared' });
  await reportStatus();
}

async function precacheAll() {
  let manifest;
  try {
    manifest = await loadManifest();
  } catch (err) {
    await post({ type: 'precache-error', message: String(err.message || err) });
    return;
  }

  // Zijn de assets sinds de vorige download vervangen, dan is wat we hebben
  // niet meer te vertrouwen en beginnen we schoon opnieuw.
  let cache = await caches.open(ASSET_CACHE);
  const stamp = await cache.match(VERSION_KEY);
  const seen = stamp ? await stamp.text() : null;
  if (seen && seen !== manifest.version) {
    await caches.delete(ASSET_CACHE);
    cache = await caches.open(ASSET_CACHE);
  }

  const total = manifest.assets.length;
  let done = 0;
  let failed = 0;

  const queue = manifest.assets.slice();

  async function worker() {
    for (;;) {
      const rel = queue.shift();
      if (rel === undefined) return;
      const req = new Request(rel, { cache: 'no-cache' });
      try {
        if (!(await cache.match(req, { ignoreVary: true }))) {
          const res = await fetch(req);
          if (res.ok) await cache.put(req, res.clone());
          else failed++;
        }
      } catch (err) {
        failed++;
      }
      done++;
      // Niet bij elk bestand een bericht: dat zou honderden keren per seconde
      // de hoofdthread onderbreken terwijl de balk toch maar een pixel opschuift.
      if (done % 5 === 0 || done === total) {
        await post({ type: 'precache-progress', done, total, failed });
      }
    }
  }

  await Promise.all(Array.from({ length: PARALLEL }, worker));

  await cache.put(VERSION_KEY, new Response(manifest.version));
  // Geen reportStatus erachteraan: die zou de klaarmelding meteen weer
  // overschrijven met een telling. Het spel weet uit dit bericht genoeg.
  await post({ type: 'precache-done', total, failed, bytes: manifest.bytes });
}
