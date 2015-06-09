import os
import numpy
from PIL import Image
from downloadHashes import hashImage
from cardHashes import imageToCardName
import scipy
import math, operator
import scipy.misc
import pyperclip
import imagehash
import time
import json

def callKMScript(cardName, scriptNum):
    pyperclip.copy(cardName)
    scr = """osascript -e 'tell application "Keyboard Maestro Engine" to do script "zzauto draft"'""".replace('draft', 'draft' + str(scriptNum))
    os.system(scr)

os.system("pngpaste 3cards.png")
draftCards = Image.open('3cards.png')
w, h = draftCards.size
draftCards = draftCards.crop((515, 456, 1696, 594+348))
# scipy.misc.imsave('Dtest.png', draftCards)
# exit()

dcw, dch = draftCards.size
cardSize = int(.2948633 * float(dcw))

spacing = (dcw - cardSize*3)/2
for i in range(3):
    w, h = draftCards.size
    cardImage = draftCards.crop((0 + (cardSize+spacing)*i, 0, (cardSize+spacing)*i + cardSize, h))

    scipy.misc.imsave('test' + str(i) + '.png', cardImage)

    cardName = imageToCardName(cardImage)
    print cardName
    callKMScript(cardName, i)
    time.sleep(1)
