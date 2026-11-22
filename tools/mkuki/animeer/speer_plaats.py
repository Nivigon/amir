"""Speerplaatsing voor de Animeer tool Mkuki, kritischer dan de ruwe meting uit plaatsing.json.

Per set een vaste speerlengte L (de speer is een voorwerp, hij hoort niet te groeien of te krimpen).
Per frame met gemeten tip T, kont K en lengte m:
- m >= 0,9 L: lengte L, met de hand op dezelfde plek langs de schacht (of hetzelfde midden zonder hand).
- m < 0,9 L en een uiteinde verdwijnt in het lijf (achter het lijf of de hand): dat eind doortrekken tot L,
  speer achter het lijf.
- m < 0,9 L en beide uiteinden vrij: de speer wijst van ons af of naar ons toe (verkort). Dan een verkorte
  speer (hoek kNN: in de lengte samengedrukt, even dik), zodat hij niet dunner en kleiner wordt.
- Is er bijna niets van over (m < 0,3 L, vrij), dan is het geen speer: uit.
"""
import math
import numpy as np

KS = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
# Langere schacht (punt, lint en dikte gelijk): voor frames waar het origineel de speer langer tekende (stoot).
LS = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]
# Frames waarin de speer in het origineel al weg is (na de worp); de meting vond daar armen of benen.
UIT = {'rolworp_sp': set(range(24, 34))}
# In het origineel loopt de speer hier achter het hoofd langs (de meting zag dat niet).
ACHTER = {'strike_sp': {2, 3}, 'rolworp_sp': set(range(16, 24))}  # rol/worp 16-23: Mkuki-vuist lager, speer achter het hoofd
# Hier vindt het vuistzoeken het hoofd in plaats van de hand (de hand zit achter het hoofd): niet schuiven.
NIET_SNAP = {'worp_sp'}
# Vaste lengte per set: speer = 5,7 x de breedte van het hoofd (zo is hij in idle, ren, springen, bukken,
# sluipen en worp, 5,4 tot 5,8). In deze sets tekende Grok hem in het origineel te lang (combo en lage zwaai
# 7,6 tot 8,7, rol 6,9) of wisselend; daar is hij teruggezet naar 5,7 x hoofd. Strike en trap: zelfde maat als de idle.
# Twee maten: de lengte volgt het origineel (L, vorm), de dikte, punt en het lint volgen MAAT (5,7 x hoofd).
# Een langere of kortere speer is dus een langere of kortere schacht (hoek lNNN of kNN), niet een dikkere speer.
L_VAST = {'strike_sp': 273, 'idle_sp_los': 274, 'trap_sp': 274}
MAAT = {'rol_sp': 302, 'rolworp_sp': 342, 'combo_sp': 262, 'sweep_sp': 544, 'stof_sp': 268}
VAR = sorted(KS + [1.0] + LS)


def variant(D, maat):
    f = min(VAR, key=lambda x: abs(x - D / maat))
    return 'proj' if f == 1.0 else ('k%02d' % round(f * 100) if f < 1 else 'l%03d' % round(f * 100))


def set_lengte(sid, lengtes):
    if sid in L_VAST:
        return L_VAST[sid]
    v = sorted(lengtes)
    p90 = v[min(len(v) - 1, int(round(0.9 * (len(v) - 1))))]
    top = [x for x in v if x >= 0.85 * p90]
    return float(np.median(top))


def verdwijnt(alpha, p, u, schaal):
    """Loopt de speer voorbij punt p in richting u het lijf in (ondoorzichtige pixels voorbij het eind)?"""
    H, W = alpha.shape
    n = goed = 0
    for d in np.arange(6, 30, 2) * schaal:
        x, y = int(round(p[0] + u[0] * d)), int(round(p[1] + u[1] * d))
        if 0 <= x < W and 0 <= y < H:
            n += 1
            goed += alpha[y, x] > 100
    return n > 0 and goed / n >= 0.6


def bedekt(alpha, a, b, schaal):
    """Welk deel van het stuk a..b ligt in het origineel onder het lijf (ondoorzichtig)?"""
    H, W = alpha.shape
    n = max(2, int(np.linalg.norm(b - a) / (3 * schaal)))
    goed = tel = 0
    for t in np.linspace(0, 1, n):
        x, y = (a + (b - a) * t).round().astype(int)
        tel += 1
        if 0 <= x < W and 0 <= y < H and alpha[y, x] > 100:
            goed += 1
    return goed / tel


