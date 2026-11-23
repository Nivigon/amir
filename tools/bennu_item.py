# Het beeld van Feathers of the Bennu in de winkel en de balk: drie veren uit verenset.png, roze gekleurd zoals in het spel
# (grijs maal de kleur, BN.kleuren Pink), in een waaier. Schrijft items/bennu/veren.png en items/bennu/veren_icoon.png.
from PIL import Image, ImageChops, ImageFilter
SET = 'karakters/amir/mkuki_spel/bennu/verenset.png'
KLEUR = (255, 159, 208)
mix = tuple(round(c + (255 - c) * 0.1) for c in KLEUR)
vel = Image.open(SET).convert('RGBA')
def veer(rij, kol=0):
    v = vel.crop((kol * 240, rij * 56, kol * 240 + 240, rij * 56 + 56))
    kl = ImageChops.multiply(v.convert('RGB'), Image.new('RGB', v.size, mix)).convert('RGBA')
    kl.putalpha(v.getchannel('A'))
    return kl
W, H = 340, 512
doek = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for rij, hoek, dx in ((2, 62, -40), (1, 90, 0), (0, 118, 40)):
    v = veer(rij).resize((480, 112), Image.LANCZOS).rotate(hoek, expand=True, resample=Image.BICUBIC)
    doek.alpha_composite(v, (W // 2 - v.width // 2 + dx, H // 2 - v.height // 2 - 10))
gloed = Image.new('RGBA', (W, H), KLEUR + (0,))
a = doek.getchannel('A').filter(ImageFilter.GaussianBlur(14)).point(lambda p: int(p * 0.7))
gloed.putalpha(a)
uit = Image.alpha_composite(gloed, doek)
uit = uit.crop(uit.getbbox())
uit.save('items/bennu/veren.png')
ic = uit.copy(); ic.thumbnail((84, 128), Image.LANCZOS); ic.save('items/bennu/veren_icoon.png')
print(uit.size, ic.size)
