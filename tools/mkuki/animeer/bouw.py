"""Bouw de data en spritebladen voor de Animeer tool Mkuki.
python3 bouw.py <repo> <uitmap> <ren.html>"""
import sys, os, json, math
from PIL import Image
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from speer_plaats import vuist_snap, plaats, set_lengte, KS, LS, MAAT, UIT as SPEER_UIT, ACHTER as SPEER_ACHTER, NIET_SNAP
REPO, UIT = sys.argv[1], sys.argv[2]
AM = os.path.join(REPO, 'karakters/amir/')
MK = AM + 'mkuki/'
WORP = os.path.join(REPO, 'amir runc/amir_sprites/design/amir/')
PL = json.load(open(MK + 'plaatsing.json'))['frames']

def r(n, f): return [f % i for i in n]
SETS = [
 ('idle_sp', 'Idle met speer', 10, r(range(20), 'idle/idle_sp/idle_sp_%02d.png')),
 ('idle_sp_los', 'Idle met speer, los beeld', 10, ['idle/idle_sp.png']),
 ('idle_ns', 'Idle zonder speer', 10, ['idle/idle_ns.png']),
 ('ren_sp', 'Ren met speer', 12, r(range(1, 13), 'beweging/run/nieuw/ren_sp_%d.png')),
 ('ren_ns', 'Ren zonder speer', 12, r(range(1, 13), 'beweging/run/nieuw/ren_ns_%d.png')),
 ('jump_sp', 'Springen met speer', 12, ['beweging/jump/jumpspeer/amirjumpspear%s.png' % s for s in ['0staand','1hurk','2afzet','3stijgen','4top','5vallen','6landing']]),
 ('jump_ns', 'Springen zonder speer', 12, ['beweging/jump/jump/amirjump%s.png' % s for s in ['0staand','1hurk','2afzet','3stijgen','4top','5vallen','6landing']]),
 ('bukken_sp', 'Bukken met speer', 12, r(range(1, 9), 'beweging/bukken/bukkenspeer/bukken_in_%d_speer.png') + r(range(1, 5), 'beweging/bukken/bukkenspeer/bukken_hold_%d_speer.png')),
 ('buk_ns', 'Bukken zonder speer', 12, r(range(1, 9), 'beweging/bukken/bukken/bukken_in_%d.png') + r(range(1, 5), 'beweging/bukken/bukken/bukken_hold_%d.png')),
 ('sluipen_sp', 'Sluipen met speer', 12, r(range(22), 'beweging/sluipen/sluipen_speer_%02d.png')),
 ('sluip_ns', 'Sluipen zonder speer', 12, r(range(28), 'beweging/sluipen/sluipen_%02d.png')),
 ('rol_sp', 'Rol met speer', 12, r(range(1, 29), 'beweging/rol/met/rol_%d.png')),
 ('rol_ns', 'Rol zonder speer', 12, r(range(1, 29), 'beweging/rol/zonder/rol_%d.png')),
 ('trap_sp', 'Trap', 12, ['beweging/trap/trap_af.png', 'beweging/trap/trap_op.png']),
 ('strike_sp', 'Speerstoot', 12, r(range(1, 11), 'aanval/speerstrike/attack_sp_%d.png')),
 ('worp_sp', 'Speerworp', 12, r(range(20), 'speerworp/speerworp_%02d.png')),
 ('sweep_sp', 'Lage zwaai', 12, r(range(1, 19), 'aanval/lowsweep/sweep_%d.png')),
 ('combo_sp', 'Combo', 12, r(range(15), 'aanval/combo/combo_%02d.png')),
 ('stof_sp', 'Stofsweep', 12, r(range(14), 'aanval/stofsweep/stof_%02d.png')),
 ('rolworp_sp', 'Rol/worp', 12, r(range(1, 34), 'beweging/rol/worp/worp_%d.png')),
]
DOEL_H = 360  # beeldhoogte in de tool; bladen worden zo verkleind (fracties blijven gelijk)

def orig_pad(p):
    return (WORP + p) if p.startswith('speerworp/') else (AM + p)

