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
    session = vk.AuthSession(app_id = 'APP_ID',
        user_login = 'USER_LOGIN', 
        user_password = 'USER_PASS', 
        scope = 'photos, wall, groups, offline')

    api = vk.API(session, v='5.53', timeout=10)
    print('api is connected')  

    # get albums list
    OWNER_ID = 'OWNER_ID'
    albums = api.photos.getAlbums(owner_id = OWNER_ID)

    isResume = False
    resumeAlbumID = 1

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
        
        error404List = downloadImage(photos['items'], imgDir, imgInfoFile, isBig = False)
        count = 0
        textCode = ''
        for error404Image in error404List:
            count += 1
            print('delete 404IMAGE id = ' + str(error404Image))
            # api.photos.delete(owner_id = OWNER_ID, photo_id = error404Image)
            textCode += ('API.photos.delete({"owner_id": "'
                + OWNER_ID
                + '", "photo_id": "'
                + error404Image
                + '"}); ')
            if count%24 == 0:
                api.execute(code=textCode) 
                count = 0
                textCode = ''
                time.sleep(10) 
        if count != 0:
            api.execute(code=textCode) 
            time.sleep(10)


        getThumbnails(imgDir, thumbDir, thumbnailsSize)
        findSimilarImages(thumbDir)

        print('\nDELETE SIMILAR IMAGES!\n')
        try:
            f = open('similarImages.txt','r')
            photoIds = f.read()
            f.close()
            photoList = api.photos.getById(photos = photoIds, photo_sizes = 1)
            error404List = downloadImage(photoList, 
                deleteImgDir, 
                deleteImgInfoFile, 
                isBig = True)        
        except FileNotFoundError:
            pass

        # Save caption
        deleteImageList = os.listdir(deleteImgDir)
        deleteImageList.sort(key=sortByID)
        count = 0    
        textCode = ''
        imgID = ''
        try:
            dImgInfoFile = open(deleteImgInfoFile, 'r')
            # isDImgInfoFileNotNull = True
            # try:                
            imgInfo = json.load(dImgInfoFile)
            dImgInfoFile.close()
            # except ValueError:
            #     dImgInfoFile.close()
            #     isDImgInfoFileNotNull = False
            # if isDImgInfoFileNotNull:
            i = 0            
            while i < len(deleteImageList) - 1:
                originImage = '-1'
                deleteImage = '-1'
                if os.path.getsize(deleteImgDir + deleteImageList[i]) >= os.path.getsize(deleteImgDir + deleteImageList[i + 1]):
                    originImage = deleteImageList[i].split('.')[0]
                    deleteImage = deleteImageList[i + 1].split('.')[0]
                else:                    
                    originImage = deleteImageList[i + 1].split('.')[0]
                    deleteImage = deleteImageList[i].split('.')[0]
                
                # Save caption
                originText = imgInfo['img'][originImage]['text']
                deleteText = imgInfo['img'][deleteImage]['text']
                print('image ' + originImage + ': ' + originText)
                print('image ' + deleteImage + ': ' + deleteText)
                text = ''
                imgID = str(imgInfo['img'][originImage]['id'])
                if originText == '' and deleteText != '':
                    text = deleteText
                elif originText != '' and deleteText != '' and originText.lower() != deleteText.lower():
                    text = originText
                    text += '\n_________\n'
                    text += deleteText
                if text != '': #TODO: use exec method
                    # count += 1
                    # textCode += ('API.photos.edit({"owner_id": "'
                    #     + OWNER_ID
                    #     + '", "photo_id": "'
                    #     + imgID
                    #     + '", "caption": "'
                    #     + text
                    #     + '"}); ')
                    api.photos.edit(owner_id = OWNER_ID, 
                        photo_id = imgInfo['img'][originImage]['id'],
                        caption = text)
                    time.sleep(2)
                    #API.photos.edit({"owner_id": "-2481783", "photo_id": "290500957", "caption": "RavenMorgoth\n_________\nhttp://ravenmorgoth.deviantart.com/art/Vampire-Aristocracy-Salome-Morganti-284078296"}); 
                    #params[code]=API.photos.edit({"owner_id"%3A "-2481783"%2C "photo_id"%3A "290500957"%2C "caption"%3A "RavenMorgoth\n_________\nhttp%3A%2F%2Fravenmorgoth.deviantart.com%2Fart%2FVampire-Aristocracy-Salome-Morganti-284078296"})%3B %0A&params[v]=5.53
                # if count%24 == 0:
                #     api.execute(code=textCode) 
                #     count = 0
                #     textCode = ''
                #     time.sleep(10)             
                # Save deleteImage id
                img1 = str(imgInfo['img'][deleteImage]['id'])
                f = open('delete.txt','a+')
                f.write(img1 + '\n')       
                f.close()     
                i += 2
        except FileNotFoundError:
            pass
        # if count == 1:
        #     api.photos.edit(owner_id = OWNER_ID, 
        #         photo_id = imgID,
        #         caption = text)
        # elif count != 0:
        #     api.execute(code=textCode)
        #     time.sleep(10)        

        #delete images 
        try:
            deletePhotosFile = open('delete.txt','r')      
            count = 0    
            textCode = ''
            for deletePhoto in deletePhotosFile:
                count += 1
                deletePhoto = deletePhoto.rstrip('\n')
                print('https://vk.com/photo'
                    + OWNER_ID
                    + '_' 
                    + deletePhoto)
                textCode += ('API.photos.delete({"owner_id": "'
                    + OWNER_ID
                    + '", "photo_id": "'
                    + deletePhoto
                    + '"}); ')
                #api.photos.delete(owner_id = OWNER_ID, photo_id = deletePhoto)   
                if count%24 == 0:
                    api.execute(code=textCode) 
                    count = 0
                    textCode = ''
                    time.sleep(10) 
            if count != 0:
                api.execute(code=textCode) 
            deletePhotosFile.close() 
            time.sleep(30)
        except FileNotFoundError:
            pass

def sortByID(inputStr):
    return int(inputStr.split('.')[0])

if __name__ == '__main__':
    sys.exit(main())