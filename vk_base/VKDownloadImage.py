import json
import urllib
import sys
import urllib

from PIL import Image
import requests
from io import BytesIO

try:
    from .Similar import getImageHash
    from models.images import Images
except Exception:
    from Similar import getImageHash
    from models.images import Images

def saveImageToDB(imagesInfo, isBig = True):
    ''' Download images from vk.com 
        return images which not found in vk servers
    '''    
    size = -1 if isBig else 0

    for imagesInfo in imagesInfo:
        try:
            if Images().checkImgId(imagesInfo['id']):
                Images().update(imagesInfo)
            else:
                response = requests.get(imagesInfo['sizes'][size]['src'])
                img = Image.open(BytesIO(response.content))
                img = img.convert(mode='RGB')
                img_hash = getImageHash(img)
                Images().insert(imagesInfo, img_hash)            
        except urllib.error.HTTPError as err:
            print(err)
            print('https://vk.com/photo-2481783_' + str(imagesInfo['id']))
        except Exception as err:
            print(err)
            print('https://vk.com/photo-2481783_' + str(imagesInfo['id']))
