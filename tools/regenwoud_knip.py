"""De stukken van het regenwoud los van hun roze achtergrond.

Leest uit de hoofdmap en schrijft naar design/regenwoud/:

    regenwoudboom_magenta.jpg          regenwoudboom.png      de boom (PROPS.regenwoudboom)
    regenwoudbodem_magenta.jpg         bodem.png              de bodem: bovenvlak en wand
    regenwoudbodem_water_magenta.jpg   bodem_water.png        dezelfde strook met een poel erin

De achtergrond is geen zuiver magenta maar een donker roze (ongeveer 204, 37, 120, en bij de bodem
wat donkerder), en het zijn jpg's, dus die kleur is niet overal precies dezelfde. De kleur van de
achtergrond wordt daarom per plaatje uit de bovenhoeken gemeten, en per pixel geteld hoe ver hij
die kant op ligt: rood min groen en blauw min groen, allebei gedeeld door wat de achtergrond daar
heeft, en daarvan het kleinste. Dat getal wordt nog gedeeld door de helderheid, want in de gaatjes
van de kroon ligt de achtergrond in de schaduw van het blad, en daar is het roze donkerder (zo'n
180, 53, 106). Blad, stam, aarde en water komen niet boven nul: blauw is er niet hoger dan groen,
of rood niet. Op de rand wordt het roze uit de kleur gehaald (ontmengd), zoals bij de baviaan,
zodat er geen roze zoom blijft. Een jpg smeert de kleur bovendien over een paar pixels uit, en dan
hangt er nog roze in de dunne lianen en in de gaatjes van de kroon. Wat daarna nog de kant van de
achtergrond op wijst, wordt er daarom ook uit gehaald (`ontroze`): dat raakt alleen pixels waar
rood en blauw allebei boven groen liggen, en die komen in de stukken zelf niet voor.

De boom wordt bijgesneden en verkleind tot BRON_H hoog: zo komen er evenveel bronpixels op een Amir
als bij de gewone boom (design/tree.png, 943 hoog op 2,4 Amir), en hoeft hij net als die niet in de
kleine set. De twee bodems worden met hetzelfde kader bijgesneden (wat van allebei samen staat),
zodat ze even groot zijn en de strook met water precies over de gewone valt. Die blijven op hun
eigen maat; hoe ze in het spel komen is nog niet gekozen.

Draai opnieuw als een bronplaatje verandert.
"""
from pathlib import Path
from PIL import Image

HIER = Path(__file__).resolve().parent.parent
MAP = HIER / 'design' / 'regenwoud'
VOL, WEG = 0.25, 0.65       # onder VOL helemaal voorgrond, boven WEG helemaal achtergrond
HOOG = 3.3                  # de hoogte van de boom in Amir, zoals in PROPS
BRON_H = round(943 / 2.4 * HOOG)


def knip(naam):
    """Het plaatje met de achtergrond doorzichtig, nog niet bijgesneden."""
    im = Image.open(HIER / naam).convert('RGB')
    w, h = im.size
    px = im.load()
    # de achtergrond: het gemiddelde van twee hoekjes bovenin, waar niets staat
    hoek = [px[x, y] for y in range(4, 40) for x in list(range(4, 40)) + list(range(w - 40, w - 4))]
    K = tuple(sum(c[i] for c in hoek) / len(hoek) for i in range(3))
    rg, bg = K[0] - K[1], K[2] - K[1]
    kmax = max(K)

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
            m = min((r - g) / rg, (b - g) / bg) * kmax / max(r, g, b, 40)
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
    return uit, K


def bewaar(im, naam, K):
    MAP.mkdir(parents=True, exist_ok=True)
    im.save(MAP / naam, optimize=True)
    print((MAP / naam).relative_to(HIER), im.size, 'achtergrond', tuple(round(k) for k in K))


boom, K = knip('regenwoudboom_magenta.jpg')
boom = boom.crop(boom.getbbox())
boom = boom.resize((round(boom.width * BRON_H / boom.height), BRON_H), Image.LANCZOS)
bewaar(boom, 'regenwoudboom.png', K)

bodem, K1 = knip('regenwoudbodem_magenta.jpg')
water, K2 = knip('regenwoudbodem_water_magenta.jpg')
b1, b2 = bodem.getbbox(), water.getbbox()
kader = (min(b1[0], b2[0]), min(b1[1], b2[1]), max(b1[2], b2[2]), max(b1[3], b2[3]))
bewaar(bodem.crop(kader), 'bodem.png', K1)
bewaar(water.crop(kader), 'bodem_water.png', K2)
