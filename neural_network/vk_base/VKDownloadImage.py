import json
import urllib
import sys
import urllib

from PIL import Image
import requests
from io import BytesIO

try:
    from .Similar import getImageHash
    from . import models
except Exception:
    from Similar import getImageHash
    import models

def saveImageToDB(images_info, isBig = True):
    ''' Download images from vk.com 
        return images which not found in vk servers
    '''    
    size = -1 if isBig else 0
    
    for image_info in images_info:
        try:
            response = requests.get(image_info['sizes'][size]['src'])
            img = Image.open(BytesIO(response.content))    
            img = img.convert(mode='RGB') 
            img_hash = getImageHash(img)
            models.Images().insert(image_info, img_hash)            
        except urllib.error.HTTPError as err:
            print(err)
            print('https://vk.com/photo-2481783_' + str(image_info['id']))
        except Exception as err:
            print(err)
            print('https://vk.com/photo-2481783_' + str(image_info['id']))
