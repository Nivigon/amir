"""(ren_sp: de voorarm houdt de speer en heeft een losse vuistlaag, die blijft ongemoeid.)

Laat de renloop van Mkuki echt links-rechts wisselen.

Frames 1-6: nabij = achterbeen + voorarm (zoals Grok tekende), ver = voorbeen + achterarm.
Frames 7-12: nabij = voorbeen + achterarm, ver = achterbeen + voorarm.
Ver = donkerder (zoals het verre been in het origineel). In 7-12 komt het voorste dijbeen
voor de schort langs: de vorm van dat dijbeen komt uit het originele frame (dat precies onder
het Mkuki-frame ligt), ingekleurd met de broekkleur van Mkuki en de schaduw van het origineel.

python3 wissel.py <set> <uitmap>     (set = ren_ns of ren_sp; draaien vanuit karakters/amir)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from ledematen import laad, splits, geo, zonemasker, VB, AB, VA, AA

VER = 0.70        # helderheid van de verre ledematen
NABIJ = 1.06      # nabije iets lichter
ZONE_BROEK = (0, 0, 255)


def verzacht(m, s=1.5):
    return nd.gaussian_filter(m.astype(float), s)


def dijbeen_voor_schort(im, z, orig, lab):
    """Masker van het voorste dijbeen uit het origineel, op de plek van de schort."""
    o = orig.astype(float) / 255
    r, g, b = o[..., 0], o[..., 1], o[..., 2]
    al = orig[..., 3] > 100
    paars = al & (b > r + 0.03) & (b > g + 0.08)
    paars = nd.binary_opening(paars, iterations=1)
    H, W = al.shape
    Y, X = np.mgrid[:H, :W]
    oy, ox = np.where(al & (Y > np.where(paars)[0].min() + 15))
    i = np.argmin(ox); vb = (oy[i], ox[i])
    i = np.argmax(ox); ab = (oy[i], ox[i])
    dv, da = geo(al, [vb]), geo(al, [ab])
    voor = paars & (dv < da - 2)
    schort = zonemasker(z, (255, 255, 0))
    m = voor & schort
    # alleen het deel dat aansluit op het zichtbare voorbeen van Mkuki
    lb, n = nd.label(m)
    keep = np.zeros_like(m)
    buur = nd.binary_dilation(lab == VB, iterations=3)
    for k in range(1, n + 1):
        c = lb == k
        if (c & buur).any() and c.sum() > 30:
            keep |= c
    keep = nd.binary_closing(keep, iterations=2) & schort
    return keep, o


def main():
    set_, uit = sys.argv[1], sys.argv[2]
    os.makedirs(uit, exist_ok=True)
    for n in range(1, 13):
        p = f'mkuki/beweging/run/nieuw/{set_}_{n}'
        im = laad(p + '.png'); z = laad(p + '_zones.png')
        orig = laad(f'beweging/run/nieuw/{set_}_{n}.png')
        lab, _ = splits(im, z)
        out = im.astype(float)
        zo = z.copy()
        tweede = n > 6
        if tweede:
            # voorste dijbeen voor de schort langs
            dij, o = (dijbeen_voor_schort(im, z, orig, lab) if os.environ.get('DIJ') else (np.zeros(lab.shape, bool), None))
            broek = zonemasker(z, ZONE_BROEK) & (lab == VB)
            if dij.any() and broek.any():
                ref = im[broek][:, :3].astype(float)
                Lm = ref.mean(1)
                Lo = (o[..., :3].mean(-1) * 255)
                Lo_ref = Lo[nd.binary_dilation(dij, iterations=4) & ~dij & broek]
                basis = np.median(ref, 0) / max(np.median(Lm), 1)
                schaal = np.median(Lm) / max(np.median(Lo_ref) if Lo_ref.size else np.median(Lo[dij]), 1)
                kleur = (Lo[..., None] * schaal) * basis[None, None, :]
                out[dij, :3] = kleur[dij]
                out[dij, 3] = 255
                # donkere omtrek langs de rand van het dijbeen (stijl van de frames)
                rand = dij & ~nd.binary_erosion(dij, iterations=1)
                out[rand, :3] *= 0.55
                zo[dij, :3] = ZONE_BROEK
                lab[dij] = VB
            ver = (lab == AB) | ((lab == VA) & (set_ != 'ren_sp'))
            nab = (lab == VB) | (lab == AA)
        else:
            ver = (lab == VB) | (lab == AA)
            nab = (lab == AB) | ((lab == VA) & (set_ != 'ren_sp'))
        f = 1 + (VER - 1) * verzacht(ver) + (NABIJ - 1) * verzacht(nab)
        out[..., :3] *= f[..., None]
        Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(f'{uit}/{set_}_{n}.png')
        Image.fromarray(zo).save(f'{uit}/{set_}_{n}_zones.png')


if __name__ == '__main__':
    main()
