import numpy
from PIL import Image
import json
from downloadHashes import hashImage

hashArr = list()
m = dict()
numToNameDict = dict()
with open('cardsWithHashes.json','r') as j:
    cardsJson = json.load(j)
    for c in cardsJson['cards']:
        hashArr.append(c['imageHash'])
        m[c['imageHash']] = c['id']
        numToNameDict[c['id']] = c['name']


def imageNumToName(iNum):
    return numToNameDict[iNum]

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

def compare_images(imgA, imgB):
    imageA = imageToNumpy(imgA)
    imageB = imageToNumpy(imgB)
    # compute the mean squared error and structural similarity
    # index for the images

    resizedA = scipy.misc.imresize(imageA, getHW(imageB))
    m = mse(resizedA, imageB)

    return m



# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

def imageToCardName(original):
    hashStr = hashImage(original)

    # print process.extract(hashStr, hashArr)
    # return m[process.extractOne(hashStr, hashArr)[0]]

    # print hashStr
    scores = list()
    for h in hashArr:
        score = hamming_distance(hashStr, h)
        scores.append((score,h))
    scores = sorted(scores)

    minVal = float('inf')
    cardDir = 'hs-images/'

    # print scores
    minScore = float('inf')
    bestImageNum = None
    firstScore = scores[0][0]
    for hashScore, hsh in scores:
        if hashScore > firstScore * 1.05:
            break
        cardNum = m[hsh]
        cardImage = cardDir + str(cardNum) + '.png'
        score = compare_images(original, Image.open(cardImage))
        if score < minScore:
            minScore = score
            bestImageNum = cardNum

    return imageNumToName(bestImageNum)

from PIL import Image
import scipy
import scipy.misc
