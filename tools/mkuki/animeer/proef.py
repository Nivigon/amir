"""Bootst de tool na (lijf, speer, vuist) voor een paar frames per animatie; plaat ter controle."""
import sys, json, math
from PIL import Image, ImageDraw
U = sys.argv[1]; D = json.load(open(U + '/D.json')); sp = Image.open(sys.argv[2]).convert('RGBA')
tegels = []
for a in D['anims']:
    W, H, c = a['W'], a['H'], a['cols']
    vel = {k: Image.open(U + '/' + a['sheet'][k]) for k in 'fo'}
    vv = Image.open(U + '/' + a['sheet']['v']) if a['sheet']['v'] else None
    n = len(a['frames']); kies = sorted(set([0, n // 3, (2 * n) // 3, n - 1]))
    for i in kies:
        x, y = (i % c) * W, (i // c) * H
        L = D['init'][a['id']][i]['L']['amirspeer']
        doek = Image.new('RGBA', (W, H), (200, 200, 200, 255))
        lijf = vel['f'].crop((x, y, x + W, y + H))
        s = Image.new('RGBA', (W, H))
        if L['on']:
            w = L['w'] * W; h = w * 0.1074
            im = sp.resize((max(1, round(w)), max(1, round(h))))
            im = im.rotate(-L['rot'], expand=True, resample=Image.BICUBIC)
            s.alpha_composite(im, (round(L['cx'] * W - im.width / 2), round(L['cy'] * H - im.height / 2)))
        if L['on'] and L['behind']: doek.alpha_composite(s)
        doek.alpha_composite(lijf)
        if L['on'] and not L['behind']: doek.alpha_composite(s)
        if vv: doek.alpha_composite(vv.crop((x, y, x + W, y + H)))
        o = vel['o'].crop((x, y, x + W, y + H)); og = Image.new('RGBA', (W, H), (200, 200, 200, 255)); og.alpha_composite(o)
        t = Image.new('RGB', (W * 2, H + 16), 'white'); t.paste(og, (0, 16)); t.paste(doek, (W, 16))
        ImageDraw.Draw(t).text((4, 2), '%s %d' % (a['id'], i + 1), fill='black')
        tegels.append(t.resize((t.width * 200 // t.height, 200)))
rijbreed = 1800; rijen = []; cur = []; bw = 0
for t in tegels:
    if bw + t.width > rijbreed and cur: rijen.append(cur); cur = []; bw = 0
    cur.append(t); bw += t.width
rijen.append(cur)
P = Image.new('RGB', (rijbreed, 200 * len(rijen)), 'white')
for j, rij in enumerate(rijen):
    x = 0
    for t in rij: P.paste(t, (x, j * 200)); x += t.width
P.save(sys.argv[3]); print(P.size)
