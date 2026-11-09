#!/usr/bin/env python3
"""Knipt de balustrades voor het ingebouwde balkon uit de Grok-plaat design/stad/bron/balkon_grok.png.

De plaat (1792x1008, doorzichtige achtergrond) heeft twee rijen van vier stukken: een brede voorkant en een smalle
zijkant van hetzelfde balkon. We nemen de voorkant links boven en de smalle zijkant rechts boven (die met twee palen),
en daarvan alleen de balustrade: van net boven de bovenste regel tot de vloer. De vloerrand met de balkkoppen en de
palen met het dakje erboven blijven weg: het balkon is ingebouwd, de vloer is de balkenrij van het huis zelf.

Uit: design/stad/balkon_voor.png (de nis in het midden) en design/stad/balkon_zij.png (de hoek).

    python3 tools/balkon_knip.py

Daarna: python3 tools/gen-klein.py en python3 tools/gen-offline-manifest.py
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAD = os.path.join(ROOT, 'design', 'stad')
VEL = os.path.join(STAD, 'bron', 'balkon_grok.png')
# de stukken in de plaat (x0, y0, x1, y1), en de rijen van de balustrade daarin (vanaf de bovenkant van het stuk)
STUKKEN = {'voor': (35, 34, 541, 434), 'zij': (1484, 34, 1748, 436)}
REGEL, VLOER = 200, 353        # net boven de bovenste regel, en de bovenkant van de vloerrand


def main():
    vel = Image.open(VEL).convert('RGBA')
    for naam, (x0, y0, x1, y1) in STUKKEN.items():
        stuk = vel.crop((x0, y0 + REGEL, x1, y0 + VLOER))
        stuk = stuk.crop(stuk.getbbox())
        stuk.save(os.path.join(STAD, f'balkon_{naam}.png'), optimize=True)
        print(f'  balkon_{naam}.png: {stuk.width} x {stuk.height}')


if __name__ == '__main__':
    main()
