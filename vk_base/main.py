# -*- coding: utf-8 -*-
import vk
import json
import os
import time
import sys

try:
    from .VKDownloadImage import saveImageToDB
    from .models.images import Images
    from . import settings
except Exception:
    from VKDownloadImage import saveImageToDB
    from models.images import Images
    import settings

def getVkApi():
    """ Get vk api with access_token """
    # get access_token to vk api
    vkSession = vk.AuthSession(app_id=settings.VK['app_id'],
        user_login=settings.VK['user_login'],
        user_password=settings.VK['user_password'],
        scope=settings.VK['scope'])
    print('Connection with vk. Stand by ...')
    vkApi = vk.API(vkSession, v='5.53', timeout=999999999)
    print('VK api is connected')
    return vkApi

def findNewAlbums(albums):
    """ Find new albums 
        :param dict albums: All owners albums
    """
    allAlbums = []
    albumsTypeDir = './albums_type/'
    albumsTypeList = os.listdir(albumsTypeDir)
    for albumsType in albumsTypeList:
        with open(albumsTypeDir + albumsType) as f:
            for line in f:
                allAlbums.append(int(line))
    isFindedNewAlbums = False
    for album in albums:
        if album['id'] not in allAlbums:
            isFindedNewAlbums = True
            print(album['id'])
    return isFindedNewAlbums

def getVkImages(vkApi, albums, OWNER_ID, isResume=False, resumeAlbumID=0):
    for album in albums:   
        if isResume and album['id'] != resumeAlbumID:
            continue
        else:
            isResume = False  
        # get photos list from album['id']
        photos = vkApi.photos.get(owner_id = OWNER_ID, 
            album_id = album['id'], 
            photo_sizes='1')   
        print('Album: ', album)
        saveImageToDB(photos['items'], isBig = False)

def main():
    """ Main entry point for the script """
    OWNER_ID = settings.VK['owner_id']
    vkApi = getVkApi()
    albums = vkApi.photos.getAlbums(owner_id=OWNER_ID)

    if findNewAlbums(albums['items']):
        print('New albums are found, please add them to the database')
        return
    getVkImages(vkApi, albums['items'], OWNER_ID)

# TODO: UPDATE next TODO (Кластеризация изображения, кластеризация объектов на изображениях, классификация)
""" TODO:
адаптивная бинаризация -> выделение контуров -> вычисление дескрипторов фурье, сравнение дескрипторов.
плюсы: не зависит от разрешения, качества сжатия, изменений цветовой палитры, небольших артефактов, можно применять к кропнутым вариантам картинки.
кроме того, картинки вида «хотеть — не хотеть» будут в различных кластерах.
при небольшой адаптации может правильно учитывать повернутые изображения.
минусы: дескрипторы нельзя сравнивать побитно, придется каждый раз считать свертку для всех пар картинок (O(n^2)).
Дескриптор фурье:
https://cyberleninka.ru/article/n/algoritmicheskoe-i-programmnoe-obespechenie-dlya-raspoznavaniya-figur-s-pomoschyu-furie-deskriptorov-i-neyronnoy-seti
"""
def sortByID(inputStr):
    return int(inputStr.split('.')[0])
    # Example: deleteImageList.sort(key=sortByID)

if __name__ == '__main__':
    sys.exit(main())