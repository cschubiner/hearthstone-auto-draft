import numpy
from PIL import Image
import json
from downloadHashes import hashImage

hashArr = list()
m = dict()
numToNameDict = dict()
numToRarityDict = dict()
manualHashNums = set()
with open('manual_hashes.json','r') as j:
    cardsJson = json.load(j)
    for cardNum in cardsJson:
        hsh = str(cardsJson[cardNum])
        cardNum = int(cardNum)
        manualHashNums.add(cardNum)
        hashArr.append(hsh)
        m[hsh] = cardNum
with open('cardsWithHashes.json','r') as j:
    cardsJson = json.load(j)
    for c in cardsJson['cards']:
        cardNum = c['id']
        if cardNum not in manualHashNums:
            hsh = c['imageHash']
            hashArr.append(hsh)
            m[hsh] = cardNum
        numToNameDict[cardNum] = c['name']
        numToRarityDict[cardNum] = c['quality']

def imageNumToRarity(iNum):
    return numToRarityDict[iNum]

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

def imageToCard(original):
    hashStr = hashImage(original)

    # print process.extract(hashStr, hashArr)
    # return m[process.extractOne(hashStr, hashArr)[0]]

    with open("output_hashes.txt", "a") as myfile:
        myfile.write(hashStr + '\n')

    scores = list()
    for h in hashArr:
        score = hamming_distance(hashStr, h)
        scores.append((score,h))
    scores = sorted(scores)

    for hashScore, hsh in scores:
        cardNum = m[hsh]
        ret = imageNumToName(cardNum), imageNumToRarity(cardNum)
        print ret
        if cardNum in manualHashNums and hashScore > 7:
            continue
        yield ret

from PIL import Image
import scipy
import scipy.misc
