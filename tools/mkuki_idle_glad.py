#!/usr/bin/env python3
"""Mkuki idle met speer (idle/idle_sp, 20 frames) glad: een lijf, bewogen zoals de oude idle.

De 20 losse Grok-frames verschilden elk een beetje (nek, kralen, schort en broek wiebelden tot 5 px). Dit script neemt
alleen frame 0 van de Mkuki-skin en beweegt dat per frame zoals de oude Amir in karakters/amir/idle/idle_sp/:
  - bovenlijf en hoofd: optical flow van de oude frames (frame i naar 0), vanaf de riem naar beneden uitlopend tot 0,
    zodat riem, schort, broek en benen stilstaan (zoals in het origineel);
  - de verre arm: bovenarm om de schouder en onderarm om de elleboog, met de hoeken gemeten op de arm van de oude Amir
    (de hand gaat rond frame 10 naar de heup);
  - de vuist (boven/vuist): dezelfde flow;
  - een donkere buitenrand om het lijf en om de arm, zoals de oude Amir die heeft.
De zonekaarten gaan precies zo mee (zonder interpolatie), de speer blijft los op zijn plek uit los.json.

  python3 tools/mkuki_idle_glad.py <mkuki-checkout>

Schrijft in deze repo karakters/amir/mkuki_spel/idle/idle_sp/ (frame, _lijf, _boven, _zones, _lijf_zones, _boven_zones)
en de helft in klein/, en in <mkuki-checkout> karakters/amir/mkuki/idle/idle_sp/ (lijf, _vuist, _zones, _vuist_zones),
zodat de Animeer tool en een volgende bak dezelfde frames hebben. Het leest frame 0 uit idle/idle_sp/bron/ in <mkuki-checkout>
(de eerste keer daar neergezet), dus opnieuw draaien geeft hetzelfde.
"""
import json, os, sys
import numpy as np, cv2
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEL = os.path.join(REPO, 'karakters/amir/mkuki_spel')
KLEIN = os.path.join(REPO, 'klein/karakters/amir/mkuki_spel')
SET = 'idle/idle_sp/idle_sp_%02d'
N = 20
INKT = np.array([24, 15, 12], np.float32)      # de kleur van de rand
RIEM = 142                                       # boven deze y beweegt het lijf, eronder staat het stil
ARM = dict(x=337, y0=108, y1=205, elleboog=147, schouder=112)


def rgba(p): return np.asarray(Image.open(p).convert('RGBA'))


