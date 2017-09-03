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
    ''' Getting thumbnails for all image in directory '''
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

def DCT(img, size):
    ''' 
        get: image, width=size[0], height=size[1]
        return: upper left 8x8 block of DCTMatrix
    '''

    DCTMatrix = [[0 for x in range(size[0])] for y in range(size[1])] 
    for u in range(size[0]):
        for v in range(size[1]):
            for i in range(size[0]):
                for j in range(size[1]):
                    r, g, b = img.getpixel((i, j))
                    S = (r + g + b) // 3
                    val1 = math.pi/size[0]*(i+1./2.)*u
                    val2 = math.pi/size[1]*(j+1./2.)*v
                    DCTMatrix[u][v] += S * math.cos(val1) * math.cos(val2)
    
    matrix = [[0 for x in range(8)] for y in range(8)] 
    for i in range(8):
        for j in range(8):
            matrix[i][j] = DCTMatrix[i][j]
    return matrix

# pHash https://habrahabr.ru/post/120562/
def getImageHash(img):
    ''' return: 64-bit hash string '''

    size = 32, 32
    img = img.resize(size, Image.ANTIALIAS)
    matrix = DCT(img, size)
    average = 0
    for i in range(8):
        for j in range(8):
            if i == 0 and j == 0:
                continue
            average += matrix[i][j]
    average = average / 63

    hashString = ''
    for i in range(8):
        for j in range(8):
            if matrix[i][j] >= average:
                hashString += '1'
            else:
                hashString += '0'
    return hashString
