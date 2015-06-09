import imagehash

def locForImageNum(iNum):
    cardDir = 'hs-images/'
    return cardDir + str(iNum) + '.png'

def hashImage(image):
    h = str(imagehash.dhash(image, 16)) + str(imagehash.phash(image, 16))
    return h


if __name__ == "__main__":
    import urllib
    import json
    from PIL import Image
    urllib.urlretrieve ("https://raw.githubusercontent.com/pdyck/hearthstone-db/master/cards/all-collectibles.json", "all-collectibles.json")
    with open('all-collectibles.json','r') as f:
        cardsJson = json.load(f)
        fOut = open('cardsWithHashes.json','w')
        for c in cardsJson['cards']:
            iNum, name = c['id'], c['name']
            cardImage = Image.open(locForImageNum(iNum))
            w, h = cardImage.size
            cardImage = cardImage.crop((24, 43, w-24, h-12))
            c['imageHash'] = hashImage(cardImage)
        json.dump(cardsJson, fOut)
