import os, json, numpy as np
from PIL import Image
from scipy import ndimage
MAIN='/home/claude/proef'; OUD='/home/claude/oud/karakters/amir/mkuki'
L=json.load(open(MAIN+'/karakters/amir/mkuki_spel/lijst.json'))
def orig(p):
    for c in [MAIN+'/karakters/amir/'+p, MAIN+'/amir runc/amir_sprites/design/amir/'+p]:
        if os.path.exists(c): return c
def laad(p):
    return np.array(Image.open(orig(p)).convert('RGBA')), np.array(Image.open(OUD+'/'+p).convert('RGBA'))
def buiten(leeg):
    lab,n=ndimage.label(leeg); ids=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    return np.isin(lab,list(ids))
