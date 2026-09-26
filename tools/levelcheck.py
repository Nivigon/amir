#!/usr/bin/env python3
"""Kijkt alle leveldefinities in amir-king-of-africa.html na op ontwerpfouten.

Het script leest de levels rechtstreeks uit de HTML, samen met de getallen waar het
spel zelf mee rekent (CHAR_H, JUMP_V, GRAVITY, de loopsnelheid, PLAFOND_WEG, de maten
van de keien en de klif, enzovoort). Staat een getal niet meer waar het script het
zoekt, dan stopt het met een melding in plaats van met een oud getal verder te rekenen.

Het verandert niets: het meldt per level wat er niet klopt.

    python3 tools/levelcheck.py                  alle levels
    python3 tools/levelcheck.py "Renew 6"        alleen levels waarvan de naam dit bevat
    python3 tools/levelcheck.py -v               ook de info-regels (sprint nodig, en zo)
    python3 tools/levelcheck.py --hoog 393       op een ander scherm (standaard 720 hoog)
    python3 tools/levelcheck.py level.json       een level dat nog niet in de HTML staat (de bouwer
                                                 exporteert hetzelfde formaat)

Drie soorten meldingen:

    FOUT     het level is hierdoor stuk, of het schendt een regel uit CLAUDE.md
    LET OP   het werkt, maar krap, of het spel lost het stilletjes voor je op
    info     alleen met -v: goed om te weten, geen fout

De afsluitcode is 1 als er ergens een FOUT staat, anders 0.

Een nieuwe regel erbij: schrijf een functie met @regel('naam') erboven die per
melding een Melding teruggeeft (zie de bestaande regels onderaan). Meldt iemand iets
dat in een level niet samen kan, dan hoort dat hier als regel bij, zodat het de
volgende keer vanzelf opvalt.

Wat het script niet kan zien, en waarom:

- Maten die aan het scherm hangen (de breedte van een kei, een boom, de klif) rekent
  het uit voor één scherm, standaard 1280 bij 720 op Formaat 25. Op een ander scherm
  kan decor dat hier net vrij staat alsnog over een rand hangen; draai het dan met
  --hoog en --formaat.
- Of een trede te beklimmen is, bekijkt het per rand, met de richels en keien die
  daar staan. Het rekent niet na of de sprong van richel naar richel ook in de
  breedte lukt.
- Grotten (het raster) en de muur met de rune worden alleen op hun plek gecontroleerd,
  niet op hun binnenkant: voor de rune staat in CLAUDE.md hoe je dat nakijkt.
- Vijanden die je de weg versperren of levens kosten: het rekent alleen de vallen. Wat een
  level echt doet, zie je met de speelrobot (tools/speelrobot.js), die het in het spel afloopt.
"""
import json
import math
import os
import re
import struct
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
HTML = os.path.join(ROOT, 'amir-king-of-africa.html')


# ---- een klein stukje JavaScript lezen ---------------------------------------
# De levels zijn gewone objectliteralen, met commentaar, sleutels zonder aanhalingstekens
# en af en toe een som of een constante. Dat lezen we hier zelf, zonder Node erbij.

class Onbekend:
    """Een waarde die we niet kunnen uitrekenen (een functieaanroep, een pijlfunctie)."""
    def __repr__(self):
        return '?'


ONBEKEND = Onbekend()

_TOKEN = re.compile(r"""
    (?P<ws>\s+|//[^\n]*|/\*.*?\*/)
  | (?P<num>\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+)
  | (?P<str>'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|`(?:\\.|[^`\\])*`)
  | (?P<id>[A-Za-z_$][\w$]*)
  | (?P<op>=>|\.\.\.|[{}\[\](),:?+\-*/.<>=!&|%])
""", re.S | re.X)


def tokens(src, los=False):
    pos, out = 0, []
    while pos < len(src):
        m = _TOKEN.match(src, pos)
        if not m and los:                 # los: een teken dat we niet kennen (een regex) overslaan
            pos += 1
            continue
        if not m:
            raise ValueError('onleesbaar teken bij: ' + src[pos:pos + 30])
        pos = m.end()
        soort = m.lastgroup
        if soort == 'ws':
            continue
        out.append((soort, m.group()))
    return out


