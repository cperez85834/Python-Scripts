#The purpose of this script is to automatically download all comics (up to the number specified
# in "numOfComics") into a folder of my choosing. It uses beautiful soup to
# parse the website and get the image element of each comic, then sends a request
# to download the image and puts it in a folder. If an error occurs, it tells you
# what comic caused it and continues to the next one

import requests, bs4, pyperclip, traceback, re

baseAddress = 'https://xkcd.com/'
folderToSave = 'C:\\Users\\Broccoli\\Documents\\python\\L1\\xkcd comics\\'
numOfComics = 2349

#The comics start at one and end at numOfComics, but the range function
#doesn't include the last number of the range specified so I need to add one to it
for i in range(1, numOfComics + 1):
    res = requests.get(baseAddress + str(i))
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    imageElem = soup.select('#comic > img:nth-child(1)')

    #Exception handling in case a comic couldn't be downloaded
    try:
        imageRes = requests.get(r'https:' + imageElem[0].get('src'))

    except:
        print('Couldn\'t download comic # ' + str(i) + '!')
        continue
    
    comicName = imageElem[0].get('title')

    #Handle to the image file to be created
    comicHandle = open(folderToSave + str(i) + '.jpg', 'wb')

    #gets the data chucks of the file and stores them in the comicHandle
    for chunk in imageRes.iter_content(100000):
        comicHandle.write(chunk)

    comicHandle.close()
    print(imageElem[0].get('src'))
