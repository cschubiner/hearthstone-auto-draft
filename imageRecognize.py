import os
import numpy
from PIL import Image
from cardNumToName import cardNumToName
from cardHashes import hashToCardNum
import scipy
import math, operator
import scipy.misc
import pyperclip
import imagehash
import time

def getAllCardImages():
    cardDir = 'cardImages/'
    for f in os.listdir(cardDir):
        if f.endswith(".png"):
            imageNum = int(f.split('.png')[0])
            yield (imageNum, Image.open(cardDir + f))

def imageToNumpy(pic):
    return numpy.asarray(pic)

def getHW(image):
    height = len(image)
    width = len(image[0])
    return (height, width)

def getMostSimilarImageNum(original):
    hashStr = imagehash.phash(original, 64)

    return hashToCardNum(hashStr)

def getMostSimilarCard(original):
    return cardNumToName(getMostSimilarImageNum(original))

def callKMScript(cardName, scriptNum):
    pyperclip.copy(cardName)
    scr = """osascript -e 'tell application "Keyboard Maestro Engine" to do script "zzauto draft"'""".replace('draft', 'draft' + str(scriptNum))
    os.system(scr)

os.system("pngpaste 3cards.png")
draftCards = Image.open('3cards.png')
w, h = draftCards.size
draftCards = draftCards.crop((510, 456, 1696, 594+348))
# scipy.misc.imsave('Dtest.png', draftCards)
# exit()

dcw, dch = draftCards.size
cardSize = int(.2996633 * float(dcw))

spacing = (dcw - cardSize*3)/2
for i in range(3):
    w, h = draftCards.size
    cardImage = draftCards.crop((0 + (cardSize+spacing)*i, 0, (cardSize+spacing)*i + cardSize, h))
    # cardImage = cardImage.resize((238, 340), Image.ANTIALIAS)

    scipy.misc.imsave('test' + str(i) + '.png', cardImage)

    cardName = getMostSimilarCard(cardImage)
    print cardName
    callKMScript(cardName, i)
    # time.sleep(1)