os.makedirs(UIT + '/f', exist_ok=True); os.makedirs(UIT + '/o', exist_ok=True); os.makedirs(UIT + '/v', exist_ok=True)
anims, init, bron = [], {}, {}
for sid, naam, fps, paden in SETS:
    b0 = Image.open(MK + paden[0]); CW, CH = b0.size
    s = min(1.0, DOEL_H / CH); W, H = round(CW * s), round(CH * s)
    n = len(paden); cols = max(1, min(n, math.ceil(math.sqrt(n * H / W))))
    rows = math.ceil(n / cols)
    vel = {k: Image.new('RGBA', (cols * W, rows * H)) for k in 'fov'}
    heeft_v = False; grond = 0; frames = []; ini = []; noten = {}
    lengtes = [PL[p]['lengte'] for p in paden if p in PL]
    lmed = set_lengte(sid, lengtes) if lengtes else 274
    for i, p in enumerate(paden):
        x, y = (i % cols) * W, (i // cols) * H
        lijf = Image.open(MK + p).convert('RGBA'); assert lijf.size == (CW, CH), (p, lijf.size)
        org = Image.open(orig_pad(p)).convert('RGBA'); assert org.size == (CW, CH), (p, org.size)
        bb = org.getbbox(); grond = max(grond, bb[3] if bb else 0)
        vel['f'].paste(lijf.resize((W, H), Image.LANCZOS), (x, y))
        vel['o'].paste(org.resize((W, H), Image.LANCZOS), (x, y))
        vp = MK + p[:-4] + '_vuist.png'
        hv = os.path.exists(vp)
        if hv:
            heeft_v = True; vel['v'].paste(Image.open(vp).convert('RGBA').resize((W, H), Image.LANCZOS), (x, y))
        frames.append({'i': i, 'orig': os.path.basename(p)[:-4], 'ms': round(1000 / fps), 'v': hv})
        q = PL.get(p)
        if q and (i + 1) in SPEER_UIT.get(sid, ()):
            L = None; noten[str(i + 1)] = 'speer is hier al weg (na de worp): uit'
        elif q and q.get('lengte', 0) > 0:
            L0 = set_lengte(sid, [PL[x]['lengte'] for x in paden if x in PL])
            schaal = max(CW, CH) / 594 if max(CW, CH) > 700 else 1.0
            L, noot = plaats(sid, q, np.asarray(org)[..., 3], L0, CW, CH, schaal, MAAT.get(sid))
            L, sn = (L, '') if sid in NIET_SNAP else vuist_snap(L, q, np.asarray(lijf)[..., 3], CW, CH, L0 / 273)
            if sn: noot = (noot + ', ' if noot else '') + sn
            if L and (i + 1) in SPEER_ACHTER.get(sid, ()):
                L['behind'] = True; noot = (noot + ', ' if noot else '') + 'achter het hoofd langs'
            if noot: noten[str(i + 1)] = noot
        else:
            L = None
        if L is None:
            L = {'on': False, 'angle': 'proj', 'cx': 0.5, 'cy': 0.45, 'w': round(lmed / CW, 4), 'rot': -90,
                 'flip': False, 'behind': False, 'op': 1, 'locked': False}
        ini.append({'L': {'amirspeer': L}, 'body': {'basis': []}, 'im': {}})
        bron[sid + '-' + str(i)] = p
    for k in 'fo':
        vel[k].save('%s/%s/%s.png' % (UIT, k, sid), optimize=True)
    if heeft_v: vel['v'].save('%s/v/%s.png' % (UIT, sid), optimize=True)
    anims.append({'id': sid, 'name': naam, 'fps': fps, 'W': W, 'H': H, 'canvasW': CW, 'canvasH': CH,
                  'grond': grond, 'anchorX': CW // 2, 'cols': cols, 'vuist': heeft_v,
                  'sheet': {'f': 'f/%s.png' % sid, 'o': 'o/%s.png' % sid, 'v': ('v/%s.png' % sid) if heeft_v else None},
                  'frames': frames, 'speerNoten': noten, 'speerL': round(lmed), 'speerMaat': MAAT.get(sid, round(lmed))})
    init[sid] = ini
    print(sid, n, 'L', round(lmed), 'noten', len(noten), (CW, CH), '->', (W, H), 'cols', cols, 'speer', sum(1 for f in ini if f['L']['amirspeer']['on']), 'vuist', sum(f['v'] for f in frames))
D = {'personage': 'Amir mkuki', 'versions': [{'id': 'basis', 'name': 'Basis'}], 'anims': anims,
     'items': [{'id': 'amirspeer', 'name': 'Speer Amir', 'versioned': False, 'angles': [{'id': 'proj', 'name': 'werpspeer'}] + [{'id': 'k%02d' % round(k * 100), 'name': 'verkort %d%%' % round(k * 100)} for k in KS] + [{'id': 'l%03d' % round(f * 100), 'name': 'lange schacht %d%%' % round(f * 100)} for f in LS],
                'img': {'basis': dict([('proj', {'src': 'i/amirspeer_proj.png', 'aspect': 0.1074})] + [('k%02d' % round(k * 100), {'src': 'i/amirspeer_k%02d.png' % round(k * 100), 'aspect': round(0.1074 / k, 4)}) for k in KS] + [('l%03d' % round(f * 100), {'src': 'i/amirspeer_l%03d.png' % round(f * 100), 'aspect': round(0.1074 / f, 4)}) for f in LS])}}],
     'init': init, 'angleMasks': {}, 'zones': [], 'zoneSuggest': {}, 'kop': {}, 'bron': bron}
os.makedirs(UIT + '/i', exist_ok=True)
SP = Image.open(sys.argv[3]).convert('RGBA'); SP.save(UIT + '/i/amirspeer_proj.png')
for k in KS:
    SP.resize((round(SP.width * k), SP.height), Image.LANCZOS).save(UIT + '/i/amirspeer_k%02d.png' % round(k * 100))
for f in LS:
    # schacht tussen x 40 en 420 (van 624) uitrekken; kont, lint en punt blijven gelijk
    a0, a1 = 40, 420; extra = round(SP.width * (f - 1))
    n = Image.new('RGBA', (SP.width + extra, SP.height))
    n.paste(SP.crop((0, 0, a0, SP.height)), (0, 0))
    n.paste(SP.crop((a0, 0, a1, SP.height)).resize((a1 - a0 + extra, SP.height), Image.LANCZOS), (a0, 0))
    n.paste(SP.crop((a1, 0, SP.width, SP.height)), (a1 + extra, 0))
    n.save(UIT + '/i/amirspeer_l%03d.png' % round(f * 100))
json.dump(D, open(UIT + '/D.json', 'w'), separators=(',', ':'))