def plaats(sid, q, alpha, L, CW, CH, schaal, maat=None):
    """Geeft (laag, notitie). q is de meting uit plaatsing.json."""
    T, K = np.array(q['tip'], float), np.array(q['kont'], float)
    m = float(np.linalg.norm(T - K)) or 1.0
    u = (T - K) / m
    achter = bool(q.get('achter'))
    hoek = 'proj'; w = L; noot = ''
    if m >= 0.9 * L:
        ts = sorted(min(1.0, max(0.0, float(np.dot(np.array(h, float) - K, u)) / m)) for h in q.get('handen', []))
        if m > 1.1 * L:
            # Het origineel tekent de speer hier langer (stoot): plek en lengte van het origineel, maar met
            # een langere schacht, zodat punt, lint en dikte gelijk blijven aan de rest van de set.
            K2, T2 = K, T
            noot = 'langer zoals het origineel (%d%%)' % round(100 * m / L)
        elif ts:
            t = float(np.mean(ts))                   # plek van de hand langs de schacht, 0 = kont, 1 = tip
            K2 = K + u * t * m - u * t * L
        else:
            K2 = (T + K) / 2 - u * L / 2
        if m <= 1.1 * L: T2 = K2 + u * L
    else:
        kv, tv = verdwijnt(alpha, K, -u, schaal), verdwijnt(alpha, T, u, schaal)
        # Doortrekken mag alleen als het nieuwe stuk in het origineel echt achter het lijf zat
        # (anders hadden we de speer daar gezien): dan wijst hij van ons af of naar ons toe.
        kand = []
        if kv and not tv: kand.append((T, T - u * L, 'kont liep achter het lijf: doorgetrokken', [(K, T - u * L)]))
        if tv and not kv: kand.append((K + u * L, K, 'punt liep achter het lijf: doorgetrokken', [(T, K + u * L)]))
        if kv and tv:
            c0 = (T + K) / 2
            kand.append((c0 + u * L / 2, c0 - u * L / 2, 'beide einden achter het lijf: doorgetrokken', [(K, c0 - u * L / 2), (T, c0 + u * L / 2)]))
        gekozen = None
        for T3, K3, nt, stukken in kand:
            ok = all(bedekt(alpha, a, b, schaal) >= 0.5 for a, b in stukken)
            binnen = all(-0.02 * CW <= p[0] <= 1.02 * CW and -0.05 * CH <= p[1] <= CH for p in (T3, K3))
            if ok and binnen: gekozen = (T3, K3, nt)
        if gekozen:
            T2, K2, noot = gekozen; achter = True
        elif m < 0.3 * L:
            return None, 'bijna geen speer zichtbaar (%d van %d): uit' % (round(m), round(L))
        else:
            T2, K2 = T, K
            noot = 'verkort (wijst van ons af of naar ons toe), %d%%' % round(100 * m / L)
    D = float(np.linalg.norm(T2 - K2)); w = D
    hoek = variant(D, maat or L)
    c = (T2 + K2) / 2
    rot = math.degrees(math.atan2(T2[1] - K2[1], T2[0] - K2[0]))
    laag = {'on': True, 'angle': hoek, 'cx': round(c[0] / CW, 4), 'cy': round(c[1] / CH, 4),
            'w': round(w / CW, 4), 'rot': round(rot, 1), 'flip': False, 'behind': achter, 'op': 1, 'locked': False}
    return laag, noot


def vuist_snap(laag, q, mk_alpha, CW, CH, schaal):
    """Grok zette de hand soms ergens anders dan in het origineel (bv. rol/worp 16-23: de geheven vuist lager).
    Ligt een gemeten hand niet op het Mkuki-lijf, dan schuiven we de speer dwars op zijn as tot hij door de
    dichtstbijzijnde Mkuki-vuist loopt. Geeft (laag, notitie of '')."""
    if not laag or not laag['on'] or not q.get('handen'):
        return laag, ''
    H, W = mk_alpha.shape
    R = int(45 * schaal); r = max(2, int(4 * schaal))
    rot = math.radians(laag['rot']); u = np.array([math.cos(rot), math.sin(rot)]); n = np.array([-u[1], u[0]])
    c = np.array([laag['cx'] * CW, laag['cy'] * CH])
    yy, xx = np.mgrid[0:H, 0:W]
    verschuif = []
    for hx, hy in q['handen']:
        x, y = int(hx), int(hy)
        if mk_alpha[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1].max() >= 100:
            continue
        d2 = (xx - hx) ** 2 + (yy - hy) ** 2
        vol = (mk_alpha > 100) & (d2 <= R * R)
        if not vol.any():
            continue
        k = np.argmin(np.where(vol, d2, 1e12)); py, px = divmod(k, W)
        buurt = vol & ((xx - px) ** 2 + (yy - py) ** 2 <= (12 * schaal) ** 2)
        fx, fy = xx[buurt].mean(), yy[buurt].mean()
        verschuif.append(float(np.dot(np.array([fx, fy]) - c, n)))
    if not verschuif:
        return laag, ''
    s = float(np.mean(verschuif))
    if abs(s) < 3 * schaal:
        return laag, ''
    c2 = c + n * s
    laag = dict(laag, cx=round(c2[0] / CW, 4), cy=round(c2[1] / CH, 4))
    return laag, 'door de Mkuki-vuist geschoven (%d px)' % round(abs(s))
