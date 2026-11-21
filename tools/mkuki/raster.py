"""Bouw een 3x2-raster voor Grok uit originele frames, en zet het resultaat terug.

bouw(items, uit_png, meta_json, anker=None)
  items: lijst van dicts {pad, speer: bool, draai: bool}. Met speer wordt de speer weggehaald (speer_meet).
  anker: optioneel een al aangekleed RGBA-frame (zelfde canvas) voor tegel 1 (of tegel 6 als draai).
terug(grok_png, meta_json) -> lijst RGBA-arrays op het eigen canvas (nog niet uitgelijnd).
"""
import json, sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as nd
sys.path.insert(0, os.path.dirname(__file__))
from speer_meet import meet

W, H, TW, TH = 1800, 1100, 600, 550
MAG = (255, 0, 255)


def laad(pad):
    return np.asarray(Image.open(pad).convert('RGBA')).copy()


def zonder_speer(a, info=None):
    r = meet(a, info)
    if r is None:
        return a, None
    b = a.copy()
    b[r['masker'], 3] = 0
    # losse snippers die niet aan het lijf vastzitten weg
    al = b[..., 3] > 60
    lab, n = nd.label(al)
    if n > 1:
        sz = nd.sum(al, lab, range(1, n + 1))
        groot = sz.max()
        for i, v in enumerate(sz):
            if v < 0.02 * groot:
                b[lab == i + 1, 3] = 0
    hoofd = b[..., 3] > 60
    b[~nd.binary_dilation(hoofd, iterations=2), 3] = 0
    return b, r


def op_magenta(a):
    al = a[..., 3:4].astype(float) / 255
    rgb = a[..., :3] * al + np.array(MAG) * (1 - al)
    return rgb.astype(np.uint8)


def bouw(items, uit_png, meta_json, anker=None, overrides=None, schaal=None):
    overrides = overrides or {}
    frames = []
    for it in items:
        a = laad(it['pad'])
        r = None
        if it.get('speer'):
            a, r = zonder_speer(a, overrides.get(os.path.basename(it['pad'])))
        frames.append((it, a, r))
    ch, cw = frames[0][1].shape[:2]
    alle = [f[1] for f in frames] + ([anker] if anker is not None else [])
    m = np.zeros((ch, cw), bool)
    for a in alle:
        m |= a[..., 3] > 30
    ys, xs = np.where(m)
    x0, x1, y0, y1 = max(0, xs.min() - 4), min(cw, xs.max() + 5), max(0, ys.min() - 4), min(ch, ys.max() + 5)
    bw, bh = x1 - x0, y1 - y0
    s = schaal or min((TW - 50) / bw, (TH - 50) / bh)
    tegels = []
    if anker is not None:
        tegels.append(('anker', anker))
    for it, a, r in frames:
        tegels.append((it['pad'], a))
    assert len(tegels) <= 6
    draai = any(it.get('draai') for it, _, _ in frames)
    canvas = Image.new('RGB', (W, H), MAG)
    nw, nh = int(round(bw * s)), int(round(bh * s))
    plekken = []
    volgorde = list(range(6))
    if draai:
        volgorde = volgorde[::-1]  # anker komt na het terugdraaien linksboven: in het raster rechtsonder
    for k, (naam, a) in enumerate(tegels):
        t = volgorde[k]
        tx, ty = (t % 3) * TW, (t // 3) * TH
        crop = Image.fromarray(a[y0:y1, x0:x1]).resize((nw, nh), Image.LANCZOS)
        if draai:
            crop = crop.rotate(180)
        rgb = Image.fromarray(op_magenta(np.asarray(crop)))
        px, py = tx + (TW - nw) // 2, ty + (TH - nh) // 2
        canvas.paste(rgb, (px, py))
        plekken.append({'naam': naam, 'tegel': t, 'px': px, 'py': py})
    canvas.save(uit_png)
    meta = {'canvas': [cw, ch], 'crop': [int(x0), int(y0), int(x1), int(y1)], 'schaal': s, 'nw': nw, 'nh': nh,
            'draai': draai, 'plekken': plekken,
            'speer': {os.path.basename(it['pad']): ({k: v for k, v in r.items() if k not in ('masker', 'band')} if r else None)
                      for it, a, r in frames}}
    json.dump(meta, open(meta_json, 'w'), indent=1)
    return meta


def key(rgb):
    a = rgb.astype(float)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(R, B); mn = np.minimum(R, B)
    k = np.where(mx > 0, (mn - G) / np.maximum(mx, 1), 0)
    al = np.clip((0.80 - k) / 0.30, 0, 1)  # ramp 0,50-0,80
    s = np.clip(mn - G, 0, None) * (1 - al)
    a[..., 0] -= s; a[..., 2] -= s
    return np.dstack([np.clip(a, 0, 255), al * 255]).astype(np.uint8)


def terug(grok_png, meta_json):
    meta = json.load(open(meta_json))
    g = Image.open(grok_png).convert('RGB').resize((W, H), Image.LANCZOS)
    if meta['draai']:
        g = g.rotate(180)
        # na het draaien staat tegel t op plek 5-t; reken de plekken om
    ga = key(np.asarray(g))
    cw, ch = meta['canvas']
    x0, y0, x1, y1 = meta['crop']
    uit = []
    for p in meta['plekken']:
        px, py = p['px'], p['py']
        if meta['draai']:
            px, py = W - px - meta['nw'], H - py - meta['nh']
        stuk = Image.fromarray(ga[py:py + meta['nh'], px:px + meta['nw']])
        stuk = stuk.resize((x1 - x0, y1 - y0), Image.LANCZOS)
        doek = np.zeros((ch, cw, 4), np.uint8)
        doek[y0:y1, x0:x1] = np.asarray(stuk)
        uit.append((p['naam'], doek))
    return uit
