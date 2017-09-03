from sqlalchemy import Column, Integer, String
from . import modelsHelper

class Images(modelsHelper.Base):
    __tablename__ = 'images'
    image_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, nullable=False)
    album_id = Column(Integer, nullable=False)
    image_caption = Column(String, nullable=True)
    image_hash = Column(String, nullable=True)

    def insert(self, imagesInfo, image_hash):
        super().open()
        try:  
            image = Images()        
            image.image_id = imagesInfo['id']
            image.owner_id = imagesInfo['owner_id']
            image.album_id = imagesInfo['album_id']
            image.image_caption = imagesInfo['text']
            image.image_hash = image_hash
            self.session.add(image)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
        finally:
            super().close()

    def update(self, imagesInfo):
        super().open()
        try:  
            self.session.query(Images)\
            .filter(Images.image_id == imagesInfo['id'])\
            .update({
                'album_id': imagesInfo['album_id'],
                'image_caption': imagesInfo['text']
            })
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
        finally:
            super().close()

    def checkImgId(self, image_id):
        super().open()
        query = self.session.query(Images)\
            .filter(Images.image_id == image_id)
        value = query.first()
        super().close()
        return value