def grijs(a):
    return (cv2.cvtColor(a[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32) * (a[:, :, 3] / 255.)).astype(np.uint8)


def pm_doe(img, f):
    """f op een plaatje met voorvermenigvuldigde alfa (geen donkere randjes)."""
    x = img.astype(np.float32); a = x[:, :, 3:] / 255.
    w = f(np.concatenate([x[:, :, :3] * a, x[:, :, 3:]], 2))
    al = np.clip(w[:, :, 3:], 1e-3, None) / 255.
    rgb = np.where(w[:, :, 3:] > 0.5, w[:, :, :3] / al, 0)
    return np.clip(np.concatenate([rgb, w[:, :, 3:]], 2), 0, 255).astype(np.uint8)


def remap(img, mx, my, zone):
    if zone:
        return cv2.remap(img, mx, my, cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return pm_doe(img, lambda x: cv2.remap(x, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0))


def affien(img, M, zone):
    H, W = img.shape[:2]
    if zone:
        return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_NEAREST, borderValue=(0, 0, 0, 0))
    return pm_doe(img, lambda x: cv2.warpAffine(x, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0))


def over(a, b):
    A = Image.fromarray(a); A.alpha_composite(Image.fromarray(b)); return np.asarray(A)


def rand(img, sterk=0.75, br=1.6):
    f = img.astype(np.float32); m = (f[:, :, 3] > 110).astype(np.uint8)
    d = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    w = np.clip((br + 0.5 - d) / br, 0, 1) * sterk * (m > 0)
    f[:, :, :3] = f[:, :, :3] * (1 - w[..., None]) + INKT * w[..., None]
    return f.astype(np.uint8)


def oude_arm(a, gx, gy):
    a = a.astype(int); r, g, b, al = [a[:, :, k] for k in range(4)]
    huid = (al > 200) & (r < 130) & (r > g) & (g >= b - 5) & (r + g + b < 330)
    m = huid & (gy >= 120) & (gy <= 196) & (((gx >= 338) & (gy < 150)) | ((gx >= 322) & (gy >= 150)))
    n, l, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    return l == 1 + np.argmax(st[1:, 4])


def iou(a, b): return (a & b).sum() / max(1, (a | b).sum())


def arm_hoeken(O, gx, gy):
    """Per frame de draai van bovenarm (om de schouder) en onderarm (om de elleboog) van de oude Amir."""
    H, W = gx.shape
    A = [oude_arm(a, gx, gy) for a in O]
    S0 = np.array([349., 120.]); EY = 150
    ys, xs = np.where(A[0] & (gy > EY - 3) & (gy < EY + 3)); E0 = np.array([xs.mean(), float(EY)])
    up0 = (A[0] & (gy < EY)).astype(np.uint8); lo0 = (A[0] & (gy >= EY)).astype(np.uint8)
    t1s, t2s = [], []
    for i in range(N):
        best = None
        for dx in (-2, -1, 0, 1, 2):
            for dy in range(-7, 2):
                for t1 in range(-30, 31, 2):
                    M = cv2.getRotationMatrix2D(tuple(S0), t1, 1.0); M[:, 2] += [dx, dy]
                    u = cv2.warpAffine(up0, M, (W, H), flags=cv2.INTER_NEAREST) > 0
                    sc = iou(u, A[i] & (gy < EY + dy))
                    if best is None or sc > best[0]: best = (sc, t1, M)
        _, t1, M = best
        E = M @ np.array([E0[0], E0[1], 1])
        u = cv2.warpAffine(up0, M, (W, H), flags=cv2.INTER_NEAREST) > 0
        b2 = None
        for t2 in range(-80, 31, 2):
            Mt = np.vstack([cv2.getRotationMatrix2D(tuple(E), t2, 1.0), [0, 0, 1]]) @ np.vstack([M, [0, 0, 1]])
            lw = cv2.warpAffine(lo0, Mt[:2], (W, H), flags=cv2.INTER_NEAREST) > 0
            s = iou(u | lw, A[i])
            if b2 is None or s > b2[0]: b2 = (s, t2)
        t1s.append(t1); t2s.append(b2[1])
    zacht = lambda v: (np.roll(v, 1) + 2 * v + np.roll(v, -1)) / 4
    return zacht(zacht(np.array(t1s, float))), zacht(zacht(np.array(t2s, float)))


def speer(L, i, W, H):
    s = L['frames'][SET % i + '.png']['s']
    sp = Image.open(os.path.join(SPEL, 'bron/amirspeer_%s.png' % s['a'])).convert('RGBA')
    w = s['w'] * W; h = w * L['hoeken'][s['a']]['asp']
    sp = sp.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)
    if s['f']: sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
    sp = sp.rotate(-s['r'], resample=Image.BICUBIC, expand=True)
    c = Image.new('RGBA', (W, H)); c.alpha_composite(sp, (round(s['cx'] * W - sp.width / 2), round(s['cy'] * H - sp.height / 2)))
    return np.asarray(c)


def bewaar(a, pad, zone=False):
    im = Image.fromarray(a)
    os.makedirs(os.path.dirname(pad), exist_ok=True); im.save(pad, optimize=True)
    return im


