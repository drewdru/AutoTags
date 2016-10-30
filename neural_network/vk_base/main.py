# -*- coding: utf-8 -*-
import vk
import json
import os
import time
import sys

try:
    from .VKDownloadImage import saveImageToDB
    from .models import Images
    from . import settings
except Exception:
    from VKDownloadImage import saveImageToDB
    from models import Images
    import settings

def main():
    """Main entry point for the script."""
    # get access_token to vk api
    vkSession = vk.AuthSession(app_id = settings.VK['app_id'], 
        user_login = settings.VK['user_login'], 
        user_password = settings.VK['user_password'], 
        scope = settings.VK['scope']
    )
    api = vk.API(vkSession, v='5.53', timeout=999999999)
    print('api is connected')

    # get albums list
    OWNER_ID = settings.VK['owner_id']
    albums = api.photos.getAlbums(owner_id = OWNER_ID)

    isResume = True
    resumeAlbumID = 49782714

    # imgDir = './img/'
    # thumbDir = './thumb/'
    # thumbnailsSize = 32,32

    # imgInfoFile = './imgInfo.json'
    # deleteImgDir = './deleteImg/'
    # deleteImgInfoFile = './deleteImgInfo.json'

    for album in albums['items']:   
        if isResume and album['id'] != resumeAlbumID:
            continue
        else:
            isResume = False  
        # get photos list from album['id']
        photos = api.photos.get(owner_id = OWNER_ID, 
            album_id = album['id'], 
            photo_sizes='1')   
        print('Album: ', album)
        saveImageToDB(photos['items'], isBig = False)
        
        
        # TODO save data to database
    
    # два изображения -> rmsDiff = rmsDifference , [true if rmsDiff < 1 else false]
    #   !!!!ОБУЧЕНИЕ!!!!!
    #   проверить нейронкой два изображения 
    # pHash: https://habrahabr.ru/post/120562/  расстояния Хэмминга заменить на нейронную сеть

    """
    адаптивная бинаризация -> выделение контуров -> вычисление дескрипторов фурье, сравнение дескрипторов.
    плюсы: не зависит от разрешения, качества сжатия, изменений цветовой палитры, небольших артефактов, можно применять к кропнутым вариантам картинки.
    кроме того, картинки вида «хотеть — не хотеть» будут в различных кластерах.
    при небольшой адаптации может правильно учитывать повернутые изображения.
    минусы: дескрипторы нельзя сравнивать побитно, придется каждый раз считать свертку для всех пар картинок (O(n^2)).
    """
    # Дескриптор фурье:
    #https://cyberleninka.ru/article/n/algoritmicheskoe-i-programmnoe-obespechenie-dlya-raspoznavaniya-figur-s-pomoschyu-furie-deskriptorov-i-neyronnoy-seti

def sortByID(inputStr):
    return int(inputStr.split('.')[0])
    # Example: deleteImageList.sort(key=sortByID)

if __name__ == '__main__':
    sys.exit(main())