class Lezer:
    def __init__(self, toks, namen):
        self.t, self.i, self.namen = toks, 0, namen

    def kijk(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else ('eind', '')

    def neem(self, waarde=None):
        tok = self.kijk()
        if waarde is not None and tok[1] != waarde:
            raise ValueError('verwacht %r, kreeg %r' % (waarde, tok[1]))
        self.i += 1
        return tok

    def sla_over(self):
        """Een haakjesgroep overslaan die we niet uitrekenen."""
        diepte = 0
        while True:
            s, v = self.neem()
            if v in '([{':
                diepte += 1
            elif v in ')]}':
                diepte -= 1
                if diepte == 0:
                    return
            if s == 'eind':
                return

    def waarde(self):
        links = self.term()
        while self.kijk()[1] in ('+', '-', '*', '/'):
            op = self.neem()[1]
            rechts = self.term()
            if isinstance(links, (int, float)) and isinstance(rechts, (int, float)):
                links = {'+': links + rechts, '-': links - rechts,
                         '*': links * rechts, '/': links / rechts if rechts else ONBEKEND}[op]
            else:
                links = ONBEKEND
        if self.kijk()[1] == '?':                    # a ? b : c, niet uitrekenen
            self.neem('?'); self.waarde(); self.neem(':'); self.waarde()
            return ONBEKEND
        return links

    def term(self):
        s, v = self.kijk()
        if v == '-':
            self.neem()
            x = self.term()
            return -x if isinstance(x, (int, float)) else ONBEKEND
        if v == '+':
            self.neem()
            return self.term()
        if v == '(':
            begin = self.i
            self.neem('(')
            try:
                x = self.waarde()
                self.neem(')')
                if self.kijk()[1] == '=>':
                    raise ValueError
                return x
            except ValueError:
                self.i = begin
                self.sla_over()
                if self.kijk()[1] == '=>':
                    self.neem()
                    self.term()
                return ONBEKEND
        if v == '{':
            return self.object()
        if v == '[':
            return self.lijst()
        if s == 'num':
            self.neem()
            return float(v) if ('.' in v or 'e' in v.lower()) else int(v)
        if s == 'str':
            self.neem()
            return re.sub(r'\\(.)', r'\1', v[1:-1])
        if s == 'id':
            self.neem()
            x = {'true': True, 'false': False, 'null': None,
                 'undefined': None}.get(v, self.namen.get(v, ONBEKEND))
            while self.kijk()[1] in ('.', '(', '['):   # Math.max(...), iets.src, a[0]
                if self.kijk()[1] == '.':
                    self.neem(); self.neem()
                else:
                    self.sla_over()
                x = ONBEKEND
            if self.kijk()[1] == '=>':                 # x => ...
                self.neem(); self.term()
                return ONBEKEND
            return x
        raise ValueError('onverwacht: %r' % v)

    def object(self):
        self.neem('{')
        uit = {}
        while self.kijk()[1] != '}':
            s, k = self.neem()
            if s == 'str':
                k = k[1:-1]
            if self.kijk()[1] == ':':
                self.neem(':')
                uit[k] = self.waarde()
            else:                                      # verkort: { x } of een methode
                uit[k] = self.namen.get(k, ONBEKEND)
                if self.kijk()[1] == '(':
                    self.sla_over(); self.sla_over()
            if self.kijk()[1] == ',':
                self.neem(',')
        self.neem('}')
        return uit

    def lijst(self):
        self.neem('[')
        uit = []
        while self.kijk()[1] != ']':
            uit.append(self.waarde())
            if self.kijk()[1] == ',':
                self.neem(',')
        self.neem(']')
        return uit


def blok_na(src, begin):
    """De tekst van de eerste { of [ vanaf begin tot en met de sluitende haak."""
    i = min(j for j in (src.find('{', begin), src.find('[', begin)) if j >= 0)
    open_, dicht = src[i], '}' if src[i] == '{' else ']'
    diepte, j, in_str = 0, i, None
    while j < len(src):
        c = src[j]
        if in_str:
            if c == '\\':
                j += 1
            elif c == in_str:
                in_str = None
        elif src.startswith('//', j):
            j = src.index('\n', j)
            continue
        elif c in '\'"`':
            in_str = c
        elif c == open_:
            diepte += 1
        elif c == dicht:
            diepte -= 1
            if diepte == 0:
                return src[i:j + 1]
        j += 1
    raise ValueError('geen sluitende haak na positie %d' % begin)


class Bron:
    """De HTML, en alles wat we eruit lezen."""
    def __init__(self, pad):
        with open(pad, encoding='utf-8') as f:
            self.src = f.read()
        self.namen = {}

    def const(self, naam):
        """Een const uitrekenen; ontbreekt hij, dan stoppen we."""
        m = re.search(r'\bconst\s+' + naam + r'\s*=\s*', self.src)
        if not m:
            stop('const %s staat niet meer in de HTML' % naam)
        rest = self.src[m.end():]
        if rest[0] in '{[':
            tekst = blok_na(self.src, m.end())
        else:
            tekst = re.match(r'[^;\n]*', rest).group()
            tekst = re.sub(r',\s*[A-Za-z_]\w*\s*=.*', '', tekst)   # const A = 1, B = 2
        w = Lezer(tokens(tekst), self.namen).waarde()
        self.namen[naam] = w
        return w

    def getal(self, naam):
        w = self.const(naam)
        if not isinstance(w, (int, float)):
            stop('const %s is geen getal meer' % naam)
        return w

    def regex(self, patroon, wat):
        m = re.search(patroon, self.src)
        if not m:
            stop('kan %s niet meer vinden in de HTML (zoek: %s)' % (wat, patroon))
        return m

    def reeks_const(self, naam):
        """const A = 1, B = 2 op één regel: A en B allebei."""
        m = self.regex(r'const\s+([^;]*\b' + naam + r'\s*=[^;]*);', naam)
        for deel in m.group(1).split(','):
            if '=' in deel:
                k, v = deel.split('=', 1)
                try:
                    self.namen[k.strip()] = Lezer(tokens(v), self.namen).waarde()
                except ValueError:
                    pass
        return self.namen[naam]


def sleutels_bovenaan(blok):
    """De sleutels op het buitenste niveau van een objectliteraal."""
    toks = tokens(blok, los=True)
    uit, diepte = [], 0
    for i, (soort, v) in enumerate(toks):
        if v in '([{':
            diepte += 1
        elif v in ')]}':
            diepte -= 1
        elif diepte == 1 and soort == 'id' and i + 1 < len(toks) and toks[i + 1][1] == ':' \
                and toks[i - 1][1] in ('{', ','):
            uit.append(v)
    return uit


def stop(tekst):
    sys.stderr.write('levelcheck: ' + tekst + '\n')
    sys.exit(2)


def png_maat(pad):
    try:
        with open(os.path.join(ROOT, pad), 'rb') as f:
            kop = f.read(24)
        if kop[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', kop[16:24])
    except OSError:
        pass
    return None


# ---- de getallen van het spel -------------------------------------------------

class Spel:
    def __init__(self, bron, hoog, formaat, breed=None):
        b = bron
        self.CHAR_H = b.reeks_const('CHAR_H')
        self.JUMP_V = b.reeks_const('JUMP_V')
        self.GRAVITY = b.namen['GRAVITY']
        self.COYOTE_T = b.getal('COYOTE_T')
        self.GAP_BASE = b.getal('GAP_BASE')
        self.GAP_DEATH = b.getal('GAP_DEATH')
        self.PLAFOND_WEG = b.getal('PLAFOND_WEG')
        self.HOLTE_DAK = b.getal('HOLTE_DAK')
        self.FAR_GAP_LIFT = b.getal('FAR_GAP_LIFT')
        self.PLAYER_HALF_W = b.getal('PLAYER_HALF_W')
        self.THICKET_BOX = b.getal('THICKET_BOX')
        self.THICKET_OVERLAP = b.getal('THICKET_OVERLAP')
        self.THICKET_BACK_S = b.getal('THICKET_BACK_S')
        self.VILLAGE_FAR = b.getal('VILLAGE_FAR')
        self.VAL_VRIJ = b.getal('VAL_VRIJ')
        self.VAL_ZWAAR = b.getal('VAL_ZWAAR')
        self.VAL_MAX = b.getal('VAL_MAX')
        self.HPPOTION_HEAL = b.getal('HPPOTION_HEAL')
        self.LEVENS = b.getal('HPPOTION_HP_MAX')
        self.SPEAR_AHEAD = b.getal('SPEAR_AHEAD')
        self.PLAT = b.const('PLAT')
        self.CLIFF = b.const('CLIFF')
        self.FIN = b.const('FIN')
        self.POOL = b.const('POOL')
        self.EDGE = b.const('EDGE')
        self.PROPS = b.const('PROPS')
        self.VILLAGE = b.const('VILLAGE')
        self.SCENES = b.const('SCENES')
        self.MUZIEK = b.const('MUZIEK')
        self.ZW_KLEUREN = b.const('ZW_KLEUREN')
        # NPCS en THICKET bevatten functieaanroepen; alleen de maten zijn nodig
        self.NPCS = {}
        for m in re.finditer(r'\n\s*(\w+):\s*\{\s*w:\s*(\d+),\s*h:\s*(\d+),\s*ground:\s*\d+,'
                             r'\s*fig:\s*(\d+),\s*tall:\s*([\d.]+)', blok_na(b.src, b.src.index('const NPCS'))):
            self.NPCS[m.group(1)] = dict(w=int(m.group(2)), h=int(m.group(3)),
                                         fig=int(m.group(4)), tall=float(m.group(5)))
        self.THICKET = {}
        for m in re.finditer(r"\n\s*(\w):\s*\{[^}]*?h:\s*([\d.]+),\s*w:\s*(\d+),\s*ih:\s*(\d+)",
                             blok_na(b.src, b.src.index('const THICKET ='))):
            self.THICKET[m.group(1)] = dict(h=float(m.group(2)), w=int(m.group(3)), ih=int(m.group(4)))
        if not self.NPCS or not self.THICKET:
            stop('NPCS of THICKET heeft een andere vorm gekregen')
        # de loopsnelheid en de sprint staan niet in een const, maar in de spellus
        m = b.regex(r'world \+= dir \* (\d+) \* walkK\(\)', 'de loopsnelheid')
        self.LOOP = int(m.group(1))
        m = b.regex(r"const sprint = keys\['Shift'\] \? ([\d.]+) : 1", 'de sprintfactor')
        self.SPRINT = float(m.group(1))
        # de fakkels: zo dicht moet je erbij staan
        m = b.regex(r'Math\.abs\(world - f\.x\) < (\d+)', 'het bereik van de fakkels')
        self.EIND_BEREIK = int(m.group(1))
        # welke velden readLevel overneemt: de rest van een level wordt genegeerd
        rl = b.src[b.src.index('function readLevel'):]
        rl = blok_na(rl, rl.index('schoonLevel('))
        self.VELDEN = set(sleutels_bovenaan(rl))
        if 'rocks' not in self.VELDEN or 'ends' not in self.VELDEN:
            stop('readLevel heeft een andere vorm gekregen')

        # het scherm waarvoor we de schermafhankelijke maten uitrekenen
        self.H = hoog
        self.W = breed or hoog * 16 / 9                                   # 1280 bij 720
        self.formaat = formaat
        self.scale = hoog * (formaat / 100) / self.CHAR_H
        self.halfW = self.PLAYER_HALF_W * self.CHAR_H * self.scale      # Amir, in wereld-px
        # De sprong zoals het spel hem rekent: per beeld eerst de zwaartekracht, dan de hoogte.
        # Dat komt lager uit dan JUMP_V^2 / 2G (208): op 60 beelden per seconde 200, en op een
        # traag toestel (het spel neemt hoogstens DT_MAX per beeld) nog lager. Gemeten met de
        # speelrobot: een trede van 199 haalt hij, een van 203 niet.
        m = b.regex(r'Math\.min\(\(now - last\) / 1000, ([\d.]+)\)', 'de langste tijdstap per beeld')
        self.DT_MAX = float(m.group(1))
        self.SPRONG_THEORIE = self.JUMP_V ** 2 / (2 * self.GRAVITY)       # 208, het plafond van de formule
        self.SPRONG_H = self.sprong_top(1 / 60)                           # 200, op 60 beelden per seconde
        self.SPRONG_TRAAG = self.sprong_top(self.DT_MAX)                   # 184, op het traagste toestel

        # plaatjesmaten
        self.img = {}
        for k, d in self.PROPS.items():
            self.img['prop:' + k] = png_maat(d['src'])
        for k, d in self.VILLAGE.items():
            self.img['dorp:' + k] = png_maat(d['src'])
        self.img['plat'] = png_maat(self.PLAT['src']) or (681, 482)
        self.img['cliff'] = png_maat(self.CLIFF['src']) or (1652, 969)
        self.img['fin'] = png_maat(self.FIN['src']) or (1482, 822)

    # -- maten in wereld-px, zoals het spel ze op dit scherm uitrekent --
    def kei(self, r, terrein):
        hPx = self.CHAR_H * self.scale * self.PLAT['h'] * r['s']
        iw, ih = self.img['plat']
        wPx = iw / ih * hPx
        top = terrein(r['x']) + self.CHAR_H * self.PLAT['h'] * r['s'] * (1 - self.PLAT['top'] - self.PLAT['sink'])
        return (r['x'] - wPx / 2 + self.PLAT['l'] * wPx, r['x'] - wPx / 2 + self.PLAT['r'] * wPx, top)

    def prop_halfw(self, o):
        d = self.PROPS.get(o.get('k'))
        if not d:
            return 0
        hh = self.CHAR_H * self.scale * d['h'] * (o.get('s') or 1) * (0.60 if o.get('v') else 1)
        m = self.img.get('prop:' + o['k'])
        return (m[0] / m[1] if m else 1) * hh / 2

    def dorp_halfw(self, o):
        d = self.VILLAGE.get(o.get('id'))
        if not d:
            return 0
        depth = max(0, min(1, o.get('depth') or 0))
        h = self.CHAR_H * self.scale * d['h'] * (1 - self.VILLAGE_FAR * depth)
        m = self.img.get('dorp:' + o['id'])
        return (m[0] * h / m[1] if m else h * d.get('ar', 1)) / 2

    def npc_halfw(self, o):
        d = self.NPCS.get(o.get('k'))
        if not d:
            return 0
        h = self.CHAR_H * self.scale * d['tall'] * (o.get('s') or 1) * d['h'] / d['fig']
        return d['w'] * h / d['h'] * 0.3              # schoonLevel neemt 30 procent van de breedte

    def doornbos_hoog(self, t):
        """De hoogste klomp van een doornbos, in sprite-eenheden."""
        self.doornbos_halfw(t)
        return self._doornbos_hoog

    def doornbos_halfw(self, t):
        """makeThicket nagedaan: dezelfde hash, dezelfde klompen."""
        n = max(1, min(5, round(t.get('n') or 1)))
        sd = round(t['x']) if t.get('seed') is None else t['seed']
        teller = [0]

        def r():
            teller[0] += 1
            v = math.sin((sd * 1.37 + 11.3) * 127.1 + teller[0] * 311.7) * 43758.5453
            return v - math.floor(v)
        klompen = []
        for _ in range(n):
            v = 'a' if r() < 0.5 else 'b'
            back = n > 1 and r() < 0.5
            s0 = 0.85 + r() * 0.15
            hS = self.THICKET[v]['h'] * self.CHAR_H * s0 * (self.THICKET_BACK_S if back else 1)
            r()                                            # flip
            klompen.append(dict(wS=hS * self.THICKET[v]['w'] / self.THICKET[v]['ih'], dx=0, hS=hS))
        at = 0
        for i in range(n):
            if i > 0:
                at += (klompen[i - 1]['wS'] + klompen[i]['wS']) / 2 * (1 - self.THICKET_OVERLAP) * (0.85 + r() * 0.3)
            klompen[i]['dx'] = at
        self._doornbos_hoog = max(c['hS'] for c in klompen)
        lo = min(c['dx'] - c['wS'] / 2 for c in klompen)
        hi = max(c['dx'] + c['wS'] / 2 for c in klompen)
        return (hi - lo) / 2 * self.scale

    def klif_rechts(self):
        """Hoe ver het klifplaatje voorbij zijn muurlijn naar rechts steekt."""
        hPx = (self.H * 0.82 + 2) / (1 - self.CLIFF['sink'])
        iw, ih = self.img['cliff']
        return self.CLIFF['l'] * iw / ih * hPx

    def fakkels_halfw(self):
        iw, ih = self.img['fin']
        return self.CHAR_H * self.scale * self.FIN['h'] * iw / ih / 2

    def poel_nat(self, o):
        """Het natte stuk van een poel, in wereld-px (poolScale met het scherm van nu)."""
        s = (self.H * 0.18) / (self.EDGE['solid'] - self.EDGE['walk'])
        tw = self.POOL['W'] + (o.get('n') or 0) * self.POOL['MW']
        links = o['x'] - tw * s / 2
        return (links + self.POOL['wetL'] * s, links + (self.POOL['wetR'] + (o.get('n') or 0) * self.POOL['MW']) * s)

    # -- de sprong --
    def sprong_top(self, dt):
        """Hoe hoog de sprong komt als het spel per beeld dt verder rekent (updateJump)."""
        v, h, top = self.JUMP_V, 0.0, 0.0
        while v > 0:
            v -= self.GRAVITY * dt
            h += v * dt
            top = max(top, h)
        return top

    def boven_tijd(self, stap, dt=1 / 60):
        """Hoe lang zijn voeten boven een trede van deze hoogte zijn, per beeld geteld."""
        v, h, n = self.JUMP_V, 0.0, 0
        while v > 0 or h > 0:
            v -= self.GRAVITY * dt
            h += v * dt
            if h >= stap:
                n += 1
        return n * dt

    def sprong(self, snelheid, plafond_kop, x0, richting=-1, kracht=1.0):
        """Een sprong vanaf x0 naar links, met het plafond erbij. Geeft twee afstanden:
        tot hij weer op zijn eigen hoogte is, en tot hij zo diep zakt dat het spel hem
        opgeeft (GAP_DEATH). In het spel mag je tot die tweede afstand nog boven komen:
        wie onder de rand zakt en toch voorbij het gat komt, wordt op de grond gezet."""
        dt = 1 / 60                                  # zoals het spel: per beeld
        x, ph, pvh = x0, 0.0, self.JUMP_V * kracht
        schoon = None
        while True:
            pvh -= self.GRAVITY * dt
            ph += pvh * dt
            x += richting * snelheid * dt
            kop = plafond_kop(x)
            if ph > kop:
                ph = kop
                pvh = min(pvh, 0)
            if schoon is None and pvh <= 0 and ph <= 0:
                schoon = abs(x - x0)
            if ph < -self.GAP_DEATH:
                return schoon, abs(x - x0)


# ---- een level als wereld ----------------------------------------------------

class Level:
    def __init__(self, naam, d, spel):
        self.naam, self.d, self.spel = naam, d, spel
        g = lambda k: d.get(k) or []
        self.gaps = [q for q in g('gaps') if isinstance(q, dict)]
        for q in self.gaps:
            q['w'] = max(40, q.get('w') or spel.GAP_BASE)
        self.terraces = g('terraces')
        self.ledges = g('ledges')
        self.rocks = g('rocks')
        self.plaf = sorted((p for p in g('plafond') if isinstance(p, dict)), key=lambda p: p['x'])
        self.ends = g('ends')
        self.cliffs = g('cliffs')
        self.muur = d.get('muur')
        # readLevel zet een gang minstens HOLTE_DAK + CHAR_H diep (anders past Amir er niet in)
        # en zonder diep op 600: rekenen met wat het spel ervan maakt, niet met wat er staat
        self.holtes = []
        for o in g('holtes'):
            if isinstance(o, dict):
                q = dict(o)
                q['diep'] = max(spel.HOLTE_DAK + spel.CHAR_H, o.get('diep') or 600)
                self.holtes.append(q)
        self.keien = None
        self._route, self.pad = None, []

    def holte(self, x):
        """De gang onder de grond op deze plek (holteAt)."""
        for o in self.holtes:
            if o['l'] <= x <= o['r']:
                return o
        return None

    def terrein(self, x, zonder=None):
        """terrainH: boven een gang staat alles op de bodem ervan."""
        o = self.holte(x)
        h = -o['diep'] if o else 0
        for t in self.terraces:
            if t is not zonder and t['l'] <= x <= t['r'] and t['h'] > h:
                h = t['h']
        return h

    def plafond(self, x):
        p = self.plaf
        if len(p) < 2:
            return math.inf
        if x <= p[0]['x']:
            return p[0]['y']
        if x >= p[-1]['x']:
            return p[-1]['y']
        i = 1
        while i < len(p) - 1 and p[i]['x'] < x:
            i += 1
        a, b = p[i - 1], p[i]
        return a['y'] + (b['y'] - a['y']) * (x - a['x']) / ((b['x'] - a['x']) or 1)

    def plafond_min(self, x0, x1):
        if len(self.plaf) < 2:
            return math.inf
        m = min(self.plafond(x0), self.plafond(x1))
        for q in self.plaf:
            if x0 < q['x'] < x1 and q['y'] < m:
                m = q['y']
        return m

    def kop(self, x):
        """Hoe hoog zijn voeten mogen komen voor hij zijn hoofd stoot (plafondKop)."""
        m = self.plafond_min(x - self.spel.halfW, x + self.spel.halfW)
        return m - self.spel.CHAR_H

    def dak_kop(self, x):
        """holteKop: in een gang, buiten een gat, stoot hij zijn hoofd tegen het dak."""
        if self.holte(x) and not self.in_gat(x, x):
            return -self.spel.HOLTE_DAK - self.spel.CHAR_H
        return math.inf

    def in_gat(self, x0, x1):
        for g in self.gaps:
            if x1 > g['x'] - g['w'] / 2 and x0 < g['x'] + g['w'] / 2:
                return g
        return None

    def steun(self, x, y, tot=None):
        """De hoogste vloer onder iemand op hoogte y, zoals grondVloer en supportHeight dat
        samen uitrekenen: de grond, de bodem van een gang, een terras, een trede of een kei.
        -inf als er niets is (een gewoon ravijn). Met tot: alles tot die hoogte, voor de vraag
        wat er naast hem omhoog steekt."""
        sp = self.spel
        tot = y + 1 if tot is None else tot
        if self.keien is None:
            self.keien = [sp.kei(r, self.terrein) for r in self.rocks]
        o, gat = self.holte(x), self.in_gat(x, x)
        if o:
            best = -o['diep'] if (gat or y < -1) else 0
        else:
            best = -math.inf if gat else 0
        if best > tot:
            best = -math.inf                         # de grond naast een gang is voor wie beneden staat een wand
        op_dak = o and y >= -1 and not gat          # op de savanne boven een gang: de treden eronder dragen niet
        for t in self.terraces:
            if t['l'] <= x <= t['r'] and best < t['h'] <= tot and not (op_dak and t['h'] < -1):
                best = t['h']
        for l, r, top in self.keien:
            if l <= x <= r and best < top <= tot:
                best = top
        return best

    def steun_lijf(self, x, y, tot=None):
        """steun over de breedte van Amir."""
        hw = self.spel.halfW
        return max(self.steun(x + d * hw, y, tot) for d in (-1, -0.5, 0, 0.5, 1))

    def val(self, x0, y0, snelheid):
        """Van een rand af lopen en vallen, per beeld zoals updateJump: waar hij neerkomt.
        Geeft (x, hoogte), met hoogte None als hij in een ravijn verdwijnt."""
        sp = self.spel
        dt, x, y, vy = 1 / 60, x0, y0, 0.0
        for _ in range(60 * 8):
            vy -= sp.GRAVITY * dt
            yn = y + vy * dt
            x -= snelheid * dt
            s = self.steun_lijf(x, y)
            if yn <= s:
                return x, s
            y = yn
            if y < -sp.GAP_DEATH and not self.holte(x):
                return x, None
        return x, None

    def kop_hier(self, x, y):
        """Hoe hoog zijn voeten hier mogen komen: het plafond, en voor wie onder de grondlijn
        staat het dak van de gang (holteKop)."""
        return min(self.kop(x), self.dak_kop(x) if y < -1 else math.inf)

    def sprong_van(self, x0, y0, snelheid):
        """Een sprong vanaf x0 op hoogte y0 naar links, per beeld zoals updateJump, met het
        plafond en het dak erbij. Tegen een wand blijft hij hangen (blockByPlatforms) en zakt
        hij langs de wand. Geeft (x, hoogte) waar hij neerkomt, hoogte None in een ravijn."""
        sp = self.spel
        dt, x, y, vy = 1 / 60, x0, y0, sp.JUMP_V
        for _ in range(60 * 8):
            vy -= sp.GRAVITY * dt
            yn = min(y + vy * dt, self.kop_hier(x, y))
            if yn < y + vy * dt:
                vy = min(vy, 0)
            nx = x - snelheid * dt
            if self.steun_lijf(nx, yn, math.inf) <= yn + 2:
                x = nx                                   # anders staat er een wand: hij blijft waar hij is
            s = self.steun_lijf(x, y)
            if vy <= 0 and yn <= s:
                return x, s
            y = yn
            if y < -sp.GAP_DEATH and not self.holte(x):
                return x, None
        return x, None

    def route(self):
        """De weg die Amir aflegt als hij gewoon naar links loopt: over een gewoon ravijn
        springt hij, van een rand valt hij (op looptempo), tegen een wand klimt hij op. Geeft
        de vallen als (x, van, naar); naar is None als hij in een ravijn verdwijnt. Onderweg
        houdt hij in self.pad bij op welke hoogte Amir waar loopt (zie hoogte_op)."""
        if self._route is not None:
            return self._route
        sp = self.spel
        eind = self.einde()
        eind = eind if eind is not None else -30000
        x, y, vallen = 0.0, 0.0, []
        self.pad = []
        self._route = vallen
        while x > eind:
            self.pad.append((x, y))
            nx = x - 10
            g = self.in_gat(nx, nx)
            if g and y >= -1 and not self.holte(g['x']):
                x = g['x'] - g['w'] / 2 - 1                  # een gewoon ravijn: eroverheen
                continue
            bereik = min(y + sp.SPRONG_H, self.kop_hier(x, y))  # het dak of het plafond kapt de sprong af
            if self.steun_lijf(nx, y, math.inf) > bereik:
                break                                        # een wand die hij niet op komt: dat meldt een andere regel
            hoger = self.steun_lijf(nx, y, bereik)
            if hoger > y + 1:                                # een wand of een kei: erop
                x, y = nx, hoger
                continue
            s = self.steun_lijf(nx, y)
            if s >= y - 1:
                x, y = nx, s
                continue
            lx, ly = self.val(nx, y, sp.LOOP)
            # een speler springt liever van een rand dan dat hij valt, als hij dan hoger uitkomt
            jx, jy = self.sprong_van(x, y, sp.LOOP * sp.SPRINT)
            if jy is not None and jx < x - 5 and (ly is None or jy > ly + 1):
                x, y = jx, jy
                continue
            vallen.append((nx, y, ly))
            if ly is None:
                break
            x, y = lx, ly
        self.pad.append((x, y))
        return vallen

    def hoogte_op(self, x):
        """Op welke hoogte Amir langs de route loopt als hij op x is (None: daar komt hij niet)."""
        self.route()
        voor = [(px, py) for px, py in self.pad if px >= x]
        if not voor or self.pad[-1][0] > x + 20:
            return None
        return voor[-1][1]

    def einde(self):
        """Waar het level ophoudt: de fakkels, anders de muur, anders de klif."""
        if self.ends:
            return self.ends[0]['x']
        if self.muur:
            return self.muur['x']
        if self.cliffs:
            return self.cliffs[0]['x']
        return None

    def muurlijn(self):
        return max((c['x'] for c in self.cliffs), default=-math.inf)


class Melding:
    def __init__(self, ernst, x, tekst):
        self.ernst, self.x, self.tekst = ernst, x, tekst


REGELS = []


def regel(naam):
    def zet(f):
        REGELS.append((naam, f))
        return f
    return zet


def fout(x, t): return Melding('FOUT', x, t)
def letop(x, t): return Melding('LET OP', x, t)
def info(x, t): return Melding('info', x, t)


def n0(v):
    return '%d' % round(v)


# ---- de regels ----------------------------------------------------------------

@regel('velden')
def velden(lv, sp):
    """Wat readLevel niet kent of stilletjes weggooit, doet in het spel niets."""
    for k in lv.d:
        if k not in sp.VELDEN:
            yield fout(None, "veld '%s' wordt door readLevel niet overgenomen: in het spel doet het niets" % k)
    if lv.d.get('lagen') and lv.d['lagen'] not in sp.SCENES:
        yield fout(None, "lagen '%s' staat niet in SCENES: het level krijgt het standaarduitzicht" % lv.d['lagen'])
    if lv.d.get('muziek') and lv.d['muziek'] not in sp.MUZIEK:
        yield fout(None, "muziek '%s' staat niet in MUZIEK: er loopt bg.mp3 onder" % lv.d['muziek'])
    for o in lv.d.get('props') or []:
        if o.get('k') not in sp.PROPS:
            yield fout(o.get('x'), "prop '%s' staat niet in PROPS en wordt weggelaten" % o.get('k'))
    for o in lv.d.get('village') or []:
        if o.get('id') not in sp.VILLAGE:
            yield fout(o.get('x'), "dorpsplaat '%s' staat niet in VILLAGE en wordt weggelaten" % o.get('id'))
    for o in lv.d.get('npcs') or []:
        if o.get('k') not in sp.NPCS:
            yield fout(o.get('x'), "npc '%s' staat niet in NPCS en wordt weggelaten" % o.get('k'))
    for o in lv.d.get('spawns') or []:
        if o.get('k') not in ('groen', 'zwart', 'scorp', 'panter', 'hyenas', 'zwaard', 'fosfor'):
            yield fout(o.get('x'), "vijand '%s' bestaat niet: het spel maakt er een groene slang van" % o.get('k'))
        if o.get('c') and o.get('c') not in sp.ZW_KLEUREN:
            yield fout(o.get('x'), "kleur '%s' bestaat niet: het wordt rood" % o.get('c'))
    s = lv.d.get('sneeuw')
    if s:
        if s.get('soort') not in ('savanne', 'rots'):
            yield fout(None, "sneeuw.soort moet 'savanne' of 'rots' zijn: zo doet het hele veld niets")
        if ('van' in s) != ('tot' in s):
            yield fout(None, 'sneeuw heeft van of tot, maar niet allebei: dan telt geen van beide')
        if 'van' in s and 'tot' in s and s['tot'] > s['van']:
            yield letop(None, 'sneeuw.tot ligt rechts van van: Amir loopt naar links, dus het dek loopt af in plaats van op')
    if (lv.d.get('ends') or []) and len(lv.d['ends']) > 1:
        yield letop(lv.d['ends'][1].get('x'), 'meer dan een einde: alleen het eerste telt, de rest wordt weggelaten')


@regel('einde')
def einde(lv, sp):
    """Het level moet uit te spelen zijn, en de klif staat achter de fakkels."""
    if not lv.ends and not lv.muur:
        yield fout(None, 'geen ends en geen muur: dit level is niet uit te spelen')
        return
    wand = lv.muurlijn()
    for e in lv.ends[:1]:
        for c in lv.cliffs:
            if c['x'] >= e['x']:
                yield fout(c['x'], 'klif op %s staat niet achter de fakkels op %s (hij moet negatiever zijn)'
                           % (n0(c['x']), n0(e['x'])))
        if lv.cliffs and e['x'] + sp.EIND_BEREIK <= wand + sp.halfW:
            yield fout(e['x'], 'de fakkels zijn niet te halen: de klif op %s houdt Amir tegen voor hij er is' % n0(wand))
        elif lv.cliffs:
            vrij = (e['x'] - sp.fakkels_halfw()) - (wand + sp.klif_rechts())
            if vrij < 0:
                yield letop(e['x'], 'de fakkels staan %s px in het klifplaatje (tussen einde en klif hoort minstens %s)'
                            % (n0(-vrij), n0(sp.fakkels_halfw() + sp.klif_rechts())))
        if lv.holte(e['x']):
            o = lv.holte(e['x'])
            yield info(e['x'], 'de fakkels staan beneden in de gang, op %s' % n0(-o['diep']))
            if e['x'] - sp.EIND_BEREIK < o['l'] + sp.halfW:
                yield fout(e['x'], 'de fakkels zijn niet te halen: de wand van de gang op %s houdt Amir tegen' % n0(o['l']))
        elif lv.in_gat(e['x'] - sp.fakkels_halfw(), e['x'] + sp.fakkels_halfw()):
            yield fout(e['x'], 'de fakkels staan boven een ravijn')
        if lv.muur and lv.muur['x'] > e['x']:
            yield letop(lv.muur['x'], 'de muur staat voor de fakkels: je moet hem eerst open hebben')
    if not lv.cliffs and lv.ends and not lv.holte(lv.ends[0]['x']):
        yield info(None, 'geen klif achter het einde: je kunt voorbij de fakkels doorlopen')
    if lv.muur and not lv.ends and not lv.cliffs:
        # De rots met de rune is decor: Amir loopt erdoorheen (sinds de rots doorloopbaar is), en
        # uitspelen gaat met E voor de open deur. Zonder klif erachter loopt hij gewoon door, de
        # lege savanne in, zonder dat er ooit nog iets komt. Gezien met de speelrobot.
        yield letop(lv.muur['x'], 'het level eindigt bij de rots met de rune, maar daar staat geen klif achter: de rots '
                    'is decor, Amir loopt erdoorheen en daarna eindeloos door. Zet een klif een stuk achter de rots')


@regel('voorbij het einde')
def voorbij(lv, sp):
    """Wat voorbij de fakkels of achter de klif staat, ziet de speler nooit."""
    eind = lv.einde()
    wand = lv.muurlijn()
    if eind is None:
        return
    for veld, naam in (('spawns', 'vijand'), ('hppotions', 'kalebas'), ('rocks', 'kei'),
                       ('tips', 'tip'), ('thickets', 'doornbos'), ('gaps', 'ravijn')):
        for o in lv.d.get(veld) or []:
            x = o.get('x')
            if not isinstance(x, (int, float)) or x < -50000:
                continue                                  # zie Test 3: een vijand heel ver weg als noodgreep
            if x < wand:
                yield letop(x, '%s op %s staat achter de klif: daar kom je nooit' % (naam, n0(x)))
            elif x < eind - 50 and veld != 'tips':
                yield letop(x, '%s op %s staat voorbij het einde (%s)' % (naam, n0(x), n0(eind)))
    for o in lv.d.get('spawns') or []:
        if isinstance(o.get('x'), (int, float)) and o['x'] > 0:
            yield letop(o['x'], 'vijand op %s staat rechts van de start' % n0(o['x']))


@regel('vijanden')
def vijanden(lv, sp):
    if not lv.d.get('spawns'):
        yield letop(None, 'lege spawns: het spel valt dan terug op de vrije modus en stuurt zelf slangen op je af')
    for o in lv.d.get('spawns') or []:
        if not isinstance(o.get('x'), (int, float)):
            continue
        if lv.holte(o['x']):
            yield info(o['x'], 'vijand %s staat beneden in de gang, op %s' % (o.get('k'), n0(lv.terrein(o['x']))))
        elif lv.in_gat(o['x'] - 40, o['x'] + 40):
            yield letop(o['x'], 'vijand %s start boven een ravijn' % o.get('k'))


@regel('ravijnen')
def ravijnen(lv, sp):
    """Het breedste gat dat de sprong haalt, met het plafond en het water erbij."""
    lopen = sp.LOOP
    rennen = sp.LOOP * sp.SPRINT
    gaps = sorted(lv.gaps, key=lambda g: -g['x'])
    for i, g in enumerate(gaps):
        rand = g['x'] + g['w'] / 2                      # hier zet hij af, hij komt van rechts
        kop = lambda x: lv.kop(x) - lv.terrein(x)
        schoon_r, red_r = sp.sprong(rennen, kop, rand)
        schoon_l, _ = sp.sprong(lopen, kop, rand)
        w = g['w']
        plafond = lv.plafond_min(g['x'] - w / 2, rand) < sp.PLAFOND_WEG
        erbij = ' onder dit plafond' if plafond and schoon_r < sp.sprong(rennen, lambda x: math.inf, 0)[0] - 1 else ''
        # ligt er een gang onder (holtes), dan is dit de ingang: erin vallen is de bedoeling
        ingang = any(h['l'] <= g['x'] - w / 2 and g['x'] + w / 2 <= h['r'] for h in lv.holtes)
        half = any(g['x'] - w / 2 < h['r'] and rand > h['l'] for h in lv.holtes)
        treden = [t for t in lv.terraces if t['h'] < 0 and t['l'] < g['x'] + w / 2 and t['r'] > g['x'] - w / 2]
        if half and not ingang:
            pass                                          # half boven een gang: zie 'onder de grond'
        elif ingang and treden and max(t['h'] for t in treden) > -sp.SPRONG_H:
            yield info(g['x'], 'gat van %s breed boven een gang, met %d treden erin: een weg naar boven'
                       % (n0(w), len(treden)))
        elif ingang and w <= red_r:
            # Een ingang die je kunt overspringen: dan is de gang niet verplicht. Wie springt,
            # loopt over het dak verder en slaat alles over wat erin staat.
            yield info(g['x'], 'ingang van %s breed: %s komt Amir eroverheen, en dan slaat hij de gang over'
                       % (n0(w), 'lopend' if w <= schoon_l else 'met sprint'))
        elif ingang:
            yield info(g['x'], 'ravijn van %s breed boven een gang: de ingang, je valt erin' % n0(w))
        elif w > red_r:
            yield fout(g['x'], 'ravijn van %s breed: met sprint haalt Amir hoogstens %s%s' % (n0(w), n0(red_r), erbij))
        elif w > schoon_r:
            yield letop(g['x'], 'ravijn van %s breed: een sprintsprong komt %s ver%s. Hij haalt de overkant alleen door '
                        'onder de rand te zakken en weer omhoog gezet te worden' % (n0(w), n0(schoon_r), erbij))
        elif w > schoon_l:
            yield info(g['x'], 'ravijn van %s breed: alleen met sprint (lopend %s, sprint %s, met wegzakken %s)'
                       % (n0(w), n0(schoon_l), n0(schoon_r), n0(red_r)))
        # water vlak voor de rand: daar sprint je niet en spring je zwakker
        for p in lv.d.get('water') or []:
            nl, nr = sp.poel_nat(p)
            if nl < rand + (schoon_r - w) and nr > rand:
                yield letop(g['x'], 'poel op %s ligt vlak voor dit ravijn: in het water geen sprint en %d%% springkracht'
                            % (n0(p['x']), round(sp.POOL['jump'] * 100)))
        # terras over de rand
        for t in lv.terraces:
            if ingang and t['h'] < 0:
                continue                                  # een trede in de schacht, zie 'onder de grond'
            if t['l'] < g['x'] + w / 2 and t['r'] > g['x'] - w / 2:
                yield letop(g['x'], 'ravijn loopt onder een terras (%s tot %s) door' % (n0(t['r']), n0(t['l'])))
        # grond tussen twee ravijnen
        if i + 1 < len(gaps):
            h = gaps[i + 1]
            tussen = (g['x'] - w / 2) - (h['x'] + h['w'] / 2)
            if tussen < 0:
                yield fout(g['x'], 'ravijnen op %s en %s overlappen' % (n0(g['x']), n0(h['x'])))
            elif tussen < 2 * sp.halfW:
                yield letop(g['x'], 'tussen de ravijnen op %s en %s ligt maar %s px grond, Amir is %s breed'
                            % (n0(g['x']), n0(h['x']), n0(tussen), n0(2 * sp.halfW)))


@regel('boven een ravijn')
def boven_ravijn(lv, sp):
    """Geen decor boven een ravijn. schoonLevel lost het in het spel op, maar CLAUDE.md
    zegt: reken er niet op, zet het meteen goed. Dezelfde maten en filters als schoonLevel."""
    if not lv.gaps:
        return
    for o in lv.d.get('props') or []:
        d = sp.PROPS.get(o.get('k'))
        if not d:
            continue
        if o.get('v') and (o.get('y') or 0) >= sp.FAR_GAP_LIFT and not d.get('bouwwerk'):
            continue
        hw = sp.prop_halfw(o)
        if lv.in_gat(o['x'] - hw, o['x'] + hw):
            yield fout(o['x'], "%s '%s' staat boven een ravijn (schoonLevel schuift hem weg)"
                       % ('verre prop' if o.get('v') else 'prop', o['k']))
    for o in lv.d.get('village') or []:
        hw = sp.dorp_halfw(o)
        if o.get('id') in sp.VILLAGE and lv.in_gat(o['x'] - hw, o['x'] + hw):
            yield fout(o['x'], "dorpsplaat '%s' staat boven een ravijn" % o['id'])
    for o in lv.d.get('npcs') or []:
        hw = sp.npc_halfw(o)
        if (o.get('y') or 0) < sp.FAR_GAP_LIFT and lv.in_gat(o['x'] - hw, o['x'] + hw):
            yield fout(o['x'], "npc '%s' staat boven een ravijn" % o.get('k'))
    for t in lv.d.get('thickets') or []:
        hw = sp.doornbos_halfw(t) * sp.THICKET_BOX
        if lv.in_gat(t['x'] - hw, t['x'] + hw):
            yield fout(t['x'], 'doornbos staat boven een ravijn')
    # wat schoonLevel niet nakijkt
    for r in lv.rocks:
        l, rr, _ = sp.kei(r, lv.terrein)
        g = lv.in_gat(l, rr)
        if g and lv.in_gat(r['x'], r['x']):
            yield fout(r['x'], 'kei staat midden boven een ravijn')
        elif g:
            over = min(rr, g['x'] + g['w'] / 2) - max(l, g['x'] - g['w'] / 2)
            yield letop(r['x'], 'kei steekt %s px over de rand van het ravijn op %s (op een ander scherm meer of minder)'
                        % (n0(over), n0(g['x'])))
    for p in lv.d.get('hppotions') or []:
        if p.get('y') is None and lv.in_gat(p['x'] - 20, p['x'] + 20):
            yield fout(p['x'], 'kalebas op de grond, maar daar ligt een ravijn: hij is onbereikbaar')
    if lv.muur and lv.in_gat(lv.muur['x'] - 400, lv.muur['x']):
        yield fout(lv.muur['x'], 'de muur met de rune staat boven een ravijn')


@regel('plafond')
def plafond(lv, sp):
    """Rechtop passen, en springen waar je moet springen. Amir is CHAR_H lang; om op iets
    te springen moet het plafond op de hoogte daarvan plus CHAR_H plus ongeveer 75 liggen
    (gemeten in CLAUDE.md: op 440 boven een kei van 114 lukt het ruim, op 400 alleen precies)."""
    if len(lv.plaf) < 2:
        return
    SPELING = 75
    eind = lv.einde()
    eind = eind if eind is not None else lv.plaf[0]['x']
    wand = lv.muurlijn()
    # rechtop lopen over het hele level
    x, krap = 0, None
    while x > max(eind, wand):
        ruimte = lv.plafond_min(x - sp.halfW, x + sp.halfW) - lv.terrein(x)
        if ruimte < sp.CHAR_H:
            if krap is None:
                krap = [x, x, ruimte]
            krap[1], krap[2] = x, min(krap[2], ruimte)
        elif krap:
            yield fout(krap[0], 'van %s tot %s hangt het plafond %s boven de grond: Amir is %s en komt er niet langs'
                       % (n0(krap[0]), n0(krap[1]), n0(krap[2]), sp.CHAR_H))
            krap = None
        x -= 10
    if krap:
        yield fout(krap[0], 'van %s tot %s hangt het plafond %s boven de grond: Amir is %s en komt er niet langs'
                   % (n0(krap[0]), n0(krap[1]), n0(krap[2]), sp.CHAR_H))

    def opstap(x0, x1, top, wat, xm):
        m = lv.plafond_min(x0 - sp.halfW, x1 + sp.halfW)
        if m >= sp.PLAFOND_WEG:
            return
        if m < top + sp.CHAR_H:
            yield fout(xm, '%s is %s hoog en het plafond erboven %s: Amir past er niet op, en de %s houdt hem tegen'
                       % (wat, n0(top), n0(m), wat.split()[0]))
        elif m < top + sp.CHAR_H + SPELING:
            yield letop(xm, '%s is %s hoog en het plafond erboven %s: erop springen lukt alleen precies op tijd '
                        '(minstens %s voor een ruime sprong)' % (wat, n0(top), n0(m), n0(top + sp.CHAR_H + SPELING)))
    for r in lv.rocks:
        l, rr, top = sp.kei(r, lv.terrein)
        yield from opstap(l, rr, top, 'kei op %s' % n0(r['x']), r['x'])
    for t in lv.terraces:
        vloer = lv.terrein(t['r'] + 1, zonder=t)
        if t['h'] > vloer:
            yield from opstap(t['r'] - 150, t['r'], t['h'], 'terras %s tot %s' % (n0(t['r']), n0(t['l'])), t['r'])
    # onder een laag plafond kun je een doornbos niet overslaan, maar dat kan toch nooit;
    # een vijand in een krappe gang is wel het melden waard als hij hoger is dan de ruimte
    for s in lv.d.get('spawns') or []:
        if s.get('k') in ('panter', 'hyenas') and isinstance(s.get('x'), (int, float)):
            ruimte = lv.plafond(s['x']) - lv.terrein(s['x'])
            if ruimte < sp.CHAR_H + sp.SPRONG_H:
                yield info(s['x'], '%s start in een gang van %s hoog: Amir kan er niet overheen springen'
                           % (s['k'], n0(ruimte)))


@regel('terrassen')
def terrassen(lv, sp):
    """Elke trede omhoog moet met een sprong te halen zijn (SPRONG_H: 200 op 60 beelden per
    seconde), of er moet een richel of kei staan om op te stappen. In een gang kapt het dak de
    sprong af: daar mogen zijn voeten niet hoger dan -HOLTE_DAK - CHAR_H komen."""
    KRAP_T = 0.15          # zo lang (seconden) zijn zijn voeten boven de trede: korter is precisiewerk
    eind = lv.einde()
    for t in lv.terraces:
        if t['l'] >= t['r']:
            yield fout(t['r'], 'terras met l (%s) rechts van r (%s): l is de linkerrand, dus negatiever'
                       % (n0(t['l']), n0(t['r'])))
            continue
        vloer = lv.terrein(t['r'] + 1, zonder=t)
        if t['h'] <= vloer:
            continue
        if eind is not None and t['r'] < eind - sp.EIND_BEREIK:
            yield info(t['r'], 'terras van %s hoog staat achter het einde: een eindmuur, beklimmen hoeft niet' % n0(t['h']))
            continue
        # opstappen die er staan: richels aan deze wand en keien ervoor
        treden = []
        for o in lv.ledges:
            if abs(o['x'] - t['r']) < 60:
                treden.append(o['h'])
        for r in lv.rocks:
            l, rr, top = sp.kei(r, lv.terrein)
            if t['r'] - 20 < rr and l < t['r'] + 400:
                treden.append(top)

        def kop(van):
            k = lv.plafond_min(t['r'] - 150, t['r'] + sp.halfW) - sp.CHAR_H
            return min(k, lv.dak_kop(t['r'] + sp.halfW))   # hij zet af tegen de wand, misschien onder het dak

        def apex(van):
            return min(sp.SPRONG_H, kop(van) - van)
        bereikt, rij = {vloer}, [vloer]
        while rij:
            a = rij.pop()
            for b in treden + [t['h']]:
                if b not in bereikt and b > a and b - a < apex(a):
                    bereikt.add(b)
                    rij.append(b)
        if t['h'] not in bereikt:
            waarom = 'Amir springt %s' % n0(sp.SPRONG_H)
            if kop(vloer) - vloer < sp.SPRONG_H:
                waarom = 'het dak van de gang laat zijn voeten niet hoger komen dan %s' % n0(kop(vloer))
            yield fout(t['r'], 'terras van %s hoog op %s: vanaf %s is dat %s omhoog, %s en er staat '
                       'geen richel of kei om op te stappen' % (n0(t['h']), n0(t['r']), n0(vloer),
                                                              n0(t['h'] - vloer), waarom))
        else:
            stap = t['h'] - max(b for b in bereikt if b < t['h'])
            if sp.boven_tijd(stap) < KRAP_T:
                yield letop(t['r'], 'de laatste stap op het terras op %s is %s: bijna de hele sprong van %s '
                            '(op een traag toestel springt hij %s)' % (n0(t['r']), n0(stap), n0(sp.SPRONG_H),
                                                                       n0(sp.SPRONG_TRAAG)))
    for o in lv.ledges:
        if not any(abs(o['x'] - t['r']) < 60 and t['h'] > o['h'] for t in lv.terraces):
            yield letop(o['x'], 'richel op %s hangt niet aan een terraswand' % n0(o['x']))


@regel('onder de grond')
def onder_de_grond(lv, sp):
    """Een gang onder de grond (holtes) en de weg eruit. Een trede onder de grondlijn is een
    terras met een negatieve h: hij hoort in een gang te staan, en waar Amir erop met zijn kruin
    boven het dak uit zou komen, moet er een gat boven zitten. Ligt het einde voorbij de gang, dan
    moet er een trap naar buiten zijn: een gat in het dak met treden erin, en de bovenste binnen
    een sprong van de savanne."""
    dak = -sp.HOLTE_DAK - sp.CHAR_H                 # zo hoog mogen zijn voeten onder het dak
    for o in lv.holtes:
        if o['l'] >= o['r']:
            yield fout(o['r'], 'gang met l (%s) rechts van r (%s): l is de linkerrand, dus negatiever'
                       % (n0(o['l']), n0(o['r'])))
    for t in lv.terraces:
        if t['h'] >= 0:
            continue
        waar = 'trede op %s (%s tot %s)' % (n0(t['h']), n0(t['r']), n0(t['l']))
        o = lv.holte(t['r'])
        if not o or not lv.holte(t['l']) or lv.holte(t['l']) is not o:
            yield fout(t['r'], '%s staat onder de grondlijn maar niet helemaal in een gang: dat is massieve grond' % waar)
            continue
        if t['h'] <= -o['diep']:
            yield letop(t['r'], '%s ligt niet boven de bodem van de gang (%s): die doet niets' % (waar, n0(-o['diep'])))
        if t['h'] > dak:
            # hier steekt hij met zijn kruin boven het dak uit: dat mag alleen onder een gat
            x = t['r']
            while x > t['l']:
                if not lv.in_gat(x - 1, x - 1):
                    yield fout(x, '%s: op %s staat Amir erop met zijn hoofd in het dak (voeten hoger dan %s '
                               'kan alleen onder een gat)' % (waar, n0(x), n0(dak)))
                    break
                x -= 10
            g = lv.in_gat(t['r'], t['r'])
            if g and t['r'] + sp.halfW > g['x'] + g['w'] / 2:
                yield fout(t['r'], '%s: wie ertegenaan staat, staat nog onder het dak en springt er niet op. '
                           'Zet de rechterrand minstens %s binnen het gat' % (waar, n0(sp.halfW)))
    # de weg naar boven
    eind = lv.einde()
    for o in lv.holtes:
        if eind is None or eind >= o['l'] or lv.holte(eind):
            continue                                      # het einde ligt in de gang, of ervoor
        ingang = [g for g in lv.gaps if o['l'] <= g['x'] - g['w'] / 2 and g['x'] + g['w'] / 2 <= o['r']]
        if not ingang:
            continue                                      # er komt niemand in
        uit = False
        for g in ingang:
            gl = g['x'] - g['w'] / 2
            for t in lv.terraces:
                if t['h'] < 0 and t['l'] <= gl + sp.halfW and t['r'] > gl and -t['h'] < sp.SPRONG_H:
                    uit = True
        if not uit:
            yield fout(o['l'], 'het einde (%s) ligt voorbij de gang van %s tot %s, maar er is geen weg naar boven: '
                       'een gat in het dak met treden erin, de bovenste tegen de linkerrand van het gat en '
                       'minder dan %s onder de grondlijn' % (n0(eind), n0(o['r']), n0(o['l']), n0(sp.SPRONG_H)))


@regel('onder de grond')
def gangen(lv, sp):
    """Wat er mis kan gaan met de gang zelf en wat erboven of erin staat. Elk hiervan is met de
    speelrobot in een proefgang nagelopen (zie CLAUDE.md, "een gang onder de grond")."""
    dak = -sp.HOLTE_DAK - sp.CHAR_H                 # zo hoog mogen zijn voeten onder het dak
    ruw = [o for o in (lv.d.get('holtes') or []) if isinstance(o, dict)]
    for o in ruw:
        if (o.get('diep') or 600) < sp.HOLTE_DAK + sp.CHAR_H:
            yield letop(o.get('r'), 'gang van %s tot %s is %s diep: readLevel maakt daar %s van (het dak op %s plus Amir), '
                        'en daar rekent dit script ook mee' % (n0(o['r']), n0(o['l']), n0(o.get('diep') or 0),
                                                               n0(sp.HOLTE_DAK + sp.CHAR_H), n0(sp.HOLTE_DAK)))
    # Twee gangen tegen elkaar: holteBlok houdt hem in allebei tegelijk vast, dus op de naad
    # staat hij klem en komt hij niet verder, ook niet als de ene gang dieper is dan de andere.
    marge = 2 * (sp.halfW + 60)
    hs = sorted(lv.holtes, key=lambda o: -o['r'])
    for a, b in zip(hs, hs[1:]):
        if b['r'] > a['l'] - marge:
            yield fout(a['l'], 'de gangen van %s tot %s en van %s tot %s liggen tegen elkaar: op de naad houdt de wand '
                       'van de ene hem vast en die van de andere ook, en daar staat hij klem. Maak er een gang van '
                       '(de diepste diep) en leg de hogere stukken als treden: terrassen met een negatieve h'
                       % (n0(a['r']), n0(a['l']), n0(b['r']), n0(b['l'])))
    for g in lv.gaps:
        gr, gl = g['x'] + g['w'] / 2, g['x'] - g['w'] / 2
        for o in lv.holtes:
            if gl < o['r'] and gr > o['l'] and not (o['l'] <= gl and gr <= o['r']):
                yield fout(g['x'], 'het gat van %s tot %s ligt maar voor een deel boven de gang (%s tot %s): wie aan '
                           'de kant zonder gang erin valt, valt recht naar beneden en is dood. Leg het gat helemaal '
                           'boven de gang, of de gang verder door' % (n0(gr), n0(gl), n0(o['r']), n0(o['l'])))
    if not lv.holtes:
        return
    # een terras op de savanne boven een gang: drawClimb tekent zijn wand tot onder in beeld, en
    # blockByPlatforms houdt Amir er beneden tegen, dus het staat als een pilaar door de gang
    for t in lv.terraces:
        if t['h'] < 0:
            continue
        for o in lv.holtes:
            if t['l'] < o['r'] and t['r'] > o['l']:
                yield fout(t['r'], 'terras van %s tot %s (h %s) staat boven de gang van %s tot %s: zijn wand loopt '
                           'door tot in de gang en staat daar als een pilaar, waar Amir beneden niet langs komt'
                           % (n0(t['r']), n0(t['l']), n0(t['h']), n0(o['r']), n0(o['l'])))
    # keien: in een gang staat een kei op de bodem, en daar kapt het dak zijn sprong af
    for r in lv.rocks:
        if not lv.holte(r['x']) or lv.in_gat(r['x'] - 150, r['x'] + 150):
            continue
        l, rr, top = sp.kei(r, lv.terrein)
        if top > dak:
            yield fout(r['x'], 'kei op %s staat in de gang en is %s hoog: bovenop zou Amir met zijn hoofd in het dak zitten '
                       '(voeten hoger dan %s), dus hij komt er niet overheen en er ook niet langs'
                       % (n0(r['x']), n0(top), n0(dak)))
        elif top > dak - 60:
            yield letop(r['x'], 'kei op %s staat in de gang en is %s hoog: het dak kapt de sprong erop af op %s, '
                        'erop komen is precisiewerk' % (n0(r['x']), n0(top), n0(dak)))
    # decor in de gang staat op de bodem; wat hoger is dan de gang steekt door het dak
    def door_dak(x, hoog):
        return lv.holte(x) and not lv.in_gat(x - 60, x + 60) and lv.terrein(x) + hoog > -sp.HOLTE_DAK
    for o in lv.d.get('props') or []:
        d = sp.PROPS.get(o.get('k'))
        if not d or o.get('v'):
            continue                                    # ver decor blijft boven op de savanne
        hoog = sp.CHAR_H * d['h'] * (o.get('s') or 1) * (1 - (d.get('sink') or 0.02))
        if door_dak(o['x'], hoog):
            yield fout(o['x'], "prop '%s' staat in de gang, op de bodem (%s), en is %s hoog: hij steekt door het dak "
                       '(op %s)' % (o['k'], n0(lv.terrein(o['x'])), n0(hoog), n0(-sp.HOLTE_DAK)))
    for o in lv.d.get('village') or []:
        d = sp.VILLAGE.get(o.get('id'))
        if d and lv.holte(o['x']):
            depth = max(0, min(1, o.get('depth') or 0))
            hoog = sp.CHAR_H * d['h'] * (1 - sp.VILLAGE_FAR * depth)
            if door_dak(o['x'], hoog):
                yield fout(o['x'], "dorpsplaat '%s' staat in de gang en steekt door het dak" % o['id'])
    for o in lv.d.get('npcs') or []:
        d = sp.NPCS.get(o.get('k'))
        if d and door_dak(o['x'], sp.CHAR_H * d['tall'] * (o.get('s') or 1) + (o.get('y') or 0)):
            yield fout(o['x'], "npc '%s' staat in de gang en steekt door het dak" % o['k'])
    for t in lv.d.get('thickets') or []:
        if isinstance(t.get('x'), (int, float)) and door_dak(t['x'], sp.doornbos_hoog(t)):
            yield fout(t['x'], 'doornbos op %s staat in de gang en is %s hoog: hij steekt door het dak'
                       % (n0(t['x']), n0(sp.doornbos_hoog(t))))
    # de speer: aan het begin staat hij op SPEAR_AHEAD in de grond, en in een gang staat hij beneden
    if not lv.muur and lv.holte(sp.SPEAR_AHEAD) and not lv.in_gat(sp.SPEAR_AHEAD - 30, sp.SPEAR_AHEAD + 30):
        yield fout(sp.SPEAR_AHEAD, 'je speer staat aan het begin op %s, en daar ligt een gang: hij staat beneden op de '
                   'bodem, onder de savanne waar Amir begint. Laat de gang verderop beginnen' % n0(sp.SPEAR_AHEAD))


@regel('vallen')
def vallen(lv, sp):
    """Met valschade: de weg die Amir aflegt als hij gewoon naar links loopt, met elke val die
    onderweg niet te vermijden is. Een val loopt hij op looptempo in: wie rent, komt verder en
    soms lager of hoger uit. De kalebassen in het level drinkt hij zodra hij er een heeft en niet
    vol zit; de losse kalebassen die af en toe verschijnen tellen niet mee."""
    if not lv.d.get('valschade'):
        return
    kalebassen = sorted((p['x'] for p in lv.d.get('hppotions') or [] if isinstance(p.get('x'), (int, float))),
                        reverse=True)
    levens, zak, k = sp.LEVENS, 0, 0
    for x, van, naar in lv.route():
        while k < len(kalebassen) and kalebassen[k] >= x:
            zak += 1; k += 1
        while zak and levens < sp.LEVENS:
            zak -= 1; levens = min(sp.LEVENS, levens + sp.HPPOTION_HEAL)
        if naar is None:
            continue                                    # een ravijn: dat is voor de regel ravijnen
        diep = van - naar
        kost = 0 if diep < sp.VAL_VRIJ else (1 if diep < sp.VAL_ZWAAR else sp.VAL_MAX)
        if not kost:
            continue
        levens -= kost
        waar = 'de ingang van de gang' if lv.in_gat(x, x) and lv.holte(x) else 'de rand op %s' % n0(x)
        if levens <= 0:
            yield fout(x, 'val van %s naar %s bij %s kost %s: dan is hij dood, ook met de kalebassen die hij tot hier '
                       'heeft gevonden. Onderweg kost vallen alleen al meer dan de %s levens die hij heeft'
                       % (n0(van), n0(naar), waar, '2 levens' if kost == 2 else '1 leven', sp.LEVENS))
            return
        yield letop(x, 'val van %s naar %s bij %s kost %s (daarna nog %s)' % (
            n0(van), n0(naar), waar, '2 levens' if kost == 2 else '1 leven', levens))


@regel('water')
def water(lv, sp):
    for p in lv.d.get('water') or []:
        nl, nr = sp.poel_nat(p)
        for t in lv.terraces:
            if t['l'] < nr and t['r'] > nl:
                yield letop(p['x'], 'poel op %s ligt onder een terras' % n0(p['x']))


# ---- uitvoeren --------------------------------------------------------------

def lees_levels(bron):
    reeksen = re.findall(r'const (\w+_LEVELS) = \[([^\]]*)\]', bron.src)
    if not reeksen:
        stop('geen *_LEVELS-reeksen gevonden')
    uit = []
    for reeks, namen in reeksen:
        for naam in re.findall(r'\w+', namen):
            try:
                d = bron.const(naam)
            except ValueError as e:
                stop('%s is niet te lezen: %s' % (naam, e))
            uit.append((reeks, naam, d))
    return uit


def main(argv):
    hoog, formaat, uitgebreid, filters, breed, bestanden = 720, 25, False, [], None, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ('-h', '--help'):
            print(__doc__)
            return 0
        if a == '-v':
            uitgebreid = True
        elif a == '--hoog':
            i += 1; hoog = float(argv[i])
        elif a == '--breed':
            i += 1; breed = float(argv[i])
        elif a == '--formaat':
            i += 1; formaat = float(argv[i])
        elif a.endswith('.json'):
            bestanden.append(a)
        else:
            filters.append(a.lower())
        i += 1
    bron = Bron(HTML)
    sp = Spel(bron, hoog, formaat, breed)
    levels = lees_levels(bron)
    if bestanden:                                   # een level uit de bouwer (Exporteer), of met de hand
        levels = []
        for pad in bestanden:
            with open(pad, encoding='utf-8') as f:
                levels.append(('json', os.path.basename(pad), json.load(f)))
    print('scherm %d hoog, Formaat %d: Amir %.0f px breed, sprong %.0f hoog, lopend %d px/s, sprint %d px/s'
          % (hoog, formaat, 2 * sp.halfW, sp.SPRONG_H, sp.LOOP, sp.LOOP * sp.SPRINT))
    fouten = letops = 0
    for reeks, naam, d in levels:
        titel = d.get('name') or naam
        if filters and not any(f in titel.lower() or f in naam.lower() for f in filters):
            continue
        lv = Level(naam, d, sp)
        meldingen = []
        for rnaam, f in REGELS:
            for m in f(lv, sp):
                if m.ernst == 'info' and not uitgebreid:
                    continue
                meldingen.append((rnaam, m))
        fouten += sum(m.ernst == 'FOUT' for _, m in meldingen)
        letops += sum(m.ernst == 'LET OP' for _, m in meldingen)
        kop = '%s (%s)' % (titel, naam)
        if not meldingen:
            print('\n' + kop + ': in orde')
            continue
        print('\n' + kop)
        volg = {'FOUT': 0, 'LET OP': 1, 'info': 2}
        meldingen.sort(key=lambda rm: (volg[rm[1].ernst], -(rm[1].x if isinstance(rm[1].x, (int, float)) else 1)))
        for rnaam, m in meldingen:
            waar = ('x=%s' % n0(m.x)) if isinstance(m.x, (int, float)) else ''
            print('  %-6s  %-8s  %-18s %s' % (m.ernst, waar, rnaam, m.tekst))
    print('\n%d fout%s, %d keer let op' % (fouten, '' if fouten == 1 else 'en', letops))
    return 1 if fouten else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
