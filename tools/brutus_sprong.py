# Nyundo: de sprong (afzet, vlucht) en de landing uit twee Grok-clips naar enemies/brutus/frames.
# Gebruik: python3 tools/brutus_sprong.py <sprong.mp4> <landing.mp4> [uitmap voor een contactblad]
# Keyen (smalle ramp, alleen despill), een schaal en een verschuiving voor beide clips (ze delen hetzelfde
# canvas: de landing begint precies waar de sprong eindigt), omkleuren naar de speelkleuren (broek zwart,
# sjerp bloedrood, windsels ijzer) en de regels in brutus.json. Zie notities/brutus.md, "De sprong".
import sys, os, json, subprocess, tempfile, colorsys
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT = os.path.join(os.path.dirname(__file__), '..', 'enemies', 'brutus')
SCHAAL = 1.04            # clip-pixels naar grote-set-pixels (op de kop gemeten tegen idle_00)
GROND = 447              # de grondlijn in de clips (onderkant van de voeten in de afzet en de eindpose)
SPRONG = [0] + list(range(14, 67, 3))
LANDING = list(range(0, 17, 2)) + list(range(17, 23))

def frames(mp4, idx):
    d = tempfile.mkdtemp()
    subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, os.path.join(d, '%03d.png')], check=True)
    return [np.array(Image.open(os.path.join(d, f'{i + 1:03d}.png')).convert('RGB')).astype(np.float32) for i in idx]

def key(rgb):
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    k = np.minimum(R, B) - G
    bg = np.median(np.concatenate([rgb[:20].reshape(-1, 3), rgb[:, :20].reshape(-1, 3)]), 0)
    kbg = min(bg[0], bg[2]) - bg[1]
    a = np.clip((0.92 * kbg - k) / (0.30 * kbg), 0, 1)
    m = a > 0.5
    lab, n = ndimage.label(m)
    if n:
        s = ndimage.sum(m, lab, range(1, n + 1)); keep = np.zeros(n + 1, bool); keep[1:] = s > 60
        a = a * ndimage.binary_dilation(keep[lab], iterations=3)
    aa = np.maximum(a, 0.05)[..., None]
    F = np.where(a[..., None] < 0.99, (rgb - (1 - aa) * bg) / aa, rgb)
    F = np.clip(F, 0, 255)
    # magenta die Grok in snelle beweging door het lijf veegt (bal, steel, handen): geen enkele kleur van Nyundo heeft
    # rood en blauw allebei boven groen, dus zo'n pixel wordt grijs met de helderheid die groen nog aangeeft
    sp = (np.minimum(F[..., 0], F[..., 2]) - F[..., 1] > 4) & (a > 0.3)
    gr = np.clip(F[..., 1] * 1.15 + 10, 0, 255)
    F = np.where(sp[..., None], gr[..., None] * np.array([0.98, 1.0, 1.04]), F)
    F = np.where((a < 0.9)[..., None], F * 0.35, F)                  # de rand is de zwarte omlijning: geen roze of rode zoom
    return np.clip(F, 0, 255), a

def kleur(F, a):
    f = F / 255.0
    mx, mn = f.max(-1), f.min(-1); v = mx; s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-4), 0)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    h = np.zeros_like(v); d = np.maximum(mx - mn, 1e-4)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    on = a > 0.05
    broek = on & (h >= 12) & (h < 34) & (s > 0.80) & (v > 0.30)
    sjerp = on & (h >= 34) & (h < 62) & (s > 0.55) & (v > 0.45)
    wind = on & (h >= 165) & (h < 250) & (s > 0.35)
    koel = on & ~wind & (h >= 62) & (h < 340)                     # alles wat niet warm is (de bal, de steel-ijzer): Grok kleurt
    #   de bal in snelle frames blauw, groen of paars, dus grijs maken met dezelfde helderheid
    out = F.copy()
    for m, base, ref in ((broek, (34, 30, 34), 0.86), (sjerp, (139, 17, 21), 0.92), (wind, (95, 98, 105), 0.85)):
        t = np.clip(v / ref, 0, 1.25)[..., None]
        out = np.where(m[..., None], np.clip(np.array(base) * t, 0, 255), out)
    sy = np.nonzero(sjerp)[0]                                    # onder de sjerp is rood de rand van de broek, geen haar
    if len(sy):
        onder = np.zeros_like(on); onder[int(np.median(sy)):] = True
        rand = on & onder & ((h < 12) | (h >= 340)) & (s > 0.45)
        out = np.where(rand[..., None], np.clip(np.array((34, 30, 34)) * np.clip(v / 0.86, 0, 1.25)[..., None], 0, 255), out)
    out = np.where(koel[..., None], (v * 255)[..., None] * np.array([0.98, 1.0, 1.04]), out)
    return np.clip(out, 0, 255)

