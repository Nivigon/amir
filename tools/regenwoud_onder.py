#!/usr/bin/env python3
"""Maakt de onderlaag van het regenwoud uit de Grok-plaat in design/regenwoud/bron/.

Bron: onder_grok.jpg, humus met een rij mosbrokken, wortels en botjes (een edit van design/stad/straat_onder.png).
Uit:  design/regenwoud/regenwoud_onder.png, naadloos van links naar rechts en even hoog als de straatlaag (HOOG),
      zodat hij op dezelfde schaal ligt. Het spel tekent hem onder de mosgrond (zie RW_ONDER, rwOnderTeken).

Naadloos: de rechterstrook van OVER px loopt met een lineaire overvloeiing over de linkerstrook, en die strook valt
rechts af. De nieuwe linkerrand is dan precies de kolom die op de nieuwe rechterrand volgt.

    python3 tools/regenwoud_onder.py

Daarna: python3 tools/gen-offline-manifest.py. Vereist Pillow en numpy.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'design', 'regenwoud', 'bron', 'onder_grok.jpg')
UIT = os.path.join(ROOT, 'design', 'regenwoud', 'regenwoud_onder.png')
OVER = 160                        # zo breed (bron-px) is de overvloeiing bij de naad
HOOG = 334                        # de hoogte van design/stad/straat_onder.png

a = np.array(Image.open(BRON).convert('RGB')).astype(float)
h, w, _ = a.shape
t = np.linspace(0, 1, OVER)[None, :, None]           # 0 links: de rechterstrook, 1: de linkerstrook zelf
uit = a[:, :w - OVER].copy()
uit[:, :OVER] = a[:, w - OVER:] * (1 - t) + a[:, :OVER] * t
im = Image.fromarray(uit.round().clip(0, 255).astype(np.uint8))
im = im.resize((round(im.width * HOOG / h), HOOG), Image.LANCZOS)
im.save(UIT, optimize=True)
print('geschreven naar', os.path.relpath(UIT, ROOT), im.size)
