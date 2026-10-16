"""De fakkel los van zijn magenta achtergrond.

Leest de 24 aangeleverde frames uit design/fakkel/bron/ (frame_01..24.png, zuiver magenta
#FF00FF achter een wandfakkel met beugel, zie bron/LEESMIJ.txt) en schrijft design/fakkel/
frame_01..24.png: magenta wordt doorzichtig, en op de rand wordt de magenta uit de kleur
gehaald (ontmengd), zodat er geen roze zoom om de vlam en het hout blijft. Dezelfde aanpak als
tools/baviaan_knip.py.

De frames moeten uitgelijnd blijven (de fakkel staat in elk frame op exact dezelfde plek, zie
de LEESMIJ), dus ze worden NIET los bijgesneden maar allemaal op dezelfde gedeelde bbox: de
union van alles wat in een van de frames zichtbaar is. Zo trimmen we de grote lege magenta
rechterhelft weg zonder dat de vlam tussen twee frames verspringt.

Hoe magenta een pixel is: min(rood, blauw) min groen. De achtergrond is 255, de vlam (oranje,
geel, wit), het bruine hout en de donkere beugel komen niet boven nul (groen is daar nooit
lager dan rood en blauw allebei), en de lichtroze rook aan het eind blijft ook staan (die is
grijs: rood, groen en blauw dicht bij elkaar). Draai opnieuw als de bronframes veranderen,
en daarna tools/gen-klein.py en tools/gen-offline-manifest.py.
"""
from pathlib import Path
from PIL import Image

HIER = Path(__file__).resolve().parent.parent
BRON = HIER / 'design' / 'fakkel' / 'bron'
DOEL = HIER / 'design' / 'fakkel'
VOL, WEG = 30, 235          # onder VOL helemaal de fakkel, boven WEG helemaal achtergrond
N = 24

def ontmeng(im):
    """magenta -> doorzichtig, met ontmenging op de rand; geeft een RGBA-beeld terug"""
    w, h = im.size
    px = im.load()
    uit = Image.new('RGBA', (w, h))
    up = uit.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            m = min(r, b) - g
            if m <= VOL:
                up[x, y] = (r, g, b, 255)
                continue
            if m >= WEG:
                up[x, y] = (0, 0, 0, 0)
                continue
            a = 1 - (m - VOL) / (WEG - VOL)
            # c = a * voor + (1 - a) * magenta, dus voor = (c - (1 - a) * magenta) / a
            f = lambda c, mg: max(0, min(255, round((c - (1 - a) * mg) / a)))
            up[x, y] = (f(r, 255), f(g, 0), f(b, 255), round(a * 255))
    return uit

beelden = [ontmeng(Image.open(BRON / ('frame_%02d.png' % i)).convert('RGB')) for i in range(1, N + 1)]

# de gedeelde bbox: de union van wat in een van de frames zichtbaar is, zodat de uitlijning klopt
bbox = None
for im in beelden:
    bb = im.getbbox()
    if bb is None:
        continue
    bbox = bb if bbox is None else (min(bbox[0], bb[0]), min(bbox[1], bb[1]),
                                    max(bbox[2], bb[2]), max(bbox[3], bb[3]))

DOEL.mkdir(parents=True, exist_ok=True)
for i, im in enumerate(beelden, 1):
    im.crop(bbox).save(DOEL / ('frame_%02d.png' % i), optimize=True)
print('%d frames, gedeelde bbox %s -> %s' % (N, bbox, (bbox[2] - bbox[0], bbox[3] - bbox[1])))