def heup(F, a):                       # het midden van de sjerp (geel in de bron): het anker
    f = F / 255.0; r, g, b = f[..., 0], f[..., 1], f[..., 2]
    m = (a > 0.5) & (r > 0.7) & (g > 0.55) & (b < 0.35)
    xs = np.nonzero(m)[1]
    return float(np.median(xs)) if len(xs) else None

def bal_onder(F, a):                  # de onderkant van de ijzeren bal (grijs)
    mx, mn = F.max(-1), F.min(-1)
    m = (a > 0.6) & (mx - mn < 28) & (mx > 35) & (mx < 175)
    m = ndimage.binary_opening(m, iterations=2)
    lab, n = ndimage.label(m)
    if not n: return None
    s = ndimage.sum(m, lab, range(1, n + 1)); ys = np.nonzero(lab == np.argmax(s) + 1)[0]
    return int(ys.max())

def main():
    sp, la = sys.argv[1], sys.argv[2]
    uit = sys.argv[3] if len(sys.argv) > 3 else None
    S = frames(sp, SPRONG); L = frames(la, LANDING)
    F0, a0 = key(S[0]); ankX = heup(F0, a0)
    data = json.load(open(os.path.join(ROOT, 'brutus.json')))
    res = {}
    for naam, lijst, idx in (('sprong', S, SPRONG), ('landing', L, LANDING)):
        fr = []
        for j, (rgb, bron) in enumerate(zip(lijst, idx)):
            F, a = key(rgb)
            voet = int(np.nonzero((a > 0.5).any(1))[0].max())
            bo = bal_onder(F, a)
            F = kleur(F, a)
            ys, xs = np.nonzero(a > 0.02)
            x0, x1, y0, y1 = xs.min() - 2, xs.max() + 3, ys.min() - 2, ys.max() + 3
            x0, y0 = max(0, x0), max(0, y0)
            rgba = np.dstack([F, a * 255]).astype(np.uint8)[y0:y1, x0:x1]
            im = Image.fromarray(rgba, 'RGBA')
            w, h = round(im.width * SCHAAL), round(im.height * SCHAAL)
            im = im.resize((w, h), Image.LANCZOS)
            src = f'frames/{naam}_{j:02d}.png'
            im.save(os.path.join(ROOT, src), optimize=True)
            los = round((GROND - voet) * SCHAAL)      # hoe hoog Grok hem liet springen: dat doet de engine, dus eruit
            fr.append({'src': src, 'dx': round((x0 - ankX) * SCHAAL), 'dy': round((y0 - GROND) * SCHAAL) + max(0, los), 'w': w, 'h': h,
                       'ms': 50, 'bron': bron, 'los': los,
                       'bal': None if bo is None else round((GROND - bo) * SCHAAL)})
            if uit:
                c = Image.new('RGBA', (640, 480), (90, 90, 90, 255)); c.alpha_composite(Image.fromarray(np.dstack([F, a * 255]).astype(np.uint8)))
                c.convert('RGB').save(os.path.join(uit, f'{naam}_{j:02d}.png'))
        res[naam] = fr
    # de verplaatsing: waar zijn heup in de eindpose staat t.o.v. het anker (zodat de idle daarna aansluit)
    Fe, ae = key(L[-1]); hx = heup(Fe, ae)
    data['bewegingen']['sprong'] = {'loop': False, 'frames': res['sprong']}
    data['bewegingen']['landing'] = {'loop': False, 'verplaatsing': round((hx - ankX) * SCHAAL) if hx else 0, 'frames': res['landing']}
    data['sprongBron'] = ('jump1.mp4 en landing1.mp4 (Grok, begin- en eindframes uit drie sleutelhoudingen: afzet, lucht, inslag), '
                          'x' + str(SCHAAL).replace('.', ',') + ', een verschuiving voor beide; los: hoe hoog Grok zijn voeten boven de grond had (uit dy gehaald, de engine tilt hem), bal: de onderkant van de bal boven de grond')
    json.dump(data, open(os.path.join(ROOT, 'brutus.json'), 'w'), ensure_ascii=False, indent=1)
    for n in res: print(n, [(f['bron'], f['los'], f['bal']) for f in res[n]])
    print('anker', ankX, 'verplaatsing', data['bewegingen']['landing']['verplaatsing'])

main()