def main():
    mk = os.path.join(sys.argv[1], 'karakters/amir/mkuki')
    L = json.load(open(os.path.join(SPEL, 'los.json')))
    for i in range(N):
        s = L['frames'][SET % i + '.png']
        assert not s.get('sm') and not s['s'].get('b'), 'idle_sp: speer achter of maskers, niet voorzien'
    O = [rgba(os.path.join(REPO, 'karakters/amir/' + SET % i + '.png')) for i in range(N)]
    H, W = O[0].shape[:2]
    gy, gx = np.mgrid[0:H, 0:W]
    bron = os.path.join(mk, 'idle/idle_sp/bron')                       # frame 0 zoals Grok hem gaf, eenmalig bewaard
    if not os.path.isdir(bron):
        os.makedirs(bron)
        for ach in ('.png', '_vuist.png', '_zones.png', '_vuist_zones.png'):
            Image.open(os.path.join(mk, SET % 0 + ach)).save(os.path.join(bron, 'idle_sp_00' + ach))
    lijf0 = rgba(os.path.join(bron, 'idle_sp_00.png'))
    vuist0 = rgba(os.path.join(bron, 'idle_sp_00_vuist.png'))
    lz0 = rgba(os.path.join(bron, 'idle_sp_00_zones.png'))
    vz0 = rgba(os.path.join(bron, 'idle_sp_00_vuist_zones.png'))

    kled = (lz0[:, :, 3] > 0) & ~((lz0[:, :, :3] == [255, 128, 0]).all(2))   # kleding, behalve de armbanden
    armm = (lijf0[:, :, 3] > 0) & (gx >= ARM['x']) & (gy >= ARM['y0']) & (gy <= ARM['y1']) & ~kled
    def deel(img, m):
        x = img.copy(); x[~m] = 0; return x
    EY = ARM['elleboog']
    E0 = np.array([np.where(armm[EY])[0].mean(), EY]); S0 = np.array([np.where(armm[ARM['schouder']])[0].mean(), 110.])
    boven_arm = armm & (gy < EY + 3); onder_arm = armm & (gy >= EY - 3)
    t1, t2 = arm_hoeken(O, gx, gy)

    G0 = grijs(O[0])
    for i in range(N):
        fl = cv2.calcOpticalFlowFarneback(grijs(O[i]), G0, None, 0.5, 4, 21, 5, 7, 1.5, 0)
        for k in (0, 1): fl[..., k] = cv2.GaussianBlur(fl[..., k], (0, 0), 5)
        vmx = (gx + fl[..., 0]).astype(np.float32); vmy = (gy + fl[..., 1]).astype(np.float32)
        fr = fl * np.clip((RIEM - gy) / 20., 0, 1)[..., None]
        mx = (gx + fr[..., 0]).astype(np.float32); my = (gy + fr[..., 1]).astype(np.float32)
        d = -fl[int(S0[1]), int(S0[0])]
        M1 = cv2.getRotationMatrix2D(tuple(S0), t1[i], 1.0); M1[:, 2] += d
        E = M1 @ np.array([E0[0], E0[1], 1])
        M2 = (np.vstack([cv2.getRotationMatrix2D(tuple(E), t2[i], 1.0), [0, 0, 1]]) @ np.vstack([M1, [0, 0, 1]]))[:2]

        def lijf_van(img, zone):
            rest = remap(deel(img, ~armm), mx, my, zone)
            arm = over(affien(deel(img, onder_arm), M2, zone), affien(deel(img, boven_arm), M1, zone))
            if zone: return over(rest, arm)
            return rand(over(rand(rest), rand(arm)), 0.5)
        lijf = lijf_van(lijf0, False); lz = lijf_van(lz0, True)
        lz = lz.copy(); lz[lijf[:, :, 3] == 0] = 0                       # geen zone buiten het lijf
        vuist = rand(remap(vuist0, vmx, vmy, False), 0.6); vz = remap(vz0, vmx, vmy, True)
        vz = vz.copy(); vz[vuist[:, :, 3] == 0] = 0
        sp = speer(L, i, W, H)
        frame = over(over(lijf, sp), vuist)
        z = lz.copy(); z[sp[:, :, 3] > 0] = 0; z = over(z, vz)

        p = SET % i
        uit = {'.png': frame, '_lijf.png': lijf, '_boven.png': vuist,
               '_zones.png': z, '_lijf_zones.png': lz, '_boven_zones.png': vz}
        for ach, a in uit.items():
            im = bewaar(a, os.path.join(SPEL, p + ach))
            kl = im.resize((W // 2, H // 2), Image.NEAREST if 'zones' in ach else Image.LANCZOS)
            os.makedirs(os.path.dirname(os.path.join(KLEIN, p)), exist_ok=True)
            kl.save(os.path.join(KLEIN, p + ach), optimize=True)
        for ach, a in {'.png': lijf, '_vuist.png': vuist, '_zones.png': lz, '_vuist_zones.png': vz}.items():
            bewaar(a, os.path.join(mk, p + ach))
        print(p, 'bovenarm %.0f, onderarm %.0f' % (t1[i], t2[i]))


if __name__ == '__main__':
    main()
