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
# Frames waarin de speer in het origineel al weg is (na de worp); de meting vond daar armen of benen.
UIT = {'rolworp_sp': set(range(24, 34))}
# Vaste lengte per set: speer = 5,7 x de breedte van het hoofd (zo is hij in idle, ren, springen, bukken,
# sluipen en worp, 5,4 tot 5,8). In deze sets tekende Grok hem in het origineel te lang (combo en lage zwaai
# 7,6 tot 8,7, rol 6,9) of wisselend; daar is hij teruggezet naar 5,7 x hoofd. Strike en trap: zelfde maat als de idle.
L_VAST = {'strike_sp': 273, 'idle_sp_los': 274, 'trap_sp': 274, 'rol_sp': 302, 'rolworp_sp': 342,
          'combo_sp': 262, 'sweep_sp': 544, 'stof_sp': 268}


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


def plaats(sid, q, alpha, L, CW, CH, schaal):
    """Geeft (laag, notitie). q is de meting uit plaatsing.json."""
    T, K = np.array(q['tip'], float), np.array(q['kont'], float)
    m = float(np.linalg.norm(T - K)) or 1.0
    u = (T - K) / m
    achter = bool(q.get('achter'))
    hoek = 'proj'; w = L; noot = ''
    if m >= 0.9 * L:
        ts = sorted(min(1.0, max(0.0, float(np.dot(np.array(h, float) - K, u)) / m)) for h in q.get('handen', []))
        if m > 1.1 * L:
            # Uitgerekte speer (Grok rekte hem in de stoot): de kont blijft in de achterste hand,
            # de punt komt op de vaste lengte; de voorste hand moet nog om de schacht zitten.
            K2 = K.copy()
            if ts and ts[-1] * m > 0.9 * L:
                K2 = K + u * (ts[-1] * m - 0.9 * L)
        elif ts:
            t = float(np.mean(ts))                   # plek van de hand langs de schacht, 0 = kont, 1 = tip
            K2 = K + u * t * m - u * t * L
        else:
            K2 = (T + K) / 2 - u * L / 2
        T2 = K2 + u * L
        if abs(m - L) > 0.1 * L:
            noot = 'lengte gelijkgetrokken (%d naar %d)' % (round(m), round(L))
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
            k = min(KS, key=lambda x: abs(x - m / L))
            hoek = 'k%02d' % round(k * 100)
            T2, K2 = T, K; w = m
            noot = 'verkort (wijst van ons af of naar ons toe), %d%%' % round(100 * k)
    c = (T2 + K2) / 2
    rot = math.degrees(math.atan2(T2[1] - K2[1], T2[0] - K2[0]))
    laag = {'on': True, 'angle': hoek, 'cx': round(c[0] / CW, 4), 'cy': round(c[1] / CH, 4),
            'w': round(w / CW, 4), 'rot': round(rot, 1), 'flip': False, 'behind': achter, 'op': 1, 'locked': False}
    return laag, noot
