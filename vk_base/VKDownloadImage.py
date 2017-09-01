import json
import urllib
import sys
def downloadImage(images, imgDir, imgInfoFile, isBig = True):
    ''' Download images from vk.com 
        return images which not found in vk servers
    '''    
    size = -1 if isBig else 0
    imgInfo = {
        'img': {
            
        }
    }
    error404List = []
    for index, image in enumerate(images):
        try:
            u = urllib.request.urlopen(image['sizes'][size]['src'])
            raw_data = u.read()
            u.close()
            f = open(imgDir + str(index) + '.jpg','wb+')
            f.write(raw_data)
            f.close()
            imgInfo['img'][index] = {
                'id': image['id'],
                'owner_id': image['owner_id'],
                'album_id': image['album_id'],
                'text': image['text']
            }
        except urllib.error.HTTPError as err:
            print('https://vk.com/photo-2481783_' + str(image['id']))
            error404List.append(str(image['id']))
        except Exception as err:
            print('https://vk.com/photo-2481783_' + str(image['id']))
            sys.exit(err)

    outfile = open(imgInfoFile, 'w')
    json.dump(imgInfo, outfile, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    outfile.close()

    return error404List