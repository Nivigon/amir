"""De baviaan los van zijn magenta achtergrond.

Leest baviaan_base_magenta.png uit de hoofdmap en schrijft enemies/baviaan/baviaan.png:
magenta wordt doorzichtig, en op de rand wordt de magenta uit de kleur gehaald (ontmengd), zodat
er geen roze zoom om de vacht blijft. Daarna bijgesneden tot wat er van hem staat.

Hoe magenta een pixel is: min(rood, blauw) min groen. De achtergrond is 255, de vacht, de rode
borst en de blauwe snuit komen niet boven nul (groen is daar nooit lager dan rood en blauw
allebei). Draai opnieuw als het bronplaatje verandert.
"""
from pathlib import Path
from PIL import Image

HIER = Path(__file__).resolve().parent.parent
BRON = HIER / 'baviaan_base_magenta.png'
DOEL = HIER / 'enemies' / 'baviaan' / 'baviaan.png'
VOL, WEG = 30, 235          # onder VOL helemaal hem, boven WEG helemaal achtergrond

im = Image.open(BRON).convert('RGB')
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
uit = uit.crop(uit.getbbox())
DOEL.parent.mkdir(parents=True, exist_ok=True)
uit.save(DOEL, optimize=True)
print(DOEL.relative_to(HIER), uit.size)
