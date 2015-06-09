import os
import numpy
from PIL import Image
from downloadHashes import hashImage
from cardHashes import imageToCard
import scipy
import math, operator
import scipy.misc
import pyperclip
import imagehash
import json

def isSameRarity(r1, r2):
    if r1 == r2:
        return True
    a = sorted([r1, r2])
    return a[0] == 'common' and a[1] == 'free'


def callKMScript(cardName, scriptNum):
    pyperclip.copy(cardName)
    scr = """osascript -e 'tell application "Keyboard Maestro Engine" to do script "zzauto draft"'""".replace('draft', 'draft' + str(scriptNum))
    os.system(scr)

os.system("pngpaste 3cards.png")
draftCards = Image.open('3cards.png')
w, h = draftCards.size
draftCards = draftCards.crop((515, 455, 1696, 594+354))
# scipy.misc.imsave('Dtest.png', draftCards)
# exit()

dcw, dch = draftCards.size
cardSize = int(.2948633 * float(dcw))

spacing = (dcw - cardSize*3)/2
firstRarity = None
for i in range(3):
    w, h = draftCards.size
    cardImage = draftCards.crop((0 + (cardSize+spacing)*i, 0, (cardSize+spacing)*i + cardSize, h))

    scipy.misc.imsave('test' + str(i) + '.png', cardImage)

    for cardName, rarity in imageToCard(cardImage):
        if i == 0:
            firstRarity = rarity
            break
        elif isSameRarity(firstRarity, rarity):
            break


    # print cardName, rarity,'\n'
    callKMScript(cardName, i)
