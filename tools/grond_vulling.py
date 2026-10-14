"""Maakt een verticaal naadloze aarde-vultegel uit grondrand.png, voor de doorlopende onderkant van een
afgesloten savannelaag/zwevende laag (zoals rots_vulling.png voor de schachtwand). Neemt de pure-aarde band
(zonder het oppervlak en zonder de doorzichtige onderrand) en maakt die verticaal naadloos met de dubbele-
offset-blend: rolled heeft een schone boven/onderrand maar een naad in het midden, other (nog eens gerold)
heeft het omgekeerde; we mengen ze met een driehoekgewicht dat in het midden other kiest en aan de randen
rolled, zodat beide naden verdwijnen. Horizontaal is grondrand al naadloos. Verandert grondrand, draai
dit opnieuw."""
from PIL import Image, ImageChops

ROOT = '/home/user/amir'
BRON = ROOT + '/design/grondrand.png'
UIT = ROOT + '/design/klimmen/grond_vulling.png'
Y0, Y1 = 200, 300            # de pure-aarde band in grondrand (gemeten)

def main():
    im = Image.open(BRON).convert('RGBA')
    earth = im.crop((0, Y0, im.width, Y1))
    w, h = earth.size
    rolled = ImageChops.offset(earth, 0, h // 2)        # schone boven/onderrand, naad in het midden
    other = ImageChops.offset(rolled, 0, h // 2)        # schone middenrij, naad aan boven/onderrand
    rp, op = rolled.load(), other.load()
    out = Image.new('RGBA', (w, h)); ot = out.load()
    for y in range(h):
        m = 1 - abs(y - h / 2) / (h / 2)                 # 1 in het midden -> 0 aan de randen
        m = m * m * (3 - 2 * m)                          # smoothstep
        for x in range(w):
            ra, ga, ba, aa = rp[x, y]
            rb, gb, bb, ab = op[x, y]
            ot[x, y] = (round(ra * (1 - m) + rb * m), round(ga * (1 - m) + gb * m),
                        round(ba * (1 - m) + bb * m), round(aa * (1 - m) + ab * m))
    out.save(UIT)
    print('geschreven:', UIT, out.size)

if __name__ == '__main__':
    main()
