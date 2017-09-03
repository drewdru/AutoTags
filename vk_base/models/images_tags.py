from sqlalchemy import Column, Integer, String, ForeignKey
from . import modelsHelper

class ImagesTags(modelsHelper.Base):
    __tablename__ = 'images_tags'
    images_tags_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('images.image_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.tags_id'), nullable=False)
