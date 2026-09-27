#!/usr/bin/env python3
"""Knapt de run-cycle van de baviaan op: handen en voeten die in de aangeleverde frames zijn
uitgesmeerd tot een halfdoorzichtige vlek, of ontbreken, worden vervangen door schone stukken uit
andere frames van dezelfde reeks, waar dezelfde ledemaat een vergelijkbare stand heeft.

Bron: enemies/baviaan/bron/run/run_00..16.png, precies zoals aangeleverd (niet geladen door het spel,
en niet in de offline-download). Uit: enemies/baviaan/run/. Frames zonder reparatie worden byte voor
byte gekopieerd. Draai het opnieuw als de bron verandert; pas de getallen hieronder aan als je een
plak wilt verschuiven.

Per reparatie: eerst de vlek wegvegen (`wis`: halfdoorzichtige pixels in een kader, alleen waar er
buiten de vlek niets halfdoorzichtigs zit, anders slaat hij gaten in de vacht; `wisalles`: alles in een
veelhoek), dan een stuk uit een donorframe knippen (veelhoek, met een zachte rand), draaien om
een ankerpunt (graden, tegen de klok in op het scherm), eventueel schalen, en het anker op het
aansluitpunt in het doelframe leggen. Tot slot gaan losse puntjes weg die nergens aan vastzitten.
"""
import os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(ROOT, 'enemies/baviaan/bron/run/run_%02d.png')
UIT = os.path.join(ROOT, 'enemies/baviaan/run/run_%02d.png')
N = 17

def laad(i):
    return Image.open(BRON % i).convert('RGBA')

def wis(im, box, alf=250):
    a = np.array(im); x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1]; sub[sub[..., 3] < alf] = 0
    return Image.fromarray(a)

def wisalles(im, poly):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    a = np.array(im); a[np.array(m) > 0] = 0
    return Image.fromarray(a)

def plak(im, donor, poly, anker_d, anker_t, hoek=0, schaal=1.0, zacht=1.2):
    m = Image.new('L', donor.size, 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    if zacht:
        m = m.filter(ImageFilter.GaussianBlur(zacht))
    d = np.array(donor); d[..., 3] = np.minimum(d[..., 3], np.array(m)); stuk = Image.fromarray(d)
    if schaal != 1.0:
        stuk = stuk.resize((round(stuk.width * schaal), round(stuk.height * schaal)), Image.LANCZOS)
        anker_d = (round(anker_d[0] * schaal), round(anker_d[1] * schaal))
    stuk = stuk.rotate(hoek, resample=Image.BICUBIC, center=anker_d)
    laag = Image.new('RGBA', im.size, (0, 0, 0, 0))
    laag.paste(stuk, (anker_t[0] - anker_d[0], anker_t[1] - anker_d[1]), stuk)
    uit = im.copy(); uit.alpha_composite(laag)
    return uit

def puntjes(im, min_px=40):
    """losse stukjes zonder verbinding met het lijf weg (restjes van een weggeveegde vlek)"""
    a = np.array(im); lab, n = ndimage.label(a[..., 3] > 0, structure=np.ones((3, 3)))
    if n > 1:
        grootte = ndimage.sum(np.ones(lab.shape), lab, range(1, n + 1))
        weg = np.isin(lab, [k + 1 for k, g in enumerate(grootte) if g < min_px])
        a[weg] = 0
    return Image.fromarray(a)

# de achterpoot van run_02 (scherp, in dezelfde achteruit trappende stand)
POOT = [(700, 495), (772, 495), (778, 568), (696, 568)]
POOT_ANKER = (738, 500)

def run00():
    x = wis(laad(0), (20, 380, 120, 470))
    x = wisalles(x, [(20, 400), (80, 400), (100, 470), (20, 470)])
    x = plak(x, laad(15), [(60, 330), (130, 330), (135, 360), (125, 405), (60, 405)], (100, 360), (100, 403))
    x = wisalles(x, [(640, 486), (672, 470), (720, 462), (720, 540), (640, 540)])
    return plak(x, laad(2), POOT, POOT_ANKER, (664, 474), -25, 0.7)

def run01():
    x = wis(laad(1), (0, 430, 50, 500))
    x = plak(x, laad(2), [(14, 478), (62, 474), (70, 490), (64, 530), (14, 530)], (64, 488), (47, 441), -4, zacht=1.5)
    x = wisalles(x, [(668, 518), (714, 518), (714, 565), (668, 565)])
    return plak(x, laad(2), POOT, POOT_ANKER, (692, 514), 0, 0.8)

def run12():
    x = wisalles(laad(12), [(240, 345), (290, 343), (298, 362), (268, 430), (240, 430)])
    return plak(x, laad(13), [(194, 384), (230, 380), (256, 408), (256, 466), (192, 466)], (212, 390), (284, 346), -32)

def run16():
    d15 = laad(15)
    x = wis(laad(16), (30, 340, 160, 430))
    x = wisalles(x, [(30, 378), (70, 378), (70, 400), (30, 400)])
    x = plak(x, d15, [(62, 352), (112, 352), (128, 368), (128, 400), (62, 410)], (125, 378), (90, 374), -22, zacht=1.5)
    x = plak(x, d15, [(170, 402), (212, 398), (214, 455), (168, 455)], (205, 410), (134, 396), -10, zacht=1.5)
    x = wisalles(x, [(588, 464), (640, 454), (668, 452), (672, 498), (588, 498)])
    return plak(x, laad(2), POOT, POOT_ANKER, (634, 456), -25, 0.7)

REPARATIES = {0: run00, 1: run01, 12: run12, 16: run16}

def main():
    os.makedirs(os.path.dirname(UIT), exist_ok=True)
    for i in range(N):
        if i in REPARATIES:
            puntjes(REPARATIES[i]()).save(UIT % i, optimize=True)
            print('gerepareerd', os.path.relpath(UIT % i, ROOT))
        else:
            shutil.copyfile(BRON % i, UIT % i)

if __name__ == '__main__':
    main()
