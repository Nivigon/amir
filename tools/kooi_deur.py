#!/usr/bin/env python3
"""Het deurtje van de dierenkooien (design/stad/kooi/deur.png), uit de voorkant van de hoge kooi.

Een smal raam van hetzelfde hout: twee stijlen uit de linkerpaal (met het ijzeren hoekbeslag), de bovenregel en de
onderregel uit de kooi, en vijf tralies ertussen. Het spel tekent het in perspectief als het deurtje opengaat
(dkDeurTeken). Draai daarna tools/gen-offline-manifest.py.
"""
from PIL import Image
import os

ROOT = os.path.join(os.path.dirname(__file__), '..')
DIR = os.path.join(ROOT, 'design', 'stad', 'kooi')

voor = Image.open(os.path.join(DIR, 'voor_hoog.png')).convert('RGBA')
# maten in de plaat van voor_hoog (624x380): paal links 11..56, de regels 46..67 en 343..376, tralies om de 27 px
TOP, BOT = 46, 376
STIJL = (22, 52)          # een strook van de linkerpaal, met het hoekbeslag boven en onder
TRALIES = (60, 60 + 27 * 5 + 6)   # vijf tralies met hun tussenruimte, vanaf net na de paal
sw = STIJL[1] - STIJL[0]
tw = TRALIES[1] - TRALIES[0]
h = BOT - TOP
deur = Image.new('RGBA', (sw * 2 + tw, h), (0, 0, 0, 0))
deur.paste(voor.crop((TRALIES[0], TOP, TRALIES[1], BOT)), (sw, 0))
# de boven- en onderregel lopen door over de hele breedte: neem ze uit het midden van de kooi
for y0, y1 in ((TOP, 68), (340, BOT)):
    strook = voor.crop((200, y0, 200 + sw * 2 + tw, y1))
    deur.alpha_composite(strook, (0, y0 - TOP))
stijl = voor.crop((STIJL[0], TOP, STIJL[1], BOT))
deur.alpha_composite(stijl, (0, 0))
deur.alpha_composite(stijl.transpose(Image.FLIP_LEFT_RIGHT), (sw + tw, 0))
deur.save(os.path.join(DIR, 'deur.png'))
print('deur.png', deur.size)
