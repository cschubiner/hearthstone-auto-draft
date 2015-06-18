cardNum = 1
cardName = 'zombie chow'

import json

hsh = None
with open("output_hashes.txt", "r") as myfile:
    hsh = myfile.readlines()[-(4-cardNum)].strip()

manualHashes = None
with open('manual_hashes.json','r') as j:
    manualHashes = json.load(j)

cardNames = list()
cardsJson = None
with open('cardsWithHashes.json','r') as j:
    cardsJson = json.load(j)

for c in cardsJson['cards']:
    cardNames.append(c['name'])

from fuzzywuzzy import process
cardName = process.extractOne(cardName, cardNames)[0]

cardNum = None
for c in cardsJson['cards']:
    if c['name'] == cardName:
        cardNum = c['id']
        break

manualHashes[cardNum] = hsh
with open('manual_hashes.json','w') as j:
    json.dump(manualHashes, j)
