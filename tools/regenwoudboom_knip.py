"""De regenwoudboom los van zijn roze achtergrond.

Leest regenwoudboom_magenta.jpg uit de hoofdmap en schrijft design/regenwoud/regenwoudboom.png.
De achtergrond is geen zuiver magenta maar een donker roze (ongeveer 204, 37, 120), en het is een
jpg, dus die kleur is niet overal precies dezelfde. De kleur van de achtergrond wordt daarom uit de
bovenhoeken gemeten, en per pixel geteld hoe ver hij die kant op ligt: rood min groen en blauw
min groen, allebei gedeeld door wat de achtergrond daar heeft, en daarvan het kleinste. Dat
getal wordt nog gedeeld door de helderheid, want in de gaatjes van de kroon ligt de achtergrond
in de schaduw van het blad, en daar is het roze donkerder (zo'n 180, 53, 106). Het blad
is groen en de stam bruin, en bij allebei is blauw niet hoger dan groen, dus die komen niet boven
nul. Op de rand wordt het roze uit de kleur gehaald (ontmengd), zoals bij de baviaan, zodat er
geen roze zoom om de kroon blijft. Een jpg smeert de kleur bovendien over een paar pixels uit, en
dan hangt er nog roze in de dunne lianen en in de gaatjes van de kroon. Wat daarna nog de kant van
de achtergrond op wijst, wordt er daarom ook uit gehaald (`ontroze`): dat raakt alleen pixels waar
rood en blauw allebei boven groen liggen, en die komen in de boom zelf niet voor.

Daarna bijgesneden en verkleind tot BRON_H hoog: zo komen er evenveel bronpixels op een Amir als
bij de gewone boom (design/tree.png, 943 hoog op 2,4 Amir), en hoeft hij net als die niet in de
kleine set. Draai opnieuw als het bronplaatje verandert.
"""
from pathlib import Path
from PIL import Image

HIER = Path(__file__).resolve().parent.parent
BRON = HIER / 'regenwoudboom_magenta.jpg'
DOEL = HIER / 'design' / 'regenwoud' / 'regenwoudboom.png'
VOL, WEG = 0.25, 0.65       # onder VOL helemaal boom, boven WEG helemaal achtergrond
HOOG = 3.3                  # de hoogte in Amir, zoals in PROPS
BRON_H = round(943 / 2.4 * HOOG)

im = Image.open(BRON).convert('RGB')
w, h = im.size
px = im.load()
# de achtergrond: het gemiddelde van twee hoekjes bovenin, waar de kroon niet komt
hoek = [px[x, y] for y in range(4, 40) for x in list(range(4, 40)) + list(range(w - 40, w - 4))]
K = tuple(sum(c[i] for c in hoek) / len(hoek) for i in range(3))
rg, bg = K[0] - K[1], K[2] - K[1]
KMAX = max(K)

def ontroze(r, g, b):
    m = min((r - g) / rg, (b - g) / bg)
    if m <= 0:
        return r, g, b
    return round(r - m * rg), g, round(b - m * bg)

uit = Image.new('RGBA', (w, h))
up = uit.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        # los van de helderheid: in de gaatjes van de kroon ligt de achtergrond in de schaduw
        m = min((r - g) / rg, (b - g) / bg) * KMAX / max(r, g, b, 40)
        if m <= VOL:
            up[x, y] = ontroze(r, g, b) + (255,)
            continue
        if m >= WEG:
            up[x, y] = (0, 0, 0, 0)
            continue
        a = 1 - (m - VOL) / (WEG - VOL)
        # c = a * voor + (1 - a) * achtergrond, dus voor = (c - (1 - a) * achtergrond) / a
        f = lambda c, k: max(0, min(255, round((c - (1 - a) * k) / a)))
        up[x, y] = ontroze(f(r, K[0]), f(g, K[1]), f(b, K[2])) + (round(a * 255),)
uit = uit.crop(uit.getbbox())
uit = uit.resize((round(uit.width * BRON_H / uit.height), BRON_H), Image.LANCZOS)
DOEL.parent.mkdir(parents=True, exist_ok=True)
uit.save(DOEL, optimize=True)
print(DOEL.relative_to(HIER), uit.size, 'achtergrond', tuple(round(k) for k in K))
