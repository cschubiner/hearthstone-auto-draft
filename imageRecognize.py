import os
import numpy
from PIL import Image
from cardNumToName import cardNumToName
import scipy
import math, operator
import scipy.misc
import pyperclip

def imageToNumpy(pic):
    return numpy.asarray(pic)

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    aFloat = imageA.astype("float")
    bFloat = imageB.astype("float")
    err = numpy.sum((aFloat - bFloat) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def getHW(image):
    height = len(image)
    width = len(image[0])
    return (height, width)


def getDistance(image1, image2):
    h1 = image1.histogram()
    h2 = image2.histogram()

    rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return rms


def compare_images(imgA, imgB):
    imageA = imageToNumpy(imgA)
    imageB = imageToNumpy(imgB)
    # compute the mean squared error and structural similarity
    # index for the images
    # print width, height
    resizedA = scipy.misc.imresize(imageA, getHW(imageB))
    # print getHW(imageA)
    # print getHW(resizedA)
    # print getHW(imageB)
    m = mse(resizedA, imageB)

    # m = getDistance(imgA, imgB)

    return m
    # return s-m

def getAllCardImages():
    cardDir = 'cardImages/'
    for f in os.listdir(cardDir):
        if f.endswith(".png"):
            imageNum = int(f.split('.png')[0])
            yield (imageNum, Image.open(cardDir + f))

def getMostSimilarImageNum(original):
    minScore = float('inf')
    ret = None
    i = 0
    for imageNum, cardImage in getAllCardImages():
        w, h = cardImage.size
        cardImage = cardImage.crop((24, 43, w-24, h-12))
        # scipy.misc.imsave('test.png', cardImage)
        # break
        score = compare_images(original, cardImage)
        # print score
        # return imageNum
        if i % 100 == 0:
            # print i
            if ret:
                print 'curr: ' + cardNumToName(ret)
        i += 1
        if score < minScore:
            minScore = score
            ret = imageNum
    return ret

def getMostSimilarCard(original):
    return cardNumToName(getMostSimilarImageNum(original))

# os.system("screencapture screen.png")
# for i in range(4,7):
#     original = Image.open('screen' + str(i) + '.png')
#     print i, getMostSimilarCard(original)

def callKMScript(cardName, scriptNum):
    pyperclip.copy(cardName)
    scr = """osascript -e 'tell application "Keyboard Maestro Engine" to do script "zzauto draft"'""".replace('draft', 'draft' + str(scriptNum))
    os.system(scr)

os.system("pngpaste 3cards.png")
draftCards = Image.open('3cards.png')
dcw, dch = draftCards.size
cardSize = int(.2996633 * float(dcw))
# cardSize = 356
spacing = (dcw - cardSize*3)/2
for i in range(3):
    w, h = draftCards.size
    cardImage = draftCards.crop((0 + (cardSize+spacing)*i, 0, (cardSize+spacing)*i + cardSize, h))
    scipy.misc.imsave('test' + str(i) + '.png', cardImage)

    cardName = getMostSimilarCard(cardImage)
    # callKMScript(cardName, i)

# nikhil's advice. use a neural network trained on several images each. use pig features (prob not needed for neural networks -- they can just take in normal 2D arrays)
