import vk
import json
import os
import time
import sys
from VKDownloadImage import downloadImage
from Similar import getThumbnails, findSimilarImages

def main():
    """Main entry point for the script."""
    # get access_token to vk api
    session = vk.AuthSession(app_id = '4916113', 
        user_login = 'drew.dru@mail.ru', 
        user_password = '3@lExEx0Rc!$t65', 
        scope = 'photos, wall, groups, offline')
    api = vk.API(session, v='5.53', timeout=999999999)
    print('api is connected')

    # get albums list
    OWNER_ID = '-2481783'
    albums = api.photos.getAlbums(owner_id = OWNER_ID)

    isResume = False
    resumeAlbumID = 23140170

    imgDir = './img/'
    thumbDir = './thumb/'
    thumbnailsSize = 32,32
    imgInfoFile = './imgInfo.json'
    deleteImgDir = './deleteImg/'
    deleteImgInfoFile = './deleteImgInfo.json'

    for index, album in enumerate(albums['items']):    
        if isResume and album['id'] != resumeAlbumID:
            continue
        else:
            isResume = False                    
        #clear directory with images
        try:
            imageList = os.listdir(imgDir)
            for inImage in imageList:
                os.remove(imgDir + inImage)
        except FileNotFoundError:
            pass
        #clear directory with deleteImages
        try:
            imageList = os.listdir(deleteImgDir)
            for inImage in imageList:
                os.remove(deleteImgDir + inImage)
        except FileNotFoundError:
            pass
        #clear directory with Thumbnails
        try:
            imageList = os.listdir(thumbDir)
            for inImage in imageList:
                os.remove(thumbDir + inImage)
        except FileNotFoundError:
            pass
        # remove file with information about the downloaded images
        try:
            os.remove('./imgInfo.json')
        except FileNotFoundError:
            pass
        # remove file with information about the downloaded images to remove
        try:
            os.remove('./deleteImgInfo.json')
        except FileNotFoundError:
            pass
        # remove file with similar images list
        try:
            os.remove('./similarImages.txt')
        except FileNotFoundError:
            pass
        # remove file with images to delete
        try:
            os.remove('./delete.txt')
        except FileNotFoundError:
            pass
        print('removed old files')        
        print(album['id'])

        # get photos list from album['id']
        photos = api.photos.get(owner_id = OWNER_ID, 
            album_id = album['id'], 
            photo_sizes='1')        
        # TODO: save images urls, images hash, and images caption to databases 
        error404List = downloadImage(photos['items'], imgDir, imgInfoFile, isBig = False)
        getThumbnails(imgDir, thumbDir, thumbnailsSize)
        findSimilarImages(thumbDir)

def sortByID(inputStr):
    return int(inputStr.split('.')[0])
    # Example: deleteImageList.sort(key=sortByID)

if __name__ == '__main__':
    sys.exit(main())