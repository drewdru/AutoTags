from PIL import Image
import os
import math
import json

def saveURLtoSimilarImages(imgIndx1, imgIndx2):
    ''' Save similar images to similarImages.txt '''   

    imgInfoFile = open('imgInfo.json', 'r')
    imgInfo = json.load(imgInfoFile)  
    imgInfoFile.close()  
    img1 = (str(imgInfo['img'][imgIndx1]['owner_id']) 
        + '_' 
        + str(imgInfo['img'][imgIndx1]['id']))
    img2 = (str(imgInfo['img'][imgIndx2]['owner_id']) 
        + '_' 
        + str(imgInfo['img'][imgIndx2]['id']))
    print('https://vk.com/photo'+img1)
    print('https://vk.com/photo'+img2)
    
    f = open('similarImages.txt','a+')
    f.write(img1 + ',' + img2 + ',\n')
    f.close()

def getThumbnails(imgDir, thumbDir, size):
    ''' Getting thumbnails  '''
    imageList = os.listdir(imgDir)
    for inImage in imageList:
        img = Image.open(imgDir + inImage)
        img.thumbnail(size)
        img = img.convert(mode='L')
        img.save(thumbDir + inImage, "JPEG")

def rmsDifference(img1, img2, size):
    ''' Return a root mean square difference of two images '''
    res = 0 
    for i in range(size[0]):
        for j in range(size[1]):
            try:
                dif = img1[i,j] - img2[i,j]
                res += pow(dif, 2)
            except IndexError:
                break      
    res = math.sqrt( res ) / 256
    return res

def findSimilarImages(imgDir):
    ''' findSimilarImages '''
    imageList = os.listdir(imgDir)
    for index, inImage1 in enumerate(imageList):
        img1 = Image.open(imgDir + inImage1)
        startINDX = index+1
        for index2, inImage2 in enumerate(imageList[startINDX:]):
            img2 = Image.open(imgDir + inImage2)
            rmsDiff = rmsDifference(img1.load(), img2.load(), img1.size)
            if rmsDiff < 1:
                saveURLtoSimilarImages(inImage1.split('.')[0], inImage2.split('.')[0])