"""Diagnose: per frame het origineel met de gemeten lijn (groen punt = tip, rood = kont), naast Mkuki met de toolspeer."""
import sys, json, math
from PIL import Image, ImageDraw
U, setid, uit = sys.argv[1], sys.argv[2], sys.argv[3]
PL = sys.argv[4] if len(sys.argv) > 4 else None
D = json.load(open(U + '/D.json')); IMG = D['items'][0]['img']['basis']
init = json.load(open(PL)) if PL else D['init']
a = [x for x in D['anims'] if x['id'] == setid][0]
W, H, c = a['W'], a['H'], a['cols']
fo = Image.open(U + '/' + a['sheet']['o']); ff = Image.open(U + '/' + a['sheet']['f'])
vv = Image.open(U + '/' + a['sheet']['v']) if a['sheet']['v'] else None
th = int(sys.argv[5]) if len(sys.argv) > 5 else 230; tegels = []
for i, fr in enumerate(a['frames']):
    x, y = (i % c) * W, (i // c) * H
    L = init[setid][i]['L']['amirspeer']
    o = Image.new('RGBA', (W, H), (215, 215, 215, 255)); o.alpha_composite(fo.crop((x, y, x + W, y + H)))
    m = Image.new('RGBA', (W, H), (215, 215, 215, 255))
    s = Image.new('RGBA', (W, H))
    if L['on']:
        e = IMG[L['angle']]; sp = Image.open(U + '/' + e['src']).convert('RGBA')
        w = L['w'] * W; h = w * e['aspect']
        im = sp.resize((max(1, round(w)), max(1, round(h)))).rotate(-L['rot'], expand=True, resample=Image.BICUBIC)
        s.alpha_composite(im, (round(L['cx'] * W - im.width / 2), round(L['cy'] * H - im.height / 2)))
        d = ImageDraw.Draw(o); r = math.radians(L['rot']); hx, hy = math.cos(r) * w / 2, math.sin(r) * w / 2
        cx, cy = L['cx'] * W, L['cy'] * H
        d.line([cx - hx, cy - hy, cx + hx, cy + hy], fill=(0, 160, 255, 255), width=2)
        d.ellipse([cx + hx - 4, cy + hy - 4, cx + hx + 4, cy + hy + 4], fill=(0, 200, 0, 255))
        d.ellipse([cx - hx - 4, cy - hy - 4, cx - hx + 4, cy - hy + 4], fill=(230, 0, 0, 255))
    if L['on'] and L['behind']: m.alpha_composite(s)
    m.alpha_composite(ff.crop((x, y, x + W, y + H)))
    if L['on'] and not L['behind']: m.alpha_composite(s)
    if vv and fr['v']: m.alpha_composite(vv.crop((x, y, x + W, y + H)))
    t = Image.new('RGB', (2 * W + 6, H + 18), 'white'); t.paste(o, (0, 18)); t.paste(m, (W + 6, 18))
    ImageDraw.Draw(t).text((3, 3), '%d %s %s' % (i + 1, L['angle'] if L['on'] else 'UIT', a['speerNoten'].get(str(i + 1), '')), fill='black')
    tegels.append(t.resize((t.width * th // t.height, th)))
B = 1500; rows = []; cur = []; bw = 0
for t in tegels:
    if bw + t.width > B and cur: rows.append(cur); cur = []; bw = 0
    cur.append(t); bw += t.width + 4
rows.append(cur)
P = Image.new('RGB', (B, th * len(rows) + 4 * len(rows)), 'white')
for j, r in enumerate(rows):
    xx = 0
    for t in r: P.paste(t, (xx, j * (th + 4))); xx += t.width + 4
P.save(uit); print(P.size)
